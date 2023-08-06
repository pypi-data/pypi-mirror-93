"""
    Paypal Webhook resource client for the paypal resource group.

    Resource docs & Reference: https://developer.paypal.com/docs/api/webhooks/v1/
"""

import json

from datetime import datetime
from typing import TypeVar, Set, List

from pypaypal.clients.base import ClientBase, ActionLink

from pypaypal.http import ( 
    parse_url,
    PayPalSession,
    LEGACY_LIVE_API_BASE_URL, 
    LEGACY_SANDBOX_API_BASE_URL 
)

from pypaypal.entities.base import ( 
    DateRange,
    PaypalPage,
    ResponseType,
    PaypalApiResponse,
    PatchUpdateRequest,
    PaypalApiBulkResponse
)

from pypaypal.entities.webhooks import (
    Webhook,
    EventType,
    AnchorType,
    WebhookEvent,
    WebhookSignature,
    SignatureVerificationStatus
)

"""
    Base Resource Live URL
"""
_LIVE_RESOURCE_BASE_URL = parse_url(LEGACY_LIVE_API_BASE_URL, 'notifications', 'webhooks')

"""
    Base Resource Sandbox URL
"""
_SANDBOX_RESOURCE_BASE_URL = parse_url(LEGACY_SANDBOX_API_BASE_URL, 'notifications', 'webhooks')

# Webhook client
W = TypeVar('W', bound = 'WebHookClient')

# Webhook signature verification client
V = TypeVar('S', bound = 'VerifySignatureClient')

# Webhook event type client
T = TypeVar('T', bound = 'EventTypeClient')

# Webhook events client
E = TypeVar('E', bound = 'EventClient')

# Webhook evebt simulation client
S = TypeVar('S', bound = 'EventSimulationClient')

class ApiCallError(Exception):
    """Exception for methods that don't return a PaypalEntity
    """
    def __init__(self, error: PaypalApiResponse):
        super().__init__(json.dumps(ApiCallError._parse_error(error)))
        self.error_info = error
    
    @staticmethod
    def _parse_error(error: PaypalApiResponse) -> dict:
        return error.error_detail.as_json_dict() if error.error_detail else {'message': 'unknown error'}

class WebHookClient(ClientBase):
    """WebHook resource client
    """
    def __init__(self, base_url: str, session: PayPalSession):
        super().__init__(base_url, session)

    def _process_simple_response(self, api_response) -> PaypalApiResponse[Webhook]:
        """Process a simple webhook response
        
        Arguments:
            api_response {[type]} -- The http response obj from the request lib
        
        Returns:
            PaypalApiResponse[Webhook] -- Paypal response status with webhook object.
        """
        if api_response.status_code//100 != 2:
            return PaypalApiResponse.error(api_response)

        return PaypalApiResponse.success(api_response, Webhook.serialize_from_json(api_response.json()))

    
    def create_webhook(self, url: str, event_types: List[EventType], subscribe_all: bool = False) -> PaypalApiResponse[Webhook]:
        """Calls the paypal API to create a webhook
        
        Arguments:
            url {str} --  Internet accessible URL configured to listen incoming POST notification messages with event info.
            event_types {List[EventType]} -- An array of events to which to subscribe your webhook.
        
        Returns:
            PaypalApiResponse[Webhook] -- Paypal response status with webhook object.
        """
        body = json.dumps({
            'url': url, 
            'event_types': [x.to_dict() for x in event_types] if not subscribe_all else '*'
        })
        
        return self._process_simple_response(self._session.post(self._base_url, body))


    def list_webhooks(self, anchor_type: AnchorType = AnchorType.APPLICATION) -> PaypalApiBulkResponse[Webhook]:
        """Calls the paypal api to list an app webhooks
        
        Arguments:
            anchor_type {AnchorType} -- AnchorType filter
        
        Returns:
            PaypalApiBulkResponse[Webhook] -- Paypal response status with webhook objects.
        """
        api_response = self._session.get(self._base_url, params = {'anchor_type': anchor_type.name})

        if api_response.status_code//100 != 2:
            return PaypalApiBulkResponse.error(api_response)

        return PaypalApiBulkResponse.success(
            api_response, 
            [ Webhook.serialize_from_json(x) for x in api_response.json().get('webhooks', []) ]
        )
    
    def delete_webhook(self, webhook_id: str) -> PaypalApiResponse:
        """Calls the paypal API to delete a webhook by id.
        
        Arguments:
            webhook_id {str} -- Id of the Webhook to be deleted. 
        
        Returns:
            PaypalApiResponse -- Paypal response status
        """
        api_response = self._session.delete(parse_url(self._base_url, webhook_id))
        return PaypalApiResponse.error(api_response) if api_response.status_code//100 != 2 else PaypalApiResponse.success(api_response)

    def update_webhook(self, webhook_id: str, patch_request: List[PatchUpdateRequest]) -> PaypalApiResponse[Webhook]:
        """Calls the paypal API to replace webhook fields with new values
        
        Arguments:
            webhook_id {str} -- Id of the webhook to be updated
            patch_request {List[PatchUpdateRequest]} -- patch request list with updates
        
        Returns:
            PaypalApiResponse[Webhook] -- Paypal response status with webhook object. 
        """
        body = json.dumps({'patch_request': [ x.to_dict() for x in patch_request ]})
        return self._process_simple_response(self._session.patch(parse_url(self._base_url, webhook_id), body))

    def show_webhook_details(self, webhook_id: str) -> PaypalApiResponse[Webhook]:
        """Calls the paypal API to show a webhook details
        
        Arguments:
            webhook_id {str} -- Webhook id
        
        Returns:
            PaypalApiResponse[Webhook] -- Response status with webhook object.
        """
        return self._process_simple_response(self._session.get(parse_url(self._base_url, webhook_id)))

    def list_event_subscriptions_for_webhook(self, webhook_id: str) -> PaypalApiBulkResponse[EventType]:
        """Calls the paypal API to list the event subscription for a Webhook
        
        Arguments:
            webhook_id {str} -- Webhook id
        
        Returns:
            PaypalApiBulkResponse[EventType] -- Paypal response status with event type list. 
        """
        api_response = self._session.get(parse_url(self._base_url, webhook_id, 'event-types'))

        if api_response.status_code//100 != 2:
            return PaypalApiBulkResponse.error(api_response)

        return PaypalApiBulkResponse.success(
            api_response, 
            [ EventType.serialize_from_json(x) for x in api_response.json().get('event_types', []) ]
        )

    @classmethod
    def for_session(cls: T, session: PayPalSession) -> W:
        """Creates a client from a given paypal session
        
        Arguments:
            cls {T} -- class reference
            session {PayPalSession} -- the paypal session
        
        Returns:
            T -- an instance of Dispute client with the right configuration by session mode
        """
        base_url = _LIVE_RESOURCE_BASE_URL if session.session_mode.is_live() else _SANDBOX_RESOURCE_BASE_URL
        return cls(parse_url(base_url, 'webhooks'), session)

