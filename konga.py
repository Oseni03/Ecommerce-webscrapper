import asyncio
import json
from requests_html import HTMLSession
from aiohttp import ClientSession
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

import logging

# logging.basicConfig(
#   filename="konga.log", 
#   level=logging.DEBUG, 
#   format="%(asctime)s - %(message)", 
#   datefmt="%d-%b-%y %H:%M:%S")

async def fetch(url, session):
  async with session.get(url) as resp:
    html_body = await resp.read()
    return html_body
    
    
async def get_pages(search_word):
    tasks = []
  
    async with ClientSession() as session:
        num = 1
        while True:
            url = f"https://www.konga.com/search?search={search_word}&page={num}"
            try:
                tasks.append(
                    asyncio.create_task(fetch(url, session))
                )
            except:
                break
            num += 1
        pages_content = await asyncio.gather(*tasks)
        return pages_content


def parse_page(page):
    soup = BeautifulSoup(page, "lxml")
    script = soup.select_one("script#__NEXT_DATA__").text.strip().replace("\n", "")
    data = json.loads(script)
    
    products = []
    
    for item in data["props"]["initialProps"]["pageProps"]["resultsState"]["content"]["hits"]:
        products.append({
            "title": item["name"],
            "price": item["price"],
            "special_price": item["special_price"],
            "image": item["image_thumbnail_path"],
            "description": item["description"],
            "availability": item["stock"]["in_stock"],
        })
    save(products)
    return products


def save(products):
    pass


def main(search_word):
    pages = asyncio.run(get_pages(search_word))
    with ThreadPoolExecutor() as executor:
        executor.map(parse_page, pages)

if __name__=="__main__":
    with open("to_scrape/konga.html", "r") as file:
        print(parse_page(file.read()))