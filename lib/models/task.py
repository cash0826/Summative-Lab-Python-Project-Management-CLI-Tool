import json

class Task():
  def __init__(self, title, status="Pending", assigned_to=None):
    self.title = title
    self.status = status
    self.assigned_to = assigned_to
    
  @classmethod
  def from_dict(cls, data):
    return cls(title=data["title"], status=data["status"], assigned_to=data["assigned_to"])
  
  def to_dict(self):
    return {
      "title": self.title,
      "status": self.status,
      "assigned_to": self.assigned_to
    }