from .CardinalityRelationship import Relationship
from CaptionGen import CaptionGen
import random


class CardinalityQueryGen(CaptionGen):
    def __init__(self, object_list, queried_attr, number, settings, rel=Relationship.EQUAL):
        '''
        queried_attr: e.g. "red", "circle"
        number: number of objects stated in query
        '''
        self.object_list = object_list
        self.settings = settings
        self.queried_attr = queried_attr
        self.number = number
        self.rel = rel

    def gen_queries(self):
        results = []
        templates = self.read_templates('CardinalityDatasetGen/query_template.txt')
        template = templates[0] if self.settings.single_template else random.choice(
            templates)
        if self.rel == Relationship.EQUAL:
            results.append({
                "query": self.gen_query(template),
                "answer": self.gen_answer(),
                "query_abstract": self.gen_query_abstract()
            })
        else:
            results.append({
                "query": self.gen_compare_query(template),
                "answer": self.gen_compare_answer(),
                "query_abstract": self.gen_query_abstract()
            })
        return results

    def gen_query_abstract(self):
        result = {}
        result['attr'] = self.queried_attr.value
        result['number'] = self.number
        result['rel'] = self.rel
        return result

    def gen_query(self, template):
        template = template.split()
        result = []
        for w in template:
            if w == "{attr}":
                result.append(self.queried_attr.value)
            elif w == "{number}":
                result.append(str(self.number))
                # result.append(self.get_number_word(self.number))
            elif w == "{copula}":
                word = "is" if self.number == 1 else "are"
                result.append(word)
            elif w == "{objects}":
                word = "object" if self.number == 1 else "objects"
                result.append(word)
            else:
                result.append(w)
        result = " ".join(result) + "."
        return result
    
    def gen_compare_query(self, template):
        template = template.split()
        result = []
        for w in template:
            if w == "{attr}":
                result.append(self.queried_attr.value)
            elif w == "{number}":
                result.append("more than " + str(self.number))
            else:
                result.append(w)
        result = " ".join(result) + "."
        return result

    def gen_compare_answer(self):
        return len(list(filter(lambda x: x.hasAttr(self.queried_attr), self.object_list))) > self.number

    def gen_answer(self):
        return len(list(filter(lambda x: x.hasAttr(self.queried_attr), self.object_list))) == self.number
