# AEROSAR System Boundaries & Safety Architecture

## 1. Safety Boundary: Read vs. Command
* **Read-only Systems:** Dashboard, CV, RAG, LLM, Database, Visualization.
* **Command-Capable Layer:** Navigation Manager, MAVLink Gateway.
* **Strict Rule:** The LLM and Dashboard **cannot** directly send arbitrary MAVLink packets or bypass the Path Validator. Only the validated Navigation Manager can request high-level vehicle mode changes or waypoints.

## 2. Vehicle Communication Boundary
```text
ArduPilot
   ↓ (MAVLink over UART)
Raspberry Pi
```
*ArduPilot retains absolute authority over stabilization, RC overrides, battery failsafes, and exact motor signals.*

## 3. Network Communication Boundary
```text
Raspberry Pi
   ↓ (TCP over Wi-Fi/LTE)
Offboard Computer (Ground Station)
```

## 4. Perception Boundary
```text
Camera
   ↓
Raspberry Pi
   ↓ (TCP)
Ground Station (PC)
   ↓
OpenCV + YOLO (Detections)
   ↓
Incident Engine
```
*The Pi is a data pipe; heavy lifting is offboard.*

## 5. Robotics Boundary
```text
VehicleState (Source of Truth)
   ↓
ROS 2
   ↓
Localization → SLAM → Mapping → Path Planning → Navigation
```
*ROS handles spatial intelligence, separated from raw parsing.*

## 6. Intelligence Boundary
```text
Incident Engine
   ↓
Database
   ↓
RAG
   ↓
LLM
```

## 7. Data Freshness & Graceful Degradation
- If data becomes too old, it is marked `STALE`.
- Subsystems expose states (`AVAILABLE`, `UNAVAILABLE`, `STALE`).
- If RAG/LLM fails, CV and Telemetry continue.
- If CV fails, Telemetry and ROS continue.
- If ROS is unavailable, `VehicleState` TCP streaming and the Dashboard continue uninterrupted.
