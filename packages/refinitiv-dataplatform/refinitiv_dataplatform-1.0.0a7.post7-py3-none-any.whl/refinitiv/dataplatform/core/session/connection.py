import abc
import logging
import urllib.parse

from refinitiv.dataplatform import configure
from refinitiv.dataplatform.errors import PlatformSessionError
from refinitiv.dataplatform.core.session import connect_config
from .session import Session

from .stream_service_discovery.stream_service_discovery_handler import StreamServiceInformation, \
                                                                        PlatformStreamServiceDiscoveryHandler
from .stream_service_discovery.stream_connection_configuration import RealtimeDistributionSystemConnectionConfiguration

from .authentication_token_handler_thread import AuthenticationTokenHandlerThread

class PlatformConnection(abc.ABC):
    def __init__(self, session):
        self._session = session

        self.log = session.log
        self.debug = session.debug

        #   a mapping the stream conenction status
        #       the key is the tuple of connection name and connection type (OMM, RDP, etc.)
        self.streaming_connection_name_and_connection_type_to_status = {}

    @abc.abstractmethod
    def get_omm_login_message_key_data(self):
        pass

    @abc.abstractmethod
    async def http_request_async(self, url: str, method=None, headers=None,
                                 data=None, params=None, json=None, closure=None,
                                 auth=None, loop=None, **kwargs):
        pass

    @abc.abstractmethod
    async def get_stream_connection_configuration(self, stream_connection_name:str):
        """ this function extract the realtime distribution system information from config file.
                note that the connection_name is a name of the session. default session name is "default-session"

        Parameters
        ----------
        stream_connection_name
            a unique name of the stream connection in the config file.
        i.e. "streaming/pricing/main"

        Returns
        -------
        obj
            the stream connection configuration of the given session and stream connection name
        """
        pass

    @abc.abstractmethod
    async def waiting_for_stream_ready(self, open_state):
        pass

    @abc.abstractmethod
    def authorize(self):
        pass

    @abc.abstractmethod
    def close(self):
        pass

    def get_stream_status(self, streaming_connection_name):
        return self.streaming_connection_name_and_connection_type_to_status.get(streaming_connection_name,
                                                            Session.EventCode.StreamDisconnected)

    def set_stream_status(self, streaming_connection_name, stream_status):
        self.streaming_connection_name_and_connection_type_to_status[streaming_connection_name] = stream_status


class RefinitivDataConnection(PlatformConnection):
    def __init__(self, session):
        super().__init__(session)

        ############################################################
        #   authentication token handler 

        #   build the token handler for this platform session
        self._authentication_token_handler_thread = AuthenticationTokenHandlerThread(session, 
                                                                                        session._grant, 
                                                                                        session.authentication_token_endpoint_url,
                                                                                        server_mode=session.server_mode)

    def get_omm_login_message_key_data(self):
        return {
            "NameType": "AuthnToken",
            "Elements": {
                "AuthenticationToken": self._session._access_token,
                "ApplicationId": self._session._dacs_params.dacs_application_id,
                "Position": self._session._dacs_params.dacs_position
            }
        }

    async def http_request_async(self, 
                                    url:str, method=None, headers=None,
                                    data=None, params=None, json=None,
                                    closure=None, auth=None, loop=None, 
                                    **kwargs):
        return await self._session._http_request_async(url, method=method, headers=headers,
                                                        data=data, params=params, json=json, 
                                                        closure=closure, auth=auth, loop=loop,
                                                        **kwargs)

    async def get_stream_connection_configuration(self, stream_connection_name:str):
        """ this function extract the realtime distribution system information from config file.
                note that the connection_name is a name of the session. default session name is "default-session"

        Parameters
        ----------
        stream_connection_name
            a unique name of the stream connection in the config file.
        i.e. "streaming/pricing/main"

        Returns
        -------
        obj
            the stream connection configuration of the given session and stream connection name
        """

        #   two ways of specific stream connection are discovery endpoint and WebSocket URL

        #       WebSocket url
        streaming_connection_endpoint_websocket_url = self._session.get_streaming_webscoket_endpoint_url(stream_connection_name)
        #       discovery endpoint
        streaming_connection_discovery_endpoint_url = self._session.get_streaming_discovery_endpoint_url(stream_connection_name)
        
        #       protocols
        streaming_connection_supported_protocols = self._session.get_streaming_protocols(stream_connection_name)
        self._session.debug(f'          {stream_connection_name} supported protocol are {streaming_connection_supported_protocols}')
        
        #   check for valid path for stream discovery endpoint
        if streaming_connection_endpoint_websocket_url is not None:
        #   override discovery endpoint by specific WebSocket endpoint url
            self._session.debug(f'override streaming by WebSocket endpoint url : {streaming_connection_endpoint_websocket_url}')

            #   build the stream service information and stream connection configuration

            #       parse the WebSocket url and build stream service information
            websocket_url_parse = urllib.parse.urlparse(streaming_connection_endpoint_websocket_url)
            stream_service_information = StreamServiceInformation(scheme=websocket_url_parse.scheme, 
                                                                        host=websocket_url_parse.hostname, 
                                                                        port=websocket_url_parse.port, 
                                                                        path=websocket_url_parse.path, 
                                                                        data_formats=['tr_json2'], 
                                                                        location=None,)
            
            #   build the stream connection configuration
            return RealtimeDistributionSystemConnectionConfiguration(self._session, 
                                                                        [stream_service_information, ],
                                                                        streaming_connection_supported_protocols)

        elif streaming_connection_discovery_endpoint_url is not None:
        #   valid stream discovery endpoint url
            self.debug(f'using discovery endpoint url : {streaming_connection_discovery_endpoint_url}')

             #   request the WebSocket endpoint from discovery service
            service_discovery_handler = PlatformStreamServiceDiscoveryHandler(self._session, 
                                                                                streaming_connection_discovery_endpoint_url)
            stream_service_informations = await service_discovery_handler.get_stream_service_information()
            
            #   build the stream connection configuration
            return RealtimeDistributionSystemConnectionConfiguration(self._session, 
                                                                        stream_service_informations,
                                                                        streaming_connection_supported_protocols)
        
        else:
        #   error
            raise ValueError('ERROR!!! streaming connection needed by specific url and path in endpoint section or specific WebSocket url.')

    async def waiting_for_stream_ready(self, open_state):
        pass

    def authorize(self):
        #   request a authentication token and wait for it
        self._authentication_token_handler_thread.authorize()
        self._session.debug(f'               waiting for authorize is ready..........')
        self._authentication_token_handler_thread.wait_for_authorize_ready()

        #   handle the error in authentication thread
        if self._authentication_token_handler_thread.is_error():
        #   an error occur in the authentication thread.
            self._session.error(f'ERROR!!! CANNOT authorize to RDP authentication endpoint.\n'
                                f'               {self._authentication_token_handler_thread.last_exception}')
            self.close()

            #   raise error
            raise self._authentication_token_handler_thread.last_exception

        assert not self._authentication_token_handler_thread.is_error() and self._authentication_token_handler_thread.is_alive()

    def close(self):
        self.log(logging.DEBUG, "Close platform session...")
        #   stop the authentication thread
        self._authentication_token_handler_thread.stop()
        return super().close()


