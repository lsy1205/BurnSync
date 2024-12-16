#include <ArduinoBLE.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SH110X.h>
#include "Arduino_BMI270_BMM150.h"
#include <Wire.h>

// Define Time Interval
unsigned long currentMillis = 0;
unsigned long previousMillisBLE = 0;
const long intervalBLE = 100;

// Define Pins
int recordPin = D3;

// Define Buttons
bool buttonRecord = true;
bool preButtonRecord = true;

// Define BLE and UUID
BLEService imuService("12345678-1234-1234-1234-123456789abc"); // Define UUID
BLECharacteristic imuCharacteristic("87654321-4321-4321-4321-abcde1234567", BLERead | BLEWrite | BLENotify, 512); // 24 字节用于发送 6 个浮点数

// Define Record Boolean
bool record = false;

void setup() {
  Serial.begin(9600);
  if (Serial) {
    Serial.println("Started");
  }
  
  // Pin Mode
  pinMode(recordPin, INPUT_PULLUP);
  digitalWrite(recordPin, HIGH);

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
        currentMillis = millis();
        if (currentMillis - previousMillisBLE >= intervalBLE) {
            previousMillisBLE = currentMillis;

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
            uint8_t data[25];
            memcpy(&data[0], &accelX, 4);
            memcpy(&data[4], &accelY, 4);
            memcpy(&data[8], &accelZ, 4);
            memcpy(&data[12], &gyroX, 4);
            memcpy(&data[16], &gyroY, 4);
            memcpy(&data[20], &gyroZ, 4);
            
            data[24] = record ? 1 : 0;

            imuCharacteristic.writeValue(data, 25); // Send data

        }

        // Record Button
        buttonRecord = digitalRead(recordPin);
        
        // if(Serial){
        //     Serial.println(buttonRecord);
        // }
        if (buttonRecord == 1 && preButtonRecord == 0) {
            record = !record;
        }
        preButtonRecord = buttonRecord;
    }

    if (Serial) {
      Serial.println("Disconnected from central");
    }
  }
}
