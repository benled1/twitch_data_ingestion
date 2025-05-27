import pytest
from twitch_data_ingestor import TwitchMonitor

@pytest.fixture(params=[1, 10, 50])
def channel_limit(request) -> int:
    return request.param

@pytest.fixture
def running_twitch_monitor(channel_limit) -> TwitchMonitor:
    twitch_monitor: TwitchMonitor = TwitchMonitor(channel_limit=channel_limit)
    twitch_monitor.start()

@pytest.fixture
def twitch_monitor(channel_limit) -> TwitchMonitor:
    return TwitchMonitor(channel_limit=channel_limit)
