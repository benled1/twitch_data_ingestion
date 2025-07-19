import numpy as np
from collections import defaultdict

def compute_distance__jaccard_similarity(channel_user_map: defaultdict[str, list[str]]) -> list[list[float]]:
    def jaccard_similarity(a: set, b: set):
        return len(a & b) / len(a | b) if a | b else 0.0
    channel_user_sets = {channel: set(users) for channel, users in channel_user_map.items()}
    channels: list[str] = list(channel_user_sets.keys())
    n = len(channels)
    distance_matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if i == j:
                distance_matrix[i, j] = 0
            else:
                similarity = jaccard_similarity(channel_user_sets[channels[i]], channel_user_sets[channels[j]])
                distance_matrix[i,j] = 1 - similarity
    return distance_matrix


