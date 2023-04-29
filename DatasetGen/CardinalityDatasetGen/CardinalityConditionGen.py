import itertools
import Enums
import random
from .CardinalityCaptionGen import CardinalityCaptionGen
from .CardinalityQueryGen import CardinalityQueryGen


class CardinalityConditionGen:
    def __init__(self, object_list, queried_attr, number, settings, image_gen, train):
        self.object_list = object_list
        self.queried_attr = queried_attr
        self.number = number
        self.settings = settings
        self.image_gen = image_gen
        self.train = train

    def get_metadata(self, query, answer, caption_abstract, query_abstract):
        output = {
            "objects": [obj.__dict__() for obj in self.object_list],
            "case": (self.queried_attr, self.number),
            "query": query,
            "answer": answer,
            "caption_abstract": caption_abstract,
            "query_abstract": query_abstract,
            "split": self.train,
        }
        return output

    def gen_condition(self, num_results, caption_abstract=None):
        self.prepare_obj_list()
        captions = CardinalityCaptionGen(
            self.object_list, self.settings).gen_caption_exact(self.train, caption_abstract=caption_abstract)
        queries = CardinalityQueryGen(
            self.object_list, self.queried_attr, self.number, self.settings).gen_queries()
        self.image_gen.draw_objects(self.object_list)
        image = self.image_gen.save_image()

        result = []
        for caption in captions:
            for query in queries:
                result.append({
                    "caption": caption['caption'],
                    "query": query['query'],
                    "answer": query['answer'],
                    "image": image,
                    "split": self.train,
                    "metadata": self.get_metadata(
                        query['query'],
                        query['answer'],
                        caption['caption_abstract'],
                        query['query_abstract'],)
                })

        if num_results is not None:
            result = random.sample(result, num_results)
        return result

    def prepare_obj_list(self):
        positions = [[i, j] for i in range(
            self.settings.num_rows) for j in range(self.settings.num_cols)]
        selected_positions = random.sample(positions, len(self.object_list))
        random.shuffle(selected_positions)
        for i in range(len(self.object_list)):
            self.object_list[i].setPosition(
                selected_positions[i][0], selected_positions[i][1])
            self.object_list[i].setSize(Enums.Size.MEDIUM)
        return self.object_list
