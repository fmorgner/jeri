from jeri.core.models.manager.base import Manager


class ObjectManager(Manager):

    def __init__(self):
        self.cache = []

    def _find_object(self, **kwargs):
        for object in self.cache:
            matches = True
            for attr, value in kwargs.items():
                attr = getattr(object, attr)
                matches &= attr == value
            if matches:
                return object

    def _all(self):
        if len(self.cache) is 0:
            app = self.model._meta.app
            objects = app.backend.get_all(self.model)
            self.cache = [self.model(**o) for o in objects]
        return self.cache.copy()

    def _count(self):
        return len(self.cache)

    def _get(self, **kwargs):
        object = self._find_object(**kwargs)
        if object is None:
            app = self.model._meta.app
            data = app.backend.get(self.model, **kwargs)
            object = self.model(**data)
            self.cache.append(object)
        return object
