import pymongo

from . import get_config_module, mongo_module
from urllib.parse import urlencode


def generate_search_url(key_word, price_start, price_end):
    get_config_module.query_params["price_start"] = price_start
    get_config_module.query_params["price_end"] = price_end
    return f"{get_config_module.carousell_url}/search/{key_word}?{urlencode(get_config_module.query_params)}"


def get_search_url():
    db = mongo_module.connect_to_mongodb()
    collection = db['key_word']
    data = collection.find_one(sort=[('updated_at', pymongo.DESCENDING)])

    if not data or not data.get('list'):
        return []

    return [generate_search_url(item["key_word"], item["price_start"], item["price_end"]) for item in
            data.get('list')]
