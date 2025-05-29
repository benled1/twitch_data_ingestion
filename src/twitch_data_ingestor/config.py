import os
from dataclasses import dataclass

@dataclass
class TwitchConfig:
    client_id: str
    access_token: str
    username: str

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

