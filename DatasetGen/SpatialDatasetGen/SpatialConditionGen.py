import itertools
from .SpatialRelationship import Relationship
import Enums
import random
from .SpatialCaptionGen import SpatialCaptionGen
from .SpatialQueryGen import SpatialQueryGen

### Number of captions/queries to select per scene/condition.
NUM_CAPTIONS = 1

class SpatialConditionGen:
    def __init__(self, object_list, relationship, settings, image_gen, train):
        self.object_list = object_list
        self.relationship = relationship
        self.settings = settings
        self.image_gen = image_gen
        self.train = train

    def get_metadata(self, query, answer, query_abstract, caption_abstract):
        output = {
            "objects": [obj.__dict__() for obj in self.object_list],
            "relationship": self.relationship,
            "split": self.train,
            "query": query,
            "answer": answer,
            "query_abstract": query_abstract,
            "caption_abstract": caption_abstract
        }
        return output

    def gen_unique_conditions(self, positions, num_captions=NUM_CAPTIONS):
        """
        Generates unique conditions for the given object list, with all possible positions based on the relationship.
        Size: arranged from small to large.
        Position: arranged from left to right (HORIZONTAL, DIAGONAL_UP, DIAGONAL_DOWN), or top to bottom (VERTICAL)

        NUM_POSITIONS: the number of positions to randomly select as a subset of all possible positions.
        NUM_CAPTIONS: the number of captions/query/answer tuples to randomly select
        """
        unique_conditions = []
        for position in positions:
            obj_list = []
            for i in range(len(self.object_list)):
                obj = self.object_list[i]
                obj.setPosition(position[i][0], position[i][1])
                self.object_list[i].setSize(Enums.Size.MEDIUM)
                obj_list.append(obj)
            self.object_list = obj_list
            unique_conditions += self.gen_condition(num_captions)
        return unique_conditions

    def gen_condition(self, num_results, caption_abstract=None, query_abstract=None):
        """
        Generates a condition: each condition has a single image, and several caption/query/answer pairs.

        Left/right in caption:
        If there are 2 objects: there are 2 possible captions and 4 possible queries.
        If there are 3 objects: there are 4 possible captions and 12 possible queries.

        Chessboard notation in caption:
        If there are 2 objects: there are 2 possible captions and 4 possible queries.   
        If there are 3 objects: there are 6 possible captions and 12 possible queries.

        num_results: number of caption/query/answer pairs to return (default: 1)
        """
        captions = SpatialCaptionGen(self.object_list, self.relationship, self.settings).gen_caption_exact(
            self.train, caption_abstract=caption_abstract)
        if query_abstract is not None:
            queries = SpatialQueryGen(
                self.object_list, self.relationship, self.settings).gen_query_exact(query_abstract)
        else:
            queries = SpatialQueryGen(
                self.object_list, self.relationship, self.settings).gen_all_poss_queries()
        self.image_gen.draw_objects(self.object_list)
        image = self.image_gen.save_image()

        result = []
        for caption in captions:
            for query in queries:
                result.append({
                    "caption": caption['caption'],
                    "query": query['query'],
                    "answer": query['answer'],
                    "positions": [(obj.row, obj.column) for obj in self.object_list],
                    "image": image,
                    "split": self.train,
                    "metadata": self.get_metadata(query['query'],
                                                  query['answer'],
                                                  query['query_abstract'],
                                                  caption['caption_abstract'])
                })

        if num_results is not None:
            result = random.sample(result, num_results)
        return result

    def prepare_obj_list(self):
        """
        Randomly sets position and size of objects in object_list based on relationship.
        Size: arranged from small to large
        Position: arranged from left to right (HORIZONTAL, DIAGONAL_UP, DIAGONAL_DOWN), or top to bottom (VERTICAL)
        """
        positions = random.choice(
            Relationship.get_valid_positions(self.relationship, self.settings))
        for i in range(len(self.object_list)):
            position = random.choice(positions)
            self.object_list[i].setPosition(position[0], position[1])
            positions.remove(position)

        if self.relationship == Relationship.SIZE:
            self.object_list[0].setSize(Enums.Size.SMALL)
            self.object_list[1].setSize(Enums.Size.MEDIUM)
            self.object_list[2].setSize(Enums.Size.LARGE)
        else:
            for i in range(len(self.object_list)):
                self.object_list[i].setSize(Enums.Size.MEDIUM)
            if self.relationship in [Relationship.HORIZONTAL, Relationship.DIAGONAL_UP, Relationship.DIAGONAL_DOWN]:
                self.object_list.sort(key=lambda obj: obj.column)
            elif self.relationship == Relationship.VERTICAL:
                self.object_list.sort(key=lambda obj: obj.row)
        return self.object_list
