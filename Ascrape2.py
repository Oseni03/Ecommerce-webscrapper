import asyncio
from aiohttp import ClientSession 
import pathlib 

async def fetch(url, session):
  async with session.get(url) as resp:
    html_body = await resp.read()
    return html_body

async def fetch_with_sem(url, session, sem):
  async with sem:
    return await fetch(url, session)

async def main(start_yr=2020, years_ago=5):
  tasks = []
  # semaphore 
  sem = asyncio.Semaphore(10)
  async with ClientSession() as session:
    for i in range(0, years_ago):
      year = start_yr - i 
      url = f"https://www.boxofficemojo/year/{year}"
      tasks.append(
        asyncio.create_task(fetch(url, session))
      )
      
      ## OR ##
      
      tasks.append(
        asyncio.create_task(fetch_with_sem(url, session, sem))
      )
    pages_content = await asyncio.gather(*tasks)
    return pages_content


html_data = asyncio.run(main())