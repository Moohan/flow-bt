# Flow BT - Flow 2 BLE Client Library

A Python client library for interacting with Flow 2 air quality monitors via Bluetooth Low Energy (BLE).

## Installation

```bash
pip install flow-bt
```

## Usage

```python
import asyncio
from flow_bt import Flow2Client

async def main():
    client = Flow2Client("E4:3D:7F:05:7C:FA")  # Your device MAC
    
    def on_data(msg_type, payload):
        if msg_type == "live":
            print(f"PM2.5: {payload:.2f} µg/m³")
    
    await client.connect()
    await client.start_stream(on_data)
    await asyncio.sleep(10)  # Stream for 10 seconds
    await client.disconnect()

asyncio.run(main())
```

## CLI

```bash
# Discover nearby devices
flow-bt discover

# Stream live data from a specific device
flow-bt read E4:3D:7F:05:7C:FA --duration 60
```

## License

MIT License