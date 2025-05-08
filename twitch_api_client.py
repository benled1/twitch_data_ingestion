from typing import List

class TwitchAPIClient:
    """
    Client to wrap calls that interact with Twitch data. 
    """

    def __init__(self, client_id: str, access_token: str) -> None:
        self.client_id = client_id
        self.access_token = access_token
    
