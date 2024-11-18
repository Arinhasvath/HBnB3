from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.facade import facade

api = Namespace("reviews", description="Review operations")

review_model = api.model(
    "Review",
    {
        "id": fields.String(readonly=True, description="Review identifier"),
        "text": fields.String(required=True, description="Review content"),
        "rating": fields.Integer(
            required=True, description="Rating (1-5)", min=1, max=5
        ),
        "place_id": fields.String(
            required=True, description="Place identifier"
        ),
        "user_id": fields.String(readonly=True, description="User identifier"),
    },
)


@api.route("/")
class ReviewList(Resource):
    @api.doc("list_reviews")
    @api.marshal_list_with(review_model)
    def get(self):
        """List all reviews - Public endpoint"""
        return facade.get_all_reviews()

    @api.doc("create_review")
    @api.expect(review_model)
    @api.marshal_with(review_model, code=201)
    @jwt_required()
    def post(self):
        """Create a new review - Authenticated users only"""
        try:
            current_user = get_jwt_identity()
            review_data = api.payload
            place_id = review_data.get("place_id")

            # Vérifier si le lieu existe
            place = facade.get_place(place_id)
            if not place:
                api.abort(404, "Place not found")

            # Vérifier que l'utilisateur n'est pas le propriétaire
            if str(place.owner_id) == str(current_user.get("id")):
                api.abort(400, "You cannot review your own place")

            # Vérifier si l'utilisateur a déjà reviewé ce lieu
            existing_review = facade.get_user_review_for_place(
                current_user.get("id"), place_id
            )
            if existing_review:
                api.abort(400, "You have already reviewed this place")

            # Ajouter l'ID utilisateur
            review_data["user_id"] = current_user.get("id")
            return facade.create_review(review_data), 201

        except ValueError as e:
            api.abort(400, str(e))


@api.route("/<string:review_id>")
@api.param("review_id", "The review identifier")
class Review(Resource):
    @api.doc("get_review")
    @api.marshal_with(review_model)
    def get(self, review_id):
        """Get a review by ID - Public endpoint"""
        review = facade.get_review(review_id)
        if not review:
            api.abort(404, "Review not found")
        return review

    @api.doc("update_review")
    @api.expect(review_model)
    @api.marshal_with(review_model)
    @jwt_required()
    def put(self, review_id):
        """Update a review - Author only"""
        try:
            current_user = get_jwt_identity()
            review = facade.get_review(review_id)

            if not review:
                api.abort(404, "Review not found")

            # Vérifier que l'utilisateur est l'auteur
            if str(review.user_id) != str(current_user.get("id")):
                api.abort(403, "Unauthorized action")

            # Empêcher la modification du place_id
            if (
                "place_id" in api.payload
                and api.payload["place_id"] != review.place_id
            ):
                api.abort(400, "Cannot change the place of a review")

            return facade.update_review(review_id, api.payload)

        except ValueError as e:
            api.abort(400, str(e))

    @api.doc("delete_review")
    @api.response(204, "Review deleted")
    @jwt_required()
    def delete(self, review_id):
        """Delete a review - Author only"""
        try:
            current_user = get_jwt_identity()
            review = facade.get_review(review_id)

            if not review:
                api.abort(404, "Review not found")

            # Vérifier que l'utilisateur est l'auteur
            if str(review.user_id) != str(current_user.get("id")):
                api.abort(403, "Unauthorized action")

            facade.delete_review(review_id)
            return "", 204

        except Exception as e:
            api.abort(500, str(e))


@api.route("/places/<string:place_id>/reviews")
@api.param("place_id", "The place identifier")
class PlaceReviews(Resource):
    @api.doc("get_place_reviews")
    @api.marshal_list_with(review_model)
    def get(self, place_id):
        """Get all reviews for a specific place - Public endpoint"""
        place = facade.get_place(place_id)
        if not place:
            api.abort(404, "Place not found")
        return facade.get_reviews_by_place(place_id)
