import json
from lib.models.task import Task

class Project():
  def __init__(self, title, description, due_date, owner_email=None):
    self.title = title
    self.description = description
    self.due_date = due_date
    self.owner_email = owner_email
    
  @classmethod
  def from_dict(cls, data):
    return cls(title=data["title"], description=data["description"], due_date=data["due_date"], owner_email=data.get("owner_email"))
  
  @classmethod
  def from_json(cls, json_str):
    data = json.loads(json_str)
    return cls.from_dict(data)
  
  def to_dict(self):
    return {
      "title": self.title,
      "description": self.description,
      "due_date": self.due_date,
      "owner_email": self.owner_email
    }
  
  def __str__(self):
    return str(self.to_dict())