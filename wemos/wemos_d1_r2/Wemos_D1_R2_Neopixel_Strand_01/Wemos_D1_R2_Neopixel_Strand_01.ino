// Simple NeoPixel test.  Lights just a few pixels at a time so a
// 1m strip can safely be powered from Arduino 5V pin.  Arduino
// may nonetheless hiccup when LEDs are first connected and not
// accept code.  So upload code first, unplug USB, connect pixels
// to GND FIRST, then +5V and digital pin 6, then re-plug USB.
// A working strip will show a few pixels moving down the line,
// cycling between red, green and blue.  If you get no response,
// might be connected to wrong end of strip (the end wires, if
// any, are no indication -- look instead for the data direction
// arrows printed on the strip).

// https://www.tweaking4all.com/hardware/arduino/adruino-led-strip-effects/


#include <Adafruit_NeoPixel.h>

#define PIN    D6
//#define N_LEDS 16 // Circular 16LED
#define N_LEDS 300 // 5M LED STRIPE

#define BRIGHTNESS 128

#define CHASE_NO_PIXELS 50
#define CHASE_DELAY 2

#define RANDOM_DELAY_1 2
#define RANDOM_DELAY_2 10
#define RANDOM_LOOPS 20


Adafruit_NeoPixel strip = Adafruit_NeoPixel(N_LEDS, PIN, NEO_GRB + NEO_KHZ800);

void setup() {
  strip.begin();
  strip.setBrightness(BRIGHTNESS);
  randomSeed(analogRead(0));
}

void loop() {
  
  chase(strip.Color(255, 0, 0)); // Red
  chase(strip.Color(0, 255, 0)); // Green
  chase(strip.Color(0, 0, 255)); // Blue

  //colorWipe(strip.Color(255, 0, 0), 10); // Red
  //colorWipe(strip.Color(0, 255, 0), 10); // Green
  //colorWipe(strip.Color(0, 0, 255), 10); // Blue

  // Send a theater pixel chase in...
  theaterChase(strip.Color(127, 127, 127), 50); // White
  theaterChase(strip.Color(127, 0, 0), 50); // Red
  theaterChase(strip.Color(0, 0, 127), 50); // Blue

  rainbow(20);
  rainbowCycle(20);
  theaterChaseRainbow(50);


//  for(uint16_t i=0; i<RANDOM_LOOPS; i++) {
//    randomColors1(RANDOM_DELAY_1);
//  }

  for(uint16_t i=0; i<RANDOM_LOOPS; i++) {
    randomColors2(RANDOM_DELAY_2);
  }

}

// #######################################################


static void chase(uint32_t c) {
  for(uint16_t i=0; i<strip.numPixels()+CHASE_NO_PIXELS; i++) {
      strip.setPixelColor(i  , c); // Draw new pixel
      strip.setPixelColor(i-CHASE_NO_PIXELS, 0); // Erase pixel a few steps back
      strip.show();
      delay(CHASE_DELAY);
  }
}


// Fill the dots one after the other with a color
void colorWipe(uint32_t c, uint8_t wait) {
  for(uint16_t i=0; i<strip.numPixels(); i++) {
    strip.setPixelColor(i, c);
    strip.show();
    delay(wait);
  }
}

void rainbow(uint8_t wait) {
  uint16_t i, j;

  for(j=0; j<256; j++) {
    for(i=0; i<strip.numPixels(); i++) {
      strip.setPixelColor(i, Wheel((i+j) & 255));
    }
    strip.show();
    delay(wait);
  }
}

// Slightly different, this makes the rainbow equally distributed throughout
void rainbowCycle(uint8_t wait) {
  uint16_t i, j;

  for(j=0; j<256*5; j++) { // 5 cycles of all colors on wheel
    for(i=0; i< strip.numPixels(); i++) {
      strip.setPixelColor(i, Wheel(((i * 256 / strip.numPixels()) + j) & 255));
    }
    strip.show();
    delay(wait);
  }
}

//Theatre-style crawling lights.
void theaterChase(uint32_t c, uint8_t wait) {
  for (int j=0; j<10; j++) {  //do 10 cycles of chasing
    for (int q=0; q < 3; q++) {
      for (uint16_t i=0; i < strip.numPixels(); i=i+3) {
        strip.setPixelColor(i+q, c);    //turn every third pixel on
      }
      strip.show();

      delay(wait);

      for (uint16_t i=0; i < strip.numPixels(); i=i+3) {
        strip.setPixelColor(i+q, 0);        //turn every third pixel off
      }
    }
  }
}

//Theatre-style crawling lights with rainbow effect
void theaterChaseRainbow(uint8_t wait) {
  for (int j=0; j < 256; j++) {     // cycle all 256 colors in the wheel
    for (int q=0; q < 3; q++) {
      for (uint16_t i=0; i < strip.numPixels(); i=i+3) {
        strip.setPixelColor(i+q, Wheel( (i+j) % 255));    //turn every third pixel on
      }
      strip.show();

      delay(wait);

      for (uint16_t i=0; i < strip.numPixels(); i=i+3) {
        strip.setPixelColor(i+q, 0);        //turn every third pixel off
      }
    }
  }
}

// Input a value 0 to 255 to get a color value.
// The colours are a transition r - g - b - back to r.
uint32_t Wheel(byte WheelPos) {
  WheelPos = 255 - WheelPos;
  if(WheelPos < 85) {
    return strip.Color(255 - WheelPos * 3, 0, WheelPos * 3);
  }
  if(WheelPos < 170) {
    WheelPos -= 85;
    return strip.Color(0, WheelPos * 3, 255 - WheelPos * 3);
  }
  WheelPos -= 170;
  return strip.Color(WheelPos * 3, 255 - WheelPos * 3, 0);
}


void randomColors1(uint8_t wait) {
  uint32_t color = strip.Color(random(0,255), random(0,255), random(0,255));
  for(uint16_t i=0; i<strip.numPixels(); i++) {
    strip.setPixelColor(i, color);
    strip.show();
    delay(wait);
  }
}


void randomColors2(uint8_t wait) {

  uint32_t color = strip.Color(random(0,255), random(0,255), random(0,255));
  for(uint16_t i=0; i<strip.numPixels(); i++) {
    if(i%8==0) {
      color = strip.Color(random(0,255), random(0,255), random(0,255));
    }
    strip.setPixelColor(i, color);    
    strip.show();
    delay(wait);
  }
}

