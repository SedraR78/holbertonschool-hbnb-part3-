from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from app.services.facade import HBnBFacade

api = Namespace('auth', description='Authentication operations')
facade = HBnBFacade()

# Login model
login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email', example='Valentin.D@example.com'),
    'password': fields.String(required=True, description='User password', example='SecureWord789*')
})

@api.route('/login')
class Login(Resource):
    """Handles user authentication and JWT generation."""

    @api.expect(login_model, validate=True)
    def post(self):
        creds = api.payload
        user = facade.get_user_by_email(creds['email'])

        if not user or not user.verify_password(creds['password']):
            return {'error': 'Invalid credentials'}, 401

        token = create_access_token(
            identity=str(user.id),
            additional_claims={'is_admin': user.is_admin}
        )

        return {
            'access_token': token,
            'user': {
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'is_admin': user.is_admin
            }
        }, 200


@api.route('/protected')
class ProtectedResource(Resource):
    """Example of a JWT-protected endpoint."""

    @api.doc(security='Bearer')
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        is_admin = get_jwt().get('is_admin', False)
        return {'message': f'Hello, {user_id}', 'user_id': user_id, 'is_admin': is_admin}, 200


@api.route('/admin-only')
class AdminOnlyResource(Resource):
    """Admin-only protected endpoint."""

    @api.doc(security='Bearer')
    @jwt_required()
    def get(self):
        claims = get_jwt()
        if not claims.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        return {
            'message': 'Welcome, admin!',
            'user_id': get_jwt_identity(),
            'admin_data': 'This is sensitive admin information'
        }, 200
