from .SpatialRelationship import Relationship
from Enums import Colours, Shapes
from .SpatialConditionGen import SpatialConditionGen
import random
from Obj import Obj
from ImageGen import ImageGen
from Settings import Settings
import pandas as pd
from const import INDEX_FILEPATH


class SpatialDatasetGen:
    def __init__(self):
        self.settings = Settings(
            num_rows=3, num_cols=3, num_objs=2, single_template=True)

    def gen_dataset(self, numConditions):
        image_gen = ImageGen(self.settings.image_height, self.settings.image_width,
                             self.settings.num_rows, self.settings.num_cols)
        conditions = []
        num_tokens_per_condition = 1

        for i in range(numConditions):
            object_list = self.gen_objects(self.settings.num_objs) + self.gen_objects(2)
            condition = SpatialConditionGen(object_list, None, self.settings, image_gen).gen_condition(
                num_tokens_per_condition, i%2)
            conditions += condition

        df = pd.DataFrame.from_dict(conditions)
        test_train_split = len(conditions) // 5 * 4
        df["split"] = ["train" for i in range(
            test_train_split)] + ["test" for i in range(len(conditions)-test_train_split)]
        df.to_csv(INDEX_FILEPATH + "index.csv")

    def gen_objects(self, num_objects):
        object_list = []
        while len(object_list) < num_objects:
            obj = self.gen_random_object()
            if len(list(filter(lambda o: o.sameAttr(obj), object_list))) == 0:
                object_list.append(obj)
        return object_list

    def gen_random_object(self):
        colours = list(Colours)
        shapes = list(Shapes)
        colour = random.choice(colours)
        shape = random.choice(shapes)
        return Obj(shape, colour, None)
