from .basemodel import BaseModel
from app.database import db

class Amenity(BaseModel):
    __tablename__ = 'amenities'
    
    name = db.Column(db.String(50), nullable=False, unique=True)
    
    def __init__(self, **kwargs):
        super().__init__()
        if 'name' in kwargs:
            self.name = kwargs['name']

    # ... properties et to_dict