"""
    Subscription resource client for the paypal resource group.

    Resource docs & Reference: https://developer.paypal.com/docs/api/subscriptions/v1/
"""
import json

from datetime import datetime
from typing import Type, TypeVar, List, NamedTuple

from pypaypal.entities.base import Money
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

from pypaypal.entities.payments.captures import Capture

from pypaypal.entities.subscriptions.subscriptions import ( 
    Subscription, 
    ShippingDetail,
    SubscriptionTransaction,
    SubscriptionApplicationContext
)

"""
    Base Resource Live URL
"""
_LIVE_RESOURCE_BASE_URL = parse_url(LEGACY_LIVE_API_BASE_URL, 'billing', 'subscriptions')

"""
    Base Resource Sandbox URL
"""
_SANDBOX_RESOURCE_BASE_URL = parse_url(LEGACY_SANDBOX_API_BASE_URL, 'billing', 'subscriptions')

T = TypeVar('T', bound = 'SubscriptionClient')

class SubscriptionQuantityUpdateRequest(NamedTuple):
    """Immutable class to request a subscription quantity update for a product/service.
    """
    plan_id: str
    quantity: str
    shipping_amount: Money
    shipping_address: ShippingDetail
    application_context: SubscriptionApplicationContext

    def to_dict(self) -> dict:
        return {
            'plan_id': self.plan_id,
            'quantity': self.quantity,
            'shipping_amount': self.shipping_amount.to_dict(),
            'shipping_address': self.shipping_address.to_dict(),
            'application_context': self.application_context.to_dict()
        }

