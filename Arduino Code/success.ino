/*
 * --------------------------------------------------------------------------------------------------------------------
 * Example sketch/program showing how to read new NUID from a PICC to serial.
 * --------------------------------------------------------------------------------------------------------------------
 * This is a MFRC522 library example; for further details and other examples see: https://github.com/miguelbalboa/rfid
 * 
 * Example sketch/program showing how to the read data from a PICC (that is: a RFID Tag or Card) using a MFRC522 based RFID
 * Reader on the Arduino SPI interface.
 * 
 * When the Arduino and the MFRC522 module are connected (see the pin layout below), load this sketch into Arduino IDE
 * then verify/compile and upload it. To see the output: use Tools, Serial Monitor of the IDE (hit Ctrl+Shft+M). When
 * you present a PICC (that is: a RFID Tag or Card) at reading distance of the MFRC522 Reader/PCD, the serial output
 * will show the type, and the NUID if a new card has been detected. Note: you may see "Timeout in communication" messages
 * when removing the PICC from reading distance too early.
 * 
 * @license Released into the public domain.
 * 
 * Typical pin layout used:
 * -----------------------------------------------------------------------------------------
 *             MFRC522      Arduino       Arduino   Arduino    Arduino          Arduino
 *             Reader/PCD   Uno/101       Mega      Nano v3    Leonardo/Micro   Pro Micro
 * Signal      Pin          Pin           Pin       Pin        Pin              Pin
 * -----------------------------------------------------------------------------------------
 * RST/Reset   RST          9             5         D9         RESET/ICSP-5     RST
 * SPI SS      SDA(SS)      10            53        D10        10               10
 * SPI MOSI    MOSI         11 / ICSP-4   51        D11        ICSP-4           16
 * SPI MISO    MISO         12 / ICSP-1   50        D12        ICSP-1           14
 * SPI SCK     SCK          13 / ICSP-3   52        D13        ICSP-3           15
 */
#include <WiFiNINA.h>
#include <LiquidCrystal_I2C.h>
#include <ArduinoHttpClient.h>
#include <string.h>
#include <stdio.h>
#include <Wire.h>
#include <SPI.h>
#include <MFRC522.h>

#define SS_PIN 10
#define RST_PIN 9
 
MFRC522 rfid(SS_PIN, RST_PIN); // Instance of the class

MFRC522::MIFARE_Key key; 

// Init array that will store new NUID 
char nuidPICC[4];

char ssid[] = "iPhone (169)";
char pass[] = "Vishal@22";


const char serverName[] = "reman.herokuapp.com";
int port = 443;
WiFiSSLClient wifi;
HttpClient client = HttpClient(wifi, serverName, port);

int status = WL_IDLE_STATUS;

LiquidCrystal_I2C lcd = LiquidCrystal_I2C(0x27,16,2);

int relay = 8;


void setup() { 
  Serial.begin(9600);
  SPI.begin(); // Init SPI bus
  rfid.PCD_Init(); // Init MFRC522 
  lcd.init();          // Initiate the LCD module
  lcd.backlight();     // Turn on the backlight
  lcd.setCursor(0,0);
  lcd.print("Welcome");
  delay(3000);
  
  lcd.clear();

  pinMode (relay,OUTPUT);

  // check for the WiFi module:

  // if (WiFi.status() == WL_NO_MODULE) {

  //   Serial.println("Communication with WiFi module failed!");

  //   // don't continue

  //   while (true);

  // }

  // String fv = WiFi.firmwareVersion();
  //   Serial.println(fv);
  // if (fv < WIFI_FIRMWARE_LATEST_VERSION) {

  //   Serial.println("Please upgrade the firmware");

  // }


// WiFi.begin(ssid, pass);
  while (status != WL_CONNECTED) {
    Serial.print("Attempting to connect to WPA SSID: ");
    lcd.setCursor(0,0);
    lcd.print("Conncting to Wifi");
    // delay(3000); 
    Serial.println(ssid);
    status = WiFi.begin(ssid, pass);
    delay(5000);
  }

  // for (byte i = 0; i < 6; i++) {
  //   key.keyByte[i] = 0xFF;
  // }
  Serial.println("connected to wifi");
  lcd.setCursor(0,1);
  lcd.print("Connected");
  delay(3000);
  lcd.clear();
  Serial.println("Scan your card: ");
  lcd.setCursor(0,0);
  lcd.print("Scan your card");
  // delay(3000);
  // lcd.clear();
}
 
