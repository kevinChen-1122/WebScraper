from concurrent.futures import ThreadPoolExecutor
from module import search_product_module, generator_url_module, mongo_module, browser_pool_module, get_config_module
from datetime import datetime
import cProfile
import io
import pstats


def start_search_product_task():
    driver_pool = []
    try:
        urls = generator_url_module.get_search_url()
        if not urls:
            raise Exception("can not get urls")

        driver_pool = browser_pool_module.BrowserPoolModule(pool_size=get_config_module.browser_pool_size)

        with ThreadPoolExecutor(max_workers=get_config_module.max_workers) as executor:
            futures = [executor.submit(search_product_module.search_product, url, driver_pool) for url in urls]

            for future in futures:
                try:
                    future.result()
                except Exception as error:
                    raise Exception(error)

    finally:
        if driver_pool:
            driver_pool.close_all()


def main():
    try:
        task_start = datetime.now()
        start_timestamp = task_start.strftime("%Y-%m-%d %H:%M:%S")
        # profiler = cProfile.Profile()
        # profiler.enable()
        start_search_product_task()
        # profiler.disable()
        # output_stream = io.StringIO()
        # stats = pstats.Stats(profiler, stream=output_stream).sort_stats('cumulative')
        # stats.print_stats()

        task_end = datetime.now()
        end_timestamp = task_end.strftime("%Y-%m-%d %H:%M:%S")
        task_log = {
            "start": start_timestamp,
            "end": end_timestamp,
            "cost": (task_end - task_start).total_seconds(),
            # "stats": output_stream.getvalue()
        }
        db = mongo_module.connect_to_mongodb()
        mongo_module.insert_document(db['task_log'], task_log)
    except Exception as error:
        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] - {error}")


if __name__ == "__main__":
    main()
