import uuid
import threading
from decimal import Decimal

from restaurants.enums import RestaurantStatus

class Restaurant:
    id: uuid.UUID
    name: str
    phone: str
    status: RestaurantStatus
    avg_preparation_time: Decimal
    lock: threading.Lock

    def __init__(self):
        self.id = uuid.uuid4()
        self.status = RestaurantStatus.ACTIVE
        self.lock = threading.Lock()

    def set_name(self, name: str):
        self.name = name

    def set_phone(self, phone: str):
        self.phone = phone

    def set_status(self, status: RestaurantStatus):
        self.status = status

    def set_avg_preparation_time(self, avg_preparation_time: Decimal):
        self.avg_preparation_time = avg_preparation_time

    def get_avg_preparation_time(self):
        return self.avg_preparation_time

    def __repr__(self):
        return str(self.__dict__)