void loop() {



  // Look for new cards
  if ( ! rfid.PICC_IsNewCardPresent())
    return;

  // Verify if the NUID has been readed
  if ( ! rfid.PICC_ReadCardSerial())
    return;

   char uid[32] = "";
   array_to_string(rfid.uid.uidByte, 4, uid);

  Serial.print("Scanned Card: ");
  Serial.println(uid);
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print("Verifing...");
  // delay(5000);
  // lcd.clear();

  // char requestBody[] = '{ "uidVal": uid, "deviceId": "12345"  }';
  char requestBody1[25];
   char requestBody2[25];
  //  char dId[24]="";
    strcpy(requestBody1, "uidVal=");
    strcpy(requestBody2,"&deviceId=123");
    strcat(requestBody1, uid);
    
    strcat(requestBody1, requestBody2);
    Serial.println(requestBody1);
    
// String httpRequestData = "value1=" + test;
    Serial.println("making POST request");

    // String contentType = "application/x-www-form-urlencoded";
    // String postData = requestBody;

    client.post("/reman/givedata/", "application/x-www-form-urlencoded", requestBody1);
    int statusCode = client.responseStatusCode();
    Serial.print("Status code: ");
    Serial.println(statusCode);
    String response = client.responseBody();
    Serial.print("Response: ");
    Serial.println(response);
    // len = string_length(response);
    // Serial.println(len);
    // Serial.println("Wait 10 seconds");
    char last = response[15];
    Serial.println(last);
    delay(5000);
    if(last == 't')
    {
      lcd.clear();
      lcd.setCursor(0,0);
      lcd.print("Authorized");
      Serial.println("bd");
      digitalWrite(relay,HIGH);
      delay(5000);
      Serial.println("ad");
    }
    else if(last == '1')
    {
      lcd.clear();
      lcd.setCursor(0,0);
      lcd.print("Not Authorized");
    }
    else
    { 
      lcd.clear();
      lcd.print("user does not exist");      
    }

//  for (byte i = 0; i < 4; i++) {
//    Serial.print("print byte:");
//       Serial.print(rfid.uid.uidByte[i], HEX);
//    Serial.print("print char:");
//    Serial.print((char)rfid.uid.uidByte[i], HEX);
//       nuidPICC[i] = (char)rfid.uid.uidByte[i];
//     }
   
  // printHex(rfid.uid.uidByte, rfid.uid.size);
    // Serial.println();
   rfid.PICC_HaltA();
// Serial.print(nuidPICC);
  
  rfid.PCD_StopCrypto1();
}



// void printHex(byte *buffer, byte bufferSize) {
//   for (byte i = 0; i < bufferSize; i++) {
//     Serial.print(buffer[i] < 0x10 ? " 0" : " ");
//     Serial.print(buffer[i], HEX);
//   }
// }


void array_to_string(byte array[], unsigned int len, char buffer[])
{
   for (unsigned int i = 0; i < len; i++)
   {
      byte nib1 = (array[i] >> 4) & 0x0F;
      byte nib2 = (array[i] >> 0) & 0x0F;
      buffer[i*2+0] = nib1  < 0xA ? '0' + nib1  : 'A' + nib1  - 0xA;
      buffer[i*2+1] = nib2  < 0xA ? '0' + nib2  : 'A' + nib2  - 0xA;
   }
   buffer[len*2]='\0';
}

int string_length(char *str) {
   int length = 0;
   
   while (*str != '\0') {
      length++;
      str++;
   }
   
   return length;
}