
# Protocol Reverse Engineering Walkthrough

## Goal

Reverse engineer the extended BLE protocol for the Flow 2 device to enable history data extraction.

## Steps Taken

### 1. Device Identification

- Used `scan_all.py` to identify the device.
- **Result:** Device `FLOW-00:43:A6` (`E4:3D:7F:05:7C:FA`) found.
- **Service UUID:** `30390100-4e55-4c10-9dce-b654f35fdf99`.

### 2. Protocol Analysis (CSV Extraction)

- Ran `packet_parser.py` (previous turn) to extract BLE packets from capture.
- **Result:** `flow2_filtered_data.csv` generated.
- **Findings:**
  - **Auth:** `30390401...` access.
  - **Command:** `30390101...` (Write `02` for Activate, `010500` for Fetch).
  - **Data:** `30390102...` (Bulk notifications).

### 3. Verification (Live)

- Created `data_explorer.py` to test the sequence: `Auth -> Subscribe -> Activate -> Fetch`.
- **Result:**
  - Authenticated successfully.
  - Received Indication `01 02 00 80 10 00 00` after sending `02` (Activate).
  - Sent `01 05 00` (Fetch), but received no data (Device likely has empty history).

### 4. Data Decoding (Offline)

- Created `csv_decoder.py` and `analyze_structure.py` to analyze the history packets from the CSV.
- **Result:**
  - Confirmed History Packet format: 244 bytes.
  - Identified Timestamp periodicity of **13 bytes** (mostly).
  - Decoded valid timestamps (e.g., `2025-11-12`) from the raw hex samples.

## Conclusion

The protocol is mapped. Authenticated connection and Activation command `0x02` are confirmed working. The Fetch command `01 05 00` is consistent with traces, though the empty live device yielded no payload. The data structure is a packed array of records (timestamp + measurements).
