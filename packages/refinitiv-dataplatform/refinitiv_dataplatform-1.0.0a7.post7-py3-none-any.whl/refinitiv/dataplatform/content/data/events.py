from .historical_pricing import HistoricalPricing
from refinitiv.dataplatform.legacy.tools import get_default_session


class Definition:
    """Class that defines parameters for requesting events from historical pricing"""
    def __init__(self,
                 universe,
                 session=None,
                 eventTypes=None,
                 start=None,
                 end=None,
                 adjustments=None,
                 count=None,
                 fields=None,
                 on_response=None,
                 closure=None):
        self.session = session
        if session is None:
            self.session = get_default_session()

        if self.session is None:
            raise AttributeError('A Session must be started')
        self.universe = universe
        self.eventTypes = eventTypes
        self.start = start
        self.end = end
        self.adjustments = adjustments
        self.count = count
        self.fields = fields
        self.on_response = on_response
        self.closure = closure

    def get_data(self):
        historical_pricing = HistoricalPricing(session=self.session, on_response=self.on_response)
        return historical_pricing._get_events(universe=self.universe,
                                              eventTypes=self.eventTypes,
                                              start=self.start,
                                              end=self.end,
                                              adjustments=self.adjustments,
                                              count=self.count,
                                              fields=self.fields,
                                              closure=self.closure)
