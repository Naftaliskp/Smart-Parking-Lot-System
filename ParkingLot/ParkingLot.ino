#include <esp_now.h>
#include <WiFi.h>
#include <LiquidCrystal.h>

const char* ssid = "OPPO Reno5 F";
const char* password = "86903513";
uint8_t broadcastAddress[] = {0x7C, 0x9E, 0xBD, 0x48, 0x85, 0xB4};
LiquidCrystal lcd(14, 12, 13, 15, 2, 4);
int sensor = 23;
int red = 21;
int green = 22;
String send_msg;
String receive_msg;
String success;

typedef struct struct_message {
    String message;
} struct_message;

struct_message send_Data;
struct_message receive_Data;

void OnDataSent(const uint8_t *mac_addr, esp_now_send_status_t status) {
  if (status ==0){
    success = "Delivery Success :)";
  }
  else{
    success = "Delivery Fail :(";
  }
}
void OnDataRecv(const uint8_t * mac, const uint8_t *incomingData, int len) {
  memcpy(&receive_Data, incomingData, sizeof(receive_Data));
  receive_msg = receive_Data.message;
  Serial.println(receive_msg);
}

void setup() {
  Serial.begin(115200);
  pinMode(sensor, INPUT);
  pinMode(red, OUTPUT);
  pinMode(green, OUTPUT);
  digitalWrite(red,HIGH);
  digitalWrite(green,LOW);
  lcd.begin(16, 2);
  lcd.setCursor(0,0);
  lcd.print("SmartParkingLot");
  
  WiFi.mode(WIFI_AP_STA);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");
  
  if (esp_now_init() != ESP_OK) {
    Serial.println("Error initializing ESP-NOW");
    return;
  }
  esp_now_register_send_cb(OnDataSent);

  esp_now_peer_info_t peerInfo;
  memcpy(peerInfo.peer_addr, broadcastAddress, 6);
  peerInfo.channel = 0;  
  peerInfo.encrypt = false;

  if (esp_now_add_peer(&peerInfo) != ESP_OK){
    Serial.println("Failed to add peer");
    return;
  }
}

void loop() {
  digitalRead(sensor);
  if (!digitalRead(sensor)){
    delay(1000);
    Serial.println("ada");
    send_msg = "ada";
    send_Data.message = send_msg;
    esp_err_t result = esp_now_send(broadcastAddress, (uint8_t *) &send_Data, sizeof(send_Data));
    esp_now_register_recv_cb(OnDataRecv);
    if(receive_msg == "fix ada"){
      Serial.println("fix ada");
      digitalWrite(red,LOW);
      digitalWrite(green,HIGH);
      lcd.setCursor(0,1);
      lcd.print("Parkir terisi");
    }
    else if(!receive_msg || receive_msg == "fix ga ada"){
      Serial.println("fix ga ada");
      digitalWrite(red,HIGH);
      digitalWrite(green,LOW);
      lcd.setCursor(0,1);
      lcd.print("Parkir kosong");
    }
  }
  else {
    Serial.println("ga ada");
    digitalWrite(red,HIGH);
    digitalWrite(green,LOW);
    lcd.setCursor(0,1);
    lcd.print("Parkir kosong");
  }
}
