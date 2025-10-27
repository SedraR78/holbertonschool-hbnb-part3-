from .base_model import BaseModel

class User(BaseModel):
    def __init__(self,first_name,last_name,email,is_admin=False):
        super().__init__() 
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self._constraints()
        
    def _constraints(self):
        
        """Ensure User meets all business constraints"""
        if len(self.first_name) > 50:
            raise ValueError("First name too long")
        if len(self.last_name) > 50:
            raise ValueError("Last name too long")
        """ checking if there is @  email"""
        if "@" not in self.email:
            raise ValueError("Invalid email format")
        
        """check if after the @ we have a point (the string count like 1 elements so -1)"""
        domaine = self.email.split("@")[-1]  #
        if "." not in domaine:
            raise ValueError("Email must contain domain with .")
