Robotic Car Control and Sensor Mapping
This project involves the development of a four-wheeled robotic car using an Arduino Uno WiFi R2, integrating C++ and Python for control and real-time sensor data acquisition. The car uses ultrasonic sensors for environmental mapping and collision avoidance.

Features
Remote Control: Operate the car remotely using UDP communication for seamless interaction.
Real-Time Mapping: Utilizes ultrasonic sensors to create a real-time map of the surroundings, visualized using Python.
Servo and Sensor Integration: Employs servo motors to adjust sensor angles and collect data for comprehensive area coverage.
Asynchronous Communication: Implements multithreading for efficient data handling and motor control.
Visualization: Provides a dynamic plot of sensor data, updating live as the car navigates its environment.
Technologies and Libraries Used
Arduino Uno WiFi R2: For microcontroller programming and sensor integration.
Python: For remote control and data visualization.
Socket: For UDP communication.
Matplotlib: For dynamic plotting of sensor data.
Keyboard: For capturing keyboard events.
Threading: For handling data reception asynchronously.
C++: For core control logic and communication.
WiFiNINA: For WiFi connectivity.
Servo: For controlling servo motors.
WiFiUDP: For handling UDP communication.
UDP Protocol: For efficient, low-latency data exchange.
