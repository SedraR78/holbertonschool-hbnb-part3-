from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt

api = Namespace('amenities', description='Amenity operations', security='Bearer Auth')

""" Define the amenity model for input validation and documentation """
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

@api.route('/')
class AmenityList(Resource):
    @api.doc(security=[])
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new amenity"""
        amenity_data = api.payload
        
        existing_amenity = facade.amenity_repo.get_by_attribute('name', amenity_data.get('name'))
        if existing_amenity:
            return {'error': 'Invalid input data'}, 400
        try:
            new_amenity = facade.create_amenity(amenity_data)
            return new_amenity.to_dict(), 201
        except Exception as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of amenities retrieved successfully')
    @api.doc(security=[])
    def get(self):
        """Retrieve a list of all amenities"""
        amenities = facade.get_all_amenities()
        return [amenity.to_dict() for amenity in amenities], 200


@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.doc(security=[])
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        return amenity.to_dict(), 200

    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        amenity_data = api.payload
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        try:
            facade.update_amenity(amenity_id, amenity_data)
            return {"message": "Amenity updated successfully"}, 200
        except Exception as e:
            return {'error': str(e)}, 400


@api.route('/admin/')
class AdminAmenityCreate(Resource):
    @api.expect(amenity_model, validate=True)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Amenity name already exists')
    @api.response(403, 'Admin privileges required')
    @jwt_required()
    def post(self):
        """Add a new amenity (admin only)"""
        claims = get_jwt()
        
        if not claims.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        amenity_data = api.payload
        name = amenity_data.get('name')

        """ Check if amenity name already exists """
        existing_amenity = facade.get_amenity_by_name(name)
        if existing_amenity:
            return {'error': 'Amenity name already exists'}, 400

        try:
            new_amenity = facade.create_amenity(amenity_data)
            return new_amenity.to_dict(), 201
        except Exception as e:
            return {'error': str(e)}, 400

@api.route('/admin/<amenity_id>')
class AdminAmenityResource(Resource):
    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Admin privileges required')
    @jwt_required()
    def put(self, amenity_id):
        """Modify the details of an amenity (admin only)"""
        claims = get_jwt()
        
        if not claims.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        amenity_data = api.payload

        """ Check if amenity exists """
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404

        """ Check name uniqueness if name is being changed """
        if 'name' in amenity_data and amenity_data['name'] != amenity.name:
            existing_amenity = facade.get_amenity_by_name(amenity_data['name'])
            if existing_amenity:
                return {'error': 'Amenity name already exists'}, 400

        try:
            updated_amenity = facade.update_amenity(amenity_id, amenity_data)
            return updated_amenity.to_dict(), 200
        except Exception as e:
            return {'error': str(e)}, 400
