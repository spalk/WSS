#include <Wire.h>               // Only needed for Arduino 1.6.5 and earlier
#include "SH1106.h"

#include "font_tinos_40.h"

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
    display.setTextAlignment(TEXT_ALIGN_CENTER);
    display.setFont((uint8_t *) Tinos_Bold_48);
    display.drawString(64, 0, "+24.6");
    display.drawHorizontalLine(0, 52, 128);
    display.setFont(ArialMT_Plain_10);
    display.drawString(64, 54, "Tomorrow:  +22..+24");
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