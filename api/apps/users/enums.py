from enum import Enum


class GenderEnum(str, Enum):
    MALE = "Male"
    FEMALE = "Female"
    OTHER = "Other"

    @classmethod
    def choices(cls):
        return tuple((i.value, i.value) for i in cls)


class StatusEnum(str, Enum):
    SINGLE = "Single"
    MARRIED = "Married"

    @classmethod
    def choices(cls):
        return tuple((i.value, i.value) for i in cls)


class UserTypeEnum(str, Enum):
    FULL_TIME = "Full-time"
    PART_TIME = "Part-time"
    PROBATION = "Probation"

    @classmethod
    def choices(cls):
        return tuple((i.value, i.value) for i in cls)
