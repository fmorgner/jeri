from jeri.core.models.manager.base import Manager


class RelatedManager(Manager):

    def __init__(self, wrapped):
        self.wrapped = wrapped
        self.relations = set()
        pass

    def _all(self):
        objects = []
        for uri in self.relations:
            objects.append(self.wrapped.get(uri=uri))
        return objects

    def _count(self):
        return len(self.relations)

    def _get(self, **kwargs):
        pass

    def add_relation(self, uri):
        self.relations.add(uri)
