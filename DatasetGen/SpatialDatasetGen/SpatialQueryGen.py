from CaptionGen import CaptionGen
from .SpatialRelationship import Relationship
from const import SPATIAL_DATASET_TEMPLATE, SPATIAL_DATASET_TEMPLATE_2
import random


class SpatialQueryGen(CaptionGen):
    def __init__(self, object_list, relationship, settings):
        self.object_list = object_list
        self.relationship = relationship
        self.settings = settings

    def gen_query_exact(self, query_abstract):
        '''
        Returns the query based on the abstract query.
        '''
        templates = self.read_templates(SPATIAL_DATASET_TEMPLATE)
        template = templates[0]
        obj1 = self.object_list[query_abstract[0]]
        rel = query_abstract[1]
        obj2 = self.object_list[query_abstract[2]]
        result = []
        result.append({
            "query": self.gen_caption_two_objs(template, obj1, obj2, rel),
            "answer": self.gen_answer(obj1, obj2, self.relationship),
            "query_abstract": query_abstract
        })
        return result

    def gen_queries(self):
        """
        Returns the exact query without swapping the order of the objects.
        """
        result = []
        first_rel, second_rel = Relationship.get_rel(self.relationship)
        templates = self.read_templates(SPATIAL_DATASET_TEMPLATE)
        template = templates[0] # if self.settings.single_template else random.choice(templates)

        obj1 = self.object_list[0]
        obj2 = self.object_list[1]

        result.append({
            "query": self.gen_caption_two_objs(template, obj1, obj2, first_rel),
            "answer": self.gen_answer(obj1, obj2, self.relationship),
            "query_abstract": [0, first_rel, 1]
        })
        result.append({
            "query": self.gen_caption_two_objs(template, obj1, obj2, second_rel),
            "answer": not self.gen_answer(obj1, obj2, self.relationship),
            "query_abstract": [0, second_rel, 1]
        })
        return result

    def gen_all_poss_queries(self):
        """
        Returns all possible query/answer pairs, given a condition (represented by an object list) and relationship. 
        If there are 2 objects, there are 4 query/answer pairs returned.
        If there are 3 objects, there are 12 query/answer pairs returned.

        Given 3 objects (x, y, z) and relationships Rel/Rel' (e.g. Left/Right), the following queries are returned:
        0: Rel(x, y) , 1: Rel(x, z) , 2: Rel(y, x)  
        3: Rel(y, z) , 4: Rel(z, x) , 5: Rel(z, y)  
        6: Rel'(x, y) , 7: Rel'(x, z), 8: Rel'(y, x)  
        9: Rel'(y, z) , 10: Rel'(z, x)  , 11: Rel'(z, y)
        """
        result = []
        first_rel, second_rel = Relationship.get_rel(self.relationship)
        templates = self.read_templates(SPATIAL_DATASET_TEMPLATE)
        template = templates[0] # if self.settings.single_template else random.choice(templates)

        for obj1 in range(len(self.object_list)):
            for obj2 in range(len(self.object_list)):
                if obj1 is not obj2 and self.object_list[obj1].for_query and self.object_list[obj2].for_query:
                    result.append({
                        "query": self.gen_caption_two_objs(template, self.object_list[obj1], self.object_list[obj2], first_rel),
                        "answer": self.gen_answer(self.object_list[obj1], self.object_list[obj2], self.relationship),
                        "query_abstract": [obj1, first_rel, obj2]
                    })

                    result.append({
                        "query": self.gen_caption_two_objs(template, self.object_list[obj1], self.object_list[obj2], second_rel),
                        "answer": not self.gen_answer(self.object_list[obj1], self.object_list[obj2], self.relationship),
                        "query_abstract": [obj1, second_rel, obj2]
                    })
        return result

    def gen_answer(self, obj1, obj2, relationship):
        if relationship == Relationship.HORIZONTAL:
            return obj1.column < obj2.column
        elif relationship == Relationship.VERTICAL:
            return obj1.row < obj2.row
        elif relationship == Relationship.DIAGONAL_DOWN:
            return obj1.column < obj2.column and obj1.row < obj2.row
        elif relationship == Relationship.DIAGONAL_UP:
            return obj1.column < obj2.column and obj1.row > obj2.row
        elif relationship == Relationship.SIZE:
            return obj1.size.value < obj2.size.value
