import uuid
import threading
from decimal import Decimal

from users.enums import UserStatus


class User:
    id: uuid.UUID
    name: str
    phone: str
    status: UserStatus
    lock: threading.Lock

    def __init__(self):
        self.id = uuid.uuid4()
        self.status = UserStatus.ACTIVE
        self.lock = threading.Lock()

    def set_name(self, name: str):
        self.name = name

    def set_phone(self, phone: str):
        self.phone = phone

    def set_status(self, status: UserStatus):
        self.status = status

    def __repr__(self):
        return str(self.__dict__)


class Customer(User):
    def __init__(self):
        super().__init__()


class Rider(User):
    vehicle_speed: Decimal

    def __init__(self):
        super().__init__()
        self.vehicle_speed = Decimal("0")

    def set_vehicle_speed(self, vehicle_speed: Decimal):
        self.vehicle_speed = vehicle_speed
