from app.database import db
from .basemodel import BaseModel

class Amenity(BaseModel):
    __tablename__ = 'amenities'
    

    name = db.Column(db.String(50), nullable=False, unique=True)
    
    def __init__(self, **kwargs):

        super().__init__()
        if 'name' in kwargs:
            self.name = kwargs['name']  

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,  
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }