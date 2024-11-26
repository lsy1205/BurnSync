import asyncio
from bleak import BleakScanner, BleakClient         #要pip install bleak
import struct
import csv
import time

DEVICE_NAME = "BLE IMU Device"  
CHARACTERISTIC_UUID = "87654321-4321-4321-4321-abcde1234567"  # Arduino UUID

output_file = "imu_data.csv"
with open(output_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Timestamp", "Accel X", "Accel Y", "Accel Z", "Gyro X", "Gyro Y", "Gyro Z"])

def handle_data(sender, data):
    accelX, accelY, accelZ, gyroX, gyroY, gyroZ = struct.unpack('<ffffff', data)
    timestamp = time.time()
    print(f"Timestamp: {timestamp}, Accel: ({accelX}, {accelY}, {accelZ}), Gyro: ({gyroX}, {gyroY}, {gyroZ})")

    with open(output_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, accelX, accelY, accelZ, gyroX, gyroY, gyroZ])

async def run():
    print("Scanning for device...")
    device = await BleakScanner.find_device_by_filter(lambda d, ad: d.name and DEVICE_NAME in d.name)
    
    if not device:
        print("Device not found. Make sure the device is advertising and try again.")
        return

    async with BleakClient(device) as client:
        print(f"Connected to {device.name}")

        await client.start_notify(CHARACTERISTIC_UUID, handle_data)
        await asyncio.sleep(60)
        await client.stop_notify(CHARACTERISTIC_UUID)

loop = asyncio.get_event_loop()
loop.run_until_complete(run())
