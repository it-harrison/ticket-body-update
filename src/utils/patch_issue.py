import httpx
from .requests import URL, get_headers

# update the body of a ticket by means of an update_func
async def patch_issue(semaphore, number, errors, update_func):
  async with semaphore:
    async with httpx.AsyncClient(headers=get_headers()) as client:
      try:
        url = f'{URL}/{number}'
        response = await client.get(url)
        response.raise_for_status()
        _body = response.json()['body']
        body = update_func(_body)
        patch_response = await client.patch(url, json={'body': body})
        patch_response.raise_for_status()
      except httpx._exceptions.HTTPStatusError:
        errors.append((number, response.status_code))