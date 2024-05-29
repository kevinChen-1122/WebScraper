from urllib.parse import urlparse, urlunparse
from datetime import datetime, timedelta
import re


def is_new_product(string_of_since_at):
    return string_of_since_at and int(parse_relative_time(string_of_since_at)) < 300


def parse_url(url):
    parsed_url = urlparse(url)
    return urlunparse(parsed_url._replace(query=''))


def parse_relative_time(relative_time_str):
    match = re.match(r'(\d+)\s+(\w+)\s+ago$', relative_time_str)
    if match:
        value, unit = int(match.group(1)), match.group(2).lower()
        unit = unit.rstrip('s')
        time_units = {
            'second': 1,
            'minute': 60,
            'hour': 3600,
            'day': 86400,
            'week': 604800,
            'month': 2628000,
            'year': 31536000,
        }
        if unit in time_units:
            return value * time_units[unit]
    return None


def date_format(relative_time_str):
    seconds = parse_relative_time(relative_time_str)
    if not seconds:
        return None
    current_time = datetime.now()
    return (current_time - timedelta(seconds=seconds)).strftime("%Y-%m-%d %H:%M:%S")