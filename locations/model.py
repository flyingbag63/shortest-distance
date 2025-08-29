import uuid
import threading
from datetime import datetime
from decimal import Decimal

from locations.enums import LocationType


class Location:
    id: uuid.UUID
    object_id: uuid.UUID
    location_type: LocationType
    timestamp: datetime
    longitude: Decimal
    latitude: Decimal
    lock: threading.Lock

    def __init__(self):
        self.id = uuid.uuid4()
        self.lock = threading.Lock()

    def set_object_id(self, object_id: uuid.UUID):
        self.object_id = object_id

    def set_location_type(self, location_type: LocationType):
        self.location_type = location_type

    def set_timestamp(self, timestamp: datetime):
        self.timestamp = timestamp

    def set_longitude(self, longitude: Decimal):
        self.longitude = longitude

    def set_latitude(self, latitude: Decimal):
        self.latitude = latitude

    def __repr__(self):
        return str(self.__dict__)

    def is_restaurant(self):
        return self.location_type == LocationType.RESTAURANT

    def get_object_id(self):
        return self.object_id

    def get_location_type(self):
        return self.location_type

    def get_timestamp(self):
        return self.timestamp
