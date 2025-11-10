# Mini Sonar with Arduino and Processing

This project demonstrates a simple mini sonar system using an **Arduino**, an **ultrasonic sensor**, and a **servo motor**, with real-time visualization in **Processing**. It is designed for beginners to learn about sensor interfacing, serial communication, and graphical visualization.

---

## Table of Contents
- [Components](#components)
- [Wiring](#wiring)
- [Arduino Code](#arduino-code)
- [Processing Visualization](#processing-visualization)
- [How It Works](#how-it-works)
- [Running the Project](#running-the-project)
- [Notes](#notes)

---

## Components
- Arduino Uno (or compatible board)  
- HC-SR04 Ultrasonic Sensor  
- SG90 / MG90 Servo Motor  
- Jumper wires  
- Breadboard (optional)  

---

## Wiring

**Ultrasonic Sensor**  
- VCC → 5V  
- GND → GND  
- Trig → Pin 10  
- Echo → Pin 11  

**Servo Motor**  
- Signal → Pin 12  
- VCC → 5V  
- GND → GND  

> Do not power the servo directly from Arduino if it draws too much current; use an external 5V source if needed.

---

## Arduino Code

The Arduino code rotates the servo motor back and forth between 15° and 165° while measuring distances with the ultrasonic sensor. For each step:

1. The servo moves to a new angle.  
2. The ultrasonic sensor measures the distance to the nearest object.  
3. Arduino sends a line of data over the serial port in the format:


- `angle` = current servo angle (degrees)  
- `distance` = measured distance (cm)  
- `.` = delimiter to signal the end of the measurement  

This data is read by Processing for visualization. You can find the code in `ard_ide.ino`.

---

## Processing Visualization

The Processing sketch reads the serial data from Arduino and creates a radar-like interface. Key steps include:

1. **Serial reading**: Processing reads each line from the serial port until it encounters the `.` delimiter. It extracts the angle and distance values.  
2. **Mapping coordinates**: The distance is mapped to pixels on the screen, and the angle determines the direction from the radar center.  
3. **Radar beam**: A moving line represents the current servo position.  
4. **Echo points**: Detected objects are drawn as points, which gradually fade to simulate sonar blips.  
5. **UI**: A bottom bar shows the current angle and distance, along with the project name.

The radar display updates continuously, giving a dynamic visualization of detected objects.

You can find the Processing code in `sketch_251108b.pde`.

---

## How It Works

1. Arduino rotates the servo in small increments, scanning the environment.  
2. The ultrasonic sensor measures distances at each angle.  
4. Arduino sends the measurements to Processing via serial communication.  
5. Processing parses the data, calculates the position of each detected object, and draws it on a radar display.  
6. Previous points fade over time, creating a “blip” effect similar to a real sonar.  

---

## Running the Project

1. Connect your Arduino to the computer.  
2. Upload `ard_ide.ino` to your Arduino board.  
3. Open Processing and run `sketch_251108b.pde`.  
4. Update the serial port in Processing to match your Arduino (for example, `"COM3"` on Windows or `"/dev/tty.usbmodemXXXX"` on macOS).  
5. Observe the radar display as the servo sweeps and the ultrasonic sensor detects objects.

---

## Notes

- The visualization works best for objects within 0–40 cm.  
- Avoid pointing the sensor at soft or absorbent surfaces, which may not reflect sound reliably.  
- You can adjust the servo sweep angles or speed in the Arduino code to fit your setup.  

---

This project is ideal for beginners learning about Arduino sensors, serial communication and graphical visualization using Processing.
