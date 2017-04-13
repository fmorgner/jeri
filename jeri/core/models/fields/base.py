from inspect import isclass
from jeri.core.models.manager.related import RelatedManager


class Field:
    """
    A generic base class for all Field. It main purpose is to handle field
    registration and provide generic hydration functionality
    """

    def __init__(self, name=None, dried_name=None, **kwargs):
        if len(kwargs) != 0:
            raise AttributeError('Unexpected arguments {}'.format(kwargs))
        self.name = name
        if dried_name:
            self.dried_name = dried_name
        elif self.name:
            self.dried_name = name.lower()

    def __repr__(self):
        fstring = '{module}.{class}: {name}@{dried_name}'
        data = {
            'module': self.__class__.__module__,
            'class': self.__class__.__name__,
            'name': self.name,
            'dried_name': self.dried_name
        }
        return fstring.format_map(data)

    def __str__(self):
        fstring = '{model_name}.{name}'
        data = {
            'model_name': self.model._meta.model_name,
            'name': self.name
        }
        return fstring.format_map(data)

    def apply_to_class(self, cls, name):
        if self.name is None:
            self.name = name
            self.dried_name = self.name.lower()
        self.model = cls
        cls._meta.add_field(self)
        setattr(cls, self.name, self)

    def hydrate(self, object, data):
        setattr(object, self.name, data)


class RelatedField(Field):

    def __init__(self, to, lazy=True, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.to = to
        self.lazy = lazy
        self.manager = RelatedManager

    def apply_to_class(self, cls, name):
        super().apply_to_class(cls, name)
        if isclass(self.to) and hasattr(self.to, '_meta'):
            return
        assert(type(self.to) == str)
        cls._meta.add_model_callback(self.resolve_model_references)

    def resolve_model_references(self, models):
        if self.to not in models:
            raise RuntimeError('Unresolvable model type {}'.format(self.to))
        self.to = models[self.to]
