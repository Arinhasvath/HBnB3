from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token
from app.services.facade import facade
from flask import Flask, request, jsonify
from app.models.user import User
from app import db

api = Namespace("auth", description="Authentication operations")

login_model = api.model(
    "Login",
    {
        "email": fields.String(required=True, description="User email"),
        "password": fields.String(required=True, description="User password"),
    },
)


@app.route("/api/users", methods=["POST"])
def create_user():
    data = request.get_json()
    try:
        new_user = User(
            username=data["username"],
            password=data["password"],
            email=data["email"],
        )
        db.session.add(new_user)
        db.session.commit()
        return (
            jsonify(
                {
                    "message": "User created successfully",
                    "user": new_user.to_dict(),
                }
            ),
            201,
        )
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400


@api.route("/login")
class Login(Resource):
    @api.expect(login_model)
    @api.response(200, "Login successful")
    @api.response(401, "Authentication failed")
    @api.response(400, "Validation Error")
    def post(self):
        """Authenticate user and return JWT token"""
        try:
            print(
                f"Login attempt received with payload: {
                    api.payload}"
            )  # Debug log

            if not api.payload:
                print("No payload received")  # Debug log
                return {"message": "Missing login credentials"}, 400

            if "email" not in api.payload or "password" not in api.payload:
                print("Missing email or password in payload")  # Debug log
                return {"message": "Email and password are required"}, 400

            email = api.payload["email"].strip()
            password = api.payload["password"]

            print(f"Looking for user with email: {email}")  # Debug log

            user = facade.get_user_by_email(email)

            if not user:
                print(f"No user found with email: {email}")  # Debug log
                return {"message": "Invalid credentials"}, 401

            print(f"Found user: {user.email}, verifying password")  # Debug log

            if not user.verify_password(password):
                print("Password verification failed")  # Debug log
                return {"message": "Invalid credentials"}, 401

            token_data = {
                "id": str(user.id),
                "is_admin": getattr(user, "is_admin", False),
            }

            access_token = create_access_token(identity=token_data)

            print("Login successful, token generated")  # Debug log

            return {
                "access_token": access_token,
                "token_type": "Bearer",
                "user": {
                    "id": str(user.id),
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                },
            }, 200

        except Exception as e:
            print(f"Login error: {str(e)}")  # Debug log
            return {"message": f"Error during login: {str(e)}"}, 500
