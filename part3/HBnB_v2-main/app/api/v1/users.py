from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user')
})

admin_user_update_model = api.model('AdminUserUpdate', {
    'first_name': fields.String(required=False, description='First name of the user'),
    'last_name': fields.String(required=False, description='Last name of the user'),
    'email': fields.String(required=False, description='Email of the user'),
    'password': fields.String(required=False, description='Password of the user')
})

@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new user"""
        user_data = api.payload

        
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        try:
            new_user = facade.create_user(user_data)
            return new_user.to_dict(exclude = ['password']), 201
        except Exception as e:
            return {'error': str(e)}, 400
        
    @api.response(200, 'List of users retrieved successfully')
    def get(self):
        """Retrieve a list of users"""
        users = facade.get_users()
        return [user.to_dict(exclude = ['password']) for user in users], 200
    
@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        """ Exclude Password in Response """
        return user.to_dict(exclude = ['password']), 200

    @api.expect(user_model)
    @api.response(200, 'User updated successfully')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def put(self, user_id):
        current_user = get_jwt_identity()
        user_data = api.payload

        if user_id != current_user:
            return {'error': 'Unauthorized action'}, 403
        
        if 'email' in user_data or 'password' in user_data:
            return {'error': 'You cannot modify email or password'}, 400
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        try:
            facade.update_user(user_id, user_data)
            return user.to_dict(exclude = ['password']), 200
        except Exception as e:
            return {'error': str(e)}, 400

@api.route('/admin/')
class AdminUserCreate(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created by admin')
    @api.response(400, 'Email already registered')
    @api.response(403, 'Admin privileges required')
    @jwt_required()
    def post(self):
        """Create a new user (admin only)"""
        claims = get_jwt()  
        
        
        if not claims.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        user_data = api.payload
        email = user_data.get('email')

        
        existing_user = facade.get_user_by_email(email)
        if existing_user:
            return {'error': 'Email already registered'}, 400

        try:
            new_user = facade.create_user(user_data)
            return {
                'message': 'User created successfully via admin endpoint',
                'user': new_user.to_dict(exclude=['password'])
            }, 201
        except Exception as e:
            return {'error': str(e)}, 400
@api.route('/admin/<user_id>')
class AdminUserResource(Resource):
    @api.expect(admin_user_update_model)
    @api.response(200, 'User updated successfully by admin')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Admin privileges required')
    @jwt_required()
    def put(self, user_id):
        """Update any user details (admin only)"""
        claims = get_jwt()  
        
        if not claims.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        data = api.payload
        email = data.get('email')

        if email:
            
            existing_user = facade.get_user_by_email(email)
            if existing_user and existing_user.id != user_id:
                return {'error': 'Email is already in use'}, 400

        try:
            updated_user = facade.update_user(user_id, data)
            return updated_user.to_dict(exclude=['password']), 200
        except Exception as e:
            return {'error': str(e)}, 400
