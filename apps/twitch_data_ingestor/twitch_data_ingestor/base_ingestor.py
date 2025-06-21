from abc import ABC, abstractmethod


class BaseIngestor(ABC):

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass

    @abstractmethod
    def _ingest(self):
        pass