class VerifySignatureClient(ClientBase):
    """Verify WebHook Signatire resource client
    """
    def __init__(self, base_url: str, session: PayPalSession):
        super().__init__(base_url, session)

    def verify_webhook_signature(self, signature: WebhookSignature) -> SignatureVerificationStatus:
        """Calls the paypal API to verify a webhook signature (it usually comes in the headers).
        
        Arguments:
            signature {WebhookSignature} -- The signature
        
        Returns:
            SignatureVerificationStatus -- Verification status
        
        Raises:
            ApiCallError -- If there's an error calling the API.
        """        
        api_response = self._session.post(self._base_url, json.dumps(signature.to_dict()))

        if api_response.status_code//100 != 2:
            raise ApiCallError(PaypalApiResponse.error(api_response))

        return SignatureVerificationStatus[api_response.json().get('verification_status')]

    @classmethod
    def for_session(cls: T, session: PayPalSession) -> V:
        """Creates a client from a given paypal session
        
        Arguments:
            cls {T} -- class reference
            session {PayPalSession} -- the paypal session
        
        Returns:
            T -- an instance of Dispute client with the right configuration by session mode
        """
        base_url = _LIVE_RESOURCE_BASE_URL if session.session_mode.is_live() else _SANDBOX_RESOURCE_BASE_URL
        return cls(parse_url(base_url, 'verify-webhook-signature'), session)
    
class EventTypeClient(ClientBase):
    """Verify WebHook Signatire resource client
    """
    def __init__(self, base_url: str, session: PayPalSession):
        super().__init__(base_url, session)

    def list_available_events(self) -> PaypalApiBulkResponse[EventType]:
        """Calls the paypal API to get a list of available events to which any webhook can subscribe.
        
        Returns:
            PaypalApiBulkResponse[EventType] -- Paypal response status with the event type list.
        """
        api_response = self._session.get(self._base_url)

        if api_response.status_code//100 != 2:
            return PaypalApiBulkResponse.error(api_response)

        return PaypalApiBulkResponse.success(
            api_response, 
            [ EventType.serialize_from_json(x) for x in api_response.json().get('event_types', []) ]
        )

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
        return cls(parse_url(base_url, 'webhooks-event-types'), session)
    
