"""Auth Gateway Service - Main application."""
import secrets
from datetime import datetime, timezone, timedelta
from fastapi import FastAPI, Depends, HTTPException, status, Request, Response, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.models import Auth0User, UserSession
from app.schemas import (
    LoginCallbackRequest,
    LogoutRequest,
    UserSessionResponse,
    HealthResponse,
    ErrorResponse,
)
from app.auth0_client import auth0_client
from app.user_sync import user_sync_service

# Create FastAPI app
app = FastAPI(
    title="Auth Gateway Service",
    description="Authentication gateway integrating Auth0 with trading bot services",
    version="1.0.0",
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ===== Health Check =====

@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return HealthResponse(service="auth_gateway_service")


# ===== Auth Endpoints =====

@app.get("/auth/login", tags=["Authentication"])
async def login_redirect():
    """
    Redirect to Auth0 login page.
    This is the entry point for user authentication.
    """
    auth_url = (
        f"https://{settings.auth0_domain}/authorize?"
        f"response_type=code&"
        f"client_id={settings.auth0_client_id}&"
        f"redirect_uri={settings.auth0_callback_url}&"
        f"scope=openid profile email&"
        f"audience={settings.auth0_audience}"
    )
    return RedirectResponse(url=auth_url)


@app.post("/auth/callback", response_model=UserSessionResponse, tags=["Authentication"])
@app.get("/auth/callback", response_model=UserSessionResponse, tags=["Authentication"])
async def auth_callback(
    code: str,
    state: str | None = None,
    response: Response = None,
    db: Session = Depends(get_db),
):
    """
    Handle Auth0 callback after successful authentication.

    Flow:
    1. Exchange authorization code for tokens
    2. Validate access token
    3. Sync user with local database
    4. Fetch user entitlements
    5. Create session
    6. Return session info
    """
    try:
        # Exchange code for tokens
        tokens = await auth0_client.exchange_code_for_tokens(
            code=code,
            redirect_uri=settings.auth0_callback_url,
        )

        access_token = tokens["access_token"]
        id_token = tokens.get("id_token")

        # Validate and decode access token
        payload = await auth0_client.validate_token(access_token)

        # Sync user with local database
        auth0_user = await user_sync_service.sync_auth0_user(
            db=db,
            auth0_sub=payload.sub,
            email=payload.sub.split("|")[1] if "|" in payload.sub else payload.sub,  # Fallback
        )

        # Fetch entitlements
        entitlements = await user_sync_service.get_user_entitlements(auth0_user.local_user_id)

        # Create session
        session_id = secrets.token_urlsafe(32)
        expires_at = datetime.now(timezone.utc) + timedelta(seconds=settings.session_max_age)

        user_session = UserSession(
            session_id=session_id,
            local_user_id=auth0_user.local_user_id,
            auth0_sub=payload.sub,
            access_token_jti=payload.sub,  # Use sub as identifier
            expires_at=expires_at,
        )
        db.add(user_session)
        db.commit()

        # Set session cookie
        response.set_cookie(
            key=settings.session_cookie_name,
            value=session_id,
            max_age=settings.session_max_age,
            secure=settings.session_cookie_secure,
            httponly=settings.session_cookie_httponly,
            samesite=settings.session_cookie_samesite,
        )

        # Build response
        return UserSessionResponse(
            session_id=session_id,
            user_id=auth0_user.local_user_id,
            email=auth0_user.email,
            name=auth0_user.name,
            picture=auth0_user.picture,
            plan_code=payload.plan_code,
            roles=payload.roles or [],
            expires_at=expires_at,
            capabilities=entitlements.get("capabilities", {}),
            quotas=entitlements.get("quotas", {}),
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Authentication failed: {str(e)}"
        ) from e


@app.get("/auth/session", response_model=UserSessionResponse, tags=["Authentication"])
async def get_session(
    request: Request,
    db: Session = Depends(get_db),
):
    """
    Get current session information.
    Validates session cookie and returns user info with entitlements.
    """
    # Get session ID from cookie
    session_id = request.cookies.get(settings.session_cookie_name)
    if not session_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No active session"
        )

    # Fetch session from database
    user_session = db.query(UserSession).filter(
        UserSession.session_id == session_id,
        UserSession.revoked_at.is_(None),
        UserSession.expires_at > datetime.now(timezone.utc),
    ).first()

    if not user_session:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired session"
        )

    # Update last activity
    user_session.last_activity = datetime.now(timezone.utc)
    db.commit()

    # Fetch Auth0 user mapping
    auth0_user = db.query(Auth0User).filter(
        Auth0User.local_user_id == user_session.local_user_id
    ).first()

    if not auth0_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User mapping not found"
        )

    # Fetch entitlements
    entitlements = await user_sync_service.get_user_entitlements(auth0_user.local_user_id)

    # TODO: Fetch plan_code and roles from Auth0 or cache
    return UserSessionResponse(
        session_id=session_id,
        user_id=auth0_user.local_user_id,
        email=auth0_user.email,
        name=auth0_user.name,
        picture=auth0_user.picture,
        plan_code=None,  # TODO: Get from entitlements or Auth0
        roles=[],  # TODO: Get from Auth0 token
        expires_at=user_session.expires_at,
        capabilities=entitlements.get("capabilities", {}),
        quotas=entitlements.get("quotas", {}),
    )


