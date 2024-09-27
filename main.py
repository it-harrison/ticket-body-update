import asyncio
import httpx
from dotenv import load_dotenv
from src.utils.patch_issue import patch_issue
# import the "update_body" and "get_tickets" functions you want to use
from src.update_mpr_artifacts.update_function import update_body, get_tickets

INFLIGHT_LIMIT = 5

load_dotenv()

async def main():
  try:
    ticket_numbers = get_tickets()
    errors = []
    # only have 10 requests in flight at a time
    semaphore = asyncio.Semaphore(INFLIGHT_LIMIT)
    tasks = [asyncio.create_task(patch_issue(semaphore, number, errors, update_body)) 
      for number in ticket_numbers]
    await asyncio.gather(*tasks)
    if len(errors) > 0:
      print('the errors are \n', errors)
  except httpx._exceptions.HTTPError or httpx._exceptions.HTTPStatusError as e:
    print(f'could not get ticket numbers: {e}')
  
  print('all tickets updated!')

if __name__ == "__main__":
  asyncio.run(main())
