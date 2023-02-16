import asyncio
from aiohttp import ClientSession 


results = []

def get_tasks(session, start_yr=2020, years_ago=5):
  tasks = []
  for i in range(0, years_ago):
    year = start_yr - i 
    url = f"https://www.boxofficemojo/year/{year}"
    tasks.append(session.get(url, ssl=False))
  return tasks 


async def main():
  with ClientSession() as session:
    tasks = get_tasks(session) 
    responses = asyncio.gather(*tasks)
    for resp in responses:
      results.append(await resp.json())


asyncio.run(main())