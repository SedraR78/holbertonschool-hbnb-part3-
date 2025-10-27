# HBnB API Testing Implementation

## 📋 Task Overview

This project implements comprehensive testing and validation for the HBnB API endpoints. The implementation includes model validation, automated unit tests, cURL testing, and Swagger documentation.

## ✅ Requirements Completed

### 1. Basic Validation Implementation

**User Model:**
- ✅ `first_name`, `last_name`, `email` cannot be empty
- ✅ Email must be in valid format (contains @ and domain)

**Place Model:**
- ✅ `title` cannot be empty  
- ✅ `price` must be positive number
- ✅ `latitude` between -90 and 90
- ✅ `longitude` between -180 and 180

**Review Model:**
- ✅ `text` cannot be empty
- ✅ `user_id` and `place_id` must reference valid entities
- ✅ `rating` must be between 1-5

**Amenity Model:**
- ✅ `name` cannot be empty or whitespace

### 2. Automated Unit Tests

**Two comprehensive test suites created:**

#### Model Tests (`test_models.py`)
- **32 tests** covering all validation rules
- Tests both valid and invalid data scenarios
- Boundary testing for coordinates, ratings, string lengths

#### Endpoint Tests (`test_endpoints.py`) 
- **30 tests** covering all API endpoints
- CRUD operations for all entities
- Error handling for invalid requests
- Relationship endpoints (reviews by place)

### 3. Manual Testing with cURL

**Example test commands:**

```bash
# Test valid user creation
curl -X POST "http://localhost:5000/api/v1/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com"
  }'

# Test invalid email
curl -X POST "http://localhost:5000/api/v1/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe", 
    "email": "invalid-email"
  }'

# Test boundary coordinates
curl -X POST "http://localhost:5000/api/v1/places/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test Place",
    "price": 100,
    "latitude": 95.0,
    "longitude": 2.35,
    "owner_id": "test-owner"
  }'