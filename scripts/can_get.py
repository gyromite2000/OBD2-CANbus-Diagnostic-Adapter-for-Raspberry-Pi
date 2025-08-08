import can
import os

# CAN interface details
INTERFACE_NAME = "can0"
BITRATE = 100000

def setup_can_interface():
    try:
        os.system(f"sudo ip link set {INTERFACE_NAME} down")
        os.system(f"sudo ip link set {INTERFACE_NAME} type can bitrate {BITRATE}")
        os.system(f"sudo ip link set {INTERFACE_NAME} txqueuelen 65536")
        os.system(f"sudo ifconfig {INTERFACE_NAME} up")
    except OSError as e:
        raise OSError(f"Error configuring CAN interface: {e}")

def receive_messages(can_bus):
    try:
        while True:
            message = can_bus.recv()
            print(f"Received message: {message}")
    except can.CanError as e:
        print(f"Error receiving message: {e}")

def main():
    # Set up CAN interface
    setup_can_interface()

    # Assign can0 to the appropriate CAN bus object
    can0 = can.interface.Bus(channel=INTERFACE_NAME, bustype='socketcan')

    # Receive messages
    receive_messages(can0)

if __name__ == "__main__":
    main()
