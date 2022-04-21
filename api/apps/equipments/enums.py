from enum import Enum

class EquipmentStatus(str, Enum):
    BAD = "Bad"
    REMOVED = "Removed"
    GOOD = "Good"
    NORMAL = "Normal"
    MAINTAIN = "Maintain"
    
    @classmethod
    def choices(cls):
        return tuple((i.value, i.value) for i in cls)
    

class MaterialStatus(str, Enum):
    HIGH = 1
    MEDIUM = 2
    LOW = 3
    OUT = 4
    
    @classmethod
    def choices(cls):
        return tuple((i.value, i.value) for i in cls)
    