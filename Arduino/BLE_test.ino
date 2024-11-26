#include <ArduinoBLE.h>

BLEService customService("180C"); // 自訂服務 UUID
BLEUnsignedIntCharacteristic customCharacteristic("2A56", BLERead | BLENotify); // 自訂特徵值 UUID

void setup() {
  Serial.begin(9600);
  while (!Serial);

  if (!BLE.begin()) {
    Serial.println("初始化 BLE 失敗");
    while (1);
  }

  BLE.setLocalName("ArduinoNano33BLE");
  BLE.setAdvertisedService(customService);
  customService.addCharacteristic(customCharacteristic);
  BLE.addService(customService);

  customCharacteristic.writeValue(0);

  BLE.advertise();
  Serial.println("開始廣播");
}

void loop() {
  BLEDevice central = BLE.central();

  if (central) {
    Serial.print("已連線至中央裝置: ");
    Serial.println(central.address());

    while (central.connected()) {
      unsigned int dataToSend = analogRead(A0); // 讀取模擬輸入作為範例資料
      customCharacteristic.writeValue(dataToSend);
      delay(1000); // 每秒傳送一次
    }

    Serial.print("中央裝置已斷開連線: ");
    Serial.println(central.address());
  }
}
