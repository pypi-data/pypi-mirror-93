from enum import Enum


class CoCoDeviceClass(Enum):
    SWITCHES = 'switches'
    LIGHTS = 'lights'
    SHUTTERS = 'shutters'
    FANS = 'fans'
    SWITCHED_FANS = 'switched-fans'
    GENERIC = 'generic'
