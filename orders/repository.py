import uuid
from typing import List
from orders.model import Order


class OrderRepository:
    _order_id_to_order_map = {}
    _customer_id_to_order_ids_map = {}
    _restaurant_id_to_order_ids_map = {}

    @classmethod
    def insert_one(cls, order: Order) -> Order:
        if order.id not in cls._order_id_to_order_map:
            cls._order_id_to_order_map[order.id] = order
            if order.customer_id not in cls._customer_id_to_order_ids_map:
                cls._customer_id_to_order_ids_map[order.customer_id] = []
            cls._customer_id_to_order_ids_map[order.customer_id].append(order.id)
            if order.restaurant_id not in cls._restaurant_id_to_order_ids_map:
                cls._restaurant_id_to_order_ids_map[order.restaurant_id] = []
            cls._restaurant_id_to_order_ids_map[order.restaurant_id].append(order.id)
        else:
            raise Exception("Order id already exists")
        return order

    @classmethod
    def get_by_id(cls, order_id: uuid.UUID) -> Order:
        if order_id not in cls._order_id_to_order_map:
            raise Exception("Order id does not exist")
        return cls._order_id_to_order_map[order_id]

    @classmethod
    def get_by_customer_id(cls, customer_id: uuid.UUID) -> List[Order]:
        order_ids = cls._customer_id_to_order_ids_map.get(customer_id, [])
        return [
            cls._order_id_to_order_map[order_id]
            for order_id in order_ids
            if order_id in cls._order_id_to_order_map
        ]

    @classmethod
    def get_by_restaurant_id(cls, restaurant_id: uuid.UUID) -> List[Order]:
        order_ids = cls._restaurant_id_to_order_ids_map.get(restaurant_id, [])
        return [
            cls._order_id_to_order_map[order_id]
            for order_id in order_ids
            if order_id in cls._order_id_to_order_map
        ]

    @classmethod
    def get_all(cls) -> List[Order]:
        return list(cls._order_id_to_order_map.values())

    @classmethod
    def update(cls, order: Order):
        if order.id not in cls._order_id_to_order_map:
            raise Exception("Order id does not exist")
        cls._order_id_to_order_map[order.id] = order
