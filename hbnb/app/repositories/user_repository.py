from .base_repository import BaseRepository
from app.models.user import User


class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__(User)

    def get_by_email(self, email):
        return self.model.query.filter_by(email=email).first()

    def get_by_admin(self, is_admin=True):
        return self.model.query.filter_by(is_admin=is_admin).all()
