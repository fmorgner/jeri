import importlib
from inspect import isclass
from jeri.core.models import Model


class Application:

    def __init__(self, app_name, backend, models):
        self.app_name = app_name
        self.backend = backend

        self.load_models(models)

    def load_models(self, models):
        if not hasattr(self, '_models'):
            self._models = dict()

        models = importlib.import_module(models)
        for key, value in models.__dict__.items():
            if isclass(value) and issubclass(value, Model):
                if value != Model:
                    self._models[key] = value
        for _, model in self.models.items():
            model.set_application(self)

    @property
    def models(self):
        return self._models.copy()
