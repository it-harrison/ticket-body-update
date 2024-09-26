import os

def get_text(file_name="text.md"):
  
  file_dir = os.path.dirname(os.path.realpath(__file__))
  file_path = os.path.join(file_dir, file_name)
  with open(file_path, 'r') as file:
    content = file.read()
    return content