from random import randint
import unittest

import Enums
import Obj
from QuantifierDatasetGen.QuantifierDatasetGen import QuantifierDatasetGen
from QuantifierDatasetGen.QuantifierRelationship import Relationship
from Settings import Settings
import random


class TestQuantifierDatasetGen(unittest.TestCase):
    def test_gen_objects_all_rel(self):
        X = Enums.Colours.RED
        Y = Enums.Shapes.CIRCLE
        number = random.randint(1, 5)
        dataset_gen = QuantifierDatasetGen()
        objects = dataset_gen.get_objects_all_rel(X, Y, number)
        self.assertEqual(Relationship.evaluate_all(X, Y, objects), True)

    def test_gen_objects_notall_rel(self):
        X = Enums.Colours.RED
        Y = Enums.Shapes.CIRCLE
        number = random.randint(1, 5)
        dataset_gen = QuantifierDatasetGen()
        objects = dataset_gen.get_objects_not_all_rel(X, Y, number)
        self.assertEqual(Relationship.evaluate_not_all(X, Y, objects), True)

    def test_gen_objects_only_rel(self):
        X = Enums.Shapes.CIRCLE
        Y = Enums.Colours.RED
        number = random.randint(1, 5)
        dataset_gen = QuantifierDatasetGen()
        objects = dataset_gen.get_objects_only_rel(X, Y, number)
        self.assertEqual(Relationship.evaluate_only(X, Y, objects), True)

    def test_gen_objects_not_only_rel(self):
        X = Enums.Shapes.CIRCLE
        Y = Enums.Colours.RED
        number = random.randint(1, 5)
        dataset_gen = QuantifierDatasetGen()
        objects = dataset_gen.get_objects_not_only_rel(X, Y, number)
        self.assertEqual(Relationship.evaluate_not_only(X, Y, objects), True)

    def test_gen_objects_some_rel(self):
        X = Enums.Colours.RED
        Y = Enums.Shapes.CIRCLE
        number = random.randint(1, 5)
        dataset_gen = QuantifierDatasetGen()
        objects = dataset_gen.get_objects_some_rel(X, Y, number)
        self.assertEqual(Relationship.evaluate_some(X, Y, objects), True)

    def test_gen_objects_none_rel(self):
        X = Enums.Shapes.CIRCLE
        Y = Enums.Colours.RED
        number = random.randint(1, 5)
        dataset_gen = QuantifierDatasetGen()
        objects = dataset_gen.get_objects_none_rel(X, Y, number)
        self.assertEqual(Relationship.evaluate_none(X, Y, objects), True)


if __name__ == '__main__':
    unittest.main()
