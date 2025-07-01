import os
import argparse
import numpy as np
from .chat_processor import ChatProcessor
from core.utils.config import MongoConfig, TwitchConfig, get_mongo_config, get_twitch_config
from core.utils.twitch_api_client import TwitchAPIClient
from datetime import datetime, date
from pymongo import MongoClient

def _process_chats(month: date) -> dict[str, np.ndarray]:
    chat_proc: ChatProcessor = ChatProcessor(month=month)
    channel_pos: dict[str, np.ndarray] = chat_proc.compute_coords_jaccard()
    return channel_pos

def _update_chats(channel_pos: dict[str, np.ndarray], month: date) -> None: 
    _mongo_config: MongoConfig = get_mongo_config()
    _twitch_config: TwitchConfig = get_twitch_config()
    twitch_client: TwitchAPIClient = TwitchAPIClient(_twitch_config.client_id, _twitch_config.access_token) 
    mongo_client = MongoClient(_mongo_config.uri)
    db = mongo_client[_mongo_config.db]

    # insert coords and update channel metadata
    _coords_coll = db["channel_coords"]
    _channel_metadata_coll = db["channels"]
    for channel in channel_pos:
        # gather data
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

        # update db records
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

if __name__ == "__main__":
    parser: argparse.ArgumentParser = argparse.ArgumentParser(description="Process pre-ingested twitch data.")
    parser.add_argument("--month", required=True, help="Month in YYYY-MM format")
    args = parser.parse_args()
    try:
        parsed_date = datetime.strptime(args.month + "-01", "%Y-%m-%d").date()
    except ValueError:
        print("Invalid format. Use YYYY-MM")
        exit(1)
    channel_pos: dict[str, np.ndarray] = _process_chats(parsed_date)
    res = _update_chats(channel_pos=channel_pos, month=parsed_date)
    exit(res)




