import math
from abc import ABC, abstractmethod
from decimal import Decimal

from graphs.dto import NodeDTO, HaversineNode
from graphs.enums import DistanceCalculationStrategy

PRECISION = Decimal("1.00")


class DistanceCalculator(ABC):

    @classmethod
    @abstractmethod
    def calculate(cls, node1: NodeDTO, node2: NodeDTO) -> Decimal:
        pass

    @classmethod
    @abstractmethod
    def get_strategy(cls) -> DistanceCalculationStrategy:
        pass


class HaversineDistanceCalculator(DistanceCalculator):
    EARTH_RADIUS_KM: Decimal = 6371.0

    @classmethod
    def calculate(cls, node1: HaversineNode, node2: HaversineNode) -> Decimal:
        lat1 = float(node1.latitude)
        lat2 = float(node2.latitude)
        lon1 = float(node1.longitude)
        lon2 = float(node2.longitude)

        d_lat = (lat2 - lat1) * math.pi / 180.0
        d_lon = (lon2 - lon1) * math.pi / 180.0

        lat1 = lat1 * math.pi / 180.0
        lat2 = lat2 * math.pi / 180.0

        a = pow(math.sin(d_lat / 2), 2) + pow(math.sin(d_lon / 2), 2) * math.cos(
            lat1
        ) * math.cos(lat2)

        c = 2 * math.asin(math.sqrt(a))
        return Decimal(cls.EARTH_RADIUS_KM * c).quantize(PRECISION)

    @classmethod
    def get_strategy(cls) -> DistanceCalculationStrategy:
        return DistanceCalculationStrategy.HAVERSINE


class DistanceCalculatorFactory:
    _CALCULATION_STRATEGY_TO_CALCULATOR = {
        DistanceCalculationStrategy.HAVERSINE: HaversineDistanceCalculator(),
    }

    @classmethod
    def get_calculator(
        cls, strategy: DistanceCalculationStrategy
    ) -> DistanceCalculator:
        return cls._CALCULATION_STRATEGY_TO_CALCULATOR.get(strategy)
