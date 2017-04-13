""" This module provides the 'Backend' abstract baseclass for Jeri backends.
"""
from abc import abstractmethod, ABCMeta


class Backend(metaclass=ABCMeta):
    """ The 'Backend' class defines the interface that Jeri backends are
    expected to implement.
    """

    @abstractmethod
    def get(self, model, **kwargs):
        """ Retrieve a single instance of the given model from the backend.

        Parameters
        ----------
        model: jeri.core.models.Model
            The model modelling the instance to be retrieved.

        **kwargs: dict
            Filtering criteria used to select the desired instance. The actual
            keys are highly dependent on the model that is being querried.
        """
        return None

    @abstractmethod
    def get_all(self, model, **kwargs):
        """ Retrieve all instances of the given model from the backend.

        Parameters
        ----------
        model: jeri.core.models.Model
            The model modelling the instance to be retrieved.

        **kwargs: dict
            Filtering criteria used to select the desired instances. The actual
            keys are highly dependent on the model that is being querried.
        """
        return []

    @property
    @abstractmethod
    def id_key(self):
        """ The key used by the backend to uniquely identify resources.
        """
        pass

    @property
    @abstractmethod
    def uri_key(self):
        """ The key used by the backend to address a unique resource.
        """
        pass
