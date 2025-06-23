import os
from datetime import datetime, date
from chat_processor import ChatProcessor
from dotenv import load_dotenv
from config import MongoConfig, get_mongo_config
from pymongo import MongoClient
load_dotenv()

month = date(2025, 6, 1)
chat_proc = ChatProcessor(month=month)
channel_pos = chat_proc.compute_coords_jaccard()

_mongo_config: MongoConfig = get_mongo_config()
client = MongoClient(_mongo_config.uri)
db = client[_mongo_config.db]
_coll = db["channel_coords"]
for channel in channel_pos:
    doc = {
        "channel": channel,
        "coords": channel_pos[channel].tolist(),
        "month": datetime.combine(month, datetime.min.time()),
        "ts": datetime.utcnow()
    }
    try:
        print(f"Inserting channel coords for {channel}...")
        _coll.insert_one(doc)
    except Exception as db_err:
        print(f"Mongo insert error: {db_err}")



