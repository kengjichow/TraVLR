from ImageGen import ImageGen
import unittest
import cv2 as cv
from Settings import Settings
from SpatialDatasetGen.SpatialDatasetGen import SpatialDatasetGen, Settings
from SpatialDatasetGen.SpatialConditionGen import SpatialConditionGen
import Enums
from SpatialDatasetGen.SpatialRelationship import Relationship


class TestSpatialConditionGen(unittest.TestCase):
    def setUp(self):
        self.settings_3 = Settings(
            num_rows=3, num_cols=3, num_objs=3, single_template=True)
        self.settings_2 = Settings(
            num_rows=3, num_cols=3, num_objs=2, single_template=True)
        self.image_gen_3 = ImageGen(self.settings_3.image_height, self.settings_3.image_width,
                                    self.settings_3.num_rows, self.settings_3.num_cols)
        self.image_gen_2 = ImageGen(self.settings_2.image_height, self.settings_2.image_width,
                                    self.settings_2.num_rows, self.settings_2.num_cols)

    def test_gen_unique_conditions_1(self):
        '''
        Total number of conditions expected = 36 for 3 objects, position already fixed.
        3 rows * 3 possible object pairs * 4 queries per pair = 36
        '''
        object_list = SpatialDatasetGen().gen_objects(3)
        rel = Relationship.HORIZONTAL
        condition = SpatialConditionGen(object_list, rel, self.settings_3, self.image_gen_3).gen_unique_conditions(
            num_captions=None, num_positions=None)
        print(condition)
        self.assertEqual(len(condition), 36)
    
    def test_gen_unique_conditions_2(self):
        '''
        Total number of conditions expected = 36 for 2 objects, position already fixed.
        9 possible positions * 4 queries per pair = 36
        '''
        object_list = SpatialDatasetGen().gen_objects(2)
        rel = Relationship.HORIZONTAL
        condition = SpatialConditionGen(object_list, rel, self.settings_2, self.image_gen_2).gen_unique_conditions(
            num_captions=None, num_positions=None)
        print(condition)
        self.assertEqual(len(condition), 9)

    def test_gen_condition_1(self):
        obj_list = SpatialDatasetGen().gen_objects(3)
        rel = Relationship.DIAGONAL_DOWN
        condition_gen = SpatialConditionGen(
            obj_list, rel, self.settings_3, self.image_gen_3)
        condition_gen.prepare_obj_list()
        condition = condition_gen.gen_condition(4, caption_exact=False)
        expected = [[(i, j) for j in range(12)] for i in range(4)].sort()
        codes = list(map(lambda c: c["code"], condition)).sort()
        self.assertEqual(codes, expected)
        self.assertIsNotNone(condition[0]["image"])

    def test_gen_condition_2(self):
        obj_list = SpatialDatasetGen().gen_objects(2)
        rel = Relationship.DIAGONAL_UP
        condition_gen = SpatialConditionGen(
            obj_list, rel, self.settings_2, self.image_gen_2)
        condition_gen.prepare_obj_list()
        condition = condition_gen.gen_condition(4, caption_exact=False)
        expected = [[(i, j) for j in range(4)] for i in range(2)].sort()
        codes = list(map(lambda c: c["code"], condition)).sort()
        self.assertEqual(codes, expected)
        self.assertIsNotNone(condition[0]["image"])

    def test_prepare_object_list_1(self):
        obj_list = SpatialDatasetGen().gen_objects(3)
        rel = Relationship.DIAGONAL_DOWN
        obj_list = SpatialConditionGen(obj_list, rel,
                                       self.settings_3, self.image_gen_3).prepare_obj_list()
        expected = [(0, 0), (1, 1), (2, 2)]
        self.assertEqual(
            (obj_list[0].row, obj_list[0].column), expected[0])
        self.assertEqual(
            (obj_list[1].row, obj_list[1].column), expected[1])
        self.assertEqual(
            (obj_list[2].row, obj_list[2].column), expected[2])

    def test_prepare_object_list_2(self):
        obj_list = SpatialDatasetGen().gen_objects(3)
        rel = Relationship.DIAGONAL_UP
        obj_list = SpatialConditionGen(
            obj_list, rel, self.settings_3, self.image_gen_3).prepare_obj_list()
        expected = [(2, 0), (1, 1), (0, 2)]
        self.assertEqual(
            (obj_list[0].row, obj_list[0].column), expected[0])
        self.assertEqual(
            (obj_list[1].row, obj_list[1].column), expected[1])
        self.assertEqual(
            (obj_list[2].row, obj_list[2].column), expected[2])

    def test_prepare_object_list_3(self):
        obj_list = SpatialDatasetGen().gen_objects(3)
        rel = Relationship.HORIZONTAL
        obj_list = SpatialConditionGen(
            obj_list, rel, self.settings_3, self.image_gen_3).prepare_obj_list()
        actual = [(obj_list[0].row, obj_list[0].column),
                  (obj_list[1].row, obj_list[1].column),
                  (obj_list[2].row, obj_list[2].column)]
        self.assertEqual(actual == [(0, 0), (0, 1), (0, 2)]
                         or actual == [(1, 0), (1, 1), (1, 2)]
                         or actual == [(2, 0), (2, 1), (2, 2)], True)

    def test_prepare_object_list_4(self):
        obj_list = SpatialDatasetGen().gen_objects(3)
        rel = Relationship.VERTICAL
        obj_list = SpatialConditionGen(
            obj_list, rel, self.settings_3, self.image_gen_3).prepare_obj_list()
        actual = [(obj_list[0].row, obj_list[0].column),
                  (obj_list[1].row, obj_list[1].column),
                  (obj_list[2].row, obj_list[2].column)]
        self.assertEqual(actual == [(0, 0), (1, 0), (2, 0)]
                         or actual == [(0, 1), (1, 1), (2, 1)]
                         or actual == [(0, 2), (1, 2), (2, 2)], True)

    def test_prepare_object_list_5(self):
        obj_list = SpatialDatasetGen().gen_objects(3)
        rel = Relationship.SIZE
        obj_list = SpatialConditionGen(
            obj_list, rel, self.settings_3, self.image_gen_3).prepare_obj_list()
        self.assertEqual(obj_list[0].size, Enums.Size.SMALL)
        self.assertEqual(obj_list[1].size, Enums.Size.MEDIUM)
        self.assertEqual(obj_list[2].size, Enums.Size.LARGE)

    def test_prepare_object_list_6(self):
        obj_list = SpatialDatasetGen().gen_objects(2)
        rel = Relationship.DIAGONAL_DOWN
        obj_list = SpatialConditionGen(
            obj_list, rel, self.settings_3, self.image_gen_3).prepare_obj_list()
        actual = [(obj_list[0].row, obj_list[0].column),
                  (obj_list[1].row, obj_list[1].column)]
        self.assertEqual(actual == [(0, 0), (1, 1)]
                         or actual == [(1, 1), (2, 2)]
                         or actual == [(0, 0), (2, 2)]
                         or actual == [(0, 1), (1, 2)]
                         or actual == [(1, 0), (2, 1)], True)


if __name__ == '__main__':
    unittest.main()
