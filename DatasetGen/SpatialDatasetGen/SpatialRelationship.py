from enum import Enum
import random
import itertools


class Position():
    def __init__(self, settings):
        '''
        No repetition of the same row or column being queried.
        '''
        all_horizontal_positions = Relationship.get_no_restriction_position(
            Relationship.HORIZONTAL, settings, None)
        columns_dict = {}
        for pos in all_horizontal_positions:
            col_pair = tuple(sorted((pos[0][1], pos[1][1])))
            if col_pair not in columns_dict:
                columns_dict[col_pair] = []
            columns_dict[col_pair].append(pos)
        column_keys = list(columns_dict.keys())
        random.shuffle(column_keys)

        test_keys = [(0, 4), (1, 3), (2, 5)]
        train_keys = list(filter(lambda x: x not in test_keys, column_keys))

        self.train_horizontal_positions = [
            i for j in train_keys for i in columns_dict[j]]
        self.test_horizontal_positions = [
            i for j in test_keys for i in columns_dict[j]]

        all_vertical_positions = Relationship.get_no_restriction_position(
            Relationship.VERTICAL, settings, None)
        row_dict = {}
        for pos in all_vertical_positions:
            row_pair = tuple(sorted((pos[0][0], pos[1][0])))
            if row_pair not in row_dict:
                row_dict[row_pair] = []
            row_dict[row_pair].append(pos)
        row_keys = list(row_dict.keys())
        random.shuffle(row_keys)

        test_keys = [(1, 5), (0, 2), (3, 4)]
        train_keys = list(filter(lambda x: x not in test_keys, row_keys))

        self.train_vertical_positions = [
            i for j in train_keys for i in row_dict[j]]
        self.test_vertical_positions = [
            i for j in test_keys for i in row_dict[j]]

    def get_position(self, relationship, train, num_positions):
        if relationship == Relationship.VERTICAL:
            if train:
                return random.sample(self.train_vertical_positions, num_positions)
            else:
                return random.sample(self.test_vertical_positions, num_positions)
        elif relationship == Relationship.HORIZONTAL:
            if train:
                return random.sample(self.train_horizontal_positions, num_positions)
            else:
                return random.sample(self.test_horizontal_positions, num_positions)


class Relationship(str, Enum):
    HORIZONTAL = "left/right"
    VERTICAL = "above/below"
    DIAGONAL_UP = "left+above/right+below"
    DIAGONAL_DOWN = "left+below/right+above"
    SIZE = "smaller/larger"

    def get_rel(relationship):
        if relationship == Relationship.HORIZONTAL:
            return ("to the left of", "to the right of")
        elif relationship == Relationship.VERTICAL:
            return ("above", "below")
        elif relationship == Relationship.DIAGONAL_DOWN:
            return ("above and to the left of", "below and to the right of")
        elif relationship == Relationship.DIAGONAL_UP:
            return ("below and to the left of", "above and to the right of")
        elif relationship == Relationship.SIZE:
            return ("smaller than", "larger than")

    def get_no_restriction_position(relationship, settings, num_positions):
        '''
        Objects may occur anywhere in the grid. Only restriction is that two objects queried must not be 
        neutral with respect to the relationship.

        Total number of possibilities (the order matters) using Relationship.HORIZONTAL as an example:
        ((num_rows * num_cols) * (num_rows * num_cols - num_rows)) / 2 * (num_rows * num_cols - 2)

        E.g. with 3x3 grid: (9 * 6)/2 * 7 = 189

        First two objects are already ordered from selection. Last object is selected randomly from remaining positions.
        Return list of (9 * 6)/2
        '''
        queried_objects_pos = Relationship.get_all_positions(settings)
        queried_objects_pos = list(
            itertools.permutations(queried_objects_pos, 2))
        queried_objects_pos = list(map(lambda x: list(x), queried_objects_pos))
        if relationship == Relationship.HORIZONTAL:
            queried_objects_pos = list(
                filter(lambda x: x[0][1] != x[1][1], queried_objects_pos))
        elif relationship == Relationship.VERTICAL:
            queried_objects_pos = list(
                filter(lambda x: x[0][0] != x[1][0], queried_objects_pos))
        if num_positions is not None:
            queried_objects_pos = random.sample(
                queried_objects_pos, num_positions)
        positions = []

        num_distractor_objs = settings.num_test_objs - 2
        for pos in queried_objects_pos:
            pos += random.sample(Relationship.get_all_positions(settings,
                                 used=pos), num_distractor_objs)
            positions.append(pos)
        return positions

    def get_all_positions(settings, used=[]):
        positions = [[i, j] for i in range(
            0, settings.num_rows) for j in range(0, settings.num_cols)]
        used = list(map(list, used))
        for pos in used:
            positions.remove(pos)
        return tuple(positions)

    def get_restricted_position(relationship, settings, NUM_POSITIONS):
        '''
        Two queried objects must either be in the same row or in the same column. Third object may occur anywhere.

        Total number of possibilities (the order matters) using Relationship.HORIZONTAL as an example:
        (num_rows * (num_cols P 2)) / 2 * (num_rows * num_cols - 2)

        E.g. with 3x3 grid: (3 * 6)/2 * 7 = 126

        Last object is selected randomly. 
        Returns 3*6/2 = 9 possible
        '''
        flatten = itertools.chain.from_iterable
        queried_objects_pos = Relationship.get_valid_positions(
            relationship, settings)
        queried_objects_pos = flatten(
            list(map(lambda x: itertools.combinations(x, 2), queried_objects_pos)))
        queried_objects_pos = list(
            map(lambda x: sorted(x), queried_objects_pos))
        if NUM_POSITIONS is not None:
            queried_objects_pos = random.sample(
                queried_objects_pos, NUM_POSITIONS)
        positions = []
        for pos in queried_objects_pos:
            pos += [random.choice(Relationship.get_all_positions(settings, used=pos))]
            positions.append(pos)
        return positions

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
