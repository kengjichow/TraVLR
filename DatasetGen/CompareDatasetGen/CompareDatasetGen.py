import itertools
import math
import random

from DatasetGen import DatasetGen
from Enums import Colours, Shapes
from ImageGen import ImageGen
from Settings import Settings

from .CompareConditionGen import CompareConditionGen
from .CompareRelationship import Relationship


class CompareDatasetGen(DatasetGen):
    def __init__(self):
        self.settings = Settings(
            num_rows=6, num_cols=6, num_objs=10, single_template=False)
        self.colours = [Colours.RED, Colours.BLUE, Colours.GREEN,
                        Colours.YELLOW, Colours.ORANGE]  # list(Colours)
        self.shapes = [Shapes.SQUARE, Shapes.CIRCLE, Shapes.TRIANGLE, Shapes.STAR, 
                    Shapes.HEXAGON, Shapes.OCTAGON, Shapes.PENTAGON]  # list(Shapes)
        self.test_train_split = (9, 10)  # 90% train, 10% test
        self.image_gen = ImageGen(self.settings.image_height, self.settings.image_width,
                             self.settings.num_rows, self.settings.num_cols)

    def gen_eval(self, num_conditions=50):
        cases = [(6, 7), (7, 8), (8, 9)]
        conditions = self.gen_conditions_subset(cases, num_conditions, train=False)
        self.output(conditions)

    def gen_cases(self):
        '''
        1. generate (x, y) pairs of numbers (num_cases)
        2. generate (X, Y) pairs of attributes (attr_cases)
        3. merge to form (x, y, X, Y) tuples
        '''
        num_cases = list(itertools.combinations(range(1, self.settings.num_objs), 2))
        train_num_cases = list(filter(lambda x: abs(x[0]-x[1]) < 4, num_cases))
        train_num_cases = train_num_cases + list(map(lambda x: (x[1], x[0]), train_num_cases))
        test_num_cases = list(filter(lambda x: x not in train_num_cases, num_cases))
        test_num_cases = test_num_cases + list(map(lambda x: (x[1], x[0]), test_num_cases))

        attr_type = self.shapes # set attr to shape
        attr_cases = list(itertools.combinations(list(attr_type), 2))
        test_attr_cases = random.sample(attr_cases, len(attr_cases)//5)
        train_attr_cases = list(filter(lambda x: x not in test_attr_cases, attr_cases))

        train_cases = []
        for case in train_num_cases:
            for pair in train_attr_cases:
                train_cases.append(pair + case)
        random.shuffle(train_cases)

        test_cases = []
        for case in test_num_cases:
            for pair in test_attr_cases:
                test_cases.append(pair + case)
        random.shuffle(test_cases)
        return train_cases, test_cases

    def gen_conditions(self, num_conditions):
        '''
        num_conditions: the number of conditions for an (attr, number) pair
        attr: a shape or a colour
        number: number of occurrences of objects with attr

        Total number of conditions: 
         - num_attr C 2
         - num_poss_number P 2
        '''
        train_cases, test_cases = self.gen_cases()

        num_train = num_conditions['num_train']
        num_val = num_conditions['num_val']
        num_val_test = num_conditions['num_val_test']
        num_test = num_conditions['num_test']

        num_train_conditions = (num_train + num_val +
                                num_val_test) // len(train_cases) + 1
        num_test_conditions = num_test // len(test_cases) + 1
        
        train_conditions = self.gen_conditions_subset(train_cases, num_train_conditions, train=True)
        test_conditions = self.gen_conditions_subset(test_cases, num_test_conditions, train=False)
        self.output_split(train_conditions, test_conditions, num_conditions)

    def gen_conditions_subset(self, cases, num_conditions, train):
        conditions = []
        for attr1, attr2, num_queried_objs_1, num_queried_objs_2 in cases:
            self.clear_unique_distractor_list()
            for i in range(num_conditions):
                objects = []
                query_objs_1 = self.gen_rand_objs(attr1, num_queried_objs_1)
                query_objs_2 = self.gen_rand_objs(attr2, num_queried_objs_2)
                distractors = self.gen_unique_distractor_list(10, exclude_attr=[attr1, attr2])
                objects = query_objs_1 + query_objs_2 + distractors
                random.shuffle(objects)

                relationship = random.choice(list(Relationship))
                case = (relationship, attr1, attr2, num_queried_objs_1, num_queried_objs_2, len(distractors))
                split = 'train' if train else 'test'
                gen = CompareConditionGen(objects, case, self.settings, self.image_gen, split)
                conditions += gen.gen_condition(1)
        random.shuffle(conditions)
        return conditions


