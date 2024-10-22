from .. utils import do_update, load_text
from src.utils.get_all_cc_tickets import get_all_ticket_numbers

def get_regex():
  return do_update.get_regex('LANDMARK 1', 'LANDMARK 2')

def update_body(body):
  '''
  update ticket body with new text
  '''
  new_text=load_text.get_text(__file__)
  body = do_update.update(body=body, regex=get_regex(), new_text=new_text)
  return body

# get list of ticket numbers
def get_tickets():
    #by default we return tickets with CC-Request and collaboration-cycle
    param = { 'labels': ['label-to-include']}

    # add tickets to the list that you do not want updated
    tickets_to_ignore = []

    return get_all_ticket_numbers(param, ['label-to-exclude'], tickets_to_ignore)