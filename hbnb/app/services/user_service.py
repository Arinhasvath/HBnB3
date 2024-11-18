"""
User service module
"""

from typing import Optional
from app.models.user import User
from app.services.facade import facade  # Import l'instance singleton


class UserService:
    """Service class for managing user operations"""

    def __init__(self, facade_instance=None):
        """Initialize avec une instance de façade (utilise l'instance singleton par défaut)"""
        self.facade = (
            facade_instance if facade_instance is not None else facade
        )

    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Get user by ID"""
        return self.facade.get_user(user_id)

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        return self.facade.get_user_by_email(email)

    def create_user(self, user_data: dict) -> User:
        """Create a new user"""
        if self.get_user_by_email(user_data.get("email")):
            raise ValueError("Email already exists")
        return self.facade.create_user(user_data)

    def update_user(self, user_id: str, user_data: dict) -> User:
        """Update user data"""
        user = self.get_user_by_id(user_id)
        if not user:
            raise ValueError(f"User with id {user_id} not found")

        if "email" in user_data:
            existing_user = self.get_user_by_email(user_data["email"])
            if existing_user and existing_user.id != user_id:
                raise ValueError("Email already in use")

        return self.facade.update_user(user_id, user_data)

    def delete_user(self, user_id: str) -> bool:
        """Delete a user"""
        return self.facade.delete_user(user_id)

    def is_admin(self, user_id: str) -> bool:
        """Check if user has admin privileges"""
        if not user_id:
            return False
        user = self.get_user_by_id(user_id)
        return bool(user and getattr(user, "is_admin", False))

    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """Authenticate user credentials"""
        return self.facade.authenticate_user(email, password)
