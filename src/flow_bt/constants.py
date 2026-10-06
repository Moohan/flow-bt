"""Protocol constants for Flow 2 BLE communication."""

from typing import Final

# Characteristic UUIDs
UUID_AUTH: Final[str] = "30390201-4E55-4C10-9DCE-B654F35FDF99"
UUID_COMMAND: Final[str] = "30390101-4E55-4C10-9DCE-B654F35FDF99"
UUID_DATA: Final[str] = "30390102-4E55-4C10-9DCE-B654F35FDF99"
UUID_BATTERY: Final[str] = "00002a19-0000-1000-8000-00805f9b34fb"

# Authentication
AUTH_KEY: Final[bytes] = bytes([0xA5, 0x97, 0x14, 0x69, 0x30, 0xB0, 0x13, 0x03])

# Commands
CMD_ACTIVATE: Final[bytes] = bytes([0x02])
CMD_FETCH_HISTORY: Final[bytes] = bytes.fromhex("010500")

# Packet sizes
LIVE_DATA_PACKET_SIZE: Final[int] = 20