import asyncio
import logging
from bs4 import BeautifulSoup 
from aiohttp import ClientSession 
from requests_html import HTMLSession 
from concurrent.futures import ThreadPoolExecutor

import pandas as pd


logging.basicConfig(
  filename="indeed.log", 
  level=logging.DEBUG, 
  format="%(asctime)s - %(message)", 
  datefmt="%d-%b-%y %H:%M:%S")

async def fetch(url, session):
  async with session.get(url) as resp:
    html_body = await resp.read()
    return html_body


async def get_pages(url, job_search, page_num):
  tasks = []
  # semaphore 
  # sem = asyncio.Semaphore(10)
  async with ClientSession() as session:
    for i in range(0, page_num):
      url = url.format(job_search, i)
      tasks.append(
        asyncio.create_task(fetch(url, session))
      )
  return tasks 


def parse_page(page):
  job_list = []
  
  soup = BeautifulSoup(page, "html.parser")
  items = soup.select("div.jobsearch-SerpJobCard")
  for item in items:
    title = item.select_one("h2 a").text.strip()
    company = item.select_one("span.company").text.strip()
    try:
      salary = item.select_one("span.salaryText").text.strip()
    except:
      salary = "" 
    summary = item.select_one("div.summary").text.strip()
    
    job_list.append({
      "title": title,
      "company": company,
      "salary": salary,
      "summary": summary,
    })
  save(job_list)
  return


def save(job_list):
  df = pd.DataFrame(job_list)
  print(df.head())
  df.to_csv("jobs.csv")
  return 


def main(job_search):
  url = f"https://www.indeed.co.uk/jobs?q={}&l=London,+Greater+London&start={}"
  page_num = 10
  pages = asyncio.run(get_pages(url, job_search, page_num))
  with ThreadPoolExecutor() as executor:
    executor.map(parse_page, pages)
  