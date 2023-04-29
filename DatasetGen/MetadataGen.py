import os

import jsonlines
import pandas as pd

from const import INDEX_FILEPATH
from Enums import Colours, Shapes, Size
from Obj import Obj


class MetadataGen:
    def __init__(self, metadata_file):
        self.df = self.read_metadata(metadata_file=metadata_file)

    def read_metadata(self, metadata_file):
        with jsonlines.open(metadata_file) as reader:
            for obj in reader:
                df_original = pd.DataFrame(obj).T
        return df_original

    def convert_to_objs(self, objects):
        objects = list(map(lambda x: Obj(Shapes(x['shape']), Colours(
            x['colour']), None, position=[x['row'], x['column']]), objects))
        for obj in objects:
            obj.size = Size.MEDIUM
            obj.for_query = True
        return objects

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