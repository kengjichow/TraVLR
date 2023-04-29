from .QuantifierRelationship import Relationship
from CaptionGen import CaptionGen
import random


class QuantifierQueryGen(CaptionGen):
    def __init__(self, object_list, case, settings):
        self.object_list = object_list
        self.case = case
        self.settings = settings

    def gen_queries(self):
        results = []
        templates = self.read_templates('QuantifierDatasetGen/query_template.txt')
        template = templates[0] if self.settings.single_template else random.choice(
            templates)
        rel, X, Y = self.case[0], self.case[1], self.case[2] 

        results.append({
            "query": self.gen_query(template, rel, X, Y),
            "answer": Relationship.evaluate(rel, X, Y, self.object_list),
            "query_abstract": self.gen_query_abstract(rel, X, Y)
        })
        return results

    def gen_query_abstract(self, rel, X, Y):
        query_abstract = {}
        query_abstract["rel"] = rel
        query_abstract["attr1"] = X
        query_abstract["attr2"] = Y
        return query_abstract

    def gen_query(self, template, rel, X, Y):
        template = template.split()
        result = []
        for w in template:
            if w == "{rel}":
                result.append(rel.value)
            elif w == "{X}":
                result.append(X.value)
            elif w == "{Y}":
                result.append(Y.value)
            else:
                result.append(w)
        result = " ".join(result) + "."
        result = result[0].upper()+result[1:]
        return result