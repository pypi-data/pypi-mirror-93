"""
    Payment resource capture related entities
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

from pypaypal.entities.payments.commons import SellerProtection, ExchangeRate

class CaptureStatusDetailReason(Enum):
    """See https://developer.paypal.com/docs/api/payments/v2/#definition-capture_status_details
    """
    BUYER_COMPLAINT = 1
    CHARGEBACK = 2
    ECHECK = 3
    INTERNATIONAL_WITHDRAWAL = 4
    OTHER = 5
    PENDING_REVIEW = 6
    RECEIVING_PREFERENCE_MANDATES_MANUAL_ACTION = 7
    REFUNDED = 8
    TRANSACTION_APPROVED_AWAITING_FUNDING = 9
    UNILATERAL = 10
    VERIFICATION_REQUIRED = 11

class CaptureStatus(Enum):
    COMPLETED = 1
    DECLINED = 2
    PARTIALLY_REFUNDED = 3
    PENDING = 4
    REFUNDED = 5

class CaptureStatusDetail(PayPalEntity):
    """Capture status details
    """
    def __init__(self, reason: str, **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.reason  = reason

    @property
    def reason_enum(self) -> CaptureStatusDetailReason:
        try:
            return CaptureStatusDetailReason[self.reason] if self.reason else None
        except:
            return None

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        return cls(json_data.get('reason'), json_response = json_data, response_type = response_type)

    @classmethod
    def create(cls, reason: CaptureStatusDetailReason) -> 'CaptureStatusDetail':
        return cls(reason.name)

class SellerBreakdown(PayPalEntity):
    """Capture seller receivable breakdown    
    """
    def __init__(
        self, gross_amt: Money, paypal_fee: Money, net_amt: Money, 
        receivable_amt: Money, exchange_rate: ExchangeRate, 
        platform_fees: List[PlatformFee], **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.gross_amount = gross_amt
        self.paypal_fee = paypal_fee
        self.net_amount = net_amt
        self.receivable_amount = receivable_amt
        self.exchange_rate  = exchange_rate
        self.platform_fees = platform_fees

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        platform_fees = []
        gross_amount, paypal_fee, net_amount, receivable_amount, exchange_rate = None, None, None, None, None

        if 'gross_amount' in json_data.keys():
            gross_amount = Money.serialize_from_json(json_data['gross_amount'], response_type)
        if 'paypal_fee' in json_data.keys():
            paypal_fee = Money.serialize_from_json(json_data['paypal_fee'], response_type)
        if 'net_amount' in json_data.keys():
            net_amount = Money.serialize_from_json(json_data['net_amount'], response_type)
        if 'receivable_amount' in json_data.keys():
            receivable_amount = Money.serialize_from_json(json_data['receivable_amount'], response_type)
        
        if 'platform_fees' in json_data.keys():
            platform_fees = [PlatformFee.serialize_from_json(x, response_type) for x in json_data['platform_fees']]
        
        return cls(
            gross_amount, paypal_fee, net_amount, receivable_amount, 
            exchange_rate, platform_fees, json_response = json_data, 
            response_type = response_type
        )

class Capture(PayPalEntity):
    """Payment capture obj representation.
    """
    def __init__(
        self, cap_id: str, status: str, final_capture: bool, 
        disbursement_mode: str, invoice_id: str, custom_id: str,
        amount: Money, seller_protection: SellerProtection,
        status_details: CaptureStatusDetail , seller_breakdown: SellerBreakdown, **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.id = cap_id
        self.status = status
        self.final_capture  = final_capture
        self.disbursement_mode = disbursement_mode
        self.invoice_id = invoice_id
        self.custom_id = custom_id
        self.amount = amount
        self.seller_protection = seller_protection
        self.status_details = status_details
        self.seller_receivable_breakdown = seller_breakdown
        self._create_time = self._json_response.get('create_time', kwargs.get('create_time'))
        self._update_time = self._json_response.get('update_time', kwargs.get('update_time'))
        self.links = [ActionLink(x['href'], x['rel'], x.get('method', 'GET')) for x in self._json_response.get('links', [])]
    
    @property
    def status_enum(self) -> CaptureStatus:
        try:
            return CaptureStatus[self.status] if self.status else None
        except:
            return None

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
    def Status_enum(self) -> CaptureStatusDetailReason:
        try:
            return CaptureStatusDetailReason[self.status] if self.status else None
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
    def up_link(self) -> ActionLink:
        """Retrieves a link to read this entity authorization details.
        
        Returns:
            ActionLink -- The link for requesting the information to the API.
        """
        return next(filter(lambda x: x.rel == 'up', self.links), None)
    
    @property
    def refund_link(self) -> ActionLink:
        """Retrieves a link to refund this capture.
        
        Returns:
            ActionLink -- The link for requesting the information to the API.
        """
        return next(filter(lambda x: x.rel == 'refund', self.links), None)

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        amount, seller_protection, status_detail, seller_receivable_breakdown = None, None, None, None
        
        if 'amount' in json_data.keys():
            amount = cls.serialize_from_json(json_data['amount'], response_type)
        if 'seller_protection' in json_data.keys():
            seller_protection = cls.serialize_from_json(json_data['seller_protection'], response_type)
        if 'status_details' in json_data.keys():
            status_detail = cls.serialize_from_json(json_data['status_details'], response_type)
        if 'seller_receivable_breakdown' in json_data.keys():
            seller_receivable_breakdown = cls.serialize_from_json(json_data['seller_receivable_breakdown'], response_type)

        return cls(
            json_data.get('id'), json_data.get('status'), json_data.get('final_capture'), 
            json_data.get('disbursement_mode'), json_data.get('invoice_id'), json_data.get('custom_id'), 
            amount, seller_protection, status_detail, seller_receivable_breakdown, json_response = json_data,
            response_type = response_type
        )