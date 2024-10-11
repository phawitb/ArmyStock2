#include <Keyboard.h>

// Constants for buttons
const int buttonPin2 = 2;
const int buttonPin3 = 3;

// Timing for long press detection (in milliseconds)
const unsigned long longPressDuration = 3000;

// Variables for button state tracking
unsigned long button2PressTime = 0;
unsigned long button3PressTime = 0;
bool button2LongPress = false;
bool button3LongPress = false;
bool bothLongPressHandled = false; // New flag for handling simultaneous long press
int menu = 0;

void setup() {
  // Configure buttons as input with pullup resistors
  pinMode(buttonPin2, INPUT_PULLUP);
  pinMode(buttonPin3, INPUT_PULLUP);

  // Initialize control over the keyboard
  Keyboard.begin();
}

void loop() {
  // Read the state of the buttons
  int button2State = digitalRead(buttonPin2);
  int button3State = digitalRead(buttonPin3);

  // Handle button 2 press
  if (button2State == LOW) {
    if (button2PressTime == 0) {
      // Button just pressed
      button2PressTime = millis();
    } else if (millis() - button2PressTime > longPressDuration && !button2LongPress) {
      // Long press detected
      button2LongPress = true;
      if (!bothLongPressHandled && button3LongPress) {
        onLongPressBothButtons();
      } else if (!button3LongPress) {
        onLongPressButton2();
      }
    }
  } else if (button2PressTime != 0) {
    if (!button2LongPress && millis() - button2PressTime < longPressDuration) {
      // Short press detected
      onShortPressButton2();
    }
    // Reset press tracking for button 2
    button2PressTime = 0;
    button2LongPress = false;
    bothLongPressHandled = false; // Reset the flag when buttons are released
  }

  // Handle button 3 press
  if (button3State == LOW) {
    if (button3PressTime == 0) {
      // Button just pressed
      button3PressTime = millis();
    } else if (millis() - button3PressTime > longPressDuration && !button3LongPress) {
      // Long press detected
      button3LongPress = true;
      if (!bothLongPressHandled && button2LongPress) {
        onLongPressBothButtons();
      } else if (!button2LongPress) {
        onLongPressButton3();
      }
    }
  } else if (button3PressTime != 0) {
    if (!button3LongPress && millis() - button3PressTime < longPressDuration) {
      // Short press detected
      onShortPressButton3();
    }
    // Reset press tracking for button 3
    button3PressTime = 0;
    button3LongPress = false;
    bothLongPressHandled = false; // Reset the flag when buttons are released
  }
}

// Function for short press on button 2
void onShortPressButton2() {
  Keyboard.print("c\n");
}

// Function for short press on button 3
void onShortPressButton3() {
  if (menu == 0) {
    Keyboard.print("1\n");
    menu++;
  } else if (menu == 1) {
    Keyboard.print("2\n");
    menu++;
  } else if (menu == 2) {
    Keyboard.print("c\n");
    menu = 0;
  }
}

// Function for long press on button 2
void onLongPressButton2() {
  Keyboard.print("r\n");
}

// Function for long press on button 3
void onLongPressButton3() {
  Keyboard.print("s\n");
}

// Function for simultaneous long press on both buttons
void onLongPressBothButtons() {
  Keyboard.print("h\n");
  bothLongPressHandled = true; // Set the flag to prevent multiple triggers
}
