import asyncio
from requests_html import HTMLSession
from aiohttp import ClientSession
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

import logging

logging.basicConfig(
  filename="jumia.log", 
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
            url = f"https://www.jumia.com.ng/catalog/?q={search_word}&page={num}"
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
    soup = BeautifulSoup(page, "html.parser")
    items = soup.select("div.prd-w article.c-prd")
    
    products = []
    
    for item in items:
        image = item.select_one("div.img-c img").get("src")
        title = item.select_one("div.info h3.name").text.strip()
        try:
          old_price = item.select_one("div.info p.prc span.old").text.strip()
        except:
          old_price = ""
        new_price = item.select_one("div.info p.prc span.curr").text.strip()
        
        products.append({
            "title": title,
            "image": image,
            "old_price": old_price,
            "new_price": new_price
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
    with open("to_scrape/jumia.html", "r") as file:
        print(parse_page(file.read()))