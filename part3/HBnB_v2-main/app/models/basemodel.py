import uuid
from datetime import datetime
from app import db

class BaseModel(db.Model):
    __abstract__ = True
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.now)  # ✅ Reste avec datetime.now
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)  # ✅ Reste avec datetime.now
    
    def save(self):
        """Update the updated_at timestamp whenever the object is modified"""
        self.updated_at = datetime.now()
        db.session.commit()

    def update(self, data):
        """Update the attributes of the object based on the provided dictionary"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()
        
    def is_max_length(self, name, value, max_length):
        if len(value) > max_length:
            raise ValueError(f"{name} must be {max_length} characters max.") 
        
    def is_between(self, name, value, min_val, max_val):
        if not min_val < value < max_val:
            raise ValueError(f"{name} must be between {min_val} and {max_val}.")