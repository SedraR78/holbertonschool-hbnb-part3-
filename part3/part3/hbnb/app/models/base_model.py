import uuid
from datetime import datetime

class BaseModel:
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def save(self):
        """Update the updated_at timestamp whenever the object is modified"""
        self.updated_at = datetime.now()

    def update(self, data):
        """Update the attributes of the object based on the provided dictionary"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()  

    @classmethod
    def create(cls, **kwargs):
        instance = cls(**kwargs)
        return instance

    def to_dict(self):
        """Convert instance to dictionary for JSON serialization"""
        model_dict = self.__dict__.copy()
        model_dict['__class__'] = self.__class__.__name__
        model_dict['created_at'] = self.created_at.isoformat()
        model_dict['updated_at'] = self.updated_at.isoformat()

        if hasattr(self, 'amenities'):
            if all(hasattr(amenity, 'to_dict') for amenity in self.amenities):
                model_dict['amenities'] = [amenity.to_dict() for amenity in self.amenities]
            else:
                model_dict['amenities'] = self.amenities  
                
        if hasattr(self, 'reviews'):
            model_dict['reviews'] = [review.to_dict() for review in self.reviews]
    
        if hasattr(self, 'owner') and hasattr(self.owner, 'to_dict'):
            model_dict['owner'] = self.owner.to_dict()
    
        
        return model_dict
        

    def delete(self): 
        pass