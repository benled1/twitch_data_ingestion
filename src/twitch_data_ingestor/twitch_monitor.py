import os
import json
import time
import threading
from typing import List
from .twitch_api_client import TwitchAPIClient
from .chat_ingestor import ChatIngestor
from .base_ingestor import BaseIngestor
from dotenv import load_dotenv

load_dotenv()

class TwitchMonitor:
    """
    Monitor loop that registers twitch channels for active monitoring.
    Only registered channels have data recorded and ingested. 
    """

    def __init__(self, channel_limit: int=20):
        self.channel_limit: int = channel_limit
        self.active_channels: List = [] 
        self.active_ingestors: dict[str, dict[str, BaseIngestor]] = {}


        self._monitor_thread: threading.Thread = None
        self._stop_event = threading.Event()
        self._twitch_client_id: str = os.getenv("TWITCH_CLIENT_ID")
        self._twitch_access_token: str = os.getenv("TWITCH_ACCESS_TOKEN")
        self._api_client: TwitchAPIClient = TwitchAPIClient(client_id=self._twitch_client_id, access_token=self._twitch_access_token )

    def start(self) -> None:
        self.monitor_thread: threading.Thread = threading.Thread(target=self._monitor_loop)
        self.monitor_thread.start()
    
    def stop(self) -> None:
        self._stop_event.set()
        self._monitor_thread.join()

    def _get_top_n_channels(self, limit: int=None) -> List[str]:
        """
        Get the top n channels on twitch measured by active viewers. 
        returns a list of usernames
        """
        streams: dict = self._api_client.get_streams()
        return [stream["user_name"] for stream in streams]
            
    def _monitor_loop(self):
        """
        Main event loop that updates the channels to monitor
        """
        while self.active:
            self.active_channels = self._get_top_n_channels(limit=self.channel_limit)

            for channel_name in self.active_channels:
                if channel_name not in self.active_ingestors:
                    chat_ingestor: ChatIngestor = ChatIngestor(channel_name=channel_name)
                    chat_ingestor.connect()
                    # do work here to add any other ingestors in the future
                    self.active_ingestors[channel_name]["chat"] = [chat_ingestor]
            
            for channel_name in self.active_ingestors:
                if channel_name not in self.active_channels:
                    chat_ingestor: ChatIngestor =  self.active_ingestors[channel_name]["chat"]
                    chat_ingestor.disconnect()
                    # do work here to remove any other ingestors in the future
                    self.active_ingestors.pop(channel_name)
            time.sleep(5)


