from abc import ABC, abstractmethod
from decimal import Decimal
from typing import List
import uuid

from graphs.dto import NodeDTO, HaversineNode
from graphs.enums import DistanceCalculationStrategy
from locations.model import Location
from restaurants.service import RestaurantService


class NodeTransformer(ABC):
    @classmethod
    @abstractmethod
    def transform_one(cls, location: Location) -> NodeDTO:
        pass

    @classmethod
    @abstractmethod
    def transform_many(cls, locations: List[Location]) -> List[NodeDTO]:
        pass

    @classmethod
    @abstractmethod
    def get_strategy(cls) -> DistanceCalculationStrategy:
        pass


class HaversineNodeTransformer(NodeTransformer):
    @classmethod
    def transform_one(cls, location: Location) -> HaversineNode:
        min_available_time = Decimal("0")
        if location.is_restaurant():
            min_available_time = RestaurantService.get_by_id(
                location.get_object_id()
            ).avg_preparation_time

        return HaversineNode(
            object_id=location.object_id,
            latitude=location.latitude,
            longitude=location.longitude,
            min_available_time=min_available_time,
            node_type=location.get_location_type(),
        )

    @classmethod
    def transform_many(cls, locations: List[Location]) -> List[HaversineNode]:
        return [cls.transform_one(location) for location in locations]

    @classmethod
    def get_strategy(cls) -> DistanceCalculationStrategy:
        return DistanceCalculationStrategy.HAVERSINE


class NodeTransformerFactory:
    _STRATEGY_TO_TRANSFORMER = {
        DistanceCalculationStrategy.HAVERSINE: HaversineNodeTransformer(),
    }

    @classmethod
    def get_transformer(cls, strategy: DistanceCalculationStrategy) -> NodeTransformer:
        return cls._STRATEGY_TO_TRANSFORMER.get(strategy)
