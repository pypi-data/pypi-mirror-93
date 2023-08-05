# coding: utf-8

__all__ = ['send_json_request', 'check_server_error']

import json
import time

import requests_async as requests

try:
    from json.decoder import JSONDecodeError
except ImportError:
    JSONDecodeError = ValueError

import sys
from .tools import is_string_type, DefaultSession
from refinitiv.dataplatform.errors import RDPError


def send_json_request(entity, payload, ID='123', debug=False, raw_response=False):
    """
    Returns the JSON response.
    This legacy can be used for advanced usage or early access to new features.

    Parameters
    ----------
    entity: string
        A string containing a service name

    payload: string
        A string containing a JSON request

    debug: boolean, optional
        When set to True, the json request and response are printed.
        Default: False

    Returns
    -------
    string
        The JSON response as a string

    Raises
    ------
    ElektronError

        If daemon is disconnected

    requests.Timeout
        If request times out

    Exception
        If request fails (HTTP code other than 200)

    ElektronError
        If daemon is disconnected
    """
    _session = DefaultSession.get_default_session()
    if _session:
        logger = _session.logger()
        logger.debug("entity: {}".format(entity))
        logger.debug("payload: {}".format(payload))

        if not is_string_type(entity):
            error_msg = 'entity must be a string identifying an UDF endpoint'
            logger.error(error_msg)
            raise ValueError(error_msg)
        try:
            if is_string_type(payload):
                data = json.loads(payload)
            elif type(payload) is dict:
                data = payload
            else:
                error_msg = 'payload must be a string or a dictionary'
                logger.error(error_msg)
                raise ValueError(error_msg)
        except JSONDecodeError as e:
            error_msg = 'payload must be json well formed.\n'
            error_msg += str(e)
            logger.error(error_msg)
            raise e

        try:
            # build the request
            udf_request = {"Entity": {"E": entity, "W": data}, "ID": ID}
            logger.debug('Request to {} :{}'.format(_session._get_udf_url(), udf_request))
            response = _session.http_request(method='POST',
                                             url=_session._get_udf_url(),
                                             headers={"Content-Type": "application/json"},
                                             # "x-tr-applicationid": _session.app_key},
                                             json=udf_request)

            try:
                logger.debug('HTTP Response code: {}'.format(response.status_code))
                logger.debug('HTTP Response: {}'.format(response.text))
            except UnicodeEncodeError:
                logger.error('HTTP Response: cannot decode error message')

            if response.status_code == 200:
                result = {}
                try:
                    result = response.json()
                    logger.debug('Response size: {}'.format(sys.getsizeof(json.dumps(result))))
                except JSONDecodeError:
                    logger.error(f"Failed to decode response to json: {response.text}")

                # Manage specifically DataGrid async mode
                if entity.startswith('DataGrid') and entity.endswith('Async'):
                    ticket = _check_ticket_async(result)
                    while ticket:
                        ticket_request = {'Entity': {
                                             'E': entity,
                                             'W': {'requests': [{'ticket': ticket}]}
                                         }}
                        logger.debug('Send ticket request:{}'.format(ticket_request))
                        # response = _session.post(_session._get_udf_url(),
                        #                          json=ticket_request,
                        #                          headers={"Content-Type": "application/json",
                        #                          "x-tr-applicationid": _session.app_key},
                        #                          timeout=15.0)
                        response = _session.http_request(method='POST',
                                                         url=_session._get_udf_url(),
                                                         headers={"Content-Type": "application/json"},
                                                         json=ticket_request)

                        result = response.json()
                        logger.debug('Response size: {}'.format(sys.getsizeof(json.dumps(result))))
                        ticket = _check_ticket_async(result)

                if not raw_response:
                    check_server_error(result)
                return response
            else:
                raise_for_status(response)

        except requests.exceptions.ConnectionError as connectionError:
            network_error = True
        if network_error:
            error_msg = 'Eikon Proxy not installed or not running. Please read the documentation to know how to install and run the proxy'
            logger.error(error_msg)
            raise RDPError('401', error_msg)


