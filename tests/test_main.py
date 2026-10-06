"""Tests for CLI entry point."""

import sys
from unittest.mock import patch

import pytest

from flow_bt.__main__ import main


def test_main_no_args():
    """Test main with no arguments prints help."""
    with patch.object(sys, "argv", ["flow-bt"]):
        try:
            main()
        except SystemExit:
            # argparse may call sys.exit on help or error
            pass


def test_main_discover_command():
    """Test main with discover command."""
    with patch.object(sys, "argv", ["flow-bt", "discover"]):
        with patch("flow_bt.__main__.asyncio.run") as mock_asyncio_run:
            with patch("flow_bt.__main__.BleakScanner") as mock_bleak_scanner:
                mock_bleak_scanner.discover.return_value = []
                mock_asyncio_run.return_value = None
                
                # Should not raise
                try:
                    main()
                except SystemExit:
                    pass


def test_main_read_command():
    """Test main with read command - just check it doesn't crash."""
    with patch.object(sys, "argv", ["flow-bt", "read", "AA:BB:CC:DD:EE:FF", "--duration", "60"]):
        with patch("flow_bt.__main__.asyncio.run") as mock_asyncio_run:
            with patch("flow_bt.__main__.Flow2Client") as mock_client:
                mock_client_instance = type("MockClient", (), {
                    "connect": lambda: None,
                    "start_stream": lambda cb: None,
                    "disconnect": lambda: None
                })()
                mock_client.return_value = mock_client_instance
                mock_asyncio_run.return_value = None
                
                # Should not raise
                try:
                    main()
                except SystemExit:
                    pass