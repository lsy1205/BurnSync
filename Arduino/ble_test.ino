#include <ArduinoBLE.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SH110X.h>
#include "Arduino_BMI270_BMM150.h"
#include <Wire.h>

// Define BLE and UUID
// #define SCREEN_WIDTH 128 // OLED 寬度
// #define SCREEN_HEIGHT 64 // OLED 高度
// #define OLED_RESET    -1
// Adafruit_SH1106G display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);
BLEService imuService("12345678-1234-1234-1234-123456789abc"); // Define UUID
BLECharacteristic imuCharacteristic("87654321-4321-4321-4321-abcde1234567", BLERead | BLEWrite | BLENotify, 512); // 24 字节用于发送 6 个浮点数

void setup() {
  Serial.begin(9600);
  if (Serial) {
    Serial.println("Started");
  }

  // 初始化 BLE
  if (!BLE.begin()) {
    if (Serial) {
      Serial.println("Failed to initialize BLE!");
    }
    while (1); 
  }

  BLE.setLocalName("BLE IMU Device");
  BLE.setAdvertisedService(imuService);

  imuService.addCharacteristic(imuCharacteristic);
  BLE.addService(imuService);

  // 初始化 IMU
  if (!IMU.begin()) {
    if (Serial) {
      Serial.println("Failed to initialize IMU!");
    }
    while (1); 
  }

  if (Serial) {
    Serial.println("BLE IMU Device is now advertising...");
  }
  BLE.advertise();
}

void loop() {
  BLEDevice central = BLE.central();

  if (central) {
    if (Serial) {
      Serial.print("Connected to central: ");
      Serial.println(central.address());
    }

    while (central.connected()) {
      float accelX, accelY, accelZ;
      float gyroX, gyroY, gyroZ;

      // Read acceleration
      if (IMU.accelerationAvailable()) {
        IMU.readAcceleration(accelX, accelY, accelZ);
      }

      //Read gyroscope
      if (IMU.gyroscopeAvailable()) {
        IMU.readGyroscope(gyroX, gyroY, gyroZ);
      }

      if (imuCharacteristic.written()) {
        String receivedString;
        char buffer[32]; // 假設最大字串長度為 32
        int len = imuCharacteristic.readValue(buffer, sizeof(buffer));
      }

      // Concat
      uint8_t data[24];
      memcpy(&data[0], &accelX, 4);
      memcpy(&data[4], &accelY, 4);
      memcpy(&data[8], &accelZ, 4);
      memcpy(&data[12], &gyroX, 4);
      memcpy(&data[16], &gyroY, 4);
      memcpy(&data[20], &gyroZ, 4);

      imuCharacteristic.writeValue(data, 24); // Send dataa
      delay(100); // sample rate:  100 us => 10Hz  (每秒10次)
    }

    if (Serial) {
      Serial.println("Disconnected from central");
    }
  }
}
