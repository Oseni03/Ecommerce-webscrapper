import json
import asyncio
from requests_html import HTMLSession
from aiohttp import ClientSession
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

import logging

logging.basicConfig(
  filename="jiji.log", 
  level=logging.DEBUG, 
  format="%(asctime)s - %(message)", 
  datefmt="%d-%b-%y %H:%M:%S")


async def fetch(url, session):
  async with session.get(url) as resp:
    html_body = await resp.read()
    return html_body
    
    
async def get_pages(search_word):
    tasks = []
    
    async with ClientSession() as session:
        num = 1
        while True:
            url = f"https://jiji.ng/api_web/v1/listing?query={search_word}&page={num}"
            try:
                tasks.append(
                    asyncio.create_task(fetch(url, session))
                )
            except:
                break
            num += 1
        pages_content = await asyncio.gather(*tasks)
        return pages_content


def parse_json(page):
    products = []
    
    items = page["adverts_list"]["adverts"]
    for item in items:
        products.append({
            "title": item["title"],
            # "tags": [{name: value} for name, value in item["attrs"]],
            "image": item["image_obj"]["url"],
            "price": item["price_obj"]["value"],
            "location": item["region_item_text"],
            "description": item["short_description"],
            "status": item["status"],
            "url": item["url"],
        })
    save(products)
    return products


def save(products):
    pass


def main(search_word):
    pages = asyncio.run(get_pages(search_word))
    with ThreadPoolExecutor() as executor:
        executor.map(parse_json, pages)

if __name__=="__main__":
    # with open("to_scrape/jiji.json", "r") as file:
    #     fp = json.load(file)
    #     print(parse_json(fp))
    
    data = json.load(open('to_scrape/jiji.json'))
    jtopy=json.dumps(data) #json.dumps take a dictionary as input and returns a string as output.
    dict_json=json.loads(jtopy) # json.loads take a string as input and returns a dictionary as output.
    print(parse_json(dict_json))