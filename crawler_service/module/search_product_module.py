from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
from . import mongo_module, line_notify_module
from urllib.parse import urlparse, urlunparse
from datetime import datetime, timedelta
import re


def is_new_product(string_of_since_at):
    return string_of_since_at and int(parse_relative_time(string_of_since_at)) < 300


def get_random_sleep_time():
    return random.randrange(3)


def parse_url(url):
    parsed_url = urlparse(url)
    return urlunparse(parsed_url._replace(query=''))


def parse_relative_time(relative_time_str):
    match = re.match(r'(\d+)\s+(\w+)\s+ago', relative_time_str)
    if match:
        value, unit = int(match.group(1)), match.group(2).lower()
        unit = unit.rstrip('s')
        time_units = {
            'second': 1,
            'minute': 60,
            'hour': 3600,
            'day': 86400,
            'week': 604800,
            'month': 2628000,
            'year': 31536000,
        }
        if unit in time_units:
            return value * time_units[unit]
    return None


def date_format(relative_time_str):
    seconds = parse_relative_time(relative_time_str)
    if not seconds:
        return None
    current_time = datetime.now()
    return (current_time - timedelta(seconds=seconds)).strftime("%Y-%m-%d %H:%M:%S")


def extract_product_data(product):
    seller_id_element = product.find_elements(By.XPATH, ".//p[@data-testid='listing-card-text-seller-name']")
    product_link_element = product.find_elements(By.XPATH, ".//a[starts-with(@href, '/p')]")
    product_name_element = product.find_elements(By.XPATH, ".//img[contains(@src, 'products')]")
    price_element = product.find_elements(By.XPATH, ".//p[@title[starts-with(., 'NT$')]]")
    product_add_since_element = product.find_elements(By.XPATH, ".//p[contains(text(), 'second ago')"
                                                                "or contains(text(), 'seconds ago')"
                                                                "or contains(text(), 'minute ago')"
                                                                "or contains(text(), 'minutes ago')"
                                                                "or contains(text(), 'hour ago')"
                                                                "or contains(text(), 'hours ago')"
                                                                "or contains(text(), 'day ago')"
                                                                "or contains(text(), 'days ago')"
                                                                "or contains(text(), 'months ago')"
                                                                "or contains(text(), 'month ago')"
                                                                "or contains(text(), 'year ago')"
                                                                "or contains(text(), 'years ago')]")

    return {
        "seller_id": seller_id_element[0].text if seller_id_element else "",
        "product_link": parse_url(product_link_element[0].get_attribute("href")) if product_link_element else "",
        "product_name": product_name_element[0].get_attribute("title") if product_name_element else "",
        "price": price_element[0].text if price_element else "",
        "product_add_at": date_format(product_add_since_element[0].text) if product_add_since_element else "",
        "product_add_since": product_add_since_element[0].text if product_add_since_element else ""
    }


def search_product(url, driver_pool):
    driver = None
    try:
        driver = driver_pool.get_driver()
        time.sleep(get_random_sleep_time())
        driver.get(url)

        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

        db = mongo_module.connect_to_mongodb()
        collection = db['get_url_log']
        mongo_module.insert_document(collection,
                                     {"search_url": url, "page": driver.page_source, "created_at": timestamp})

        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH,
                                            "//main[@id='main']/div[2]/div/section[3]/div[1]/div/div/div[1]/div[not("
                                            "@data-google-query-id) and not(descendant::*[@data-google-query-id])]"))
        )

        time.sleep(2)

        product_list = driver.find_elements(By.XPATH,
                                            "//main[@id='main']/div[2]/div/section[3]/div[1]/div/div/div[1]/div[not("
                                            "@data-google-query-id) and not(descendant::*[@data-google-query-id])]")

        time.sleep(2)
        results = []

        for product in product_list:
            product_data = extract_product_data(product)
            results.append({**product_data, "page_source": product.get_attribute('outerHTML'), "created_at": timestamp})

            collection = db['line_notify_log']
            msg = "新商品\n" + product_data["product_name"] + "\n" + product_data["product_link"]
            if is_new_product(product_data["product_add_since"]) and not mongo_module.find_documents(collection,
                                                                                                     {"msg": msg}):
                line_notify_module.send_line_notify(msg)

        if results:
            collection = db['search_product']
            mongo_module.update_documents(collection, results)

    except Exception as e:
        print(f"Error occurred while processing {url}: {e}")
        raise
    finally:
        if driver:
            driver.get("about:blank")
            driver_pool.release_driver(driver)
