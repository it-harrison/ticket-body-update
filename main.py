import asyncio
import httpx
from dotenv import load_dotenv
from src.utils.patch_issue import patch_issue
from  src.utils.get_all_cc_tickets import get_all_ticket_numbers
# import the update function you want to use
from src.update_vfs_scheduling.update_function import update_body

INFLIGHT_LIMIT = 10

load_dotenv()

async def main():
  try:
    ticket_numbers = get_all_ticket_numbers()
    errors = []
    # only have 10 requests in flight at a time
    semaphore = asyncio.Semaphore(INFLIGHT_LIMIT)
    tasks = [asyncio.create_task(patch_issue(semaphore, number, errors, update_body)) 
      for number in ticket_numbers]
    await asyncio.gather(*tasks)
    if len(errors) > 0:
      print('the errors are \n', errors)
    print('all tickets updated!')
  except httpx._exceptions.HTTPError or httpx._exceptions.HTTPStatusError as e:
    print(f'could not get ticket numbers: {e}')
  

if __name__ == "__main__":
  asyncio.run(main())

