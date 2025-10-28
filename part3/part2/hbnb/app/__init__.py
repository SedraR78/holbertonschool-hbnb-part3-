from flask import Flask
from flask_restx import Api, Resource
from config import config
from .api.v1.reviews import api as reviews_ns
from .api.v1.places import api as places_ns
from .api.v1.amenities import api as amenities_ns
from .api.v1.users import api as users_ns


def create_app(config_name="default"):
    """Create Flask app and register API namespaces based on config."""
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    api = Api(
        app,
        version="1.0",
        title="HBnB API",
        description="HBnB Application API",
        doc="/api/v1/",  # Swagger UI at /api/v1/
    )

    # Register API namespaces
    api.add_namespace(places_ns, path="/api/v1/places")
    api.add_namespace(reviews_ns, path="/api/v1/reviews")
    api.add_namespace(amenities_ns, path="/api/v1/amenities")
    api.add_namespace(users_ns, path="/api/v1/users")

    # Simple root endpoint
    @api.route("/")
    class WelcomeResource(Resource):
        def get(self):
            return {"message": "Welcome to HBNB API - Visit /api/v1/ for documentation"}

    # Another simple test endpoint
    @api.route("/hello")
    class HelloResource(Resource):
        def get(self):
            return {"message": "Hello from HBNB API"}

    return app
