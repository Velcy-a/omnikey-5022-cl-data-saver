from smartcard.CardMonitoring import CardMonitor, CardObserver
from smartcard.util import toHexString
import json
import datetime
import time
import os

# Standard PC/SC APDU command to get the UID of a contactless card
GET_UID_APDU = [0xFF, 0xCA, 0x00, 0x00, 0x00]

class RFIDObserver(CardObserver):
    def update(self, observable, actions):
        (addedcards, removedcards) = actions
        
        # Trigger when a card enters the reader's field
        for card in addedcards:
            try:
                connection = card.createConnection()
                connection.connect()
                
                # Transmit the APDU command to the card
                data, sw1, sw2 = connection.transmit(GET_UID_APDU)
                
                # sw1 0x90 and sw2 0x00 means the command executed successfully
                if sw1 == 0x90 and sw2 == 0x00:
                    uid_hex = toHexString(data).replace(" ", "")
                    print(f"Card Read Success: UID = {uid_hex}")
                    
                    self.save_to_json(uid_hex)
                else:
                    print(f"Failed to read UID. Status words: {hex(sw1)} {hex(sw2)}")
                    
            except Exception as e:
                print(f"Connection error: {e}")

    def save_to_json(self, uid):
        filename = "rfid_data.json"
        record = {
            "timestamp": datetime.datetime.now().isoformat(),
            "uid": uid
        }
        
        # Load existing data if the file exists and isn't empty
        if os.path.exists(filename):
            try:
                with open(filename, "r") as f:
                    data_list = json.load(f)
            except json.JSONDecodeError:
                # If the file exists but is corrupted/empty, start a new list
                data_list = []
        else:
            data_list = []
            
        # Append the new scan to our list
        data_list.append(record)
        
        # Write the entire list back to the file with nice formatting
        with open(filename, "w") as f:
            json.dump(data_list, f, indent=4)

if __name__ == "__main__":
    print("Initializing OMNIKEY 5022 CL monitoring...")
    
    # Initialize the monitor and attach our observer
    monitor = CardMonitor()
    observer = RFIDObserver()
    monitor.addObserver(observer)
    
    print("Listening for cards... Press Ctrl+C to exit.")
    
    try:
        # Keep the main thread alive while the monitor runs in the background
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down reader...")
    finally:
        monitor.deleteObserver(observer)