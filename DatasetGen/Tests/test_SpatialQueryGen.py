import unittest
from SpatialDatasetGen.SpatialQueryGen import SpatialQueryGen
import Enums, Obj
from Settings import Settings
from SpatialDatasetGen import SpatialDatasetGen
from SpatialDatasetGen.SpatialRelationship import Relationship


class TestSpatialQueryGen(unittest.TestCase):
    def test_gen_captions_1(self):
        settings = Settings(
            num_rows=3, num_cols=3, num_objs=3, single_template=True)
        rel = Relationship.HORIZONTAL
        obj1 = Obj.Obj(Enums.Shapes.PENTAGON, Enums.Colours.YELLOW, None)
        obj2 = Obj.Obj(Enums.Shapes.STAR, Enums.Colours.BROWN, None)
        obj3 = Obj.Obj(Enums.Shapes.TRAPEZIUM, Enums.Colours.PURPLE, None)
        obj1.row, obj1.column = 0, 0
        obj2.row, obj2.column = 0, 1
        obj3.row, obj3.column = 0, 2
        obj_list = [obj1, obj2, obj3]

        captions = dict(SpatialQueryGen(
            obj_list, rel, settings).gen_queries())
        self.assertEqual(
            captions[0]['query'], 'The yellow pentagon is left of the brown star.')
        self.assertEqual(
            captions[0]['answer'], True)
        self.assertEqual(
            captions[10]['query'], 'The purple trapezium is right of the yellow pentagon.')
        self.assertEqual(
            captions[10]['answer'], True)

    def test_gen_captions_2(self):
        settings = Settings(
            num_rows=3, num_cols=3, num_objs=2, single_template=True)
        rel = Relationship.HORIZONTAL
        obj1 = Obj.Obj(Enums.Shapes.PENTAGON, Enums.Colours.YELLOW, None)
        obj2 = Obj.Obj(Enums.Shapes.STAR, Enums.Colours.BROWN, None)
        obj1.row, obj1.column = 0, 0
        obj2.row, obj2.column = 0, 1
        obj_list = [obj1, obj2]

        captions = dict(SpatialQueryGen(obj_list, rel, settings).gen_queries())
        self.assertEqual(
            captions[0]['query'], 'The yellow pentagon is left of the brown star.')
        self.assertEqual(
            captions[0]['answer'], True)
        self.assertEqual(
            captions[2]['query'], 'The yellow pentagon is right of the brown star.')
        self.assertEqual(
            captions[2]['answer'], False)


if __name__ == '__main__':
    unittest.main()
