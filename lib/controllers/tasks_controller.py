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
      new_task = Task(title=args.title, status=args.status, assigned_to=args.assigned_to, associated_project=args.project_title)
      self.data.append(new_task.to_dict())
      print(f"Added task: {new_task.title} was successfully added to project {args.project_title}.")
      return new_task
    
    def complete_task(self, args):
      for task in self.data:
        if task["title"] == args.title and task["associated_project"] == args.project_title:
          task["status"] = "Completed"
          print(f"Task '{args.title}' in project '{args.project_title}' marked as completed.")
          return task
      print(f"Error: No task found with title '{args.title}' in project '{args.project_title}'.")
      return None