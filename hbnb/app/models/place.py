"""Place model module"""

from app.db import db
from app.models.base_model import BaseModel
from app.models.association_tables import place_amenities


class Place(BaseModel):
    """
    Classe Place représentant les logements.
    Hérite de BaseModel pour id, created_at, updated_at.
    Requirements:
    - title VARCHAR(255)
    - price doit être positif
    - owner_id lié à User
    """

    __tablename__ = "places"

    # Colonnes requises par le projet
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    owner_id = db.Column(
        db.String(36),
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    # Relations
    owner = db.relationship(
        "User",
        backref=db.backref("places", lazy=True, cascade="all, delete-orphan"),
    )

    amenities = db.relationship(
        "Amenity",
        secondary=place_amenities,
        lazy="subquery",  # Optimisé pour les requêtes fréquentes
        back_populates="places",
    )

    def __init__(self, *args, **kwargs):
        """Initialise une instance Place avec validation"""
        super().__init__(*args, **kwargs)
        self.title = kwargs.get("title", "")
        self.description = kwargs.get("description", "")
        self.price = float(kwargs.get("price", 0))
        self.latitude = kwargs.get("latitude")
        self.longitude = kwargs.get("longitude")
        self.owner_id = kwargs.get("owner_id")
        self.validate()

    def validate(self):
        """
        Valide les données du logement:
        - Titre non vide
        - Prix positif
        - Coordonnées valides si fournies
        """
        if not self.title or not self.title.strip():
            raise ValueError("Title cannot be empty")
        if not isinstance(self.price, (int, float)) or self.price < 0:
            raise ValueError("Price must be a positive number")
        if self.latitude and (not -90 <= self.latitude <= 90):
            raise ValueError("Invalid latitude")
        if self.longitude and (not -180 <= self.longitude <= 180):
            raise ValueError("Invalid longitude")

    def to_dict(self):
        """
        Convertit l'objet en dictionnaire pour l'API.
        Inclut les relations essentielles.
        """
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": float(self.price),
            "latitude": self.latitude,
            "longitude": self.longitude,
            "owner_id": self.owner_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "amenities": [a.to_dict() for a in self.amenities],
        }
