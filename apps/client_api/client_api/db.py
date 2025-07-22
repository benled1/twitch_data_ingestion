from typing import List
from .models import Channel, ChannelCoordinates
from core.utils.config import MongoConfig, get_mongo_config
from pymongo import MongoClient
from datetime import datetime, timezone

class DBClient():
    def __init__(self) -> None:
        self._mongo_config: MongoConfig = get_mongo_config()
        client = MongoClient(self._mongo_config.uri)
        db = client[self._mongo_config.db]
        self._channels_coll = db["channels"]
        self._coordinates_coll = db["channel_coords"]

    def get_channels(self, limit: int) -> List[Channel]:
        cursor = self._channels_coll.find().sort("_id", -1).limit(limit)
        return list(cursor)
    
    def get_coordinates(self, channel_name: str, month: str) -> List[ChannelCoordinates]:
        target_month=""
        try:
            target_month = datetime.strptime(month, "%Y-%m").replace(tzinfo=timezone.utc)
        except ValueError as e:
            raise ValueError(f"Invalid month format '{month}'. Expected 'YYYY-MM'.") from e
        cursor = self._coordinates_coll.find({
            "channel": {"$eq": channel_name},
            "month": {"$eq": target_month}            
            })
        return list(cursor)
