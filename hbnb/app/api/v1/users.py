"""Users API endpoints implementation."""

from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.facade import facade

api = Namespace("users", description="User operations")

user_model = api.model(
    "User",
    {
        "id": fields.String(readonly=True, description="Unique identifier"),
        "first_name": fields.String(required=True, description="First name"),
        "last_name": fields.String(required=True, description="Last name"),
        "email": fields.String(required=True, description="Email address"),
    },
)


@api.route("/")
class UserList(Resource):
    @api.doc("list_users")
    @api.marshal_list_with(user_model)
    @jwt_required()
    def get(self):
        """List all users"""
        try:
            return (
                facade.get_all_users()
            )  # Assurez-vous que cette méthode existe
        except Exception as e:
            api.abort(500, str(e))

    @api.doc("create_user")
    @api.expect(
        api.model(
            "UserInput",
            {
                "first_name": fields.String(required=True),
                "last_name": fields.String(required=True),
                "email": fields.String(required=True),
                "password": fields.String(required=True),
            },
        )
    )
    @api.response(201, "User created successfully")
    @api.response(400, "Validation Error")
    @api.response(409, "Email already registered")
    def post(self):
        """Create a new user"""
        try:
            # Vérifiez si l'email existe déjà
            if facade.get_user_by_email(api.payload["email"]):
                return {"message": "Email already registered"}, 409

            new_user = facade.create_user(api.payload)
            return {
                "message": "User created successfully",
                "id": new_user.id,
            }, 201
        except ValueError as e:
            return {"message": str(e)}, 400
        except Exception as e:
            api.abort(500, str(e))


@api.route("/<string:user_id>")
@api.param("user_id", "The user identifier")
class User(Resource):
    @api.doc("get_user")
    @api.marshal_with(user_model)
    @jwt_required()
    def get(self, user_id):
        """Fetch a user by ID"""
        try:
            # Assurez-vous que cette méthode existe
            user = facade.get_user(user_id)
            if user is None:
                api.abort(404, f"User {user_id} not found")
            return user
        except Exception as e:
            api.abort(500, str(e))

    @api.doc("update_user")
    @api.expect(user_model)
    @jwt_required()
    def put(self, user_id):
        """Update a user"""
        current_user = get_jwt_identity()

        # Vérifiez si l'utilisateur a les droits nécessaires
        if current_user["id"] != user_id and not current_user.get(
            "is_admin", False
        ):
            return {"message": "Access denied"}, 403

        try:
            updated_user = facade.update_user(user_id, api.payload)
            return updated_user
        except ValueError as e:
            api.abort(400, str(e))
