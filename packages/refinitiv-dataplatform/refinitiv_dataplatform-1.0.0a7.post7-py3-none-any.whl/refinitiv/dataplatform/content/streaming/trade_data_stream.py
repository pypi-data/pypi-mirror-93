# coding: utf-8

###############################################################
#
#   STANDARD IMPORTS
#

import sys

from collections.abc import Callable

import enum

import numpy as np

import pandas as pd

from datetime import datetime

###############################################################
#
#   REFINITIV IMPORTS
#

from refinitiv.dataplatform.delivery.stream import RDPItemStream
from refinitiv.dataplatform.delivery.stream import Openable
from refinitiv.dataplatform.delivery.stream import StreamState

#   TDS Cache
from refinitiv.dataplatform.delivery.stream.trade_data_stream_cache import TradeDataStreamCache

###############################################################
#
#   LOCAL IMPORTS
#

###############################################################
#
#   CLASS DEFINITIONS
#

class TradeDataStream(TradeDataStreamCache, Openable):
    """
        Open a streaming trading analytics subscription.

    Parameters
    ----------
    universe: list
        a list of RIC or symbol or user's id for retrieving trading analytics data.
    
    views: list
        a list of enumerate fields.
        Default: None
    
    universe_type: enum
        a type of given universe can be RIC, Symbol or UserID.
        Default: UniverseTypes.RIC

    event: bool
        enable/disable the detail of order event in the streaming. 
        Default: False

    finalized_order: bool
        enable/disable the cached of finalized order of current day in the streaming.
        Default: False

    filters: dict
        set the condition of subset of trading streaming data
        Default: None

    on_add: callable object (stream, add_message)
        Called when the stream on summary order of  universe is added by the server.
        This callback is called with the reference to the stream object and the universe full image.
        Default: None
    
    on_update: callable object (stream, update_message)
        Called when the stream on summary order of universe is updated by the server. (can be partial or full)
        This callback is called with the reference to the stream object and the universe update.
        Default: None

    on_remove: callable object (stream, remove_message)
        Called when the stream on summary order of universe is removed by the server. 
        This callback is called with the reference to the stream object and the universe removed.
        Default: None

    on_event: callable object (stream, event_message)
        Called when the stream on order of universe has new event by the server. 
        This callback is called with the reference to the stream object and the universe has a order event.
        Default: None

    on_state: callable object (stream, state_message):
        Called when the stream has new state.
        Default: None
    
    """

    class Params(object):

        def __init__(self, *args, **kwargs):
            self._universe = None
            self._views = None
            self._parameters = None
            #   callbacks
            #       order summary
            self._on_add_cb = None
            self._on_update_cb = None
            self._on_remove_cb = None
            #       order events
            self._on_event_cb = None
            #       state
            self._on_state_cb = None


        def universe(self, universe:list):
            self._universe = universe
            return self

        def views(self, views:list):
            self._views = views
            return self

        def parameters(self, parameters:dict):
            self._parameters = parameters
            return self

        def on_add(self, on_add_cb:Callable):
            self._on_add_cb = on_add_cb
            return self
        
        def on_update(self, on_update_cb:Callable):
            self._on_update_cb = on_update_cb
            return self

        def on_remove(self, on_remove_cb:Callable):
            self._on_remove_cb = on_remove_cb
            return self

        def on_event(self, on_event_cb:Callable):
            self._on_event_cb = on_event_cb
            return self

        def on_state(self, on_state_cb:Callable):
            self._on_state_cb = on_state_cb
            return self

    class Views(enum.Enum):
        """ Trading analytic service's fields """
        OrderKey = 'OrderKey'
        OrderTime = 'OrderTime'
        OrderStatus = 'OrderStatus'
        TopOrderId = 'TopOrderId'
        OrderQuantity = 'OrderQuantity'
        LeavesQuantity = 'LeavesQuantity'
        TotalExecutedQuantity = 'TotalExecutedQuantity'
        TotalExecutedPrice = 'TotalExecutedPrice'
        TotalExecutedValue = 'TotalExecutedValue'
        NumberofFills = 'NumberofFills'
        PercentExecuted = 'PercentExecuted'
        AveragePrice = 'AveragePrice'
        AnalyticStartDateTime = 'AnalyticStartDateTime'
        AnalyticStartDateTimeSource = 'AnalyticStartDateTimeSource'
        AnalyticEndDateTime = 'AnalyticEndDateTime'
        AnalyticEndDateTimeEventType = 'AnalyticEndDateTimeEventType'
        OrderLifeDuration = 'OrderLifeDuration'
        RediEventType = 'RediEventType'
        RediOrderStatus = 'RediOrderStatus'
        RediOrderId = 'RediOrderId'
        RediCorePubRegion = 'RediCorePubRegion'
        Side = 'Side'
        LimitPrice = 'LimitPrice'
        StopPrice = 'StopPrice'
        DestinationType = 'DestinationType'
        AlgoId = 'AlgoId'
        TimeInForce = 'TimeInForce'
        LastCapacity = 'LastCapacity'
        InstrumentIdType = 'InstrumentIdType'
        InstrumentId = 'InstrumentId'
        RIC = 'RIC'
        PrimaryListedRIC = 'PrimaryListedRIC'
        CompositeRIC = 'CompositeRIC'
        TradingCurrencyCode = 'TradingCurrencyCode'
        IncorporationCountryCode = 'IncorporationCountryCode'
        TRBCEconomicSectorCode = 'TRBCEconomicSectorCode'
        TRBCBusinessSectorCode = 'TRBCBusinessSectorCode'
        TRBCIndustryGroupCode = 'TRBCIndustryGroupCode'
        TRBCIndustryCode = 'TRBCIndustryCode'
        TRBCActivityCode = 'TRBCActivityCode'
        AssetCategory = 'AssetCategory'
        InstrumentLongName = 'InstrumentLongName'
        AssetClassType = 'AssetClassType'
        ListingStatus = 'ListingStatus'
        ContractType = 'ContractType'
        ContractDate = 'ContractDate'
        NextContractId = 'NextContractId'
        NextContractDate = 'NextContractDate'
        LotSize = 'LotSize'
        LotUnitType = 'LotUnitType'
        PeriodicityType = 'PeriodicityType'
        PrimaryIssueLevelCode = 'PrimaryIssueLevelCode'
        ExchangeCode = 'ExchangeCode'
        MIC = 'MIC'
        AccountId = 'AccountId'
        UserId = 'UserId'
        FirmId = 'FirmId'
        BrokerCode = 'BrokerCode'

    class UniverseTypes(enum.Enum):
        RIC = 'RIC'
        Symbol = 'Symbol'
        UserID = 'UserID'
    
    class Events(enum.Enum):
        No = 'None'
        Full = 'Full'

    class FinalizedOrders(enum.Enum):
        """ finalized order in cached """
        No = 'None',
        P1D = 'P1D'

    def __init__(self, universe:list, 
                        views:list = None, 
                        #   parameters
                        universe_type = None,
                        events:object = None,
                        finalized_orders:object = None,
                        filters:list = None,
                        #   extended parameters
                        extended_params:dict = None,
                        #   session
                        session = None,
                        api:str = None,
                        #   order summary
                        on_add:Callable = None,
                        on_update:Callable = None,
                        on_remove:Callable = None,
                        #   order events
                        on_event:Callable = None,
                        #   state
                        on_state:Callable = None,
                        #   cache
                        max_order_summary_cache:int = None,
                        max_order_events_cache:int = None,
                    ):
        #   set parameters default value
        if universe_type is None:
        #   set a default for universe type to be RIC
            universe_type = self.UniverseTypes.RIC

        if events is None:
        #   set a default for event to be False
            events = self.Events.Full
        
        if finalized_orders is None:
        #   set a default for finalized order to be False
            finalized_orders = self.FinalizedOrders.P1D
            
        #   validate arguments
        if not isinstance(universe_type, self.UniverseTypes):
        #   invalid universe type
            raise TypeError(f'ERROR!!! Invalid universe type[{universe_type}].')

        #   cache
        #       order summary
        if max_order_summary_cache is None:
            max_order_summary_cache = 1500
        #       order events
        if max_order_events_cache is None:
            max_order_events_cache = 100

        #   TDS information 
        self._universe = universe
        self._views = views
        #   parameters
        self._universe_type = universe_type
        self._event_details = events
        self._finalized_orders = finalized_orders
        self._filters = filters
        self._extended_params = extended_params

        #   session
        from refinitiv.dataplatform.legacy.tools import DefaultSession
        self._session = session or DefaultSession.get_default_session()
        assert self._session is not None

        #   initialize the parent classes
        TradeDataStreamCache.__init__(self, max_order_summary_cache, max_order_events_cache)
        Openable.__init__(self, loop=self._session._loop, logger=self._session)

        #   api
        self._api = api if api is not None else 'streaming/trading-analytics/redi'

        #   callback functions
        #       order summary
        self._on_add_cb = on_add
        self._on_update_cb = on_update
        self._on_remove_cb = on_remove
        #       order events
        self._on_event_cb = on_event

        #       state
        self._on_state_cb = on_state

        #   build RDP item stream for TDS
        self._stream = RDPItemStream(session=self._session,
                                        service=None,
                                        #   TDS
                                        universe=self._universe, 
                                        views=[view.value for view in self._views] if self._views is not None else None, 
                                        parameters=self._parameters,
                                        api=self._api,
                                        extended_params=self._extended_params,
                                        on_ack=self.__on_ack,
                                        on_response=self.__on_response,
                                        on_update=self.__on_update,
                                        on_alarm=self.__on_alarm)

        # #   stream state
        # self._stream_state = self._stream.state

        #   order summary header field names
        #       dictionary of header information
        self._order_summary_headers = None
        #       list of header names
        self._order_summary_header_names = None

    # @property
    # def state(self):
    #     return self._stream_state

    @property
    def _parameters(self):
        #   build RDP item stream parameters
        return {'universeType':self._universe_type.value,
                    'events': self._event_details.value,
                    'finalizedorders': self._finalized_orders.value,
                    'filters': self._filters
                }

    ####################################################
    #   open/close methods 

    async def _do_open_async(self):
        #   clear caches
        self._clear_caches()

        #   open RDP item stream
        self._session.debug(f'Start asynchronously StreamingTDS subscription {self._stream.stream_id} for {self._universe}')
        self.state = await self._stream.open_async()

    async def _do_close_async(self):
        self._session.debug(f'Stop asynchronously StreamingTDS subscription {self._stream.stream_id} for {self._universe}')
        self.state = await self._stream.close_async()

    def _do_pause(self):
        # for override
        pass

    def _do_resume(self):
        # for override
        pass
    
    ####################################################
    #   functions 
    
    def get_order_summary(self, universe:list = None,
                                start_datetime:object=None, 
                                end_datetime:object=None):
        """ get the snapshot of order summary in dataframe """
        #   convert to nunpy array for build pandas dataframe
        data = np.array([order_summary for order_summary in self._order_summary_dict.values()])
        df = pd.DataFrame.from_records(data, columns=self._order_summary_header_names)

        #   check for filter
        if (universe and 'RIC' in df.columns) \
            or ((start_datetime or end_datetime) and ('OrderTime' in df.columns)):
        #   do filter by universe and/or order time

            if universe:
            #   filter by universe
                df = df[df.RIC.isin(universe)]

            if start_datetime:
            #   filter by start date/time
                df = df[df.OrderTime >= start_datetime.strftime('%Y-%m-%dT%H:%M:%S.%f')]

            if end_datetime:
            #   filter by end date/time
                df = df[df.OrderTime <= end_datetime.strftime('%Y-%m-%dT%H:%M:%S.%f')]

            #   done
            return df

        else:
        #   no filter required
            return df

    def get_order_events(self, universe:list = None, 
                            start_datetime:object=None, 
                            end_datetime:object=None):
        """ get the snanpshot of order events in dataframe """
        data = np.array(self.get_last_order_events())

        #   check empty case
        if data.size == 0:
        #   no data, so return None
            return None

        #   build column name
        order_event_column_name = ['OrderKey', ]
        order_event_column_name.extend(self._event_column_names)

        #   get row and column for data
        data_num_rows, data_num_cols = data.shape
        assert data_num_cols == len(order_event_column_name)

        #   build datafarme
        df = pd.DataFrame.from_records(data, columns=order_event_column_name)

        #   check for filter
        if (universe and 'OrderKey' in df.columns) \
            or ((start_datetime or end_datetime) and ('EventTime' in df.columns)):
        #   do filter by universe

            if universe:
            #   filter by universe
                df = df[df.OrderKey.str.contains('|'.join(universe), regex=True)]

            if start_datetime:
            #   filter by start date/time
                df = df[df.EventTime >= start_datetime.strftime('%Y-%m-%dT%H:%M:%S.%f')]

            if end_datetime:
            #   filter by end date/time
                df = df[df.EventTime <= end_datetime.strftime('%Y-%m-%dT%H:%M:%S.%f')]

            #   done
            return df

        else:
        #   no filter required
            return df

    ####################################################
    #   callbacks 

    #   RDP
    def __on_ack(self, stream, ack):
        pass

    def __on_response(self, stream:object, response:dict):
        """ extract the response order summaries, order events and state """
        
        #   extract headers, data, message and state
        #       headers
        assert 'headers' in response
        self._order_summary_headers = response.get('headers', None)
        assert self._order_summary_headers is not None
        assert isinstance(self._order_summary_headers, list)

        #   generate a list of header name
        self._order_summary_header_names = [item.get('id', None) for item in self._order_summary_headers]
        
        #       data
        if 'data' in response:
            #   extract order summaries
            added_order_summary_data_list = response.get('data', None)
            assert added_order_summary_data_list is not None
            assert isinstance(added_order_summary_data_list, list)

            #   call the callback function on_add

            #   loop over all new order summary data
            for added_order_summary_data in added_order_summary_data_list:
                assert len(added_order_summary_data) == len(self._order_summary_headers)
                #   call the on_add callback function
                self._on_add(stream, added_order_summary_data)
            
        #       events
        if 'messages' in response:
            #   extract order events
            order_event_list = response.get('message', None)
            assert order_event_list is not None
            assert isinstance(order_event_list, list)

            #   call the callback function on_event

            #   loop over all new order events
            for order_event in order_event_list:
                #   call the on_event callback function
                self._on_event(stream, order_event)

        # #       state
        # assert 'state' in response
        # state = response.get('state', None)
        # assert state is not None
        
        # #           stream state
        # assert 'stream' in state
        # stream_state = state.get('stream', None)
        # assert stream_state is not None
        
        # if stream_state and stream_state == 'Open':
        # #   set state of this streaming TDS to open
        #     self._stream_state = StreamState.Open

        # elif stream_state and stream_state == 'Closed':
        # #   set state of this streaming TDS to closed
        #     self._stream_state = StreamState.Closed

        # #   call the on_state callback
        # self._on_state(stream, state)


    def __on_update(self, stream, update):
        """ extract the update (add/update/remove) order summaries and new order status. """
        
        #   extract data(add), update, remove and messages (order events)
        #       data
        if 'data' in update:
            #   update contains a new order summary data
            added_order_summary_data_list = update.get('data', None)
            assert added_order_summary_data_list is not None
            assert isinstance(added_order_summary_data_list, list)

            #   loop over all new order summary data
            for added_order_summary_data in added_order_summary_data_list:
                assert len(added_order_summary_data) == len(self._order_summary_headers)
                #   call the on_add callback function
                self._on_add(stream, added_order_summary_data)

        #       update
        if 'update' in update:
            #   update contains an updated order summary data
            updated_order_summary_dict_list = update.get('update', None)
            assert updated_order_summary_dict_list is not None
            assert isinstance(updated_order_summary_dict_list, list)

            #   loop over all updated order summary data
            for updated_order_summary_dict in updated_order_summary_dict_list:
                #   call the on_update callback function
                self._on_update(stream, updated_order_summary_dict)

        #       remove
        if 'remove' in update:
            #   update contains a removed order summary data
            removed_order_summary_data_list = update.get('remove', None)
            assert removed_order_summary_data_list is not None
            assert isinstance(removed_order_summary_data_list, list)

            #   loop over all removed order summary data
            for removed_order_summary_data in removed_order_summary_data_list:
                #   call the on_update callback function
                self._on_remove(stream, removed_order_summary_data)
        
        #       messages
        if 'messages' in update:
            #   update contains a order event.
            order_event_list = update.get('messages', None)
            assert order_event_list is not None
            assert isinstance(order_event_list, list)

            #   loop over all new order events
            for order_event in order_event_list:
                #   call the on_event callback function
                self._on_event(stream, order_event)

            #   update the cache
            self._add_order_event(order_event)
    
    def __on_alarm(self, stream, alarm):
        pass

    
    #   TDS
    def _on_add(self, stream, add_message:list):
        """ order summary add callback from RDPItemStream """
        assert len(add_message) > 1

        #   update the cache
        order_key = add_message[0]
        self._add_order_summary(order_key, add_message)

        #   call the add callback function
        if self._on_add_cb:
            #   convert add message to a dict between field name and value
            add_message_dict = dict(zip(self._order_summary_header_names, add_message))
            #   valid on_add callback
            try:
                self._on_add_cb(self, add_message_dict)
            except Exception as e:
                #   on_add callback has an exception
                self._session.error(f'StreamingTDS on_add callback raised exception: {e!r}')
                self._session.debug(f'Traceback : {sys.exc_info()[2]}')

    def _on_update(self, stream, update_message:dict):
        """ order summary update callback from RDPItemStream """

        #   update the cache
        assert 'key' in update_message
        order_key = update_message['key']
        self._update_order_summary(order_key, update_message)

        #   call the update callback function
        if self._on_update_cb:
            #   valid on_update callback
            try:
                self._on_update_cb(self, update_message)
            except Exception as e:
                #   on_update callback has an exception
                self._session.error(f'StreamingTDS on_update callback raised exception: {e!r}')
                self._session.debug(f'Traceback : {sys.exc_info()[2]}')
    
    def _on_remove(self, stream, remove_message:dict):
        """ order summary remove callback from RDPItemStream """
        #   call the remove callback function
        if self._on_remove_cb:
            #   valid on_remove callback
            try:
                self._on_remove_cb(self, remove_message)
            except Exception as e:
                #   on_remove callback has an exception
                self._session.error(f'StreamingTDS on_remove callback raised exception: {e!r}')
                self._session.debug(f'Traceback : {sys.exc_info()[2]}')
    
    def _on_event(self, stream, event_message:dict):
        """ order event callback from RDPItemStream """
        #   call the event callback function
        if self._on_event_cb:
            #   valid on_event callback
            try:
                self._on_event_cb(self, event_message)
            except Exception as e:
                #   on_add callback has an exception
                self._session.error(f'StreamingTDS on_event callback raised exception: {e!r}')
                self._session.debug(f'Traceback : {sys.exc_info()[2]}')

    def _on_state(self, stream, state_message:dict):
        """ state event callback """
        #   call the state callback function
        if self._on_state_cb:
            #   valid on_state callback
            try:
                self._on_state_cb(self, state_message)
            except Exception as e:
                #   on_add callback has an exception
                self._session.error(f'StreamingTDS on_state callback raised exception: {e!r}')
                self._session.debug(f'Traceback : {sys.exc_info()[2]}')
