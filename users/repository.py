import uuid
from typing import List
from users.model import Customer, Rider

class CustomerRepository:
    _customer_id_to_customer_map = {}

    @classmethod
    def insert_one(cls, customer: Customer) -> Customer:
        if customer.id not in cls._customer_id_to_customer_map:
            cls._customer_id_to_customer_map[customer.id] = customer
        else:
            raise Exception('Customer id already exists')
        return customer

    @classmethod
    def get_by_id(cls, customer_id: uuid.UUID) -> Customer:
        if customer_id not in cls._customer_id_to_customer_map:
            raise Exception('Customer id does not exist')
        return cls._customer_id_to_customer_map[customer_id]

    @classmethod
    def get_all(cls) -> List[Customer]:
        return list(
            cls._customer_id_to_customer_map.values()
        )

    @classmethod
    def update(cls, customer: Customer):
        cls._customer_id_to_customer_map[customer.id] = customer

class RiderRepository:
    _rider_id_to_rider_map = {}

    @classmethod
    def insert_one(cls, rider: Rider) -> Rider:
        if rider.id not in cls._rider_id_to_rider_map:
            cls._rider_id_to_rider_map[rider.id] = rider
        else:
            raise Exception('Rider id already exists')
        return rider

    @classmethod
    def get_by_id(cls, rider_id: uuid.UUID) -> Rider:
        if rider_id not in cls._rider_id_to_rider_map:
            raise Exception('Rider id does not exist')
        return cls._rider_id_to_rider_map[rider_id]

    @classmethod
    def update(cls, rider: Rider):
        cls._rider_id_to_rider_map[rider.id] = rider

    @classmethod
    def get_all(cls) -> List[Rider]:
        return list(
            cls._rider_id_to_rider_map.values()
        )