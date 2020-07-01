#include <ESP8266WiFi.h>
#include <Adafruit_BME280.h>
#include <OneWire.h>

Adafruit_BME280 bme; // I2C

// OneWire DS18B20
OneWire  ds(D4);

// Replace with your network details
const char* ssid = "Keenetic-9275";
const char* password = "icbpnHXz";
const char* host = "85d.ru";
const char* sensorname = "wemos_south_balcony";
const char* key = "9b33a5";  // first 6 symbols of md5 hash of sensorname
float h, t, p;
char temperatureString[6];
char humidityString[6];
char pressureString[7];
char temperatureDSString[6];
String req, par, ds_sensor_name, ds_sensor_key;


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
    dtostrf(getTemperatureDS(), 5, 2, temperatureDSString);

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

    // send t DS
    Serial.println();
    Serial.println("*** Sending temperature from DS sensor ***");
    par = 't';
    ds_sensor_name = "wemos_south_balcony_DS18B20";
    ds_sensor_key = "ac56f7";
    req = create_url_(par, temperatureDSString, ds_sensor_name, ds_sensor_key);
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
    return t-1;
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

String create_url_(String p, String v, String s, String k){
    // create a URI for the request
    // http://localhost:5000/sensor-data?sensorname=wemos_south_balcony&parameter=t&value=24&key=9b33a5
    String url = "/sensor-data";
    url += "?sensorname=";
    url += s;
    url += "&parameter=";
    url += p;
    url += "&value=";
    url += v;
    url += "&key=";
    url += k;
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

float getTemperatureDS (){
    byte i;
    byte present = 0;
    byte type_s;
    byte data[12];
    byte addr[8];
    float celsius;

    if ( !ds.search(addr))
    {
        ds.reset_search();
        delay(250);
        return 0;
    }

    if (OneWire::crc8(addr, 7) != addr[7])
    {
        Serial.println("CRC is not valid!");
        return 0;
    }

    // the first ROM byte indicates which chip
    switch (addr[0])
    {
    case 0x10:
        type_s = 1;
        break;
    case 0x28:
        type_s = 0;
        break;
    case 0x22:
        type_s = 0;
        break;
    default:
        Serial.println("Device is not a DS18x20 family device.");
        return 0;
    }

    ds.reset();
    ds.select(addr);
    ds.write(0x44, 1);        // start conversion, with parasite power on at the end
    delay(1000);
    present = ds.reset();
    ds.select(addr);
    ds.write(0xBE);         // Read Scratchpad

    for ( i = 0; i < 9; i++)
    {
        data[i] = ds.read();
    }

    // Convert the data to actual temperature
    int16_t raw = (data[1] << 8) | data[0];
    if (type_s)
    {
        raw = raw << 3; // 9 bit resolution default
        if (data[7] == 0x10)
        {
            raw = (raw & 0xFFF0) + 12 - data[6];
        }
    }
    else
    {
        byte cfg = (data[4] & 0x60);
        if (cfg == 0x00) raw = raw & ~7;  // 9 bit resolution, 93.75 ms
        else if (cfg == 0x20) raw = raw & ~3; // 10 bit res, 187.5 ms
        else if (cfg == 0x40) raw = raw & ~1; // 11 bit res, 375 ms
    }
    celsius = (float)raw / 16.0;
    return celsius;
}