import pytest



def test_monitor_loop(twitch_monitor, channel_limit) -> None:
    assert twitch_monitor.channel_limit == channel_limit

