from datetime import datetime
from typing import Optional
from bson import ObjectId

class UserInDB:
    def __init__(
        self,
        email: str,
        hashed_password: str,
        full_name: str,
        id: Optional[ObjectId] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        is_active: bool = True,
        is_verified: bool = False,
    ):
        self.id = id
        self.email = email
        self.hashed_password = hashed_password
        self.full_name = full_name
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
        self.is_active = is_active
        self.is_verified = is_verified

    def dict(self):
        return {
            "_id": self.id,
            "email": self.email,
            "hashed_password": self.hashed_password,
            "full_name": self.full_name,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "is_active": self.is_active,
            "is_verified": self.is_verified,
        }

    @classmethod
    def from_dict(cls, user_dict: dict):
        return cls(
            id=user_dict.get("_id"),
            email=user_dict["email"],
            hashed_password=user_dict["hashed_password"],
            full_name=user_dict["full_name"],
            created_at=user_dict.get("created_at"),
            updated_at=user_dict.get("updated_at"),
            is_active=user_dict.get("is_active", True),
            is_verified=user_dict.get("is_verified", False),
        )