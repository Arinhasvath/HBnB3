from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.facade import facade

api = Namespace("places", description="Place operations")

# API Models
place_model = api.model(
    "Place",
    {
        "id": fields.String(readonly=True, description="Place identifier"),
        "title": fields.String(
            required=True, description="Title of the place"
        ),
        "description": fields.String(
            required=True, description="Description of the place"
        ),
        "price": fields.Float(required=True, description="Price per night"),
        "latitude": fields.Float(
            required=True, description="Latitude location"
        ),
        "longitude": fields.Float(
            required=True, description="Longitude location"
        ),
        "owner_id": fields.String(
            readonly=True, description="Owner identifier"
        ),
    },
)


@api.route("/")
class PlaceList(Resource):
    @api.doc("list_places")
    @api.marshal_list_with(place_model)
    def get(self):
        """Public endpoint - List all places"""
        return facade.get_all_places()

    @api.doc("create_place")
    @api.expect(place_model)
    @api.marshal_with(place_model, code=201)
    @jwt_required()
    def post(self):
        """Protected endpoint - Create a new place"""
        try:
            # Get current authenticated user
            current_user = get_jwt_identity()

            # Prepare place data
            place_data = api.payload
            place_data["owner_id"] = current_user.get("id")

            # Create place and return 201 status code
            return facade.create_place(place_data), 201

        except ValueError as e:
            api.abort(400, str(e))


@api.route("/<string:place_id>")
@api.param("place_id", "The place identifier")
class Place(Resource):
    @api.doc("get_place")
    @api.marshal_with(place_model)
    def get(self, place_id):
        """Public endpoint - Get place details"""
        place = facade.get_place(place_id)
        if not place:
            api.abort(404, f"Place {place_id} not found")
        return place

    @api.doc("update_place")
    @api.expect(place_model)
    @api.marshal_with(place_model)
    @jwt_required()
    def put(self, place_id):
        """Protected endpoint - Update place (owner only)"""
        try:
            # Get current authenticated user
            current_user = get_jwt_identity()

            # Check if place exists
            place = facade.get_place(place_id)
            if not place:
                api.abort(404, "Place not found")

            # Verify ownership
            if str(place.owner_id) != str(current_user.get("id")):
                api.abort(
                    403, "Unauthorized: only the owner can modify this place"
                )

            # Update place
            return facade.update_place(place_id, api.payload)

        except ValueError as e:
            api.abort(400, str(e))

    @api.doc("delete_place")
    @api.response(204, "Place deleted")
    @jwt_required()
    def delete(self, place_id):
        """Protected endpoint - Delete place (owner only)"""
        try:
            # Get current authenticated user
            current_user = get_jwt_identity()

            # Check if place exists
            place = facade.get_place(place_id)
            if not place:
                api.abort(404, "Place not found")

            # Verify ownership
            if str(place.owner_id) != str(current_user.get("id")):
                api.abort(
                    403, "Unauthorized: only the owner can delete this place"
                )

            # Delete place
            facade.delete_place(place_id)
            return "", 204

        except Exception as e:
            api.abort(500, str(e))
