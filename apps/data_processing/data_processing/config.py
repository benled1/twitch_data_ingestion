import os
from dataclasses import dataclass

@dataclass
class MongoConfig:
    uri: str
    db: str

def _get_mongo_config() -> MongoConfig:
    return MongoConfig(
        uri=os.getenv("MONGO_URI"),
        db=os.getenv("MONGO_DB")
    )

_mongo_config = None

def get_mongo_config() -> MongoConfig:
    global _mongo_config
    if _mongo_config is None:
        _mongo_config = _get_mongo_config()
    return _mongo_config