@app.post("/auth/logout", tags=["Authentication"])
async def logout(
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    """
    Logout user by revoking session.
    """
    # Get session ID from cookie
    session_id = request.cookies.get(settings.session_cookie_name)

    if session_id:
        # Revoke session in database
        user_session = db.query(UserSession).filter(
            UserSession.session_id == session_id
        ).first()

        if user_session:
            user_session.revoked_at = datetime.now(timezone.utc)
            db.commit()

    # Clear session cookie
    response.delete_cookie(
        key=settings.session_cookie_name,
        secure=settings.session_cookie_secure,
        httponly=settings.session_cookie_httponly,
        samesite=settings.session_cookie_samesite,
    )

    # Build Auth0 logout URL
    logout_url = (
        f"https://{settings.auth0_domain}/v2/logout?"
        f"client_id={settings.auth0_client_id}&"
        f"returnTo={settings.auth0_logout_url}"
    )

    return {
        "message": "Logged out successfully",
        "logout_url": logout_url,
    }


@app.post("/auth/validate", tags=["Authentication"])
async def validate_token(
    authorization: str = Header(..., description="Bearer token"),
    db: Session = Depends(get_db),
):
    """
    Validate Auth0 access token (for service-to-service auth).
    Returns decoded token payload with user info.
    """
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header"
        )

    token = authorization[7:]  # Remove "Bearer " prefix

    try:
        # Validate token
        payload = await auth0_client.validate_token(token)

        # Fetch Auth0 user mapping
        auth0_user = db.query(Auth0User).filter(
            Auth0User.auth0_sub == payload.sub
        ).first()

        if not auth0_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found locally"
            )

        # Return payload with local user_id
        return {
            "valid": True,
            "auth0_sub": payload.sub,
            "local_user_id": auth0_user.local_user_id,
            "email": auth0_user.email,
            "roles": payload.roles or [],
            "plan_code": payload.plan_code,
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token validation failed: {str(e)}"
        ) from e


# ===== User Info Endpoint =====

@app.get("/auth/user", tags=["User"])
async def get_current_user(
    request: Request,
    db: Session = Depends(get_db),
):
    """
    Get current authenticated user information.
    Requires valid session cookie.
    """
    # Get session ID from cookie
    session_id = request.cookies.get(settings.session_cookie_name)
    if not session_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )

    # Fetch session
    user_session = db.query(UserSession).filter(
        UserSession.session_id == session_id,
        UserSession.revoked_at.is_(None),
        UserSession.expires_at > datetime.now(timezone.utc),
    ).first()

    if not user_session:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid session"
        )

    # Fetch user info
    auth0_user = db.query(Auth0User).filter(
        Auth0User.local_user_id == user_session.local_user_id
    ).first()

    if not auth0_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return {
        "id": auth0_user.local_user_id,
        "email": auth0_user.email,
        "name": auth0_user.name,
        "picture": auth0_user.picture,
        "email_verified": auth0_user.email_verified,
        "last_login": auth0_user.last_login,
        "login_count": auth0_user.login_count,
    }


# ===== Error Handlers =====

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error=exc.detail,
            code=f"HTTP_{exc.status_code}"
        ).model_dump()
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    """Handle unexpected exceptions."""
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="Internal server error",
            detail=str(exc) if settings.debug else None,
            code="INTERNAL_ERROR"
        ).model_dump()
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=settings.debug)
