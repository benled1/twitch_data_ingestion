import re
import socket
import time
import threading
from datetime import datetime
from pymongo import MongoClient
from .base_ingestor import BaseIngestor
from core.utils.config import get_twitch_config, TwitchConfig, get_mongo_config, MongoConfig

class ChatIngestor(BaseIngestor):

    def __init__(self, channel_name: str):
        self._channel_name = channel_name
        self._stop_event = threading.Event()
        self._twitch_config: TwitchConfig = get_twitch_config()
        self._mongo_config: MongoConfig = get_mongo_config()

        client = MongoClient(self._mongo_config.uri)
        db = client[self._mongo_config.db]
        self._coll = db["twitch_chat"]

        self._ingestion_thread: threading.Thread = None

    def connect(self) -> None:
        try:
            self._ingestion_thread = threading.Thread(target=self._ingest, daemon=True)
            self._ingestion_thread.start()
        except Exception as e:
            print(f"Error while connecting chat ingestor for {self._channel_name}: {e}")

    def disconnect(self) -> None:
        try:
            self._stop_event.set()
            self._ingestion_thread.join()
        except Exception as e:
            print(f"Error while stopping monitor: {e}")

    def _ingest(self) -> None:
        server, port = "irc.chat.twitch.tv", 6667
        sock = socket.socket()
        sock.connect((server, port))
        sock.sendall(f"PASS oauth:{self._twitch_config.access_token}\r\n".encode())
        sock.sendall(f"NICK {self._twitch_config.username}\r\n".encode())
        sock.sendall(f"JOIN #{self._channel_name}\r\n".encode())

        msg_pattern = re.compile(
            r"^:(\w+)!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :(.*)$"
        )
        buffer = ""

        while not self._stop_event.is_set():
            try:
                buffer += sock.recv(2048).decode()
            except socket.error:
                time.sleep(1)
                continue

            lines = buffer.split("\r\n")
            buffer = lines.pop()

            for line in lines:
                if line.startswith("PING"):
                    sock.sendall(b"PONG :tmi.twitch.tv\r\n")
                    continue

                m = msg_pattern.match(line)
                if not m:
                    continue

                user, msg = m.groups()
                doc = {
                    "channel": self._channel_name,
                    "user":    user,
                    "message": msg,
                    "ts":       datetime.utcnow()
                }
                try:
                    print(f"Inserting doc: {doc}")
                    # improve perf here by collecting chats and then doing group writes.
                    self._coll.insert_one(doc)
                except Exception as db_err:
                    # you may want better logging or retries here
                    print(f"Mongo insert error: {db_err}")
