from ImageGen import ImageGen
from .SpatialRelationship import Relationship
import Enums
import random
from .SpatialCaptionGen import SpatialCaptionGen
from .SpatialQueryGen import SpatialQueryGen


class SpatialConditionGen:
    def __init__(self, object_list, relationship, settings, image_gen):
        self.object_list = object_list
        self.relationship = relationship
        self.settings = settings
        self.image_gen = image_gen

    def gen_condition(self, num_results):
        """
        If self.relationship, then the query and caption/image matches. Else the query and image/caption is mismatched.
        """
        self.prepare_obj_list()
        queries = SpatialQueryGen(
            [self.object_list[0]], self.relationship, self.settings).gen_queries()

        if self.relationship:
            captions = SpatialCaptionGen(
            [self.object_list[0]], self.relationship, self.settings).gen_captions()
            self.image_gen.draw_objects([self.object_list[0]])
            image = self.image_gen.save_image()
        else:
            captions = SpatialCaptionGen(
            [self.object_list[1]], self.relationship, self.settings).gen_captions()
            self.image_gen.draw_objects([self.object_list[1]])
            image = self.image_gen.save_image()

        result = []
        for caption in captions:
            for query in queries:
                result.append({
                    "caption": caption,
                    "query": query,
                    "answer": (self.relationship),
                    "code": (self.relationship),
                    "image": image
                })

        result = random.sample(result, num_results)
        return result

    def prepare_obj_list(self):
        positions = [(0,0), (0,1), (0,2), (1,0), (1,1), (1,2), (2,0), (2,1), (2,2)]
        for i in range(len(self.object_list)):
            position = random.choice(positions)
            self.object_list[i].setPosition(position[0], position[1])
            positions.remove(position)

        for i in range(len(self.object_list)):
            self.object_list[i].setSize(Enums.Size.MEDIUM)