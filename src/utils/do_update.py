import re

def get_regex(before, after):
  '''
  generate a regex to break apart a ticket's body
  provide a before group and after group to target 
  a middle group for replacement
  '''
  return rf"(.*{before})(.*)({after}.*)"


def update(body, regex, new_text):
  '''
  update a ticket's body with a regex that splits the body into three groups
  replace the middle group with new_text
  '''
  matches = re.search(regex, body, re.DOTALL)
  if matches:
    return f'{matches.group(1)}{new_text}{matches.group(3)}'
  return body


