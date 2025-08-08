import os
import can  #Requires sudo pip install python-can ...or... sudo apt-get install python3-can
import time
import sys
from datetime import datetime, timedelta

# CAN interface details
INTERFACE_NAME = "can0"
BITRATE = 100000

# Message details
ARBITRATION_ID = 0x123
DATA = [0, 1, 2, 3, 4, 5, 6, 7]

# Loop settings
DELAY = 7  # Delay between messages in seconds
LOOP_DURATION = timedelta(minutes=10)  # Set the loop duration

####################################
def main():
# Set up CAN interface
    try:
        os.system(f"sudo ip link set {INTERFACE_NAME} down")
        os.system(f"sudo ip link set {INTERFACE_NAME} type can bitrate {BITRATE}")
        os.system(f"sudo ip link set {INTERFACE_NAME} txqueuelen 65536")
        os.system(f"sudo ifconfig {INTERFACE_NAME} up")
    except OSError as e:
        raise OSError(f"Error configuring CAN interface: {e}")

    # Assign can0 to the appropriate CAN bus object
    can0 = can.interface.Bus(channel=INTERFACE_NAME, bustype='socketcan')


    # Main loop
    start_time = datetime.now()
    while datetime.now() - start_time < LOOP_DURATION:
        send_message(can0)  # Pass can0 as an argument to send_message
        time.sleep(DELAY)
        print(".", end="", flush=True)
    ########################################
    # Bring down interface and print message
    os.system(f'sudo ifconfig {INTERFACE_NAME} down')
    print(f"Finished sending CAN messages. Loop duration: {(datetime.now() - start_time).t>

def send_message(can_bus):  # Receive can0 as an argument
    try:
        msg = can.Message(arbitration_id=ARBITRATION_ID, data=DATA, is_extended_id=False)
        can_bus.send(msg)  # Use the passed can_bus object
    except can.CanError as e:
        print(f"Error sending message: {e}")
        # Implement a short retry mechanism here if desired

if __name__ == "__main__":
    main()
