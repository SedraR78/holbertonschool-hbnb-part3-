from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

api = Namespace('protected', description='Protected endpoints')

@api.route('/')
class ProtectedResource(Resource):
    @jwt_required()
    def get(self):
        """
        Protected endpoint - requires valid JWT token
        Returns user identity and admin status from token claims
        """
        current_user = get_jwt_identity()
        claims = get_jwt()
        
        return {
            'message': f'Hello, user {current_user}',
            'is_admin': claims.get('is_admin', False)
        }, 200