from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_user_service
from app.core.config import settings
from app.core.security import create_access_token
from app.schemas.user import UserCreate, UserLogin, Token, UserResponse
from app.services.user_service import UserService

router = APIRouter()

def format_user_response(user) -> UserResponse:
    return UserResponse(
        id=str(user.id),
        email=user.email,
        full_name=user.full_name,
        created_at=user.created_at,
        is_active=user.is_active,
        is_verified=user.is_verified
    )

@router.post("/register", response_model=Token)
async def register(
    user_create: UserCreate,
    user_service: UserService = Depends(get_user_service)
):
    # Check if user already exists
    if await user_service.user_exists(user_create.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    try:
        # Create user
        user = await user_service.create_user(user_create)
        
        # Create access token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.email},
            expires_delta=access_token_expires
        )
        
        # Format response
        user_response = format_user_response(user)
        
        return Token(
            access_token=access_token,
            token_type="bearer",
            user=user_response
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.post("/login", response_model=Token)
async def login(
    user_credentials: UserLogin,
    user_service: UserService = Depends(get_user_service)
):
    user = await user_service.authenticate_user(
        user_credentials.email,
        user_credentials.password
    )
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires
    )
    
    user_response = format_user_response(user)
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        user=user_response
    )