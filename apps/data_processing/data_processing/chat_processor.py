from datetime import datetime
from config import MongoConfig, get_mongo_config
from pymongo import MongoClient


class ChatProcessor:

    def __init__(self, start: datetime, end: datetime) -> None:
        self.start: datetime = start
        self.end: datetime = end
        self._mongo_config: MongoConfig = get_mongo_config()

        client = MongoClient(self._mongo_config.uri)
        db = client[self._mongo_config.db]
        self._coll = db["twitch_chat"]
        pass

    def read_chats(self,) -> None:
        query = {
            "ts": {
                "$gte": self.start,
                "$lte": self.end
            }
        }
        res = self._coll.find(query)
        for doc in res:
            print(doc["channel"], doc["user"], doc["message"], doc["ts"])

