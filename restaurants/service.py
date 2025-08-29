import uuid
from decimal import Decimal
from typing import List

from restaurants.enums import RestaurantStatus
from restaurants.model import Restaurant
from restaurants.repository import RestaurantRepository


class RestaurantService:
    @classmethod
    def create(cls, name: str, phone: str, preparation_time: Decimal) -> Restaurant:
        restaurant = Restaurant()
        restaurant.set_name(name)
        restaurant.set_phone(phone)
        restaurant.set_status(RestaurantStatus.ACTIVE)
        restaurant.set_avg_preparation_time(preparation_time)
        RestaurantRepository.insert_one(restaurant)
        return restaurant

    @classmethod
    def get_by_id(cls, restaurant_id: uuid.UUID) -> Restaurant:
        return RestaurantRepository.get_by_id(restaurant_id)

    @classmethod
    def get_all(cls) -> List[Restaurant]:
        return RestaurantRepository.get_all()
