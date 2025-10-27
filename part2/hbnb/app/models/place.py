from .base_model import BaseModel

class Place(BaseModel):
    def __init__(self,title,description,price,latitude,longitude,owner):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner   
        self.amenities = []  
        self.reviews = []   

        self._constraints()  
    
    def _constraints(self):
        """Ensure Place meets all business constraints"""
        if len(self.title) > 100:
            raise ValueError("Title too long")
        if self.price < 0:
            raise ValueError("Price must be positive")
        if not (-90 <= self.latitude <= 90):
            raise ValueError("Latitude must be between -90 and 90")
        if not (-180 <= self.longitude <= 180):
            raise ValueError("Longitude must be between -180 and 180")

        
        
    def add_amenity(self, amenity):
            """Add an amentiy to the place."""
            self.amenities.append(amenity)


    def add_review(self, review):
            """Add a review to the place."""
            self.reviews.append(review)