from .esg import BaseDefinition
from .data_type import DataType


class Definition(BaseDefinition):
    def __init__(self, universe, start=None, end=None, session=None, closure=None, on_response=None):
        super().__init__(universe, start=start, end=end, session=session, closure=closure, on_response=on_response)
        self.__data_type = DataType.StandardScores
