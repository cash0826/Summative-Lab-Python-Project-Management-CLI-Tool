# Creating a Command Line Interface using Object Oriented Programming

## Setup Instructions

### Install Python, Pip and Pipenv

Ensure Python, Pip and Pipenv are installed. Pipenv will install any required dependencies.

```bash
python --version
pip --version
pipenv install
pipenv shell
```

## CLI Commands

There are 3 main subcommands: user, project and task

For user, there are the following options: `add-user`, `list-user`.
 - to add a user, you must enter -n followed by the name of the user, and -e to enter email.
 - to see saved users, enter 'list-user'. No arguments are required.


For project, these are the options: `add-project`, `list-projects`.
 - to add a project, you must enter -t followed by the title of the project, -d for description, -due for due date and -owner for the owner's email.
 - to list projects, there is 1 requirement: you must enter -owner and the owner's email to search projects by the owner's email.


For task, these are the options: `add-task`, `complete-tasks`
- to add a task, you must enter -t, title of the task, -p, project title of the associate project, and -a, user that the project is assigned to. 
 - You can also enter -s, for status, but it is not a required field. It will default to Pending.
- to complete a task, you must enter -t, for the title of the task, and -p the project title that the task is associated with.


## Features
- Data is persisted using helper methods in util storage and lib controllers
- Data is saved to JSON files
- Classes are defined for instances using private attributes
- argparse is utilized to create commands and subcommands


## Known Issues & Concepts Left to Expand on
- Improve commands to be more user friendly
- General structure could improve: Tasks should fall under Projects, and Projects should fall under Users
- due_date validation for an actual date (Done!)
- Import PyPi packages to improve readability (Attempted. With Typer, subcommands are simplified but would require completely changing the code)
- Unit testing