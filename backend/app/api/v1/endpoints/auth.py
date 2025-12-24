from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
from starlette.requests import Request
from starlette.responses import RedirectResponse
import httpx

from ....core.database import get_db
from ....core.security import verify_password, get_password_hash, create_access_token, decode_access_token
from ....core.config import settings
from ....domain.user.models import User
from ....domain.user.schemas import UserCreate, UserResponse, Token, GoogleAuthResponse


router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")

# Configure OAuth
config = Config(environ={
    'GOOGLE_CLIENT_ID': settings.GOOGLE_CLIENT_ID,
    'GOOGLE_CLIENT_SECRET': settings.GOOGLE_CLIENT_SECRET
})

oauth = OAuth(config)
oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'}
)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception
    
    email: str = payload.get("sub")
    if email is None:
        raise credentials_exception
    
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    
    if user is None:
        raise credentials_exception
    
    return user


@router.post("/register", response_model=UserResponse)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    # Check if user exists
    result = await db.execute(select(User).where(User.email == user_data.email))
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create user
    hashed_password = get_password_hash(user_data.password)
    user = User(email=user_data.email, hashed_password=hashed_password)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    
    return user


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    # Get user
    result = await db.execute(select(User).where(User.email == form_data.username))
    user = result.scalar_one_or_none()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token = create_access_token(data={"sub": user.email})
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.post("/logout")
async def logout(current_user: User = Depends(get_current_user)):
    """Logout endpoint - client should clear token after calling this"""
    return {"message": "Successfully logged out"}


@router.get("/google/login")
async def google_login(request: Request):
    """Initiate Google OAuth flow"""
    redirect_uri = settings.GOOGLE_REDIRECT_URI
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get("/google/callback")
async def google_callback(request: Request, db: AsyncSession = Depends(get_db)):
    """Handle Google OAuth callback"""
    try:
        # Get token from Google
        token = await oauth.google.authorize_access_token(request)
        
        # Get user info from Google
        user_info = token.get('userinfo')
        if not user_info:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to get user info from Google"
            )
        
        email = user_info.get('email')
        google_id = user_info.get('sub')
        full_name = user_info.get('name')
        picture = user_info.get('picture')
        
        if not email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email not provided by Google"
            )
        
        # Check if user exists
        result = await db.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()
        
        is_new_user = user is None
        
        if user:
            # Update OAuth info if not set
            if not user.oauth_provider:
                user.oauth_provider = 'google'
                user.oauth_id = google_id
                user.full_name = full_name
                user.picture_url = picture
                await db.commit()
                await db.refresh(user)
        else:
            # Create new user
            user = User(
                email=email,
                oauth_provider='google',
                oauth_id=google_id,
                full_name=full_name,
                picture_url=picture,
                is_active=True
            )
            db.add(user)
            await db.commit()
            await db.refresh(user)
        
        # Create access token
        access_token = create_access_token(data={"sub": user.email})
        
        # Redirect to frontend with token
        # For new users, add a flag to redirect to profile
        frontend_url = "http://localhost:5173"
        redirect_path = "/auth/callback"
        redirect_query = f"token={access_token}"
        if is_new_user:
            redirect_query += "&firstLogin=true"
        
        return RedirectResponse(
            url=f"{frontend_url}{redirect_path}?{redirect_query}"
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"OAuth authentication failed: {str(e)}"
        )