class EventClient(ClientBase):
    """Verify WebHook Signatire resource client
    """
    def __init__(self, base_url: str, session: PayPalSession):
        super().__init__(base_url, session)

    def list_event_notifications(
            self, page_size: int = 10, transaction_id: str = None, 
            event_type: str = None, date: DateRange = None
        ) -> PaypalPage[WebhookEvent]:
        params = { 'page_size': 10 }

        if transaction_id != None: 
            params['transaction_id'] = transaction_id
        if event_type != None: 
            params['event_type'] = event_type
        if date != None and date.start_time != None: 
            params['start_time'] = datetime.strftime(date.start, '%Y-%m-%dT%H:%M:%S') 
        if date != None and date.end_time != None:
            params['end_time'] = datetime.strftime(date.end, '%Y-%m-%dT%H:%M:%S')
        
        api_response = self._session.get(self._base_url, params = params)

        if api_response.status_code // 100 != 2:
            return PaypalPage.error(api_response)
        
        return PaypalPage.full_parse_success(api_response, WebhookEvent, 'events')

    def show_event_notification_details(self, event_id: str) -> PaypalApiResponse[WebhookEvent]:
        """Calls the API to get the details for a webhook event notification.
        
        Arguments:
            event_id {str} -- The webhook notification event id
        
        Returns:
            PaypalApiResponse[WebhookEvent] -- Paypal response status with event obj.
        """
        api_response = self._session.get(parse_url(self._base_url, event_id))

        if api_response.status_code // 100 != 2:
            return PaypalApiResponse.error(api_response)
        
        return PaypalApiResponse.success(api_response, WebhookEvent.serialize_from_json(api_response.json()))

    def resend_event_notification(self, event_id: str, webhooks_ids: List[str] = []) -> PaypalApiResponse[WebhookEvent]:
        """Calls the paypal API to resend notification events
        
        Arguments:
            event_id {str} -- The webhook event id
        
        Keyword Arguments:
            webhooks_ids {List[str]} -- webhooks notification to resend (all pending if empty) (default: {[]})
        
        Returns:
            PaypalApiResponse[WebhookEvent] -- A response with the webhooks events.
        """
        body = { 'webhook_ids': webhooks_ids or [] }
        api_response = self._session.post(parse_url(self._base_url, event_id), json.dumps(body))

        if api_response.status_code // 100 != 2:
            return PaypalApiResponse.error(api_response)
        
        return PaypalApiResponse.success(api_response, WebhookEvent.serialize_from_json(api_response.json()))

    @classmethod
    def for_session(cls: T, session: PayPalSession) -> E:
        """Creates a client from a given paypal session
        
        Arguments:
            cls {T} -- class reference
            session {PayPalSession} -- the paypal session
        
        Returns:
            T -- an instance of Dispute client with the right configuration by session mode
        """
        base_url = _LIVE_RESOURCE_BASE_URL if session.session_mode.is_live() else _SANDBOX_RESOURCE_BASE_URL
        return cls(parse_url(base_url, 'webhooks-events'), session)

class SimulateEventClient(ClientBase):
    """Verify WebHook Signatire resource client
    """
    def __init__(self, base_url: str, session: PayPalSession):
        super().__init__(base_url, session)

    def simulate_webhook_event(self, webhook_id: str, url: str, event_type: str, resource_version: str) -> PaypalApiResponse[WebhookEvent]:
        """Calls the paypal API to send a webhook simulation
        
        Arguments:
            webhook_id {str} -- Webhook id, if ommited url is required
            url {str} -- endpoint url, if ommited id is required 
            event_type {str} -- The event name, one per request
            resource_version {str} -- event type version
        
        Returns:
            PaypalApiResponse[WebhookEvent] -- A response with the webhooks events.
        """
        body = { 'event_type': event_type }
        
        if body['url'] != None: 
            body['url'] = url
        if body['webhook_id'] != None: 
            body['webhooks_id'] = webhook_id
        if body['resource_version'] != None: 
            body['resource_version'] = resource_version

        api_response = self._session.post(self._base_url, json.dumps(body))

        if api_response.status_code // 100 != 2:
            return PaypalApiResponse.error(api_response)
        
        return PaypalApiResponse.success(api_response, WebhookEvent.serialize_from_json(api_response.json()))


    @classmethod
    def for_session(cls: T, session: PayPalSession) -> E:
        """Creates a client from a given paypal session
        
        Arguments:
            cls {T} -- class reference
            session {PayPalSession} -- the paypal session
        
        Returns:
            T -- an instance of Dispute client with the right configuration by session mode
        """
        base_url = _LIVE_RESOURCE_BASE_URL if session.session_mode.is_live() else _SANDBOX_RESOURCE_BASE_URL
        return cls(parse_url(base_url, 'simulate-event'), session)
