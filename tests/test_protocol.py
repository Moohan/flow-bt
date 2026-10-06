"""Tests for protocol utilities."""

import struct

from flow_bt.protocol import decode_live_pm_value


class TestDecodeLivePMValue:
    """Tests for PM2.5 value decoding from live data packets."""

    def test_valid_pm_value_normal(self):
        """Test decoding a normal PM2.5 value."""
        packet = bytearray(20)
        struct.pack_into("<f", packet, 8, 12.5)
        
        result = decode_live_pm_value(bytes(packet))
        assert result is not None
        assert abs(result - 12.5) < 0.001

    def test_valid_pm_value_zero(self):
        """Test decoding zero PM2.5 value."""
        packet = bytearray(20)
        struct.pack_into("<f", packet, 8, 0.0)
        
        result = decode_live_pm_value(bytes(packet))
        assert result is not None
        assert abs(result - 0.0) < 0.001

    def test_invalid_packet_too_short(self):
        """Test that packets shorter than 20 bytes return None."""
        packet = b"\x00" * 19
        result = decode_live_pm_value(packet)
        assert result is None

    def test_invalid_packet_too_long(self):
        """Test that packets longer than 20 bytes return None."""
        packet = b"\x00" * 21
        result = decode_live_pm_value(packet)
        assert result is None

    def test_invalid_packet_empty(self):
        """Test that empty packets return None."""
        packet = b""
        result = decode_live_pm_value(packet)
        assert result is None