from .basemodel import BaseModel
from app.database import db


place_amenity = db.Table('place_amenity',
    db.Column('place_id', db.String(36), db.ForeignKey('places.id'), primary_key=True),
    db.Column('amenity_id', db.String(36), db.ForeignKey('amenities.id'), primary_key=True)
)

class Place(BaseModel):
    __tablename__ = 'places'
    
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    
    """ FOREIGN KEYS"""
    owner_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    
    """ RELATIONS"""
    reviews = db.relationship('Review', backref='place', lazy=True, cascade='all, delete-orphan')
    amenities = db.relationship('Amenity', secondary=place_amenity, lazy='subquery',
                               backref=db.backref('places', lazy=True))
    
    def __init__(self, **kwargs):
        super().__init__()
        if 'title' in kwargs:
            self.title = kwargs['title']
        if 'description' in kwargs:
            self.description = kwargs['description']
        if 'price' in kwargs:
            self.price = kwargs['price']
        if 'latitude' in kwargs:
            self.latitude = kwargs['latitude']
        if 'longitude' in kwargs:
            self.longitude = kwargs['longitude']
        if 'owner_id' in kwargs:
            self.owner_id = kwargs['owner_id']

    

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'owner_id': self.owner_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }