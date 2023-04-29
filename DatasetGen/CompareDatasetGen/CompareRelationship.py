from enum import Enum


class Relationship(str, Enum):
    FEWER = "fewer"
    MORE = "more"

    def get_answer(X, Y):
        if X < Y: 
            return Relationship.FEWER
        else:
            return Relationship.MORE ## or equal to


