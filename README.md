# Giss Print Agent

A standalone client-side middleware to enable silent printing from web applications to local Windows printers.

## Overview

This tool runs a lightweight Flask server on a Windows client machine. It accepts print requests (Base64 encoded PDFs) via a REST API and uses **SumatraPDF** to perform silent, background printing.

## Prerequisites

1.  **Windows OS**: Required for `pywin32` and `SumatraPDF.exe`.
2.  **SumatraPDF**: Download the portable version of `SumatraPDF.exe` and place it in the project root (during development) or in the same folder as the final `.exe`.
3.  **Python 3.x**: Required for development and building.

## Project Structure

- `src/main.py`: Flask server entry point.
- `requirements.txt`: Python dependencies.
- `build.bat`: Windows batch script to build the standalone executable.
- `README.md`: This documentation.

## Setup & Development

1.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
2.  Place `SumatraPDF.exe` in the root directory.
3.  Run the server:
    ```bash
    python src/main.py
    ```
    The server listens on `http://127.0.0.1:5000`.

## Building the Executable

To generate a standalone Windows executable:

1.  Run the build script:
    ```batch
    build.bat
    ```
2.  The output `GissPrintAgent.exe` will be in the `dist/` folder.

## Distribution

When distributing to end-users, ensure they have:
1.  `GissPrintAgent.exe`
2.  `SumatraPDF.exe` (must be in the same folder as the agent)

## API Reference

### 1. List Printers
- **Endpoint**: `GET /printers`
- **Description**: Returns a JSON list of all installed printer names.

### 2. Print Document
- **Endpoint**: `POST /print`
- **Payload**:
    ```json
    {
        "printer_name": "HP_LaserJet_Pro",
        "pdf_data": "JVBERi0xLjQKJ..."
    }
    ```
- **Description**: Decodes the Base64 PDF and sends it to the specified printer silently.
