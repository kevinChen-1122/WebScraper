from module import logger_module, google_spreadsheets_module, mongo_module
from datetime import datetime
import json
import pymongo


def update_search_product_key_word():
    try:
        response = google_spreadsheets_module.get_key_word()
        json_data = json.loads(response)

        key_word = [dict(zip(['key_word', 'price_start', 'price_end'], sublist))
                    for sublist in {tuple(sublist) for sublist in json_data["values"]} if sublist]

        db = mongo_module.connect_to_mongodb()
        collection = db['key_word']
        data = collection.find_one(sort=[('updated_at', pymongo.DESCENDING)])

        if not data or not data.get('list') or data.get('list') != key_word:
            now = datetime.now()
            timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
            mongo_module.insert_document(collection, {"list": key_word, "updated_at": timestamp})

    except Exception as e:
        new_log = logger_module.get_logger()
        new_log.error(f"Error processing : {e}")


def main():
    try:
        update_search_product_key_word()
    except Exception as e:
        new_log = logger_module.get_logger()
        new_log.error(f"Error processing : {e}")


if __name__ == "__main__":
    main()
