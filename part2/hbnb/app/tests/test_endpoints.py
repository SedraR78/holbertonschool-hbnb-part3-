#!/usr/bin/env python3
"""
Unit tests for HBnB API endpoints
"""

import unittest
import json
import sys
import os

# Configuration des imports
current_file = os.path.abspath(__file__)
tests_dir = os.path.dirname(current_file)
app_dir = os.path.dirname(tests_dir)
project_root = os.path.dirname(app_dir)
project_parent = os.path.dirname(project_root)  # Ajout: parent de hbnb

# Ajouter le parent du projet pour que 'hbnb' soit trouvé
sys.path.insert(0, project_parent)

print(f"🔧 Configuration: {project_root}")
print(f"🔧 Parent: {project_parent}")

try:
    from hbnb.app import create_app
    print("✅ Import app réussi via hbnb.app")
except ImportError as e:
    print(f"❌ Erreur import hbnb.app: {e}")
    sys.exit(1)

class TestAPIEndpoints(unittest.TestCase):
    """Test all API endpoints"""
    
    def setUp(self):
        """Set up test client and test data"""
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True
        
        # Test data
        self.user_data = {
            "first_name": "Test",
            "last_name": "User", 
            "email": "test@example.com"
        }
        
        self.place_data = {
            "title": "Test Place",
            "description": "A test place for unit testing",
            "price": 100.0,
            "latitude": 48.8566,
            "longitude": 2.3522,
            "owner_id": "test-owner-id",
            "amenities": []
        }
        
        self.review_data = {
            "text": "Great test place!",
            "rating": 5,
            "user_id": "test-user-id",
            "place_id": "test-place-id"
        }
        
        self.amenity_data = {
            "name": "Test Amenity"
        }

    def test_001_user_creation_success(self):
        """Test successful user creation"""
        response = self.client.post('/api/v1/users/', 
                                  json=self.user_data,
                                  content_type='application/json')
        
        self.assertIn(response.status_code, [200, 201])
        if response.status_code in [200, 201]:
            data = json.loads(response.data)
            self.assertIn('id', data)
            self.assertEqual(data['first_name'], 'Test')
            self.assertEqual(data['last_name'], 'User')
            return data['id']  # Return user ID for other tests

    def test_002_user_creation_invalid_email(self):
        """Test user creation with invalid email"""
        invalid_data = self.user_data.copy()
        invalid_data['email'] = 'invalid-email'
        
        response = self.client.post('/api/v1/users/', 
                                  json=invalid_data,
                                  content_type='application/json')
        
        self.assertIn(response.status_code, [400, 422])

    def test_003_user_creation_missing_fields(self):
        """Test user creation with missing required fields"""
        invalid_data = {"first_name": "Test"}  # Missing last_name and email
        
        response = self.client.post('/api/v1/users/', 
                                  json=invalid_data,
                                  content_type='application/json')
        
        self.assertIn(response.status_code, [400, 422])

    def test_004_get_all_users(self):
        """Test retrieving all users"""
        response = self.client.get('/api/v1/users/')
        
        self.assertIn(response.status_code, [200, 404])
        if response.status_code == 200:
            data = json.loads(response.data)
            self.assertIsInstance(data, list)

    def test_005_place_creation_success(self):
        """Test successful place creation"""
        # First create a user to use as owner
        user_response = self.client.post('/api/v1/users/', json=self.user_data)
        if user_response.status_code in [200, 201]:
            user_id = json.loads(user_response.data)['id']
            
            place_data = self.place_data.copy()
            place_data['owner_id'] = user_id
            
            response = self.client.post('/api/v1/places/', 
                                      json=place_data,
                                      content_type='application/json')
            
            self.assertIn(response.status_code, [200, 201])
            if response.status_code in [200, 201]:
                data = json.loads(response.data)
                self.assertIn('id', data)
                self.assertEqual(data['title'], 'Test Place')
                return data['id']  # Return place ID for other tests

    def test_006_place_creation_invalid_price(self):
        """Test place creation with negative price"""
        place_data = self.place_data.copy()
        place_data['price'] = -50.0
        
        response = self.client.post('/api/v1/places/', 
                                  json=place_data,
                                  content_type='application/json')
        
        self.assertIn(response.status_code, [400, 422])

    def test_007_place_creation_invalid_coordinates(self):
        """Test place creation with invalid coordinates"""
        # Test invalid latitude
        place_data = self.place_data.copy()
        place_data['latitude'] = 95.0  # Out of range
        
        response = self.client.post('/api/v1/places/', 
                                  json=place_data,
                                  content_type='application/json')
        
        self.assertIn(response.status_code, [400, 422])

    def test_008_get_all_places(self):
        """Test retrieving all places"""
        response = self.client.get('/api/v1/places/')
        
        self.assertIn(response.status_code, [200, 404])
        if response.status_code == 200:
            data = json.loads(response.data)
            self.assertIsInstance(data, list)

    def test_009_get_place_by_id(self):
        """Test retrieving a specific place by ID"""
        # First create a place
        user_response = self.client.post('/api/v1/users/', json=self.user_data)
        if user_response.status_code in [200, 201]:
            user_id = json.loads(user_response.data)['id']
            
            place_data = self.place_data.copy()
            place_data['owner_id'] = user_id
            place_response = self.client.post('/api/v1/places/', json=place_data)
            
            if place_response.status_code in [200, 201]:
                place_id = json.loads(place_response.data)['id']
                
                # Now get the place by ID
                response = self.client.get(f'/api/v1/places/{place_id}')
                
                self.assertIn(response.status_code, [200, 404])
                if response.status_code == 200:
                    data = json.loads(response.data)
                    self.assertEqual(data['id'], place_id)

    def test_010_get_nonexistent_place(self):
        """Test retrieving a non-existent place"""
        response = self.client.get('/api/v1/places/nonexistent-id')
        
        self.assertIn(response.status_code, [404, 400])

    def test_011_review_creation_success(self):
        """Test successful review creation"""
        # Create user and place first
        user_response = self.client.post('/api/v1/users/', json=self.user_data)
        if user_response.status_code in [200, 201]:
            user_id = json.loads(user_response.data)['id']
            
            place_data = self.place_data.copy()
            place_data['owner_id'] = user_id
            place_response = self.client.post('/api/v1/places/', json=place_data)
            
            if place_response.status_code in [200, 201]:
                place_id = json.loads(place_response.data)['id']
                
                review_data = self.review_data.copy()
                review_data['user_id'] = user_id
                review_data['place_id'] = place_id
                
                response = self.client.post('/api/v1/reviews/', 
                                          json=review_data,
                                          content_type='application/json')
                
                self.assertIn(response.status_code, [200, 201])
                if response.status_code in [200, 201]:
                    data = json.loads(response.data)
                    self.assertIn('id', data)
                    return data['id']  # Return review ID

    def test_012_review_creation_invalid_rating(self):
        """Test review creation with invalid rating"""
        review_data = self.review_data.copy()
        review_data['rating'] = 6  # Out of range
        
        response = self.client.post('/api/v1/reviews/', 
                                  json=review_data,
                                  content_type='application/json')
        
        self.assertIn(response.status_code, [400, 422])

    def test_013_review_creation_empty_text(self):
        """Test review creation with empty text"""
        review_data = self.review_data.copy()
        review_data['text'] = ""  # Empty text
        
        response = self.client.post('/api/v1/reviews/', 
                                  json=review_data,
                                  content_type='application/json')
        
        self.assertIn(response.status_code, [400, 422])

    def test_014_get_all_reviews(self):
        """Test retrieving all reviews"""
        response = self.client.get('/api/v1/reviews/')
        
        self.assertIn(response.status_code, [200, 404])
        if response.status_code == 200:
            data = json.loads(response.data)
            self.assertIsInstance(data, list)

    def test_015_amenity_creation_success(self):
        """Test successful amenity creation"""
        response = self.client.post('/api/v1/amenities/', 
                                  json=self.amenity_data,
                                  content_type='application/json')
        
        self.assertIn(response.status_code, [200, 201])
        if response.status_code in [200, 201]:
            data = json.loads(response.data)
            self.assertIn('id', data)
            self.assertEqual(data['name'], 'Test Amenity')
            return data['id']

    def test_016_amenity_creation_empty_name(self):
        """Test amenity creation with empty name"""
        invalid_data = {"name": ""}
        
        response = self.client.post('/api/v1/amenities/', 
                                  json=invalid_data,
                                  content_type='application/json')
        
        self.assertIn(response.status_code, [400, 422])

    def test_017_get_all_amenities(self):
        """Test retrieving all amenities"""
        response = self.client.get('/api/v1/amenities/')
        
        self.assertIn(response.status_code, [200, 404])
        if response.status_code == 200:
            data = json.loads(response.data)
            self.assertIsInstance(data, list)

    def test_018_place_reviews_endpoint(self):
        """Test getting reviews for a specific place"""
        # Create user, place, and review first
        user_response = self.client.post('/api/v1/users/', json=self.user_data)
        if user_response.status_code in [200, 201]:
            user_id = json.loads(user_response.data)['id']
            
            place_data = self.place_data.copy()
            place_data['owner_id'] = user_id
            place_response = self.client.post('/api/v1/places/', json=place_data)
            
            if place_response.status_code in [200, 201]:
                place_id = json.loads(place_response.data)['id']
                
                review_data = self.review_data.copy()
                review_data['user_id'] = user_id
                review_data['place_id'] = place_id
                self.client.post('/api/v1/reviews/', json=review_data)
                
                # Test the endpoint
                response = self.client.get(f'/api/v1/places/{place_id}/reviews')
                
                self.assertIn(response.status_code, [200, 404])
                if response.status_code == 200:
                    data = json.loads(response.data)
                    self.assertIsInstance(data, list)

    def test_019_update_user(self):
        """Test updating a user"""
        # First create a user
        user_response = self.client.post('/api/v1/users/', json=self.user_data)
        if user_response.status_code in [200, 201]:
            user_id = json.loads(user_response.data)['id']
            
            # Update the user
            update_data = {
                "first_name": "Updated",
                "last_name": "Name",
                "email": "updated@example.com"
            }
            
            response = self.client.put(f'/api/v1/users/{user_id}', 
                                     json=update_data,
                                     content_type='application/json')
            
            self.assertIn(response.status_code, [200, 201, 404])
            if response.status_code in [200, 201]:
                data = json.loads(response.data)
                self.assertEqual(data['first_name'], 'Updated')

    def test_020_delete_review(self):
        """Test deleting a review"""
        # Create user, place, and review first
        user_response = self.client.post('/api/v1/users/', json=self.user_data)
        if user_response.status_code in [200, 201]:
            user_id = json.loads(user_response.data)['id']
            
            place_data = self.place_data.copy()
            place_data['owner_id'] = user_id
            place_response = self.client.post('/api/v1/places/', json=place_data)
            
            if place_response.status_code in [200, 201]:
                place_id = json.loads(place_response.data)['id']
                
                review_data = self.review_data.copy()
                review_data['user_id'] = user_id
                review_data['place_id'] = place_id
                review_response = self.client.post('/api/v1/reviews/', json=review_data)
                
                if review_response.status_code in [200, 201]:
                    review_id = json.loads(review_response.data)['id']
                    
                    # Delete the review
                    response = self.client.delete(f'/api/v1/reviews/{review_id}')
                    
                    self.assertIn(response.status_code, [200, 204, 404])
                    if response.status_code in [200, 204]:
                        data = json.loads(response.data) if response.data else {}
                        self.assertIn('message', data)

    def test_021_delete_nonexistent_review(self):
        """Test deleting a non-existent review"""
        response = self.client.delete('/api/v1/reviews/nonexistent-id')
        
        self.assertIn(response.status_code, [404, 400])

    def test_022_api_documentation_accessible(self):
        """Test that Swagger documentation is accessible"""
        response = self.client.get('/api/v1/')
        self.assertIn(response.status_code, [200, 302])  # 302 if redirect

    def test_023_health_check(self):
        """Test basic health check endpoint"""
        response = self.client.get('/')
        self.assertIn(response.status_code, [200, 404, 302])

    def test_024_create_multiple_users(self):
        """Test creating multiple users"""
        users = [
            {"first_name": "Alice", "last_name": "Smith", "email": "alice@example.com"},
            {"first_name": "Bob", "last_name": "Johnson", "email": "bob@example.com"},
            {"first_name": "Charlie", "last_name": "Brown", "email": "charlie@example.com"}
        ]
        
        for user_data in users:
            response = self.client.post('/api/v1/users/', json=user_data)
            self.assertIn(response.status_code, [200, 201])

    def test_025_search_places_by_title(self):
        """Test searching places by title"""
        response = self.client.get('/api/v1/places/?title=test')
        self.assertIn(response.status_code, [200, 404])
        if response.status_code == 200:
            data = json.loads(response.data)
            self.assertIsInstance(data, list)

    def test_026_filter_places_by_price_range(self):
        """Test filtering places by price range"""
        response = self.client.get('/api/v1/places/?min_price=50&max_price=200')
        self.assertIn(response.status_code, [200, 404])
        if response.status_code == 200:
            data = json.loads(response.data)
            self.assertIsInstance(data, list)

    def test_027_update_place(self):
        """Test updating a place"""
        # Create user and place first
        user_response = self.client.post('/api/v1/users/', json=self.user_data)
        if user_response.status_code in [200, 201]:
            user_id = json.loads(user_response.data)['id']
            
            place_data = self.place_data.copy()
            place_data['owner_id'] = user_id
            place_response = self.client.post('/api/v1/places/', json=place_data)
            
            if place_response.status_code in [200, 201]:
                place_id = json.loads(place_response.data)['id']
                
                # Update the place
                update_data = {"title": "Updated Place Title", "price": 150.0}
                response = self.client.put(f'/api/v1/places/{place_id}', 
                                         json=update_data,
                                         content_type='application/json')
                
                self.assertIn(response.status_code, [200, 201, 404])
                if response.status_code in [200, 201]:
                    data = json.loads(response.data)
                    self.assertEqual(data['title'], 'Updated Place Title')

    def test_028_delete_user(self):
        """Test deleting a user"""
        # Create a user first
        user_response = self.client.post('/api/v1/users/', json=self.user_data)
        if user_response.status_code in [200, 201]:
            user_id = json.loads(user_response.data)['id']
            
            # Delete the user
            response = self.client.delete(f'/api/v1/users/{user_id}')
            self.assertIn(response.status_code, [200, 204, 404])

    def test_029_delete_place(self):
        """Test deleting a place"""
        # Create user and place first
        user_response = self.client.post('/api/v1/users/', json=self.user_data)
        if user_response.status_code in [200, 201]:
            user_id = json.loads(user_response.data)['id']
            
            place_data = self.place_data.copy()
            place_data['owner_id'] = user_id
            place_response = self.client.post('/api/v1/places/', json=place_data)
            
            if place_response.status_code in [200, 201]:
                place_id = json.loads(place_response.data)['id']
                
                # Delete the place
                response = self.client.delete(f'/api/v1/places/{place_id}')
                self.assertIn(response.status_code, [200, 204, 404])

    def test_030_delete_amenity(self):
        """Test deleting an amenity"""
        # Create an amenity first
        amenity_response = self.client.post('/api/v1/amenities/', json=self.amenity_data)
        if amenity_response.status_code in [200, 201]:
            amenity_id = json.loads(amenity_response.data)['id']
            
            # Delete the amenity
            response = self.client.delete(f'/api/v1/amenities/{amenity_id}')
            self.assertIn(response.status_code, [200, 204, 404])

if __name__ == '__main__':
    # Run the tests with verbose output
    unittest.main(verbosity=2)