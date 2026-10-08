"""
navigation_status.py

Defines standard statuses for the AEROSAR navigation stack.
"""

class NavigationStatus:
    IDLE = "IDLE"
    WAITING_FOR_INPUTS = "WAITING_FOR_INPUTS"
    READY = "READY"
    PLANNING = "PLANNING"
    PATH_READY = "PATH_READY"
    NAVIGATING = "NAVIGATING"
    PAUSED = "PAUSED"
    GOAL_REACHED = "GOAL_REACHED"
    CANCELLED = "CANCELLED"
    FAILED = "FAILED"
    SAFETY_HOLD = "SAFETY_HOLD"
