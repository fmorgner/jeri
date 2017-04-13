from jeri.core.models.meta.error import MetaAttributeError


WELL_KNOWN_ATRRIBUTES = [
    'endpoint'
]


class Meta:

    def __init__(self, meta):
        self.endpoint = None
        self.fields = set()
        self.meta = meta
        self.model_callbacks = []

    def apply_to_class(self, cls, name):
        setattr(cls, name, self)
        self.model = cls

        self.class_name = cls.__name__
        self.model_name = self.class_name.lower()
        self.endpoint = self.model_name + 's'

        if self.meta:
            attributes = self.meta.__dict__.copy()
            for attr in self.meta.__dict__:
                if attr.startswith('_'):
                    del attributes[attr]

            for attr in WELL_KNOWN_ATRRIBUTES:
                if attr in attributes:
                    setattr(self, attr, attributes.pop(attr))
                elif hasattr(self.meta, attr):
                    setattr(self, attr, getattr(self.meta, attr))

            if attributes != {}:
                raise MetaAttributeError('Unknown attributes %s' % attributes)
        del self.meta

    def add_field(self, field):
        self.fields.add(field)

    def set_application(self, app):
        if hasattr(self, 'app'):
            raise RuntimeError('Model is already initialized!')
        self.app = app
        for cb in self.model_callbacks:
            cb(self.app.models)

    def add_model_callback(self, cb):
        self.model_callbacks.append(cb)
