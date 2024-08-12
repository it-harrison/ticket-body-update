import httpx
from . requests import get_headers, URL
from collections import namedtuple

Ticket = namedtuple("Ticket", "number labels")

#params for GH request
def get_params(page, base):
  default = {
    'per_page': 100,
    'page': page,
    'labels': ['CC-Request', 'collaboration-cycle']
  }
  if base:
    return {**default, **base}
  return default


# get a page of CC request tickets
def get_ticket_numbers(ticket_numbers, params):
  with httpx.Client() as client:
    resp = client.get(URL, headers=get_headers(), params=params)
    resp.raise_for_status()
    tickets = resp.json()
    for ticket in tickets:
      labels = [label['name'] for label in ticket['labels']]
      ticket_numbers.append(Ticket(ticket['number'], labels))
    return len(tickets)

# aggregate all pages of CC request tickets
def get_all_ticket_numbers(params=None):
  tickets = []
  page = 1
  while True:
    _params = get_params(page, params)
    more = get_ticket_numbers(tickets, _params)
    if more < 100:
      break
    page += 1
  filtered_data = get_tickets_with_all_labels(tickets, _params['labels'])
  return filtered_data

# our default is opposite of GH: we want tickets with all specified labels (AND not OR)
def get_tickets_with_all_labels(numbers, labels):
  def check(ticket):
    for label in labels:
      if label not in ticket.labels:
        return False
    return True
  
  cc_tickets = filter(check, numbers)
  return [ticket.number for ticket in cc_tickets]