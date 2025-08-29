import json
import uuid
from dataclasses import dataclass
from decimal import Decimal
from typing import List, Dict

from locations.enums import LocationType

PRECISION = Decimal("1.00")


@dataclass(frozen=True)
class NodeDTO:
    object_id: uuid.UUID
    node_type: LocationType
    min_available_time: Decimal

    def is_customer(self):
        return self.node_type == LocationType.CUSTOMER

    def is_restaurant(self):
        return self.node_type == LocationType.RESTAURANT

    def is_rider(self):
        return self.node_type == LocationType.RIDER

    def to_dict(self):
        return self.__dict__

    def __eq__(self, other):
        return isinstance(other, NodeDTO) and self.object_id == other.object_id


@dataclass(frozen=True)
class HaversineNode(NodeDTO):
    latitude: Decimal
    longitude: Decimal

    def __hash__(self):
        return hash((self.object_id, self.latitude, self.longitude))

    def __eq__(self, other):
        return (
            self.latitude == other.latitude
            and self.longitude == other.longitude
            and super().__eq__(other)
        )

    def to_dict(self):
        return {
            "latitude": self.latitude.quantize(PRECISION),
            "longitude": self.longitude.quantize(PRECISION),
            "object_id": self.object_id,
            "node_type": self.node_type.value,
            "min_available_time": self.min_available_time.quantize(PRECISION),
        }


@dataclass
class NodeEdge:
    from_node: NodeDTO
    to_node: NodeDTO
    weight: Decimal

    def __str__(self):
        return f"From Node: {self.from_node.object_id}, To Node: {self.to_node.object_id}, Weight: {self.weight}"


class Graph:
    def __init__(self):
        self.root = None
        self.nodes: List[NodeDTO] = []
        self.edge_map: Dict[NodeDTO, List[NodeEdge]] = {}

    def set_root(self, root: NodeDTO):
        self.root = root

    def get_customer_nodes(self):
        return list(filter(lambda node: node.is_customer(), self.nodes))

    def get_restaurant_nodes(self):
        return list(filter(lambda node: node.is_restaurant(), self.nodes))

    def get_nodes(self):
        return self.nodes

    def add_node(self, node: NodeDTO):
        self.nodes.append(node)

    def add_nodes(self, nodes: List[NodeDTO]):
        self.nodes.extend(nodes)

    def add_edge(self, from_node: NodeDTO, to_node: NodeDTO, weight: Decimal):
        if from_node not in self.edge_map:
            self.edge_map[from_node] = []

        self.edge_map[from_node].append(NodeEdge(from_node, to_node, weight))

    def get_edges(self, node: NodeDTO) -> List[NodeEdge]:
        return self.edge_map[node]
