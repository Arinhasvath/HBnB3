from app.db import db
from app.models.base_model import BaseModel

class User(BaseModel):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}  # Permettre la redéfinition

    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)