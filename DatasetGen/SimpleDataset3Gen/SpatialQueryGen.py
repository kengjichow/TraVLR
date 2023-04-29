from SpatialDatasetGen.SpatialTextGen import SpatialTextGen
from .SpatialRelationship import Relationship
from const import SPATIAL_DATASET_TEMPLATE
import random


class SpatialQueryGen(SpatialTextGen):
    def __init__(self, object_list, relationship, settings):
        super().__init__(object_list, relationship, settings)

    def gen_queries(self):
        templates = self.read_templates(SPATIAL_DATASET_TEMPLATE)
        template = templates[0] if self.settings.single_template else random.choice(
            templates)
        return [self.gen_caption_two_objs(template, self.object_list[0], self.object_list[1], self.relationship)]