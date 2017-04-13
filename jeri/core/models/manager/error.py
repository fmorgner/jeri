class FilterError(RuntimeError):
    """
    This error is raised when a filter can never match on a given model class
    """
    pass


class MultipleResultsError(RuntimeError):
    """
    This filter is raised when multiple results are returned while a single
    one was expected
    """
