from CompareDatasetGen.CompareRelationship import Relationship
from CaptionGen import CaptionGen
from CaptionGen import CaptionGen
import random


class CompareQueryGen(CaptionGen):
    def __init__(self, object_list, case, settings):
        self.object_list = object_list
        self.settings = settings
        self.case = case

    def gen_queries(self):
        results = []
        templates = self.read_templates('CompareDatasetGen/query_template.txt')
        template = templates[0] if self.settings.single_template else random.choice(
            templates)
        rel, X, Y = self.case[0], self.case[1], self.case[2]

        results.append({
            "query": self.gen_query(template, rel, X, Y),
            "answer": self.gen_answer(rel, X, Y),
            "query_abstract": self.gen_query_abstract(rel, X, Y)
        })
        return results

    def gen_query(self, template, rel, X, Y):
        template = template.split()
        result = []
        for w in template:
            if w == "{rel}":
                result.append(rel.value)
            elif w == "{X}":
                result.append(X.value + 's')
            elif w == "{Y}":
                result.append(Y.value + 's')
            else:
                result.append(w)
        result = " ".join(result) + "."
        return result

    def gen_query_abstract(self, rel, X, Y):
        result = {}
        result['attr1'] = X
        result['attr2'] = Y
        result['rel'] = rel
        return result

    def gen_answer(self, rel, X, Y):
        numX = len(list(filter(lambda x: x.hasAttr(X), self.object_list)))
        numY = len(list(filter(lambda x: x.hasAttr(Y), self.object_list)))
        answer = Relationship.get_answer(numX, numY)
        return rel == answer
