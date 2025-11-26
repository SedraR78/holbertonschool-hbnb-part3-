from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token
from app.services import facade
from app.models.user import User

api = Namespace('auth', description='Authentication operations', security=[])

"""
Login request model for input validation
"""
login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

@api.route('/login')
class Login(Resource):
    @api.expect(login_model)
    def post(self):
        """
        Authenticate user and return JWT token
        - Verifies email/password credentials
        - Returns access token for authenticated requests
        """
        credentials = api.payload
        
        """Step 1: Find user by email"""
        user = facade.get_user_by_email(credentials['email'])
        
        """Step 2: Verify user exists and password matches"""
        user_obj: User = user
        if not user or not user_obj.verify_password(credentials['password']):
            return {'error': 'Invalid credentials'}, 401

        """Step 3: Generate JWT token with user identity and admin status"""
        access_token = create_access_token(
            identity=str(user.id),
            additional_claims={"is_admin": user.is_admin}
        )
        
        """Step 4: Return access token to client"""
        return {
            'access_token': access_token,
            'token_type': 'bearer'
        }, 200