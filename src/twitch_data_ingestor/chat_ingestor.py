from .base_ingestor import BaseIngestor


class ChatIngestor(BaseIngestor):

    def __init__(self, channel_name: str):
        self.channel_name: str = channel_name
        pass
    
    def connect(self):
        print(f"Connected to {self.channel_name}'s chat.")

    def disconnect(self):
        print(f"Diconnected from {self.channel_name}'s chat.")