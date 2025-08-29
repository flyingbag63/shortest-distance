from typing import List

from route_finder.dto import RouteDTO


def flatten(route: RouteDTO) -> List[RouteDTO]:
    route_list: List[RouteDTO] = []
    while route:
        route_list.append(route)
        route = route.previous_route

    route_list.reverse()
    return route_list
