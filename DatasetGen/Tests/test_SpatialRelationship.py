from SpatialDatasetGen.SpatialRelationship import Relationship, Position
import unittest
from Settings import Settings


class TestSpatialRelationship(unittest.TestCase):
    def setUp(self):
        self.settings = Settings(num_rows=3, num_cols=3, num_objs=3, num_test_objs=3, single_template=False)

    def test_get_restricted_position(self):
        positions = Relationship.get_restricted_position(Relationship.HORIZONTAL, self.settings, None)
        self.assertEqual(len(positions), 9)

    def test_get_no_restriction_position(self):
        positions = Relationship.get_no_restriction_position(Relationship.HORIZONTAL, self.settings, None)
        self.assertEqual(len(positions), 27)

    def test_split_positions(self):
        possible_positions = Position(self.settings)
        test = list(map(lambda x: tuple((tuple(x[0]), tuple(x[1]))), possible_positions.test_vertical_positions))
        train = list(map(lambda x: tuple((tuple(x[0]), tuple(x[1]))), possible_positions.train_vertical_positions))
        self.assertFalse(set(test).intersection(set(train)))

        test = list(map(lambda x: tuple((tuple(x[0]), tuple(x[1]))), possible_positions.test_horizontal_positions))
        train = list(map(lambda x: tuple((tuple(x[0]), tuple(x[1]))), possible_positions.train_horizontal_positions))
        self.assertFalse(set(test).intersection(set(train)))

        test = list(map(lambda x: tuple((x[0][0], x[1][0])), possible_positions.test_vertical_positions))
        train = list(map(lambda x: tuple((x[0][0], x[1][0])), possible_positions.train_vertical_positions))
        self.assertFalse(set(test).intersection(set(train)))

        print(possible_positions.train_horizontal_positions)

    # def test_split_positions_2(self):
    #     settings = Settings(num_rows=10, num_cols=10, num_objs=3, num_test_objs=5, single_template=False)
    #     possible_positions = Position(settings)
    #     test = list(map(lambda x: tuple((x[0][0], x[1][0])), possible_positions.test_vertical_positions))
    #     # print(set(test))
    #     train = list(map(lambda x: tuple((x[0][0], x[1][0])), possible_positions.train_vertical_positions))
    #     # print(set(train))
    #     self.assertFalse(set(test).intersection(set(train)))
    #     self.assertEqual(45, len(set(test).union(set(train))))
    #     # print(sorted(list(set(test).union(set(train)))))

    #     test = list(map(lambda x: tuple((tuple(x[0]), tuple(x[1]))), possible_positions.test_horizontal_positions))
    #     train = list(map(lambda x: tuple((tuple(x[0]), tuple(x[1]))), possible_positions.train_horizontal_positions))
    #     self.assertFalse(set(test).intersection(set(train)))

    # def test_split_positions_3(self):
    #     settings = Settings(num_rows=6, num_cols=6, num_objs=3, num_test_objs=3, single_template=False)
    #     possible_positions = Position(settings)
    #     test = list(map(lambda x: tuple((x[0][0], x[1][0])), possible_positions.test_vertical_positions))
    #     # print(set(test))
    #     train = list(map(lambda x: tuple((x[0][0], x[1][0])), possible_positions.train_vertical_positions))
    #     # print(set(train))
    #     self.assertFalse(set(test).intersection(set(train)))
    #     self.assertEqual(45, len(set(test).union(set(train))))
    #     # print(sorted(list(set(test).union(set(train)))))

    #     test = list(map(lambda x: tuple((tuple(x[0]), tuple(x[1]))), possible_positions.test_horizontal_positions))
    #     train = list(map(lambda x: tuple((tuple(x[0]), tuple(x[1]))), possible_positions.train_horizontal_positions))
    #     self.assertFalse(set(test).intersection(set(train)))

if __name__ == '__main__':
    unittest.main()
