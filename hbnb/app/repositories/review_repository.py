from .base_repository import BaseRepository
from app.models.review import Review


class ReviewRepository(BaseRepository):
    def __init__(self):
        super().__init__(Review)

    def get_by_user(self, user_id):
        return self.model.query.filter_by(user_id=user_id).all()

    def get_by_place(self, place_id):
        return self.model.query.filter_by(place_id=place_id).all()

    def get_by_rating(self, rating):
        return self.model.query.filter_by(rating=rating).all()

    def get_average_rating_for_place(self, place_id):
        from sqlalchemy import func

        result = (
            self.model.query.with_entities(func.avg(self.model.rating))
            .filter_by(place_id=place_id)
            .first()
        )
        return float(result[0]) if result[0] else 0.0
