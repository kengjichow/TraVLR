import unittest
import Enums
import Obj
from ImageGen import ImageGen


class TestImageGen(unittest.TestCase):
    def test_gen_image_1(self):
        obj1 = Obj.Obj(Enums.Shapes.PENTAGON, Enums.Colours.YELLOW, None)
        obj1.row, obj1.column = (0, 0)
        obj1.size = Enums.Size.SMALL

        obj2 = Obj.Obj(Enums.Shapes.STAR, Enums.Colours.BROWN, None)
        obj2.row, obj2.column = (1, 1)
        obj2.size = Enums.Size.MEDIUM

        obj3 = Obj.Obj(Enums.Shapes.TRAPEZIUM, Enums.Colours.PURPLE, None)
        obj3.row, obj3.column = (2, 2)
        obj3.size = Enums.Size.LARGE

        obj_list = [obj1, obj2, obj3]
        image_gen = ImageGen(500, 500, 3, 3)
        image_gen.draw_objects(obj_list)
        image_gen.show_image()

    def test_gen_image_2(self):
        obj1 = Obj.Obj(Enums.Shapes.PARALLELOGRAM, Enums.Colours.BLACK, None)
        obj1.row, obj1.column = (0, 0)
        obj1.size = Enums.Size.SMALL

        obj2 = Obj.Obj(Enums.Shapes.CIRCLE, Enums.Colours.RED, None)
        obj2.row, obj2.column = (0, 1)
        obj2.size = Enums.Size.MEDIUM

        obj3 = Obj.Obj(Enums.Shapes.SQUARE, Enums.Colours.GREEN, None)
        obj3.row, obj3.column = (2, 0)
        obj3.size = Enums.Size.LARGE

        obj_list = [obj1, obj2, obj3]
        image_gen = ImageGen(700, 700, 3, 3)
        image_gen.draw_objects(obj_list)
        image_gen.show_image()

    def test_gen_image_3(self):
        obj1 = Obj.Obj(Enums.Shapes.TRIANGLE, Enums.Colours.BLUE, None)
        obj1.row, obj1.column = (0, 0)
        obj1.size = Enums.Size.SMALL

        obj2 = Obj.Obj(Enums.Shapes.OCTAGON, Enums.Colours.ORANGE, None)
        obj2.row, obj2.column = (0, 1)
        obj2.size = Enums.Size.MEDIUM

        obj3 = Obj.Obj(Enums.Shapes.HEXAGON, Enums.Colours.GREEN, None)
        obj3.row, obj3.column = (2, 0)
        obj3.size = Enums.Size.LARGE

        obj_list = [obj1, obj2]
        image_gen = ImageGen(300, 500, 3, 3)
        image_gen.draw_objects(obj_list)
        image_gen.show_image()


if __name__ == '__main__':
    unittest.main()
