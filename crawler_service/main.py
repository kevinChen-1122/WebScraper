import time
import schedule
from concurrent.futures import ThreadPoolExecutor, as_completed
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from module import search_product_module, generator_url_module, logger_module


def initialize_browser_pool(pool_size=2):
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
        user_agent = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 9_13_2) AppleWebKit/613.1.89 (KHTML, like Gecko) "
                      "Version/10.1.4 Safari/611.2.4")
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


def start_search_product_task():
    urls = generator_url_module.get_search_url()
    driver_pool = initialize_browser_pool(6)

    with ThreadPoolExecutor(max_workers=6) as executor:
        futures = {executor.submit(search_product_module.search_product, url, driver_pool): url for url in urls}

        for future in as_completed(futures):
            url = futures[future]
            try:
                future.result()
            except Exception as e:
                new_log = logger_module.get_logger()
                new_log.error(f"Error processing url {url}: {e}")

    for driver in driver_pool:
        driver.quit()
    driver_pool.clear()


# 任務調度
def schedule_tasks():
    schedule.every(5).minutes.do(start_search_product_task)


def main():
    try:
        schedule_tasks()

        while True:
            schedule.run_pending()
            time.sleep(1)
    except Exception as e:
        new_log = logger_module.get_logger()
        new_log.error(f"Error processing : {e}")


if __name__ == "__main__":
    main()
