"""Payouts resource client for the paypal resource group.

    Resource docs & Reference: https://developer.paypal.com/docs/api/payments.payouts-batch/v1/
"""

import json

from typing import Type, TypeVar, List
from pypaypal.clients.base import ClientBase, ActionLink

from pypaypal.http import ( 
    parse_url,
    PayPalSession,
    LEGACY_LIVE_API_BASE_URL,
    LEGACY_SANDBOX_API_BASE_URL
)

from pypaypal.entities.base import ( 
    PaypalPage,
    ResponseType, 
    PaypalApiResponse, 
    PatchUpdateRequest,
    PaypalApiBulkResponse
)

from pypaypal.entities.payouts import (
    PayoutItem,
    PagedPayout,
    PayoutHeader,
    SenderBatchHeader
)

"""
    Base Resource Live URL
"""
_LIVE_RESOURCE_BASE_URL = parse_url(LEGACY_LIVE_API_BASE_URL, 'payments')

"""
    Base Resource Sandbox URL
"""
_SANDBOX_RESOURCE_BASE_URL = parse_url(LEGACY_SANDBOX_API_BASE_URL, 'payments')

T = TypeVar('T', bound = 'PayoutClient')

I = TypeVar('I', bound = 'PayoutItemClient')

class PayoutClient(ClientBase):
    """Payout resource group client class.
    """
    
    def __init__(self, url: str, session: PayPalSession):
        super().__init__(url, session)
    
    def create_batch_payout(self, sender_batch_header: SenderBatchHeader, items: List[PayoutItem], request_id: str = None) -> PaypalApiResponse[PayoutHeader]:
        """Calls the paypal API to create a batch payout to one or more recipients
        
        Arguments:
            sender_batch_header {SenderBatchHeader} -- Sender-provided payout header for a payout request.
            items {List[PayoutItem]} -- A list of individual payout items.
        
        Keyword Arguments:
            request_id {str} -- Request id for idempotence (default: {None})
        
        Returns:
            PaypalApiResponse[PayoutHeader] -- A response with the generated header.
        """
        headers = dict()
        url = self._base_url

        if request_id:
            headers['PayPal-Request-Id'] = request_id
        
        body = json.dumps({ sender_batch_header.to_dict(), items.to_dict() })
        api_response = self._session.post(url, body, headers = headers) if headers else self._session.post(url, body)

        if api_response.status_code // 100 != 2:
            return PaypalApiResponse.error(api_response)

        j_data = api_response.json().get('batch_header')

        return PaypalApiResponse.success(api_response, PayoutHeader.serialize_from_json(j_data) if j_data else None)

    def show_payout_batch_details(
        self, payout_batch_id: str, page: int = 1, page_size: int = 1000, 
        fields: str = None, total_required: bool = True) -> PaypalApiResponse[PagedPayout]:
        
        url = parse_url(self._base_url, payout_batch_id)
        params = { 'page': page,  'page_size': page_size, 'total_required': total_required }

        if fields:
            params['fields'] = fields
        
        api_response = self._session.get(url, params)

        if api_response.status_code // 100 != 2:
            return PaypalApiResponse.error(api_response)

        return PaypalApiResponse.success(api_response, PagedPayout.serialize_from_json(api_response.json()))

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
        return cls(parse_url(base_url, 'payouts'), session)

class PayoutItemClient(ClientBase):
    """Payout items resource group client class.
    """
    def __init__(self, url: str, session: PayPalSession):
        super().__init__(url, session)

    def show_payout_item_details(self, payout_item_id: str) -> PaypalApiResponse[PayoutItem]:
        """Calls the paypal API to show a payout item details
        
        Arguments:
            payout_item_id {str} -- Desired payout item id
        
        Returns:
            PaypalApiResponse[PayoutItem] -- Response with the item data if successful
        """        
        api_response = self._session.get(parse_url(self._base_url, payout_item_id))

        if api_response.status_code // 100 != 2:
            return PaypalApiResponse.error(api_response)

        return PaypalApiResponse.success(api_response, PayoutItem.serialize_from_json(api_response.json()))

    def cancel_unclaimed_payout_item(self, payout_item_id: str) -> PaypalApiResponse[PayoutItem]:
        """Calls the paypal API to cancel an unclaimed payout item details
        
        Arguments:
            payout_item_id {str} -- Desired payout item id
        
        Returns:
            PaypalApiResponse[PayoutItem] -- Response with the item data if successful
        """        
        api_response = self._session.post(parse_url(self._base_url, payout_item_id))

        if api_response.status_code // 100 != 2:
            return PaypalApiResponse.error(api_response)

        j_data = api_response.json()
        
        if j_data:
            PaypalApiResponse.success(api_response, PayoutItem.serialize_from_json(j_data))

        return PaypalApiResponse.success(api_response)

    @classmethod
    def for_session(cls: T, session: PayPalSession) -> I:
        """Creates a client from a given paypal session
        
        Arguments:
            cls {T} -- class reference
            session {PayPalSession} -- the paypal session
        
        Returns:
            T -- an instance of Dispute client with the right configuration by session mode
        """
        base_url = _LIVE_RESOURCE_BASE_URL if session.session_mode.is_live() else _SANDBOX_RESOURCE_BASE_URL
        return cls(parse_url(base_url, 'payouts-item'), session)
