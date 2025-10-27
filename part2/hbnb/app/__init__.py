from flask import Flask
from flask_restx import Api, Resource

from .api.v1.reviews import api as reviews_ns 
from .api.v1.places import api as places_ns 
from .api.v1.amenities import api as amenities_ns
from .api.v1.users import api as users_ns

def create_app():
    app = Flask(__name__)
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API', doc='/api/v1/')

 
    # Register all API namespaces
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(users_ns, path='/api/v1/users')

    @api.route('/')
    class WelcomeResource(Resource):
        def get(self):
            return {"message": "Welcome to HBNB API - Visit /api/v1/ for documentation"}
    
    # Hello endpoint (tu peux garder si tu veux)
    @api.route('/hello')
    class HelloResource(Resource):
        def get(self):
            return {"message": "Hello from HBNB API"}
    
    return app