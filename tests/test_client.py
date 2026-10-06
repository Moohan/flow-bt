"""Tests for Flow2Client."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from flow_bt.client import Flow2Client
from flow_bt.exceptions import Flow2ConnectionError, NotConnectedError


@pytest.fixture
def client():
    """Create a Flow2Client instance for testing."""
    return Flow2Client("CC:BB:AA:EE:22:11")


def test_client_init(client):
    """Test client initialization."""
    assert client.address == "CC:BB:AA:EE:22:11"
    assert client.client is None
    assert client.is_streaming is False


@pytest.mark.asyncio
async def test_read_battery_not_connected(client):
    """Test read_battery raises NotConnectedError when not connected."""
    with pytest.raises(NotConnectedError):
        await client.read_battery()


@pytest.mark.asyncio
async def test_start_stream_not_connected(client):
    """Test start_stream raises NotConnectedError when not connected."""
    with pytest.raises(NotConnectedError):
        await client.start_stream(lambda m, p: None)


@pytest.mark.asyncio
async def test_fetch_history_not_connected(client):
    """Test fetch_history raises NotConnectedError when not connected."""
    with pytest.raises(NotConnectedError):
        await client.fetch_history()


@pytest.mark.asyncio
async def test_connect_failure(client):
    """Test connect raises ConnectionError on failure."""
    with patch("flow_bt.client.BleakClient") as mock_bleak:
        mock_instance = AsyncMock()
        mock_bleak.return_value = mock_instance
        mock_instance.connect.side_effect = Exception("Bluetooth down")

        with pytest.raises(Flow2ConnectionError, match="Could not connect"):
            await client.connect()


@pytest.mark.asyncio
async def test_stop_stream_when_not_streaming(client):
    """Test stop_stream does nothing when not streaming."""
    # Should not raise any exception
    await client.stop_stream()


@pytest.mark.asyncio
async def test_disconnect_when_not_connected(client):
    """Test disconnect handles case when not connected."""
    # Should not raise any exception
    await client.disconnect()