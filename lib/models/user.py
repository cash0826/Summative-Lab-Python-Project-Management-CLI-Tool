from lib.models.person import Person
from lib.models.project import Project

class User(Person):
  def __init__(self, name, email):
    super().__init__(name, email)
    
  def to_dict(self):
    return {"name": self.name, "email": self.email}
    
  @classmethod
  def from_dict(cls, data):
    return cls(name=data.get("name"), email=data.get("email"))
  
  def __str__(self):
    return str(self.to_dict())