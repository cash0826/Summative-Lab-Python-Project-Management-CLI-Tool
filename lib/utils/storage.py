import os
import json

def load_settings(file_path="./settings.json"):
  if os.path.exists(file_path):
    try:
      with open(file_path, "r") as file:
        return json.load(file)
    except (json.JSONDecodeError, IOError):
      pass
  return {}
  
def get_setting(key, default=None):
  settings = load_settings()
  return settings.get(key, default)

def load_data(file_path):
  if not os.path.exists(file_path):
    return []
  try:
    with open(file_path, "r") as file:
      return json.load(file)
  except (json.JSONDecodeError, IOError) as e:
    print(f"Error loading data from {file_path}: {e}")
    return []

def save_data(file_path, data):
  directory = os.path.dirname(file_path)
  if directory and not os.path.exists(directory):
    os.makedirs(directory)
  try:
    with open(file_path, "w") as file:
      json.dump(data, file, indent=2)
  except IOError as e:
    print(f"Error saving data to {file_path}: {e}")