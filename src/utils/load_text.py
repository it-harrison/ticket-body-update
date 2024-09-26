import os

def get_text(calling_file, file_name="text.md"):
  file_dir = os.path.dirname(os.path.realpath(calling_file))
  file_path = os.path.join(file_dir, file_name)
  with open(file_path, 'r') as file:
    content = file.read()
    return content