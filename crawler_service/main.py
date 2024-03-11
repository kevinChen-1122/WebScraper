from concurrent.futures import ProcessPoolExecutor
from module import search_product_module, generator_url_module, mongo_module
from datetime import datetime


def start_search_product_task():
    urls = generator_url_module.get_search_url()
    if not urls:
        raise Exception("can not get urls")

    with ProcessPoolExecutor(max_workers=6) as executor:
        futures = [executor.submit(search_product_module.search_product, url) for url in urls]

        for future in futures:
            try:
                future.result()
            except Exception as error:
                raise Exception(error)


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
    except Exception as error:
        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] - {error}")


if __name__ == "__main__":
    main()
