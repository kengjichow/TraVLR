import itertools
import random

import numpy as np
from Enums import Colours, Shapes
from ImageGen import ImageGen
from Obj import Obj
from Settings import Settings

from DatasetGen import DatasetGen
from .SpatialConditionGen import SpatialConditionGen
from .SpatialRelationship import Position, Relationship


class SpatialDatasetGen(DatasetGen):
    def __init__(self):
        self.settings = Settings(
            num_rows=6, num_cols=6, num_objs=3, num_test_objs=3, single_template=False)
        self.colours = [Colours.RED, Colours.BLUE, Colours.GREEN,
                        Colours.YELLOW, Colours.ORANGE]  # list(Colours)
        self.shapes = [Shapes.SQUARE, Shapes.CIRCLE, Shapes.TRIANGLE, Shapes.STAR,
                       Shapes.HEXAGON, Shapes.OCTAGON, Shapes.PENTAGON]  # list(Shapes)
        self.test_train_split = (9, 10)  # 90% train, 10% test
        self.image_gen = ImageGen(self.settings.image_height, self.settings.image_width,
                                  self.settings.num_rows, self.settings.num_cols)
        self.seed = 6
        random.seed(self.seed)
        self.objects_position_map = {}

    def label_split(self, conditions, split):
        for cond in conditions:
            cond['split'] = split
            cond['metadata']['split'] = split

    def gen_conditions(self, num_conditions):
        '''
        Generates a dataset covering all possible positions for three objects.
        Given X objects, the number of conditions is XP3 x num_positions.
        Given the Horizontal relationship, num_positions=3 for a 3x3 grid.

        Conditions are first split into train and test set based on 2 objects designated as objects to appear in the query.
        This ensures that a query with the same 2 objects will not occur in both the train and test set.
        '''
        # divide by two for each relationship
        num_train = num_conditions['num_train'] // 2
        num_val = num_conditions['num_val'] // 2
        num_val_test = num_conditions['num_val_test'] // 2
        num_test = num_conditions['num_test'] // 2

        object_lists = self.gen_all_object_lists(2, for_query=True)
        # object_lists = object_lists[:200]  # comment out

        train_test_split = len(object_lists) // 5 * 4
        train_object_lists = object_lists[:train_test_split]
        test_object_lists = object_lists[train_test_split:]

        train_all_conditions = []
        val_all_conditions = []
        val_test_all_conditions = []
        test_all_conditions = []

        possible_positions = Position(self.settings)
        for rel in [Relationship.HORIZONTAL, Relationship.VERTICAL]:
            train_conditions = self.gen_conditions_subset(
                rel, train_object_lists, possible_positions, split="train", num_pos=4)
            train_conditions = random.sample(
                train_conditions, num_train+num_val+num_val_test)

            train_conditions, val_conditions, val_test_conditions = np.split(train_conditions, [
                int(len(train_conditions)*(num_train /
                    (num_train+num_val+num_val_test))),
                int(len(train_conditions)*((num_train+num_val) /
                    (num_train+num_val+num_val_test))),
            ])
            self.label_split(val_conditions, "val")
            self.label_split(val_test_conditions, "val_test")

            train_all_conditions += list(train_conditions)
            val_all_conditions += list(val_conditions)
            val_test_all_conditions += list(val_test_conditions)

            test_conditions = self.gen_conditions_subset(
                rel, test_object_lists, possible_positions, split="test", num_pos=3)
            test_conditions = random.sample(test_conditions, num_test)
            test_all_conditions += list(test_conditions)

        conditions = train_all_conditions + val_all_conditions + \
            val_test_all_conditions + test_all_conditions
        self.output(conditions)

    def gen_conditions_subset(self, rel, object_lists, possible_positions, split, num_pos):
        conditions = []
        for object_list in object_lists:
            distractor_objs = self.gen_all_object_lists(
                1, for_query=False, remove=object_list)
            positions = possible_positions.get_position(rel, train=(
                split == 'train'), num_positions=len(distractor_objs)*num_pos)
            pos_idx = 0
            for distractor_idx in range(len(distractor_objs)):
                objs = object_list + list(distractor_objs[distractor_idx])
                for pos in positions[pos_idx:pos_idx+num_pos]:
                    condition = SpatialConditionGen(
                        objs, rel, self.settings, self.image_gen, split).gen_unique_conditions([pos])
                    conditions += condition
                pos_idx += num_pos
        return conditions

    def gen_all_object_lists(self, num_objects, for_query=False, remove=[]):
        '''
        Returns every permutation of num_objects number of objects, selected from the full set of possible objects.
        The remove array defines the objects that should be excluded from the set of possible objects to select from.
        '''
        all_objects = [Obj(shape, colour, None)
                       for shape in self.shapes for colour in self.colours]
        for to_remove in remove:
            all_objects = list(
                filter(lambda x: not x.sameAttr(to_remove), all_objects))
        object_lists = list(itertools.combinations(all_objects, num_objects))
        object_lists = list(map(list, object_lists))
        random.shuffle(object_lists)
        if for_query:
            for object_list in object_lists:
                for obj in object_list:
                    obj.for_query = True
        return object_lists

    def gen_objects(self, num_objects, for_query=True):
        object_list = []
        while len(object_list) < num_objects:
            obj = self.gen_random_object()
            if len(list(filter(lambda o: o.sameAttr(obj), object_list))) == 0:
                obj.for_query = for_query
                object_list.append(obj)
        return object_list

    def gen_random_object(self):
        colour = random.choice(self.colours)
        shape = random.choice(self.shapes)
        return Obj(shape, colour, None)
