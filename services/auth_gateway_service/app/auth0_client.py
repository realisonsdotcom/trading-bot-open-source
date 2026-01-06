"""Auth0 client for token validation and user management."""
import time
from typing import Any
import httpx
from jose import jwt, JWTError
from jose.backends.cryptography_backend import CryptographyRSAKey
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from fastapi import HTTPException, status

from app.config import settings
from app.schemas import Auth0TokenPayload, Auth0UserInfo


class Auth0Client:
    """Client for Auth0 API interactions."""

    def __init__(self):
        self.domain = settings.auth0_domain
        self.client_id = settings.auth0_client_id
        self.client_secret = settings.auth0_client_secret
        self.audience = settings.auth0_audience
        self.issuer = settings.auth0_issuer
        self.jwks_url = settings.auth0_jwks_url

        # Management API
        self.mgmt_client_id = settings.auth0_management_client_id
        self.mgmt_client_secret = settings.auth0_management_client_secret
        self.mgmt_api_url = settings.auth0_management_api_url
        self.mgmt_audience = settings.auth0_management_audience or f"https://{self.domain}/api/v2/"

        # Cache for JWKS keys
        self._jwks_cache: dict[str, Any] = {}
        self._jwks_cache_time: float = 0
        self._jwks_cache_ttl: int = 3600  # 1 hour

        # Management API token cache
        self._mgmt_token: str | None = None
        self._mgmt_token_expires: float = 0

    async def get_jwks(self) -> dict[str, Any]:
        """Fetch JWKS from Auth0 with caching."""
        now = time.time()
        if self._jwks_cache and (now - self._jwks_cache_time) < self._jwks_cache_ttl:
            return self._jwks_cache

        async with httpx.AsyncClient() as client:
            response = await client.get(self.jwks_url)
            response.raise_for_status()
            jwks = response.json()

        self._jwks_cache = jwks
        self._jwks_cache_time = now
        return jwks

    async def get_signing_key(self, token: str) -> CryptographyRSAKey:
        """Get signing key for token validation."""
        # Decode header to get kid
        try:
            unverified_header = jwt.get_unverified_header(token)
        except JWTError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid token header: {str(e)}"
            ) from e

        kid = unverified_header.get("kid")
        if not kid:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token header missing 'kid'"
            )

        # Fetch JWKS and find matching key
        jwks = await self.get_jwks()
        keys = jwks.get("keys", [])

        rsa_key = None
        for key in keys:
            if key.get("kid") == kid:
                rsa_key = key
                break

        if not rsa_key:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Unable to find signing key for kid: {kid}"
            )

        # Convert JWK to PEM
        try:
            from jose.backends.cryptography_backend import CryptographyRSAKey
            return CryptographyRSAKey(rsa_key, algorithm="RS256")
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Failed to create signing key: {str(e)}"
            ) from e

    async def validate_token(self, token: str) -> Auth0TokenPayload:
        """Validate Auth0 JWT token."""
        try:
            # Get signing key
            signing_key = await self.get_signing_key(token)

            # Decode and validate token
            payload = jwt.decode(
                token,
                signing_key,
                algorithms=["RS256"],
                audience=self.audience,
                issuer=self.issuer,
            )

            return Auth0TokenPayload(**payload)

        except JWTError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Token validation failed: {str(e)}"
            ) from e
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Unexpected error validating token: {str(e)}"
            ) from e

    async def get_management_token(self) -> str:
        """Get Auth0 Management API token with caching."""
        now = time.time()
        if self._mgmt_token and now < self._mgmt_token_expires:
            return self._mgmt_token

        # Request new token
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"https://{self.domain}/oauth/token",
                json={
                    "client_id": self.mgmt_client_id,
                    "client_secret": self.mgmt_client_secret,
                    "audience": self.mgmt_audience,
                    "grant_type": "client_credentials",
                },
            )
            response.raise_for_status()
            data = response.json()

        self._mgmt_token = data["access_token"]
        # Set expiry with 5-minute buffer
        self._mgmt_token_expires = now + data.get("expires_in", 86400) - 300

        return self._mgmt_token

    async def get_user_info(self, auth0_sub: str) -> Auth0UserInfo:
        """Fetch user info from Auth0 Management API."""
        token = await self.get_management_token()

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.mgmt_api_url}/users/{auth0_sub}",
                headers={"Authorization": f"Bearer {token}"},
            )
            response.raise_for_status()
            user_data = response.json()

        return Auth0UserInfo(**user_data)

    async def update_user_metadata(
        self,
        auth0_sub: str,
        app_metadata: dict[str, Any] | None = None,
        user_metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Update user metadata in Auth0."""
        token = await self.get_management_token()

        payload = {}
        if app_metadata is not None:
            payload["app_metadata"] = app_metadata
        if user_metadata is not None:
            payload["user_metadata"] = user_metadata

        async with httpx.AsyncClient() as client:
            response = await client.patch(
                f"{self.mgmt_api_url}/users/{auth0_sub}",
                headers={"Authorization": f"Bearer {token}"},
                json=payload,
            )
            response.raise_for_status()
            return response.json()

    async def create_user(
        self,
        email: str,
        password: str | None = None,
        email_verified: bool = False,
        app_metadata: dict[str, Any] | None = None,
        user_metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Create a new user in Auth0."""
        token = await self.get_management_token()

        payload: dict[str, Any] = {
            "connection": "Username-Password-Authentication",
            "email": email,
            "email_verified": email_verified,
        }

        if password:
            payload["password"] = password

        if app_metadata:
            payload["app_metadata"] = app_metadata

        if user_metadata:
            payload["user_metadata"] = user_metadata

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.mgmt_api_url}/users",
                headers={"Authorization": f"Bearer {token}"},
                json=payload,
            )

            if response.status_code == 409:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="User with this email already exists"
                )

            response.raise_for_status()
            return response.json()

    async def assign_roles(self, auth0_sub: str, role_ids: list[str]) -> None:
        """Assign roles to a user in Auth0."""
        token = await self.get_management_token()

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.mgmt_api_url}/users/{auth0_sub}/roles",
                headers={"Authorization": f"Bearer {token}"},
                json={"roles": role_ids},
            )
            response.raise_for_status()

    async def exchange_code_for_tokens(self, code: str, redirect_uri: str) -> dict[str, Any]:
        """Exchange authorization code for tokens."""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"https://{self.domain}/oauth/token",
                json={
                    "grant_type": "authorization_code",
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "code": code,
                    "redirect_uri": redirect_uri,
                },
            )
            response.raise_for_status()
            return response.json()


# Singleton instance
auth0_client = Auth0Client()
