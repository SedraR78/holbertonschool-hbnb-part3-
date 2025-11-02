"""
Review endpoints for the HBnB API.
Handles CRUD operations for reviews (Create, Read, Update, Delete).
"""
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import facade

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})


@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model, validate=True)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(404, 'User or Place not found')
    @jwt_required()
    def post(self):
        """
        Register a new review.
        Requires JWT authentication.
        The authenticated user is set as the review author.
        """
        review_data = api.payload
        current_user_id = get_jwt_identity()
        
        # Override user_id with authenticated user
        review_data['user_id'] = current_user_id

        # Validate text is not empty
        if not review_data.get('text') or not review_data.get('text').strip():
            return {'error': 'Review text is required'}, 400
        
        # Validate rating is between 1 and 5
        rating = review_data.get('rating')
        if rating is None or rating < 1 or rating > 5:
            return {'error': 'Rating must be between 1 and 5'}, 400
        
        # Check if place exists
        place = facade.get_place(review_data.get('place_id'))
        if not place:
            return {'error': 'Place not found'}, 404
        
        # Prevent users from reviewing their own places
        if place.owner.id == current_user_id:
            return {'error': 'You cannot review your own place'}, 400

        try:
            new_review = facade.create_review(review_data)
            return {
                'id': new_review.id,
                'text': new_review.text,
                'rating': new_review.rating,
                'user_id': new_review.user.id,
                'place_id': new_review.place.id,
                'created_at': new_review.created_at.isoformat(),
                'updated_at': new_review.updated_at.isoformat()
            }, 201
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """
        Retrieve a list of all reviews.
        Public endpoint - no authentication required.
        """
        reviews = facade.get_all_reviews()
        return [
            {
                'id': review.id,
                'text': review.text,
                'rating': review.rating,
                'user_id': review.user.id,
                'place_id': review.place.id
            }
            for review in reviews
        ], 200


@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """
        Get review details by ID.
        Public endpoint - no authentication required.
        """
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        
        return {
            'id': review.id,
            'text': review.text,
            'rating': review.rating,
            'user_id': review.user.id,
            'place_id': review.place.id,
            'created_at': review.created_at.isoformat(),
            'updated_at': review.updated_at.isoformat()
        }, 200

    @api.expect(review_model, validate=True)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized action')
    @jwt_required()
    def put(self, review_id):
        """
        Update a review's information.
        - Regular users can only update their own reviews
        - Admins can update any review (bypass ownership)
        """
        review_data = api.payload
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)

        # Check if review exists
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        
        # Check authorship or admin status (ADMIN BYPASS)
        if not is_admin and review.user.id != current_user_id:
            return {'error': 'Unauthorized action - You can only modify your own reviews'}, 403

        # Validate text is not empty
        if not review_data.get('text') or not review_data.get('text').strip():
            return {'error': 'Review text is required'}, 400
        
        # Validate rating is between 1 and 5
        rating = review_data.get('rating')
        if rating is None or rating < 1 or rating > 5:
            return {'error': 'Rating must be between 1 and 5'}, 400
        
        # Prevent changing user_id and place_id
        review_data.pop('user_id', None)
        review_data.pop('place_id', None)

        try:
            updated_review = facade.update_review(review_id, review_data)
            return {
                'id': updated_review.id,
                'text': updated_review.text,
                'rating': updated_review.rating,
                'user_id': updated_review.user.id,
                'place_id': updated_review.place.id,
                'created_at': updated_review.created_at.isoformat(),
                'updated_at': updated_review.updated_at.isoformat()
            }, 200
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    @api.response(403, 'Unauthorized action')
    @jwt_required()
    def delete(self, review_id):
        """
        Delete a review.
        - Regular users can only delete their own reviews
        - Admins can delete any review (bypass ownership)
        """
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)
        
        # Check if review exists
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        
        # Check authorship or admin status (ADMIN BYPASS)
        if not is_admin and review.user.id != current_user_id:
            return {'error': 'Unauthorized action - You can only delete your own reviews'}, 403
        
        facade.delete_review(review_id)
        return {'message': 'Review deleted successfully'}, 200


@api.route('/places/<place_id>')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """
        Get all reviews for a specific place.
        Public endpoint - no authentication required.
        """
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        
        reviews = facade.get_reviews_by_place(place_id)
        return [
            {
                'id': review.id,
                'text': review.text,
                'rating': review.rating,
                'user_id': review.user.id
            }
            for review in reviews
        ], 200