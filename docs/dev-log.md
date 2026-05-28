# Dev Log

## Phase 3A — Basic Servo Control

### Objective
Verify Arduino can control MG90S servo through PWM.

### Wiring
- Brown -> GND
- Red -> 5V
- Yellow -> Pin 9

### Result
Successfully rotated servo between 0 deg, 90 deg, and 180 deg.

### Observations
- Servo movement is stable
- No power instability observed
- Arduino USB power sufficient for single servo

# Phase 3B — Python Serial Communication

## Objective
Control MG90S servo directly from Python through USB serial communication.

## Architecture

Python
↓
PySerial
↓
USB Serial
↓
Arduino
↓
PWM Signal
↓
Servo

## Communication Protocol
- Baud rate: 9600
- Data format: newline-delimited angle values

## Result
Successfully transmitted angle commands from Python to Arduino.

## Observations
- Servo response nearly instantaneous
- Serial communication stable
- Angle constraints functioning correctly

# Phase 4 — AI-Controlled Servo Tracking

## Objective
Integrate the computer vision tracking system with the servo control pipeline so that detected target movement physically controls servo rotation.

## System Architecture

Camera
↓
OpenCV Video Capture
↓
YOLOv8 Person Detection
↓
Target Selection
↓
Tracking Error Calculation
↓
Exponential Smoothing
↓
Python Control Logic
↓
PySerial Communication
↓
Arduino Serial Receiver
↓
PWM Servo Signal
↓
MG90S Servo Rotation

## Tracking Logic

The system calculates the horizontal distance between:

* screen center
* detected target center

This value becomes the tracking error.

Positive horizontal error:

* target is right of center
* servo should rotate right

Negative horizontal error:

* target is left of center
* servo should rotate left

## Control System Concept

The servo angle acts as the actuator output.

The tracking error acts as the control input.

The system continuously:

1. detects target position
2. computes error
3. adjusts servo angle
4. physically repositions camera

This forms a basic closed-loop control system.

## Planned Implementation

### Step 1

Mount webcam onto pan assembly.

### Step 2

Send servo angle commands automatically from Python.

### Step 3

Map tracking error to servo angle adjustments.

### Step 4

Tune smoothing and responsiveness.

## Engineering Concepts Learned

* Computer vision inference
* Real-time frame processing
* Serial communication
* PWM servo control
* Embedded systems integration
* Closed-loop control systems
* Hardware/software interaction

## Mechanical Integration Notes

### Bracket Compatibility Issue
The purchased pan bracket was designed for MG996R-class servos, while the current project uses MG90S micro servos.

### Issue Observed
The included metal hub adapter did not fit the MG90S servo shaft, indicating a spline and mounting compatibility mismatch.

### Resolution
Used the MG90S-compatible cross horn attachment as the mechanical interface between the servo shaft and the bracket.

### Engineering Takeaway
This highlighted the importance of checking servo spline size, mounting dimensions, torque requirements, and mechanical compatibility before selecting hardware.

## Future Improvements

* Dual-axis pan-tilt tracking
* PID control
* Raspberry Pi edge deployment
* Multi-object tracking
* Autonomous target prediction
* ROS2 integration
* Edge AI optimization