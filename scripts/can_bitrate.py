import os
import can
import time
INTERFACE_NAME = "can0"

def receive_message(can_bus, bitrate):
#    try:

    start_time = time.time()

    while time.time() - start_time < 3:
        message = can_bus.recv(timeout=1)
        if message is not None:
            print(f".........................................")
            print(f"Received message: {message}")
            print(f".........................................")

#    except can.CanError as e:
#        print(f"Error receiving message: {e}")

def main():
    #83333,9600,10000,10400,19200,20000,38400,41200,50000,57600,83333,100000,110000,115200,125000,250000,480000,500000,800000,1000000,2000000
    #    for bitrate in [50000, 100000, 125000, 250000, 500000, 1000000]:
    #    for bitrate in [9600,10000,10400,19200,20000,38400,41200,50000,57600,83333,100000,110000,115200,125000,250000,480000,500000,800000,1000000,2000000]:
    # Try common bitrates until successful
    for bitrate in [9600,10000,10400,19200,20000,38400,41200,50000,57600,83333,100000,110000,115200,125000,250000,480000,500000,800000,1000000,2000000]:
        try:

            print(f"Seting Interface to {bitrate}")

            os.system(f"sudo ip link set {INTERFACE_NAME} down")
            os.system(f"sudo ip link set {INTERFACE_NAME} type can bitrate {bitrate}")
            os.system(f"sudo ip link set {INTERFACE_NAME} txqueuelen 65536")
            os.system(f"sudo ifconfig {INTERFACE_NAME} up")

            can0 = can.interface.Bus(channel=INTERFACE_NAME, bustype='socketcan')
            receive_message(can0, bitrate)  # Listen for incoming messages
            #return  # Exit the loop once successful
        except can.CanError:
            pass

    else:
        raise Exception("Unable to find a suitable bitrate")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
