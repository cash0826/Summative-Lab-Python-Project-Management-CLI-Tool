import json

class Person():
  def __init__(self, name, email):
      self.name = name
      self.email = email

class User(Person):
  def __init__(self, name, email):
    super().__init__(name, email)
    
  def to_dict(self):
    return {"name": self.name, "email": self.email}
    
  @classmethod
  def from_dict(cls, data):
    return cls(name=data.get("name"), email=data.get("email"))
  
  def user_projects(self):
    return [project for project in Project.all_projects if project.owner_email == self.email]
  
  def __str__(self):
    return str(self.to_dict())
  
class Project():
  def __init__(self, title, description, due_date):
    self.title = title
    self.description = description
    self.due_date = due_date
    
  @classmethod
  def from_dict(cls, data):
    return cls(title=data["title"], description=data["description"], due_date=data["due_date"])
  
  @classmethod
  def from_json(cls, json_str):
    data = json.loads(json_str)
    return cls.from_dict(data)
  
  def tasks(self):
    return [task for task in Task.all_tasks if task.project_title == self.title]
  
  def __str__(self):
    return str(self.to_dict())
  
class Task():
  def __init__(self, title, status, assigned_to):
    self.title = title
    self.status = status
    self.assigned_to = assigned_to
    
  @classmethod
  def from_dict(cls, data):
    return cls(title=data["title"], status=data["status"], assigned_to=data["assigned_to"])
  
  @classmethod
  def from_json(cls, json_str):
    data = json.loads(json_str)
    return cls.from_dict(data)
  
  def __str__(self):
    return str(self.to_dict())