def _check_ticket_async(server_response):
    """
    Check server response.

    Check is the server response contains a ticket.

    :param server_response: request's response
    :type server_response: requests.Response
    :return: ticket value if response contains a ticket, None otherwise
    """
    logger = DefaultSession.get_default_session().logger()
    # ticket response should contains only one key
    if len(server_response) == 1:
        for key, value in server_response.items():
            ticket = value[0]
            if ticket and ticket.get('estimatedDuration'):
                ticket_duration = int(ticket['estimatedDuration'])
                ticket_duration = min(ticket_duration, 15000)
                ticket_value = ticket['ticket']
                message = 'Receive ticket from {}, wait for {} second'.format(key, ticket_duration / 1000.0)
                if ticket_duration > 1000:
                    message = message + 's'
                logger.info(message)
                time.sleep(ticket_duration / 1000.0)
                return ticket_value
    return None


def check_server_error(server_response, session=None):
    """
    Check server response.

    Check is the server response contains an HTPP error or a server error.

    :param server_response: request's response
    :type server_response: requests.Response
    :return: nothing

    :raises: Exception('HTTP error : <_message>) if response contains HTTP response
              ex: '<500 Server error>'
          or Exception('Server error (<error code>) : <server_response>') if UDF returns an error
              ex: {u'ErrorCode': 500, u'ErrorMessage': u'Requested datapoint was not found: News_Headlines', u'Id': u''}

    """
    if session:
        logger = session.logger()
    else:
        logger = DefaultSession.get_default_session().logger()

    # check HTTP response (server response is an object that can contain ErrorCode attribute)
    if hasattr(server_response, 'ErrorCode'):
        logger.error(getattr(server_response, 'ErrorMessage'))
        raise RDPError(server_response['ErrorCode'],
                       getattr(server_response, 'ErrorMessage'))

    # # check HTTPError on proxy request
    # str_response = server_response.text
    # if str_response.startswith('<') and str_response.endswith('>'):
    #     logger.error(str_response)
    #     raise ElektronError(server_response['ErrorCode'],
    #                         getattr(server_response, 'ErrorMessage'))
    #     raise requests.HTTPError(response=server_response)

    # check UDF response (server response is JSON and it can contain ErrorCode + ErrorMessage keys)
    if isinstance(server_response, dict):
        if 'ErrorCode' in server_response and 'ErrorMessage' in server_response:
            error_message = server_response['ErrorMessage']
            # if len(_message.split(',')) > 4:
            #     status, reason_phrase, version, content, headers = _message.split(',')[:5]
            logger.error(error_message)
            raise RDPError(server_response['ErrorCode'], error_message)

    # check DataGrid response (server response is JSON or text and it can contain error + optionally transactionId keys)
    if 'error' in server_response:
        if 'transactionId' in server_response:
            error_message = f"{server_response['error']} (transactionId:{server_response['transactionId']}"
        else:
            error_message = f"{server_response['error']} (no transactionId)"
        logger.error(error_message)
        raise RDPError(400, error_message)


def raise_for_status(response):
    """Raises stored :class:`HTTPError`, if one occurred."""

    error_msg = ''
    if isinstance(response.reason_phrase, bytes):
        # We attempt to decode utf-8 first because some servers
        # choose to localize their reason strings. If the string
        # isn't utf-8, we fall back to iso-8859-1 for all other
        # encodings. (See PR #3538)
        try:
            reason = response.reason_phrase.decode('utf-8')
        except UnicodeDecodeError:
            reason = response.reason_phrase.decode('iso-8859-1')
    else:
        reason = response.reason_phrase

    logger = DefaultSession.get_default_session().logger()

    # if DefaultSession.get_default_session().get_log_level() < logging.INFO:
    #     # Check if retry-after is in headers
    #     rate_limit = response.headers.get('x-ratelimit-limit')
    #     rate_remaining = response.headers.get('x-ratelimit-remaining')
    #     volume_limit = response.headers.get('x-volumelimit-limit')
    #     volume_remaining = response.headers.get('x-volumelimit-remaining')
    #
    #     retry_after = response.headers.get('retry-after')
    #     logger.trace('Headers: x_ratelimit_limit={} / x_ratelimit_remaining={} '.format(rate_limit, rate_remaining))
    #     logger.trace('         x_volumelimit_limit={} / x_volumelimit_remaining={}'.format(volume_limit, volume_remaining))
    #     logger.trace('         retry_after {}'.format(retry_after))

    if 400 <= response.status_code < 500:
        error_msg = u'Client Error: %s - %s' % (reason, response.text)
    elif 500 <= response.status_code < 600:
        error_msg = u'Server Error: %s - %s' % (reason, response.text)

    if error_msg:
        logger.error(u'Error code {} | {}'.format(response.status_code, error_msg))
        raise RDPError(response.status_code, error_msg)
