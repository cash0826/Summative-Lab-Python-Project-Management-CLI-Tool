from lib.models.user import User
from lib.utils import storage

class UsersControllers:
  def __init__(self, filepath):
    self.filepath = filepath
    self.data = []
    
  def __enter__(self):
    self.data = [User.from_dict(user) for user in storage.load_data(self.filepath)]
    return self
  
  def __exit__(self, exc_type, exc_value, traceback):
      storage.save_data(self.filepath, [user.to_dict() for user in self.data])
  
  def add_user(self, args):
    # check if user already has a matching email
    if any(user.email == args.email for user in self.data):
      print(f"Error: User with email {args.email} already exists.")
      return None
    
    new_user = User(name=args.name, email=args.email)
    self.data.append(new_user)
    print(f"Added user: {new_user.name} was successfully added: {new_user}")
    return new_user
  
  def list_users(self):
    if not self.data:
      print("No users found.")
      return []
    for user in self.data:
      print(f"[User] Name: {user.name}, Email: {user.email}")
    return self.data