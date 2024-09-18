from .. utils import do_update
from . import helpers
from src.utils.get_all_cc_tickets import get_all_ticket_numbers


def get_regex():
  return do_update.get_regex('**Staging Review artifacts**', '##### Platform actions')

def update_body(body):
  '''
  update ticket body with new text
  '''
  body = do_update.update(body=body, regex=get_regex(), new_text=helpers.get_sr_text())
  return body

# get list of all tickets except those with staging-review label
def get_tickets():
    return get_all_ticket_numbers(None, ['staging-review'])
