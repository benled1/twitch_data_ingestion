import os
import json
import time
import threading
from typing import List
from core.utils import TwitchAPIClient
from .chat_ingestor import ChatIngestor
from .base_ingestor import BaseIngestor

class TwitchMonitor:
    """
    Monitor loop that registers twitch channels for active monitoring.
    Only registered channels have data recorded and ingested. 
    """

    def __init__(self, channel_limit: int=20) -> None:
        self.channel_limit: int = channel_limit
        self.active_channels: List = [] 
        self.active_ingestors: dict[str, dict[str, BaseIngestor]] = {}

        
        self._monitor_interval: int = 30 # seconds
        self._monitor_thread: threading.Thread = None
        self._stop_event = threading.Event()
        self._twitch_client_id: str = os.getenv("TWITCH_CLIENT_ID")
        self._twitch_access_token: str = os.getenv("TWITCH_ACCESS_TOKEN")
        self._api_client: TwitchAPIClient = TwitchAPIClient(client_id=self._twitch_client_id, access_token=self._twitch_access_token )

    def start(self) -> None:
        try: 
            self.monitor_thread: threading.Thread = threading.Thread(target=self._monitor_loop)
            self.monitor_thread.start()
        except Exception as e:
            print(f"Error while starting monitor: {e}")
    
    def stop(self) -> None:
        try:
            self._stop_event.set()
            self._monitor_thread.join()
        except Exception as e:
            print(f"Error while stopping monitor: {e}")

    def _get_top_n_channels(self, limit: int=None) -> List[str]:
        """
        Get the top n channels on twitch measured by active viewers. 
        returns a list of usernames
        """
        streams: dict = self._api_client.get_streams(params={"first": limit})
        return [stream["user_name"] for stream in streams]
            
    def _monitor_loop(self) -> None:
        """
        Main event loop that updates the channels to monitor
        """
        while not self._stop_event.is_set():
            self.active_channels = self._get_top_n_channels(limit=self.channel_limit)
            assert(len(self.active_channels)==self.channel_limit, f"{len(self.active_channels)} != {self.channel_limit}")

            for channel_name in self.active_channels:
                if channel_name not in self.active_ingestors:
                    chat_ingestor: ChatIngestor = ChatIngestor(channel_name=channel_name)
                    chat_ingestor.connect()
                    # do work here to add any other ingestors in the future
                    self.active_ingestors[channel_name] = {"chat": chat_ingestor}

            deletion_list : List = []
            for channel_name in self.active_ingestors:
                if channel_name not in self.active_channels:
                    deletion_list.append(channel_name)
            for channel_name in deletion_list:
                chat_ingestor: ChatIngestor =  self.active_ingestors[channel_name]["chat"]
                chat_ingestor.disconnect()
                # do work here to remove any other ingestors in the future
                self.active_ingestors.pop(channel_name)
            deletion_list = []
            assert(len(self.active_channels)==len(self.active_ingestors))
            print("-----")
            time.sleep(self._monitor_interval)

        deletion_list: List = []
        for channel_name in self.active_ingestors:
            deletion_list.append(channel_name)
        
        for channel_name in deletion_list:
            chat_ingestor: ChatIngestor = self.active_ingestors[channel_name]["chat"]
            chat_ingestor.disconnect()
            self.active_ingestors.pop(channel_name)
        deletion_list = []
        assert(not self.active_ingestors) # check that active channels dict is empty.


