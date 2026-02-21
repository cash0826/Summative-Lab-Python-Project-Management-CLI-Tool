import os
import json

def load_settings(file_path="settings.json"):
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

