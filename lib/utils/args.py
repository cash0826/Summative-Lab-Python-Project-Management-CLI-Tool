import argparse
from lib.controllers.projects_controller import ProjectsControllers
from lib.controllers.users_controllers import UsersControllers

def add_user_command(args):
    with UsersControllers("./data/users.json") as controller:
        return controller.add_user(args)

def list_users_command():
    with UsersControllers("./data/users.json") as controller:
        return controller.list_users()

def add_project(args):
    with ProjectsControllers("./data/projects.json") as controller:
        return controller.add_project(args)
      
def list_projects_for_user(args):
    with ProjectsControllers("./data/projects.json") as controller:
        return controller.list_projects_for_user(args)

def parse_args():
  parser = argparse.ArgumentParser(description="Project Management CLI Tool")
  
  # Single subparser for all top-level commands (users, projects, tasks)
  subparsers = parser.add_subparsers(dest="command", help="Available commands")
  
  # Subparsers for User Management
  user_parser = subparsers.add_parser("user", help="User management commands")
  user_subparsers = user_parser.add_subparsers(dest="user_command")
  
  ## Add user command
  add_user_parser = user_subparsers.add_parser("add-user", help="Add a new user")
  add_user_parser.add_argument("--name", required=True, help="Name of the user")
  add_user_parser.add_argument("--email", required=True, help="Email of the user")
  add_user_parser.set_defaults(func=add_user_command)
  
  ## List users command
  list_users_parser = user_subparsers.add_parser("list-users", help="List all users")
  list_users_parser.set_defaults(func=list_users_command)
  
  # Subparsers for Project Management would go here
  project_parser = subparsers.add_parser("project", help="Project management commands")
  project_subparsers = project_parser.add_subparsers(dest="project_command")
  
  ## Add project command
  add_project_parser = project_subparsers.add_parser("add-project", help="Add a new project")
  add_project_parser.add_argument("--title", required=True, help="Title of the project")
  add_project_parser.add_argument("--description", required=True, help="Description of the project")
  add_project_parser.add_argument("--due_date", required=True, help="Due date of the project")
  add_project_parser.add_argument("--owner_email", required=True, help="Email of the project owner")
  add_project_parser.set_defaults(func=add_project) # add project to be defined
  
  ## List projects by user command
  list_projects_parser = project_subparsers.add_parser("list-projects", help="List all projects for a user")
  list_projects_parser.add_argument("-u", "--user_email", required=True, help="Email of the user to list projects for")
  list_projects_parser.set_defaults(func=list_projects_for_user) # list projects for user to be defined
  
  # # Subparsers for Task Management would go here
  # task_parser = subparsers.add_parser("task", help="Task management commands")
  # task_subparsers = task_parser.add_subparsers(dest="task_command")
  
  # ## Add task command
  # add_task_parser = task_parser.add_parser("add_task", help="Add a new task")
  # add_task_parser.add_argument("--title", required=True, help="Title of the task")
  # add_task_parser.add_argument("--status", required=True, help="Status of the task")
  # add_task_parser.add_argument("--assigned_to", required=True, help="User assigned to the task")
  # add_task_parser.set_defaults(func=add_task) # add task to be defined
  
  # ## Complete task command
  # complete_task_parser = task_parser.add_parser("complete_task", help="Mark a task as completed")
  # complete_task_parser.add_argument("--task", required=True, help="Name of the task to mark as completed")
  # complete_task_parser.set_defaults(func=complete_task) # complete task to be defined
  
  return parser.parse_args()