class SubscriptionClient(ClientBase):
    """Subscriptions resource group client class.
    """
    def __init__(self, url: str, session: PayPalSession):
        super().__init__(url, session)

    def create_subscription(self, subscription: Subscription, request_id: str = None, response_type: ResponseType = ResponseType.MINIMAL) -> PaypalApiResponse[Subscription]:
        """Calls the paypal API to create a subscription
        
        Arguments:
            subscription {Subscription} -- The subscription to be made (use the create factory method)
        
        Keyword Arguments:
            request_id {str} -- Paypal request id for idempotence (default: {None})
            response_type {ResponseType} -- Peferred response type (default: {ResponseType.MINIMAL})
        
        Returns:
            PaypalApiResponse[Subscription] -- an API response object with the subscription info
        """
        url = self._base_url
        body = json.dumps(subscription.to_dict())
        headers = { 'Prefer': response_type.as_header_value() }

        if request_id:
            headers['PayPal-Request-Id'] = request_id
        
        api_response = self._session.post(url, body, headers = headers)

        if api_response.status_code // 100 != 2:
            return PaypalApiResponse.error(api_response)
        
        return PaypalApiResponse.success(api_response, Subscription.serialize_from_json(api_response.json(), response_type))

    def update_subscription(self, subscription_id: str, update_request: List[PatchUpdateRequest]) -> PaypalApiResponse:
        """Patch request to update a subscription. See the docs for details 
        
        Arguments:
            subscription_id {str} -- id of the subscription to be updated.
            update_request {PatchUpdateRequest} -- request object with update info.
        
        Returns:
            PaypalApiResponse -- Response obj with operation status
        """
        url = parse_url(self._base_url, subscription_id) 
        body = json.dumps([ {'op': x.operation, 'value': x.value, 'path': x.path } for x in update_request ])

        api_response = self._session.patch(url, body)

        if api_response.status_code // 100 != 2:
            return PaypalApiResponse.error(api_response)
        
        return PaypalApiResponse.success(api_response)

    def show_subscription_details(self, subscription_id: str) -> PaypalApiResponse[Subscription]:
        """Calls the paypal API to get a subscription details
        
        Arguments:
            subscription_id {str} -- The subscription identifier
        
        Returns:
            PaypalApiResponse[Subscription] -- Api response obj with the subscription info.
        """
        api_response = self._session.get(parse_url(self._base_url, subscription_id))

        if api_response.status_code // 100 != 2:
            return PaypalApiResponse.error(api_response)
        
        return PaypalApiResponse.success(api_response, Subscription.serialize_from_json(api_response.json()))

    def activate_subscription(self, subscription_id: str) -> PaypalApiResponse:
        """Calls the API to activate a subscription
        
        Arguments:
            subscription_id {str} -- The id of the subscription to activate
        
        Returns:
            PaypalApiResponse -- Response with the operation status
        """
        return self._execute_subscription_action(subscription_id, 'activate')

    def reactivate_subscription(self, subscription_id: str, reason: str) -> PaypalApiResponse:
        """Calls the API to re-activate a subscription
        
        Arguments:
            subscription_id {str} -- The id of the subscription to activate
        
        Returns:
            PaypalApiResponse -- Response with the operation status
        """
        return self._execute_subscription_action(subscription_id, 'activate', reason)
    
    def cancel_subscription(self, subscription_id: str, reason: str) -> PaypalApiResponse:
        """Calls the API to cancel a subscription
        
        Arguments:
            subscription_id {str} -- The id of the subscription to cancel
        
        Returns:
            PaypalApiResponse -- Response with the operation status
        """
        return self._execute_subscription_action(subscription_id, 'cancel', reason)

    def capture_authorized_payment_on_subscription(
            self, subscription_id: str, note: str, amount: Money, 
            capture_type: str = 'OUTSTANDING_BALANCE', request_id: str = None
        ) -> PaypalApiResponse[Capture]:
        """ Calls the Paypal API to perform a capture on an authorized payment 
            from the subscriber on the subscription.
        
        Arguments:
            subscription_id {str} -- the subscription id
            note {str} -- The reason or note for the subscription charge.
            amount {Money} -- The amount of the outstanding balance. Must not be greater than the current outstanding balance amount.
        
        Returns:
            PaypalApiResponse[Capture] -- A response with a capture
        """
        url = parse_url(self._base_url, subscription_id, 'capture')
        
        body = json.dumps({
            'note': note, 
            'amount': amount.to_dict(), 
            'capture_type': capture_type
        })

        if not request_id:
            api_response = self._session.post(url, body)
        else:
            api_response = self._session.post(url, body, headers = { 'PayPal-Request-Id': request_id })
             
        if api_response.status_code // 100 != 2:
            return PaypalApiResponse.error(api_response)
        
        j_data = api_response.json()
        return PaypalApiResponse.success(api_response, Capture.serialize_from_json(j_data) if j_data else None)

    def update_quantity_in_subscription(self, subscription_id: str, update: SubscriptionQuantityUpdateRequest) -> PaypalApiResponse[Subscription]:
        """Calls the paypal API to updates the quantity of the product or service in a subscription. 
           this method can also be used to to switch the plan and update the shipping_amount, 
           shipping_address values for the subscription. This type of update requires the buyer's consent.
        
        Arguments:
            subscription_id {str} -- the subscription id
            update {SubscriptionQuantityUpdateRequest} -- update request info.
        
        Returns:
            PaypalApiResponse[Subscription] -- Response status with subscription details
        """
        body = json.dumps(update.to_dict())
        url = parse_url(self._base_url, subscription_id, 'revise')

        api_response = self._session.post(url, body)
             
        if api_response.status_code // 100 != 2:
            return PaypalApiResponse.error(api_response)
        
        return PaypalApiResponse.success(api_response, Subscription.serialize_from_json(api_response.json()))

    def suspend_subscription(self, subscription_id: str, reason: str) -> PaypalApiResponse:
        """Calls the API to suspend a subscription
        
        Arguments:
            subscription_id {str} -- The id of the subscription to cancel
        
        Returns:
            PaypalApiResponse -- Response with the operation status
        """
        return self._execute_subscription_action(subscription_id, 'suspend', reason)

    def _execute_subscription_action(self, subscription_id: str, action_name: str, reason: str = None) -> PaypalApiResponse:
        """Executes a generic and simple subscription action call to the Paypal API
        
        Arguments:
            subscription_id {str} -- The subscription id
            action_name {str} -- API URL action name
        
        Keyword Arguments:
            reason {str} -- A comment or reason if needed (default: {None})
        
        Returns:
            PaypalApiResponse -- [description]
        """
        body = json.dumps({ 'reason': reason }) if reason else None
        url = parse_url(self._base_url, subscription_id, action_name)

        api_response = self._session.post(url, body)

        if api_response.status_code // 100 != 2:
            return PaypalApiResponse.error(api_response)
        
        return PaypalApiResponse.success(api_response)

    def list_subscription_transactions(self, subscription_id: str, start_time: datetime, end_time: datetime) -> PaypalPage[SubscriptionTransaction]:
        """Calls the API to lists transactions for a subscription.
        
        Arguments:
            subscription_id {str} -- The subscription id
            start_time {datetime} -- transaction start time
            end_time {datetime} -- transaction end time
        
        Returns:
            PaypalPage[SubscriptionTransaction] -- Paged transaction info
        """
        fmt = '%Y-%m-%dT%H:%M:%S'
        url = parse_url(self._base_url, subscription_id, 'transactions')        
        params = { end_time.strftime(fmt), start_time.strftime(fmt) }

        api_response = self._session.get(url, params)

        if api_response.status_code // 100 != 2:
            return PaypalPage.error(api_response)
        
        return PaypalPage.full_parse_success(api_response, SubscriptionTransaction, 'transaction')

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
