import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class TwitchConfig:
    client_id: str
    access_token: str
    username: str

@dataclass
class MongoConfig:
    uri: str
    db: str

def _get_twitch_config() -> TwitchConfig: 
    return TwitchConfig(
        client_id=os.getenv("TWITCH_CLIENT_ID"),
        access_token=os.getenv("TWITCH_ACCESS_TOKEN"),
        username=os.getenv("TWITCH_USERNAME")
    )

_twitch_config = None

def get_twitch_config() -> TwitchConfig:
    global _twitch_config
    if _twitch_config is None:
        _twitch_config = _get_twitch_config()
    return _twitch_config

def _get_mongo_config() -> MongoConfig:
    print(os.getenv("MONGO_URI"))
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


