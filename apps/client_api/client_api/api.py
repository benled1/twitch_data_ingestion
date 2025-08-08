from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Annotated, Any
from .models import Channel, ChannelCoordinates, ChannelNode, ChannelEdge
from .db import DBClient

app = FastAPI()
db_client: DBClient = DBClient()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/channels", response_model=List[Channel])
async def get_channels(limit: Annotated[int, Query(gt=0, le=1000)] = 100) -> List[Channel]:
    try:
        channels = db_client.get_channels(limit=limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to fetch channels")
    return channels

@app.get("/coordinates", response_model=List[ChannelCoordinates])
async def get_coordinates(channel_name: str, month: str) -> List[ChannelCoordinates]:
    try:
        coordinates = db_client.get_coordinates(channel_name=channel_name, month=month)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch channels with exception: {e}")
    print(f"The reponse = {coordinates}")
    return coordinates

@app.get("/channel_node", response_model=ChannelNode)
async def get_channel_node(channel_name: str, month: str) -> ChannelNode:
    try:
        node = db_client.get_nodes(channel_name=channel_name, month=month)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch channels with exception: {e}")
    return node


@app.get("/channel_edges", response_model=List[ChannelEdge])
async def get_channel_edges(channel_name: str, month: str) -> List[ChannelEdge]:
    print(f"channel name = {channel_name}")
    print(f"month = {month}")
    try:
        edges = db_client.get_source_edges(channel_name=channel_name, month=month)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch channels with exception: {e}")
    print(f"The reponse = {edges}")
    return edges