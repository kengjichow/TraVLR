from enum import Enum


class Relationship(str, Enum):
    ALL = "all"
    NOTALL = "not all"
    SOME = "some of"
    NONE = "none of"
    ONLY = "only"
    NOT_ONLY = "not only"

    def evaluate(rel, X, Y, object_list):
        if rel == Relationship.ALL:
            return Relationship.evaluate_all(X, Y,object_list)
        elif rel == Relationship.NOTALL:
            return Relationship.evaluate_not_all(X, Y, object_list)
        elif rel == Relationship.ONLY:
            return Relationship.evaluate_only(X, Y, object_list)
        elif rel == Relationship.NOT_ONLY:
            return Relationship.evaluate_not_only(X, Y, object_list)
        elif rel == Relationship.SOME:
            return Relationship.evaluate_some(X, Y, object_list)
        elif rel == Relationship.NONE:
            return Relationship.evaluate_none(X, Y, object_list)

    def evaluate_all(X, Y, object_list):
        Xs = list(filter(lambda x: x.hasAttr(X), object_list))
        Ys = list(filter(lambda x: x.hasAttr(Y), Xs))
        return len(Xs) == len(Ys)

    def evaluate_not_all(X, Y, object_list):
        Xs = list(filter(lambda x: x.hasAttr(X), object_list))
        Ys = list(filter(lambda x: x.hasAttr(Y), Xs))
        return len(Xs) > len(Ys)

    def evaluate_some(X, Y, object_list):
        Xs = list(filter(lambda x: x.hasAttr(X), object_list))
        Ys = list(filter(lambda x: x.hasAttr(Y), Xs))
        return len(Ys) > 0

    def evaluate_none(X, Y, object_list):
        Xs = list(filter(lambda x: x.hasAttr(X), object_list))
        Ys = list(filter(lambda x: x.hasAttr(Y), Xs))
        return len(Ys) == 0

    def evaluate_only(X, Y, object_list):
        Ys = list(filter(lambda x: x.hasAttr(Y), object_list))
        Xs = list(filter(lambda x: x.hasAttr(X), Ys))
        return len(Ys) == len(Xs)

    def evaluate_not_only(X, Y, object_list):
        Ys = list(filter(lambda x: x.hasAttr(Y), object_list))
        Xs = list(filter(lambda x: x.hasAttr(X), Ys))
        return len(Ys) > len(Xs)


