import enum


class VehicleKind(str, enum.Enum):
    FIRE_TRUCK = "FIRE_TRUCK"
    POLICE_STATION = "POLICE_STATION"
    AMBULANCE = "AMBULANCE"