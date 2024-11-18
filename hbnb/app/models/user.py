"""User model module"""

from app.db import db
from app.models.base_model import BaseModel
from werkzeug.security import generate_password_hash, check_password_hash


class User(BaseModel):
    """
    Classe User représentant les utilisateurs.
    Hérite de BaseModel pour id, created_at, updated_at.
    Requirements:
    - email unique
    - password hashé
    - is_admin pour droits administrateur
    """

    __tablename__ = "users"

    # Colonnes selon requirements
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def __init__(self, *args, **kwargs):
        """
        Initialise un utilisateur avec hashage du mot de passe
        """
        super().__init__(*args, **kwargs)
        if "password" in kwargs:
            self.set_password(kwargs["password"])
        self.validate()

    def validate(self):
        """
        Valide les données utilisateur:
        - Email valide
        - Noms non vides
        """
        if not self.first_name or not self.first_name.strip():
            raise ValueError("first_name cannot be empty")
        if not self.last_name or not self.last_name.strip():
            raise ValueError("last_name cannot be empty")
        if not self.email or "@" not in self.email:
            raise ValueError("Invalid email format")

    def set_password(self, password):
        """Hash le mot de passe avant stockage"""
        if not password:
            raise ValueError("Password cannot be empty")
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """Vérifie si le mot de passe correspond"""
        return check_password_hash(self.password, password)

    def to_dict(self):
        """
        Convertit l'objet en dictionnaire pour l'API.
        Note: le mot de passe n'est jamais envoyé
        """
        return {
            "id": self.id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "is_admin": self.is_admin,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
