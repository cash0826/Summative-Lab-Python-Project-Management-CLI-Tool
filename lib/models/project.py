import json
from lib.models.task import Task

class Project():
  def __init__(self, title, description, due_date, owner_email=None):
    self._title = title
    self._description = description
    self._due_date = due_date
    self._owner_email = owner_email
    
  @property
  def title(self):
    return self._title
  
  @property
  def description(self):
    return self._description
  
  @property
  def due_date(self):
    return self._due_date
  
  @property
  def owner_email(self):
    return self._owner_email
  
  @title.setter
  def title(self, value):
    self._title = value
    
  @description.setter
  def description(self, value):
    self._description = value
  
  @due_date.setter
  def due_date(self, value):
    self._due_date = value
    
  @owner_email.setter
  def owner_email(self, value):
    self._owner_email = value
    
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