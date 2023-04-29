from CaptionGen import CaptionGen
from .SpatialRelationship import Relationship
from CaptionGen import CaptionGen


class SpatialTextGen(CaptionGen):
    def __init__(self, object_list, relationship, settings):
        self.object_list = object_list
        self.relationship = relationship
        self.settings = settings

    def get_rel(self, relationship):
        if relationship == Relationship.HORIZONTAL:
            return ("left of", "right of")
        elif relationship == Relationship.VERTICAL:
            return ("above", "below")
        elif relationship == Relationship.DIAGONAL_DOWN:
            return ("above and left of", "below and right of")
        elif relationship == Relationship.DIAGONAL_UP:
            return ("below and left of", "above and right of")
        elif relationship == Relationship.SIZE:
            return ("smaller than", "larger than")
