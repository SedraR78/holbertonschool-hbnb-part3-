from app.database import db
from .repository import Repository  

class SQLAlchemyRepository(Repository):
    """SQLAlchemy implementation of Repository pattern"""
    
    def __init__(self, model_class):
        self.model_class = model_class
    
    def add(self, obj):
        """Add object to DB session and commit"""
        db.session.add(obj)
        db.session.commit()
        return obj
    
    def get(self, obj_id):
        return self.model_class.query.get(obj_id)
    
    def get_all(self):
        return self.model_class.query.all()
    
    def update(self, obj_id, data):
        """Update object attributes dynamically"""
        obj = self.get(obj_id)
        if obj:
            # Dynamic attribute setting from dict
            if isinstance(data, dict):
                for key, value in data.items():
                    if hasattr(obj, key):
                        setattr(obj, key, value)
            db.session.commit()
        return obj
    
    def delete(self, obj_id):
        obj = self.get(obj_id)
        if obj:
            db.session.delete(obj)
            db.session.commit()
            return True
        return False
    
    def get_by_attribute(self, attr_name, attr_value):
        """Dynamic query by any attribute using getattr"""
        return self.model_class.query.filter(
            getattr(self.model_class, attr_name) == attr_value
        ).first()