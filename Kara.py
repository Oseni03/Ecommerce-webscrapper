import asyncio
from requests_html import HTMLSession
from aiohttp import ClientSession
from bs4 import BeautifulSoup

import logging

logging.basicConfig(
  filename="kara.log", 
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
            url = f"https://kara.com.ng/catalogsearch/result/index/?p={num}&q={search_word}"
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
    items = soup.select("ol.products.product-items li.product-item")
    
    products = []
    
    for item in items:
        image = item.select_one("img.product-image-photo").get("src")
        title = item.select_one("h2.product-item-name").text.strip()
        price = item.select_one("div.price-final_price span.price-wrapper").get("data-price-amount")
        url = item.select_one("h2.product-item-name a").get("href")
        
        products.append({
            "title": title,
            "image": image,
            "price": price,
            "url": url,
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
    with open("to_scrape/kara.html", "r") as file:
        print(parse_page(file.read()))