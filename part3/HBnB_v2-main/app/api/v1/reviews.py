from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

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
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        """Register a new review"""
        current_user = get_jwt_identity()
        review_data = api.payload
        review_data['user_id'] = current_user
        place = facade.get_place(review_data['place_id'])
        if not place:
            return {'error': 'Place not found'}, 400
        user = facade.get_user(review_data['user_id'])
        if not user:
            return {'error': 'User not found'}, 400
        if place.owner.id == current_user:
            return {'error': 'User cannot review their own place'}, 400
        """Check for duplicate review """
        existing_reviews = facade.get_reviews_by_place(review_data['place_id'])
        user_review = [r for r in existing_reviews if r.user.id == current_user]
        if user_review:
            return {'error': 'You have already reviewed this place'}, 400
    
        try:
            new_review = facade.create_review(review_data)
            return new_review.to_dict(), 201
        except Exception as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        return [review.to_dict() for review in facade.get_all_reviews()], 200

@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        return review.to_dict(), 200

    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def put(self, review_id):
        """Update a review's information"""
        current_user_id = get_jwt_identity()
        claims = get_jwt()  # Get JWT claims to check admin status
        
        review_data = api.payload
        review = facade.get_review(review_id)
        
        if not review:
            return {'error': 'Review not found'}, 404
        
        # Allow admins to bypass ownership check
        if not claims.get('is_admin') and review.user.id != current_user_id:
            return {'error': 'Unauthorized action'}, 403
        
        try:
            facade.update_review(review_id, review_data)
            return {'message': 'Review updated successfully'}, 200
        except Exception as e:
            return {'error': str(e)}, 400

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    @jwt_required()
    def delete(self, review_id):
        """Delete a review"""
        current_user_id = get_jwt_identity()
        claims = get_jwt()  # Get JWT claims to check admin status
        
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        
        # Allow admins to bypass ownership check
        if not claims.get('is_admin') and review.user.id != current_user_id:
            return {'error': 'Unauthorized action'}, 403
        
        try:
            facade.delete_review(review_id)
            return {'message': 'Review deleted successfully'}, 200
        except Exception as e:
            return {'error': str(e)}, 400