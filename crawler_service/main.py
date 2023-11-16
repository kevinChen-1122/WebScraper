from concurrent.futures import ThreadPoolExecutor, as_completed
from module import search_product, url_generator, logger
from config import config

def main():
    urls = [url_generator.get_search_url(item["key_word"], item["price_start"], item["price_end"]) for item in config.key_word]

    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {executor.submit(search_product.search_product, url): url for url in urls}

        for future in as_completed(futures):
            url = futures[future]
            try:
                result = future.result()
            except Exception as e:
                new_log = logger.get_logger()
                new_log.error(f"Error processing url {url}: {e}")
if __name__ == "__main__":
    main()
