import uuid
from datetime import datetime
from decimal import Decimal
from typing import List

from orders.enums import OrderStatus
from orders.model import Order
from orders.repository import OrderRepository

class OrderService:
    @classmethod
    def create(cls, customer_id: uuid.UUID, restaurant_id: uuid.UUID, amount: Decimal) -> Order:
        order = Order()
        order.set_customer_id(customer_id)
        order.set_restaurant_id(restaurant_id)
        order.set_amount(amount)
        order.set_placed_at(datetime.now())
        order.set_status(OrderStatus.PENDING)
        OrderRepository.insert_one(order)
        return order

    @classmethod
    def get_by_id(cls, order_id: uuid.UUID) -> Order:
        return OrderRepository.get_by_id(order_id)

    @classmethod
    def get_by_customer_id(cls, customer_id: uuid.UUID) -> List[Order]:
        return OrderRepository.get_by_customer_id(customer_id)

    @classmethod
    def get_by_restaurant_id(cls, restaurant_id: uuid.UUID) -> List[Order]:
        return OrderRepository.get_by_restaurant_id(restaurant_id)

    @classmethod
    def get_all(cls) -> List[Order]:
        return list(
            OrderRepository.get_all()
        )