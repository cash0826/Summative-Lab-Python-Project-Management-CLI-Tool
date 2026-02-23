from lib.models.project import Project
from lib.utils import storage
from datetime import datetime

class ProjectsControllers():
  def __init__(self, filepath):
    self.filepath = filepath
    self.data = []
        
  def __enter__(self):
    # Load projects from file
    self.data = [Project.from_dict(project) for project in storage.load_data(self.filepath)]
    return self
  
  def __exit__(self, exc_type, exc_value, traceback):
    # Save projects to file
    storage.save_data(self.filepath, [project.to_dict() for project in self.data])
    
  def add_project(self, args):
    # check if email exists in users.json
    users = storage.load_data("./data/users.json")
    if not any(user["email"] == args.owner_email for user in users):
      print(f"Error: No user found with email {args.owner_email}.")
      return None
    
    # check if project with same title already exists
    if any(project.title == args.title for project in self.data):
      print(f"Error: A project with the title '{args.title}' already exists.")
      return None
    
    # check if due_date is a valid date
    try:
      due_date = datetime.strptime(args.due_date, '%m/%d/%Y').date()
    except ValueError:
      print("Due Date needs to be in this date format: MM/DD/YYYY")
      return None
    
    # Append new project to data list
    new_project = Project(title=args.title, description=args.description, due_date=due_date, owner_email=args.owner_email)
    self.data.append(new_project)
    print(f"Added project: {new_project.title} was successfully added: {new_project}")
    return new_project
  
  def list_projects_by_owner(self, args):
    user_projects = [project for project in self.data if project.owner_email == args.owner_email]
    # check email exists in users.json
    users = storage.load_data("./data/users.json")
    if not any(user["email"] == args.owner_email for user in users):
      print(f"Error: No user found with email {args.owner_email}.")
      return []
    
    # check if user has any projects
    if not user_projects:
      print(f"No projects found for user with email {args.owner_email}.")
      return []
    for project in user_projects:
      print(f"[Project] Title: {project.title}, Description: {project.description}, Due Date: {project.due_date}")
    return user_projects