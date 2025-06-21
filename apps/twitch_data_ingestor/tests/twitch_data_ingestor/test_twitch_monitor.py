import threading
import pytest
import time
from unittest.mock import patch, MagicMock

@patch("twitch_data_ingestor.twitch_monitor.TwitchMonitor._get_top_n_channels")
@patch("twitch_data_ingestor.chat_ingestor.ChatIngestor.connect")
@patch("twitch_data_ingestor.chat_ingestor.ChatIngestor.disconnect")
def test_monitor_loop(mock_chat_ingestor_disconnect, mock_chat_ingestor_connect, mock_get_top_n_channels, twitch_monitor, channel_limit) -> None:
    assert twitch_monitor.channel_limit == channel_limit
    mock_get_top_n_channels.return_value = [f"channel_{n}" for n in range(channel_limit)]

    twitch_monitor.start()
    twitch_monitor.stop()
    time.sleep(1)
    assert(len(twitch_monitor.active_channels)==channel_limit)
    assert(mock_chat_ingestor_connect.call_count==channel_limit)
    twitch_monitor.monitor_thread.join()

