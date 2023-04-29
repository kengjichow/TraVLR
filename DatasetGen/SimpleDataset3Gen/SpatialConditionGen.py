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
        Three objects are provided. Two will be the object in the list. 
        The last object is used for the query in the incorrect case
        """
        wrong_object_list = self.object_list[2:]
        self.object_list = self.object_list[:2]

        self.prepare_obj_list()
        captions = SpatialCaptionGen(
            self.object_list, self.relationship, self.settings).gen_captions()
        self.image_gen.draw_objects(self.object_list)
        image = self.image_gen.save_image()

        if correct:
            queries = SpatialQueryGen(
                self.object_list, self.relationship, self.settings).gen_queries()
        else:
            queries = SpatialQueryGen(
                wrong_object_list, self.relationship, self.settings).gen_queries()

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
        positions = [(0,0), (0,1), (0,2), (1,0), (1,1), (1,2), (2,0), (2,1), (2,2)]
        for i in range(len(self.object_list)):
            position = random.choice(positions)
            self.object_list[i].setPosition(position[0], position[1])
            positions.remove(position)

        for i in range(len(self.object_list)):
            #size = random.choice(list(Enums.Size))
            self.object_list[i].setSize(Enums.Size.MEDIUM)
