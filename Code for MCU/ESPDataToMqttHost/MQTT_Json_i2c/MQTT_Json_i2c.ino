#include <ArduinoJson.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include <INA226_asukiaaa.h>
//*************Defining Ohm************//
const uint16_t ina226calib = INA226_asukiaaa::calcCalibByResistorMilliOhm(2); // Max 5120 milli ohm
// const uint16_t ina226calib = INA226_asukiaaa::calcCalibByResistorMicroOhm(2000);
INA226_asukiaaa voltCurrMeter(INA226_ASUKIAAA_ADDR_A0_GND_A1_GND, ina226calib);
//*************Defining Ohm************//
int16_t ma, mv, mw;

const char* ssid = "mobilecampus";
const char* password =  "intranet";
const char* mqttServer = "172.22.20.98";
const int mqttPort = 1883;
#define MQTT_SERIAL_PUBLISH_CH "/bot/data"
#define MQTT_SERIAL_RECEIVER_CH "/icircuit/ESP32/serialdata/rx"

WiFiClient espClient;
PubSubClient client(espClient);
 
//*************My code*************************//

void setup_wifi() {
    delay(10);
    // We start by connecting to a WiFi network
    Serial.println();
    Serial.print("Connecting to ");
    Serial.println(ssid);
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
      delay(500);
      Serial.print(".");
    }
    randomSeed(micros());
    Serial.println("");
    Serial.println("WiFi connected");
    Serial.println("IP address: ");
    Serial.println(WiFi.localIP());
}


void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Create a random client ID
    String clientId = "ESP32Client-";
    clientId += String(random(0xffff), HEX);
    // Attempt to connect
    if (client.connect(clientId.c_str())) {
      Serial.println("connected");
      //Once connected, publish an announcement...
      client.publish(MQTT_SERIAL_PUBLISH_CH, "hello from ESP");
      // ... and resubscribe
      client.subscribe(MQTT_SERIAL_RECEIVER_CH);
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

void callback(char* topic, byte *payload, unsigned int length) {
    Serial.println("-------new message from broker-----");
    Serial.print("channel:");
    Serial.println(topic);
    Serial.print("data:");  
    Serial.write(payload, length);
    Serial.println();
}

//***************i2c function*************//
void i2c_func(){

  if (voltCurrMeter.readMV(&mv) == 0) {
    Serial.println(String(mv) + "mV");
  } else {
    Serial.println("Cannot read voltage.");
  }
  if (voltCurrMeter.readMA(&ma) == 0) {
    Serial.println(String(ma) + "mA");
  } else {
    Serial.println("Cannot read current.");
  }
  if (voltCurrMeter.readMW(&mw) == 0) {
    Serial.println(String(mw) + "mW");
  } else {
    Serial.println("Cannot read watt.");
  }
}
void setup() {
 
  Serial.begin(115200);
  Serial.setTimeout(500);// Set time out for 
  setup_wifi();
  
  client.setServer(mqttServer, mqttPort);
  client.setCallback(callback);
  reconnect();
   
   if (voltCurrMeter.begin() != 0) {
    Serial.println("Failed to begin INA226");
  }

}
 
void loop() {
 
 i2c_func();
const int capacity = JSON_OBJECT_SIZE(256);
StaticJsonDocument<capacity> doc;
 
doc["FC-Current"] = "Amp";
doc["FC-Voltage"] = "Volt";
doc["BAT-Current"] = "MiliAmp";
doc["BAT-Voltage"] = "MiliVolt";
  JsonArray values = doc.createNestedArray("values");
 //BAT values
  values.add(mv);
  values.add(ma);
  //add FC values inside values.add(FC_Voltage) vs values.add(FC_current)
  values.add(23);
  values.add(23);
 
  char JSONmessageBuffer[256];
  serializeJson(doc, JSONmessageBuffer, sizeof(JSONmessageBuffer));
  Serial.println("Sending message to MQTT topic..");
  Serial.println(JSONmessageBuffer);
 
  if (client.publish("esp/test", JSONmessageBuffer) == true) {
    Serial.println("Success sending message");
  } else {
    Serial.println("Error sending message");
  }
 
  client.loop();
  Serial.println("-------------"); 
  delay(2000);
 
}