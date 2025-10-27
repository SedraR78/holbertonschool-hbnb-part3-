# HBnB API - Vacation Rental Platform

A RESTful API for a vacation rental platform built with Flask and Flask-RESTx. Implements a complete backend with user management, property listings, reviews, and amenities.

## 🏗️ Project Architecture

Clean architecture with separation of concerns:
hbnb/
├── app/
│ ├── api/v1/ # Presentation Layer
│ ├── models/ # Business Logic Layer
│ ├── services/ # Application Layer
│ └── persistence/ # Data Layer



## 📋 Features

### Core Entities
- **Users**: Registration and profile management
- **Places**: Property listings with location and pricing
- **Reviews**: User ratings and comments
- **Amenities**: Property features management

### API Endpoints

#### Users
- `POST /api/v1/users/` - Create new user
- `GET /api/v1/users/` - List all users
- `GET /api/v1/users/<user_id>` - Get user details
- `PUT /api/v1/users/<user_id>` - Update user
- `DELETE /api/v1/users/<user_id>` - Delete user

#### Places
- `POST /api/v1/places/` - Create property listing
- `GET /api/v1/places/` - List all properties
- `GET /api/v1/places/<place_id>` - Get property details
- `PUT /api/v1/places/<place_id>` - Update property
- `GET /api/v1/places/<place_id>/reviews` - Get property reviews

#### Reviews
- `POST /api/v1/reviews/` - Create new review
- `GET /api/v1/reviews/` - List all reviews
- `GET /api/v1/reviews/<review_id>` - Get review details
- `PUT /api/v1/reviews/<review_id>` - Update review
- `DELETE /api/v1/reviews/<review_id>` - Delete review

#### Amenities
- `POST /api/v1/amenities/` - Create amenity
- `GET /api/v1/amenities/` - List amenities
- `GET /api/v1/amenities/<amenity_id>` - Get amenity details
- `PUT /api/v1/amenities/<amenity_id>` - Update amenity
- `DELETE /api/v1/amenities/<amenity_id>` - Delete amenity

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- pip

### Installation

1. **Create virtual environment**
    
   python -m venv venv
   source venv/bin/activate


2)  Install dependencies

pip install -r requirements.txt

3)  Run the application

python run.py

API available at http://localhost:5001

📚 API Documentation
Interactive Swagger documentation:

http://localhost:5001/api/v1/

    🏛️ Design Patterns:

Facade Pattern:
HBnBFacade provides unified interface to business logic and data access.

Repository Pattern:
Abstracts data storage with in-memory implementation.

Layered Architecture:
Presentation: Flask-RESTx endpoints

Business Logic: Domain models with validation

Persistence: Repository interface

    🔧 Key Features
Data Validation : Each entity validates business rules:

. User email format and name length

. Place coordinates and pricing

. Review ratings and content

UUID Identification: UUIDv4 for all entities provides:

. Global uniqueness

. Enhanced security

. No ID conflicts

Relationship Management  : 
. Places reference owners (Users)

. Reviews link Users to Places

. Places have multiple Amenities

    Testing Examples : 

1) Create User

curl -X POST "http://localhost:5000/api/v1/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com"
  }'

2) Create Place

curl -X POST "http://localhost:5000/api/v1/places/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Beach Villa",
    "price": 150.0,
    "latitude": 34.0522,
    "longitude": -118.2437,
    "owner_id": "USER_UUID"
  }'

📁 Project Structure

hbnb/
├── app/
│ ├── api/
│ │ └── v1/
│ │ ├── users.py
│ │ ├── places.py
│ │ ├── reviews.py
│ │ └── amenities.py
│ ├── models/
│ │ ├── base_model.py
│ │ ├── user.py
│ │ ├── place.py
│ │ ├── review.py
│ │ └── amenity.py
│ ├── services/
│ │ ├── facade.py
│ │ └── repository.py
│ └── persistence/
│ └── repository.py
├── tests/
│ ├── test_models.py
│ └── test_endpoints.py
├── run.py
├── config.py
└── requirements.txt






