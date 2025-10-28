# models/user.py
"""
User model for the HBnB application.
Represents a user who can own places and write reviews.
"""
from app.models.base_model import BaseModel
from app import bcrypt
import re


class User(BaseModel):
    """User class representing a user in the system."""

    def __init__(self, first_name, last_name, email, password, is_admin=False):
        super().__init__()
        self.first_name = self._validate_name(first_name, "First name")
        self.last_name = self._validate_name(last_name, "Last name")
        self.email = self._validate_email(email)
        self.password = self._hash_password(password)
        self.is_admin = is_admin
        self.places = []
        self.reviews = []

    @staticmethod
    def _validate_name(name, field_name):
        if not name or not isinstance(name, str):
            raise ValueError(f"{field_name} is required and must be a string")
        if len(name) > 50:
            raise ValueError(f"{field_name} must not exceed 50 characters")
        return name.strip()

    @staticmethod
    def _validate_email(email):
        if not email or not isinstance(email, str):
            raise ValueError("Email is required and must be a string")
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, email):
            raise ValueError("Invalid email format")
        return email.lower().strip()

    @staticmethod
    def _validate_password(password):
        if not password or not isinstance(password, str):
            raise ValueError("Password is required and must be a string")
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long")
        return password

    def _hash_password(self, password):
        validated_password = self._validate_password(password)
        return bcrypt.generate_password_hash(validated_password).decode('utf-8')

    def verify_password(self, password):
        """Verify a password against the stored hash."""
        return bcrypt.check_password_hash(self.password, password)

    def add_place(self, place):
        if place not in self.places:
            self.places.append(place)

    def add_review(self, review):
        if review not in self.reviews:
            self.reviews.append(review)

    def to_dict(self):
        """Convert User instance to dictionary without password."""
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'is_admin': self.is_admin,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    def __repr__(self):
        return f"<User {self.id} - {self.first_name} {self.last_name}>"
