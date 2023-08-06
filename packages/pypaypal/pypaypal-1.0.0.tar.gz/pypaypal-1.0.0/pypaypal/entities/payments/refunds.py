"""
    Payment resource refunds related entities
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

class RefundStatusDetailReason(Enum):
    ECHECK = 1

class RefundStatus(Enum):
    PENDING = 1
    COMPLETED = 2
    CANCELED = 3

class RefundStatusDetail(PayPalEntity):
    """Refund status details
    """
    def __init__(self, reason: str, **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.reason  = reason

    @property
    def reason_enum(self) -> RefundStatusDetailReason:
        try:
            return RefundStatusDetailReason[self.reason] if self.reason else None
        except:
            return None

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        return cls(json_data.get('reason'), json_response = json_data, response_type = response_type)

    @classmethod
    def create(cls, reason: RefundStatusDetailReason = RefundStatusDetailReason.ECHECK) -> 'RefundStatusDetail':
        return cls(reason.name)

class RefundNetAmtBreakdown(PayPalEntity):
    """net_amount_breakdown obj representation
    """
    def __init__(self, payable_amt: Money, converted_amt: Money, exchange_rate: ExchangeRate, **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.payable_amount = payable_amt
        self.converted_amount = converted_amt
        self.exchange_rate = exchange_rate

    @classmethod    
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        payable_amount, converted_amount, exchange_rate = None, None, None

        if 'payable_amount' in json_data.keys():
            payable_amount = Money.serialize_from_json(json_data['payable_amount', response_type])
        if 'converted_amount' in json_data.keys():
            converted_amount = Money.serialize_from_json(json_data['converted_amount', response_type])
        if 'exchange_rate' in json_data.keys():
            exchange_rate = ExchangeRate.serialize_from_json(json_data['exchange_rate', response_type])
        
        return cls(
            payable_amount, converted_amount, exchange_rate, 
            json_response = json_data, response_type = response_type
        )

class SellerRefundBreakdown(PayPalEntity):
    """Capture seller receivable breakdown    
    """
    def __init__(
        self, gross_amt: Money, paypal_fee: Money, net_amt: Money, 
        total_refunded_amount: Money, net_amt_breakdown: RefundNetAmtBreakdown, 
        platform_fees: List[PlatformFee], **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.gross_amount = gross_amt
        self.paypal_fee = paypal_fee
        self.net_amount = net_amt
        self.total_refunded_amount = total_refunded_amount
        self.net_amount_breakdown = net_amt_breakdown
        self.platform_fees = platform_fees

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        platform_fees, net_amount_breakdown = [], None
        gross_amount, paypal_fee, net_amount, total_refunded_amount = None, None, None, None

        if 'gross_amount' in json_data.keys():
            gross_amount = Money.serialize_from_json(json_data['gross_amount'], response_type)
        if 'paypal_fee' in json_data.keys():
            paypal_fee = Money.serialize_from_json(json_data['paypal_fee'], response_type)
        if 'net_amount' in json_data.keys():
            net_amount = Money.serialize_from_json(json_data['net_amount'], response_type)
        if 'total_refunded_amount' in json_data.keys():
            total_refunded_amount = Money.serialize_from_json(json_data['total_refunded_amount'], response_type)
        if 'net_amount_breakdown' in json_data.keys():
            net_amount_breakdown = RefundNetAmtBreakdown.serialize_from_json(json_data['net_amount_breakdown'], response_type)

        if 'platform_fees' in json_data.keys():
            platform_fees = [PlatformFee.serialize_from_json(x, response_type) for x in json_data['platform_fees']]
        
        return cls(
            gross_amount, paypal_fee, net_amount, total_refunded_amount, 
            net_amount_breakdown, platform_fees, json_response = json_data, 
            response_type = response_type
        )

class Refund(PayPalEntity):
    """Refund obj representation.
    """

    def __init__(
        self, refund_id: str, status: str,
        invoice_id: str, amount: Money, note_to_payer: str, 
        status_details: RefundStatusDetail, seller_breakdown: SellerRefundBreakdown, **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))    
        self.id = refund_id
        self.status = status
        self.invoice_id = invoice_id
        self.amount = amount
        self.note_to_payer = note_to_payer
        self.status_details = status_details
        self.seller_breakdown = seller_breakdown
        self._create_time = self._json_response.get('create_time', kwargs.get('create_time'))
        self._update_time = self._json_response.get('update_time', kwargs.get('update_time'))
        self.links = [ActionLink(x['href'], x['rel'], x.get('method', 'GET')) for x in self._json_response.get('links', [])]

    @property
    def status_enum(self) -> RefundStatus:
        try:
            return RefundStatus[self.status] if self.status else None
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
    def Status_enum(self) -> RefundStatusDetailReason:
        try:
            return RefundStatusDetailReason[self.status] if self.status else None
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
        """Retrieves a link to read this entity capture details.
        
        Returns:
            ActionLink -- The link for requesting the information to the API.
        """
        return next(filter(lambda x: x.rel == 'up', self.links), None)

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        amount, status_details, seller_breakdown = None, None, None
        
        if 'amount' in json_data.keys():
            amount = Money.serialize_from_json(json_data['amount'], response_type)
        if 'status_details' in json_data.keys():
            status_details = RefundStatusDetail.serialize_from_json(json_data['status_details'], response_type)
        if 'seller_breakdown' in json_data.keys():
            seller_breakdown = SellerRefundBreakdown.serialize_from_json(json_data['seller_breakdown'], response_type)

        return cls(
            json_data.get('id'), json_data.get('status'), json_data.get('invoice_id'), 
            amount, json_data.get('note_to_payer'), status_details, seller_breakdown,
            json_response = json_data, response_type = response_type
        )
