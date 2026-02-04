
# Flow 2 BLE Protocol Analysis

## Overview

This document details the reverse-engineered BLE protocol for the Flow 2 air quality monitor, based on trace analysis and live verification.

## Connection Details

- **Device Name:** `FLOW-XX:XX:XX` (e.g., `FLOW-00:43:A6`)
- **Service UUID:** `30390100-4e55-4c10-9dce-b654f35fdf99` (Flow Service)

## Characteristics

| UUID | Description | Properties |
|------|-------------|------------|
| `30390201-4e55-4c10-9dce-b654f35fdf99` | **Authentication** | Write |
| `30390101-4e55-4c10-9dce-b654f35fdf99` | **Command / Control** | Write, Indicate |
| `30390102-4e55-4c10-9dce-b654f35fdf99` | **Data Stream** | Notify |

## Authentication Flow

Before sending commands or receiving data, the client must authenticate.

1. **Connect** to the device.
2. **Write** the 8-byte key to `UUID_AUTH` (`30390201...`).
   - Key: `0xa5 0x97 0x14 0x69 0x30 0xb0 0x13 0x03`

## Commands

### Activation (Live Data)

Enables sensor readings and live data streaming.

- **Char:** `UUID_COMMAND` (`30390101...`)
- **Command:** `0x02`
- **Response (Indication):** `01 02 00 80 10 00 00` (Status OK)

### Fetch History

Triggers the download of stored history data.

- **Char:** `UUID_COMMAND` (`30390101...`)
- **Command:** `01 05 00`
- **Behavior:** Device sends a sequence of large notifications on `UUID_DATA`.

## Data Format

### Live Data Packet (Notify)

- **Size:** 20 bytes
- **Structure:**
  - `Header`: 8 bytes
  - `PM Value`: Float (Little Endian) at offset 8 (`data[8:12]`)
  - `Other`: 8 bytes

### History Data Packet (Notify)

- **Size:** 244 bytes (typically)
- **Structure:**
  - **Header:** 1 byte (packet sequence/type?)
  - **Payload:** Array of records.
- **Record Structure:**
  - **Size:** ~13 bytes (variable padding observed)
  - **Timestamp:** 4 bytes (Little Endian, Unix Epoch) at offset 0.
  - **Data:** ~9 bytes usually following timestamp.
  - **Periodicity:** Records appear every 13 bytes, with occasional 15-byte or larger gaps (suggesting variable length or stuffing).

## Example History Decoding

From trace data:

- **Packet:** `02 f8 86 14 69 ...`
- **Record 0:** `f8 86 14 69` -> TS `1762952952` (2025-11-12 13:09:12)
- **Record 1 (Offset 14):** `08 86 14 69` -> TS `1762952712` (2025-11-12 13:05:12) (Delta -4 mins? Order might be LIFO or FIFO).

## Python Implementation

See `flow2_client.py` for the reference implementation of the connection and fetch sequence.
