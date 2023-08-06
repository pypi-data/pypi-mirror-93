"""
    Payment authorizations resource clients for the paypal resource group.

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
    PaypalApiResponse,
    PaymentInstruction,
    PaypalApiBulkResponse
)

from pypaypal.entities.payments.captures import Capture
from pypaypal.entities.payments.authorizations import Authorization

"""
    Base Resource Live URL
"""
_LIVE_RESOURCE_BASE_URL = parse_url(LIVE_API_BASE_URL, 'payments', 'authorizations')

"""
    Base Resource Sandbox URL
"""
_SANDBOX_RESOURCE_BASE_URL = parse_url(SANDBOX_API_BASE_URL, 'payments', 'authorizations')


T = TypeVar('T', bound = 'AuthorizationClient')

class AuthorizationClient(ClientBase):
    """Authorizations resource group client class.
    """
    def __init__(self, url: str, session: PayPalSession):
        super().__init__(url, session)
    
    def show_authorization_details(self, authorization_id: str) -> PaypalApiResponse[Authorization]:
        """Calls the paypal API to show details for an authorized payment, by ID.
        
        Arguments:
            authorization_id {str} -- The authorization id
        
        Returns:
            PaypalApiResponse[Authorization] -- An api response with the authorization details
        """
        api_response = self._session.get(parse_url(self._base_url, authorization_id))

        if api_response.status_code != 200:
            return PaypalApiResponse(True, api_response)

        return PaypalApiResponse(False, api_response, Authorization.serialize_from_json(api_response.json()))
    
    def capture_authorized_payment(
        self, authorization_id: str, invoice_id: str = None, note_to_payer: str = None,
        instruction: PaymentInstruction = None, amount: Money = None, final_capture: bool = False,
        request_id: str = None, response_type: ResponseType = ResponseType.MINIMAL) -> PaypalApiResponse[Capture]:
        """Calls the paypal API to capture an authorized payment, by ID.
        
        Arguments:
            authorization_id {str} -- authorization id
            invoice_id {str} -- associated invoice
            note_to_payer {str} -- informational notes about the settlement. Appears in the payer's transaction history and received emails.
        
        Keyword Arguments:
            instruction {PaymentInstruction} -- Any additional payment instructions for PayPal for Partner customers (default: {None})
            amount {Money} -- The amount to capture. If none the full amount will be captured (default: {None}).
            final_capture {bool} -- dictates whether you can make additional captures against the authorized payment (default: {False}).
            request_id {str} -- Paypal request id for idempotence (default: {None})
            response_type {ResponseType} -- desired response type (default: {ResponseType.MINIMAL})
        
        Returns:
            PaypalApiResponse[Authorization] -- An api response with the authorization details
        """
        body = dict()
        url = parse_url(self._base_url, authorization_id, 'capture')
        headers = {
            'Prefer': response_type.as_header_value()            
        }

        if request_id:
            headers['PayPal-Request-Id'] = request_id
        
        if invoice_id:
            body['invoice_id'] = invoice_id
        if note_to_payer:
            body['note_to_payer'] = note_to_payer
        if final_capture:
            body['final_capture'] = final_capture
        if instruction:
            body['instruction'] = instruction        
        if amount:
            body['amount'] = amount.to_dict()

        api_response = self._session.post(url, json.dumps(body), headers = headers)

        if api_response.status_code != 201:
            return PaypalApiResponse(True, api_response)

        return PaypalApiResponse(False, api_response, Capture.serialize_from_json(api_response.json()))

    def reauthorize_payment(
        self, authorization_id: str, amount: Money, request_id: str = None,
        response_type: ResponseType = ResponseType.MINIMAL) -> PaypalApiResponse[Authorization]:
        """Calls the paypal API to reauthorize an authorized payment, by ID. 
           See the api docs for a full set of rules.
        
        Arguments:
            authorization_id {str} -- The authorization id
            amount {Money} -- The amount to reauthorize for an authorized payment.
        Returns:
            PaypalApiResponse[Authorization] -- An api response with the authorization details
        """
        body = dict()
        url = parse_url(self._base_url, authorization_id, 'reauthorize')
        headers = {
            'Prefer': response_type.as_header_value()            
        }

        if request_id:
            headers['PayPal-Request-Id'] = request_id
        
        if amount:
            body['amount'] = amount.to_dict()

        api_response = self._session.post(url, json.dumps(body), headers = headers)

        if api_response.status_code != 201:
            return PaypalApiResponse(True, api_response)

        return PaypalApiResponse(False, api_response, Authorization.serialize_from_json(api_response.json()))

    def void_payment(self, authorization_id: str, auth_assertion_token: str = None) -> PaypalApiResponse:
        """Calls the paypal API to void an authorized payment, by ID. 
           See the api docs for a full set of rules.
        
        Arguments:
            authorization_id {str} -- The authorization id

        Keyword Arguments:
            auth_assertion_token {str} -- PayPal-Auth-Assertion see: https://developer.paypal.com/docs/api/payments/v2/docs/api/reference/api-requests/#paypal-auth-assertion (default: {None})
            
        Returns:
            PaypalApiResponse -- An api response with the authorization details.
        """
        api_response = None
        url = parse_url(self._base_url, authorization_id, 'void')

        if auth_assertion_token:
            api_response = self._session.post(url, None, headers = {'PayPal-Auth-Assertion' : auth_assertion_token})
        else:
            api_response = self._session.post(url, None)

        if api_response.status_code != 204:
            return PaypalApiResponse(True, api_response)

        return PaypalApiResponse(False, api_response)

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
