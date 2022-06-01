from enum import Enum, IntEnum


class SortByEnum(str, Enum):
    BY_RATING = "rating"
    BY_PREMIERE_DATE = "premiere_date"


class SortOrderEnum(IntEnum):
    ASC = 1
    DESC = -1

