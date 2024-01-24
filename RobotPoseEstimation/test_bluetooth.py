import asyncio
from bleak import BleakScanner, BleakClient, BleakError

# https://makecode.microbit.org/pkg/LaboratoryForPlayfulComputation/pxt-BlockyTalkyBLE

BLOCKY_TALKY_SERVICE_UUID = '0b78ac2d-fe36-43ac-32d0-a29d8fbe05d6'
TX_CHARACTERISTIC_UUID = '0b78ac2d-fe36-43ac-32d0-a29d8fbe05d7' # tranmission channel
RX_CHARACTERISTIC_UUID = '0b78ac2d-fe36-43ac-32d0-a29d8fbe05d8'

async def discover_and_write():
    scanner = BleakScanner()
    timeout = 5
    print(f"Starting scan... [Timeout: {timeout} seconds]")
    # Scan for devices for 5 seconds
    await scanner.start()
    await asyncio.sleep(timeout)
    await scanner.stop()

    devices = scanner.discovered_devices

    # Search for the MicroBit by its name or services
    for device in devices:
        if device.name is not None and "BBC micro:bit" in device.name:
            address = device.address
            print("Found MicroBit with 'BBC micro:bit' name and address:", address)
            async with BleakClient(address, timeout=timeout) as client:
                try:
                    print("Attempting to connect to MicroBit...")

                    # this won't work on our version of the microbit since the
                    # bluetooth services take up too much RAM and are never
                    # instantiated
                    await client.connect()

                    # Convert "Forward" to bytes and write to the characteristic
                    # This was just to test if the robot can get any data at all
                    data = "Forward"
                    data_bytes = data.encode("utf-8")
                    await client.write_gatt_char(TX_CHARACTERISTIC_UUID, data_bytes, True)

                    print("Data written successfully to MicroBit!")
                    return

                except BleakError as e:
                    print(f"Error occurred: {e}")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(discover_and_write())
