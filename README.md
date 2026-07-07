# OMNIKEY 5022 JSON Logger
This repository contains a base Python script that interfaces with an HID OMNIKEY 5022 CL smartcard reader. It uses PC/SC to listen for RFID/NFC tags and automatically logs the detected UIDs into a structured JSON file

## Requirements & Dependencies

To run this script, you need **Python 3.x** and the following dependencies:

### 1. Python Libraries
* **[pyscard](https://pyscard.sourceforge.io/)** (Python smart card library) - Used to interface with PC/SC compliant readers.

You can install it via pip:
pip install pyscard

### 2. Linux Dependencies
* **You'll need pcscd & libpcsclite-dev installed.

Example:
* sudo apt install pcscd libpcsclite-dev

Then you need to enable the service pcscd service itself:

* sudo systemctl enable --now pcscd

### 3. Windows Dependencies

* **If you are installing pyscard on Windows, pip may need to compile it from source. To do this, you need a C++ compiler.

* You'll need Visual Studio Build Tools
  
[Download Microsoft C++ Build Tools here](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
