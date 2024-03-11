from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
import multiprocessing
import random


class BrowserPoolModule:
    def __init__(self, pool_size=2):
        self.pool_size = pool_size
        self.manager = multiprocessing.Manager()
        self.pool = self.manager.list()
        self._initialize()

    def _initialize(self):
        for _ in range(self.pool_size):
            driver = self._create_driver()
            self.pool.append(driver)

    @staticmethod
    def _create_driver():
        options = Options()
        options.binary_location = "/usr/bin/chromium"

        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-blink-features")
        options.add_argument("--disable-blink-features=AutomationControlled")

        options.add_experimental_option('useAutomationExtension', False)
        user_agent = (f"Mozilla/5.0 (Macintosh; Intel Mac OS X 9_13_{random.randrange(10)}) "
                      f"AppleWebKit/613.{random.randrange(20)}.89 (KHTML, like Gecko) "
                      f"Version/10.{random.randrange(10)}.{random.randrange(10)}"
                      f"Safari/611.{random.randrange(10)}.{random.randrange(10)}")
        options.add_argument('--user-agent=%s' % user_agent)
        options.add_experimental_option("excludeSwitches", ['enable-automation'])

        s = Service("/usr/bin/chromedriver")
        driver = webdriver.Chrome(service=s, options=options)
        return driver

    def get_driver(self):
        if self.pool:
            return self.pool.pop(0)
        else:
            raise Exception("Browser pool is empty")

    def release_driver(self, driver):
        self.pool.append(driver)

    def close_all(self):
        for driver in self.pool:
            driver.quit()
        self.pool.clear()
