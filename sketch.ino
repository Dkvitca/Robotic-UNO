#include <SPI.h>
#include <WiFiNINA.h>
#include <WiFiUdp.h>
#include <Servo.h>

// WiFi credentials
char ssid[] = "";//your wifi name
char pass[] = "";//your wifi password

// Motor control pins
int IN1 = 2;
int IN2 = 4;
int IN3 = 7;
int IN4 = 8;
int ENA = 5;
int ENB = 6;

// Ultrasonic sensor pins
const int trigPin = A1;
const int echoPin = A0;
Servo myServo;

// UDP settings
WiFiUDP udp;
const int localPort = 8888;
char packetBuffer[255];

// Server settings

IPAddress serverIP(,,,);  // Computer's IPv4 : (x,x,x,x) for example (0,0,0,0)
unsigned int serverPort = 8888;

// Sweep and measurement state
int sweepPosition = 0;    // Current servo position
int step = 6;             // Step size for servo movement
int delayTime = 100;       // Delay for smooth servo movement
bool isSweeping = true;  // Flag for sweep state

void setup() {
  Serial.begin(9600);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  myServo.attach(A2); // Servo on pin A2

  // Connect to WiFi
  while (WiFi.begin(ssid, pass) != WL_CONNECTED) {
    delay(10000);
  }
  Serial.println("Connected to WiFi");

  // Start UDP
  udp.begin(localPort);
}

void loop() {
  // Check for incoming UDP commands
  int packetSize = udp.parsePacket();
  if (packetSize) {
    int len = udp.read(packetBuffer, 255);
    if (len > 0) {
      packetBuffer[len] = 0;
    }
    Serial.print("Received command: ");
    Serial.println(packetBuffer);
    processCommand(packetBuffer);
  }

  // Handle sweeping and measurement
  if (isSweeping) {
    sweepAndMeasure();
  }
}

void processCommand(char* command) {
  if (strcmp(command, "forward") == 0) {
    moveForward();
  } else if (strcmp(command, "back") == 0) {
    moveBackward();
  } else if (strcmp(command, "right") == 0) {
    turnRight();
  } else if (strcmp(command, "left") == 0) {
    turnLeft();
  } else if (strcmp(command, "stop") == 0) {
    stopMotors();
  } else if (strcmp(command, "start_sweep") == 0) {
    isSweeping = true;
    sweepPosition = 0; // Start sweeping from 0 degrees
    myServo.write(sweepPosition); // Move servo to start position
  } else if (strcmp(command, "stop_sweep") == 0) {
    isSweeping = false;
  }
}

void moveForward() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  analogWrite(ENA, 200);

  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
  analogWrite(ENB, 200);
}

void moveBackward() {
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  analogWrite(ENA, 200);

  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
  analogWrite(ENB, 200);
}

void turnLeft() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  analogWrite(ENA, 200);

  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
  analogWrite(ENB, 200);
}

void turnRight() {
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  analogWrite(ENA, 200);

  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
  analogWrite(ENB, 200);
}

void stopMotors() {
  analogWrite(ENA, 0);
  analogWrite(ENB, 0);
}

void sweepAndMeasure() {
  // Perform sweeping in small increments
  if (sweepPosition >= 180) {
    sweepPosition = 0; // Reset to 0 degrees
  } else {
    sweepPosition += step; // Move to next position
  }

  myServo.write(sweepPosition); // Move servo to current position
  delay(delayTime); // Wait for servo to reach position

  measureAndSendDistance(sweepPosition); // Measure and send distance


}

void measureAndSendDistance(int pos) {
  long duration;
  int distance;

  // Clear the trigPin
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);

  // Set the trigPin on HIGH state for 10 microseconds
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  // Read the echoPin, returns the sound wave travel time in microseconds
  duration = pulseIn(echoPin, HIGH);

  // Calculate the distance
  distance = duration * 0.034 / 2;

  // Print the distance to the Serial Monitor for debugging
  Serial.print("Angle: ");
  Serial.print(pos);
  Serial.print(" Distance: ");
  Serial.println(distance);

  // Send the data via UDP
  String data = String(pos) + "," + String(distance);
  udp.beginPacket(serverIP, serverPort);
  udp.write(data.c_str());
  udp.endPacket();
}
