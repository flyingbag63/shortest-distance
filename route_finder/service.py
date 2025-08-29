import heapq
import uuid
from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Set, List, Dict, Optional

from graphs.dto import Graph, NodeDTO
from route_finder.dto import RouteDTO, DijkstraNode
from route_finder.enums import RoutePlanningStrategy


class RouteFinder(ABC):
    @classmethod
    @abstractmethod
    def get_strategy(cls) -> RoutePlanningStrategy:
        pass

    @classmethod
    @abstractmethod
    def find(cls, graph: Graph, customer_restaurant_map: Dict[uuid.UUID, List[uuid.UUID]]) -> RouteDTO:
        pass

    @classmethod
    def _get_object_index_map(cls, restaurant_nodes: List[NodeDTO]) -> Dict[NodeDTO, int]:
        restaurant_index_map: Dict[NodeDTO, int] = {}
        for index, node in enumerate(restaurant_nodes):
            restaurant_index_map[node] = index

        return restaurant_index_map

    @classmethod
    def _get_object_node_map(cls, nodes: List[NodeDTO]) -> Dict[uuid.UUID, NodeDTO]:
        object_node_map: Dict[uuid.UUID, NodeDTO] = {}
        for node in nodes:
            object_node_map[node.object_id] = node

        return object_node_map


class DijkstraWithMaskRouteFinder(RouteFinder):
    @classmethod
    def get_strategy(cls):
        return RoutePlanningStrategy.DIJKSTRA_WITH_MASK

    @classmethod
    def find(cls, graph: Graph, customer_restaurant_map: Dict[uuid.UUID, List[uuid.UUID]]) -> RouteDTO:
        root: NodeDTO = graph.root
        root_node = DijkstraNode(
            root, Decimal("0"), 0
        )
        nodes: List[NodeDTO] = (
            graph.get_customer_nodes() +
            graph.get_restaurant_nodes()
        )
        object_index_map: Dict[NodeDTO, int] = cls._get_object_index_map(nodes)
        object_node_map: Dict[uuid.UUID, NodeDTO] = cls._get_object_node_map(nodes)

        heap = []
        heapq.heappush(heap, (root_node, RouteDTO(root_node, Decimal("0"), None)))
        visited: Set[DijkstraNode] = set()
        best_route: Optional[RouteDTO] = None

        while heap:
            dijkstra_node, route_till_here = heapq.heappop(heap)
            if dijkstra_node in visited:
                continue

            visited.add(dijkstra_node)

            if cls._is_complete(graph, dijkstra_node):
                best_route = route_till_here
                break

            for edge in graph.get_edges(dijkstra_node.get_node()):
                to_node: NodeDTO = edge.to_node
                cost: Decimal = edge.weight
                mask: int = dijkstra_node.get_mask()
                new_cost: Optional[Decimal] = None
                if to_node.is_customer() and cls._all_restaurants_visited(
                    customer_restaurant_map.get(to_node.object_id, []), mask,
                    object_node_map, object_index_map
                ):
                    customer_index = object_index_map[to_node]
                    new_cost: Decimal = dijkstra_node.get_cost() + cost
                    mask |= (1 << customer_index)
                elif to_node.is_restaurant():
                    restaurant_index = object_index_map[to_node]
                    min_available_time: Decimal = to_node.min_available_time
                    new_cost: Decimal = max(
                        min_available_time,
                        dijkstra_node.get_cost() + cost
                    )
                    mask |= (1 << restaurant_index)

                if new_cost is not None:
                    to_dijkstra_node: DijkstraNode = DijkstraNode(
                        to_node,
                        new_cost,
                        mask
                    )
                    new_route: RouteDTO = RouteDTO(
                        to_dijkstra_node,
                        to_dijkstra_node.get_cost(),
                        previous_route=route_till_here
                    )
                    heapq.heappush(heap, (to_dijkstra_node, new_route))

        return best_route

    @classmethod
    def _all_restaurants_visited(
            cls, required_restaurants: List[uuid.UUID], mask: int,
            object_node_map: Dict[uuid.UUID, NodeDTO], restaurant_index_map: Dict[NodeDTO, int]
    ) -> bool:
        return all(
            map(
                lambda index: mask & (1 << index),
                [
                    restaurant_index_map[object_node_map[restaurant]]
                    for restaurant in required_restaurants
                ]
            )
        )

    @classmethod
    def _is_complete(cls, graph: Graph, node: DijkstraNode) -> bool:
        n = len(graph.nodes) - 1
        return node.mask & ((1 << n) - 1) == (1 << n) - 1


class RouteFinderFactory:
    _STRATEGY_TO_ROUTE_FINDER = {
        RoutePlanningStrategy.DIJKSTRA_WITH_MASK: DijkstraWithMaskRouteFinder(),
    }

    @classmethod
    def get_route_finder(cls, strategy: RoutePlanningStrategy) -> RouteFinder:
        return cls._STRATEGY_TO_ROUTE_FINDER.get(strategy)
