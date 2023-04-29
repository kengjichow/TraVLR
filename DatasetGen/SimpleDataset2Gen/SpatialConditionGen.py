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

    def gen_condition(self, num_results, correct):
        """
        If correct, then the query and caption/image matches. Else the query and image/caption is mismatched.
        """
        if correct:
            queries = SpatialQueryGen(
                [self.object_list[0]], self.relationship, self.settings).gen_queries()
        else:
            false_relationship = random.choice(list(filter(lambda x: x != self.relationship, [
                                               "left", "right"])))
            queries = SpatialQueryGen(
                [self.object_list[0]], false_relationship, self.settings).gen_queries()

        self.prepare_obj_list()
        captions = SpatialCaptionGen(
            [self.object_list[0]], self.relationship, self.settings).gen_captions()
        self.image_gen.draw_objects(self.object_list)
        image = self.image_gen.save_image()

        result = []
        for caption in captions:
            for query in queries:
                result.append({
                    "caption": caption,
                    "query": query,
                    "answer": correct,
                    "code": correct,
                    "image": image
                })

        result = random.sample(result, num_results)
        return result

    def prepare_obj_list(self):
        positions = [0,1,2]
        for i in range(len(self.object_list)):
            if self.relationship == "left":
                position = random.choice(positions)
                self.object_list[i].setPosition(position, 0)
                positions.remove(position)
            if self.relationship == "top":
                position = random.choice(positions)
                self.object_list[i].setPosition(0, position)
                positions.remove(position)
            if self.relationship == "bottom":
                position = random.choice(positions)
                self.object_list[i].setPosition(2, position)
                positions.remove(position)
            if self.relationship == "right":
                position = random.choice(positions)
                self.object_list[i].setPosition(position, 2)
                positions.remove(position)
            if self.relationship == "centre":
                self.object_list[i].setPosition(1, 1)

        for i in range(len(self.object_list)):
            size = random.choice(list(Enums.Size))
            self.object_list[i].setSize(size)
