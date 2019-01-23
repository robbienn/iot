#include "DHT.h"

#include <SPI.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <TimeLib.h>
#include <NtpClientLib.h>
#include <ESP8266WiFi.h>
#include <BlynkSimpleEsp8266.h>

char auth[] = "";

// MAC addresses of WEMOS D1 Mini boards @home
#define MAC_LOZNICE "60:01:94:14:E2:EC"
#define MAC_OBYVAK "A0:20:A6:07:56:B5"
#define MAC_DECAK "5C:CF:7F:34:46:A5"

// WiFI AP configuration
//#define YOUR_WIFI_SSID "Tieto Any Device"
//#define YOUR_WIFI_PASSWD "3aIM:DX6j:4KqD"

#define YOUR_WIFI_SSID ""
#define YOUR_WIFI_PASSWD ""


// DHT shield configuration
#define DHTPIN D4     // what pin we're connected to
#define DHTTYPE DHT22   // DHT 22  (AM2302)
DHT dht(DHTPIN, DHTTYPE);

// OLED shield configuration
#define OLED_RESET 0  // GPIO0
Adafruit_SSD1306 display(OLED_RESET);

// Button shield configuration
const byte buttonPin = D3;
unsigned long lastDebounceTime = 0;  // the time the button state last switched
unsigned long debounceDelay = 1000;    // the state must remain the same for this many millis to register the button press

// NTP
int8_t timeZone = 1;
int8_t minutesTimeZone = 0;
bool wifiFirstConnected = false;

// App params and vars
long iterationNumber = 0;
bool lcdIsOn = true;
String location = "UNKNOWN";
int loop_delay_after_failure = 5000;
int loop_delay_after_date_time = 5000;
int loop_delay_after_th = 5000;
float temperature, humidity; // Temperature and humidity value
String date_str, time_str, timestamp;

// NTP
/*************************************************************************/
void onSTAConnected (WiFiEventStationModeConnected ipInfo) {
    Serial.printf ("Connected to %s\r\n", ipInfo.ssid.c_str ());
}

// Start NTP only after IP network is connected
void onSTAGotIP (WiFiEventStationModeGotIP ipInfo) {
    Serial.printf ("Got IP: %s\r\n", ipInfo.ip.toString ().c_str ());
    Serial.printf ("Connected: %s\r\n", WiFi.status () == WL_CONNECTED ? "yes" : "no");
    wifiFirstConnected = true;
}

// Manage network disconnection
void onSTADisconnected (WiFiEventStationModeDisconnected event_info) {
    Serial.printf ("Disconnected from SSID: %s\n", event_info.ssid.c_str ());
    Serial.printf ("Reason: %d\n", event_info.reason);
    //NTP.stop(); // NTP sync can be disabled to avoid sync errors
}

void processSyncEvent (NTPSyncEvent_t ntpEvent) {
    if (ntpEvent) {
        Serial.print ("Time Sync error: ");
        if (ntpEvent == noResponse)
            Serial.println ("NTP server not reachable");
        else if (ntpEvent == invalidAddress)
            Serial.println ("Invalid NTP server address");
    } else {
        Serial.print ("Got NTP time: ");
        Serial.println (NTP.getTimeDateString (NTP.getLastNTPSync ()));
    }
}

boolean syncEventTriggered = false; // True if a time even has been triggered
NTPSyncEvent_t ntpEvent; // Last triggered event


/*************************************************************************/
void checkButtonPressed()
{
  Serial.println("Interrupt callback called");
  if ((millis() - lastDebounceTime) > debounceDelay) {
      lcdIsOn = ! lcdIsOn;
      Serial.print("LCD On is now:"); Serial.println(lcdIsOn);
  } else {
      Serial.println("interrupt Ignored");
  }
  lastDebounceTime = millis();

 print_th();  
}

