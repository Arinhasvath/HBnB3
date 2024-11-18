"""Amenities API endpoints implementation."""

from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.facade import facade  # Import singleton facade instance
from app.services.user_service import UserService
import logging

# Configuration des logs
logger = logging.getLogger(__name__)

api = Namespace("amenities", description="Amenity operations")

# API Models
amenity_model = api.model(
    "Amenity",
    {
        "id": fields.String(readonly=True, description="Unique identifier"),
        "name": fields.String(
            required=True, description="Name of the amenity"
        ),
        "created_at": fields.DateTime(readonly=True),
        "updated_at": fields.DateTime(readonly=True),
    },
)

# Création d'une seule instance de UserService
user_service = UserService(facade)


@api.route("/")
class AmenityList(Resource):
    @api.doc("list_amenities", responses={200: ("Success", [amenity_model])})
    @api.marshal_list_with(amenity_model)
    def get(self):
        """List all amenities"""
        try:
            return facade.get_all_amenities()
        except Exception as e:
            logger.error(f"Error getting amenities: {str(e)}")
            return {"error": "Internal server error"}, 500

    @api.doc(
        "create_amenity",
        responses={
            201: ("Created", amenity_model),
            400: "Validation Error",
            403: "Admin privileges required",
        },
    )
    @api.expect(
        api.model(
            "AmenityInput",
            {
                "name": fields.String(
                    required=True, description="Name of the amenity"
                )
            },
        )
    )
    @jwt_required()
    def post(self):
        """Create a new amenity (admin only)"""
        try:
            # Get current user from JWT
            current_user = get_jwt_identity()
            logger.debug(f"User attempting to create amenity: {current_user}")

            # Verify admin status
            if not user_service.is_admin(current_user.get("id")):
                return {"error": "Admin privileges required"}, 403

            # Validate input
            name = api.payload.get("name", "").strip()
            if not name:
                return {"error": "Name is required"}, 400

            # Create amenity using facade
            amenity = facade.create_amenity({"name": name})
            return amenity, 201

        except ValueError as e:
            logger.warning(f"Validation error: {str(e)}")
            return {"error": str(e)}, 400
        except Exception as e:
            logger.error(f"Error creating amenity: {str(e)}")
            return {"error": "Internal server error"}, 500


@api.route("/<string:amenity_id>")
@api.param("amenity_id", "The amenity identifier")
class AmenityResource(Resource):
    @api.doc(
        "get_amenity",
        responses={200: ("Success", amenity_model), 404: "Amenity not found"},
    )
    @api.marshal_with(amenity_model)
    def get(self, amenity_id):
        """Fetch an amenity by ID"""
        try:
            amenity = facade.get_amenity(amenity_id)
            if not amenity:
                return {"error": "Amenity not found"}, 404
            return amenity
        except Exception as e:
            logger.error(f"Error getting amenity: {str(e)}")
            return {"error": "Internal server error"}, 500

    @api.doc(
        "update_amenity",
        responses={
            200: ("Success", amenity_model),
            400: "Validation Error",
            403: "Admin privileges required",
            404: "Amenity not found",
        },
    )
    @api.expect(
        api.model(
            "AmenityUpdate",
            {
                "name": fields.String(
                    required=True, description="New name of the amenity"
                )
            },
        )
    )
    @jwt_required()
    def put(self, amenity_id):
        """Update an amenity (admin only)"""
        try:
            current_user = get_jwt_identity()

            # Verify admin status
            if not user_service.is_admin(current_user.get("id")):
                return {"error": "Admin privileges required"}, 403

            # Check if amenity exists
            if not facade.get_amenity(amenity_id):
                return {"error": "Amenity not found"}, 404

            # Validate input
            name = api.payload.get("name", "").strip()
            if not name:
                return {"error": "Name is required"}, 400

            # Update amenity
            amenity_data = {"name": name}
            amenity = facade.update_amenity(amenity_id, amenity_data)
            return amenity

        except ValueError as e:
            return {"error": str(e)}, 400
        except Exception as e:
            logger.error(f"Error updating amenity: {str(e)}")
            return {"error": "Internal server error"}, 500

    @api.doc(
        "delete_amenity",
        responses={
            204: "Amenity deleted",
            403: "Admin privileges required",
            404: "Amenity not found",
        },
    )
    @jwt_required()
    def delete(self, amenity_id):
        """Delete an amenity (admin only)"""
        try:
            current_user = get_jwt_identity()

            # Verify admin status
            if not user_service.is_admin(current_user.get("id")):
                return {"error": "Admin privileges required"}, 403

            # Check if amenity exists
            if not facade.get_amenity(amenity_id):
                return {"error": "Amenity not found"}, 404

            # Delete amenity
            facade.delete_amenity(amenity_id)
            return "", 204

        except Exception as e:
            logger.error(f"Error deleting amenity: {str(e)}")
            return {"error": "Internal server error"}, 500
