from . import helpers
from .. utils import do_update

def get_regex(touchpoint):
  '''
  get regex for each touchpoint
  '''
  return {
    'di': do_update.get_regex('### Design Intent.*actions', '\*\*Design Intent artifacts'),
    'mpr': do_update.get_regex('### Midpoint Review.*actions','\*\*Midpoint Review artifacts'),
    'sr': do_update.get_regex('### Staging Review.*actions', '\*\*Staging Review artifacts')
  }[touchpoint]

def get_text(touchpoint):
  '''
  get the new text for each touchpoint
  '''
  return helpers.__dict__[f'get_{touchpoint}_text']()

def update_body(body):
  '''
  update ticket body with new text for all touchpoints
  '''
  for touchpoint in ['di', 'mpr', 'sr']:
    regex = get_regex(touchpoint)
    body = do_update.update(body, regex, get_text(touchpoint))
  return body
