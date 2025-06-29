import argparse
from core.chat_ingestion import TwitchMonitor
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    parser: argparse.ArgumentParser = argparse.ArgumentParser(description="Run an ingestor service to collect external data.")

    parser.add_argument("--channel_limit", required=True, help="Max number of channels to collect chats from at once. (int)")
    args = parser.parse_args()

    # run twitch chat ingestion
    twitch_monitor = TwitchMonitor(channel_limit=args.channel_limit)
    twitch_monitor.start()