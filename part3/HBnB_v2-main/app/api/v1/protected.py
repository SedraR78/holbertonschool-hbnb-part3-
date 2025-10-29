from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

api = Namespace('protected', description='Protected endpoints')

@api.route('/')
class ProtectedResource(Resource):
    @jwt_required()
    def get(self):
        """A protected endpoint that requires a valid JWT token"""
        current_user = get_jwt_identity()  # Retrieve the user's identity from the token
        
        # If you need to see if the user is an admin or not, you can access additional claims using get_jwt()
        claims = get_jwt()
        
        return {
            'message': f'Hello, user {current_user}',
            'is_admin': claims.get('is_admin', False)
        }, 200