import os
import argparse
import numpy as np
from .chat_to_coordinate_processor import ChatToCoordinateProcessor
from core.utils.config import MongoConfig, TwitchConfig, get_mongo_config, get_twitch_config
from core.utils.twitch_api_client import TwitchAPIClient
from datetime import datetime, date, timedelta
from pymongo import MongoClient
from collections import defaultdict

def get_channel_chat_map(month: date) -> defaultdict[str, list[str]]:

    def _get_month_bounds(input_date: date) -> tuple[datetime, datetime]:
        day: int = 1
        start: datetime = datetime(input_date.year, input_date.month, day)

        if input_date.month == 12:
            next_month: datetime = datetime(input_date.year + 1, 1, day)
        else:
            next_month: datetime = datetime(input_date.year, input_date.month + 1, day)

        end: datetime = next_month - timedelta(microseconds=1)

        return start, end

    _month_bounds: tuple[datetime, datetime] = _get_month_bounds(month)
    _query_start_time: datetime = _month_bounds[0]
    _query_end_time: datetime = _month_bounds[1]
    _channel_user_map: defaultdict[str, list[str]] = {}

    _mongo_config: MongoConfig = get_mongo_config()
    client = MongoClient(_mongo_config.uri)
    db = client[_mongo_config.db]
    _twitch_chat_coll = db["twitch_chat"]
    channel_users_map: defaultdict = defaultdict(set)
    query = {
        "ts": {
            "$gte": _query_start_time,
            "$lte": _query_end_time
        }
    }
    try: 
        res = _twitch_chat_coll.find(query)
        for record in res:
            channel = record["channel"]
            user = record["user"]
            channel_users_map[channel].add(user)
            print(f"Mapping {channel} and {user}...")
    except Exception as e:
        print(f"Error while parsing query into channel user mappings: Error: {e}") 

    return channel_users_map

def update_chats(channel_pos: dict[str, np.ndarray], month: date) -> None: 
    _mongo_config: MongoConfig = get_mongo_config()
    _twitch_config: TwitchConfig = get_twitch_config()
    twitch_client: TwitchAPIClient = TwitchAPIClient(_twitch_config.client_id, _twitch_config.access_token) 
    mongo_client = MongoClient(_mongo_config.uri)
    db = mongo_client[_mongo_config.db]

    _coords_coll = db["channel_coords"]
    _channel_metadata_coll = db["channels"]
    for channel in channel_pos:
        coords_doc = {
            "channel": channel,
            "coords": channel_pos[channel].tolist(),
            "month": datetime.combine(month, datetime.min.time()),
            "ts": datetime.utcnow()
        }

        channel_metadata = twitch_client.get_channel_info(params={"login": channel})
        channel_metadata_doc = {
            "channel": channel,
            "metadata": channel_metadata
        }

        try:
            print(f"Updating or Inserting coords for {channel}...")
            filter = {"channel": channel}
            _coords_coll.update_one(filter, {"$set": coords_doc}, upsert=True)
            print(f"Updating or Inserting channel metadata for {channel}...")
            _channel_metadata_coll.update_one(filter, {"$set": channel_metadata_doc}, upsert=True)

        except Exception as db_err:
            print(f"Mongo insert error: {db_err}")
            return 1
    return 0
