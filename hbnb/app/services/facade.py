"""Complete Facade service implementation."""

from typing import Optional, List, Dict, Any
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import and_, or_, func
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review
from app.db import db


class HBnBFacade:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if not hasattr(self, "_initialized"):
            self._initialized = True

    # Base CRUD operations
    def _add_and_commit(self, obj: Any) -> None:
        """Helper to add and commit with error handling"""
        try:
            db.session.add(obj)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise ValueError(f"Database error: {str(e)}")

    def _delete_and_commit(self, obj: Any) -> bool:
        """Helper to delete and commit with error handling"""
        try:
            db.session.delete(obj)
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            db.session.rollback()
            raise ValueError(f"Database error: {str(e)}")

    # User methods
    def get_user(self, user_id: str) -> Optional[User]:
        """Get user by ID"""
        return User.query.get(user_id)

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        return User.query.filter_by(email=email).first()

    def get_all_users(self) -> List[User]:
        """Get all users"""
        return User.query.all()

    def create_user(self, user_data: dict) -> User:
        """Create new user with validation"""
        if self.get_user_by_email(user_data.get("email")):
            raise ValueError("Email already registered")
        try:
            user = User(**user_data)
            user.validate()
            self._add_and_commit(user)
            return user
        except (ValueError, SQLAlchemyError) as e:
            raise ValueError(f"Error creating user: {str(e)}")

    def update_user(
        self, user_id: str, user_data: dict, check_email: bool = True
    ) -> User:
        """Update existing user"""
        user = self.get_user(user_id)
        if not user:
            raise ValueError("User not found")

        if check_email and "email" in user_data:
            existing_user = self.get_user_by_email(user_data["email"])
            if existing_user and existing_user.id != user_id:
                raise ValueError("Email already registered")

        try:
            for key, value in user_data.items():
                if key == "password":
                    user.set_password(value)
                else:
                    setattr(user, key, value)
            user.validate()
            db.session.commit()
            return user
        except (ValueError, SQLAlchemyError) as e:
            db.session.rollback()
            raise ValueError(f"Error updating user: {str(e)}")

    def delete_user(self, user_id: str) -> bool:
        """Delete user and all related data"""
        user = self.get_user(user_id)
        if not user:
            return False
        return self._delete_and_commit(user)

    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """Authenticate user and return user object if successful"""
        user = self.get_user_by_email(email)
        if user and user.check_password(password):
            return user
        return None

    # Place methods
    def get_place(self, place_id: str) -> Optional[Place]:
        """Get place by ID"""
        return Place.query.get(place_id)

    def get_user_places(self, user_id: str) -> List[Place]:
        """Get all places owned by user"""
        return Place.query.filter_by(owner_id=user_id).all()

    def get_all_places(self, filters: dict = None) -> List[Place]:
        """Get all places with optional filters"""
        query = Place.query
        if filters:
            if "price_min" in filters:
                query = query.filter(Place.price >= filters["price_min"])
            if "price_max" in filters:
                query = query.filter(Place.price <= filters["price_max"])
            if "amenities" in filters:
                query = query.filter(
                    Place.amenities.any(Amenity.id.in_(filters["amenities"]))
                )
        return query.all()

    def create_place(self, place_data: dict, owner_id: str) -> Place:
        """Create new place"""
        try:
            place_data["owner_id"] = owner_id
            if "amenity_ids" in place_data:
                amenities = [
                    self.get_amenity(aid)
                    for aid in place_data.pop("amenity_ids")
                ]
                if None in amenities:
                    raise ValueError("One or more amenities not found")
            else:
                amenities = []

            place = Place(**place_data)
            place.amenities = amenities
            place.validate()
            self._add_and_commit(place)
            return place
        except (ValueError, SQLAlchemyError) as e:
            raise ValueError(f"Error creating place: {str(e)}")

    def update_place(
        self, place_id: str, place_data: dict, owner_id: str = None
    ) -> Place:
        """Update place with owner verification"""
        place = self.get_place(place_id)
        if not place:
            raise ValueError("Place not found")

        if owner_id and str(place.owner_id) != str(owner_id):
            raise ValueError("Unauthorized: not the owner")

        try:
            if "amenity_ids" in place_data:
                amenities = [
                    self.get_amenity(aid)
                    for aid in place_data.pop("amenity_ids")
                ]
                if None in amenities:
                    raise ValueError("One or more amenities not found")
                place.amenities = amenities

            for key, value in place_data.items():
                if hasattr(place, key):
                    setattr(place, key, value)

            place.validate()
            db.session.commit()
            return place
        except (ValueError, SQLAlchemyError) as e:
            db.session.rollback()
            raise ValueError(f"Error updating place: {str(e)}")

    def delete_place(self, place_id: str, owner_id: str = None) -> bool:
        """Delete place with owner verification"""
        place = self.get_place(place_id)
        if not place:
            return False

        if owner_id and str(place.owner_id) != str(owner_id):
            raise ValueError("Unauthorized: not the owner")

        return self._delete_and_commit(place)

    # Review methods
    def get_review(self, review_id: str) -> Optional[Review]:
        """Get review by ID"""
        return Review.query.get(review_id)

    def get_place_reviews(self, place_id: str) -> List[Review]:
        """Get all reviews for a place"""
        return Review.query.filter_by(place_id=place_id).all()

    def get_user_reviews(self, user_id: str) -> List[Review]:
        """Get all reviews by a user"""
        return Review.query.filter_by(user_id=user_id).all()

    def create_review(self, review_data: dict, user_id: str) -> Review:
        """Create review with validations"""
        try:
            place = self.get_place(review_data.get("place_id"))
            if not place:
                raise ValueError("Place not found")

            if str(place.owner_id) == str(user_id):
                raise ValueError("Cannot review your own place")

            existing = Review.query.filter_by(
                user_id=user_id, place_id=review_data["place_id"]
            ).first()

            if existing:
                raise ValueError("Already reviewed this place")

            review_data["user_id"] = user_id
            review = Review(**review_data)
            review.validate()
            self._add_and_commit(review)
            return review
        except (ValueError, SQLAlchemyError) as e:
            raise ValueError(f"Error creating review: {str(e)}")

    def update_review(
        self, review_id: str, review_data: dict, user_id: str = None
    ) -> Review:
        """Update review with author verification"""
        review = self.get_review(review_id)
        if not review:
            raise ValueError("Review not found")

        if user_id and str(review.user_id) != str(user_id):
            raise ValueError("Unauthorized: not the author")

        try:
            protected = ["place_id", "user_id"]
            update_data = {
                k: v for k, v in review_data.items() if k not in protected
            }

            for key, value in update_data.items():
                setattr(review, key, value)

            review.validate()
            db.session.commit()
            return review
        except (ValueError, SQLAlchemyError) as e:
            db.session.rollback()
            raise ValueError(f"Error updating review: {str(e)}")

    def delete_review(self, review_id: str, user_id: str = None) -> bool:
        """Delete review with author verification"""
        review = self.get_review(review_id)
        if not review:
            return False

        if user_id and str(review.user_id) != str(user_id):
            raise ValueError("Unauthorized: not the author")

        return self._delete_and_commit(review)

    # Amenity methods
    def get_amenity(self, amenity_id: str) -> Optional[Amenity]:
        """Get amenity by ID"""
        return Amenity.query.get(amenity_id)

    def get_all_amenities(self) -> List[Amenity]:
        """Get all amenities"""
        return Amenity.query.all()

    def create_amenity(self, amenity_data: dict) -> Amenity:
        """Create new amenity"""
        try:
            amenity = Amenity(**amenity_data)
            amenity.validate()
            self._add_and_commit(amenity)
            return amenity
        except (ValueError, SQLAlchemyError) as e:
            raise ValueError(f"Error creating amenity: {str(e)}")

    def add_place_amenity(
        self, place_id: str, amenity_id: str, admin_id: str = None
    ) -> bool:
        """Add amenity to place."""
        try:
            if admin_id:
                admin = self.get_user(admin_id)
                if not admin or not admin.is_admin:
                    raise ValueError("Admin privileges required")

            place = self.get_place(place_id)
            amenity = self.get_amenity(amenity_id)

            if not place or not amenity:
                raise ValueError("Place or amenity not found")

            if amenity not in place.amenities:
                place.amenities.append(amenity)
                db.session.commit()
            return True
        except SQLAlchemyError as e:
            db.session.rollback()
            raise ValueError(f"Error adding amenity to place: {str(e)}")

    def remove_place_amenity(
        self, place_id: str, amenity_id: str, admin_id: str = None
    ) -> bool:
        """Remove amenity from place."""
        try:
            if admin_id:
                admin = self.get_user(admin_id)
                if not admin or not admin.is_admin:
                    raise ValueError("Admin privileges required")

            place = self.get_place(place_id)
            amenity = self.get_amenity(amenity_id)

            if not place or not amenity:
                raise ValueError("Place or amenity not found")

            if amenity in place.amenities:
                place.amenities.remove(amenity)
                db.session.commit()
            return True
        except SQLAlchemyError as e:
            db.session.rollback()
            raise ValueError(f"Error removing amenity from place: {str(e)}")

    def get_place_with_amenities(self, place_id: str) -> Dict[str, Any]:
        """Get place with all amenities."""
        place = self.get_place(place_id)
        if not place:
            raise ValueError("Place not found")

        return {
            **place.to_dict(),
            "amenities": [amenity.to_dict() for amenity in place.amenities],
            "reviews": [review.to_dict() for review in place.reviews],
        }

    def search_places(self, filters: Dict[str, Any] = None) -> List[Place]:
        """Search places with filters."""
        query = Place.query

        if filters:
            if "price_min" in filters:
                query = query.filter(Place.price >= filters["price_min"])
            if "price_max" in filters:
                query = query.filter(Place.price <= filters["price_max"])
            if "amenities" in filters:
                query = query.filter(
                    Place.amenities.any(Amenity.id.in_(filters["amenities"]))
                )
            if "rating_min" in filters:
                query = (
                    query.join(Review)
                    .group_by(Place.id)
                    .having(func.avg(Review.rating) >= filters["rating_min"])
                )

        return query.all()

    def get_user_stats(self, user_id: str) -> Dict[str, Any]:
        """Get statistics for a user."""
        user = self.get_user(user_id)
        if not user:
            raise ValueError("User not found")

        return {
            "places_count": len(user.places),
            "reviews_count": len(user.reviews),
            "average_rating": db.session.query(func.avg(Review.rating))
            .filter_by(user_id=user_id)
            .scalar()
            or 0.0,
        }

    def get_place_stats(self, place_id: str) -> Dict[str, Any]:
        """Get statistics for a place."""
        place = self.get_place(place_id)
        if not place:
            raise ValueError("Place not found")

        reviews = place.reviews
        if not reviews:
            return {
                "review_count": 0,
                "average_rating": 0,
                "rating_distribution": {str(i): 0 for i in range(1, 6)},
            }

        rating_dist = {str(i): 0 for i in range(1, 6)}
        for review in reviews:
            rating_dist[str(review.rating)] += 1

        return {
            "review_count": len(reviews),
            "average_rating": sum(r.rating for r in reviews) / len(reviews),
            "rating_distribution": rating_dist,
            "amenities_count": len(place.amenities),
        }

    # Admin methods
    def admin_create_user(self, user_data: dict, admin_id: str) -> User:
        """Create user with admin privileges check"""
        admin = self.get_user(admin_id)
        if not admin or not admin.is_admin:
            raise ValueError("Admin privileges required")
        return self.create_user(user_data)

    def admin_update_user(
        self, user_id: str, user_data: dict, admin_id: str
    ) -> User:
        """Update any user as admin"""
        admin = self.get_user(admin_id)
        if not admin or not admin.is_admin:
            raise ValueError("Admin privileges required")
        return self.update_user(user_id, user_data)

    def admin_delete_user(self, user_id: str, admin_id: str) -> bool:
        """Delete user as admin"""
        admin = self.get_user(admin_id)
        if not admin or not admin.is_admin:
            raise ValueError("Admin privileges required")
        return self.delete_user(user_id)

    def admin_manage_place(
        self, place_id: str, place_data: dict, admin_id: str
    ) -> Place:
        """Admin can manage any place"""
        admin = self.get_user(admin_id)
        if not admin or not admin.is_admin:
            raise ValueError("Admin privileges required")

        if place_id:
            return self.update_place(place_id, place_data)
        return self.create_place(place_data, place_data.get("owner_id"))

    def admin_manage_amenity(
        self, amenity_id: str, amenity_data: dict, admin_id: str
    ) -> Amenity:
        """Admin can manage amenities"""
        admin = self.get_user(admin_id)
        if not admin or not admin.is_admin:
            raise ValueError("Admin privileges required")

        if amenity_id:
            amenity = self.get_amenity(amenity_id)
            if not amenity:
                raise ValueError("Amenity not found")

            try:
                for key, value in amenity_data.items():
                    setattr(amenity, key, value)
                amenity.validate()
                db.session.commit()
                return amenity
            except SQLAlchemyError as e:
                db.session.rollback()
                raise ValueError(f"Error updating amenity: {str(e)}")
        else:
            return self.create_amenity(amenity_data)

    def admin_delete_amenity(self, amenity_id: str, admin_id: str) -> bool:
        """Admin can delete any amenity"""
        admin = self.get_user(admin_id)
        if not admin or not admin.is_admin:
            raise ValueError("Admin privileges required")

        amenity = self.get_amenity(amenity_id)
        if not amenity:
            raise ValueError("Amenity not found")

        return self._delete_and_commit(amenity)

    def admin_manage_review(
        self, review_id: str, review_data: dict, admin_id: str
    ) -> Review:
        """Admin can manage any review"""
        admin = self.get_user(admin_id)
        if not admin or not admin.is_admin:
            raise ValueError("Admin privileges required")

        if review_id:
            return self.update_review(review_id, review_data)
        return self.create_review(review_data, review_data.get("user_id"))

    def admin_get_stats(self, admin_id: str) -> Dict[str, Any]:
        """Get admin statistics"""
        admin = self.get_user(admin_id)
        if not admin or not admin.is_admin:
            raise ValueError("Admin privileges required")

        return {
            "users_count": User.query.count(),
            "places_count": Place.query.count(),
            "reviews_count": Review.query.count(),
            "amenities_count": Amenity.query.count(),
            "average_rating": db.session.query(
                func.avg(Review.rating)
            ).scalar()
            or 0.0,
            "places_by_rating": db.session.query(
                Place.id,
                Place.title,
                func.avg(Review.rating).label("avg_rating"),
            )
            .join(Review)
            .group_by(Place.id)
            .all(),
        }


# Create singleton instance
facade = HBnBFacade()
