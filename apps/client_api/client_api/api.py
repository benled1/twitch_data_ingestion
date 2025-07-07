from fastapi import FastAPI, HTTPException, Query
from typing import List, Annotated
from .models import Channel
from .db import DBClient

app = FastAPI()
db_client: DBClient = DBClient()

@app.get("/channels", response_model=List[Channel])
async def get_channels(limit: Annotated[int, Query(gt=0, le=1000)] = 100) -> List[Channel]:
    try:
        channels = db_client.get_channels(limit=limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to fetch channels")
    return channels