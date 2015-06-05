class MeasureImproperlyConfigured(Exception):
    """
    There is no registered measure, or no active measure, or the active measure
    has less than two measure values registered.
    """
    pass

class FactorsImproperlyConfigured(Exception):
    """
    There is no registered factor, or no active factor in the application.
    """
    pass
