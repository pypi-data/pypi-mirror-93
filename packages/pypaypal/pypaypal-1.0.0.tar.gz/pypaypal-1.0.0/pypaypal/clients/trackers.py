"""
    Tracker resource clients for the paypal resource group.

    Resource docs & Reference: https://developer.paypal.com/docs/api/tracking/v1/ 
"""

import json
from typing import Type, TypeVar, List

from pypaypal.clients.base import ClientBase
from pypaypal.entities.base import ResponseType, PaypalApiResponse

from pypaypal.entities.trackers import Tracker

from pypaypal.http import ( 
    parse_url,
    PayPalSession,     
    LEGACY_LIVE_API_BASE_URL, 
    LEGACY_SANDBOX_API_BASE_URL 
)

"""
    Base Resource Live URL
"""
_LIVE_RESOURCE_BASE_URL = parse_url(LEGACY_LIVE_API_BASE_URL,'shipping/trackers')

"""
    Base Resource Sandbox URL
"""
_SANDBOX_RESOURCE_BASE_URL = parse_url(LEGACY_SANDBOX_API_BASE_URL,'shipping/trackers')

"""
    Supported tracker properties for tracking creation
"""
_TRACKER_PROPERTIES = { 
    'status', 'carrier', 'transaction_id', 'tracking_number', 'quantity', 'notify_buyer',
    'shipment_date', 'last_updated_time', 'carrier_name_other', 'postage_payment_id', 
    'tracking_number_validated' 
}

T = TypeVar('T', bound = 'TrackersClient')

class TrackersClient(ClientBase):
    """Trackers resource group client class
    """

    def __init__(self, url: str, session: PayPalSession):
        """Client ctor
        
        Arguments:
            session {PayPalSession} -- The http session 
        """
        super().__init__(url, session)

    def show_tracking_info(self, transaction_id: str, tracking_number: int, response_type: ResponseType= ResponseType.MINIMAL) -> PaypalApiResponse[Tracker]:
        """Gets the tracking info for a given tracker key
        
        Arguments:
            transaction_id {str} -- The id of the transaction
            tracking_number {int} -- The tracking number

        Keyword Arguments:
            response_type {ResponseType} -- [description] (default: {ResponseType.MINIMAL})
        
        Returns:
            PaypalApiResponse[Tracker] -- Response container with a Tracker instance including the required information
        """     
        headers = { 'Prefer': response_type.as_header_value() } 
        url = parse_url(self._base_url, f'{transaction_id}-{tracking_number}')
        api_response = self._session.get(url, None, headers=headers)
        
        if api_response.status_code != 200:
            return PaypalApiResponse(True, api_response)
        return PaypalApiResponse(False, api_response, Tracker.serialize_from_json(api_response.json(), response_type))

    def update_tracking_info(self, transaction_id: str, tracking_number: int, **kwargs) -> PaypalApiResponse[Tracker]:
        """Updates tracking info in the api
        
        Arguments:
            transaction_id {str} -- The id of the transaction
            tracking_number {int} -- The tracking number

        Keyword Arguments:
            mappings with the fields to be updated, see the docs for the names & values.
        
        Returns:
            PaypalApiResponse[Tracker] -- Response container with the response status
        """
        url = parse_url(self._base_url, f'{transaction_id}-{tracking_number}')
        api_response = self._session.put(url, json.dumps(kwargs))        
        error = api_response.status_code != 204

        return PaypalApiResponse(error, api_response)

    def add_trackers(self, trackers: List[Tracker], response_type: ResponseType= ResponseType.MINIMAL) -> PaypalApiResponse[Tracker]:
        """Adds trackers to a transaction
        
        Arguments:
            trackers {List[Tracker]} -- [description]
        
        Returns:
            PaypalApiResponse[Tracker] -- [description]
        """
        body = []
        url = parse_url(self._base_url, 'trackers-batch')
        headers = { 'Prefer': response_type.as_header_value() }

        for t in trackers:
            b = t.to_dict()
            b['shipment_date'] = b.pop('_shipment_date', None)
            b['last_updated_time'] = b.pop('_last_updated_time', None)
            self._clean_dictionary(b, _TRACKER_PROPERTIES)
            body.append(b)
        
        api_response = self._session.post(url, json.dumps(body), headers = headers)
        
        if api_response.status_code != 200:
            return PaypalApiResponse(True, api_response)
        return PaypalApiResponse(False, api_response, Tracker.serialize_from_json(api_response.json(), response_type))

    def tracking_info_by_entity(self, tracker: Tracker, response_type: ResponseType= ResponseType.MINIMAL) -> PaypalApiResponse[Tracker]:
        """Gets the tracking info for a given tracking entity
        
        Arguments:
            tracker {Tracker} -- a tracking entity
        
        Returns:
            PaypalApiResponse[Tracker] -- Response container with a Tracker instance including the required information
        """
        url = tracker.read_link
        headers = { 'Prefer': response_type.as_header_value() }
        api_response = self._execute_action_link(url, None, headers = headers)

        if api_response.status_code != 200:
            return PaypalApiResponse(True, api_response)
        return PaypalApiResponse(False, api_response, Tracker.serialize_from_json(api_response.json(), response_type))

    def update_tracking_info_by_entity(self, tracker: Tracker) -> PaypalApiResponse[Tracker]:
        """Updates tracking info in the api
        
        Arguments:
            transaction_id {str} -- The id of the transaction
            tracking_number {int} -- The tracking number

        Keyword Arguments:
            mappings with the fields to be updated, see the docs for the names & values.
        
        Returns:
            PaypalApiResponse[Tracker] -- Response container with the response status
        """
        body = tracker.json_data
        url = tracker.update_link

        for item in tracker.to_dict().items():
            key = item.key
            if key in body.keys():
                body[key] = item.value

        api_response = self._execute_action_link(url, body)
        error = api_response.status_code != 204
        return PaypalApiResponse(error, api_response)

    @classmethod
    def for_session(cls: T, session: PayPalSession) -> T:
        """Creates a tracker client from a given paypal session
        
        Arguments:
            cls {T} -- class reference
            session {PayPalSession} -- the paypal session
        
        Returns:
            T -- an instance of TrackersClient with the right configuration by session mode
        """
        base_url = _LIVE_RESOURCE_BASE_URL if session.session_mode.is_live() else _SANDBOX_RESOURCE_BASE_URL
        return cls(base_url, session)