import uuid
from decimal import Decimal
from typing import List

from users.enums import UserStatus
from users.model import Customer, Rider
from users.repository import CustomerRepository, RiderRepository

class CustomerService:
    @classmethod
    def create(cls, name: str, phone: str) -> Customer:
        customer = Customer()
        customer.set_name(name)
        customer.set_phone(phone)
        customer.set_status(UserStatus.ACTIVE)
        CustomerRepository.insert_one(customer)
        return customer

    @classmethod
    def get_by_id(cls, customer_id: uuid.UUID) -> Customer:
        return CustomerRepository.get_by_id(customer_id)

    @classmethod
    def get_all(cls) -> List[Customer]:
        return CustomerRepository.get_all()

class RiderService:
    @classmethod
    def create(cls, name: str, phone: str, vehicle_speed: Decimal) -> Rider:
        rider = Rider()
        rider.set_name(name)
        rider.set_phone(phone)
        rider.set_vehicle_speed(vehicle_speed)
        rider.set_status(UserStatus.ACTIVE)
        RiderRepository.insert_one(rider)
        return rider

    @classmethod
    def get_by_id(cls, rider_id: uuid.UUID) -> Rider:
        return RiderRepository.get_by_id(rider_id)

    @classmethod
    def get_active_riders(cls) -> List[Rider]:
        return [
            rider for rider in RiderRepository.get_all()
            if rider.status == UserStatus.ACTIVE
        ]