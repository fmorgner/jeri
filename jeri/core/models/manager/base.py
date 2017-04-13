from abc import abstractmethod, ABCMeta
from jeri.core.models.manager.error import FilterError, MultipleResultsError


class Manager(metaclass=ABCMeta):

    """
    A generic base class for all model managers. It provides basic
    registration functionality and defines the interface that managers have to
    implement. This class cannot be instantiated as it would be meaningless to
    do so.
    """

    @abstractmethod
    def _all(self):
        """
        Internal object retrieval method to get all remote objects the manager
        is responsible for.

        Subclasses must implement this method and return a list of objects of
        the type managed by the manager instance.
        """
        pass

    @abstractmethod
    def _count(self):
        """
        Internal object count method.

        Subclasses must implement this methid and return the number of objects
        this manager is reponsible for.
        """
        pass

    @abstractmethod
    def _get(self, **kwargs):
        """
        Internal object retrieval method to get a single remote object the
        manager is responsible for.

        Subclasses must implement this method and return a single object
        matching the filter criteria specified by the kwargs dict. The
        implementation does not have to ensure that a single object is
        returned.

        Might return None if no object matches the filter criteria.
        """
        pass

    def apply_to_class(self, cls, name):
        setattr(cls, name, self)
        self.model = cls
        self.endpoint = cls._meta.endpoint

    def flush(self):
        self._do_flush()

    def all(self):
        return self._all()

    def count(self):
        return self._count()

    def get(self, **kwargs):
        for attr, _ in kwargs.items():
            if not hasattr(self.model, attr):
                raise FilterError('\'{}\' has no attribute \'{}\''.format(
                    self.model.__class__, attr))

        result = self._get(**kwargs)
        if hasattr(result, '__iter__'):
            raise MultipleResultsError()
        return result
