import os
import requests
from typing import List

class TwitchAPIClient:
    """
    Client to wrap calls that interact with Twitch data. 
    """

    def __init__(self, client_id: str, access_token: str) -> None:
        self.client_id = client_id
        self.access_token = access_token
        self._root_url = "https://api.twitch.tv"

    def get_streams(self, params: dict, headers: dict) -> List:
        request_path = os.path.join(self._root_url, "helix/streams")
        response = requests.get(request_path, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        response_data = response.json().get("data", [])
        return response_data

