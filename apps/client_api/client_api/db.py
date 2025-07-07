from typing import List
from core.utils.config import MongoConfig, get_mongo_config
from pymongo import MongoClient

class DBClient():
    def __init__(self) -> None:
        self._mongo_config: MongoConfig = get_mongo_config()
        client = MongoClient(self._mongo_config.uri)
        db = client[self._mongo_config.db]
        self._channels_coll = db["channels"]

    def get_channels(self, limit: int) -> List:
        cursor = self._channels_coll.find().sort("_id", -1).limit(limit)
        return list(cursor)
