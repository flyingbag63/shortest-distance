import uuid
from typing import List, Set

from locations.model import Location
from locations.service import LocationService
from users.model import Rider
from users.service import RiderService
from orders.model import Order


class OrderMatcher:
    @classmethod
    def match(cls, orders: List[Order]) -> Rider:
        active_riders = RiderService.get_active_riders()
        if not active_riders:
            raise Exception("No active riders available")
        return active_riders[0]

    @classmethod
    def get_locations(cls, orders: List[Order]) -> List[Location]:
        locations: Set[Location] = set()
        for order in orders:
            customer_id: uuid.UUID = order.customer_id
            restaurant_id: uuid.UUID = order.restaurant_id
            locations.add(LocationService.get_latest_by_object_id(customer_id))
            locations.add(LocationService.get_latest_by_object_id(restaurant_id))

        return list(locations)
