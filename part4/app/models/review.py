from .basemodel import BaseModel
from app import db

class Review(BaseModel):
    __tablename__ = 'reviews'
    
    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    

    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)
    

    __table_args__ = (db.UniqueConstraint('user_id', 'place_id', name='unique_user_place'),)
    
    def __init__(self, **kwargs):
        super().__init__()
        if 'text' in kwargs:
            self.text = kwargs['text']
        if 'rating' in kwargs:
            self.rating = kwargs['rating']
        if 'user_id' in kwargs:
            self.user_id = kwargs['user_id']
        if 'place_id' in kwargs:
            self.place_id = kwargs['place_id']



    def to_dict(self):
        return {
            'id': self.id,
            'text': self.text,
            'rating': self.rating,
            'user_id': self.user_id,
            'place_id': self.place_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }