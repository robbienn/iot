#include "wifi_settings.h"
#include "DHT.h"

#include <SPI.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#include <TimeLib.h>
#include <NtpClientLib.h>
#include <ESP8266WiFi.h>

// DHT shield configuration
#define DHTPIN D4     // what pin we're connected to
#define DHTTYPE DHT22   // DHT 22  (AM2302)
DHT dht(DHTPIN, DHTTYPE);

// OLED shield configuration
#define OLED_RESET 0  // GPIO0
Adafruit_SSD1306 display(OLED_RESET);

String location = "UNKNOWN";
int loop_delay_after_th = 5000;
float temperature, humidity; // Temperature and humidity value

const int sleepMinutes = 10;
int sleepSeconds = 60 * sleepMinutes;

bool lcdIsOn = true;

const char* server = "api.thingspeak.com";
const char* api_key = "TO_BE_CHANGED"; // BBP office

WiFiClient client;

/*************************************************************************/
void print_th()
{
  display.clearDisplay();

  if (lcdIsOn) {
    display.setTextSize(2);
    display.setCursor(0, 0);
    display.println(temperature);

    display.setCursor(0, 30);
    display.println(humidity);

    display.setCursor(0, 19);
    display.setTextSize(1);
    display.print(location);  display.print(" ");
  }

  display.display();
}

/*************************************************************************/
void get_and_set_location()
{
  String mac_address = WiFi.macAddress();
  Serial.print("MAC: "); Serial.println(mac_address);
  Serial.print("Location: ");
  if (mac_address == MAC_LOZNICE) {
    Serial.println("LOZNICE");
    location = "LOZ";
  } else if (mac_address == MAC_KUCHYN) {
    Serial.println("KUCHYN");
    location = "KUCH";
  } else if (mac_address == MAC_DECAK) {
    Serial.println("DETSKY POKOJ");
    location = "DECAK";
  } else {
    Serial.println(" unknown due to unknown MAC address!");
  }
}

/* SETUP */

void setup()
{

  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);
  
  Serial.begin(115200);
  Serial.println("Serial console initialized");

  get_and_set_location();
  Serial.println("Location determined");

  dht.begin();
  Serial.println("DHT initialized");

  WiFi.mode (WIFI_STA);
  WiFi.begin (WIFI_SSID, WIFI_PASSWD);
  while (WiFi.status() != WL_CONNECTED) {
     delay(500);
     Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
 
  // by default, we'll generate the high voltage from the 3.3v line internally! (neat!)
  display.begin(SSD1306_SWITCHCAPVCC, 0x3C);  // initialize with the I2C addr 0x3C (for the 64x48)
  // init done
  display.clearDisplay();
  display.setTextColor(WHITE);

  display.setTextSize(3);
  display.setCursor(0, 0);
  display.println("OK");
  display.display();
  Serial.println("Display initialized and cleared");

  delay(1000);
  Serial.print("WiFi is "); Serial.println(WiFi.isConnected() ? "connected" : "not connected");


  temperature = dht.readTemperature();
  humidity = dht.readHumidity();
  if (isnan(temperature) || isnan(humidity))
  {
    Serial.println("Failed to read from DHT sensor!");
  } else {
    Serial.print("T: "); Serial.print(temperature); Serial.print(" - H: "); Serial.println(humidity);
    for (int l = 1; l <= 5; l++) {

    display.clearDisplay();
    display.setTextColor(WHITE);
    display.setTextSize(3);
    display.setCursor(0, 0);
    display.println(l);
    display.display();
    delay(loop_delay_after_th);     
      print_th();
      delay(loop_delay_after_th);
    }
  }

  display.clearDisplay();
  display.display();

  if (client.connect(server,80)) {
    Serial.println("Connect to ThingSpeak - OK"); 
    String dataToThingSpeak = "";
    dataToThingSpeak+="GET /update?api_key=";
    dataToThingSpeak+=api_key;
    dataToThingSpeak+="&field1=";
    dataToThingSpeak+=String(temperature);  
    dataToThingSpeak+="&field2=";
    dataToThingSpeak+=String(humidity);  
  
    dataToThingSpeak+=" HTTP/1.1\r\nHost: my.wemos.com\r\nConnection: close\r\n\r\n";
    dataToThingSpeak+="";
    client.print(dataToThingSpeak);  // 
 
    int timeout = millis() + 5000;
    while (client.available() == 0) {
        if (timeout - millis() < 0) {
          Serial.println(">>> ThingSpeak Timeout !");
          client.stop();
          return;
        }
      }
   }
 
  // Odezva z ThingSpeak 
  while(client.available()) {
      String line = client.readStringUntil('\r');
      Serial.print(line);
  }

  Serial.print("");

  Serial.print("going to deep sleep");
  digitalWrite(LED_BUILTIN, HIGH);   
  ESP.deepSleep(sleepSeconds * 1000000);

}


/* LOOP */

void loop()
{
}