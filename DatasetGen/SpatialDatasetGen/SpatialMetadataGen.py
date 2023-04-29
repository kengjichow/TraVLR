
from ImageGen import ImageGen
from MetadataGen import MetadataGen
from Settings import Settings

from .SpatialConditionGen import SpatialConditionGen
from .SpatialRelationship import Relationship


class SpatialMetadataGen(MetadataGen):
    def __init__(self, metadata_file):
        super().__init__(metadata_file)
        self.settings = Settings(
            num_rows=6, num_cols=6, num_objs=3, num_test_objs=3, single_template=False)
        self.image_gen = ImageGen(self.settings.image_height, self.settings.image_width,
                                  self.settings.num_rows, self.settings.num_cols)

    def gen_dataset(self):
        conditions = []
        for row in self.df.itertuples():
            rel = Relationship(row.relationship)
            object_list = self.convert_to_objs(row.objects)
            split = row.split
            condition = SpatialConditionGen(object_list, rel, self.settings, self.image_gen, split).gen_condition(
                1, row.caption_abstract, row.query_abstract)
            conditions += condition
        self.output(conditions)
