"""Unit tests for Flow2Client."""

import pytest
from unittest.mock import AsyncMock, patch
from flow_bt.client import Flow2Client
from flow_bt.exceptions import ConnectionError, NotConnectedError

@pytest.fixture
def client():
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

        with pytest.raises(ConnectionError, match="Could not connect"):
            await client.connect()
