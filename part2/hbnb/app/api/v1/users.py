from flask_restx import Namespace, Resource, fields
from hbnb.app.services import facade

api = Namespace('users', description='User operations')

user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name'),
    'last_name': fields.String(required=True, description='Last name'), 
    'email': fields.String(required=True, description='Email address')
})

@api.route('/')
class UserList(Resource):
    @api.expect(user_model)
    def post(self):
        """Create a new user"""
        data = api.payload
        try:
            user = facade.create_user(data)
            return user.to_dict(), 201
        except ValueError as e:
            return {'error': str(e)}, 400
    
    def get(self):
        """Get all users"""
        users = facade.get_all_users()
        return [user.to_dict() for user in users], 200

@api.route('/<user_id>')
class UserResource(Resource):
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if user:
            return user.to_dict(), 200
        return {'error': 'User not found'}, 404
    
    @api.expect(user_model)
    def put(self, user_id):
        """Update user information"""
        data = api.payload
        try:
            user = facade.update_user(user_id, data)
            return user.to_dict(), 200
        except ValueError as e:
            return {'error': str(e)}, 400
        
    def delete(self, user_id):
        """Delete a user by ID"""
        try:
            result = facade.delete_user(user_id)
            return result, 200
        except ValueError as e:
            return {'error': str(e)}, 404