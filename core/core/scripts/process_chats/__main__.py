import os
import argparse
import numpy as np
from .chat_to_coordinate_processor import ChatToCoordinateProcessor
from core.utils.config import MongoConfig, TwitchConfig, get_mongo_config, get_twitch_config
from core.utils.twitch_api_client import TwitchAPIClient
from datetime import datetime, date, timedelta
from pymongo import MongoClient
from collections import defaultdict
from core.scripts.process_chats.utils import get_channel_chat_map, update_chats

if __name__ == "__main__":
    parser: argparse.ArgumentParser = argparse.ArgumentParser(description="Process pre-ingested twitch data.")
    parser.add_argument("--month", required=True, help="Month in YYYY-MM format")
    args = parser.parse_args()
    try:
        parsed_date = datetime.strptime(args.month + "-01", "%Y-%m-%d").date()
    except ValueError:
        print("Invalid format. Use YYYY-MM")
        exit(1)
    
    channel_user_map: defaultdict[str, list[str]] = get_channel_chat_map(month=parsed_date)
    chat_to_coordinate_processor: ChatToCoordinateProcessor = ChatToCoordinateProcessor(channel_user_map=channel_user_map, )
    channel_pos: dict[str, np.ndarray] = chat_to_coordinate_processor.get_channel_coordinates()
    res: int = update_chats(channel_pos=channel_pos, month=parsed_date)
    exit(res)




