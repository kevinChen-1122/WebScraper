from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
from . import mongo_module
from urllib.parse import urlparse, urlunparse
from .logger import get_logger
import json
import re


def get_random_sleep_time():
    return random.randrange(3)


def parse_url(url):
    parsed_url = urlparse(url)
    return urlunparse(parsed_url._replace(query=''))


def extract_product_data(product):
    seller_id_element = product.find_elements(By.XPATH, ".//p[@data-testid='listing-card-text-seller-name']")
    product_link_element = product.find_elements(By.XPATH, ".//a[starts-with(@href, '/p')]")
    product_name_element = product.find_elements(By.XPATH, ".//img[contains(@src, 'products')]")
    price_element = product.find_elements(By.XPATH, ".//p[@title[starts-with(., 'NT$')]]")

    return {
        "seller_id": seller_id_element[0].text if seller_id_element else "",
        "product_link": parse_url(product_link_element[0].get_attribute("href")) if product_link_element else "",
        "product_name": product_name_element[0].get_attribute("title") if product_name_element else "",
        "price": price_element[0].text if price_element else ""
    }


def search_product(url, driver_pool):
    driver = None
    try:
        driver = driver_pool.pop()
        time.sleep(get_random_sleep_time())
        driver.get(url)
        time.sleep(4 + get_random_sleep_time())
        # print(driver.page_source)

        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

        db = mongo_module.connect_to_mongodb()
        collection = db['get_url_log']
        mongo_module.insert_document(collection,
                                     {"search_url": url, "page": driver.page_source, "created_at": timestamp})

        WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.XPATH,
                                            "//main[@id='main']/div[2]/div/section[3]/div[1]/div/div/div[1]/div[not("
                                            "@data-google-query-id) and not(descendant::*[@data-google-query-id])]"))
        )

        product_list = driver.find_elements(By.XPATH,
                                            "//main[@id='main']/div[2]/div/section[3]/div[1]/div/div/div[1]/div[not("
                                            "@data-google-query-id) and not(descendant::*[@data-google-query-id])]")
        results = []

        for product in product_list:
            product_data = extract_product_data(product)
            results.append({**product_data, "page_source": product.get_attribute('outerHTML'), "created_at": timestamp})

        if results:
            # db = mongo_module.connect_to_mongodb()
            collection = db['search_product']
            mongo_module.update_documents(collection, results)

        # pattern = r"/search/(.*?)\?"
        # match = re.search(pattern, url)
        # filename = f"data/{timestamp}({match.group(1)}).txt"
        # with open(filename, 'w', encoding='utf-8') as f:
        #     json.dump(results, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Error occurred while processing {url}: {e}")
        raise
    finally:
        if driver:
            driver.get("about:blank")
            driver_pool.append(driver)
