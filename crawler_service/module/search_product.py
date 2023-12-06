from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import random
from .logger import get_logger
import json

def get_random_sleep_time():
    return random.randrange(5)

def initialize_driver():
    options = Options()
    options.binary_location = "/usr/bin/chromium"

    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features")
    options.add_argument("--disable-blink-features=AutomationControlled")

    options.add_experimental_option('useAutomationExtension', False)
    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 9_13_2) AppleWebKit/613.1.89 (KHTML, like Gecko) Version/10.1.4 Safari/611.2.4"
    options.add_argument('--user-agent=%s' % user_agent)
    options.add_experimental_option("excludeSwitches", ['enable-automation'])

    s = Service("/usr/bin/chromedriver")
    driver = webdriver.Chrome(service=s, options=options)

    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
                        Object.defineProperty(navigator, 'webdriver', {
                          get: () => undefined
                        })
                      """
    })
    return driver

def extract_product_data(product):
    seller_id_element = product.find_elements(By.XPATH, ".//p[@data-testid='listing-card-text-seller-name']")
    product_link_element = product.find_elements(By.XPATH, ".//a[starts-with(@href, '/p')]")
    product_name_element = product.find_elements(By.XPATH, ".//img[contains(@src, 'products')]")
    price_element = product.find_elements(By.XPATH, ".//p[@title[starts-with(., 'NT$')]]")

    return {
        "seller_id": seller_id_element[0].text if seller_id_element else "",
        "product_link": product_link_element[0].get_attribute("href") if product_link_element else "",
        "product_name": product_name_element[0].get_attribute("title") if product_name_element else "",
        "price": price_element[0].text if price_element else ""
    }

def search_product(url):
    driver = None
    try:
        driver = initialize_driver()
        driver.get(url)
        time.sleep(4+get_random_sleep_time())

        # print(driver.page_source)

        product_list = driver.find_elements(By.XPATH, "//main[@id='main']/div[2]/div/section[3]/div[1]/div/div/div[1]/div[not(@data-google-query-id) and not(descendant::*[@data-google-query-id])]")
        results = []

        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")

        for product in product_list:
            product_data = extract_product_data(product)
            results.append({**product_data, "page_source":product.get_attribute('outerHTML'), "created_at": timestamp})

        filename = f"data/{timestamp}.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Error occurred while processing {url}: {e}")
        raise
    finally:
        if driver:
            driver.quit()