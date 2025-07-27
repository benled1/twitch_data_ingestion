import numpy as np
from core.utils.config import MongoConfig, get_mongo_config
from sklearn.manifold import MDS, TSNE
from collections import defaultdict
from datetime import datetime, date, timedelta
from pymongo import MongoClient
from typing import Callable



class ChatProcessor:

    def __init__(
        self, 
        channel_user_map: defaultdict[str, list[str]],
        calc_distance_func: Callable[[defaultdict[str, list[str]]], list[list[float]]],
        calc_3d_embedding_func: Callable[[list[list[float]], list[str]], dict[str, np.ndarray]],
    ) -> None:
        self._channel_user_map: defaultdict[str, list[str]] = channel_user_map
        self._get_channel_distance = calc_distance_func
        self._cluster_channels_3d = calc_3d_embedding_func


    def get_channel_coordinates(self) -> dict[str, np.ndarray]:
        distance_matrix: list[list[float]] = self._get_channel_distance(self._channel_user_map)
        channel_positions: dict[str, np.ndarray] = self._cluster_channels_3d(distance_matrix, list(self._channel_user_map.keys()))
        return channel_positions

    def get_channel_connected_graph(self) -> None:
        pass
    