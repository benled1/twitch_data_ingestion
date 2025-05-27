import time
import threading
from .base_ingestor import BaseIngestor


class ChatIngestor(BaseIngestor):

    def __init__(self, channel_name: str):
        self.channel_name: str = channel_name
        self.stop_event: threading.Event = threading.Event()
    
    def connect(self) -> None:
        print(f"Connected to {self.channel_name}'s chat.")

    def disconnect(self) -> None:
        print(f"Diconnected from {self.channel_name}'s chat.")
    
    def ingest(self) -> None:
        while not self.stop_event.is_set():
            print(f"ingesting data from {self.channel_name}...")
            time.sleep(5)