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