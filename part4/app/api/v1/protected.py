from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

api = Namespace('protected', description='Protected endpoints', security='Bearer Auth')

# Response model
protected_response = api.model('ProtectedResponse', {
    'message': fields.String(description='Response message'),
    'is_admin': fields.Boolean(description='Admin status from token')
})

@api.route('/')
class ProtectedResource(Resource):
    @api.doc(
        security='Bearer Auth',  
        description='Protected endpoint - requires valid JWT token. Click Authorize button first!',
        responses={
            200: 'Success - Returns user identity and admin status',
            401: 'Unauthorized - Missing or invalid token'
        }
    )
    @api.response(200, 'Success', protected_response)
    @api.response(401, 'Unauthorized')
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