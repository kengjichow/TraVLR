import os
import random

import jsonlines
import numpy as np
import pandas as pd

from const import INDEX_FILEPATH
from Enums import Colours, Shapes
from Obj import Obj


class DatasetGen:
    def split_val(self, train_conditions, num_train, num_val, num_val_test):
        train_conditions, val_conditions, val_test_conditions = np.split(train_conditions, [
            int(len(train_conditions)*(num_train/(num_train+num_val+num_val_test))),
            int(len(train_conditions)*((num_train+num_val) /
                (num_train+num_val+num_val_test))),
        ])
        self.label_split(val_conditions, "val")
        self.label_split(val_test_conditions, "val_test")
        return list(train_conditions), list(val_conditions), list(val_test_conditions)

    def label_split(self, conditions, split):
        for cond in conditions:
            cond['split'] = split
            cond['metadata']['split'] = split

    def output_split(self, train_conditions, test_conditions, num_conditions):
        num_train = num_conditions['num_train']
        num_val = num_conditions['num_val']
        num_val_test = num_conditions['num_val_test']
        num_test = num_conditions['num_test']

        train_conditions = random.sample(
            train_conditions, num_train + num_val + num_val_test)
        test_conditions = random.sample(test_conditions, num_test)
        train_conditions, val_conditions, val_test_conditions = self.split_val(
            train_conditions, num_train, num_val, num_val_test)

        conditions = train_conditions + val_conditions + \
            val_test_conditions + test_conditions
        self.output(conditions)

    def output(self, conditions):
        with jsonlines.open(INDEX_FILEPATH + 'metadata.jsonl', mode='w') as writer:
            metadata = [{k: v for k, v in enumerate(
                map(lambda x: x["metadata"], conditions))}]
            writer.write_all(metadata)
        df = pd.DataFrame.from_dict(conditions)
        df = df.drop(columns=['metadata'])
        df.to_csv(INDEX_FILEPATH + "index.csv")
        
        unused_images = [i for i in range(self.image_gen.image_idx)]
        unused_images = list(
            filter(lambda x: x not in list(df['image']), unused_images))
        for image in unused_images:
            os.remove("{}images/{}.jpg".format(INDEX_FILEPATH, str(image)))

    def gen_rand_objs(self, attr, num_objs, for_query=True):
        objects = []
        attr_type = type(attr)
        for i in range(num_objs):
            shape = attr if attr_type == Shapes else random.choice(self.shapes)
            colour = attr if attr_type == Colours else random.choice(
                self.colours)
            obj = Obj(shape, colour, None)
            obj.for_query = for_query
            objects.append(obj)
        return objects

    def gen_unique_distractor_list(self, max_num_objects, exclude_attr=[]):
        if not self.unique_distractor_lists:
            self.unique_distractor_lists = []
        num_objects = random.randint(1, max_num_objects)
        distractor_objs = self.gen_distractor_objs(num_objects, exclude_attr)
        distractor_objs_tuple = self.get_object_list_tuple(distractor_objs)
        while distractor_objs_tuple in self.unique_distractor_lists:
            num_objects = random.randint(1, max_num_objects)
            distractor_objs = self.gen_distractor_objs(
                num_objects, exclude_attr)
            distractor_objs_tuple = self.get_object_list_tuple(distractor_objs)
        self.unique_distractor_lists.append(distractor_objs_tuple)
        return distractor_objs

    def get_object_list_tuple(self, object_list):
        return sorted(
            tuple(map(lambda obj: (obj.colour.value, obj.shape.value), object_list)))

    def clear_unique_distractor_list(self):
        self.unique_distractor_lists = []

    def gen_distractor_objs(self, num_objects, exclude_attr=[]):
        object_list = []
        while len(object_list) < num_objects:
            colour = random.choice(
                list(filter(lambda x: x not in exclude_attr, self.colours)))
            shape = random.choice(
                list(filter(lambda x: x not in exclude_attr, self.shapes)))
            obj = Obj(shape, colour, None)
            obj.for_query = False
            object_list.append(obj)
        return object_list
