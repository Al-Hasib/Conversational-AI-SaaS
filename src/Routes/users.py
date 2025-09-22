from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_current_active_user, get_user_service
from app.models.user import UserInDB
from app.schemas.user import UserResponse, UserUpdate
from app.services.user_service import UserService

router = APIRouter()

def format_user_response(user: UserInDB) -> UserResponse:
    return UserResponse(
        id=str(user.id),
        email=user.email,
        full_name=user.full_name,
        created_at=user.created_at,
        is_active=user.is_active,
        is_verified=user.is_verified
    )

@router.get("/users/me", response_model=UserResponse)
async def get_current_user_profile(
    current_user: UserInDB = Depends(get_current_active_user)
):
    return format_user_response(current_user)

@router.put("/users/me", response_model=UserResponse)
async def update_current_user(
    user_update: UserUpdate,
    current_user: UserInDB = Depends(get_current_active_user),
    user_service: UserService = Depends(get_user_service)
):
    updated_user = await user_service.update_user(
        str(current_user.id),
        user_update
    )
    
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return format_user_response(updated_user)

@router.delete("/users/me")
async def delete_current_user(
    current_user: UserInDB = Depends(get_current_active_user),
    user_service: UserService = Depends(get_user_service)
):
    success = await user_service.delete_user(str(current_user.id))
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return {"message": "User deleted successfully"}

@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user_by_id(
    user_id: str,
    current_user: UserInDB = Depends(get_current_active_user),
    user_service: UserService = Depends(get_user_service)
):
    user = await user_service.get_user_by_id(user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return format_user_response(user)

@router.get("/protected")
async def protected_route(
    current_user: UserInDB = Depends(get_current_active_user)
):
    return {
        "message": "This is a protected route",
        "user": current_user.email,
        "user_id": str(current_user.id)
    }