# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
from datetime import datetime

import scrapy


class CrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class ProductItem(scrapy.Item):
    seller_id = scrapy.Field()
    product_link = scrapy.Field()
    product_name = scrapy.Field()
    price = scrapy.Field()
    product_add_at = scrapy.Field()
    product_add_since = scrapy.Field()
    created_at = scrapy.Field()
