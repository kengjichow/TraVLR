import unittest
import Enums
import Obj
from Settings import Settings
from SpatialDatasetGen.SpatialCaptionGen import SpatialCaptionGen
from SpatialDatasetGen.SpatialRelationship import Relationship
from SpatialDatasetGen import SpatialDatasetGen


class TestSpatialCaptionGen(unittest.TestCase):
    def test_gen_captions_exact_1(self):
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

        caption = dict(SpatialCaptionGen(
            obj_list, rel, settings).gen_caption_exact("SpatialDatasetGen/captions3.txt"))[0]
        self.assertEqual(
            caption, 'The yellow pentagon is at A 1 the brown star is at B 1 and the purple trapezium is at C 1.')

    def test_gen_captions_exact_2(self):
        settings = Settings(
            num_rows=3, num_cols=3, num_objs=3, single_template=True)
        rel = Relationship.HORIZONTAL
        obj1 = Obj.Obj(Enums.Shapes.PENTAGON, Enums.Colours.YELLOW, None)
        obj2 = Obj.Obj(Enums.Shapes.STAR, Enums.Colours.BROWN, None)
        obj1.row, obj1.column = 0, 0
        obj2.row, obj2.column = 1, 1
        obj_list = [obj1, obj2]

        caption = dict(SpatialCaptionGen(
            obj_list, rel, settings).gen_caption_exact("SpatialDatasetGen/captions2.txt"))[0]
        self.assertEqual(
            caption, 'The yellow pentagon is at A 1 and the brown star is at B 2.')

    def test_gen_captions_1(self):
        settings = Settings(
            num_rows=3, num_cols=3, num_objs=3, single_template=True)
        rel = Relationship.HORIZONTAL
        obj1 = Obj.Obj(Enums.Shapes.PENTAGON, Enums.Colours.YELLOW, None)
        obj2 = Obj.Obj(Enums.Shapes.STAR, Enums.Colours.BROWN, None)
        obj3 = Obj.Obj(Enums.Shapes.TRAPEZIUM, Enums.Colours.PURPLE, None)
        obj_list = [obj1, obj2, obj3]

        captions = dict(SpatialCaptionGen(
            obj_list, rel, settings).gen_captions())
        self.assertEqual(
            captions[0], 'The yellow pentagon is left of the brown star. The brown star is left of the purple trapezium.')
        self.assertEqual(
            captions[1], 'The yellow pentagon is left of the brown star. The purple trapezium is right of the brown star.')
        self.assertEqual(
            captions[2], 'The brown star is right of the yellow pentagon. The brown star is left of the purple trapezium.')
        self.assertEqual(
            captions[3], 'The brown star is right of the yellow pentagon. The purple trapezium is right of the brown star.')

    def test_gen_captions_2(self):
        settings = Settings(
            num_rows=3, num_cols=3, num_objs=2, single_template=True)
        rel = Relationship.HORIZONTAL
        obj1 = Obj.Obj(Enums.Shapes.PENTAGON, Enums.Colours.YELLOW, None)
        obj2 = Obj.Obj(Enums.Shapes.STAR, Enums.Colours.BROWN, None)
        obj_list = [obj1, obj2]

        captions = dict(SpatialCaptionGen(
            obj_list, rel, settings).gen_captions())
        self.assertEqual(
            captions[0], 'The yellow pentagon is left of the brown star.')
        self.assertEqual(
            captions[1], 'The brown star is right of the yellow pentagon.')


if __name__ == '__main__':
    unittest.main()
