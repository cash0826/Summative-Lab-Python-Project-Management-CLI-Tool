from lib.models.task import Task
from lib.utils import storage

class TasksController:
    def __init__(self, filepath):
        self.filepath = filepath
        self.data = []
    
    def __enter__(self):
        self.data = storage.load_data(self.filepath)
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        storage.save_data(self.filepath, self.data)
        
    def add_task(self, args):
      # Check if task has a matching project title
      if not any(project["title"] == args.project_title for project in storage.load_data("./data/projects.json")):
        print(f"Error: No project found with title {args.project_title}.")
        return None
      
      # Check if task has a matching user
      if not any(user["name"] == args.assigned_to for user in storage.load_data("./data/users.json")):
        print(f"Error: No user found with email {args.assigned_to}.")
        return None
      
      # Check if task with same title already exists in the same project (duplicates)
      if any(task["title"] == args.title and task["associated_project"] == args.project_title for task in self.data):
        print(f"Error: A task with title '{args.title}' already exists in project '{args.project_title}'.")
        return None
      
      # Append new task to data list and save to file
      new_task = Task(title=args.title, associated_project=args.project_title, assigned_to=args.assigned_to, status=args.status)
      self.data.append(new_task.to_dict())
      print(f"Added task: {new_task.title} was successfully added to project {args.project_title}.")
      return new_task
    
    def complete_task(self, args):
      # check if task exists with matching title
      task = any(task["title"] == args.task and task["associated_project"] == args.project_title for task in self.data)
      if not task:
        print(f"Error: No task found with title '{args.task}' in project '{args.project_title}'.")
        return None
      
      # check if project exists with matching title
      if not any(project["title"] == args.project_title for project in storage.load_data("./data/projects.json")):
        print(f"Error: No project found with title {args.project_title}.")
        return None
      
      # update the status of the matching task
      for task in self.data:
        if task["title"] == args.task and task["associated_project"] == args.project_title:
          task["status"] = "Completed"
          print(f"Task '{args.task}' in project '{args.project_title}' marked as completed.✅")
          return task