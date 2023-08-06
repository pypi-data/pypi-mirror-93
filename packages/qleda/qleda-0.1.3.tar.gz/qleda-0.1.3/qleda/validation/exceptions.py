

class DirtySessionException(Exception):
    """
        A clean Session was expected
    """
    pass


class RecordRelatedException(Exception):

    def __init__(self, query_result, message: str):
        self.query_result = query_result
        super(RecordRelatedException, self).__init__(message)


class EmptyPinNames(RecordRelatedException):
    """
        Not all Pin Names are defined.
    """
    def __init__(self, query_result, message: str = 'Not all Pin Names are defined'):
        super(EmptyPinNames, self).__init__(query_result, message)
