from enum import Enum


class RoutePlanningStrategy(Enum):
    ALL_POSSIBLE_PATHS = "All Possible Paths"
    DIJKSTRA_WITH_MASK = "Dijkstra With Mask"
