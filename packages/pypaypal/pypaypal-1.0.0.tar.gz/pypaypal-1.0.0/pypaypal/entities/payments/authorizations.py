"""
    Payment authorizations resource related entities
"""

from enum import Enum
from datetime import datetime
from typing import Type, List

import dateutil.parser

from pypaypal.entities.base import (
    T,
    Money,
    ActionLink,
    PlatformFee,
    ResponseType,    
    PayPalEntity
)

from pypaypal.entities.payments.commons import SellerProtection

class StatusDetailReason(Enum):
    PENDING_REVIEW = 1 # Authorization is pending manual review

class AuthorizationStatus(Enum):
    CREATED = 1
    CAPTURED = 2
    DENIED = 3
    EXPIRED = 4
    PARTIALLY_CAPTURED = 5
    VOIDED = 6
    PENDING = 7

class AuthStatusDetail(PayPalEntity):
    """Authorization status details
    """
    def __init__(self, reason: str, **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.reason  = reason

    @property
    def reason_enum(self) -> StatusDetailReason:
        try:
            return StatusDetailReason[self.reason] if self.reason else None
        except:
            return None

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        return cls(json_data.get('reason'), json_response = json_data, response_type = response_type)

    @classmethod
    def create(cls, reason: StatusDetailReason = StatusDetailReason.PENDING_REVIEW) -> 'AuthStatusDetail':
        return cls(reason.name)

class Authorization(PayPalEntity):
    """Payment authorizatio obj representation
    """

    def __init__(
        self, auth_id: str, status: str, amount: Money, status_details: AuthStatusDetail,
        invoice_id: str, custom_id: str, seller_protection: SellerProtection, **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.id = auth_id
        self.status = status
        self.amount = amount
        self.status_details = status_details
        self.invoice_id = invoice_id
        self.custom_id = custom_id
        self.seller_protection = seller_protection
        self._create_time = self._json_response.get('create_time', kwargs.get('create_time'))
        self._update_time = self._json_response.get('update_time', kwargs.get('update_time'))
        self._expiration_time = self._json_response.get('expiration_time', kwargs.get('expiration_time'))
        self.links = [ActionLink(x['href'], x['rel'], x.get('method', 'GET')) for x in self._json_response.get('links', [])]
   
    @property
    def create_time(self) -> datetime:
        try:
            return dateutil.parser.parse(self._create_time) if self._create_time else None
        except:
            return None

    @property
    def update_time(self) -> datetime:
        try:
            return dateutil.parser.parse(self._update_time) if self._update_time else None
        except:
            return None

    @property
    def expiration_time(self) -> datetime:
        try:
            return dateutil.parser.parse(self._expiration_time) if self._expiration_time else None
        except:
            return None

    @property
    def Status_enum(self) -> AuthorizationStatus:
        try:
            return AuthorizationStatus[self.status] if self.status else None
        except:
            return None

    @property
    def read_link(self) -> ActionLink:
        """Retrieves a link to read this entity details.
        
        Returns:
            ActionLink -- The link for requesting the information to the API.
        """
        return next(filter(lambda x: x.rel == 'self', self.links), None)

    @property
    def capture_link(self) -> ActionLink:
        """Retrieves a link to perform a capture on this authorized payment.
        
        Returns:
            ActionLink -- The link for requesting the information to the API.
        """
        return next(filter(lambda x: x.rel == 'capture', self.links), None)

    @property
    def void_link(self) -> ActionLink:
        """Retrieves a link to void this authorization
        
        Returns:
            ActionLink -- The link for requesting the information to the API.
        """
        return next(filter(lambda x: x.rel == 'void', self.links), None)

    @property
    def reauthorize_link(self) -> ActionLink:
        """Retrieves a link to reauthorize this payment.
        
        Returns:
            ActionLink -- The link for requesting the information to the API.
        """
        return next(filter(lambda x: x.rel == 'reauthorize', self.links), None)

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        amount, seller_protection, status_details = None, None, None
    
        if 'amount' in json_data.keys():
            amount = Money.serialize_from_json(json_data['amount'], response_type)
        if 'seller_protection' in json_data.keys():
            seller_protection = SellerProtection.serialize_from_json(json_data['seller_protection'], response_type)
        if 'status_details' in json_data.keys():
            status_details = AuthStatusDetail.serialize_from_json(json_data['status_details'], response_type)

        return cls(
            json_data.get('id'), json_data.get('status'), 
            amount, status_details, json_data.get('invoice_id'), json_data.get('custom_id'),
            seller_protection, json_response = json_data, response_type = response_type
        )
