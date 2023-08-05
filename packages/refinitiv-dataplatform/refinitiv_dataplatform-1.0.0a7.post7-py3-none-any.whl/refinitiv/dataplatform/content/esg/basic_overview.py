from .esg import ESG
from .data_type import DataType


class Definition:
    def __init__(self, universe, session=None, closure=None, on_response=None):
        self.universe = universe
        self.session = session
        self.closure = closure
        self.on_response = on_response

    def get_data(self):
        esg = ESG(self.session, self.on_response)
        data_response = esg._get_data(universe=self.universe, data_type=DataType.BasicOverview, closure=self.closure)
        return data_response
