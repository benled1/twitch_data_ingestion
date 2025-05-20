from .twitch_monitor import TwitchMonitor

if __name__ == "__main__":
    print("Running the Twitch Monitor")
    monitor = TwitchMonitor(channel_limit=20)
    monitor.monitor_loop()