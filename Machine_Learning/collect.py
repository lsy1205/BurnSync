import asyncio
from bleak import BleakScanner, BleakClient
import struct
import time
import json

# 设备名称和 UUID 配置
DEVICE_NAME = "BLE IMU Device_DCN"
CHARACTERISTIC_UUID = "87654321-4321-4321-4321-abcde1234567"  # 替换为你的设备 UUID

# 输出 JSON 文件路径
output_file = "./test_data.json"

# 初始化存储数据的结构
imu_data = {
    "AccelX": [],
    "AccelY": [],
    "AccelZ": [],
    "GyroX": [],
    "GyroY": [],
    "GyroZ": []
}

def handle_data(sender, data):
    """
    处理从 BLE 设备接收到的数据，并存储到 imu_data 结构中。
    """
    # 解码数据 (假设数据格式为 6 个 float 类型值)
    accelX, accelY, accelZ, gyroX, gyroY, gyroZ = struct.unpack('<ffffff', data)
    timestamp = time.time()

    # 将数据追加到 imu_data 结构中
    imu_data["AccelX"].append(accelX)
    imu_data["AccelY"].append(accelY)
    imu_data["AccelZ"].append(accelZ)
    imu_data["GyroX"].append(gyroX)
    imu_data["GyroY"].append(gyroY)
    imu_data["GyroZ"].append(gyroZ)
    #imu_data["Timestamp"].append(timestamp)

    #print(f"Data Received - Timestamp: {timestamp}, Accel: ({accelX}, {accelY}, {accelZ}), Gyro: ({gyroX}, {gyroY}, {gyroZ})")

async def monitor_connection(client):
    """
    持续监控 BLE 连接状态。
    """
    try:
        while await client.is_connected():
            await asyncio.sleep(1)  # 每秒检查一次连接状态
        print("Bluetooth connection lost. Saving data...")
    except Exception as e:
        print(f"Error during connection monitoring: {e}")

async def run():
    print("Scanning for device...")
    device = await BleakScanner.find_device_by_filter(lambda d, ad: d.name and DEVICE_NAME in d.name)

    if not device:
        print("Device not found. Make sure the device is advertising and try again.")
        return

    try:
        async with BleakClient(device) as client:
            print(f"Connected to {device.name}")

            # 启用 BLE 通知
            await client.start_notify(CHARACTERISTIC_UUID, handle_data)

            # 创建一个任务来监控连接状态
            monitor_task = asyncio.create_task(monitor_connection(client))

            print("Receiving data. Disconnect the device to stop.")
            await monitor_task  # 等待监控任务完成（蓝牙断开时退出）

            # 停止 BLE 通知（如果未正常结束，确保任务不会泄露）
            await client.stop_notify(CHARACTERISTIC_UUID)

    except Exception as e:
        print(f"Error during Bluetooth operation: {e}")
    finally:
        # 无论是否断开，保存 JSON 数据
        with open(output_file, "w") as json_file:
            json.dump(imu_data, json_file, indent=4)
        print(f"IMU data saved to {output_file}")

# 运行程序
asyncio.run(run())
