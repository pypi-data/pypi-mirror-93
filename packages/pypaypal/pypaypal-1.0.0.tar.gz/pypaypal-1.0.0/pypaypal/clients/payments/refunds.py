"""
    Payment refunds resource clients for the paypal resource group.

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
    ResponseType,
    PaypalApiResponse,
)

from pypaypal.entities.payments.refunds import Refund

"""
    Base Resource Live URL
"""
_LIVE_RESOURCE_BASE_URL = parse_url(LIVE_API_BASE_URL, 'payments', 'refunds')

"""
    Base Resource Sandbox URL
"""
_SANDBOX_RESOURCE_BASE_URL = parse_url(SANDBOX_API_BASE_URL, 'payments', 'refunds')

T = TypeVar('T', bound = 'RefundClient')

class RefundClient(ClientBase):
    """Refunds resource group client class.
    """
    def __init__(self, url: str, session: PayPalSession):
        super().__init__(url, session)

    def show_refund_details(self, refund_id: str) -> PaypalApiResponse[Refund]:
        """Calls the paypal API to show details for an authorized payment, by ID.
        
        Arguments:
            refund_id {str} -- The refund id
        
        Returns:
            PaypalApiResponse[Refund] -- An api response with the refund details
        """
        api_response = self._session.get(parse_url(self._base_url, refund_id))

        if api_response.status_code != 200:
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
