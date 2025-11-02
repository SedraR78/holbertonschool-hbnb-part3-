"""
Amenity endpoints for the HBnB API.
Handles CRUD operations for amenities (Create, Read, Update).
"""
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import facade

api = Namespace('amenities', description='Amenity operations')

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity', max_length=50)
})

@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model, validate=True)
    @api.response(200, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Admin privileges required')
    @api.response(409, 'Amenity already exists')
    @jwt_required()
    def post(self):
        """
        Register a new amenity.
        ADMIN ONLY: Only administrators can create amenities.
        """
        # Check if current user is admin
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)
        
        if not is_admin:
            return {'error': 'Admin privileges required to create amenities'}, 403
        
        amenity_data = api.payload
        
        # Validate name is not empty
        if not amenity_data.get('name') or not amenity_data.get('name').strip():
            return {'error': 'Amenity name is required and must be a string'}, 400
        
        try:
            # Check if amenity with same name already exists (case-insensitive)
            existing_amenities = facade.get_all_amenities()
            for amenity in existing_amenities:
                if amenity.name.lower().strip() == amenity_data['name'].lower().strip():
                    return {'error': 'Amenity with this name already exists'}, 409
            
            new_amenity = facade.create_amenity(amenity_data)
            return {
                'id': new_amenity.id,
                'name': new_amenity.name,
                'created_at': new_amenity.created_at.isoformat(),
                'updated_at': new_amenity.updated_at.isoformat()
            }, 200
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """
        Retrieve a list of all amenities.
        Public endpoint - no authentication required.
        """
        amenities = facade.get_all_amenities()
        return [
            {
                'id': amenity.id,
                'name': amenity.name,
                'created_at': amenity.created_at.isoformat(),
                'updated_at': amenity.updated_at.isoformat()
            }
            for amenity in amenities
        ], 200


@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """
        Get amenity details by ID.
        Public endpoint - no authentication required.
        """
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        
        return {
            'id': amenity.id,
            'name': amenity.name,
            'created_at': amenity.created_at.isoformat(),
            'updated_at': amenity.updated_at.isoformat()
        }, 200

    @api.expect(amenity_model, validate=True)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Admin privileges required')
    @api.response(409, 'Amenity name already exists')
    @jwt_required()
    def put(self, amenity_id):
        """
        Update an amenity's information.
        ADMIN ONLY: Only administrators can modify amenities.
        """
        # Check if current user is admin
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)
        
        if not is_admin:
            return {'error': 'Admin privileges required to modify amenities'}, 403
        
        amenity_data = api.payload
        
        # Check if amenity exists
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        
        # Validate name is not empty
        if not amenity_data.get('name') or not amenity_data.get('name').strip():
            return {'error': 'Amenity name is required and must be a string'}, 400
        
        try:
            # Check if another amenity with same name already exists (case-insensitive)
            existing_amenities = facade.get_all_amenities()
            for existing_amenity in existing_amenities:
                if (existing_amenity.id != amenity_id and 
                    existing_amenity.name.lower().strip() == amenity_data['name'].lower().strip()):
                    return {'error': 'Amenity with this name already exists'}, 409
            
            updated_amenity = facade.update_amenity(amenity_id, amenity_data)
            return {
                'id': updated_amenity.id,
                'name': updated_amenity.name,
                'created_at': updated_amenity.created_at.isoformat(),
                'updated_at': updated_amenity.updated_at.isoformat()
            }, 200
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'Amenity deleted successfully')
    @api.response(404, 'Amenity not found')
    @api.response(403, 'Admin privileges required')
    @jwt_required()
    def delete(self, amenity_id):
        """
        Delete an amenity.
        ADMIN ONLY: Only administrators can delete amenities.
        """
        # Check if current user is admin
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)
        
        if not is_admin:
            return {'error': 'Admin privileges required to delete amenities'}, 403
        
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        
        # Delete the amenity using facade
        facade.delete_amenity(amenity_id)
        return {'message': 'Amenity deleted successfully'}, 200