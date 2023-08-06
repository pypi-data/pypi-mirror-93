"""Referenced ReferencedPayouts resource client for the paypal resource group.

    Resource docs & Reference: https://developer.paypal.com/docs/api/referenced-ReferencedPayouts/v1/
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
    ResponseType, 
    PaypalApiResponse, 
    PatchUpdateRequest,
    PaypalApiBulkResponse
)

from pypaypal.entities.rpayouts import (
    ExecutionType,
    ReferencedPayoutsItem,
    ReferencedPayoutRequest,
    ReferencedPayoutResponse
)

"""
    Base Resource Live URL
"""
_LIVE_RESOURCE_BASE_URL = parse_url(LEGACY_LIVE_API_BASE_URL, 'payments')

"""
    Base Resource Sandbox URL
"""
_SANDBOX_RESOURCE_BASE_URL = parse_url(LEGACY_SANDBOX_API_BASE_URL, 'payments')

T = TypeVar('T', bound = 'ReferencedPayoutClient')

I = TypeVar('I', bound = 'ReferencedPayoutItemClient')

class ReferencedPayoutClient(ClientBase):
    """ReferencedPayout resource group client class.
    """
    
    def __init__(self, url: str, session: PayPalSession):
        super().__init__(url, session)
    
    def create_referenced_batch_payout(
        self, request: ReferencedPayoutRequest, request_id: str = None, partnerAttrId: str = None) -> PaypalApiBulkResponse[ActionLink]:
        """Creates a referenced batch payout for asynchronous, offline processing
        
        Arguments:
            request {ReferencedPayoutRequest} -- Request processing info
        
        Keyword Arguments:
            request_id {str} -- paypal request id for idempotence (default: {None})
            partnerAttrId {str} -- paypal partner attribution id (default: {None})
        
        Returns:
            PaypalApiBulkResponse[ActionLink] -- Batch links
        """
        headers = dict()

        if request_id:
            headers['PayPal-Request-Id'] = request_id
        if partnerAttrId:
            headers['PayPal-Partner-Attribution-Id'] = partnerAttrId
        if request.execution_type.is_async:
            headers['Prefer'] = 'respond-async'

        body = request.to_dict()
        body.pop('_execution_type', None)
        api_response = self._session.post(self._base_url, json.dumps(body), headers = headers)

        if api_response.status_code // 100 != 2:
            return PaypalApiBulkResponse.error(api_response)

        j_data = api_response.json()
        links = [ ActionLink(x['href'], x['rel'], x.get('method', 'GET')) for x in j_data.get('links', []) ]

        return PaypalApiBulkResponse.success(api_response, links)
    
    def _process_referenced_list_response(self, api_response) -> PaypalApiResponse[ReferencedPayoutResponse]:
        """Process the API response for the list batch payouts calls
        
        Arguments:
            api_response {[type]} -- Http api response
        
        Returns:
            PaypalApiResponse[ReferencedPayoutResponse] -- response info
        """
        if api_response.status_code // 100 != 2:
            return PaypalApiBulkResponse.error(api_response)
        
        j_data = api_response.json()
        return PaypalApiBulkResponse.success(api_response, ReferencedPayoutResponse.serialize_from_json(j_data) if j_data else None)        

    def list_referenced_batch_payout_items(self, payouts_batch_id: str) -> PaypalApiResponse[ReferencedPayoutResponse]:
        """Calls the API to list the payout items in a referenced batch payout. Each item in the list includes payout item details. 
        
        Arguments:
            payouts_batch_id {str} -- The batch id
        
        Returns:
            PaypalApiResponse[ReferencedPayoutResponse] -- Listed referenced payouts with the directive
        """
        return self._process_referenced_list_response(self._session.get(parse_url(self._base_url, payouts_batch_id)))

    def list_referenced_batch_payout_items_by_link(self, link: ActionLink) -> PaypalApiResponse[ReferencedPayoutResponse]:
        """Calls the API to list the payout items in a referenced batch payout. Each item in the list includes payout item details. 
        
        Arguments:
            payouts_batch_id {str} -- The batch id
        
        Returns:
            PaypalApiResponse[ReferencedPayoutResponse] -- Listed referenced payouts with the directive
        """
        return self._process_referenced_list_response(self._session.get(link.href))

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
        return cls(parse_url(base_url, 'referenced-payouts'), session)

class ReferencedPayoutItemClient(ClientBase):
    """Payout items resource group client class.
    """
    def __init__(self, url: str, session: PayPalSession):
        super().__init__(url, session)

    def _process_item_response(self, api_response) -> PaypalApiResponse[ReferencedPayoutsItem]:
        """Process the api response for a referenced payout item 
        
        Arguments:
            api_response {[type]} -- The paypal API response
        
        Returns:
            PaypalApiResponse[ReferencedPayoutsItem] -- The processed item
        """
        if api_response.status_code // 100 != 2:
            return PaypalApiBulkResponse.error(api_response)

        j_data = api_response.json()        
        return PaypalApiBulkResponse.success(
            api_response, 
            ReferencedPayoutsItem.serialize_from_json(j_data) if j_data else None
        )

    def create_referenced_payout_item(
            self, item: ReferencedPayoutsItem, request_id: str = None, 
            partnerAttrId: str = None, execution_type: ExecutionType = ExecutionType.SYNC
        ) -> PaypalApiResponse[ReferencedPayoutsItem]:
        """Calls the API to create a referenced payout item.
        
        Arguments:
            item {ReferencedPayoutsItem} -- The item to be registered
        
        Keyword Arguments:
            request_id {str} -- request id for idempotence (default: {None})
            partnerAttrId {str} -- paypal partner attribution id (default: {None})
            execution_type {ExecutionType} -- how will the API process the transaction (default: {ExecutionType.SYNC})
        
        Returns:
            PaypalApiResponse[ReferencedPayoutsItem] -- Api Response obj with the item basic info (id & links).
        """
        headers = dict()

        if request_id:
            headers['PayPal-Request-Id'] = request_id
        if partnerAttrId:
            headers['PayPal-Partner-Attribution-Id'] = partnerAttrId
        if execution_type.is_async:
            headers['Prefer'] = 'respond-async'

        return self._process_item_response(
            self._session.post(self._base_url, json.dumps(item.to_dict()), headers = headers)
        )
    
    def show_referenced_payout_item_details(self, payout_item_id: str, partnerAttrId: str = None) -> PaypalApiResponse[ReferencedPayoutsItem]:
        """Calls the paypal api to show a referenced payout item details.
        
        Arguments:
            payout_item_id {str} -- The item to be listed
        
        Keyword Arguments:
            partnerAttrId {str} -- paypal partner attribution id (default: {None})
        
        Returns:
            PaypalApiResponse[ReferencedPayoutsItem] -- Api Response obj with the item
        """
        url = parse_url(self._base_url, payout_item_id)
        headers = {'PayPal-Partner-Attribution-Id' : partnerAttrId } if payout_item_id else dict()
        return self._process_item_response(self._session.get(url, headers = headers))

    def show_referenced_payout_item_details_by_link(self, link: ActionLink, partnerAttrId: str = None) -> PaypalApiResponse[ReferencedPayoutsItem]:
        """Calls the paypal api to show a referenced payout item details.
        
        Arguments:
            link {ActionLink} -- Action link with the entity read url.8
        
        Keyword Arguments:
            partnerAttrId {str} -- paypal partner attribution id (default: {None})
        
        Returns:
            PaypalApiResponse[ReferencedPayoutsItem] -- Api Response obj with the item
        """
        url = link.href
        headers = {'PayPal-Partner-Attribution-Id' : partnerAttrId } if payout_item_id else dict()
        return self._process_item_response(self._session.get(url, headers = headers))

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
        return cls(parse_url(base_url, 'referenced-payouts-items'), session)