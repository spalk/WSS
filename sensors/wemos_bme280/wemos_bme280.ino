#include <ESP8266WiFi.h>
#include <Adafruit_BME280.h>
#include <string>
using std::string;

Adafruit_BME280 bme; // I2C

// Replace with your network details
const char* ssid = "YOUR_WIFI";
const char* password = "WIFI_PASSWORD";
const char* host = "hostname.com";
const char* sensorname = "wemos";
const char* key = "key_phrase";  // first 6 symbols of md5 hash of sensorname
float h, t, p;
char temperatureString[6];
char humidityString[6];
char pressureString[7];
String req, par;


WiFiClient nmClient;
// only runs once on boot
void setup() {
    // Initializing serial port for debugging purposes
    Serial.begin(115200);
    delay(10);

    // Connecting to WiFi network
    Serial.println();
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
    Serial.println(F("BME280 start"));

    if (!bme.begin()) {
        Serial.println("Could not find a valid BME280 sensor, check wiring!");
        while (1);
    }
}

// runs over and over again
void loop() {
    // float to String
    dtostrf(getTemperature(), 5, 2, temperatureString);
    dtostrf(getPressure(), 6, 2, pressureString);
    dtostrf(getHumidity(), 5, 2, humidityString);

    // send t
    Serial.println();
    Serial.println("*** Sending temperature ***");
    par = 't';
    req = create_url(par, temperatureString);
    Serial.println(req);
    send_data(req);
    delay(100);

    // send p
    Serial.println();
    Serial.println("*** Sending pressure ***");
    par = 'p';
    req = create_url(par, pressureString);
    Serial.println(req);
    send_data(req);
    delay(100);

    //send h
    Serial.println();
    Serial.println("*** Sending humidity ***");
    par = 'h';
    req = create_url(par, humidityString);
    Serial.println(req);
    send_data(req);
    delay(600000);
}

float getTemperature(){
    t = 0;
    float valt;
    for (int i=0; i<30; i++) {
        delay (random(50,500));
        valt = bme.readTemperature();
        t = t+valt;
    }
    t=t/30;
    return t;
}

float getPressure(){
    p = 0;
    float valp;
    for (int i=0; i<30; i++) {
        delay (random(50,500));
        valp = bme.readPressure();
        p = p+valp;
    }
    p=p/30/100.0F*0.75;  //mmhg
    return p;
}

float getHumidity() {
    h = 0;
    float valh;
    for (int i=0; i<30; i++) {
        delay (random(50,500));
        valh = bme.readHumidity();
        h = h+valh;
    }
    h=h/30;
    return h;
}

String create_url(String p, String v){
    // create a URI for the request
    // http://localhost:5000/sensor-data?sensorname=wemos_south_balcony&parameter=t&value=24&key=9b33a5
    String url = "/sensor-data";
    url += "?sensorname=";
    url += sensorname;
    url += "&parameter=";
    url += p;
    url += "&value=";
    url += v;
    url += "&key=";
    url += key;
    return url;
}

void send_data (String url){
    // sending data to server
    Serial.print("Connecting to: ");
    Serial.println(host);
    WiFiClientSecure client;
    const int httpPort = 443;
    if (!client.connect(host, httpPort)) {
        Serial.println("connection failed");
        return;
    }

    Serial.print("Requesting URL: ");
    Serial.println(url);
    // This will send the request to the server
    client.print(String("GET ") + url +
                        " HTTP/1.1\r\n" +
                        "Host: " + host + "\r\n" +
                        "Upgrade-Insecure-Requests: 1" +
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
    while (client.available()){
        String line = client.readStringUntil('\r');
        Serial.print(line);
    }
    Serial.println();
    Serial.println("Closing connection");
}
