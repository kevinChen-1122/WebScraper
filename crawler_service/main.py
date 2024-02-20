from concurrent.futures import ThreadPoolExecutor, as_completed
from module import search_product_module, generator_url_module, logger_module, browser_pool_module


def start_search_product_task():
    urls = generator_url_module.get_search_url()
    driver_pool = browser_pool_module.BrowserPoolModule(pool_size=6)

    with ThreadPoolExecutor(max_workers=6) as executor:
        futures = {executor.submit(search_product_module.search_product, url, driver_pool): url for url in urls}

        for future in as_completed(futures):
            url = futures[future]
            try:
                future.result()
            except Exception as e:
                new_log = logger_module.get_logger()
                new_log.error(f"Error processing url {url}: {e}")

    driver_pool.close_all()


def main():
    try:
        start_search_product_task()
    except Exception as e:
        new_log = logger_module.get_logger()
        new_log.error(f"Error processing : {e}")


if __name__ == "__main__":
    main()
