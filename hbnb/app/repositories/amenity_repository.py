from .base_repository import BaseRepository
from app.models.amenity import Amenity


class AmenityRepository(BaseRepository):
    def __init__(self):
        super().__init__(Amenity)

    def get_by_name(self, name):
        return self.model.query.filter_by(name=name).first()

    def get_by_place(self, place_id):
        return self.model.query.join("places").filter_by(id=place_id).all()
