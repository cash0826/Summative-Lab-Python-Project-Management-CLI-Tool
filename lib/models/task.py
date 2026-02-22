import json

class Task():
  def __init__(self, title, associated_project, assigned_to, status=None):
    self._title = title
    self._associated_project = associated_project
    self._assigned_to = assigned_to
    self._status = status if status is not None else "Pending"

  @property
  def title(self):
    return self._title
  
  @property
  def associated_project(self):
    return self._associated_project
  
  @property
  def assigned_to(self):
    return self._assigned_to
  
  @property
  def status(self):
    return self._status
  
  @title.setter
  def title(self, value):
    self._title = value
  
  @associated_project.setter
  def associated_project(self, value):
    self._associated_project = value
    
  @assigned_to.setter
  def assigned_to(self, value):
    self._assigned_to = value
     
  @status.setter
  def status(self, value):
    self._status = value
    
  @classmethod
  def from_dict(cls, data):
    return cls(title=data["title"], status=data["status"], assigned_to=data["assigned_to"])
  
  def to_dict(self):
    return {
      "title": self.title,
      "associated_project": self.associated_project,
      "assigned_to": self.assigned_to,
      "status": self.status
    }