from .base_model import BaseModel

class Review(BaseModel):
    def __init__(self, text, rating, user_id, place_id):
        super().__init__()
        self.text = text
        self.rating = rating  
        self.user_id = user_id
        self.place_id = place_id
        self._constraints()
        
    def _constraints(self):
        """Ensure Review meets all business constraints"""
        if not (1 <= self.rating <= 5):
            raise ValueError("Rating must be between 1 and 5")
        if not self.text or len(self.text.strip()) == 0:
            raise ValueError("Comment cannot be empty")