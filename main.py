import json
import pprint
import uuid
from decimal import Decimal
import random
from typing import List, Dict

from graphs.builder import GraphBuilder
from graphs.dto import Graph
from locations.enums import LocationType
from locations.model import Location
from locations.service import LocationService
from order_matcher.service import OrderMatcher
from orders.model import Order
from orders.service import OrderService
from restaurants.model import Restaurant
from restaurants.service import RestaurantService
from route_finder.dto import RouteDTO
from route_finder.enums import RoutePlanningStrategy
from route_finder.service import RouteFinderFactory, RouteFinder
from users.model import Customer, Rider
from users.service import CustomerService, RiderService
from utils import flatten

PRECISION = Decimal("1.00")


def generate_restaurants_and_locations(count: int):
    for index in range(count):
        name: str = f"RESTAURANT:{index}"
        phone: str = f"RESTAURANT_PHONE:{index}"
        preparation_time: Decimal = Decimal(random.randint(10, 100))
        restaurant: Restaurant = RestaurantService.create(name, phone, preparation_time)
        latitude: Decimal = Decimal(random.uniform(-90.0, 90.0)).quantize(PRECISION)
        longitude: Decimal = Decimal(random.uniform(-180.0, 180.0)).quantize(PRECISION)
        LocationService.create(
            restaurant.id, LocationType.RESTAURANT, longitude, latitude
        )


def generate_customers_and_locations(count: int):
    for index in range(count):
        name: str = f"CUSTOMER:{index}"
        phone: str = f"CUSTOMER_PHONE:{index}"
        customer: Customer = CustomerService.create(name, phone)
        latitude: Decimal = Decimal(random.uniform(-90.0, 90.0)).quantize(PRECISION)
        longitude: Decimal = Decimal(random.uniform(-180.0, 180.0)).quantize(PRECISION)
        LocationService.create(customer.id, LocationType.CUSTOMER, longitude, latitude)


def generate_riders_and_locations(count: int):
    for index in range(count):
        name: str = f"RIDER:{index}"
        phone: str = f"RIDER_PHONE:{index}"
        speed: Decimal = Decimal("20")
        rider: Rider = RiderService.create(name, phone, speed)
        latitude: Decimal = Decimal(random.uniform(-90.0, 90.0)).quantize(PRECISION)
        longitude: Decimal = Decimal(random.uniform(-180.0, 180.0)).quantize(PRECISION)
        LocationService.create(rider.id, LocationType.RIDER, longitude, latitude)


def generate_orders(count: int):
    customers: List[Customer] = CustomerService.get_all()
    restaurants: List[Restaurant] = RestaurantService.get_all()
    for index in range(count):
        customer: Customer = customers[index]
        random_restaurant: Restaurant = random.choice(restaurants)
        OrderService.create(customer.id, random_restaurant.id, Decimal("100"))


def get_customer_restaurant_map(
    orders: List[Order],
) -> Dict[uuid.UUID, List[uuid.UUID]]:
    customer_restaurant_map: Dict[uuid.UUID, List[uuid.UUID]] = {}
    for order in orders:
        customer_id: uuid.UUID = order.customer_id
        restaurant_id: uuid.UUID = order.restaurant_id
        if customer_id not in customer_restaurant_map:
            customer_restaurant_map[customer_id] = []

        customer_restaurant_map[customer_id].append(restaurant_id)

    return customer_restaurant_map


def get_object_name_map(orders: List[Order]) -> Dict[uuid.UUID, str]:
    object_name_map: Dict[uuid.UUID, str] = {}
    for order in orders:
        customer_id: uuid.UUID = order.customer_id
        restaurant_id: uuid.UUID = order.restaurant_id

        object_name_map[customer_id] = CustomerService.get_by_id(customer_id).name
        object_name_map[restaurant_id] = RestaurantService.get_by_id(restaurant_id).name

    return object_name_map


def main():
    generate_restaurants_and_locations(100)
    generate_customers_and_locations(100)
    generate_riders_and_locations(1)
    generate_orders(2)
    customer_restaurant_map: Dict[uuid.UUID, List[uuid.UUID]] = (
        get_customer_restaurant_map(OrderService.get_all())
    )
    rider: Rider = OrderMatcher.match(OrderService.get_all())
    locations: List[Location] = OrderMatcher.get_locations(OrderService.get_all())
    locations.append(LocationService.get_latest_by_object_id(rider.id))

    graph: Graph = GraphBuilder.build(rider, locations)
    route_finder: RouteFinder = RouteFinderFactory.get_route_finder(
        RoutePlanningStrategy.DIJKSTRA_WITH_MASK
    )
    route: RouteDTO = route_finder.find(graph, customer_restaurant_map)
    route_list: List[RouteDTO] = flatten(route)
    route_map = {}
    route_json: list = []
    for r in route_list:
        route_json.append(r.to_dict_without_previous())

    route_map["route"] = route_json
    print(json.dumps(route_map, default=str))


main()
