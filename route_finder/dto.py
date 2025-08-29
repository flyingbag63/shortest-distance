import json
from abc import ABC
from dataclasses import dataclass
from decimal import Decimal
from typing import Optional

from graphs.dto import NodeDTO


class TraversalNode(ABC):
    pass


class DijkstraNode(TraversalNode):
    def __init__(self, node: NodeDTO, cost: Decimal, mask: int):
        self.node = node
        self.cost = cost
        self.mask = mask

    def __lt__(self, other: "DijkstraNode") -> bool:
        return (
                self.cost < other.cost or
                (self.cost == other.cost and self.mask < other.mask)
        )

    def get_mask(self) -> int:
        return self.mask

    def get_cost(self) -> Decimal:
        return self.cost

    def get_node(self) -> NodeDTO:
        return self.node

    def __hash__(self) -> int:
        return hash((self.node, self.mask))

    def __eq__(self, other: "DijkstraNode") -> bool:
        return self.node == other.node and self.mask == other.mask

    def to_dict(self):
        return {
            **self.node.to_dict(),
            "cost": self.cost,
            "mask": self.mask,
        }


@dataclass
class RouteDTO:
    node: TraversalNode
    cost_till_here: Decimal
    previous_route: Optional["RouteDTO"]

    def __lt__(self, other: "RouteDTO") -> bool:
        return self.cost_till_here < other.cost_till_here

    def to_dict(self):
        return {
            "node": self.node,
            "cost_till_here": self.cost_till_here,
            "previous_route": self.previous_route.to_dict() if self.previous_route else None,
        }

    def to_dict_without_previous(self):
        return {
            "node": self.node.to_dict(),
            "cost_till_here": self.cost_till_here
        }