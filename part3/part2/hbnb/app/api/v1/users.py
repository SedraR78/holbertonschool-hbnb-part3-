# app/api/v1/users.py
"""
User endpoints for the HBnB API.
Handles CRUD operations for users (Create, Read, Update).
"""
from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation (including password)
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user', max_length=50),
    'last_name': fields.String(required=True, description='Last name of the user', max_length=50),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user', min_length=8)
})

# Define a separate model for updates (all fields optional, no password updates here)
user_update_model = api.model('UserUpdate', {
    'first_name': fields.String(required=False, description='First name of the user', max_length=50),
    'last_name': fields.String(required=False, description='Last name of the user', max_length=50),
    'email': fields.String(required=False, description='Email of the user')
})


@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered or invalid input')
    def post(self):
        """Register a new user"""
        user_data = api.payload

        # Password validation (at least 8 characters)
        if not user_data.get('password') or len(user_data['password']) < 8:
            return {'error': 'Password must be at least 8 characters'}, 400

        # Check for email uniqueness
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        try:
            # The password is hashed inside the User model
            new_user = facade.create_user(user_data)
            return new_user.to_dict(), 201  # to_dict() excludes password
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': f'An error occurred: {str(e)}'}, 500

    @api.response(200, 'List of users retrieved successfully')
    def get(self):
        """Retrieve a list of all users"""
        try:
            users = facade.get_all_users()
            return [user.to_dict() for user in users], 200  # Password excluded
        except Exception as e:
            return {'error': f'An error occurred: {str(e)}'}, 500


@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        try:
            user = facade.get_user(user_id)
            if not user:
                return {'error': 'User not found'}, 404

            return user.to_dict(), 200  # Password excluded
        except Exception as e:
            return {'error': f'An error occurred: {str(e)}'}, 500

    @api.expect(user_update_model, validate=True)
    @api.response(200, 'User successfully updated')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data or email already registered')
    def put(self, user_id):
        """Update user information"""
        user_data = api.payload

        if not user_data:
            return {'error': 'No data provided for update'}, 400

        # Check if user exists
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        # Check if email is being changed and if it's already taken by another user
        if 'email' in user_data and user_data['email'] != user.email:
            existing_user = facade.get_user_by_email(user_data['email'])
            if existing_user and existing_user.id != user_id:
                return {'error': 'Email already registered'}, 400

        try:
            updated_user = facade.update_user(user_id, user_data)
            return updated_user.to_dict(), 200
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': f'An error occurred while updating the user: {str(e)}'}, 500
