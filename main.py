import asyncio
from dotenv import load_dotenv
from src.utils.patch_issue import patch_issue
# import the "update_body" and "get_tickets" functions you want to use
from src.update_sr_artifacts_ii.update_function import update_body, get_tickets
from src.utils.get_all_cc_tickets import GetTicketsError

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
  except GetTicketsError as e:
    print(f'could not get ticket numbers: {e}')
  finally:
    print(f'{len(ticket_numbers)} total tickets, {len(ticket_numbers) - len(errors)} updated, {len(errors)} errors:')
    [print(error) for error in errors]
      
  
if __name__ == "__main__":
  asyncio.run(main())
