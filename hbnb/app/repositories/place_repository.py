"""place repository module"""

from .base_repository import BaseRepository
from app.models.place import Place
from sqlalchemy import and_


class PlaceRepository(BaseRepository):
    def __init__(self):
        super().__init__(Place)

    def get_by_owner(self, owner_id):
        return self.model.query.filter_by(owner_id=owner_id).all()

    def get_by_price_range(self, min_price, max_price):
        return self.model.query.filter(
            and_(self.model.price >= min_price, self.model.price <= max_price)
        ).all()

    def search_by_location(self, lat, lon, radius):
        # Simplified distance calculation
        return self.model.query.filter(
            and_(
                self.model.latitude.between(lat - radius, lat + radius),
                self.model.longitude.between(lon - radius, lon + radius),
            )
        ).all()
