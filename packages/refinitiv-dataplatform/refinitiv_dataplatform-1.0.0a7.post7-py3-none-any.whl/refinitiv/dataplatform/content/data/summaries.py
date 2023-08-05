from .historical_pricing import HistoricalPricing
from refinitiv.dataplatform.legacy.tools import get_default_session


class Definition:
    """Class that defines parameters for requesting summaries from historical pricing"""
    def __init__(self,
                 universe,
                 session=None,
                 interval=None,
                 start=None,
                 end=None,
                 adjustments=None,
                 sessions=None,
                 count=None,
                 fields=None,
                 on_response=None,
                 closure=None):
        self.session = session
        if self.session is None:
            self.session = get_default_session()

        if self.session is None:
            raise AttributeError('A Session must be started')

        self.universe = universe
        self.interval = interval
        self.start = start
        self.end = end
        self.adjustments = adjustments
        self.sessions = sessions
        self.count = count
        self.fields = fields
        self.on_response = on_response
        self.closure = closure

    def get_data(self):
        historical_pricing = HistoricalPricing(session=self.session, on_response=self.on_response)
        return historical_pricing._get_summaries(universe=self.universe,
                                                 interval=self.interval,
                                                 start=self.start,
                                                 end=self.end,
                                                 adjustments=self.adjustments,
                                                 sessions=self.sessions,
                                                 count=self.count,
                                                 fields=self.fields,
                                                 closure=self.closure)
