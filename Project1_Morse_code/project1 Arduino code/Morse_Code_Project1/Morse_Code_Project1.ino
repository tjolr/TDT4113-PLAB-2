
// constants won't change. They're used here to set pin numbers:
const int buttonPin = 2;    // the number of the pushbutton pin
const int ledPinDash = 13; // the number of the LED pin
const int ledPinDot = 12;

//Timeconstants
const int T = 300;
const int dot = T;
const int dash = 3*T;
const int shortPause = 1.8*T;
const int mediumPause = 5*T;
const int longPause = 20*T;


// Variables will change:
int buttonState = HIGH;             // the current reading from the input pin
int lastButtonState = HIGH;   // the previous reading from the input pin
bool initButton = false; //initiates on first click


// the following variables are unsigned longs because the time, measured in
// milliseconds, will quickly become a bigger number than can be stored in an int.
unsigned long lastDebounceTime = 0;  // the last time the output pin was toggled
unsigned long debounceDelay = 50;    // the debounce time; increase if the output flickers
unsigned long buttonLastPressedTime = 0;
unsigned long pauseTimeStart = 0;

void setup() {
  pinMode(buttonPin, INPUT);
  pinMode(ledPinDash, OUTPUT);
  pinMode(ledPinDot, OUTPUT);

  Serial.begin(9600);
}

void loop() {
  // read the state of the switch into a local variable:
  int reading = digitalRead(buttonPin);

  // check to see if you just pressed the button
  // (i.e. the input went from LOW to HIGH), and you've waited long enough
  // since the last press to ignore any noise:

  // If the switch changed, due to noise or pressing:
  if (reading != lastButtonState) {
    // reset the debouncing timer
    lastDebounceTime = millis();
    initButton = true;
  }
  
  if ((millis() - lastDebounceTime) > debounceDelay && initButton == true) {
    // whatever the reading is at, it's been there for longer than the debounce
    // delay, so take it as the actual current state:

    // if the button state has changed:
    if (reading != buttonState) {
      buttonState = reading;
      
      if (buttonState == LOW) {
        digitalWrite(ledPinDash, LOW);
        digitalWrite(ledPinDot, LOW);

        buttonLastPressedTime = millis();

        int timeSincePauseStarted = millis() - pauseTimeStart;

        if (timeSincePauseStarted >= shortPause && timeSincePauseStarted < mediumPause) {
          //Symbol pause - short pause
          Serial.print("2");
        } else if (timeSincePauseStarted >= mediumPause && timeSincePauseStarted < longPause){
          //Word pause - medium pause
          Serial.print("3");
        } 
        
        pauseTimeStart = 0;
        
      } else if (buttonState == HIGH) {
        int timeSincePressed = millis() - buttonLastPressedTime;
        if(timeSincePressed <= dot){ 
          //Printing a Dot
          Serial.print("0");
          digitalWrite(ledPinDot, HIGH);
        } else if (timeSincePressed > dot && timeSincePressed <= dash) {
          //Printing a Dash
          Serial.print("1");
          digitalWrite(ledPinDash, HIGH);
        }        
        pauseTimeStart = millis();
        buttonLastPressedTime = 0;
      }  
    }
      
  }

  // save the reading. Next time through the loop, it'll be the lastButtonState:
  lastButtonState = reading;
}







 
