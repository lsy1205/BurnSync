import asyncio
from bleak import BleakClient, BleakScanner

DEVICE_NAME = "ArduinoNano33BLE"
CHARACTERISTIC_UUID = "60CE8A50-B73A-EF35-95EC-50E8C5699014" # 請使用完整的 UUID

async def run():
    devices = await BleakScanner.discover()
    for d in devices:
        if d.name == DEVICE_NAME:
            async with BleakClient(d.address) as client:
                print(f"連接到 {d.address}")
                def notification_handler(sender, data):
                    value = int.from_bytes(data, byteorder='little')
                    print(f"接收到資料: {value}")

                await client.start_notify(CHARACTERISTIC_UUID, notification_handler)
                await asyncio.sleep(30.0) # 接收 30 秒
                await client.stop_notify(CHARACTERISTIC_UUID)
            return
    print("找不到指定的裝置")

asyncio.run(run())
