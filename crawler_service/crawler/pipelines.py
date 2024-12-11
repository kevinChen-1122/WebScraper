# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo
from module import search_product_module


class MongoPipeline:
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):

        if search_product_module.is_new_product(item["product_add_since"]):
            notify_data = {
                "item": item,
                "status": "PENDING",
                "created_at": item["created_at"]
            }
            self.db['notify_log'].update_one(
                {"item.product_link": item["product_link"]},
                {"$setOnInsert": notify_data},
                upsert=True
            )

        self.db['search_product'].update_one({"product_link": item["product_link"]}, {"$set": item}, upsert=True)
        return item
