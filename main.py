import asyncio
import httpx
import re
import helpers

TOKEN = '<your GH token>'
URL = 'https://api.github.com/repos/department-of-veterans-affairs/va.gov-team/issues'

def getHeaders():
  return {
      'Authorization': f'Bearer {TOKEN}',
      'Content-Type': 'application/json',
      'Accept': 'application/vnd.github.v3+json'
    }

def getTicketNumbers(page, nums):
  params = {
    'per_page': 100,
    'page': page,
    'labels': ['CC-Request', 'collaboration-cycle']
  }

  with httpx.Client() as client:
    resp = client.get(URL, headers=getHeaders(), params=params)
    resp.raise_for_status()
    tickets = resp.json()
    for ticket in tickets:
      nums.append(ticket['number'])
    return len(tickets)

def getAllTicketNumbers():
  ticketNums = []
  page = 1
  while True:
    more = getTicketNumbers(page, ticketNums)
    if more < 100:
      break
    page+=1
  return ticketNums

def getAsyncClient():
  return httpx.AsyncClient(headers=getHeaders())

async def patchIssue(number, errors):
  client = getAsyncClient()
  async with client:
    url = f'{URL}/{number}'
    try:
      response = await client.get(url)
      response.raise_for_status()
      body = response.json()['body']
      body = updateBody(body)
      patchResponse = await client.patch(url, json={'body': body})
      patchResponse.raise_for_status()
    except httpx._exceptions.HTTPStatusError:
      errors.append(number)

def getRegex(touchpoint):
  return {
    'di': r'(.*)(### Design Intent.*actions)(.*)(\*\*Design Intent artifacts)(.*)',
    'mpr': r'(.*)(### Midpoint Review.*actions)(.*)(\*\*Midpoint Review artifacts)(.*)',
    'sr': r'(.*)(### Staging Review.*actions)(.*)(\*\*Staging Review artifacts)(.*)'
  }[touchpoint]

def getText(touchpoint):
  if touchpoint == 'di':
    return helpers.getDIText()
  elif touchpoint == 'mpr':
    return helpers.getMPRText()
  elif touchpoint == 'sr':
    return helpers.getSRText()

def updateBody(body):
  for touchpoint in ['di', 'mpr', 'sr']:
    regex = getRegex(touchpoint)
    matches = re.search(regex, body, re.DOTALL)
    if matches:
      body = f'''{matches.group(1)}{matches.group(2)}
{getText(touchpoint)}{matches.group(4)}{matches.group(5)}'''
    else:
      continue
  return body

async def main():
  try:
    # tickets = getAllTicketNumbers()
    tickets = [88068]
    errors = []
    tasks = [patchIssue(ticket, errors) for ticket in tickets]
    for i in range(0, len(tasks), 10):
      group = tasks[i:i+10]
      await asyncio.gather(*group)
    if len(errors) > 0:
      print('the errors are', errors)
  except httpx._exceptions.HTTPError or httpx._exceptions.HTTPStatusError:
    print('could not get ticket numbers')
  
asyncio.run(main())

