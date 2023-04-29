from enum import Enum


class Relationship(str, Enum):
    EQUAL = "equal"
    FEWER = "fewer"
    MORE = "more"


