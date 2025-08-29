import uuid
from typing import List
from locations.model import Location


class LocationRepository:
    _location_id_to_location_map = {}
    _object_id_to_location_map = {}

    @classmethod
    def insert_one(cls, location: Location) -> Location:
        if location.id not in cls._location_id_to_location_map:
            cls._location_id_to_location_map[location.id] = location
            if location.object_id not in cls._object_id_to_location_map:
                cls._object_id_to_location_map[location.object_id] = []
            cls._object_id_to_location_map[location.object_id].append(location)
        else:
            raise Exception("Location id already exists")
        return location

    @classmethod
    def get_by_id(cls, location_id: uuid.UUID) -> Location:
        if location_id not in cls._location_id_to_location_map:
            raise Exception("Location id does not exist")
        return cls._location_id_to_location_map[location_id]

    @classmethod
    def get_by_object_id(cls, object_id: uuid.UUID) -> List[Location]:
        return cls._object_id_to_location_map.get(object_id, [])

    @classmethod
    def update(cls, location: Location):
        if location.id not in cls._location_id_to_location_map:
            raise Exception("Location id does not exist")
        cls._location_id_to_location_map[location.id] = location
