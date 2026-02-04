# Flow BT

A Python client library for interacting with Flow 2 air quality monitors via Bluetooth Low Energy (BLE).

## Features

- **Async/await API** using `asyncio` and `bleak`
- **Live data streaming** - Real-time PM2.5 readings
- **Historical data fetch** - Retrieve stored sensor measurements
- **Type hints** - Full type annotations for better IDE support
- **Well documented** - Comprehensive docstrings and examples
- **CLI Tool** - Built-in command line interface for discovery and quick testing

## Installation

```bash
pip install flow-bt
```

## Quick Start

```python
import asyncio
from flow_bt import Flow2Client

async def main():
    client = Flow2Client("YOUR_DEVICE_ADDRESS")

    def on_data(msg_type, payload):
        if msg_type == "live":
            print(f"PM2.5: {payload:.2f} µg/m³")

    await client.connect()
    await client.start_stream(on_data)
    await asyncio.sleep(10)
    await client.disconnect()

asyncio.run(main())
```

See [Examples](https://github.com/moohan/flow-bt/tree/main/examples) for more details.
