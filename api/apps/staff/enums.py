from enum import Enum

class SessionName(str, Enum):
    MOR = "Morning"
    AFF = "Afternoon"
    EVE = "Evening"
    
    @classmethod
    def choices(cls):
        return tuple((i.value, i.value) for i in cls)
        