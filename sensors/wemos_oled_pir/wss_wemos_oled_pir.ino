#include <Wire.h>               // Only needed for Arduino 1.6.5 and earlier
#include "SH1106.h"

SH1106 display(0x3c, D2, D1);     // ADDRESS, SDA, SCL

// PIR
int pirPin = D7;
int pirVal;

void setup()
{
    Serial.begin(115200);
    Serial.println();
    Serial.println();
    Serial.println("Setup");

    // Initialising the UI will init the display too.
    display.init();
    display.flipScreenVertically();
}

void weatherToDisplay() {
    display.setTextAlignment(TEXT_ALIGN_LEFT);
    display.setFont(ArialMT_Plain_10);
    display.drawString(0, 10, "Current weather:");
    display.setFont(ArialMT_Plain_10);
    display.drawString(0, 20, "+24");
    display.setFont(ArialMT_Plain_10);
    display.drawString(0, 30, "Weather tomorrow:");
    display.drawString(0, 40, "+22..+25");
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
    delay(1000);
}