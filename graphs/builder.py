from decimal import Decimal
from typing import List

from graphs.calculator import DistanceCalculatorFactory, DistanceCalculator
from graphs.dto import NodeDTO, Graph
from graphs.enums import DistanceCalculationStrategy
from graphs.transformer import NodeTransformerFactory, NodeTransformer
from locations.model import Location
from users.model import Rider

PRECISION = Decimal("1.00")


class GraphBuilder:
    @classmethod
    def build(cls, rider: Rider, locations: List[Location]) -> Graph:
        graph = Graph()
        vehicle_speed: Decimal = rider.vehicle_speed
        node_transformer: NodeTransformer = NodeTransformerFactory.get_transformer(
            DistanceCalculationStrategy.HAVERSINE
        )
        distance_calculator: DistanceCalculator = (
            DistanceCalculatorFactory.get_calculator(
                DistanceCalculationStrategy.HAVERSINE
            )
        )
        nodes: List[NodeDTO] = node_transformer.transform_many(locations)
        rider_node: NodeDTO = next(filter(lambda node: node.is_rider(), nodes))
        graph.set_root(rider_node)
        graph.add_nodes(nodes)
        for from_node in nodes:
            for to_node in nodes:
                if from_node != to_node:
                    distance: Decimal = distance_calculator.calculate(
                        from_node, to_node
                    )
                    node_weight: Decimal = distance / vehicle_speed
                    graph.add_edge(from_node, to_node, node_weight.quantize(PRECISION))

        return graph
