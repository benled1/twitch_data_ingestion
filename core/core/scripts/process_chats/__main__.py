import os
import argparse
import numpy as np
from .chat_processor import ChatProcessor
from core.utils.config import MongoConfig, TwitchConfig, get_mongo_config, get_twitch_config
from core.utils.twitch_api_client import TwitchAPIClient
from datetime import datetime, date, timedelta
from pymongo import MongoClient
from collections import defaultdict
from core.scripts.process_chats.utils import get_channel_chat_map, update_chats
from core.scripts.process_chats.calc_distance import compute_distance__jaccard_similarity
from core.scripts.process_chats.calc_3d_embedding import compute_3d_coords, compute_3d_coords_w_edges

if __name__ == "__main__":
    parser: argparse.ArgumentParser = argparse.ArgumentParser(description="Process pre-ingested twitch data.")
    parser.add_argument("--month", required=True, help="Month in YYYY-MM format")
    parser.add_argument("--similarity-type", required=False, default="jaccard", help="Specify which type of similarity algorithm to use.")
    args = parser.parse_args()
    try:
        parsed_date = datetime.strptime(args.month + "-01", "%Y-%m-%d").date()
    except ValueError:
        print("Invalid format. Use YYYY-MM")
        exit(1)
    
    channel_user_map: defaultdict[str, list[str]] = get_channel_chat_map(month=parsed_date)

    if args.similarity_type == "jaccard":
        distance_func = compute_distance__jaccard_similarity
    else:
        print("Invalid similarity-type. Must be one of jaccard, ")
        exit(1)

    chat_to_coordinate_processor: ChatProcessor = ChatProcessor(channel_user_map=channel_user_map, 
                                                                                        calc_distance_func=distance_func,
                                                                                        calc_3d_embedding_func=compute_3d_coords_w_edges)
    channel_embeddings: dict[str, dict] = chat_to_coordinate_processor.get_channel_embeddings()
    print(f"Channel embeddings: {channel_embeddings}")

    # UPDATE THE update_chats FUNCTION to use the new data return type
    res: int = update_chats(channel_embeddings=channel_embeddings, month=parsed_date)
    exit(res)