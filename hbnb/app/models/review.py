"""Review model module"""

from app.db import db
from app.models.base_model import BaseModel


class Review(BaseModel):
    """
    Classe Review pour les avis des utilisateurs sur les logements.
    Hérite de BaseModel pour id, created_at, updated_at.
    """

    __tablename__ = "reviews"

    # Colonnes selon requirements
    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    # Foreign keys avec cascade delete
    user_id = db.Column(
        db.String(36),
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    place_id = db.Column(
        db.String(36),
        db.ForeignKey("places.id", ondelete="CASCADE"),
        nullable=False,
    )

    # Contrainte unique: un utilisateur ne peut laisser qu'un avis par logement
    __table_args__ = (
        db.UniqueConstraint(
            "user_id", "place_id", name="unique_user_place_review"
        ),
    )

    # Relations avec cascade delete
    user = db.relationship(
        "User",
        backref=db.backref("reviews", lazy=True, cascade="all, delete-orphan"),
    )
    place = db.relationship(
        "Place",
        backref=db.backref("reviews", lazy=True, cascade="all, delete-orphan"),
    )

    def __init__(self, *args, **kwargs):
        """Initialise une instance Review"""
        super().__init__(*args, **kwargs)
        self.text = kwargs.get("text", "")
        self.rating = int(kwargs.get("rating", 1))
        self.user_id = kwargs.get("user_id", "")
        self.place_id = kwargs.get("place_id", "")
        self.validate()

    def validate(self):
        """
        Valide les données de l'avis:
        - text non vide
        - rating entre 1 et 5
        """
        if not self.text or not self.text.strip():
            raise ValueError("text cannot be empty")
        if not isinstance(self.rating, int) or not 1 <= self.rating <= 5:
            raise ValueError("rating must be between 1 and 5")

    def to_dict(self):
        """Convertit l'objet en dictionnaire pour l'API"""
        return {
            "id": self.id,
            "text": self.text,
            "rating": self.rating,
            "user_id": self.user_id,
            "place_id": self.place_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
