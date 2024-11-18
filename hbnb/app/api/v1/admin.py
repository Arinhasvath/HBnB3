"""Admin endpoints implementation."""

from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.facade import facade

api = Namespace("admin", description="Admin operations")

# Models for Swagger documentation
user_model = api.model(
    "User",
    {
        "id": fields.String(readonly=True),
        "email": fields.String(required=True),
        "first_name": fields.String(required=True),
        "last_name": fields.String(required=True),
        "is_admin": fields.Boolean(default=False),
    },
)

place_model = api.model(
    "Place",
    {
        "id": fields.String(readonly=True),
        "title": fields.String(required=True),
        "description": fields.String(),
        "price": fields.Float(required=True),
        "latitude": fields.Float(),
        "longitude": fields.Float(),
        "owner_id": fields.String(required=True),
    },
)

amenity_model = api.model(
    "Amenity",
    {"id": fields.String(readonly=True), "name": fields.String(required=True)},
)

stats_model = api.model(
    "Stats",
    {
        "total_users": fields.Integer(),
        "total_places": fields.Integer(),
        "total_reviews": fields.Integer(),
        "total_amenities": fields.Integer(),
        "avg_rating": fields.Float(),
    },
)


@api.route("/users/")
class AdminUsers(Resource):
    @api.doc("create_user")
    @api.expect(user_model)
    @api.marshal_with(user_model, code=201)
    @jwt_required()
    def post(self):
        """Create a new user (admin only)."""
        current_user = get_jwt_identity()
        return (
            facade.admin_create_user(api.payload, current_user.get("id")),
            201,
        )


@api.route("/users/<string:user_id>")
class AdminUser(Resource):
    @api.doc("update_user")
    @api.expect(user_model)
    @api.marshal_with(user_model)
    @jwt_required()
    def put(self, user_id):
        """Update any user (admin only)."""
        current_user = get_jwt_identity()
        return facade.admin_update_user(
            user_id, api.payload, current_user.get("id")
        )

    @api.doc("delete_user")
    @api.response(204, "User deleted")
    @jwt_required()
    def delete(self, user_id):
        """Delete any user (admin only)."""
        current_user = get_jwt_identity()
        facade.admin_delete_user(user_id, current_user.get("id"))
        return "", 204


@api.route("/places/<string:place_id>")
class AdminPlace(Resource):
    @api.doc("update_place")
    @api.expect(place_model)
    @api.marshal_with(place_model)
    @jwt_required()
    def put(self, place_id):
        """Update any place (admin only)."""
        current_user = get_jwt_identity()
        return facade.admin_manage_place(
            place_id, api.payload, current_user.get("id")
        )

    @api.doc("delete_place")
    @api.response(204, "Place deleted")
    @jwt_required()
    def delete(self, place_id):
        """Delete any place (admin only)."""
        current_user = get_jwt_identity()
        facade.admin_delete_place(place_id, current_user.get("id"))
        return "", 204


@api.route("/amenities/")
class AdminAmenities(Resource):
    @api.doc("create_amenity")
    @api.expect(amenity_model)
    @api.marshal_with(amenity_model, code=201)
    @jwt_required()
    def post(self):
        """Create a new amenity (admin only)."""
        current_user = get_jwt_identity()
        return (
            facade.admin_manage_amenity(
                None, api.payload, current_user.get("id")
            ),
            201,
        )


@api.route("/amenities/<string:amenity_id>")
class AdminAmenity(Resource):
    @api.doc("update_amenity")
    @api.expect(amenity_model)
    @api.marshal_with(amenity_model)
    @jwt_required()
    def put(self, amenity_id):
        """Update an amenity (admin only)."""
        current_user = get_jwt_identity()
        return facade.admin_manage_amenity(
            amenity_id, api.payload, current_user.get("id")
        )


@api.route("/stats")
class AdminStats(Resource):
    @api.doc("get_stats")
    @api.marshal_with(stats_model)
    @jwt_required()
    def get(self):
        """Get global statistics (admin only)."""
        current_user = get_jwt_identity()
        return facade.admin_get_stats(current_user.get("id"))
