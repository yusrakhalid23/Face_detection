#include <Keypad.h>

const byte ROWS = 4; // Four rows
const byte COLS = 3; // Three columns
char keys[ROWS][COLS] = {
  {'1', '2', '3'},
  {'4', '5', '6'},
  {'7', '8', '9'},
  {'*', '0', '#'}
};

byte rowPins[ROWS] = {8, 7, 6, 5}; // Connect to the row pinouts of the keypad
byte colPins[COLS] = {4, 3, 2}; // Connect to the column pinouts of the keypad

Keypad keypad = Keypad(makeKeymap(keys), rowPins, colPins, ROWS, COLS);

const String correctPassword = "123"; // Set your correct password here
String enteredPassword = "";
bool passwordEntryActive = false; // Flag to indicate if password entry is active

// Pin definitions for LED and buzzer
int ledPin = 13;  // Pin connected to LED
int buzzerPin = 12; // Pin connected to the buzzer

void setup() {
  Serial.begin(9600);
  pinMode(ledPin, OUTPUT);
  pinMode(buzzerPin, OUTPUT);
  digitalWrite(ledPin, LOW); // Ensure LED is off initially
  digitalWrite(buzzerPin, LOW); // Ensure buzzer is off initially
}

void loop() {
  char key = keypad.getKey();
  if (key) {
    if (key == '*') { // '*' is used as the start button
      Serial.println("START"); // Signal Python to start face detection
      passwordEntryActive = true; // Activate password entry
      enteredPassword = ""; // Clear entered password
      delay(500); // Debounce delay
    } 
    else if (key == '#') { // '#' is used as the stop button
      Serial.println("STOP"); // Signal Python to stop face detection
      passwordEntryActive = true; // Deactivate password entry
      enteredPassword = ""; // Clear entered password
      delay(500); // Debounce delay
    }
    else if (passwordEntryActive) {
      enteredPassword += key; // Add key to the password string

      if (enteredPassword.length() == 3) { // Check if the length is exactly 3
        if (enteredPassword == correctPassword) {
          Serial.println("Password Correct");
        } else {
          Serial.println("Password Incorrect");
        }
        enteredPassword = ""; // Reset password input after checking
        passwordEntryActive = false; // Deactivate password entry
      }
    }
  }

  // Read commands from Serial to control LED and buzzer
  if (Serial.available() > 0) {
    char command = Serial.read();
    if (command == 'Y') {
      digitalWrite(ledPin, LOW);  // Turn off LED
      digitalWrite(buzzerPin, LOW); // Turn off buzzer
    } else if (command == 'N') {
      digitalWrite(ledPin, HIGH);    // Turn on LED
      digitalWrite(buzzerPin, HIGH); // Turn on buzzer
    } else if (command == 'O') {
      digitalWrite(ledPin, LOW);    // Turn off LED
      digitalWrite(buzzerPin, LOW);  // Turn off buzzer
    }
  }
}
