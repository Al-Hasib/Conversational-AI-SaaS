from typing import Optional
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.security import get_password_hash, verify_password
from app.models.user import UserInDB
from app.schemas.user import UserCreate, UserUpdate

class UserService:
    def __init__(self, database: AsyncIOMotorDatabase):
        self.database = database
        self.collection = self.database.users

    async def get_user_by_email(self, email: str) -> Optional[UserInDB]:
        user_dict = await self.collection.find_one({"email": email})
        if user_dict:
            return UserInDB.from_dict(user_dict)
        return None

    async def get_user_by_id(self, user_id: str) -> Optional[UserInDB]:
        if not ObjectId.is_valid(user_id):
            return None
        user_dict = await self.collection.find_one({"_id": ObjectId(user_id)})
        if user_dict:
            return UserInDB.from_dict(user_dict)
        return None

    async def create_user(self, user_create: UserCreate) -> UserInDB:
        # Hash password
        hashed_password = get_password_hash(user_create.password)
        
        # Create user instance
        user = UserInDB(
            email=user_create.email,
            hashed_password=hashed_password,
            full_name=user_create.full_name
        )
        
        # Insert into database
        result = await self.collection.insert_one(user.dict())
        user.id = result.inserted_id
        
        return user

    async def authenticate_user(self, email: str, password: str) -> Optional[UserInDB]:
        user = await self.get_user_by_email(email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    async def update_user(self, user_id: str, user_update: UserUpdate) -> Optional[UserInDB]:
        if not ObjectId.is_valid(user_id):
            return None
            
        update_data = {k: v for k, v in user_update.dict().items() if v is not None}
        if not update_data:
            return await self.get_user_by_id(user_id)
            
        update_data["updated_at"] = UserInDB().updated_at
        
        await self.collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": update_data}
        )
        
        return await self.get_user_by_id(user_id)

    async def delete_user(self, user_id: str) -> bool:
        if not ObjectId.is_valid(user_id):
            return False
            
        result = await self.collection.delete_one({"_id": ObjectId(user_id)})
        return result.deleted_count > 0

    async def user_exists(self, email: str) -> bool:
        user = await self.collection.find_one({"email": email})
        return user is not None