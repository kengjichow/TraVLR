import itertools
import random

from DatasetGen import DatasetGen
from Enums import Colours, Shapes
from ImageGen import ImageGen
from Obj import Obj
from Settings import Settings

from .QuantifierConditionGen import QuantifierConditionGen
from .QuantifierRelationship import Relationship


class QuantifierDatasetGen(DatasetGen):
    def __init__(self):
        self.settings = Settings(
            num_rows=6, num_cols=6, num_objs=3, single_template=False)
        self.colours = [Colours.RED, Colours.BLUE, Colours.GREEN,
                        Colours.YELLOW, Colours.ORANGE, Colours.PURPLE, Colours.BROWN]  # list(Colours)
        self.shapes = [Shapes.SQUARE, Shapes.CIRCLE, Shapes.TRIANGLE, Shapes.STAR,
                       Shapes.HEXAGON, Shapes.OCTAGON, Shapes.PENTAGON]  # list(Shapes)
        self.test_train_split = (4, 5)  # 90% train, 10% test
        self.num_distractors = (2, 8)
        self.seed = 1
        self.rel_pairs = {
                Relationship.ALL: [Relationship.ALL, Relationship.NOTALL],
                Relationship.NOTALL: [Relationship.ALL, Relationship.NOTALL],
                Relationship.SOME: [Relationship.SOME, Relationship.NONE],
                Relationship.ONLY: [Relationship.ONLY, Relationship.NOT_ONLY],
                Relationship.NONE: [Relationship.SOME, Relationship.NONE],
                Relationship.NOT_ONLY: [
                    Relationship.ONLY, Relationship.NOT_ONLY]
            }
        random.seed(self.seed)
        self.image_gen = ImageGen(self.settings.image_height, self.settings.image_width,
                             self.settings.num_rows, self.settings.num_cols)

    def gen_pairs(self):
        X_attr_type = self.shapes
        Y_attr_type = self.colours
        train_attr_cases = []
        test_attr_cases = list(zip(X_attr_type, Y_attr_type))
        for X in list(X_attr_type):
            for Y in list(Y_attr_type):
                if (X, Y) not in test_attr_cases:
                    train_attr_cases.append((X, Y))

        train_num_cases, test_num_cases = self.get_num_pairs()
        X_shared_train, Y_shared_train, nonshared_train = self.gen_cases(train_num_cases, train_attr_cases)
        X_shared_test, Y_shared_test, nonshared_test = self.gen_cases(test_num_cases, test_attr_cases)

        X_shared_test = list(filter(lambda x: x not in Y_shared_test + nonshared_test, X_shared_test))
        Y_shared_test = list(filter(lambda x: x not in X_shared_test + nonshared_test, Y_shared_test))
        nonshared_test = list(filter(lambda x: x not in X_shared_test + Y_shared_test, nonshared_test))

        nonshared_train = list(filter(lambda x: x not in X_shared_train + Y_shared_train, nonshared_train))
        X_shared_train = list(filter(lambda x: x not in nonshared_train + Y_shared_train, X_shared_train))
        Y_shared_train = list(filter(lambda x: x not in X_shared_train + nonshared_train, Y_shared_train))
        
        def append_rel(cases, rels):
            result = []
            for case in cases:
                for rel in rels:
                    result.append((rel,) + case)
            random.shuffle(result)
            return result

        X_shared_train = append_rel(X_shared_train, [Relationship.NOTALL, Relationship.SOME, Relationship.ONLY])
        X_shared_test = append_rel(X_shared_test, [Relationship.NOTALL, Relationship.SOME, Relationship.ONLY])
        Y_shared_train = append_rel(Y_shared_train, [Relationship.ALL, Relationship.NOT_ONLY])
        Y_shared_test = append_rel(Y_shared_test, [Relationship.ALL, Relationship.NOT_ONLY])
        nonshared_train = append_rel(nonshared_train, [Relationship.NONE])
        nonshared_test = append_rel(nonshared_test, [Relationship.NONE])

        train_cases = X_shared_train + Y_shared_train + nonshared_train
        test_cases = X_shared_test + Y_shared_test + nonshared_test
        return train_cases, test_cases

    def gen_cases(self, num_pairs, attr_pairs):
        '''
        share_X produces cases ((num1, X, Y), (num2, X, Z)) which share the X variable
        share_Y produces cases ((num1, X, Y), (num2, Z, Y)) which share the Y variable
        nonshare produces cases ((num1, X, Y), (num2, W, Z)) which share neither variable
        '''
        def share_X(X, Y, num_pair):
            num1, num2 = num_pair
            Z = random.choice(list(filter(lambda x: x != Y, list(type(Y)))))
            case = ((num1, X, Y), (num2, X, Z))
            return case

        def share_Y(X, Y, num_pair):
            num1, num2 = num_pair
            Z = random.choice(list(filter(lambda x: x != X, list(type(X)))))
            case = ((num1, X, Y), (num2, Z, Y))
            return case

        def nonshare(X, Y, num_pair):
            num1, num2 = num_pair
            W = random.choice(list(filter(lambda x: x != X, list(type(X)))))
            Z = random.choice(list(filter(lambda x: x != Y, list(type(Y)))))
            case = ((num1, X, Z), (num2, W, Y))
            return case

        X_shared = []
        Y_shared = []
        nonshared = []

        for X, Y in attr_pairs:
            for num_pair in num_pairs:
                case = ((X, Y), share_X(X, Y, num_pair))
                if not(case in X_shared or (case[1], case[0]) in X_shared):
                    X_shared.append(case)
                case = ((X, Y), share_Y(X, Y, num_pair))
                if not(case in Y_shared or (case[1], case[0]) in Y_shared):
                    Y_shared.append(case)
                case = ((X, Y), nonshare(X, Y, num_pair))
                if not(case in nonshared or (case[1], case[0]) in nonshared):
                    nonshared.append(case)
        return X_shared, Y_shared, nonshared

    def get_num_pairs(self):
        cases = list(itertools.product(range(1, 6), repeat=2))
        random.shuffle(cases)
        train_test_split = len(
            cases) // self.test_train_split[1] * self.test_train_split[0]
        train_cases = cases[:train_test_split]
        test_cases = cases[train_test_split:]
        return train_cases, test_cases

    def gen_conditions(self, num_conditions):
        '''
        num_conditions: the number of conditions for an (attr, number) pair
        attr: a shape or a colour
        number: number of occurrences of objects with attr

        Total number of conditions: 
         - num_attr_1 * num_attr_2
        '''
        train_cases, test_cases = self.gen_pairs()

        num_train = num_conditions['num_train']
        num_val = num_conditions['num_val']
        num_val_test = num_conditions['num_val_test']
        num_test = num_conditions['num_test']

        num_train_conditions = (num_train + num_val +
                                num_val_test) // len(train_cases) + 1
        num_test_conditions = num_test // len(test_cases) + 1

        train_conditions = self.gen_conditions_subset(
            train_cases, num_train_conditions, train=True)
        test_conditions = self.gen_conditions_subset(
            test_cases, num_test_conditions, train=False)
        self.output_split(train_conditions, test_conditions, num_conditions)

    def gen_conditions_subset(self, cases, num_conditions=None, train=True):
        conditions = []
        for rel, query_pair, pair in cases:
            for i in range(num_conditions):
                rel_pair = self.rel_pairs[rel]
                relationship = random.choice(rel_pair)
                objects = self.gen_objects(query_pair, pair)
                if pair[0] == pair[1]:
                    print(pair)
                case = (relationship, query_pair[0], query_pair[1], pair)
                random.shuffle(objects)
                split = 'train' if train else 'test'
                gen = QuantifierConditionGen(
                    objects, case, self.settings, self.image_gen, split)
                conditions += gen.gen_condition(1)
        random.shuffle(conditions)
        return conditions

    def gen_objects(self, query_pair, pair):
        object_list = []
        obj1, obj2 = pair
        object_list += self.gen_queried_objects(obj1[1], obj1[2], obj1[0])
        object_list += self.gen_queried_objects(obj2[1], obj2[2], obj2[0])
        object_list += self.gen_distractor_objects([query_pair[0], obj1[1], obj2[1]], [query_pair[1], obj1[2], obj2[2]])
        return object_list

    def gen_conditions_subset_ori(self, cases, num_conditions=None, train=True):
        image_gen = ImageGen(self.settings.image_height, self.settings.image_width,
                             self.settings.num_rows, self.settings.num_cols)
        conditions = []
        for rel, X, Y, num1, num2 in cases:
            for i in range(num_conditions):
                rel_pair = self.rel_pairs[rel]
                relationship = random.choice(rel_pair)
                objects = self.get_objects(relationship, X, Y, num1, num2)
                random.shuffle(objects)
                case = (rel, X, Y, num1, num2)
                train = 'train' if train else 'test'
                gen = QuantifierConditionGen(
                    objects, case, self.settings, image_gen, train)
                conditions += gen.gen_condition(1)
        random.shuffle(conditions)
        return conditions

    def get_objects(self, rel, X, Y, num1, num2):
        if rel == Relationship.ALL:
            objects = self.get_objects_all_rel(X, Y, num1, num2)
        elif rel == Relationship.NOTALL:
            objects = self.get_objects_not_all_rel(X, Y, num1, num2)
        elif rel == Relationship.SOME:
            objects = self.get_objects_some_rel(X, Y, num1, num2)
        elif rel == Relationship.NONE:
            objects = self.get_objects_none_rel(X, Y, num1, num2)
        elif rel == Relationship.ONLY:
            objects = self.get_objects_only_rel(X, Y, num1, num2)
        elif rel == Relationship.NOT_ONLY:
            objects = self.get_objects_not_only_rel(X, Y, num1, num2)
        return objects

    def gen_queried_objects(self, X, Y, num_objs):
        objects = []
        X_attr_type = type(X)
        shape = X if X_attr_type == Shapes else Y
        colour = X if X_attr_type == Colours else Y

        for i in range(num_objs):
            obj = Obj(shape, colour, None)
            obj.for_query = True
            objects.append(obj)
        return objects

    def gen_distractor_objects(self, type1_exclude, type2_exclude):
        '''
        type1_exclude includes attributes of the same type to be excluded
        type2_exclude includes attributes of the other type to be excluded
        '''
        object_list = []
        num_AB = random.randint(
            self.num_distractors[0], self.num_distractors[1])
        for i in range(num_AB):
            if type1_exclude:
                type1_list = list(
                    filter(lambda x: x not in type1_exclude, list(type(type1_exclude[0]))))
            if type2_exclude:
                type2_list = list(
                    filter(lambda x: x not in type2_exclude, list(type(type2_exclude[0]))))
            A = random.choice(type1_list)
            B = random.choice(type2_list)
            shape = A if type(A) == Shapes else B
            colour = A if type(A) == Colours else B
            object_list.append(Obj(shape, colour, None))
        return object_list

    def get_objects_all_rel(self, X, Y, num1, num2):
        """
        All X are Y. 

        Construct num1 (X, Y) or (Y, X) objects.
        Construct num2 (Z, Y) or (Y, Z) objects.
        Construct remaining objects as (A, B).
        """
        object_list = []
        num_XY = num1
        object_list += self.gen_queried_objects(X, Y, num_XY)

        Z = random.choice(list(filter(lambda x: x != X, list(type(X)))))
        num_ZY = num2
        object_list += self.gen_queried_objects(Z, Y, num_ZY)

        object_list += self.gen_distractor_objects([X, Z], [Y])
        return object_list

    def get_objects_not_all_rel(self, X, Y, num1, num2):
        """
        Not all X are Y. 

        Construct number (X, Y) or (Y, X) objects.
        Construct 1-3 (X, Z) or (Z, X) objects.
        Construct remaining objects as (A, B).
        """
        object_list = []
        num_XY = num1
        object_list += self.gen_queried_objects(X, Y, num_XY)

        Z = random.choice(list(filter(lambda x: x != Y, list(type(Y)))))
        num_ZX = num2
        object_list += self.gen_queried_objects(Z, X, num_ZX)

        object_list += self.gen_distractor_objects([X, Z], [Y])
        return object_list

    def get_objects_none_rel(self, X, Y, num1, num2):
        """
        No Xs are Y. 

        Construct num1 (X,Z) or (Z, X) objects 
        Construct num2 (Y,W) or (W, Y) objects
        Construct remaining objects as (A, B)
        """
        object_list = []
        Z = random.choice(list(filter(lambda x: x != Y, list(type(Y)))))
        num_ZX = num1
        object_list += self.gen_queried_objects(Z, X, num_ZX)

        W = random.choice(list(filter(lambda x: x != X, list(type(X)))))
        num_WY = num2
        object_list += self.gen_queried_objects(W, Y, num_WY)

        object_list += self.gen_distractor_objects([X, Z], [Y, W])
        return object_list

    def get_objects_some_rel(self, X, Y, num1, num2):
        """
        Some Xs are Y. 

        Construct num2 (X,Y) or (Y,X) objects 
        Construct num1 (X,Z) or (Z,X) objects
        # Optionally, construct one (Y, W) or (W, Y) object 
        Construct remaining objects as (A, B)
        """
        object_list = []
        num_XY = num2
        object_list += self.gen_queried_objects(X, Y, num_XY)

        Z = random.choice(list(filter(lambda x: x != Y, list(type(Y)))))
        num_ZX = num1
        object_list += self.gen_queried_objects(Z, X, num_ZX)

        # W = random.choice(list(filter(lambda x: x != X, list(type(X)))))
        # num_WY = num1
        # object_list += self.gen_rand_objects(W, Y, num_WY)

        object_list += self.gen_distractor_objects([X, Z], [Y])
        return object_list

    def get_objects_only_rel(self, X, Y, num1, num2):
        """
        Only Xs are Y. 

        Construct num1 (X,Y) or (Y,X) objects.
        Construct num2 (X,Z) or (Z,X) objects.
        Construct remaining objects as (A, B)
        """
        object_list = []
        num_XY = num1
        object_list += self.gen_queried_objects(X, Y, num_XY)

        Z = random.choice(list(filter(lambda x: x != Y, list(type(Y)))))
        num_ZX = num2
        object_list += self.gen_queried_objects(Z, X, num_ZX)

        object_list += self.gen_distractor_objects([X, Z], [Y])
        return object_list

    def get_objects_not_only_rel(self, X, Y, num1, num2):
        """
        Not only Xs are Y. 

        Construct num1 (X,Y) or (Y,X) objects.
        Construct num2 (W,Y) or (Y,W) objects.
        # Optionally, construct some (X,Z) or (Z,X) objects.
        Construct remaining objects as (A, B)
        """
        object_list = []
        num_XY = num1
        object_list += self.gen_queried_objects(X, Y, num_XY)

        W = random.choice(list(filter(lambda x: x != X, list(type(X)))))
        num_WY = num2
        object_list += self.gen_queried_objects(W, Y, num_WY)

        # Z = random.choice(list(filter(lambda x: x != Y, list(type(Y)))))
        # num_ZX = random.randint(1, 3)
        # object_list += self.gen_rand_objects(Z, X, num_ZX)

        object_list += self.gen_distractor_objects([X, W], [Y])
        return object_list
