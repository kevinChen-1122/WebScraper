from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from config import config
from lib import url
import time
import random
import json

def fetch_data(url):
    driver = None
    try:
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-blink-features")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option('useAutomationExtension', False)
        options.binary_location = "/usr/bin/chromium"
        user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15"
        options.add_argument('--user-agent=%s' % user_agent)
        options.add_experimental_option("excludeSwitches",['enable-automation'])

        s = Service("/usr/bin/chromedriver")
        driver = webdriver.Chrome(service=s, options=options)
        time.sleep(5)
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                  "source": """
                    Object.defineProperty(navigator, 'webdriver', {
                      get: () => undefined
                    })
                  """
                })

        driver.get(url)
        time.sleep(5)

        product_list = driver.find_elements(By.XPATH,"//div[@class='D_tX D_Ak']")
        results = []

        for product in product_list:
            seller_id = product.find_element(By.XPATH, ".//div[contains(@class, 'D__h')]//p[contains(@class, 'D_oP') and contains(@class, 'D_nO') and contains(@class, 'D_oQ') and contains(@class, 'D_oU') and contains(@class, 'D_oW') and contains(@class, 'D_pa') and contains(@class, 'D_pe') and contains(@class, 'D_ph')]").text
            product_link = product.find_element(By.XPATH,".//a[contains(@class, 'D_py') and starts-with(@href, '/p')]").get_attribute("href")
            product_name = product.find_element(By.XPATH,".//p[contains(@class, 'D_oP') and contains(@class, 'D_nO') and contains(@class, 'D_oQ') and contains(@class, 'D_oU') and contains(@class, 'D_oX') and contains(@class, 'D_pa') and contains(@class, 'D_pc') and contains(@class, 'D_oY') and contains(@class, 'D_ph')]").text
            price = product.find_element(By.XPATH,".//p[contains(@class, 'D_oP') and contains(@class, 'D_nO') and contains(@class, 'D_oQ') and contains(@class, 'D_oU') and contains(@class, 'D_oW') and contains(@class, 'D_pa') and contains(@class, 'D_pe') and contains(@class, 'D_pg')]").text

            results.append({
                    "seller_id":seller_id,
                    "product_link": product_link,
                    "product_name":product_name,
                    "price":price
                })

        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
        random_number = random.random()
        filename = f"{timestamp}{random_number}.txt"

        with open(filename, 'w') as file:
            file.write(json.dumps(results))
    except Exception as e:
        with open("err.log", 'a') as file:
            file.write(json.dumps({"url":url,"error": str(e),"time":datetime.now().strftime("%Y-%m-%d_%H-%M-%S")})+"\n")
    finally:
        if driver:
            driver.quit()

a=[]
with ThreadPoolExecutor(max_workers=4) as executor:
    for item in config.key_word:
        a.append(url.get_search_url(item["key_word"],item["price_start"],item["price_end"]))

    futures = [executor.submit(fetch_data, url) for url in a]

    for future in futures:
        result = future.result()