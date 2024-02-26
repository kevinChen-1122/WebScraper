from concurrent.futures import ThreadPoolExecutor, as_completed
from module import search_product_module, generator_url_module, logger_module, browser_pool_module, mongo_module
from datetime import datetime


def start_search_product_task():
    urls = generator_url_module.get_search_url()

    if not urls:
        raise Exception(f"{__name__}/{start_search_product_task().__name__}: can not get urls")

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
        task_start = datetime.now()
        start_timestamp = task_start.strftime("%Y-%m-%d %H:%M:%S")
        db = mongo_module.connect_to_mongodb()

        start_search_product_task()

        task_end = datetime.now()
        end_timestamp = task_end.strftime("%Y-%m-%d %H:%M:%S")
        mongo_module.insert_document(
            db['task_log'],
            {"start": start_timestamp, "end": end_timestamp, "cost": (task_end - task_start).total_seconds()}
        )
    except Exception as e:
        new_log = logger_module.get_logger()
        new_log.error(f"Error processing : {e}")


if __name__ == "__main__":
    main()
