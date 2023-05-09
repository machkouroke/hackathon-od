import enum


class AlertKind(str, enum.Enum):
    INCENDIE = "INCENDIE"
    ACCIDENT = "ACCIDENT"
    AGGRESSION = "AGGRESSION"
    VOL = "VOL"