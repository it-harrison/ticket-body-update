import os

def get_sr_text():
  
  file_dir = os.path.dirname(os.path.realpath(__file__))
  file_path = os.path.join(file_dir, 'text.md')
  with open(file_path, 'r') as file:
    content = file.read()
    return content
