import asyncio
import httpx
import re
import helpers

TOKEN = '<your GH token>'
URL = 'https://api.github.com/repos/department-of-veterans-affairs/va.gov-team/issues'
INFLIGHT_LIMIT = 10

# get the headers for a request to GH api
def get_headers():
  return {
      'Authorization': f'Bearer {TOKEN}',
      'Content-Type': 'application/json',
      'Accept': 'application/vnd.github.v3+json'
    }

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
    page+=1
  return ticketNums

# get a client to make async requests
def get_async_client():
  return httpx.AsyncClient(headers=get_headers())

# wrapper to use the semaphore to update ticket
async def patch_wrapper(semaphore, number, errors):
  async with semaphore:
    await patch_issue(number, errors)

# update the ticket
async def patch_issue(number, errors):
  async with get_async_client() as client:
    try:
      url = f'{URL}/{number}'
      response = await client.get(url)
      response.raise_for_status()
      body = response.json()['body']
      body = update_body(body)
      patch_response = await client.patch(url, json={'body': body})
      patch_response.raise_for_status()
    except httpx._exceptions.HTTPStatusError:
      errors.append(number)

# get regex for each touchpoint
def get_regex(touchpoint):
  return {
    'di': r'(.*)(### Design Intent.*actions)(.*)(\*\*Design Intent artifacts)(.*)',
    'mpr': r'(.*)(### Midpoint Review.*actions)(.*)(\*\*Midpoint Review artifacts)(.*)',
    'sr': r'(.*)(### Staging Review.*actions)(.*)(\*\*Staging Review artifacts)(.*)'
  }[touchpoint]

# get the new text for each touchpoint
def get_text(touchpoint):
  if touchpoint == 'di':
    return helpers.get_di_text()
  elif touchpoint == 'mpr':
    return helpers.get_mpr_text()
  elif touchpoint == 'sr':
    return helpers.get_sr_text()

# update ticket body with new text for all touchpoints
def update_body(body):
  for touchpoint in ['di', 'mpr', 'sr']:
    regex = get_regex(touchpoint)
    matches = re.search(regex, body, re.DOTALL)
    if matches:
      start = f'{matches.group(1)}{matches.group(2)}'
      end = f'{matches.group(4)}{matches.group(5)}'
      body = f'{start}{get_text(touchpoint)}{end}'
    else:
      continue
  return body

async def main():
  try:
    ticket_numbers = get_all_ticket_numbers()
    errors = []
    # only have 10 requests in flight at a time
    semaphore = asyncio.Semaphore(INFLIGHT_LIMIT)
    tasks = [asyncio.create_task(patch_wrapper(semaphore, number, errors)) 
             for number in ticket_numbers]
    await asyncio.gather(*tasks)

    if len(errors) > 0:
      print('the errors are \n', errors)
    print('done!')
  except httpx._exceptions.HTTPError or httpx._exceptions.HTTPStatusError:
    print('could not get ticket numbers')
  
asyncio.run(main())

