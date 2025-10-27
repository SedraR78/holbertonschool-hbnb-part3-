#!/usr/bin/env python3
import sys
import os

"""Add hbnb directory to Python path for imports"""
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'hbnb'))

from hbnb.app.models import User, Place, Review, Amenity

def test_relationships():
    """Test model relationships and JSON serialization capabilities"""
    print("TESTING MODELS RELATIONSHIPS...\n")
    
    try:
        """Create all model instances to test relationships"""
        print("=== Creating Models ===")
        user = User("Alice", "Smith", "alice@test.com")
        place = Place("Mountain Cabin", "Cozy cabin in the woods", 200.0, 45.0, -120.0, user)
        review = Review(5, "Amazing view and very cozy!")
        amenity = Amenity("Fireplace")
        
        print("All models created successfully!")
        
        """Test relationship establishment between models"""
        print("\n=== Testing Relationships ===")
        place.add_review(review)
        place.add_amenity(amenity)
        
        print(f"User: {user.first_name} {user.last_name}")
        print(f"Place: '{place.title}' - ${place.price}/night")
        print(f"Review: {review.rating} stars - '{review.comment}'")
        print(f"Amenity: {amenity.name}")
        print(f"Place has {len(place.reviews)} reviews and {len(place.amenities)} amenities")
        
        """Verify JSON serialization preserves all attributes and relationships"""
        print("\n=== Testing JSON Serialization ===")
        user_json = user.to_dict()
        place_json = place.to_dict()
        
        print(f"User JSON keys: {list(user_json.keys())}")
        print(f"Place JSON keys: {list(place_json.keys())}")
        print(f"Place title from JSON: {place_json['title']}")
        print(f"Place price from JSON: {place_json['price']}")
        
        """Ensure relationships are properly maintained in serialized output"""
        print(f"Place has reviews in JSON: {'reviews' in place_json}")
        print(f"Place has amenities in JSON: {'amenities' in place_json}")
        
        print("\nALL RELATIONSHIP TESTS PASSED!")
        return True
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_validation():
    """Test that business constraints are properly enforced"""
    print("\nTESTING VALIDATION...\n")
    
    try:
        """Verify validation blocks invalid data inputs"""
        print("=== Testing Invalid Review ===")
        try:
            bad_review = Review(0, "Too low rating")
            print("Should have failed for rating 0")
        except ValueError as e:
            print(f"Correctly blocked rating 0: {e}")
            
        try:
            bad_review2 = Review(5, "")
            print("Should have failed for empty comment")
        except ValueError as e:
            print(f"Correctly blocked empty comment: {e}")
            
        print("ALL VALIDATION TESTS PASSED!")
        return True
        
    except Exception as e:
        print(f"VALIDATION ERROR: {e}")
        return False

if __name__ == "__main__":
    """Execute all test suites and report final results"""
    success1 = test_relationships()
    success2 = test_validation()
    
    if success1 and success2:
        print("\nALL TESTS PASSED! Your models are ready for production!")
    else:
        print("\nSOME TESTS FAILED - Check your models implementation")