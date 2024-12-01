import asyncio
from bleak import BleakScanner, BleakClient  # 要pip install bleak
import struct
import csv
import time

DEVICE_NAME = "BLE IMU Device_DCN"
CHARACTERISTIC_UUID = "87654321-4321-4321-4321-abcde1234567"  # Arduino UUID

output_file = "imu_data.csv"
with open(output_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Timestamp", "Accel X", "Accel Y", "Accel Z", "Gyro X", "Gyro Y", "Gyro Z", "Start Flag"])

start_flag = 0

def handle_data(sender, data):
    global start_flag
    accelX, accelY, accelZ, gyroX, gyroY, gyroZ = struct.unpack('<ffffff', data)
    timestamp = time.time()
    #print(f"Timestamp: {timestamp}, Accel: ({accelX}, {accelY}, {accelZ}), Gyro: ({gyroX}, {gyroY}, {gyroZ}), Start Flag: {start_flag}")

    with open(output_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, accelX, accelY, accelZ, gyroX, gyroY, gyroZ, start_flag])

async def toggle_start_flag():
    global start_flag
    while True:
        # start_flag = 0
        await asyncio.sleep(2)
        start_flag = start_flag + 1
        # await asyncio.sleep(2)
        print("Start")

async def run():
    print("Scanning for device...")
    device = await BleakScanner.find_device_by_filter(lambda d, ad: d.name and DEVICE_NAME in d.name)

    if not device:
        print("Device not found. Make sure the device is advertising and try again.")
        return

    async with BleakClient(device) as client:
        print(f"Connected to {device.name}")

        await client.start_notify(CHARACTERISTIC_UUID, handle_data)
        toggle_task = asyncio.create_task(toggle_start_flag())
        await asyncio.sleep(60)
        toggle_task.cancel()
        await client.stop_notify(CHARACTERISTIC_UUID)

loop = asyncio.get_event_loop()
loop.run_until_complete(run())