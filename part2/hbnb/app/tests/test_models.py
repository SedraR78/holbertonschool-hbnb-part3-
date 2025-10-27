#!/usr/bin/env python3
"""
Unit tests for HBnB models - VERSION CORRIGÉE
"""

import unittest
import sys
import os

# Configuration des imports - SOLUTION CORRIGÉE
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import direct depuis models/ sans passer par app/
try:
    # Essayer d'importer depuis le dossier models/
    from models.user import User
    from models.place import Place  
    from models.review import Review
    from models.amenity import Amenity
    print("✅ Import réussi depuis models/")
except ImportError as e:
    print(f"❌ Erreur import: {e}")
    # Afficher la structure pour debug
    print("📁 Structure des dossiers:")
    for root, dirs, files in os.walk('.'):
        level = root.replace('.', '').count(os.sep)
        indent = ' ' * 2 * level
        print(f'{indent}{os.path.basename(root)}/')
        for file in files:
            if file.endswith(('.py', '.json')) and not file.startswith('__'):
                print(f'{indent}  📄 {file}')
    sys.exit(1)

class TestModels(unittest.TestCase):
    """Test all model classes and their validation"""
    
    # GARDE TOUS TES TESTS EXISTANTS - ils sont excellents !
    def test_001_user_creation_valid(self):
        """Test creating a valid user"""
        user = User("John", "Doe", "john@example.com")
        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.last_name, "Doe")
        self.assertEqual(user.email, "john@example.com")
        self.assertFalse(user.is_admin)

    def test_002_user_creation_invalid_email(self):
        """Test user creation with invalid email - missing @"""
        with self.assertRaises(ValueError):
            User("John", "Doe", "invalid-email")

    def test_003_user_creation_invalid_email_no_dot(self):
        """Test user creation with invalid email - missing domain dot"""
        with self.assertRaises(ValueError):
            User("John", "Doe", "test@example")

    def test_004_user_creation_long_first_name(self):
        """Test user creation with too long first name"""
        with self.assertRaises(ValueError):
            User("A" * 51, "Doe", "test@example.com")  # First name too long

    def test_005_user_creation_long_last_name(self):
        """Test user creation with too long last name"""
        with self.assertRaises(ValueError):
            User("John", "D" * 51, "test@example.com")  # Last name too long

    def test_006_user_is_admin_default(self):
        """Test that is_admin defaults to False"""
        user = User("John", "Doe", "john@example.com")
        self.assertFalse(user.is_admin)

    def test_007_user_is_admin_true(self):
        """Test creating user with is_admin True"""
        user = User("Admin", "User", "admin@example.com", is_admin=True)
        self.assertTrue(user.is_admin)

    def test_008_place_creation_valid(self):
        """Test creating a valid place"""
        user = User("Owner", "Test", "owner@example.com")
        place = Place(
            title="Beautiful House",
            description="Amazing place with great view",
            price=150.0,
            latitude=48.8566,
            longitude=2.3522,
            owner=user
        )
        
        self.assertEqual(place.title, "Beautiful House")
        self.assertEqual(place.description, "Amazing place with great view")
        self.assertEqual(place.price, 150.0)
        self.assertEqual(place.latitude, 48.8566)
        self.assertEqual(place.longitude, 2.3522)
        self.assertEqual(place.owner, user)

    def test_009_place_creation_invalid_negative_price(self):
        """Test place creation with negative price"""
        user = User("Owner", "Test", "owner@example.com")
        with self.assertRaises(ValueError):
            Place(
                title="Invalid Place",
                description="Test description",
                price=-50.0,  # Negative price
                latitude=48.8566,
                longitude=2.3522,
                owner=user
            )

    def test_010_place_creation_invalid_latitude_high(self):
        """Test place creation with latitude too high"""
        user = User("Owner", "Test", "owner@example.com")
        with self.assertRaises(ValueError):
            Place(
                title="Invalid Place",
                description="Test",
                price=100.0,
                latitude=95.0,  # Too high (max 90)
                longitude=2.3522,
                owner=user
            )

    def test_011_place_creation_invalid_latitude_low(self):
        """Test place creation with latitude too low"""
        user = User("Owner", "Test", "owner@example.com")
        with self.assertRaises(ValueError):
            Place(
                title="Invalid Place",
                description="Test",
                price=100.0,
                latitude=-95.0,  # Too low (min -90)
                longitude=2.3522,
                owner=user
            )

    def test_012_place_creation_invalid_longitude_high(self):
        """Test place creation with longitude too high"""
        user = User("Owner", "Test", "owner@example.com")
        with self.assertRaises(ValueError):
            Place(
                title="Invalid Place",
                description="Test",
                price=100.0,
                latitude=48.8566,
                longitude=190.0,  # Too high (max 180)
                owner=user
            )

    def test_013_place_creation_invalid_longitude_low(self):
        """Test place creation with longitude too low"""
        user = User("Owner", "Test", "owner@example.com")
        with self.assertRaises(ValueError):
            Place(
                title="Invalid Place",
                description="Test",
                price=100.0,
                latitude=48.8566,
                longitude=-190.0,  # Too low (min -180)
                owner=user
            )

    def test_014_place_add_amenity(self):
        """Test adding amenity to place"""
        user = User("Owner", "Test", "owner@example.com")
        place = Place("Test Place", "Nice place", 100, 48.85, 2.35, user)
        amenity = Amenity("Wi-Fi")
        
        # Initially no amenities
        self.assertEqual(len(place.amenities), 0)
        
        # Add amenity
        place.add_amenity(amenity)
        self.assertIn(amenity, place.amenities)
        self.assertEqual(len(place.amenities), 1)

    def test_015_place_add_multiple_amenities(self):
        """Test adding multiple amenities to place"""
        user = User("Owner", "Test", "owner@example.com")
        place = Place("Luxury Villa", "Very nice", 300, 43.71, 7.26, user)
        wifi = Amenity("Wi-Fi")
        pool = Amenity("Swimming Pool")
        parking = Amenity("Parking")
        
        place.add_amenity(wifi)
        place.add_amenity(pool)
        place.add_amenity(parking)
        
        self.assertEqual(len(place.amenities), 3)
        self.assertIn(wifi, place.amenities)
        self.assertIn(pool, place.amenities)
        self.assertIn(parking, place.amenities)

    def test_016_place_add_review(self):
        """Test adding review to place"""
        user = User("Owner", "Test", "owner@example.com")
        place = Place("Test Place", "Nice place", 100, 48.85, 2.35, user)
        review = Review("Great stay!", 5, "user123", "place123")
        
        # Initially no reviews
        self.assertEqual(len(place.reviews), 0)
        
        # Add review
        place.add_review(review)
        self.assertIn(review, place.reviews)
        self.assertEqual(len(place.reviews), 1)

    def test_017_review_creation_valid(self):
        """Test creating a valid review"""
        review = Review(
            text="Great place! Very clean and comfortable.",
            rating=5,
            user_id="user-12345",
            place_id="place-67890"
        )
        
        self.assertEqual(review.text, "Great place! Very clean and comfortable.")
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.user_id, "user-12345")
        self.assertEqual(review.place_id, "place-67890")

    def test_018_review_creation_rating_too_low(self):
        """Test review creation with rating too low"""
        with self.assertRaises(ValueError):
            Review("Bad place", 0, "user123", "place123")  # Rating too low (min 1)

    def test_019_review_creation_rating_too_high(self):
        """Test review creation with rating too high"""
        with self.assertRaises(ValueError):
            Review("Amazing place", 6, "user123", "place123")  # Rating too high (max 5)

    def test_020_review_creation_empty_text(self):
        """Test review creation with empty text"""
        with self.assertRaises(ValueError):
            Review("", 5, "user123", "place123")  # Empty text

    def test_021_review_creation_whitespace_text(self):
        """Test review creation with only whitespace text"""
        with self.assertRaises(ValueError):
            Review("   ", 5, "user123", "place123")  # Only whitespace

    def test_022_review_valid_ratings_boundary(self):
        """Test review creation with boundary ratings (1 and 5)"""
        # Minimum rating should work
        review1 = Review("Not great", 1, "user123", "place123")
        self.assertEqual(review1.rating, 1)
        
        # Maximum rating should work
        review5 = Review("Excellent!", 5, "user123", "place123")
        self.assertEqual(review5.rating, 5)

    def test_023_amenity_creation_valid(self):
        """Test creating a valid amenity"""
        amenity = Amenity("Swimming Pool")
        self.assertEqual(amenity.name, "Swimming Pool")

    def test_024_amenity_creation_empty_name(self):
        """Test amenity creation with empty name"""
        with self.assertRaises(ValueError):
            Amenity("")  # Empty name

    def test_025_amenity_creation_whitespace_name(self):
        """Test amenity creation with whitespace name"""
        with self.assertRaises(ValueError):
            Amenity("   ")  # Only whitespace

    def test_026_to_dict_method_user(self):
        """Test User to_dict method"""
        user = User("John", "Doe", "john@example.com")
        user_dict = user.to_dict()
        
        # Check basic structure
        self.assertIn('id', user_dict)
        self.assertIn('created_at', user_dict)
        self.assertIn('updated_at', user_dict)
        self.assertIn('__class__', user_dict)
        
        # Check values
        self.assertEqual(user_dict['first_name'], "John")
        self.assertEqual(user_dict['last_name'], "Doe")
        self.assertEqual(user_dict['email'], "john@example.com")
        self.assertEqual(user_dict['is_admin'], False)
        self.assertEqual(user_dict['__class__'], "User")

    def test_027_to_dict_method_place(self):
        """Test Place to_dict method"""
        user = User("Owner", "Test", "owner@example.com")
        place = Place("Test Place", "Description", 100, 48.85, 2.35, user)
        place_dict = place.to_dict()
        
        # Check basic structure
        self.assertIn('id', place_dict)
        self.assertIn('title', place_dict)
        self.assertIn('price', place_dict)
        self.assertIn('amenities', place_dict)
        self.assertIn('reviews', place_dict)
        self.assertIn('owner', place_dict)
        
        # Check values
        self.assertEqual(place_dict['title'], "Test Place")
        self.assertEqual(place_dict['price'], 100)
        self.assertEqual(place_dict['latitude'], 48.85)
        self.assertEqual(place_dict['longitude'], 2.35)
        self.assertEqual(place_dict['__class__'], "Place")
        self.assertIsInstance(place_dict['amenities'], list)
        self.assertIsInstance(place_dict['reviews'], list)

    def test_028_to_dict_method_review(self):
        """Test Review to_dict method"""
        review = Review("Great place", 5, "user123", "place456")
        review_dict = review.to_dict()
        
        # Check basic structure
        self.assertIn('id', review_dict)
        self.assertIn('text', review_dict)
        self.assertIn('rating', review_dict)
        self.assertIn('user_id', review_dict)
        self.assertIn('place_id', review_dict)
        
        # Check values
        self.assertEqual(review_dict['text'], "Great place")
        self.assertEqual(review_dict['rating'], 5)
        self.assertEqual(review_dict['user_id'], "user123")
        self.assertEqual(review_dict['place_id'], "place456")
        self.assertEqual(review_dict['__class__'], "Review")

    def test_029_to_dict_method_amenity(self):
        """Test Amenity to_dict method"""
        amenity = Amenity("Wi-Fi")
        amenity_dict = amenity.to_dict()
        
        # Check basic structure
        self.assertIn('id', amenity_dict)
        self.assertIn('name', amenity_dict)
        self.assertIn('created_at', amenity_dict)
        self.assertIn('updated_at', amenity_dict)
        
        # Check values
        self.assertEqual(amenity_dict['name'], "Wi-Fi")
        self.assertEqual(amenity_dict['__class__'], "Amenity")

    def test_030_base_model_inheritance(self):
        """Test that all models inherit BaseModel properties"""
        user = User("Test", "User", "test@example.com")
        place = Place("Test", "Desc", 100, 48.85, 2.35, user)
        review = Review("Test", 3, "user1", "place1")
        amenity = Amenity("Test")
        
        # All should have BaseModel attributes
        for obj in [user, place, review, amenity]:
            self.assertTrue(hasattr(obj, 'id'))
            self.assertTrue(hasattr(obj, 'created_at'))
            self.assertTrue(hasattr(obj, 'updated_at'))
            self.assertTrue(hasattr(obj, 'to_dict'))
            self.assertTrue(hasattr(obj, 'update'))
            self.assertTrue(hasattr(obj, 'save'))

    def test_031_update_method(self):
        """Test update method on models"""
        user = User("Original", "Name", "original@example.com")
        original_name = user.first_name
        
        # Update first name
        user.update({"first_name": "Updated"})
        self.assertEqual(user.first_name, "Updated")
        self.assertNotEqual(user.first_name, original_name)
        
        # Verify updated_at changed
        self.assertIsNotNone(user.updated_at)

    def test_032_place_title_length_validation(self):
        """Test place title length validation"""
        user = User("Owner", "Test", "owner@example.com")
        
        # Title exactly 100 characters should work
        valid_title = "A" * 100
        place = Place(valid_title, "Test", 100, 48.85, 2.35, user)
        self.assertEqual(place.title, valid_title)
        
        # Title 101 characters should fail
        with self.assertRaises(ValueError):
            invalid_title = "A" * 101
            Place(invalid_title, "Test", 100, 48.85, 2.35, user)

if __name__ == '__main__':
    # Run the tests with verbose output
    unittest.main(verbosity=2)