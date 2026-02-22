import json

class Task():
  def __init__(self, title, status="Pending", assigned_to=None):
    self._title = title
    self._status = status
    self._assigned_to = assigned_to
    self._associated_project = None  # This will be set when the task is added to a project
    
  @property
  def title(self):
    return self._title
  
  @property
  def status(self):
    return self._status
  
  @property
  def assigned_to(self):
    return self._assigned_to
  
  @property
  def associated_project(self):
    return self._associated_project
  
  @title.setter
  def title(self, value):
    self._title = value
    
  @status.setter
  def status(self, value):
    self._status = value
    
  @assigned_to.setter
  def assigned_to(self, value):
    self._assigned_to = value
    
  @associated_project.setter
  def associated_project(self, value):
    self._associated_project = value
    
  @classmethod
  def from_dict(cls, data):
    return cls(title=data["title"], status=data["status"], assigned_to=data["assigned_to"])
  
  def to_dict(self):
    return {
      "title": self.title,
      "status": self.status,
      "assigned_to": self.assigned_to
    }