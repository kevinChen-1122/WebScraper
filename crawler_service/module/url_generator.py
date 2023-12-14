from config import config
from urllib.parse import urlencode


def get_search_url(key_word, price_start, price_end):
    config.query_params["price_start"] = price_start
    config.query_params["price_end"] = price_end
    return f"{config.carousell_url}/search/{key_word}?{urlencode(config.query_params)}"
