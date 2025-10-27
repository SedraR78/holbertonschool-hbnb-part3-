from flask_restx import Namespace, Resource, fields
from hbnb.app.services import facade

api = Namespace('amenities', description='Amenity operations')

amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

@api.route('/')
class AmenityList(Resource):
    """Handle operations for the list of amenities"""
    
    @api.expect(amenity_model)
    def post(self):
        """Create a new amenity"""
        data = api.payload
        try:
            amenity = facade.create_amenity(data)
            return amenity.to_dict(), 201
        except ValueError as e:
            return {'error': str(e)}, 400
    
    def get(self):
        """Retrieve all amenities"""
        amenities = facade.get_all_amenities()
        return [amenity.to_dict() for amenity in amenities], 200

@api.route('/<amenity_id>')
class AmenityResource(Resource):
    """Handle operations for a specific amenity"""
    
    def get(self, amenity_id):
        """Get details of a specific amenity by ID"""
        amenity = facade.get_amenity(amenity_id)
        if amenity:
            return amenity.to_dict(), 200
        return {'error': 'Amenity not found'}, 404
    
    @api.expect(amenity_model)
    def put(self, amenity_id):
        """Update an amenity's information"""
        data = api.payload
        try:
            amenity = facade.update_amenity(amenity_id, data)
            return amenity.to_dict(), 200
        except ValueError as e:
            if "not found" in str(e).lower():
                return {'error': 'Amenity not found'}, 404
            return {'error': str(e)}, 400
    
    def delete(self, amenity_id):
        """Delete an amenity by ID"""
        try:
            result = facade.delete_amenity(amenity_id)
            return result, 200
        except ValueError as e:
            return {'error': str(e)}, 404