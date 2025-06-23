import numpy as np
from sklearn.manifold import MDS
from collections import defaultdict
from datetime import datetime, date, timedelta
from config import MongoConfig, get_mongo_config
from pymongo import MongoClient


class ChatProcessor:

    def __init__(self, month: date) -> None:
        _month_bounds: tuple[datetime, datetime] = self._get_month_bounds(month)
        self.start: datetime = _month_bounds[0]
        self.end: datetime = _month_bounds[1]
        self._mongo_config: MongoConfig = get_mongo_config()

        client = MongoClient(self._mongo_config.uri)
        db = client[self._mongo_config.db]
        self._coll = db["twitch_chat"]
    

    def compute_coords_jaccard(self) -> None:
        channel_user_map: defaultdict = self._map_channel_users()
        distance_matrix: list[list[float]] = self._compute_jaccard_similarity_distance_matrix(channel_user_map)
        channel_positions: dict[str, np.ndarray] = self._reduce_distance_dimensions(distance_matrix, list(channel_user_map.keys()))
        return channel_positions

    def _get_month_bounds(self, input_date: date) -> tuple[datetime, datetime]:
        start = datetime(input_date.year, input_date.month, 1)

        if input_date.month == 12:
            next_month = datetime(input_date.year + 1, 1, 1)
        else:
            next_month = datetime(input_date.year, input_date.month + 1, 1)

        end = next_month - timedelta(microseconds=1)

        return start, end

    def _map_channel_users(self) -> defaultdict:
        channel_users_map: defaultdict = defaultdict(set)
        query = {
            "ts": {
                "$gte": self.start,
                "$lte": self.end
            }
        }
        try: 
            res = self._coll.find(query)
            for record in res:
                channel = record["channel"]
                user = record["user"]
                channel_users_map[channel].add(user)
                print(f"Mapping {channel} and {user}...")
        except Exception as e:
            print(f"Error while parsing query into channel user mappings: Error: {e}") 

        return channel_users_map
    
    def _compute_jaccard_similarity_distance_matrix(self, channel_user_map: defaultdict) -> list[list[float]]:
        channels = list(channel_user_map.keys())
        n = len(channels)
        similarity_matrix = np.zeros((n, n))

        for i in range(n):
            users_i = channel_user_map[channels[i]]
            for j in range(i + 1, n):
                print(f"Computing similarity between {channels[i]} and {channels[j]}...")
                users_j = channel_user_map[channels[j]]
                intersection = users_i & users_j
                union = users_i | users_j
                jaccard = len(intersection) / len(union) if union else 0.0
                similarity_matrix[i][j] = similarity_matrix[j][i] = jaccard
        distance_matrix = 1 - similarity_matrix
        return distance_matrix

    def _reduce_distance_dimensions(self, distance_matrix: list[list[float]], channels: list[str]) -> dict[str, np.ndarray]:
        print(f"Reducing distance dimensionality...")
        mds = MDS(n_components=3, dissimilarity="precomputed", random_state=42)
        coords = mds.fit_transform(distance_matrix)
        channel_positions = {channels[i]: coords[i] for i in range(len(channels))}

        # script to show test plot
        import matplotlib.pyplot as plt
        from mpl_toolkits.mplot3d import Axes3D

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        xs, ys, zs = coords[:, 0], coords[:, 1], coords[:, 2]
        ax.scatter(xs, ys, zs)

        for i, name in enumerate(channels):
            ax.text(xs[i], ys[i], zs[i], name)

        plt.show()

        print(type(coords[0]))
        return channel_positions
    

