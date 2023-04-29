import random

from DatasetGen import DatasetGen
from Enums import Colours, Shapes
from ImageGen import ImageGen
from Settings import Settings

from .CardinalityConditionGen import CardinalityConditionGen


class CardinalityDatasetGen(DatasetGen):
    def __init__(self):
        self.settings = Settings(
            num_rows=6, num_cols=6, num_objs=6, single_template=False)
        self.colours = [Colours.RED, Colours.BLUE, Colours.GREEN,
                        Colours.YELLOW, Colours.ORANGE]  # list(Colours)
        self.shapes = [Shapes.SQUARE, Shapes.CIRCLE, Shapes.TRIANGLE, Shapes.STAR,
                       Shapes.HEXAGON, Shapes.OCTAGON, Shapes.PENTAGON]  # list(Shapes)
        self.overlap_input = False
        self.test_train_split = (9, 10)  # 90% train, 10% test
        self.image_gen = ImageGen(self.settings.image_height, self.settings.image_width,
                                  self.settings.num_rows, self.settings.num_cols)
        self.seed = 6
        random.seed(self.seed)

    def gen_eval(self, num_conditions=50):
        cases = [(6, 7), (7, 8), (8, 9)]
        conditions = self.gen_conditions_subset(
            cases, num_conditions, train=False)
        self.output(conditions)

    def gen_conditions(self, num_conditions):
        '''
        num_conditions: the number of conditions for an (attr, number) pair
        attr: a shape or a colour
        number: number of occurrences of objects with attr
        '''
        # split by test and train
        train_cases = []
        test_cases = []
        attr_type = list(self.shapes)  # set attr to shape
        test_number = [[1, 5], [2, 6], [3, 1], [4, 2], [5, 3], [6, 4]]
        for attr_idx in range(len(list(attr_type))):
            for num_queried_objs in range(1, self.settings.num_objs+1):
                if num_queried_objs in test_number[attr_idx-1]:
                    test_cases.append((attr_type[attr_idx], num_queried_objs))
                else:
                    train_cases.append((attr_type[attr_idx], num_queried_objs))

        num_train = num_conditions['num_train']
        num_val = num_conditions['num_val']
        num_val_test = num_conditions['num_val_test']
        num_test = num_conditions['num_test']

        num_train_conditions = (num_train + num_val +
                                num_val_test) // len(train_cases) + 1
        num_test_conditions = (num_test) // len(test_cases) + 1

        if self.overlap_input:
            train_conditions = self.gen_conditions_subset_swap(
                train_cases, num_train_conditions, train=True)
            test_conditions = self.gen_conditions_subset_swap(
                test_cases, num_test_conditions, train=False)
        else:
            train_conditions = self.gen_conditions_subset(
                train_cases, num_train_conditions, train=True)
            test_conditions = self.gen_conditions_subset(
                test_cases, num_test_conditions, train=False)
        self.output_split(train_conditions, test_conditions, num_conditions)

    def gen_conditions_overlap(self, num_conditions=10):
        '''
        num_conditions: the number of conditions for an (attr, number) pair
        attr: a shape or a colour
        number: number of occurrences of objects with attr
        '''
        cases = []
        attr_type = self.colours  # set attr to shape
        for attr in list(attr_type):
            for num_queried_objs in range(self.settings.num_objs):  # [0, x)
                cases.append((attr, num_queried_objs))
        random.shuffle(cases)

        conditions = self.gen_conditions_subset(
            cases, num_conditions, train=True)
        train_test_split = len(
            conditions) // self.test_train_split[1] * self.test_train_split[0]
        train_conditions = conditions[:train_test_split]
        test_conditions = conditions[train_test_split:]
        for cond in test_conditions:
            cond['split'] = 'test'
            cond['metadata']['split'] = 'test'
        self.output(train_conditions + test_conditions)

    def gen_conditions_compare(self, cases, num_conditions, train):
        conditions = []
        for attr, query_number in cases:
            unique_distractor_lists = []
            for i in range(num_conditions):
                objects = []
                num_queried_objs = random.randint(0, self.settings.num_objs)
                query_objs = self.gen_rand_objs(attr, num_queried_objs)
                # random.randint(1, max(1, self.settings.num_objs - num_queried_objs))
                num_distractor_objs = random.randint(1, 10)
                distractor_objs = self.gen_distractor_objs(
                    num_distractor_objs, exclude_attr=[attr])

                distractor_objs_tuple = sorted(
                    tuple(map(lambda obj: (obj['colour'], obj['shape']))))
                while distractor_objs_tuple in unique_distractor_lists:
                    distractor_objs_tuple = sorted(
                        tuple(map(lambda obj: (obj['colour'], obj['shape']))))
                unique_distractor_lists.append(distractor_objs_tuple)

                objects = query_objs + distractor_objs
                random.shuffle(objects)

                split = 'train' if train else 'test'
                gen = CardinalityConditionGen(
                    objects, attr, query_number, self.settings, self.image_gen, split)
                conditions += gen.gen_condition(1)
        random.shuffle(conditions)
        return conditions

    def gen_conditions_subset_swap(self, cases, num_conditions, train):
        conditions = []
        for attr, num_queried_objs in cases:
            for i in range(num_conditions):
                objects = []
                answer = random.choice([True, False])
                wrong_answers = [i for i in range(1, self.settings.num_objs+1)]
                wrong_answers.remove(num_queried_objs)
                number = num_queried_objs if answer else random.choice(
                    wrong_answers)

                query_objs = self.gen_rand_objs(attr, number)
                # random.randint(1, max(1, self.settings.num_objs - num_queried_objs))
                num_distractor_objs = random.randint(1, 10)
                distractor_objs = self.gen_distractor_objs(
                    num_distractor_objs, exclude_attr=[attr])
                objects = query_objs + distractor_objs
                random.shuffle(objects)

                split = 'train' if train else 'test'
                gen = CardinalityConditionGen(
                    objects, attr, num_queried_objs, self.settings, self.image_gen, split)
                conditions += gen.gen_condition(1)
        random.shuffle(conditions)
        return conditions

    def gen_conditions_subset(self, cases, num_conditions, train):
        '''
        Cases include (attr, num_queried_objs) pair
        '''
        conditions = []
        for attr, num_queried_objs in cases:
            self.clear_unique_distractor_list()
            wrong_answers = list(
                filter(lambda case: case[0] == attr and case[1] != num_queried_objs, cases))
            for i in range(num_conditions):
                objects = []
                query_objs = self.gen_rand_objs(attr, num_queried_objs)
                distractors = self.gen_unique_distractor_list(
                    10, exclude_attr=[attr])
                objects = query_objs + distractors
                random.shuffle(objects)

                answer = random.choice([True, False])
                # wrong_answers = [i for i in range(1, self.settings.num_objs+1)]
                # wrong_answers.remove(num_queried_objs)
                number = num_queried_objs if answer else random.choice(
                    wrong_answers)[1]

                split = 'train' if train else 'test'
                gen = CardinalityConditionGen(
                    objects, attr, number, self.settings, self.image_gen, split)
                conditions += gen.gen_condition(1)
        random.shuffle(conditions)
        return conditions
