import httpx
from . requests import get_headers, URL

# get a page of CC request tickets
def get_ticket_numbers(page, nums):
  params = {
    'per_page': 100,
    'page': page,
    'labels': ['CC-Request', 'collaboration-cycle']
  }

  with httpx.Client() as client:
    resp = client.get(URL, headers=get_headers(), params=params)
    resp.raise_for_status()
    tickets = resp.json()
    for ticket in tickets:
      nums.append(ticket['number'])
    return len(tickets)

# aggregate all pages of CC request tickets
def get_all_ticket_numbers():
  ticketNums = []
  page = 1
  while True:
    more = get_ticket_numbers(page, ticketNums)
    if more < 100:
      break
    page += 1
  return ticketNums