/*************************************************************************/
void print_th()
{
  display.clearDisplay();
  
  if (lcdIsOn) {
    display.setTextSize(2);
    display.setCursor(0,0);
    display.println(temperature);
  
    display.setCursor(0,30);
    display.println(humidity);
  
    display.setCursor(0,19);
    display.setTextSize(1);
    display.print(location);  display.print(" "); display.println(iterationNumber);
  }
  
  display.display();

  Blynk.virtualWrite(V5, humidity);
  Blynk.virtualWrite(V6, temperature);
}

/*************************************************************************/
void print_date_time()
{
  display.clearDisplay();
  
  if (lcdIsOn) {
    display.setTextSize(2);
    display.setCursor(0,0);
    display.println(date_str);
  
    display.setCursor(0,30);
    display.println(time_str);
  
    display.setCursor(0,19);
    display.setTextSize(1);
    display.print(location);  display.print(" "); display.println(iterationNumber);
  }
  
  display.display();

  Blynk.virtualWrite(V4, timestamp);
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
  } else if (mac_address == MAC_OBYVAK) {
    Serial.println("OBYVAK");
    location = "OBYVAK";
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
  Serial.begin(115200);
  Serial.println("Serial console initialized");

  // NTP
  static WiFiEventHandler e1, e2, e3;
  WiFi.mode (WIFI_STA);
  WiFi.begin (YOUR_WIFI_SSID, YOUR_WIFI_PASSWD);

  NTP.onNTPSyncEvent ([](NTPSyncEvent_t event) {
      ntpEvent = event;
      syncEventTriggered = true;
  });
  e1 = WiFi.onStationModeGotIP (onSTAGotIP);// As soon WiFi is connected, start NTP Client
  e2 = WiFi.onStationModeDisconnected (onSTADisconnected);
  e3 = WiFi.onStationModeConnected (onSTAConnected);

  Blynk.begin(auth, YOUR_WIFI_SSID, YOUR_WIFI_PASSWD);

  get_and_set_location();
  Serial.println("Location determined");
  
  dht.begin();
  Serial.println("DHT initialized");
  
  attachInterrupt(digitalPinToInterrupt(buttonPin), checkButtonPressed, FALLING);
  Serial.println("Button interrupt attached");

  // by default, we'll generate the high voltage from the 3.3v line internally! (neat!)  
  display.begin(SSD1306_SWITCHCAPVCC, 0x3C);  // initialize with the I2C addr 0x3C (for the 64x48)
  // init done
  display.clearDisplay();
  display.setTextColor(WHITE);  
  display.display();
  Serial.println("Display initialized and cleared");

  pinMode(buttonPin, INPUT); 

  delay(1000);
}


/* LOOP */

void loop() 
{
  iterationNumber++;
  Serial.println("##############################");
  Serial.print("Iteration #");Serial.println(iterationNumber);

  if (wifiFirstConnected) {
      wifiFirstConnected = false;
      NTP.begin ("pool.ntp.org", timeZone, true, minutesTimeZone);
      NTP.setInterval (63);
  }

  if (syncEventTriggered) {
      processSyncEvent (ntpEvent);
      syncEventTriggered = false;
  }

  date_str = NTP.getDateStr().substring(0,5);
  time_str = NTP.getTimeStr().substring(0,5);
  timestamp = date_str + " - " + time_str;
  Serial.print("DATE: "); Serial.print(date_str); Serial.print(", TIME: ");  Serial.println(time_str);

  Serial.print("WiFi is "); Serial.println(WiFi.isConnected() ? "connected" : "not connected");
  Serial.print("Uptime: "); Serial.print(NTP.getUptimeString()); Serial.print(" since "); Serial.println(NTP.getTimeDateString(NTP.getFirstSync()).c_str());

  Blynk.run();

  temperature = dht.readTemperature();
  humidity = dht.readHumidity();  
  if (isnan(temperature) || isnan(humidity)) 
  {
    Serial.println("Failed to read from DHT sensor!");   
    delay(loop_delay_after_failure);
  } else {
    Serial.print("T: "); Serial.print(temperature); Serial.print(" - H: "); Serial.println(humidity);    
    for (int l=1; l<=5; l++) {
        print_date_time();
        delay(loop_delay_after_date_time);
        print_th();
        delay(loop_delay_after_th);
    }    
  }
   
}

