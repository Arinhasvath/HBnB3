"""Amenity model module"""

from app.db import db
from app.models.base_model import BaseModel

# Import table d'association
from app.models.association_tables import place_amenities


class Amenity(BaseModel):
    """
    Classe Amenity représentant les équipements disponibles.
    Hérite de BaseModel pour id, created_at, updated_at.
    """

    __tablename__ = "amenities"

    # Colonne name unique et non-nullable selon requirements
    name = db.Column(db.String(255), nullable=False, unique=True)

    # Relation many-to-many avec Place via place_amenities
    places = db.relationship(
        "Place",
        secondary=place_amenities,
        back_populates="amenities",
        lazy="dynamic",  # Chargement à la demande pour performance
    )

    def __init__(self, *args, **kwargs):
        """Initialise une instance Amenity"""
        super().__init__(*args, **kwargs)
        self.name = kwargs.get("name", "")
        self.validate()

    def validate(self):
        """Valide les données de l'équipement"""
        if not self.name or not self.name.strip():
            raise ValueError("name cannot be empty")

    def to_dict(self):
        """Convertit l'objet en dictionnaire pour l'API"""
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
