"""User synchronization service between Auth0 and local database."""
import secrets
from datetime import datetime, timezone
from typing import Any
import httpx
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.config import settings
from app.models import Auth0User
from app.auth0_client import auth0_client
from app.schemas import Auth0UserInfo


class UserSyncService:
    """Service for synchronizing users between Auth0 and local database."""

    def __init__(self):
        self.user_service_url = settings.user_service_url
        self.billing_service_url = settings.billing_service_url
        self.entitlements_service_url = settings.entitlements_service_url

    async def sync_auth0_user(
        self,
        db: Session,
        auth0_sub: str,
        email: str,
        auth0_user_info: Auth0UserInfo | None = None,
    ) -> Auth0User:
        """
        Synchronize an Auth0 user with local database.

        If user doesn't exist locally:
        1. Create user in user_service
        2. Assign default plan in billing_service
        3. Create Auth0User mapping
        4. Update Auth0 app_metadata with customer_id

        If user exists:
        1. Update Auth0User mapping
        2. Update last_login timestamp
        """
        # Check if mapping already exists
        auth0_user = db.query(Auth0User).filter(Auth0User.auth0_sub == auth0_sub).first()

        if auth0_user:
            # Update existing mapping
            auth0_user.last_login = datetime.now(timezone.utc)
            auth0_user.login_count += 1

            if auth0_user_info:
                auth0_user.email = auth0_user_info.email
                auth0_user.email_verified = auth0_user_info.email_verified
                auth0_user.name = auth0_user_info.name
                auth0_user.nickname = auth0_user_info.nickname
                auth0_user.picture = auth0_user_info.picture

            db.commit()
            db.refresh(auth0_user)
            return auth0_user

        # Fetch full user info from Auth0 if not provided
        if not auth0_user_info:
            auth0_user_info = await auth0_client.get_user_info(auth0_sub)

        # Create local user
        local_user_id = await self._create_local_user(
            email=auth0_user_info.email,
            name=auth0_user_info.name,
            email_verified=auth0_user_info.email_verified,
        )

        # Assign default plan
        await self._assign_default_plan(local_user_id)

        # Create Auth0User mapping
        auth0_user = Auth0User(
            auth0_sub=auth0_sub,
            local_user_id=local_user_id,
            email=auth0_user_info.email,
            email_verified=auth0_user_info.email_verified,
            name=auth0_user_info.name,
            nickname=auth0_user_info.nickname,
            picture=auth0_user_info.picture,
            auth0_created_at=self._parse_auth0_timestamp(auth0_user_info.created_at),
            last_login=datetime.now(timezone.utc),
            login_count=1,
        )
        db.add(auth0_user)
        db.commit()
        db.refresh(auth0_user)

        # Update Auth0 app_metadata with customer_id and plan
        await auth0_client.update_user_metadata(
            auth0_sub=auth0_sub,
            app_metadata={
                "customer_id": local_user_id,
                "plan_code": settings.default_plan_code,
            },
        )

        return auth0_user

    async def _create_local_user(
        self,
        email: str,
        name: str | None,
        email_verified: bool = False,
    ) -> int:
        """Create user in local user_service."""
        # Parse name into first/last
        first_name, last_name = None, None
        if name:
            parts = name.split(" ", 1)
            first_name = parts[0]
            last_name = parts[1] if len(parts) > 1 else None

        payload = {
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "is_active": email_verified,  # Only activate if email verified
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.user_service_url}/users/register",
                    json=payload,
                    timeout=10.0,
                )
                response.raise_for_status()
                user_data = response.json()
                return user_data["id"]

        except httpx.HTTPStatusError as e:
            if e.response.status_code == 409:
                # User already exists, fetch ID
                return await self._get_user_id_by_email(email)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to create user: {str(e)}"
            ) from e
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Unexpected error creating user: {str(e)}"
            ) from e

    async def _get_user_id_by_email(self, email: str) -> int:
        """Get local user ID by email."""
        try:
            async with httpx.AsyncClient() as client:
                # This endpoint should exist in user_service or we query directly
                response = await client.get(
                    f"{self.user_service_url}/users",
                    params={"email": email},
                    timeout=10.0,
                )
                response.raise_for_status()
                users = response.json()
                if users and len(users) > 0:
                    return users[0]["id"]
                raise ValueError(f"User not found: {email}")
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to fetch user by email: {str(e)}"
            ) from e

    async def _assign_default_plan(self, customer_id: int) -> None:
        """Assign default plan to new user."""
        payload = {
            "customer_id": str(customer_id),
            "plan_code": settings.default_plan_code,
            "trial_period_days": settings.default_plan_trial_days,
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.billing_service_url}/billing/subscriptions",
                    json=payload,
                    timeout=10.0,
                )
                response.raise_for_status()
        except httpx.HTTPStatusError as e:
            # Log error but don't fail user creation
            print(f"Warning: Failed to assign default plan: {e}")
        except Exception as e:
            print(f"Warning: Unexpected error assigning plan: {e}")

    def _parse_auth0_timestamp(self, timestamp: str | None) -> datetime | None:
        """Parse Auth0 timestamp string to datetime."""
        if not timestamp:
            return None
        try:
            return datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
        except Exception:
            return None

    async def get_user_entitlements(self, customer_id: int) -> dict[str, Any]:
        """Fetch user entitlements from entitlements service."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.entitlements_service_url}/entitlements/{customer_id}",
                    timeout=5.0,
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            print(f"Warning: Failed to fetch entitlements: {e}")
            # Return default empty entitlements
            return {
                "customer_id": str(customer_id),
                "capabilities": {},
                "quotas": {},
            }


# Singleton instance
user_sync_service = UserSyncService()
