import random
import pprint
from requests_html import HTMLSession
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin


UA_STRINGS = [
    "Mozilla/5.0 (Linux; Android 12; SM-S906N Build/QP1A.190711.020; wv) AppleWebKit/537.36\
        (KHTML, like Gecko) Version/4.0 Chrome/80.0.3987.119 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; SM-G996U Build/QP1A.190711.020; wv) AppleWebKit/537.36\
        (KHTML, like Gecko) Version/4.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15\
        (KHTML, like Gecko) CriOS/69.0.3497.105 Mobile/15E148 Safari/605.1"
]


def get_soup(url):
    HEADERS = {
        'User-Agent': random.choice(self.UA_STRINGS),
        'Accept-Language': 'en-US, en;q=0.5'
    }
    s = HTMLSession()
    r = s.get(url, headers=HEADERS)
    return BeautifulSoup(r.text, 'html.parser')
    
def amazon_tracker(url):
    soup = self.get_soup(url)
    
    title = soup.select_one("h1#title").text.strip()
    rating = soup.select_one("span#acrPopover title").text.strip()
    price = soup.select_one("span#price_inside_buybox").text.strip()
    description = soup.select_one("div#renewedProgramDescriptionBtf_feature_div").text.strip()
    customerReview = soup.select_one("span#acrCustomerReviewText").text.strip()
    table = soup.select_one("div#productOverview_feature_div table")
    img_list = []

    images = soup.select_one("div#altImages").select("li")
    for image in images:
        try:
            img = image.select_one("span.a-button-text").img.get("src")
        except:
            img = None
        if img:
            img_list.append(img)
    availability = soup.select_one("div#availability").strip()
    return {
        "title": title,
        "rating": rating,
        "customerReview": customerReview,
        "img_list": img_list,
        "availability": availability, 
        "description": description,
        "price": price,
        "table": table,
    }

