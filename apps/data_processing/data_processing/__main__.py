import os
from datetime import datetime
from chat_processor import ChatProcessor
from dotenv import load_dotenv
load_dotenv()

chat_proc = ChatProcessor(start=datetime(2025, 6, 19, 23, 59, 59), end=datetime(2025, 6, 21, 23, 59, 59))
channel_pos = chat_proc.compute_coords_jaccard()
print(channel_pos)



