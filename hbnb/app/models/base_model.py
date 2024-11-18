"""Base model module."""

from app.models.base_model import BaseModel
from app.db import db
import uuid
from datetime import datetime, timezone


class BaseModel(db.Model):
    """Base model class."""

    __abstract__ = True

    id = db.Column(
        db.String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    created_at = db.Column(
        db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    def to_dict(self):
        """Convert to dictionary."""
        result = {}
        for column in self.__table__.columns:
            value = getattr(self, column.name)
            if isinstance(value, datetime):
                value = value.isoformat()
            result[column.name] = value
        return result


class User(BaseModel):
    """User Model."""

    __tablename__ = "users"

    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    places = db.relationship("Place", backref="owner", lazy="select")
    reviews = db.relationship("Review", backref="user", lazy="select")

    def set_password(self, password):
        """Hash password."""
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """Verify password."""
        return check_password_hash(self.password, password)

    def validate(self):
        """Validate user data."""
        if not self.email or not self.email.strip():
            raise ValueError("email cannot be empty")
        if not self.first_name or not self.first_name.strip():
            raise ValueError("first_name cannot be empty")
        if not self.last_name or not self.last_name.strip():
            raise ValueError("last_name cannot be empty")


# app/models/place.py

place_amenities = db.Table(
    "place_amenities",
    db.Column(
        "place_id",
        db.String(36),
        db.ForeignKey("places.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    db.Column(
        "amenity_id",
        db.String(36),
        db.ForeignKey("amenities.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class Place(BaseModel):
    """Place Model."""

    __tablename__ = "places"

    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    owner_id = db.Column(
        db.String(36),
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    amenities = db.relationship(
        "Amenity",
        secondary=place_amenities,
        lazy="subquery",
        backref=db.backref("places", lazy=True),
    )
    reviews = db.relationship(
        "Review", backref="place", lazy=True, cascade="all, delete-orphan"
    )

    def validate(self):
        """Validate place data."""
        if not self.title or not self.title.strip():
            raise ValueError("title cannot be empty")
        if not isinstance(self.price, (int, float)) or self.price < 0:
            raise ValueError("price must be a positive number")


class Review(BaseModel):
    """Review Model."""

    __tablename__ = "reviews"

    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
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

    def validate(self):
        """Validate review data."""
        if not self.text or not self.text.strip():
            raise ValueError("text cannot be empty")
        if not isinstance(self.rating, int) or not 1 <= self.rating <= 5:
            raise ValueError("rating must be between 1 and 5")


class Amenity(BaseModel):
    """Amenity Model."""

    __tablename__ = "amenities"

    name = db.Column(db.String(128), nullable=False, unique=True)

    def validate(self):
        """Validate amenity data."""
        if not self.name or not self.name.strip():
            raise ValueError("name cannot be empty")
