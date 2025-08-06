from sklearn.manifold import MDS, TSNE
import numpy as np
from typing import Optional, Any

def compute_3d_coords(distance_matrix: list[list[float]], channels: list[str]) -> dict[str, dict]:
    mds = MDS(n_components=3, dissimilarity="precomputed", random_state=42)
    coords = mds.fit_transform(distance_matrix)
    channel_positions: dict[str, np.ndarray] = {channels[i]: coords[i] for i in range(len(channels))}
    
    return channel_positions

def compute_3d_coords_w_edges(distance_matrix: list[list[float]], channel_names: list[str]) -> dict[str, dict]:
    similarity = True
    threshold = 0
    D = np.array(distance_matrix)
    n = D.shape[0]
    assert D.shape == (n, n), "distance matrix must be square"
    assert len(channel_names) == n

    mds = MDS(
        n_components=3,
        dissimilarity='precomputed',
        random_state=0
    )
    coords = mds.fit_transform(D)

    nodes = [
        {
            "id": channel_names[i],
            "x": float(coords[i,0]),
            "y": float(coords[i,1]),
            "z": float(coords[i,2])
        }
        for i in range(n)
    ]

    edges = []
    for i in range(n):
        for j in range(i+1, n):
            raw_d = float(D[i,j])
            val = 1 - raw_d if similarity else raw_d
            if threshold is None or val >= threshold:
                curr_embedding = {
                    "source": channel_names[i],
                    "target": channel_names[j],
                    "value": val
                }
                print(f"Appending {curr_embedding}...")
                edges.append(curr_embedding)

    return {"nodes": nodes, "edges": edges}