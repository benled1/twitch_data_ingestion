from pymongo import MongoClient
from core.utils.config import get_mongo_config, MongoConfig



if __name__ == "__main__":
    if input("This will delete all coordinate records in the database. Are you sure you want to do this? y/n") == "y":
        config: MongoConfig = get_mongo_config()
        client = MongoClient(config.uri)
        db = client[config.db]
        collection = db["channel_coords"]

        collection.delete_many({})
        print("Deleted all coordinates")
    else:
        print("Aborted")
