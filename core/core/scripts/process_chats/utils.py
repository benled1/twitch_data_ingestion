import os
import argparse
import numpy as np
from .chat_processor import ChatProcessor
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

def update_chats(channel_embeddings: dict[str, dict], month: date) -> None: 
    _mongo_config: MongoConfig = get_mongo_config()
    _twitch_config: TwitchConfig = get_twitch_config()
    twitch_client: TwitchAPIClient = TwitchAPIClient(_twitch_config.client_id, _twitch_config.access_token) 
    mongo_client = MongoClient(_mongo_config.uri)
    db = mongo_client[_mongo_config.db]
    _node_coll = db["channel_nodes"]
    _edges_coll = db["channel_edges"]
    _channel_metadata_coll = db["channels"]

    for node in channel_embeddings["nodes"]:
        node_channel = node["id"]
        channel_metadata = twitch_client.get_channel_info(params={"login": node_channel})

        node_doc = {
            "channel": node_channel,
            "position": {"x": node["x"], "y": node["y"], "z": node["z"]},
            "month": datetime.combine(month, datetime.min.time()),
            "ts": datetime.utcnow()
        }

        channel_metadata_doc = {
            "channel": node_channel,
            "metadata": channel_metadata
        }

        try:
            print(f"Updating or inserting node info for {node_channel}...")
            node_filter = {"channel": node_channel, "month": datetime.combine(month, datetime.min.time())}
            _node_coll.update_one(node_filter, {"$set": node_doc}, upsert=True)
            print(f"Updating or Inserting channel metadata for {node_channel}...")
            metadata_filter = {"channel": node_channel}
            _channel_metadata_coll.update_one(metadata_filter, {"$set": channel_metadata_doc}, upsert=True)

        except Exception as db_err:
            print(f"Mongo insert error while inserting nodes: {db_err}")
            return 1
    
    for edge in channel_embeddings["edges"]:
        edge_doc = {
            "source_id": edge["source"],
            "target_id": edge["target"],
            "value": edge["value"],
            "month": datetime.combine(month, datetime.min.time()),
            "ts": datetime.utcnow()
        }
        try:
            print(f"Updating or inserting edge info for {edge['source']} --> {edge['target']}...")
            edge_filter = {"source_id": edge["source"], "target_id": edge["target"], "month": datetime.combine(month, datetime.min.time())}
            _edges_coll.update_one(edge_filter, {"$set": edge_doc}, upsert=True)
        except Exception as db_err:
            print(f"Mongo insert error while inserting edges: {db_err}")
            return 1
        
    return 0
