#include <Wire.h>               // Only needed for Arduino 1.6.5 and earlier
#include "SH1106.h"
#include "font_lato_light_48.h"
#include <ESP8266WiFi.h>

// Wifi Settings
const char* ssid = "Keenetic-9275";
const char* password = "icbpnHXz";
const char* host = "85d.ru";
const char* url = "/api/weather-and-forecast";

// Display
SH1106 display(0x3c, D2, D1);     // ADDRESS, SDA, SCL

// PIR
int pirPin = D7;
int pirVal;

//receiving data from api
String currentT;
String forecastT;
String dt;
String service;
int pos1 = 0;
int pos2 = 0;
int pos3 = 0;

WiFiClient nmClient;

void setup()
{
    Serial.begin(115200);
    delay(10);

    // Initialising the UI will init the display too.
    display.init();
    display.flipScreenVertically();

    // Connecting to WiFi network
    Serial.print("Connecting to ");
    Serial.println(ssid);
    WiFi.begin(ssid, password);

    Serial.print("Delay 5 sec...");
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    Serial.println("");
    Serial.println("WiFi connected");

    // Printing the ESP IP address
    Serial.println(WiFi.localIP());
}

void weatherToDisplay() {
    display.setTextAlignment(TEXT_ALIGN_CENTER);
    display.setFont((uint8_t *) Lato_Light_48);
    display.drawString(64, 0, "+24.6");
    display.drawHorizontalLine(0, 52, 128);
    display.setFont(ArialMT_Plain_10);
    display.drawString(64, 54, "Tomorrow:  +22..+24");
}

void split(String input){
    Serial.println("Splitting:");
    Serial.println(input);
    input.remove(0,9);
    Serial.println(input);
    for (int i = 0; i < input.length(); i++) {
        if (input.substring(i, i+1) == ",") {
            if (pos1 == 0){
                pos1 = i;
            }else if (pos2 == 0){
                pos2 = i;
            }else if (pos3 == 0){
                pos3 = i;
            }
        }
    }
    currentT = input.substring(0, pos1);
    forecastT = input.substring(pos1+1, pos2);
    dt = input.substring(pos2+1, pos3);
    service = input.substring(pos3+1, input.length());
    Serial.println(currentT);
    Serial.println(forecastT);
    Serial.println(dt);
    Serial.println(service);
}

void get_data (){
    WiFiClientSecure client;
    const int httpPort = 443;
    if (!client.connect(host, httpPort)) {
        Serial.println("connection failed");
        return;
    }

    // This will send the request to the server
    client.print(String("GET ") + url +
                        " HTTP/1.1\r\n" +
                        "Host: " + host + "\r\n" +
                        "Connection: close\r\n\r\n");
    unsigned long timeout = millis();
    while (client.available() == 0) {
        if (millis() - timeout > 5000){
            Serial.println(">>> Client Timeout !");
            client.stop();
            return;
        }
    }
    // Read all the lines of the reply from server and print them to Serial
    Serial.println("Result: ");
    bool read_content = false;
    while (client.available()){
        String line = client.readStringUntil('\n');
        if (line.startsWith("wss-data:")){
            split(line);
        }
    }
    Serial.println();
    Serial.println("Closing connection");
}




void loop()
{
    pirVal = digitalRead(pirPin);
    //low = no motion, high = motion
    if (pirVal == LOW)
    {
        Serial.println("No motion");
        display.clear();
        display.display();
    }
    else
    {
        Serial.println("Motion detected  ALARM");
        display.clear();
        weatherToDisplay();
        display.display();
        delay(200);
    }
    get_data();
    delay(10000);
}