from sklearn.manifold import MDS, TSNE
import numpy as np

def _reduce_distance_dimensions_mds(distance_matrix: list[list[float]], channels: list[str]) -> dict[str, np.ndarray]:
    mds = MDS(n_components=3, dissimilarity="precomputed", random_state=42)
    coords = mds.fit_transform(distance_matrix)
    channel_positions: dict[str, np.ndarray] = {channels[i]: coords[i] for i in range(len(channels))}
    return channel_positions