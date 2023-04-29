from ImageGen import ImageGen
from MetadataGen import MetadataGen
from Settings import Settings

from .CompareConditionGen import CompareConditionGen
from .CompareRelationship import Relationship
from Enums import Shapes


class CompareMetadataGen(MetadataGen):
    def __init__(self, metadata_file):
        super().__init__(metadata_file)
        self.settings = Settings(
            num_rows=6, num_cols=6, num_objs=3, num_test_objs=3, single_template=False)
        self.image_gen = ImageGen(self.settings.image_height, self.settings.image_width,
                                  self.settings.num_rows, self.settings.num_cols)

    def gen_dataset(self):
        conditions = []
        for row in self.df.itertuples():
            objects = self.convert_to_objs(row.objects)
            train = row.split
            case = row.case
            case = (Relationship(case[0]), Shapes(case[1]), Shapes(case[2])) + tuple(case[3:])
            caption_abstract = row.caption_abstract
            gen = CompareConditionGen(objects, case, self.settings, self.image_gen, train)
            conditions += gen.gen_condition(1, caption_abstract)
        self.output(conditions)
