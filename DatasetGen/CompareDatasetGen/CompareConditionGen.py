import Enums
import random
from .CompareCaptionGen import CompareCaptionGen
from .CompareQueryGen import CompareQueryGen


class CompareConditionGen:
    def __init__(self, object_list, case, settings, image_gen, train):
        self.object_list = object_list
        self.case = case
        self.settings = settings
        self.train = train
        self.image_gen = image_gen

    def get_metadata(self, query, answer, query_abstract, caption_abstract):
        output = {
            "objects": [obj.__dict__() for obj in self.object_list],
            "query": query,
            "answer": answer,
            "case": self.case,
            "query_abstract": query_abstract,
            "caption_abstract": caption_abstract,
            "split": self.train,
        }
        return output

    def gen_condition(self, num_results, caption_abstract=None):
        self.prepare_obj_list()
        captions = CompareCaptionGen(
            self.object_list, self.settings).gen_caption_exact(self.train, caption_abstract=caption_abstract)
        queries = CompareQueryGen(
            self.object_list, self.case, self.settings).gen_queries()
        self.image_gen.draw_objects(self.object_list)
        image = self.image_gen.save_image()

        result = []
        for caption in captions:
            for query in queries:
                result.append({
                    "caption": caption['caption'],
                    "query": query['query'],
                    "answer": query['answer'],
                    "split": self.train,
                    "image": image,
                    "metadata": self.get_metadata(
                        query['query'],
                        query['answer'],
                        query['query_abstract'],
                        caption['caption_abstract']
                    )
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
