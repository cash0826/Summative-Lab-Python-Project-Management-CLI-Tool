class Person():
  def __init__(self, name, email):
      self._name = name
      self._email = email
  
  @property
  def name(self):
    return self._name
  
  @name.setter
  def name(self, value):
    self._name = value
  
  @property
  def email(self):
    return self._email
  
  @email.setter
  def email(self, value):
    self._email = value