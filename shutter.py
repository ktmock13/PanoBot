import bluetooth
import time
from evdev import UInput, ecodes as e

def send_volume_up():
    ui = UInput()
    ui.write(e.EV_KEY, e.KEY_VOLUMEUP, 1)
    ui.write(e.EV_KEY, e.KEY_VOLUMEUP, 0)
    ui.syn()

def wait_for_connection():
    server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    server_sock.bind(("", bluetooth.PORT_ANY))
    server_sock.listen(1)

    uuid = "1e0ca4ea-299d-4335-93eb-27fcfe7fa848"  # Custom UUID for your application

    bluetooth.advertise_service(server_sock, "RaspberryPiShutter",
                                service_id=uuid,
                                service_classes=[uuid, bluetooth.SERIAL_PORT_CLASS],
                                profiles=[bluetooth.SERIAL_PORT_PROFILE])

    print("Waiting for Bluetooth connection...")

    client_sock, address = server_sock.accept()
    print(f"Connected to {address}")

    return client_sock

def main():
    client_sock = wait_for_connection()

    print("Waiting for 10 seconds before starting...")
    time.sleep(10)

    print("Starting to send volume up command every 5 seconds...")

    try:
        while True:
            send_volume_up()
            print("Shutter triggered")
            time.sleep(5)
    except KeyboardInterrupt:
        print("Keyboard interrupt received. Exiting...")
    finally:
        client_sock.close()

if __name__ == "__main__":
    main()