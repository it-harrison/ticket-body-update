from .. utils import do_update, load_text
from src.utils.get_all_cc_tickets import get_all_ticket_numbers

def get_regex():
  return do_update.get_regex('- [ ] Endpoint monitoring playbook', '** Not required, but nice to have artifacts')

def update_body(body):
  '''
  update ticket body with new text
  '''
  new_text=load_text.get_text(__file__)
  body = do_update.update(body=body, regex=get_regex(), new_text=new_text)
  return body

def get_tickets():
    ignore_tickets = [88958, 80777 ]
    return get_all_ticket_numbers(None, ['midpoint-review', 'staging-review'], ignore_tickets)