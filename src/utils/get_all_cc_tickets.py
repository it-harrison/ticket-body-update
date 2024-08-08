import httpx
from . requests import get_headers, URL

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
      ticket_numbers.append(ticket['number'])
    return len(tickets)

# aggregate all pages of CC request tickets
def get_all_ticket_numbers(params=None):
  ticket_numbers = []
  page = 1
  while True:
    _params = get_params(page, params)
    more = get_ticket_numbers(ticket_numbers, _params)
    if more < 100:
      break
    page += 1
  return ticket_numbers