"""
    Payment captures resource clients for the paypal resource group.

    Resource docs & Reference: https://developer.paypal.com/docs/api/payments/v2/ 
"""
import json

from datetime import datetime
from typing import Type, TypeVar, List

from pypaypal.clients.base import ClientBase, ActionLink

from pypaypal.http import ( 
    parse_url,
    PayPalSession,
    LIVE_API_BASE_URL,
    SANDBOX_API_BASE_URL
)

from pypaypal.entities.base import ( 
    Money,
    ResponseType,
    PaypalApiResponse
)

from pypaypal.entities.payments.refunds import Refund
from pypaypal.entities.payments.captures import Capture

"""
    Base Resource Live URL
"""
_LIVE_RESOURCE_BASE_URL = parse_url(LIVE_API_BASE_URL, 'payments', 'captures')

"""
    Base Resource Sandbox URL
"""
_SANDBOX_RESOURCE_BASE_URL = parse_url(SANDBOX_API_BASE_URL, 'payments', 'captures')

T = TypeVar('T', bound = 'CaptureClient')

class CaptureClient(ClientBase):
    """Captures resource group client class.
    """
    def __init__(self, url: str, session: PayPalSession):
        super().__init__(url, session)

    def show_capture_details(self, capture_id: str) -> PaypalApiResponse[Capture]:
        """Calls the paypal API to show details for an authorized payment, by ID.
        
        Arguments:
            capture_id {str} -- The capture id
        
        Returns:
            PaypalApiResponse[Capture] -- An api response with the capture details
        """
        api_response = self._session.get(parse_url(self._base_url, capture_id))

        if api_response.status_code != 200:
            return PaypalApiResponse(True, api_response)

        return PaypalApiResponse(False, api_response, Capture.serialize_from_json(api_response.json()))

    def refund_capture(
        self, capture_id: str, invoice_id: str, note_to_payer: str, 
        amount: Money = None, request_id: str = None, auth_assertion_token: str = None,
        response_type: ResponseType = ResponseType.MINIMAL) -> PaypalApiResponse[Refund]:
        """Calls the api to refund a capture
        
        Arguments:
            capture_id {str} -- capture identifier
            invoice_id {str} -- invoice related capture
            note_to_payer {str} -- notes to the customer
        
        Keyword Arguments:
            amount {Money} -- amount to be refunded if None then 'captured amount - previous refunds' (default: {None})
            request_id {str} -- request id for idempotence (default: {None})
            auth_assertion_token {str} -- auth assertion token. See paypal header docs (default: {None})
            response_type {ResponseType} -- response type. See paypal header docs (default: {ResponseType.MINIMAL})
        
        Returns:
            PaypalApiResponse[Refund] -- api response with refund details
        """

        body = dict()
        url = parse_url(self._base_url, capture_id, 'refund')

        headers = {
            'Prefer': response_type.as_header_value()            
        }

        if request_id:
            headers['PayPal-Request-Id'] = request_id
        if auth_assertion_token:
            headers['PayPal-Auth-Assertion'] = auth_assertion_token

        if invoice_id:
            body['invoice_id'] = invoice_id
        if note_to_payer:
            body['note_to_payer'] = note_to_payer
        if amount:
            body['amount'] = amount.to_dict()

        api_response = self._session.post(url, json.dumps(body), headers = headers)

        if api_response.status_code != 201:
            return PaypalApiResponse(True, api_response)

        return PaypalApiResponse(False, api_response, Refund.serialize_from_json(api_response.json()))

    @classmethod
    def for_session(cls: T, session: PayPalSession) -> T:
        """Creates a client from a given paypal session
        
        Arguments:
            cls {T} -- class reference
            session {PayPalSession} -- the paypal session
        
        Returns:
            T -- an instance of Dispute client with the right configuration by session mode
        """
        base_url = _LIVE_RESOURCE_BASE_URL if session.session_mode.is_live() else _SANDBOX_RESOURCE_BASE_URL
        return cls(base_url, session)
