import numpy as np
from core.utils.config import MongoConfig, get_mongo_config
from sklearn.manifold import MDS, TSNE
from collections import defaultdict
from datetime import datetime, date, timedelta
from pymongo import MongoClient
from typing import Callable
from pydantic import BaseModel

class ChatProcessor:

    def __init__(
        self, 
        channel_user_map: defaultdict[str, list[str]],
        calc_distance_func: Callable[[defaultdict[str, list[str]]], list[list[float]]],
        calc_3d_embedding_func: Callable[[list[list[float]], list[str]], dict[str, np.ndarray]],
    ) -> None:
        self._channel_user_map: defaultdict[str, list[str]] = channel_user_map
        self._calc_distance_func = calc_distance_func
        self._calc_3d_embedding_func = calc_3d_embedding_func


    def get_channel_embeddings(self) -> dict[str, dict]:
        distance_matrix: list[list[float]] = self._calc_distance_func(self._channel_user_map)
        channel_embeddings: dict[str, dict] = self._calc_3d_embedding_func(distance_matrix, list(self._channel_user_map.keys()))
        return channel_embeddings

    