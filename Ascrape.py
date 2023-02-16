import grequests
from bs4 import BeautifulSoup 


def get_pagination_links():
  urls = []
  
  page_num = 0
  while True:
    url = f"http://book.toscrape.com/catalogue/page-{page_num}.html"
    reqs = requests.get(url)
    if reqs:
      urls.append(reqs)
      page_num += 1
    else:
      break
  return urls


def get_data(urls):
  reqs = [grequests.get(url) for url im urls]
  resp = grequests.map(reqs)
  return resp


def parse_data(r):
  soup = BeautifulSoup(r.text, "lxml")
  articles = soup.select("article.product_prod")
  for item in articles:
    pass 
  return 


def main():
  urls = get_pagination_links()
  resp = get_data(urls)
  
  with ThreadPoolExecutor() as executor:
    executor.map(parse_data, resp)
