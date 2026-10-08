"""
goal_interface.py

Architectural placeholder for a mission goal.
Supports: NO_GOAL, GOAL_RECEIVED, GOAL_VALID, GOAL_INVALID, GOAL_REACHED, GOAL_CANCELLED
"""

class MissionGoal:
    def __init__(self):
        self.state = "NO_GOAL"
        self.target_position = None
        self.target_altitude = None
        self.target_frame = None
        self.position_tolerance = None
        self.altitude_tolerance = None
        self.mission_priority = None
        self.timestamp = None
