import uuid
from typing import List

from restaurants.model import Restaurant


class RestaurantRepository:
    _restaurant_id_to_restaurant_map = {}

    @classmethod
    def insert_one(cls, restaurant: Restaurant) -> Restaurant:
        if restaurant.id not in cls._restaurant_id_to_restaurant_map:
            cls._restaurant_id_to_restaurant_map[restaurant.id] = restaurant
        else:
            raise Exception("Restaurant id already exists")
        return restaurant

    @classmethod
    def get_by_id(cls, restaurant_id: uuid.UUID) -> Restaurant:
        if restaurant_id not in cls._restaurant_id_to_restaurant_map:
            raise Exception("Restaurant id does not exist")
        return cls._restaurant_id_to_restaurant_map[restaurant_id]

    @classmethod
    def get_all(cls) -> List[Restaurant]:
        return list(cls._restaurant_id_to_restaurant_map.values())

    @classmethod
    def update(cls, restaurant: Restaurant):
        if restaurant.id not in cls._restaurant_id_to_restaurant_map:
            raise Exception("Restaurant id does not exist")
        cls._restaurant_id_to_restaurant_map[restaurant.id] = restaurant
