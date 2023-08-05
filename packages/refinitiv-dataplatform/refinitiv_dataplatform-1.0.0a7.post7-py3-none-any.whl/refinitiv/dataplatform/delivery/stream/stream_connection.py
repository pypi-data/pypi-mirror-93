# coding: utf-8

__all__ = ['StreamConnection']

###############################################################
#
#   STANDARD IMPORTS
#

import abc
import asyncio
import functools
import json
import logging
import threading
import time
from enum import Enum, unique

import websocket

###############################################################
#
#   REFINITIV IMPORTS
#

from refinitiv.dataplatform.errors import StreamConnectionError
from refinitiv.dataplatform.core.log_reporter import LogReporter
from refinitiv.dataplatform.configure import config


###############################################################
#
#   CLASS DEFINITIONS
#


class StreamConnection(threading.Thread, LogReporter):
    """ This class is designed to be a abstract class. this class manage the login and close to/from websocket protocol.

        The following are abstract methods.
            - def _get_login_message(self):
            - def _get_close_message(self):
            - def _process_login_response_message(self, login_response_message):
            - def _on_messages(self, messages):
            - def _process_response_message(self, message):

        The following must be called to set future object to be done when received login or close response.
            - _on_receive_login_message(message)
            - _on_receive_close_message(message)
    """

    class State(Enum):
        CLOSED = 0
        PENDING = 1
        OPEN = 2

    @unique
    class FailoverState(Enum):
        """ state of the failover of stream connection """
        FailoverStarted = 0
        FailoverCompleted = 1
        FailoverError = 2

    __all_streaming_session = {}
    __register_lock = threading.Lock()
    __streaming_session_id_counter = 0

    @classmethod
    def _get_new_streaming_session_id(cls):
        cls.__streaming_session_id_counter += 1
        return cls.__streaming_session_id_counter

    @classmethod
    def register_streaming_session(cls, streaming_session):

        with cls.__register_lock:
            if not streaming_session:
                raise StreamConnectionError(1, 'Try to register unavailable streaming session')

            streaming_session_id = streaming_session.streaming_session_id

            if streaming_session_id in cls.__all_streaming_session:
                raise StreamConnectionError(1, f'Try to register again existing streaming session id {streaming_session_id}')

            streaming_session._streaming_session_id = cls._get_new_streaming_session_id()
            streaming_session.debug(f"Register streaming session {streaming_session.streaming_session_id}")
            cls.__all_streaming_session[streaming_session.streaming_session_id] = streaming_session

    @classmethod
    def unregister_streaming_session(cls, streaming_session):

        with cls.__register_lock:
            if not streaming_session:
                raise StreamConnectionError(1, 'Try to unregister unavailable streaming session')

            if streaming_session.streaming_session_id is None:
                raise StreamConnectionError(1, 'Try to unregister unavailable streaming session')

            if streaming_session.streaming_session_id not in cls.__all_streaming_session:
                raise StreamConnectionError(1,
                                            f'Try to unregister unknown streaming session id {streaming_session.streaming_session_id}')

            streaming_session.debug(f'Unregister streaming session {streaming_session.streaming_session_id}')
            cls.__all_streaming_session.pop(streaming_session.streaming_session_id)

    __all_subscriptions = {}
    __id_request = 1

    ###############################################################################################

    #   default websocket configuration
    #       websocket ping interval in secs
    _DefaultWebsocketPingInterval_secs = 120
    #       websocket ping timeout in secs
    _DefaultWebsocketPingTimeout_secs = 60
    #       websocket idle timeout in secs
    _DefaultWebsocketIdleTimeout_secs = 15

    #   default maximum retry to reconnection to websocket
    _DefaultMaxRetryConnection = 5

    def __init__(self, thread_name, session, stream_connection_name, streaming_config, *args, **kwargs):

        if session is None:
            raise ValueError("StreamConnection is passed a null session")
        if streaming_config.uri is None:
            raise ValueError("StreamConnection must have a WebsocketEndpoint")

        self._streaming_session_id = None
        self._streaming_config = streaming_config
        self._session = session
        self._on_state_cb = session._on_state
        self._on_event_cb = session._on_event
        self._is_closing = False

        self._websocket = None
        self._ws_connected = False
        self._ws_lock = threading.Lock()

        self._logger = logging.getLogger(self._session._LOGGER_NAME)
        self._state = self.State.CLOSED

        ############################################################
        #   multi-websockets support

        #   store stream connection name
        self._connection_name = stream_connection_name

        #   a mapping subscription between stream event id to the stream
        #       it is used to notify stream when websocket received response corresponding to subscribed stream event id
        #       note that stream event id is unique across all the session.
        #       stream event id is a integer value representing the event stream. It can also be used to match the request and
        #       responses.
        #       the registration of stream event id happen in session
        self._stream_event_id_to_stream_dict = {}

        #   store the stream event id for login
        self._login_stream_event_id = None

        #   future object trigger when got response from login/close request
        #       login
        self._login_response_future = None
        #       close
        self._close_response_future = None

        #   future object this stream is ready or not?
        #       future
        self._ready_future = None
        #       lock
        self._ready_lock = threading.Lock()

        #   asyncio event loop for websocket thread
        self._loop = None

        ############################################################
        #   reconnection support
        #       note that on reconnection to the websocket state will be pending

        #   set stream authentication future
        self._set_stream_authentication_token_future = None

        #   reconnection state
        self._reconnect_state = None

        #   reconnection flag
        self._do_reconnect = True
        #   maximum number of retry auto-reconnection
        self._max_retry_connection = self._DefaultMaxRetryConnection

        #   for websocket heartbeat check

        #   the following are ADS information, it will be supplied from login response message
        #       ping/pong timeout
        self._ping_pong_timeout_secs = self._DefaultWebsocketPingTimeout_secs
        #       max message size
        self._max_message_size_bytes = None

        #   websocket idle timeout in secs
        self._idle_timeout_secs = self._DefaultWebsocketIdleTimeout_secs

        #   store timestamp of last ping/pong message time
        self._last_ping_message_time = None
        self._last_pong_message_time = None

        #   store timestamp of last message that it got from websocket
        self._last_received_messages_time = None

        self._num_retries = 0
        self._is_first_connection = True
        ############################################################

        #   initialize
        self._initialize()

        LogReporter.__init__(self, logger=self._logger)
        threading.Thread.__init__(self, target=self.run, name=thread_name)
        StreamConnection.register_streaming_session(self)

    def __del__(self):
        self.debug(f'StreamConnection {self.streaming_session_id} is releasing')

        if self._websocket:
            try:
                if self._websocket.keep_running:
                    # Close web socket
                    self.debug(f"Close websocket client {self.streaming_session_id}")
                    self._websocket.close()
                    self._websocket.keep_running = False

            except Exception as e:
                self.debug(f'Exception on close websocket attempt for main stream {self.streaming_session_id}: {e!r}')

        if self.streaming_session_id in StreamConnection.__all_streaming_session:
            self.debug(f"Unregister streaming session {self.streaming_session_id}")
            StreamConnection.unregister_streaming_session(self)

    def username(self, user):
        self._streaming_config.username = user
        return self

    def position(self, position):
        self._streaming_config.position = position

    def application_id(self, app_id):
        self._streaming_config.application_id = app_id

    def auth_token(self, token):
        self._streaming_config.auth_token = token

    def connection_retry(self, retry_in_seconds):
        self._streaming_config.connection_retry = retry_in_seconds

    @property
    def streaming_session_id(self):
        return self._streaming_session_id

    @property
    def is_connected(self):
        return self._ws_connected

    @property
    def is_closing(self):
        return self._is_closing

    @is_closing.setter
    def is_closing(self, value):
        self._is_closing = value

    @property
    def ready(self):
        return self._ready_future

    #############################################
    #
    def _initialize(self):
        """ Initialize the future object before thread start. """

        #   initialize asyncio event loop for this thread

        #   asyncio event loop for websocket thread
        #       this thread will use the same loop as the session
        #   because it need to share login future object
        self._loop = self._session._loop
        asyncio.set_event_loop(self._loop)

        #   initialize login future
        self._initialize_login_future()
        #   initialize ready future
        self._initialize_ready_future()

    def _initialize_login_future(self):
        """ Create new login future, call the cancel for the exciting ready future before create new one  """
        assert self._loop is not None

        #   call cancel for the current login future
        if self._login_response_future is not None and not self._login_response_future.done():
            #   the login future is not done yet, so cancel it
            self._loop.call_soon_threadsafe(self._login_response_future.cancel)

        #   initialize new login future
        self._login_response_future = self._loop.create_future()

    def _initialize_ready_future(self):
        """ Create new ready future, call the cancel for the exciting ready future before create new one """
        assert self._loop is not None

        #   lock the ready before change the ready future
        with self._ready_lock:
            #   check for create new ready future
            if self._ready_future is None or self._ready_future.done():
                #   the ready future is done, so create new ready future
                #   create new ready future object
                self._ready_future = self._loop.create_future()

    #############################################
    #  methods to open and close the websocket  #
    def run(self):
        #############################################
        """ open the websocket connection thread """

        #   initialize flags
        #       cleanup flag
        self._is_closing = False
        timer = threading.Event()

        #   loop forever if it is not closing and reconnection flags is True
        self._num_retries = 0
        self._is_first_connection = True
        while not self.is_closing and self._do_reconnect:

            #   consistency check for future objects
            #       login
            assert self._login_response_future is not None and not self._login_response_future.done()
            #       ready
            assert self._ready_future is not None and not self._ready_future.done()

            self.debug(f"StreamingConnection {self.streaming_session_id} "
                       f"open websocket at {self._streaming_config.uri}.")

            if self._session._logger.level == logging.DEBUG:
                websocket.enableTrace(True)

            self._websocket = websocket.WebSocketApp(
                self._streaming_config.uri,
                header=["User-Agent: Python"] + self._streaming_config.header,
                on_message=self._ws_message,
                on_error=self._ws_error,
                on_open=self._ws_open,
                on_close=self._ws_close,
                on_ping=self._ws_ping,
                on_pong=self._ws_pong,
                subprotocols=[self._streaming_config.data_format, ]
                )
            self._websocket.id = self.streaming_session_id
            self._state = self.State.PENDING
            # self._websocket.run_forever(ping_interval=self._DefaultWebsocketPingInterval_secs, 
            #                             ping_timeout=self._DefaultWebsocketPingTimeout_secs)
            _proxy_config = self._streaming_config.proxy_config
            _no_proxy = self._streaming_config.no_proxy
            self.debug(f"Run websocket with {str(_proxy_config)} and {_no_proxy} http_no_proxy")
            self._websocket.run_forever(http_proxy_host=_proxy_config.host if _proxy_config else None,
                                        http_proxy_port=_proxy_config.port if _proxy_config else None,
                                        http_proxy_auth=_proxy_config.auth if _proxy_config else None,
                                        http_no_proxy=_no_proxy,
                                        proxy_type=_proxy_config.type if _proxy_config else None)

            self._websocket = None
            self.debug(f"Websocket for streaming session {self.streaming_session_id} was closed")

            ############################################
            #   auto-reconnect support 

            #   check do the reconnection or not
            if not self.is_closing and self._do_reconnect:
                #   do a websocket reconnection
                #   check for exit, if this is a first time and try to reconnect on all websockets that available
                num_websocket_endpoints = len(self._streaming_config.websocket_endpoints)
                if self._is_first_connection and self._num_retries % num_websocket_endpoints == num_websocket_endpoints - 1:
                    #   it is a first websocket connection and it try all websockets available and it cannot connect to
                    #       call session on_event callback and on_status close the stream

                    #   on_event callback
                    if self._on_event_cb:
                        self._on_event_cb(
                            self._session.EventCode.StreamDisconnected,
                            f'Streaming cannot connect to the "{self._connection_name}" API.',
                            self.streaming_session_id,
                            stream_connection_name=self._connection_name
                            )

                    #   on_status callback for all subscribe item stream

                    #   get list of subscribed streams
                    subscription_streams = self._session.get_subscription_streams_by_service(self._connection_name)
                    #  loop over all stream and call the on_reconnect callback function
                    for stream in subscription_streams:
                        #   call the refresh callback function
                        assert hasattr(stream, '_on_status')
                        status_message = {
                            'ID': stream.stream_id,
                            'Type': 'Status',
                            'Key': {'Name': stream.name},
                            'State': {
                                'Stream': "Closed",
                                'Data': "Suspect",
                                'Code': "Error",
                                'Text': f"Streaming connection to API ‘{self._connection_name}’ failed."
                                }
                            }
                        self._loop.call_soon_threadsafe(functools.partial(stream._on_status, status_message))

                    # cancel the ready and make sure the stream stream is disconnected
                    #   cancel the ready
                    if self._ready_future is not None and not self._ready_future.done():
                        #   cancel the ready future
                        self._loop.call_soon_threadsafe(functools.partial(self._ready_future.cancel, ))

                    #   set the stream to be closed
                    self._state = self.State.CLOSED

                    # exit loop
                    break

                #   check for excess maximum number of reconnection
                if self._num_retries >= (self._max_retry_connection * num_websocket_endpoints):
                    #   excess number of retry to reconnection to websocket
                    #   on_event callback
                    if self._on_event_cb:
                        self._on_event_cb(
                            self._session.EventCode.StreamDisconnected,
                            f'Streaming cannot reconnect to the "{self._connection_name}" API after multiple unsuccessful attempts.',
                            self.streaming_session_id,
                            stream_connection_name=self._connection_name
                            )

                    #   on_status callback for all subscribe item stream

                    #   get list of subscribed streams
                    subscription_streams = self._session.get_subscription_streams_by_service(self._connection_name)
                    #  loop over all stream and call the on_reconnect callback function
                    for stream in subscription_streams:
                        #   call the refresh callback function
                        assert hasattr(stream, '_on_status')
                        status_message = {
                            'ID': stream.stream_id,
                            'Type': 'Status',
                            'Key': {'Name': stream.name},
                            'State': {
                                'Stream': "Closed",
                                'Data': "Suspect",
                                'Code': "Error",
                                'Text': f"Streaming cannot reconnection to API ‘{self._connection_name}’ after multiple unsuccessful "
                                        f"attempts."
                                }
                            }
                        self._loop.call_soon_threadsafe(functools.partial(stream._on_status, status_message))

                    # exit loop
                    break

                #   websocket is disconnected, try to reconnect to the websocket
                self.debug('try to reconnecting to streaming websocket.')

                #   check for the start reconnection
                if self._reconnect_state != self.FailoverState.FailoverStarted:
                    #   start the reconnection
                    self._start_ws_reconnection()

                #   re-initialize the login and ready future
                #       login
                self._initialize_login_future()
                #       ready
                if self._ready_future.done():
                    #   only create new ready when current ready is done
                    self._initialize_ready_future()

                #   set next available websocket uri
                self._streaming_config.set_next_available_websocket_uri()
                #   waiting before do a reconnection to next available websocket uri
                self.debug(f'Try to reconnect to websocket '
                           f'uri {self._streaming_config.uri} in {self._streaming_config.reconnection_delay_secs} secs')

                #   try on all possible websockets, so wait for a moment
                timer.wait(self._streaming_config.reconnection_delay_secs)

            if config.get("auto-reconnect", False) is True:
                self._num_retries = 0
            else:
                #   increase number of retries
                self._num_retries += 1

            #   wait for a few seconds
            time.sleep(3)

        self.debug(f"Streaming session {self.streaming_session_id} will be closed")

    #############################################################
    #   open / close stream connection

    def close(self):
        """ close the stream connection """
        self._loop.run_until_complete(self.close_async())

    async def close_async(self):
        """ Close stream connection by send the close message to websocket server """

        #   close the stream connection
        await self._close_async()

    #############################################################
    #   construct the login/close message

    @abc.abstractmethod
    def _get_login_message(self):
        """ The function is used to build the login message (included authentication).
        It is designed to be override by child class that can define own login message for difference kind of connect.
            ie. Open Message Model (OMM)
                {
                    "Domain":"Login",
                    "ID":1,
                    "Key":{
                        "Elements":{
                        "ApplicationId":"555",
                        "AuthenticationToken":"aBcDeFgHiJkLmNoPqRsTuVwXyZ",
                        "Position":"127.0.0.1"
                        },
                        "NameType":"AuthnToken"
                    }
                }

        Returns
        -------
        string
            the login message from client to server
        """
        pass

    @abc.abstractmethod
    def _get_close_message(self):
        """ This function is used to build the close message.
        It is designed to be override by child class that can define own close message for difference kind of connect.
            ie. Open Message Model (OMM)
                {
                    "Domain":"Login",
                    "ID":1,
                    "Key":{
                        "Elements":{
                        "ApplicationId":"555",
                        "AuthenticationToken":"aBcDeFgHiJkLmNoPqRsTuVwXyZ",
                        "Position":"127.0.0.1"
                        },
                        "NameType":"AuthnToken"
                    }
                }

        Returns
        -------
        string
            the close message from client to server
        """
        pass

    #############################################################
    #   send messages

    async def _login_async(self):
        """ Process the login message for each content via websocket protocol """

        #   initialize login future
        self._initialize_login_future()

        #   get the login message
        login_message = self._get_login_message()

        #   set the future object to wait for this login response
        assert self._login_response_future is not None
        assert not self._login_response_future.done()
        assert not self._login_response_future.cancelled()

        #   send a login message to the server via websocket
        self.debug(f'Sending the login message. uri={self._streaming_config.uri}, message={login_message}')
        with self._ws_lock:
            self.send(login_message)

        #   wait for process login response
        await self._wait_and_process_login_response_message()

    async def _close_async(self):
        """ Process the close message for each content via websocket protocol """

        #   check the websocket are connected or not?
        if self._state != self.State.CLOSED:
            #   the websocket still open or pending, so we are going to close it

            #   check the websocket is closing or not?
            if self._is_closing:
                #   do nothing, it is closing the websocket
                self.debug(f'The stream connection is closing from {self._streaming_config.uri}')

                #   done, just waiting for close from the server
                return

            #   set flags is closing to be true
            self._is_closing = True

            #   create future object for wait until received close response from websocket server
            assert self._close_response_future is None
            self._close_response_future = asyncio.Future()

            #   get the close message
            close_message = self._get_close_message()

            #   send a close message to the server via websocket
            self.debug(f'Sending the close message.\n'
                       f'uri={self._streaming_config.uri},message={close_message}')
            with self._ws_lock:
                self.send(close_message)

            #   wait for process close response
            await self._wait_and_process_close_response_message()

            #   close the websocket connection
            self._websocket.close()
            self.debug('Web socket was closed')

            #   unregister login stream event id
            self._login_stream_event_id = None

            #  set the state
            self._state = self.State.CLOSED

        else:
            #   the stream connection is already closed
            self.debug(f'The stream connection is already closed from {self._streaming_config.uri}')

    #############################################################
    #  wait and process login/close message from websocket

    @abc.abstractmethod
    async def _wait_and_process_login_response_message(self):
        """ Wait and process the login (may include authentication) response message from websocket server
        This function will wait for login response all call the _process_login_response_message method

        Returns
        -------
        boolean
            True if the process login message success otherwise False
        """
        pass

    @abc.abstractmethod
    async def _wait_and_process_close_response_message(self):
        """ Wait and process the close response message from websocket server
        This function will wait for close response all call the _process_close_response_message method

        Returns
        -------
        boolean
            True if the process close message success otherwise False
        """
        pass

    #############################################################
    #  process authentication token update

    def set_stream_authentication_token(self, authentication_token):
        """ Re-authenticate to websocket server """
        self._session.debug('StreamConnection.set_stream_authentication_token()')

        # #   check for previous sent login message and still waiting for it
        # if self._login_response_future is not None and (
        #             not self._login_response_future.cancelled() or not self._login_response_future.done()):
        #     #   it's waiting for previous login message, so cancel it because it's going to send new login
        #     self.debug(f"Stop waiting for previous login message it because it's going to send new login")
        #     self._login_response_future.cancel()

        # #   check the previous set stream authentication token
        # if self._set_stream_authentication_token_future is not None and not self._set_stream_authentication_token_future.done():
        #     #   previous _set_stream_authentication_token is not done yet, so cancel it and set a new authentication token instead
        #     self.debug(f"Previous _set_stream_authentication_token is not done yet, cancel it and set a new authentication token instead")
        #     self._set_stream_authentication_token_future.cancel()

        #   create new future for set stream authentication token
        # self._set_stream_authentication_token_future = asyncio.run_coroutine_threadsafe(
        #     self._set_stream_authentication_token(authentication_token),
        #     loop=self._loop
        #     )
        # self._set_stream_authentication_token_future = asyncio.ensure_future(
        #                                                                 self._set_stream_authentication_token(authentication_token), 
        #                                                                 loop=self._loop)

        # self._loop.run_until_complete(self._set_stream_authentication_token_future)
        #await self._set_stream_authentication_token_future

        #   call the set new stream authentication token
        self._set_stream_authentication_token(authentication_token)

    @abc.abstractmethod
    async def _set_stream_authentication_token(self, authentication_token):
        """ Re-authenticate to websocket server """
        pass

    #############################################################
    #   handle the login/close response message

    def _on_receive_login_message(self, result):
        """ Callback function when received when received the login message of this websocket """
        if self._login_response_future is not None and not self._login_response_future.done():
            #   need to set the future to be done
            self._login_response_future.set_result(result)

    def _on_receive_close_message(self, result):
        """ Callback function when received when received the close message of this websocket """
        if self._close_response_future is not None and not self._close_response_future.done():
            #   need to set the future to be done
            self._close_response_future.set_result(result)

    def _on_ready(self):
        """ Callback function when a stream connection ready """
        assert self._ready_future is not None and not self._ready_future.done()
        self._loop.call_soon_threadsafe(self._ready_future.set_result, None)

    @abc.abstractmethod
    def _process_login_response_message(self, login_response_message):
        """ Process the login (may include authentication) response message from websocket server
        It is designed to be override by child class that can define handle own login message for difference kind of connect.
            ie. Open Message Model (OMM)
                [
                    {
                        "Domain":"Login",
                        "Elements":{
                        "MaxMsgSize":61440,
                        "PingTimeout":30
                        },
                        "ID":1,
                        "Key":{
                        "Elements":{
                            "AllowSuspectData":1,
                            "ApplicationId":"555",
                            "ApplicationName":"ADS",
                            "AuthenticationErrorCode":0,
                            "AuthenticationErrorText":"Success",
                            "Position":"127.0.0.1",
                            "ProvidePermissionExpressions":1,
                            "ProvidePermissionProfile":0,
                            "SingleOpen":1,
                            "SupportBatchRequests":7,
                            "SupportEnhancedSymbolList":1,
                            "SupportOMMPost":1,
                            "SupportOptimizedPauseResume":1,
                            "SupportPauseResume":1,
                            "SupportStandby":0,
                            "SupportViewRequests":1
                        },
                        "Name":"user"
                        },
                        "State":{
                        "Data":"Ok",
                        "Stream":"Open",
                        "Text":"Login accepted by host."
                        },
                        "Type":"Refresh"
                    }
                ]
        Parameters
        ----------
        login_response_message : string
            the close message from websocket server

        Returns
        -------
        boolean
            True if the process close message success otherwise False
        """
        return True

    def _process_close_response_message(self, close_response_message):
        """ process the close response message from websocket server.
        it is designed to be override by child class that can define handle own close message for difference kind of connect.

        Parameters
        ----------
        close_response_message : string
            the close message from websocket server

        Returns
        -------
        boolean
            True if the process close message success otherwise False
        """
        return True

    #############################################
    #  methods to send request to the websocket #
    #############################################
    def send(self, request):
        if self._websocket:
            self.debug(f"Send request: {request}")
            self._send(request)

    ############################################
    # Methods for web socket callbacks         #
    ############################################
    def _ws_open(self, *args):
        from refinitiv.dataplatform.core.session import Session
        with self._ws_lock:
            result = f"WebSocket for streaming session {self.streaming_session_id} was opened to server: {self._streaming_config.uri}"
            self.debug(result)
            if self._on_event_cb:
                self._on_event_cb(
                    Session.EventCode.StreamConnected,
                    result,
                    self.streaming_session_id,
                    stream_connection_name=self._connection_name
                    )
            self._ws_connected = True

            #   change flags to false after first login
            self._is_first_connection = False

            # self._session.loop.run_until_complete(self._login_async())

            #   get and send the login request after the websocket is opened
            login_message = self._get_login_message()
            self.debug(f'sending the login message after websocket is opened. message = {login_message}')
            self.send(login_message)

        ############################################################
        #   reconnection support

        #   call the callback function after reconnection is completed
        if self._reconnect_state:
            #   the stream connection failover is started and ready to be completed
            #       so call the _on_reconnect callback function

            #   reset the reconnection
            #       number of reties
            self._num_retries = 0
            #       delay
            self._streaming_config.reset_reconnection_config()

    def _ws_ping(self, data):
        self.debug(f'websocket ping callback - {data}')

    def _ws_pong(self, data):
        self.debug(f'websocket pong callback - {data}')

    def _ws_error(self, error):
        from refinitiv.dataplatform.core.session import Session
        with self._ws_lock:
            err = (f"WebSocket error occurred for web socket client {self.streaming_session_id} "
                   f"(login id {self._login_stream_event_id}) : {error}")
            self.error(err)
            self._ws_connected = False
            if self._on_event_cb:
                #   call on_event callback for websocket error
                self._on_event_cb(
                    Session.EventCode.StreamDisconnected,
                    err,
                    self.streaming_session_id,
                    stream_connection_name=self._connection_name
                    )

    def _ws_message(self, *args):
        messages = args[0]
        with self._ws_lock:
            self._on_messages(messages)

    def _ws_close(self, *args):
        from refinitiv.dataplatform.core.session import Session
        with self._ws_lock:
            self._state = self.State.CLOSED
            self.debug(f"Close notification from main stream {self.streaming_session_id} (login id {self._login_stream_event_id})")
            self._ws_connected = False
            self._login_stream_event_id = None
            if not self._do_reconnect:
                if self._on_event_cb:
                    self._on_event_cb(
                        Session.EventCode.StreamDisconnected,
                        f"Connection to the WebSocket server [{self._streaming_config.uri}] is down",
                        self.streaming_session_id,
                        stream_connection_name=self._connection_name
                        )
                self._state = self.State.CLOSED

    def _ws_reconnect(self, failover_state, stream_state, data_state, state_code, state_text):
        """ Callback function when the websocket connection is reconnecting.

            - send status to all subscription stream with "FailoverStarted" or "FailoverCompleted, or "FailoverError" code,
                "Suspect" data state "Open" or "Closed" stream state.
            - send on_event callback to session.
        """
        self.debug(f'StreamConnection._ws_reconnect('
                   f'failover_state={failover_state}, stream_state={stream_state}, data_state={data_state}, '
                   f'state_code={state_code}, state_text={state_text})')
        #   call the on_reconnect callback function of subscription stream

        #   call the session on_event callback function
        if self._on_event_cb:
            #   call the on_event when reconnect occurred
            self.debug('call session on_event_cb function.')
            if failover_state == self.FailoverState.FailoverStarted:
                #   call session on_event for failover started
                self._on_event_cb(
                    self._session.EventCode.StreamReconnecting,
                    f'Streaming connection to API "{self._connection_name}" failed. Trying to recover.',
                    self.streaming_session_id,
                    stream_connection_name=self._connection_name
                    )
            elif failover_state == self.FailoverState.FailoverCompleted:
                #   call session on_event for failover completed
                self._on_event_cb(
                    self._session.EventCode.StreamConnected,
                    f'Streaming successfully reconnected to the "{self._connection_name}" API.',
                    self.streaming_session_id,
                    stream_connection_name=self._connection_name
                    )
            elif failover_state == self.FailoverState.FailoverError:
                #   call session on_event for failover error
                self._on_event_cb(
                    self._session.EventCode.StreamDisconnected,
                    f'Streaming cannot reconnect to the "{self._connection_name}" API.',
                    self.streaming_session_id,
                    stream_connection_name=self._connection_name,
                    )
            else:
                #   unknown failover state
                self.error(f'ERROR!!! unknown failover state "{failover_state}" for the "{self._connection_name}" API.')
                assert False

        #   get list of subscribed streams
        subscription_streams = self._session.get_subscription_streams_by_service(self._connection_name)
        if subscription_streams is None or len(subscription_streams) == 0:
            #   no stream subscribed to this stream connection name
            self.debug(f'WARNING!!! _ws_reconnect - no stream subscribed to "{self._connection_name}" stream connection.')

        #  loop over all stream and call the on_reconnect callback function
        for stream in subscription_streams:
            self.debug(f'call stream[{stream.stream_id}] - {stream.name} on_reconnect function.')
            #   call the refresh callback function
            assert hasattr(stream, '_on_reconnect')
            # self._loop.call_soon_threadsafe(
            #     functools.partial(stream._on_reconnect, failover_state, stream_state, data_state, state_code, state_text)
            #     )
            stream._on_reconnect(failover_state, stream_state, data_state, state_code, state_text)

        self._session.debug('DONE :: StreamConnection._ws_reconnect()')

    def _ws_login_failed(self):
        """ Callback function when login to websocket failed """
        self.debug('StreamConnection._ws_login_failed()')

        

        #   set the ready to be not ready
        #       this will hold on all streams that subscribed on this stream connection.
        self._initialize_ready_future()

        #   check for the reconnection has been started or not?urn
        if self._reconnect_state == self.FailoverState.FailoverStarted:
            #   do nothing because, the websocket restart already occurred
            
            #   trigger the start of reconnection event
            self._start_ws_reconnection()

        #   request a new authentication token to session
        self._session.request_stream_authentication_token()

    def _start_ws_reconnection(self):
        """ Start the websocket reconnection state and trigger the callback event """

        #   change the reconnect state to started
        self._reconnect_state = self.FailoverState.FailoverStarted
        #   call the reconnect callback function
        self._ws_reconnect(self._reconnect_state,
                           "Open",
                           "Suspect",
                           "FailoverStarted",
                           f"Streaming connection to API ‘{self._connection_name}’ failed. Trying to recover.")

    def _completed_ws_reconnection(self):
        """ Completed the websocket reconnection state and trigger the callback event """

        #   change the reconnect state to completed
        self._reconnect_state = self.FailoverState.FailoverCompleted
        #   call the reconnect callback function
        self._ws_reconnect(self._reconnect_state,
                           "Open",
                           "Ok",
                           "FailoverCompleted",
                           f"Streaming connection to API ‘{self._connection_name}’ successfully reconnected.")

    ############################################
    # Send request method                      #
    ############################################
    def _send(self, msg):
        try:
            if self._ws_connected:
                self._websocket.send(json.dumps(msg))
            else:
                self.debug(f"WebSocket {self.streaming_session_id} isn't connected, can't send msg {json.dumps(msg)}")
        except websocket.WebSocketConnectionClosedException as e:
            self.error(f"WebSocketConnectionClosedException: {e}")

    ##############################################################
    #   process response messages

    @abc.abstractmethod
    def _on_messages(self, messages):
        """ Received messages callback function from websocket.
        This function designed to be extract websocket raw data to be a object messages ie. json format
            and call _process_response_message method to process each massage.
        """
        pass

    @abc.abstractmethod
    def _process_response_message(self, message):
        """ Process a single response message from websocket server.
        It is designed to be override by child class that can define how to handle response message.
        """
        pass

    ############################################
    #   session callback function

    def _session_on_event_cb(self, streaming_session_id, event_code, event_msg, stream_connection_name):
        """ Call a session on_event callback function """
        #   validate the session on_event is a valid function call
        if self._on_event_cb and callable(self._on_event_cb):
            #   valid session on_event callback function
            self._on_event_cb(
                event_code,
                event_msg,
                streaming_session_id,
                stream_connection_name
                )
