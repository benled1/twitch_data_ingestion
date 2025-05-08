from typing import List

class TwitchMonitor:
    """
    Monitor loop that registers twitch channels for active monitoring.
    Only registered channels have data recorded and ingested. 
    """

    def __init__(self):
        self.active_channels: List = []
        self.active: bool = False 

    def get_top_n_channels(self, limit: int) -> List[str]:
        """
        Get the top n channels on twitch measured by active viewers.
        """
        pass

    def monitor_loop(self):
        """
        Main event loop that updates the channels to monitor
        """
        while self.active:
            # create a TwitchAPIClient class which will handle all the calls to twitch
            pass

        pass
