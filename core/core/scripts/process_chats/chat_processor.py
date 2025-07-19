import numpy as np
from core.utils.config import MongoConfig, get_mongo_config
from sklearn.manifold import MDS, TSNE
from collections import defaultdict
from datetime import datetime, date, timedelta
from pymongo import MongoClient


class ChatProcessor:

    def __init__(self, month: date) -> None:
        _month_bounds: tuple[datetime, datetime] = self._get_month_bounds(month)

        self._query_start_time: datetime = _month_bounds[0]
        self._query_end_time: datetime = _month_bounds[1]
        self._channel_user_map: defaultdict[str, list[str]] = {}

        self._mongo_config: MongoConfig = get_mongo_config()
        client = MongoClient(self._mongo_config.uri)
        db = client[self._mongo_config.db]
        self._twitch_chat_coll = db["twitch_chat"]

    def compute_coords_jaccard(self) -> dict[str, np.ndarray]:
        channel_user_map: defaultdict[str, list[str]] = self._map_channel_users()
        distance_matrix: list[list[float]] = self._compute_jaccard_similarity_distance_matrix(channel_user_map)
        channel_positions: dict[str, np.ndarray] = self._reduce_distance_dimensions_tsne(distance_matrix, list(channel_user_map.keys()))
        return channel_positions

    def _get_month_bounds(self, input_date: date) -> tuple[datetime, datetime]:
        day: int = 1
        start: datetime = datetime(input_date.year, input_date.month, day)

        if input_date.month == 12:
            next_month: datetime = datetime(input_date.year + 1, 1, day)
        else:
            next_month: datetime = datetime(input_date.year, input_date.month + 1, day)

        end: datetime = next_month - timedelta(microseconds=1)

        return start, end

    def _map_channel_users(self) -> defaultdict:
        channel_users_map: defaultdict = defaultdict(set)
        query = {
            "ts": {
                "$gte": self._query_start_time,
                "$lte": self._query_end_time
            }
        }
        try: 
            res = self._twitch_chat_coll.find(query)
            for record in res:
                channel = record["channel"]
                user = record["user"]
                channel_users_map[channel].add(user)
                print(f"Mapping {channel} and {user}...")
        except Exception as e:
            print(f"Error while parsing query into channel user mappings: Error: {e}") 

        return channel_users_map
    
    
    def _compute_jaccard_similarity_distance_matrix(self, channel_user_map: defaultdict[str, list[str]]) -> list[list[float]]:
        channels_list: list[str] = list(channel_user_map.keys())
        n = len(channels_list)
        similarity_matrix = np.zeros((n, n))

        for i in range(n):
            channel_i_users: list[str] = channel_user_map[channels_list[i]]
            for j in range(i + 1, n):
                print(f"Computing similarity between {channels_list[i]} and {channels_list[j]}...")
                channel_j_users: list[str] = channel_user_map[channels_list[j]]
                intersection = channel_i_users & channel_j_users
                union = channel_i_users | channel_j_users
                jaccard = len(intersection) / len(union) if union else 0.0
                similarity_matrix[i][j] = similarity_matrix[j][i] = jaccard
        distance_matrix = 1 - similarity_matrix
        return distance_matrix

    def _reduce_distance_dimensions_mds(self, distance_matrix: list[list[float]], channels: list[str]) -> dict[str, np.ndarray]:
        print(f"Reducing distance dimensionality...")
        mds = MDS(n_components=3, dissimilarity="precomputed", random_state=42)
        coords = mds.fit_transform(distance_matrix)
        channel_positions = {channels[i]: coords[i] for i in range(len(channels))}
        return channel_positions

    def _reduce_distance_dimensions_tsne(self, distance_matrix: list[list[float]], channels: list[str]) -> dict[str, np.ndarray]:
        print(f"Reducing distance dimensionality...")
        tsne = TSNE(n_components=3, metric="precomputed", random_state=42, early_exaggeration=100)
        coords = tsne.fit_transform(distance_matrix)
        channel_positions = {channels[i]: coords[i] for i in range(len(channels))}
        return channel_positions