#include <Wire.h>               // Only needed for Arduino 1.6.5 and earlier
#include "SH1106.h"
#include "font_lato_light_48.h"
#include <ESP8266WiFi.h>

// Wifi Settings
const char* ssid = "Keenetic-9275";
const char* password = "icbpnHXz";

// Host
const char* host = "85d.ru";
const char* url = "/api/weather-and-forecast";

// Display
SH1106 display(0x3c, D2, D1);     // ADDRESS, SDA, SCL
int showTimeout = 10000; // time before off display

// PIR
int pirPin = D7;
int pirVal; //low = no motion, high = motion

// Data from api
String currentT;
String forecastT;
String dt;
String service;

// Delimiter positions
int pos1 = 0;
int pos2 = 0;
int pos3 = 0;
int dataTimeout = 300000; // time before off display

// Timers
unsigned long data_time;
unsigned long show_time;


WiFiClient nmClient;

void ProgressBar(int progress){
    display.drawProgressBar(0, 32, 120, 10, progress);
}

void log(String msg, int progress){
    display.clear();
    display.setTextAlignment(TEXT_ALIGN_CENTER);
    display.drawString(64, 10, msg);
    ProgressBar(progress);
    display.display();
    Serial.println(msg);
    delay(800);
}

void split(String input){
    Serial.print("Splitting: ");
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
        Serial.println("Connection failed");
        return;
    }

    // Send the request to the server
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

    // Read reply from server
    Serial.println("Result: ");
    while (client.available()){
        String line = client.readStringUntil('\n');
        if (line.startsWith("wss-data:")){
            split(line);
            break;
        }
    }
    Serial.println("Closing connection");
}

void mainView() {
    display.clear();
    display.setTextAlignment(TEXT_ALIGN_CENTER);
    display.setFont((uint8_t *) Lato_Light_48);
    display.drawString(64, -5, currentT);
    display.drawHorizontalLine(0, 48, 128);
    display.setFont(ArialMT_Plain_10);
    display.drawString(64, 50, "RP5 for " + dt + ":  " + forecastT);
    display.display();
}

void displayOff() {
    display.clear();
    display.display();
}

void setup()
{
    Serial.begin(115200);
    delay(10);

    // Initialising display
    display.init();
    //display.flipScreenVertically();

    // Welcome screen
    display.clear();
    display.setTextAlignment(TEXT_ALIGN_CENTER);
    display.setFont(ArialMT_Plain_10);
    display.drawHorizontalLine(0, 8, 128);
    display.drawHorizontalLine(0, 42, 128);
    display.display();
    delay(500);
    display.drawString(64, 10, "welcome to");
    display.drawString(64, 30, "WSS");
    display.display();
    delay(3000);
    display.clear();
    ProgressBar(0);
    delay(1000);
    // Connecting to WiFi network
    log("Connecting to WiFi...", 10);
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    ProgressBar(20);
    delay(1000);
    log("WiFi connected successfully", 30);

    // Get data
    log("Receiving data...", 50);
    get_data();
    log("Data received successfully", 70);
    log("Loading main screen...", 80);
    ProgressBar(90);
    ProgressBar(100);
    delay(500);
    data_time = millis();

    // Show main view
    mainView();
    show_time = millis();
}

void loop()
{
    // Motion detection
    pirVal = digitalRead(pirPin);
    if (pirVal == LOW){
        Serial.println("No motion");
        if (millis() - show_time > showTimeout){
            displayOff();
        }
    } else {
        Serial.println("Motion detected");
        mainView();
        show_time = millis();
    }

    // Data update
    if (millis() - data_time > dataTimeout){
        get_data();
        data_time = millis();
    }

    // Delay
    delay(1000);
}