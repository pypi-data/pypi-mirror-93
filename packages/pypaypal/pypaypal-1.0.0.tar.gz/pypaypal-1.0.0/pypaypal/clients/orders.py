"""
    Checkout Order resource clients for the paypal resource group.

    Resource docs & Reference: https://developer.paypal.com/docs/api/orders/v2/  
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
    ResponseType, 
    PaypalApiResponse, 
    PatchUpdateRequest,
    PaypalApiBulkResponse
)

from pypaypal.entities.orders import Order, PaymentSource

"""
    Base Resource Live URL
"""
_LIVE_RESOURCE_BASE_URL = parse_url(LIVE_API_BASE_URL, 'checkout', 'orders')

"""
    Base Resource Sandbox URL
"""
_SANDBOX_RESOURCE_BASE_URL = parse_url(SANDBOX_API_BASE_URL, 'checkout', 'orders')


T = TypeVar('T', bound = 'OrderClient')

class OrderClient(ClientBase):
    """Orders resource group client class.
    """
    def __init__(self, url: str, session: PayPalSession):
        super().__init__(url, session)

    def create_order(self, order: Order, request_id: str = None, partner_attr_id: str = None, response_type: ResponseType = ResponseType.MINIMAL) -> PaypalApiResponse[Order]:
        """Calls the paypal Api to create an order
        
        Arguments:
            order {Order} -- The order information.
        
        Keyword Arguments:
            request_id {str} -- Paypal request id for idempotency (default: {None})
            partner_attr_id {str} --  Identifies the caller as a PayPal partner. To receive revenue attribution. (default: {None})
            response_type {ResponseType} -- Response type to be handled (default: {ResponseType.MINIMAL})
        
        Returns:
            PaypalApiResponse[Order] -- An api response with the order
        """
        url = self._base_url
        
        headers = { 'Prefer': response_type.as_header_value() }

        if request_id:
            headers['PayPal-Request-Id'] = request_id
        if partner_attr_id:
            headers['PayPal-Partner-Attribution-Id'] = partner_attr_id
        
        api_response = self._session.post(url, json.dumps(order.to_dict()), headers = headers)

        if api_response.status_code // 100 != 2:
            return PaypalApiResponse(True, api_response)

        return PaypalApiResponse(False, api_response, Order.serialize_from_json(api_response.json(), response_type))

    def update_order(self, order_id: str, updates: List[PatchUpdateRequest]) -> PaypalApiResponse:
        """Updates an order with the CREATED or APPROVED status.
        
        Arguments:
            order_id {str} -- The id of the order to be updated.
            updates {List[PatchUpdateRequest]} -- The updates to be made.
        
        Returns:
            PaypalApiResponse -- API operation response
        """
        url = parse_url(self._base_url, order_id)
        body = json.dumps([{ 'op': x.operation, 'path': x.path, 'value': x.value } for x in updates ])

        api_response = self._session.patch(url, body)

        if api_response.status_code != 204:
            return PaypalApiResponse(True, api_response)

        return PaypalApiResponse(False, api_response)

    def show_order_details(self, order_id: str) -> PaypalApiResponse[Order]:
        """Calls the api to retrieve the order details
        
        Arguments:
            order_id {str} -- The id of the order.
        
        Returns:
            PaypalApiResponse -- API operation response with the order if successful
        """
        api_response = self._session.get(parse_url(self._base_url, order_id))

        if api_response.status_code != 200:
            return PaypalApiResponse(True, api_response)

        return PaypalApiResponse(False, api_response, Order.serialize_from_json(api_response.json()))

    def authorize_payment_for_order(
        self, order_id: str, payment_source: PaymentSource = None,
        request_id: str = None,  client_metadata_id: str = None,
        auth_assertion: str = None, response_type: ResponseType = ResponseType.MINIMAL) -> PaypalApiResponse[Order]:
        """Calls the API to Authorize a payment for an order. 
           To successfully authorize payment for an order, 
           the buyer must first approve the order 
           or a valid payment_source must be provided in the request.
        
        Arguments:
            order_id {str} -- The order id
        
        Keyword Arguments:
            payment_source {PaymentSource} -- Source of payment for the order if the user wasn't redirected in the order creation to approve the payment. (default: {None})
            request_id {str} -- Request id for idempotence (default: {None})
            client_metadata_id {str} -- Verifies that the payment originates from a valid, user-consented device and application. Must be included in order to be eligible for PayPal Seller Protection. (default: {None})
            auth_assertion {str} -- A JWT assertion that identifies the merchant (default: {None})
            response_type {ResponseType} --  (default: {ResponseType.MINIMAL})
        
        Returns:
            PaypalApiResponse[Order] -- API operation response with the order if successful
        """
        url = parse_url(self._base_url, order_id, 'authorize')
        
        headers = { 'Prefer': response_type.as_header_value() }

        if request_id:
            headers['PayPal-Request-Id'] = request_id
        if  auth_assertion:
            headers['PayPal-Auth-Assertion'] = auth_assertion
        if client_metadata_id:
            headers['PayPal-Client-Metadata-Id'] = client_metadata_id

        if payment_source:
            api_response = self._session.post(url, json.dumps(payment_source.to_dict()), headers = headers)
        else:
            api_response = self._session.post(url, None)

        if api_response.status_code // 100 != 2:
            return PaypalApiResponse(True, api_response)
        
        return PaypalApiResponse(False, api_response, Order.serialize_from_json(api_response.json(), response_type))

    def capture_payment_for_order(
        self, order_id: str, payment_source: PaymentSource = None,
        request_id: str = None,  client_metadata_id: str = None,
        auth_assertion: str = None, response_type: ResponseType = ResponseType.MINIMAL) -> PaypalApiResponse[Order]:
        """Calls the API to Capture a payment for an order. 
           To successfully authorize payment for an order, 
           the buyer must first approve the order 
           or a valid payment_source must be provided in the request.
        
        Arguments:
            order_id {str} -- The order id
        
        Keyword Arguments:
            payment_source {PaymentSource} -- Source of payment for the order if the user wasn't redirected in the order creation to approve the payment. (default: {None})
            request_id {str} -- Request id for idempotence (default: {None})
            client_metadata_id {str} -- Verifies that the payment originates from a valid, user-consented device and application. Must be included in order to be eligible for PayPal Seller Protection. (default: {None})
            auth_assertion {str} -- A JWT assertion that identifies the merchant (default: {None})
            response_type {ResponseType} --  (default: {ResponseType.MINIMAL})
        
        Returns:
            PaypalApiResponse[Order] -- API operation response with the order if successful
        """
        url = parse_url(self._base_url, order_id, 'capture')
        
        headers = { 'Prefer': response_type.as_header_value() }

        if request_id:
            headers['PayPal-Request-Id'] = request_id
        if  auth_assertion:
            headers['PayPal-Auth-Assertion'] = auth_assertion
        if client_metadata_id:
            headers['PayPal-Client-Metadata-Id'] = client_metadata_id

        if payment_source:
            api_response = self._session.post(url, json.dumps(payment_source.to_dict()), headers = headers)
        else:
            api_response = self._session.post(url, None)

        if api_response.status_code // 100 != 2:
            return PaypalApiResponse(True, api_response)
        
        return PaypalApiResponse(False, api_response, Order.serialize_from_json(api_response.json(), response_type))

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
