from enum import Enum


class Shapes(str, Enum):
    SQUARE = "square"
    CIRCLE = "circle"
    TRIANGLE = "triangle"
    PENTAGON = "pentagon"
    HEXAGON = "hexagon"
    OCTAGON = "octagon"
    STAR = "star"
    TRAPEZIUM = "trapezium"
    PARALLELOGRAM = "parallelogram"


class Size(str, Enum):
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"

    def get_ratio(size):
        if size == Size.SMALL:
            return 0.3
        elif size == Size.MEDIUM:
            return 0.55
        elif size == Size.LARGE:
            return 0.95


class Colours(str, Enum):
    RED = "red"
    BLUE = "blue"
    GREEN = "green"
    YELLOW = "yellow"
    PURPLE = "purple"
    ORANGE = "orange"
    BLACK = "black"
    BROWN = "brown"

    def rgb(colour):
        colour_map = {
            Colours.RED: (0, 0, 255),
            Colours.BLUE: (255, 0, 0),
            Colours.GREEN: (0, 255, 0),
            Colours.YELLOW: (0, 255, 255),
            Colours.PURPLE: (250, 230, 230),
            Colours.ORANGE: (0, 165, 255),
            Colours.BLACK: (0, 0, 0),
            Colours.BROWN: (42, 42, 165),
        }

        return colour_map[colour]
