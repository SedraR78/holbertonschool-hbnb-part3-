
from app.database import db
from .basemodel import BaseModel
import re

class User(BaseModel):
    __tablename__ = 'users'
    
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    
    
    places = db.relationship('Place', backref='owner', lazy=True, cascade='all, delete-orphan')
    reviews = db.relationship('Review', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def __init__(self, **kwargs):
        super().__init__()
        if 'first_name' in kwargs:
            self.first_name = kwargs['first_name']
        if 'last_name' in kwargs:
            self.last_name = kwargs['last_name']
        if 'email' in kwargs:
            self.email = kwargs['email']
        if 'password' in kwargs:
            self.hash_password(kwargs['password'])
        if 'is_admin' in kwargs:
            self.is_admin = kwargs.get('is_admin', False)

    def hash_password(self, password):
        from app import bcrypt  
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        from app import bcrypt  
        return bcrypt.check_password_hash(self.password, password)
    
    def to_dict(self, exclude=None):
        if exclude is None:
            exclude = []
        if 'password' not in exclude:
            exclude.append('password')
            
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'is_admin': self.is_admin,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }