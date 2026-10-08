# AEROSAR Integration Matrix (Step 7)

This matrix defines the inputs, outputs, and dependencies of every major subsystem in the AEROSAR project. It strictly enforces the boundary between real-time ROS control and the asynchronous UI/Intelligence layers.

| Component       | Input          | Output            | Real Data Required | ROS Required |
| --------------- | -------------- | ----------------- | ------------------ | ------------ |
| **MAVLink Gateway**| ArduPilot (FC)| Telemetry Stream  | Yes                | No           |
| **TCP Layer**   | Network Link   | Serialized Data   | Yes                | No           |
| **VehicleState**| MAVLink stream | Normalized state  | Yes                | No           |
| **Camera**      | Physical Lens  | Video Frames      | Yes                | No           |
| **YOLO / CV**   | Video Frames   | Detections        | Yes                | No           |
| **Incident Eng.**| Detections    | Structured Incidents| Yes              | No           |
| **Localization**| Sensors/State  | Pose (odom)       | Yes                | Yes          |
| **SLAM**        | Sensors/Pose   | Map / Pose refine | Yes                | Yes          |
| **Path Planner**| Pose/Map/Goal  | Path              | Yes                | Yes          |
| **Navigation**  | Validated Path | Command requests  | Yes                | Yes          |
| **Database**    | Processed Data | Storage/History   | Yes                | No           |
| **RAG**         | Knowledge Base | Retrieval Context | Yes                | No           |
| **LLM**         | Context/Prompt | Intelligence      | Yes                | No           |
| **Dashboard**   | System outputs | UI Visualization  | Yes                | No           |
