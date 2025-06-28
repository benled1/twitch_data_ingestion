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
        self.headers = {
            "Client-ID": self.client_id,
            "Authorization": f"Bearer {self.access_token}",
        }

    def get_streams(self, params: dict={}) -> List:
        request_path = os.path.join(self._root_url, "helix/streams")
        response = requests.get(request_path, headers=self.headers, params=params, timeout=10)
        response.raise_for_status()
        response = response.json().get("data", [])
        return response

    def get_channel_info(self, params: dict={}) -> List:
        request_path = os.path.join(self._root_url, "helix/users")
        response = requests.get(request_path, headers=self.headers, params=params, timeout=10)
        response.raise_for_status()
        return response.json()