class DeployedConnection(PlatformConnection):
    """ this class is designed for a connection to the realtime distribution system (aka. deployed platform or TREP)"""
    def __init__(self, session):
        super().__init__(session)
        self.streaming_connection_name_and_connection_type_to_status[self._session._deployed_platform_connection_name] = \
            Session.EventCode.StreamDisconnected

    def get_omm_login_message_key_data(self):
        return { "Name": self._session._dacs_params.deployed_platform_username,
                    "Elements": {
                        "ApplicationId": self._session._dacs_params.dacs_application_id,
                        "Position": self._session._dacs_params.dacs_position
                    }
                }

    async def http_request_async(self, url: str, method=None, headers=None, data=None, params=None, json=None,
                                 closure=None, auth=None, loop=None, **kwargs):
        raise PlatformSessionError(-1,
                                   'Error!!! Platform session cannot connect to refinitiv dataplatform. '
                                   'Please check or provide the access right.')

    async def get_stream_connection_configuration(self, stream_connection_name:str):
        """ this function extract the realtime distribution system information from config file.
                note that the connection_name is a name of the session. default session name is "default-session"

        Parameters
        ----------
        stream_connection_name
            a unique name of the stream connection in the config file.
        i.e. "streaming/pricing/main"

        Returns
        -------
        obj
            the stream connection configuration of the given session and stream connection name
        """
        
        #   get the realtime distribution system information from config file
        realtime_distribution_system_url_key = f'{configure.keys.platform_realtime_distribution_system(self._session._session_name)}.url'
        realtime_distribution_system_url = configure.get_str(realtime_distribution_system_url_key)
        self.debug(f'using the Refinitiv realtime url at {realtime_distribution_system_url}')

        #   construct host for host name and port
        realtime_distribution_system_url_parse = urllib.parse.urlparse(realtime_distribution_system_url)
        self.debug(f'      realtime_distribution_system scheme   = {realtime_distribution_system_url_parse.scheme}')
        self.debug(f'      realtime_distribution_system endpoint = {realtime_distribution_system_url_parse.hostname}')
        self.debug(f'      realtime_distribution_system port     = {realtime_distribution_system_url_parse.port}')

        #   build the StreamServiceInformation
        stream_service_information = StreamServiceInformation(scheme=realtime_distribution_system_url_parse.scheme, 
                                                                host=realtime_distribution_system_url_parse.hostname, 
                                                                port=realtime_distribution_system_url_parse.port, 
                                                                path=None, 
                                                                data_format=['tr_json2'], 
                                                                location=None,)
        
        #   build the stream connection configuration
        #       note it has only one realtime distribution.
        return RealtimeDistributionSystemConnectionConfiguration(self._session, 
                                                                    [stream_service_information, ],
                                                                    ['OMM', ])

    async def waiting_for_stream_ready(self, open_state):
        self.debug('waiting for deployed platform streaming ready.')

        #   do waiting for deployed platform session
        await self._session.wait_for_streaming(self._session._deployed_platform_connection_name) and open_state()

    def authorize(self):
        pass

    def close(self):
        self.log(logging.DEBUG, "Close platform session...")
        self._session._auth_manager.close()
        return super().close()


class RefinitivDataAndDeployedConnection(DeployedConnection, RefinitivDataConnection):
    def __init__(self, session):
        DeployedConnection.__init__(self, session)
        RefinitivDataConnection.__init__(self, session)

    async def http_request_async(self, url: str, method=None, headers=None, data=None, params=None, json=None,
                                 closure=None, auth=None, loop=None, **kwargs):
        return await RefinitivDataConnection.http_request_async(self, 
                                                        url, method=method, headers=headers,
                                                        data=data, params=params, json=json, 
                                                        closure=closure, auth=auth, loop=loop, 
                                                        **kwargs)

    def authorize(self):
        RefinitivDataConnection.authorize(self)

