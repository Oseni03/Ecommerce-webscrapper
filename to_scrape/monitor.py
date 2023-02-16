from bs4 import BeautifulSoup
from requests_html import HTMLSession

import random
import json

UA_STRINGS = [
  "Mozilla/5.0 (Linux; Android 12; SM-S906N Build/QP1A.190711.020; wv) AppleWebKit/537.36\
      (KHTML, like Gecko) Version/4.0 Chrome/80.0.3987.119 Mobile Safari/537.36",
  "Mozilla/5.0 (Linux; Android 10; SM-G996U Build/QP1A.190711.020; wv) AppleWebKit/537.36\
      (KHTML, like Gecko) Version/4.0 Mobile Safari/537.36",
  "Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15\
      (KHTML, like Gecko) CriOS/69.0.3497.105 Mobile/15E148 Safari/605.1"
]


def get_page(url, filename):
    HEADERS = {
        'User-Agent': random.choice(UA_STRINGS),
        'Accept-Language': 'en-US, en;q=0.5'
    }
    s = HTMLSession()
    r = s.get(url, headers=HEADERS)
    soup = BeautifulSoup(r.text, 'html.parser')
    try:
      with open(f"{filename}.html", "w") as file:
        file.write(str(soup.prettify()))
    except:
      with open(f"{filename}.html", "w") as file:
        file.write(r.text)
    return "Done"


def get_api(url, filename):
    HEADERS = {
        'User-Agent': random.choice(UA_STRINGS),
        'Accept-Language': 'en-US, en;q=0.5'
    }
    s = HTMLSession()
    resp = s.get(url, headers=HEADERS)
    with open(f"{filename}.json", "w") as file:
      json.dump(resp.json(), file)
    return "done"
  
  
# print(get_page("https://www.jumia.com.ng/catalog/?q=phone&page=2", "jumia"))
# print(get_page("https://www.jumia.com.ng/tecno-spark-9-4gb64gb-memory-sky-mirror-197165342.html", "jumia_prod_page"))

# print(get_page("https://www.konga.com/search?search=Iphone&page=2", "konga"))
# print(get_page("https://www.konga.com/product/iphone-usb-c-fast-charger-20w-pd-type-c-5963832?seller_id=209912&sku_id=5963832&sclid=hT2vJ42Y3VanWofDQ1AX07SQ6f0CH8Uy", "konga_prod_page"))

# print(get_page("https://payporte.com/catalogsearch/result/index/?p=3&q=versace+fema", "payporte"))
# print(get_page("https://payporte.com/maternity-off-shoulder-lettuce-trim-rib-knit-crop-top.html", "payporte_prod_page"))

# print(get_page("https://slot.ng/catalogsearch/result/index/?p=2&q=Iphone", "slot"))
# print(get_page("https://slot.ng/iphone-11-pro-3d-screen-guard.html", "slot_prod_page"))

# print(get_page("https://kara.com.ng/catalogsearch/result/index/?p=2&q=iPhone", "kara"))
# print(get_page("https://kara.com.ng/d-link-dch-s150-wi-fi-smart-motion-sensor", "kara_prod_page"))

# print(get_page("https://jiji.ng/search?query=Corolla", "jiji"))
# print(get_page("https://jiji.ng/mushin/car-parts-and-accessories/today-corolla-boot-yy2IeiyZ7D479pEA0ZBKKMde.html?page=3&pos=21&cur_pos=21&ads_per_page=23&ads_count=9839&lid=eAHoZc50iiliY8zd&indexPosition=66", "jiji_prod_page"))
# print(get_api("https://jiji.ng/api_web/v1/listing?query=Air+conditioner&page=2", "jiji")) # JSON API


# print(get_page("https://obiwezy.com/catalogsearch/result/index/?p=2&q=Iphone", "obiwezy"))
# print(get_page("https://obiwezy.com/kolors-safari-themed-phone-case-for-iphone-12-pro-max.html", "obiwezy_prod_page"))

# print(get_page("https://www.ajebomarket.com/catalogsearch/result/index/?p=2&q=Shoe", "ajebomarket"))
# print(get_page("https://www.ajebomarket.com/j-f-s-wooven-tassel-brown.html", "ajebomarket_prod_page"))

# print(get_page("https://buycars.ng/?s=Toyota&post_type=product&dgwt_wcas=1", "buycars"))
# print(get_page("https://buycars.ng/product/sienna-xle/", "buycars_prod_page"))

# print(get_api("https://olist.ng/api/item/home-recommend?page=7&size=10&city_id=0", "olist_recommendation"))
# print(get_api("https://olist.ng/api/item/search?page=6&size=10&keyword=Iphone%206&cat_id=&subcat_id=&state_id=&priceMax=&priceMin=", "olist"))

# print(get_page("https://www.kaiglo.com/category/search?search=Iphone%206", "kaiglo"))
# print(get_page("https://www.kaiglo.com/", "kaiglo_recommendation"))

# print(get_api("https://api.kilimall.com/ke/v1/product/search?a_id=&brand_id=&gc_id=&logistic_type=&keyword=Iphone+6&min=&max=&size=50&page=2", "kilimall"))
# print(get_api("https://api.kilimall.com/ke/v1/product/recommend?size=50&page=3&total=500&type=1", "kilimall_recommendation"))

print(get_page("https://www.imdb.com/calendar/?ref_=rlm&region=TR&type=MOVIE", "imdb_calender"))