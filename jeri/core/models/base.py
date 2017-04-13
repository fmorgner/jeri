from inspect import isclass
from jeri.core.models.manager import ObjectManager
from jeri.core.models.meta import Meta


class MetaModel(type):

    def __new__(cls, name, bases, attributes):
        if not [base for base in bases if isinstance(base, MetaModel)]:
            return super().__new__(cls, name, bases, attributes)

        new_attributes = {'__module__': attributes.pop('__module__')}
        if '__classcell__' in attributes:
            new_attributes['__classcell__'] = attributes.pop('__classcell__')
        new_class = super().__new__(cls, name, bases, new_attributes)

        meta = attributes.pop('Meta', None)
        if not meta:
            meta = getattr(new_class, 'Meta', None)
        new_class.apply_to_class('_meta', Meta(meta))

        manager = ObjectManager()
        new_class.apply_to_class('objects', manager)

        for attribute_name, attribute in attributes.items():
            new_class.apply_to_class(attribute_name, attribute)

        return new_class

    def apply_to_class(cls, name, obj):
        if not isclass(obj) and hasattr(obj, 'apply_to_class'):
            obj.apply_to_class(cls, name)
        else:
            setattr(cls, name, obj)

    def set_application(cls, app):
        if hasattr(cls, '_meta'):
            cls._meta.set_application(app)


class Model(metaclass=MetaModel):

    id = None
    uri = None

    def __init__(self, **kwargs):
        field_iterator = iter(self._meta.fields)
        for field in field_iterator:
            if field.name in kwargs:
                value = kwargs.pop(field.name)
                field.hydrate(self, value)
        if self._meta.app.backend.id_key in kwargs:
            self.id = kwargs[self._meta.app.backend.id_key]
        if self._meta.app.backend.uri_key in kwargs:
            self.uri = kwargs[self._meta.app.backend.uri_key]
