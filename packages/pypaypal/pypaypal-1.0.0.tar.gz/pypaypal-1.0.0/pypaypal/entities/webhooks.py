"""
    Module for Webhook related entities.
"""

from enum import Enum
from datetime import datetime
from typing import Type, List

import dateutil.parser

from pypaypal.entities.base import (
    T,
    ActionLink,
    ResponseType,    
    PayPalEntity
)

class AnchorType(Enum):
    """Webhook anchor type for filtering
    """
    ACCOUNT = 1
    APPLICATION = 2

class SignatureVerificationStatus(Enum):
    SUCCESS = 1
    FAILURE = 2

class ResourceVersion(PayPalEntity):
    """Resource version object representation
    """

    def __init__(self, resource_version: str, **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.resource_version = resource_version
    
    @classmethod
    def create(cls, resource_version: str) -> 'ResourceVersion':
        return cls(resource_version)

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        return cls(**json_data, json_response = json_data, response_type = response_type)

class EventType(PayPalEntity):
    """Event type obj representation
    """

    _ARRAY_TYPES = { 'resource_version': ResourceVersion }

    def __init__(
            self, name: str = None, description: str = None, status: str = None, 
            resource_version: List[ResourceVersion] = [], **kwargs
        ):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.name = name
        self.description = description
        self.status = status
        self.resource_version = resource_version or []
    
    @classmethod
    def create(cls, name: str, description: str, status: str, resource_version: List[ResourceVersion]) -> 'EventType':
        return cls(name, description, status, resource_version)

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        args = super()._build_args(json_data, entity_types = dict(), array_types = cls._ARRAY_TYPES)
        return cls(**args, json_response = json_data, response_type = response_type)

class Webhook(PayPalEntity):
    """Webhook obj representation
    """

    _ARRAY_TYPES = { 'event_types': EventType }

    def __init__(self, webhook_id: str = None, url: str = None, event_types: List[EventType] = [], **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.url = url
        self.webhook_id = webhook_id
        self.event_types = event_types or []
        self.links = [ActionLink(x['href'], x['rel'], x.get('method', 'GET')) for x in self._json_response.get('links', [])]

    def to_dict(self) -> dict:
        ret = super().to_dict()
        if ret['webhook_id']:
            ret['id'] = ret.pop('webhook_id')
        return ret

    @classmethod
    def create(cls, url: str, event_types: List[EventType]) -> 'Webhook':
        return cls(None, url, event_types)

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        args = super()._build_args(json_data, entity_types = dict(), array_types = cls._ARRAY_TYPES)
        return cls(**args, json_response = json_data, response_type = response_type)
    
class ResourceAmountDetails(PayPalEntity):
    """Resource Details obj representation
    """

    def __init__(self, subtotal: str, **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.subtotal = subtotal
    
    @classmethod
    def create(cls, subtotal: str) -> 'ResourceAmountDetails':
        return cls(subtotal)

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:        
        return cls(**json_data, json_response = json_data, response_type = response_type)

class ResourceAmount(PayPalEntity):
    """Resource amount obj representation
    """

    _ENTITY_TYPES = { 'details': ResourceAmountDetails }

    def __init__(self, total: str = None, currency: str = None, details: ResourceAmountDetails = None, **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.total = total
        self.details = details
        self.currency = currency
    
    @classmethod
    def create(cls, total: str, currency: str, details: ResourceAmountDetails) -> 'ResourceAmount':
        return cls(total, currency, details)

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:        
        args = super()._build_args(json_data, cls._ENTITY_TYPES)
        return cls(**args, json_response = json_data, response_type = response_type)

class Resource(PayPalEntity):
    """Resource obj representation
    """
    
    _ENTITY_TYPES = { 'amount': ResourceAmount }

    def __init__(self, resource_id: str = None, state: str = None, amount: ResourceAmount = None, **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.state = state
        self.amount = amount
        self.resource_id = resource_id
        self._update_time = self._json_response.get('update_time', kwargs.get('update_time'))
        self._create_time = self._json_response.get('create_time', kwargs.get('create_time'))
        self.links = [ActionLink(x['href'], x['rel'], x.get('method', 'GET')) for x in self._json_response.get('links', [])]

    def to_dict(self) -> dict:
        ret = super().to_dict()
        if ret['resource_id']:
            ret['id'] = ret.pop('resource_id')
        return ret

    @property
    def update_time(self) -> datetime:
        try:
            return dateutil.parser.parse(self._update_time) if self._update_time else None
        except:
            return None

    @property
    def create_time(self) -> datetime:
        try:
            return dateutil.parser.parse(self._create_time) if self._create_time else None
        except:
            return None

    @classmethod
    def create(cls, resource_id: str, state: str, amount: ResourceAmount) -> 'Resource':
        return cls(resource_id, state, amount)

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        args = super()._build_args(json_data, cls._ENTITY_TYPES)
        return cls(**args, json_response = json_data, response_type = response_type)

class WebhookEvent(PayPalEntity):
    """WebhookEvent obj representation
    """
    
    _ENTITY_TYPES = { 'resource': Resource }

    def __init__(
            self, event_id: str = None, resource_type: str = None, 
            event_version: str = None, event_type: str = None, summary: str = None, 
            resource_version: str = None, resource: Resource = None, **kwargs
        ):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.summary = summary
        self.event_id = event_id
        self.resource = resource
        self.event_type = event_type
        self.resource_type = resource_type
        self.event_version = event_version
        self.resource_version = resource_version
        self._create_time = self._json_response.get('create_time', kwargs.get('create_time'))
        self.links = [ActionLink(x['href'], x['rel'], x.get('method', 'GET')) for x in self._json_response.get('links', [])]

    def to_dict(self) -> dict:
        ret = super().to_dict()
        if ret['event_id']:
            ret['id'] = ret.pop('event_id')
        return ret

    @property
    def create_time(self) -> datetime:
        try:
            return dateutil.parser.parse(self._create_time) if self._create_time else None
        except:
            return None

    @classmethod
    def create(cls, event_id: str = None, resource_type: str = None,
            event_version: str = None, event_type: str = None, summary: str = None,
            resource_version: str = None, resource: Resource = None) -> 'WebhookEvent':
        return cls(
            summary = summary, event_id = event_id, event_type = event_type,
            resource_type = resource_type, event_version = event_version,
            resource = resource, resource_version = resource_version
        )

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        args = super()._build_args(json_data, cls._ENTITY_TYPES)
        return cls(**args, json_response = json_data, response_type = response_type)

class WebhookSignature(PayPalEntity):
    """Webhook cert Signature obj representation
    """

    _ENTITY_TYPES = { 'webhook_event': WebhookEvent }

    def __init__(
            self, auth_algo: str = None, cert_url: str = None, 
            transmission_id: str = None, transmission_sig: str = None, 
            transmission_time: str = None, webhook_id: str = None, 
            webhook_event: WebhookEvent = None, **kwargs
        ):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.cert_url = cert_url
        self.auth_algo = auth_algo
        self.webhook_id = webhook_id
        self.webhook_event = webhook_event
        self.transmission_id = transmission_id
        self.transmission_sig = transmission_sig
        self.transmission_time = transmission_time
    
    @classmethod
    def create(
            cls, auth_algo: str, cert_url: str, transmission_id: str, 
            transmission_sig: str, transmission_time: str, webhook_id: str, 
            webhook_event: WebhookEvent
        ) -> 'WebhookSignature':
        return cls(
                auth_algo = auth_algo, cert_url = cert_url, 
                transmission_id = transmission_id, transmission_sig = transmission_sig, 
                transmission_time = transmission_time, webhook_id = webhook_id, 
                webhook_event = webhook_event 
            )

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        args = super()._build_args(json_data, cls._ENTITY_TYPES)
        return cls(**args, json_response = json_data, response_type = response_type)


