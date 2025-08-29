import uuid
from datetime import datetime
from decimal import Decimal
from typing import List

from locations.enums import LocationType
from locations.model import Location
from locations.repository import LocationRepository


class LocationService:
    @classmethod
    def create(
        cls,
        object_id: uuid.UUID,
        location_type: LocationType,
        longitude: Decimal,
        latitude: Decimal,
    ) -> Location:
        location = Location()
        location.set_object_id(object_id)
        location.set_location_type(location_type)
        location.set_timestamp(datetime.now())
        location.set_longitude(longitude)
        location.set_latitude(latitude)
        LocationRepository.insert_one(location)
        return location

    @classmethod
    def get_by_id(cls, location_id: uuid.UUID) -> Location:
        return LocationRepository.get_by_id(location_id)

    @classmethod
    def get_by_object_id(cls, object_id: uuid.UUID) -> List[Location]:
        return LocationRepository.get_by_object_id(object_id)

    @classmethod
    def get_latest_by_object_id(cls, object_id: uuid.UUID) -> Location:
        locations = LocationRepository.get_by_object_id(object_id)
        if not locations:
            raise Exception("No locations found for the given object id")
        return max(locations, key=lambda loc: loc.timestamp)
