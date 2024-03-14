from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from . import mongo_module
from urllib.parse import urlparse, urlunparse
from datetime import datetime, timedelta
import re
import traceback


def is_new_product(string_of_since_at):
    return string_of_since_at and int(parse_relative_time(string_of_since_at)) < 300


def parse_url(url):
    parsed_url = urlparse(url)
    return urlunparse(parsed_url._replace(query=''))


def parse_relative_time(relative_time_str):
    match = re.match(r'(\d+)\s+(\w+)\s+ago$', relative_time_str)
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
    product_add_since_element = product.find_element(By.XPATH, ".//div[1]/a[1]/div[2]/div/p")

    return {
        "seller_id": seller_id_element[0].text if seller_id_element else "",
        "product_link": parse_url(product_link_element[0].get_attribute("href")) if product_link_element else "",
        "product_name": product_name_element[0].get_attribute("title") if product_name_element else "",
        "price": price_element[0].text if price_element else "",
        "product_add_at": date_format(product_add_since_element.text) if product_add_since_element else "",
        "product_add_since": product_add_since_element.text if product_add_since_element else ""
    }


def search_product(url, driver_pool):
    driver = None

    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

    # get_page_log = {
    #     "search_url": url,
    #     "page": '',
    #     "created_at": timestamp
    # }
    product_list_data = []
    product_notify_data = []
    db = mongo_module.connect_to_mongodb()
    collection = db['line_notify_log']

    try:
        driver = driver_pool.get_driver()
        driver.get(url)
        # get_page_log["page"] = driver.page_source

        time.sleep(3)

        product_list = WebDriverWait(driver, 3).until(
            EC.presence_of_all_elements_located((By.XPATH,
                                                 "//div[@data-testid[starts-with(., 'listing-card-')"
                                                 "and substring-after(., 'listing-card-') ="
                                                 "translate(substring-after(., 'listing-card-'), ' ', '')]]"))
        )

        for product in product_list:
            product_data = extract_product_data(product)
            product_list_data.append({
                **product_data,
                "page_source": product.get_attribute('outerHTML'),
                "created_at": timestamp
            })

            if is_new_product(product_data["product_add_since"]):
                product_notify_data.append({
                    "content": product_data["product_name"] + "\n" + product_data["product_link"],
                    "status": "PENDING",
                    "created_at": timestamp
                })
    except Exception:
        raise Exception(f"{traceback.format_exc()}")
    finally:
        if driver:
            driver.get("about:blank")
            driver_pool.release_driver(driver)

        # if get_page_log:
        #     mongo_module.insert_document(db['get_url_log'], get_page_log)

        if product_list_data:
            mongo_module.update_documents(db['search_product'], product_list_data)

        if product_notify_data:
            existing_contents = collection.distinct("content")
            filtered_data = [data for data in product_notify_data if data["content"] not in existing_contents]
            if filtered_data:
                mongo_module.insert_documents(collection, filtered_data)
