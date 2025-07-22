from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Annotated, Any
from .models import Channel, ChannelCoordinates
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