import asyncio
from bleak import BleakScanner, BleakClient  # 要pip install bleak
import struct
import csv
import time
import winsound  # 用於播放音效

DEVICE_NAME = "BLE IMU Device"
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

    with open(output_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, accelX, accelY, accelZ, gyroX, gyroY, gyroZ, start_flag])

# 播放音效
def play_sound():
    frequency = 440  # Hz (音頻頻率)
    duration = 500  # 毫秒 (音頻長度)
    winsound.Beep(frequency, duration)

async def toggle_start_flag():
    global start_flag
    while True:
        await asyncio.sleep(3)
        start_flag += 1
        print(f"Start Flag: {start_flag}")
        play_sound()  # 每次 start_flag 增加時播放音效

async def run():
    print("Scanning for device...")
    device = await BleakScanner.find_device_by_filter(lambda d, ad: d.name and DEVICE_NAME in d.name)

    if not device:
        print("Device not found. Make sure the device is advertising and try again.")
        return

    async with BleakClient(device) as client:
        print(f"Connected to {device.name}")

        await client.start_notify(CHARACTERISTIC_UUID, handle_data)
        toggle_task = asyncio.create_task(toggle_start_flag())  # 開始定期增加 start_flag
        await asyncio.sleep(90)
        toggle_task.cancel()  # 結束時取消定期任務
        await client.stop_notify(CHARACTERISTIC_UUID)

asyncio.run(run())
