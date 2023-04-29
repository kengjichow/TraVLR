from ImageGen import ImageGen
from MetadataGen import MetadataGen
from Settings import Settings

from Enums import Shapes
from .CardinalityConditionGen import CardinalityConditionGen


class CardinalityMetadataGen(MetadataGen):
    def __init__(self, metadata_file):
        super().__init__(metadata_file)
        self.settings = Settings(
            num_rows=6, num_cols=6, num_objs=3, num_test_objs=3, single_template=False)
        self.image_gen = ImageGen(self.settings.image_height, self.settings.image_width,
                                  self.settings.num_rows, self.settings.num_cols)

    def gen_dataset(self):
        conditions = []
        for row in self.df.itertuples():
            object_list = self.convert_to_objs(row.objects)
            train = row.split
            attr = Shapes(row.query_abstract["attr"])
            number = row.query_abstract["number"]
            caption_abstract = row.caption_abstract
            gen = CardinalityConditionGen(
                    object_list, attr, number, self.settings, self.image_gen, train)
            conditions += gen.gen_condition(1, caption_abstract=caption_abstract)
        self.output(conditions)
