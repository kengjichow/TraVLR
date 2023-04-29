from enum import Enum


class Relationship(Enum):
    HORIZONTAL = "left/right"
    VERTICAL = "above/below"
    DIAGONAL_UP = "left+above/right+below"
    DIAGONAL_DOWN = "left+below/right+above"
    SIZE = "smaller/larger"

    def get_valid_positions(relationship, settings):
        """
        Returns a list of lists given a relationship, grid size and number of objects. 
        Each sublist represents valid positions a set of objects may be placed.
        For instance, given a HORIZONTAL relationship, each list contains the coordinates of a single row.
        """
        num_rows = settings.num_rows
        num_cols = settings.num_cols
        min_cells = settings.num_objs

        if relationship == Relationship.HORIZONTAL:
            return [[(i, j) for j in range(0, num_cols)] for i in range(0, num_rows)]
        elif relationship == Relationship.VERTICAL:
            return [[(j, i) for j in range(0, num_rows)] for i in range(0, num_cols)]
        elif relationship == Relationship.DIAGONAL_UP:
            start_points = [(i, 0) for i in range(0, num_rows)] + \
                [(num_rows-1, i) for i in range(1, num_cols)]
            diagonals = list(map(lambda pt: list(zip([i for i in range(
                pt[0], -1, -1)], [j for j in range(pt[1], num_cols)])), start_points))
            return list(filter(lambda diag: len(diag) >= min_cells, diagonals))
        elif relationship == Relationship.DIAGONAL_DOWN:
            start_points = [(i, 0) for i in range(1, num_rows)] + \
                [(0, i) for i in range(0, num_cols)]
            diagonals = list(map(lambda pt: list(zip([i for i in range(pt[0], num_rows)], [
                             j for j in range(pt[1], num_cols)])), start_points))
            return list(filter(lambda diag: len(diag) >= min_cells, diagonals))
        elif relationship == Relationship.SIZE:
            return [[(i, j) for i in range(num_rows)] for j in range(num_cols)]