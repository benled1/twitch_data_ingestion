# Try different similarity and clustering combinations
## TODO before testing
- Develop a way of testing clustering and distance algorithms that is quick and conclusive
  - Develop a quick way of swapping between different clustering and distance algorithms
    - Isolate distance calc, clustering from ChatProcessor and inject as dependencies
  - Develop a metric or standard for testing how good a set of algorithms is


## Similarity Measures:
- Jaccard
- Overlap Coefficient (Simpson's Coefficient)
- 

## Clustering/Dimensionality Reduction
- MDS 
- TSNE
- Sammon mapping


# BUGS
## Sev-1 
- many missing channels from the visualization.
  - ex. Ludwig is in the channel coords for month of July but is not in the final visualization.
  - this could be a prob with either the client api or the frontend.




https://chatgpt.com/share/68787660-6ad4-800f-a158-55d22c375565
# Developer Guide

1. Create a .env from the template in the root of the project

2. Run using docker compose
```
docker compose -f compose.dev.yaml up --build -d
```
