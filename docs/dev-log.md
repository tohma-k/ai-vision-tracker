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

Python -> PySerial -> USB Serial -> Arduino -> PWM Signal -> Servo

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

![Architecture](architecture.png)

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
The included metal hub adapter did not fit the MG90S servo shaft, indicating a spline and mounting compatibility mismatch between the bracket hardware and the selected actuator.

### Resolution
Used the MG90S-compatible cross horn attachment as the rotational interface between the servo shaft and the pan bracket.

### Engineering Takeaway
This highlighted the importance of validating:
- servo spline compatibility
- mounting dimensions
- torque requirements
- mechanical interface standards
before hardware procurement and integration.

## Prototype Mechanical Coupling

### Issue
The included bracket mounting hardware remained mechanically incompatible with the MG90S spline geometry and mounting pattern.

### Temporary Solution
Implemented a temporary horn-to-bracket fixture using adhesive mounting techniques to rapidly prototype rotational movement prior to designing a permanent mechanical interface.

### Result
The assembly achieved:
- stable rotational motion
- smooth servo actuation
- acceptable mechanical rigidity
- reliable bracket movement during sweep testing

### Motion Characteristics
- MG90S torque proved sufficient for single-axis bracket rotation
- Rotational movement remained smooth under light load
- No major oscillation or instability observed during testing
- Servo response remained consistent under Arduino USB power

### Engineering Takeaway
Rapid prototyping enabled validation of:
- actuator performance
- control behavior
- rotational stability
- mechanical feasibility
before investing additional time into mechanical refinement.

### Control Direction Calibration
Initial testing showed the pan servo moved opposite the target direction due to the physical mounting orientation. Reversed the servo angle update sign to align software control logic with the mechanical assembly.

### Tracking Stability Tuning
Initial AI-controlled tracking produced jagged servo motion due to detection noise and overly frequent control updates. Increased the deadzone, reduced proportional gain, and added a servo update interval to smooth physical movement.

### Runtime Performance
- System operated at approximately 8 FPS during real-time person tracking
- Frame rate sufficient for low-speed servo actuation and proof-of-concept autonomous tracking
- CPU inference identified as the primary performance bottleneck

### Current Limitations
- Motion is functional but still slightly jagged
- Single-axis pan tracking only
- Temporary taped horn-to-bracket coupling
- No external servo power yet

## Future Improvements

* Dual-axis pan-tilt tracking
* PID control
* Raspberry Pi edge deployment
* Multi-object tracking
* Autonomous target prediction
* ROS2 integration
* Edge AI optimization

## Phase 5 — Proportional Control Tuning

### Objective
Improve tracking smoothness by replacing fixed-step servo movement with proportional control.

### Result
Servo movement became more responsive to large target errors while reducing excessive movement near the center.

### Parameters Tested
- Deadzone: 60 pixels
- Proportional gain: 0.015
- Servo update interval: 0.10 seconds
- Smoothing alpha: 0.13

### Other Optimizations
- Reduced YOLO inference load by resizing camera input to 640×480, improving real-time tracking performance by roughly 25% from ~8 FPS to ~10 FPS.
- Implemented threaded webcam capture to separate video acquisition from the tracking loop, but the runtime performance decreased from 10 to 8 FPS, likely due to thread overhead and frame copying while YOLO inference remained the primary bottleneck. Reverted to direct OpenCV frame capture.
- Reduced YOLO's inference image size. imgsz=320: 10 to 20~ FPS, no significant degradation in person detection quality during testing.

## Phase 6 — Dual-Axis Servo Control

### Objective
Extend the single-axis tracking system to support pan and tilt control using two MG90S servos.

### Hardware Update
- Pan servo connected to Arduino pin 9
- Tilt servo connected to Arduino pin 10
- Both servos share Arduino 5V and GND during prototype testing

### Result
Successfully controlled pan and tilt servos through comma-separated serial commands from Python.

### Serial Protocol
Format: `pan,tilt`
Example: `90,120`

### Mechanical Scaling Limitation
The initial prototype successfully validated AI-controlled tracking using MG90S servos and a temporary mounting solution. As the system expanded to dual-axis pan-tilt tracking, mechanical rigidity became the primary limitation. Future revisions will use actuators designed for the bracket interface to improve load capacity and mounting stability.

### Mechanical Update
Purchased a pair of MG996Rs. The brackets fit perfectly with the new servos. Also purchased a 5V 5A AC to DC power supply with a female terminal connector for sufficient power supply for the two servos.

### Hardware Updates
- Replaced MG90s servos with MG996R high-torque servos.
- Added dedicated external sservo power supply.
- Mounted webcam onto pan-tilt assembly.
- Integrated pan and tilt axes into one platform.

### Wiring

#### Pan Servo

| Servo Wire | Connection |
|------------|------------|
| Red | External 5V Supply |
| Brown | Common GND |
| Orange | Arduino Pin 9 |

#### Tilt Servo

| Servo Wire | Connection |
|------------|------------|
| Red | External 5V Supply |
| Brown | Common GND |
| Orange | Arduino Pin 10 |

#### Arduino

| Pin | Connection |
|------|-----------|
| GND | Common Ground Rail |
| Pin 9 | Pan Servo Signal |
| Pin 10 | Tilt Servo Signal |
| USB | Laptop |

#### Power Supply

| Terminal | Connection |
|-----------|-----------|
| +5V | Servo Power Rail |
| GND | Common Ground Rail |

### Validation Results
- Verified smooth pan and tilt movement under webcam load.
- Confirmed external power supply provided sufficient current for dual-servo operation.
- Observed stable operation without brownouts, resets, or unexpected servo behavior.

### Software Updates
- Updated angle contraints to prevent:
    - tilt bracket collisions with base assembly.
    - Camera interference with the mounting structure.
    - Excessive movement that could destabilize the platform.