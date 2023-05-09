import enum


class AlertKind(str, enum.Enum):
    INCENDIE = "INCENDIE"
    ACCIDENT = "ACCIDENT"
    Aggression = "AGGRESSION"