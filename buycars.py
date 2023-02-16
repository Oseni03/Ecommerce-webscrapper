import asyncio
from requests_html import HTMLSession
from aiohttp import ClientSession
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

import logging

logging.basicConfig(
  filename="buycars.log", 
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
            url = f"https://buycars.ng/?s={search_word}&post_type=product&dgwt_wcas=1"
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
    items = soup.select("li.et-item.post.product")
    
    products = []
    
    for item in items:
        image = item.select_one("div.image-container.visible img.attachment-shop_catalog").get("data-src")
        title = item.select_one("h6.post-title").text.strip()
        price = item.select_one("div.post-body span.price").text.strip().replace(",", "")
        url = item.select_one("h6.post-title a").get("href")
        
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


def stock_checker(page):
    soup = BeautifulSoup(page, "html.parser")
    availability = soup.select_one("div[title='Availability'] span").text.strip()
    qty = soup.select_one("div[title='Qty']").text.strip().replace("\n", "").replace("          ", " ")
    return {"availability": availability, "qty": qty}


def main(search_word):
    pages = asyncio.run(get_pages(search_word))
    with ThreadPoolExecutor() as executor:
        executor.map(parse_page, pages)


if __name__=="__main__":
    with open("to_scrape/buycars.html", "r") as file:
        print(parse_page(file.read()))