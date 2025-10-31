from flask import Flask
from flask_restx import Api, Resource
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from config import config

from .api.v1.reviews import api as reviews_ns
from .api.v1.places import api as places_ns
from .api.v1.amenities import api as amenities_ns
from .api.v1.users import api as users_ns

bcrypt = Bcrypt()
jwt = JWTManager()

def create_app(config_name="default"):
    """Create and configure the Flask app."""
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Initialize extensions
    bcrypt.init_app(app)
    jwt.init_app(app)

    # API setup with Swagger UI
    api = Api(
        app,
        version="1.0",
        title="HBnB API",
        description="HBnB Application API",
        doc="/api/v1/",
        authorizations={
            'Bearer': {
                'type': 'apiKey',
                'in': 'header',
                'name': 'Authorization',
                'description': "Enter: **Bearer &lt;JWT&gt;**"
            }
        },
        security='Bearer'
    )

    # Register Namespaces
    api.add_namespace(places_ns, path="/api/v1/places")
    api.add_namespace(reviews_ns, path="/api/v1/reviews")
    api.add_namespace(amenities_ns, path="/api/v1/amenities")
    api.add_namespace(users_ns, path="/api/v1/users")

    # Root endpoint
    @api.route("/")
    class Welcome(Resource):
        def get(self):
            return {
                "message": "Welcome to HBnB API",
                "documentation": "/api/v1/",
                "version": "1.0",
                "endpoints": {
                    "auth": "/api/v1/auth",
                    "users": "/api/v1/users",
                    "places": "/api/v1/places",
                    "reviews": "/api/v1/reviews",
                    "amenities": "/api/v1/amenities"
                }
            }

    # Hello test route
    @api.route("/hello")
    class Hello(Resource):
        def get(self):
            return {"message": "Hello from HBnB API"}

    # Health check
    @api.route("/health")
    class Health(Resource):
        def get(self):
            return {
                "status": "healthy",
                "bcrypt_initialized": isinstance(bcrypt, Bcrypt),
                "jwt_initialized": isinstance(jwt, JWTManager)
            }

    return app
