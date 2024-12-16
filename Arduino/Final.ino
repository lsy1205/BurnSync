#include <ArduinoBLE.h>
#include <ACROBOTIC_SSD1306.h>

#include "Arduino_BMI270_BMM150.h"

#include <Wire.h>

#include "MAX30105.h"
#include "heartRate.h"

// Define Time Interval
unsigned long currentMillis = 0;
unsigned long previousMillisBLE = 0;
const long intervalBLE = 100;

// Define Pins
int recordPin = D3;

// Define Buttons
bool buttonRecord = true;
bool preButtonRecord = true;

// MAX30102
MAX30105 particleSensor;

const byte RATE_SIZE = 4; //Increase this for more averaging. 4 is good.
byte rates[RATE_SIZE]; //Array of heart rates
byte rateSpot = 0;
long lastBeat = 0; //Time at which the last beat occurred

float beatsPerMinute;
int beatAvg;

char formattedBeat[4]; // 用於存儲格式化後的字串，3 位數字 + 結束符號 '\0'

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

  // OLED
  Wire.begin();	
  oled.init();                      // Initialze SSD1306 OLED display
  oled.clearDisplay();              // Clear screen
  oled.setTextXY(0,0);
  oled.putString("BurnSync");
  oled.setTextXY(1,0);
  oled.putString("Fitness Tracker");
  
  oled.setTextXY(3,0);
  oled.putString("Disconnected");
  
  // Initialize sensor
  if (!particleSensor.begin(Wire, I2C_SPEED_FAST)) //Use default I2C port, 400kHz speed
  {
    Serial.println("MAX30105 was not found. Please check wiring/power. ");
    while (1);
  }
  Serial.println("Place your index finger on the sensor with steady pressure.");

  particleSensor.setup(); //Configure sensor with default settings
  particleSensor.setPulseAmplitudeRed(0x0A); //Turn Red LED to low to indicate sensor is running
  particleSensor.setPulseAmplitudeGreen(0); //Turn off Green LED

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
    if (central.connected()) {
        oled.setTextXY(3,0);
        oled.putString("Connected   ");
        oled.setTextXY(6,0);
        oled.putString("Heart Rate ");
        oled.setTextXY(7,0);
        oled.putString("Avg BPM: ");
    }
    while (central.connected()) {
        currentMillis = millis();

        // IMU Data
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
        
        if (buttonRecord == 1 && preButtonRecord == 0) {
            record = !record;
        }
        preButtonRecord = buttonRecord;
        if (record) {
            oled.setTextXY(4,0);
            oled.putString("Recording    ");
        } else {
            oled.setTextXY(4,0);
            oled.putString("Not Recording");
        }

        // Heart Rate
        long irValue = particleSensor.getIR();

        if (checkForBeat(irValue) == true)
        {
          Serial.println("Got new data!");
          //We sensed a beat!
          long delta = millis() - lastBeat;
          lastBeat = millis();

          beatsPerMinute = 60 / (delta / 1000.0);

          if (beatsPerMinute < 150 && beatsPerMinute > 50)
          {
            rates[rateSpot++] = (byte)beatsPerMinute; //Store this reading in the array
            rateSpot %= RATE_SIZE; //Wrap variable

            //Take average of readings
            beatAvg = 0;
            for (byte x = 0 ; x < RATE_SIZE ; x++)
              beatAvg += rates[x];
            beatAvg /= RATE_SIZE;
          }
        }

        if (Serial) {
          Serial.print("IR=");
          Serial.print(irValue);
          Serial.print(", BPM=");
          Serial.print(beatsPerMinute);
          Serial.print(", Avg BPM=");
          Serial.println(beatAvg);
        }

        if (irValue < 50000){
          if (Serial) {
            Serial.println("No finger?");
          }
          oled.setTextXY(7,10);
          oled.putString("???");
        } else {
          oled.setTextXY(7,10);
          sprintf(formattedBeat, "%3d", beatAvg);
          oled.putString(formattedBeat);
        }
    }
    oled.setTextXY(3,0);
    oled.putString("Disconnected");
    oled.setTextXY(6,0);
    oled.putString("           ");
    oled.setTextXY(7,0);
    oled.putString("             ");

    if (Serial) {
      Serial.println("Disconnected from central");
    }
  }
}
