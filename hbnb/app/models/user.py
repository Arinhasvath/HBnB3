"""User model"""
from app.db import db
from app.models.base_model import BaseModel
from werkzeug.security import generate_password_hash, check_password_hash

class User(BaseModel):
   __tablename__ = 'users'
   
   email = db.Column(db.String(120), unique=True, nullable=False)
   password = db.Column(db.String(255), nullable=False)
   first_name = db.Column(db.String(100), nullable=False)
   last_name = db.Column(db.String(100), nullable=False)
   is_admin = db.Column(db.Boolean, default=False)

   def __init__(self, *args, **kwargs):
       super().__init__(*args, **kwargs)
       if 'password' in kwargs:
           self.set_password(kwargs['password'])
       self.validate()

   def set_password(self, password):
       if not password:
           raise ValueError("Password cannot be empty")
       self.password = generate_password_hash(password)

   def check_password(self, password):
       return check_password_hash(self.password, password) if self.password else False

   def validate(self):
       if not self.first_name or not self.first_name.strip():
           raise ValueError("first_name cannot be empty")
       if not self.last_name or not self.last_name.strip():
           raise ValueError("last_name cannot be empty")
       if not self.email or not self.email.strip() or '@' not in self.email:
           raise ValueError("Invalid email format")

   def to_dict(self):
       data = super().to_dict()
       del data['password']
       return data
