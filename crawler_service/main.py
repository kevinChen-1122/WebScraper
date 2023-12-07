from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from concurrent.futures import ThreadPoolExecutor, as_completed
from module import search_product, url_generator, logger
from config import config

def init_driver_pool(pool_size=4):
    driver_pool = []
    for _ in range(pool_size):
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

        driver_pool.append(driver)

    return driver_pool

def main():
    urls = [url_generator.get_search_url(item["key_word"], item["price_start"], item["price_end"]) for item in config.key_word]

    driver_pool = init_driver_pool(4)

    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {executor.submit(search_product.search_product, url, driver_pool): url for url in urls}

        for future in as_completed(futures):
            url = futures[future]
            try:
                result = future.result()
            except Exception as e:
                new_log = logger.get_logger()
                new_log.error(f"Error processing url {url}: {e}")

    for driver in driver_pool:
        driver.quit()
    driver_pool.clear()

if __name__ == "__main__":
    main()
