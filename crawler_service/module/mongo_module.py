import pymongo
from config import config


def connect_to_mongodb():
    try:
        client = pymongo.MongoClient(config.mongo_host, config.mongo_port, username=config.username,
                                     password=config.password)
        db = client[config.database_name]
        return db
    except pymongo.errors.ConnectionFailure as e:
        print(f"Failed to connect to MongoDB: {e}")
        return None


def insert_document(collection, document):
    try:
        collection.insert_one(document)
        print("Document inserted successfully!")
    except Exception as e:
        print(f"Failed to insert document: {e}")


def insert_documents(collection, documents):
    try:
        collection.insert_many(documents)
        print("Document inserted successfully!")
    except Exception as e:
        print(f"Failed to insert document: {e}")


def find_documents(collection, query=None):
    try:
        if query:
            documents = collection.find(query)
        else:
            documents = collection.find()

        return list(documents)
    except Exception as e:
        print(f"Failed to find documents: {e}")
        return []


def update_document(collection, query, update_data):
    try:
        collection.update_one(query, {"$set": update_data})
        print("Document updated successfully!")
    except Exception as e:
        print(f"Failed to update document: {e}")


def delete_document(collection, query):
    try:
        collection.delete_one(query)
        print("Document deleted successfully!")
    except Exception as e:
        print(f"Failed to delete document: {e}")


def update_documents(collection, query):
    try:
        bulk_operations = [pymongo.UpdateOne({"product_link": doc["product_link"]}, {"$set": doc}, upsert=True) for
                           doc in query]
        collection.bulk_write(bulk_operations)
        print("Document replace successfully!")
    except Exception as e:
        print(f"Failed to replace document: {e}")
