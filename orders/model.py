import uuid
import threading
from datetime import datetime
from decimal import Decimal
from orders.enums import OrderStatus


class Order:
    id: uuid.UUID
    customer_id: uuid.UUID
    restaurant_id: uuid.UUID
    amount: Decimal
    placed_at: datetime
    status: OrderStatus
    lock: threading.Lock

    def __init__(self):
        self.id = uuid.uuid4()
        self.status = OrderStatus.PENDING
        self.lock = threading.Lock()

    def set_customer_id(self, customer_id: uuid.UUID):
        self.customer_id = customer_id

    def set_restaurant_id(self, restaurant_id: uuid.UUID):
        self.restaurant_id = restaurant_id

    def set_amount(self, amount: Decimal):
        self.amount = amount

    def set_placed_at(self, placed_at: datetime):
        self.placed_at = placed_at

    def set_status(self, status: OrderStatus):
        self.status = status

    def __repr__(self):
        return f"ID: {self.id}, CUSTOMER_ID: {self.customer_id}, RESTAURANT_ID: {self.restaurant_id}, AMOUNT: {self.amount}\n"
