"""
    Module with dispute related entities
"""

from enum import Enum
from datetime import datetime
from typing import Type, List

import dateutil.parser

from pypaypal.entities.base import (
    T, 
    Money, 
    ActionLink, 
    PayPalEntity, 
    ResponseType, 
    PaypalMessage, 
    PaypalMerchant, 
    PatchUpdateRequest 
)

class DisputeState(Enum):
    """Enumeration of dispute states
    """
    # Filters the disputes in the response to those with the REQUIRED_ACTION dispute state.
    REQUIRED_ACTION =  1
    # Filters the disputes in the response to those with the REQUIRED_OTHER_PARTY_ACTION dispute state.
    REQUIRED_OTHER_PARTY_ACTION =  2
    # Filters the disputes in the response to those with the UNDER_PAYPAL_REVIEW dispute state.
    UNDER_PAYPAL_REVIEW = 3 
    # Filters the disputes in the response to those with the RESOLVED dispute state.
    RESOLVED = 4
    # Filters the disputes in the response to those with the OPEN_INQUIRIES dispute state.
    OPEN_INQUIRIES = 5
    # Filters the disputes in the response to those with the APPEALABLE dispute state.
    APPEALABLE = 6

class DisputeStatus(Enum):
    """Enumeration for the possible dispute status
    """
    # The dispute is open.
    OPEN = 1
    # The dispute is waiting for a response from the customer.
    WAITING_FOR_BUYER_RESPONSE = 2
    # The dispute is waiting for a response from the merchant.
    WAITING_FOR_SELLER_RESPONSE = 3
    # The dispute is under review with PayPal.
    UNDER_REVIEW = 4
    # The dispute is resolved.
    RESOLVED = 5
    # The default status if the dispute does not have one of the other statuses.
    OTHER = 6

class DisputeReason(Enum):
    """Enumeration with known dispute reasons
    """
    # The customer did not receive the merchandise or service.
    MERCHANDISE_OR_SERVICE_NOT_RECEIVED = 1
    # The customer reports that the merchandise or service is not as described.
    MERCHANDISE_OR_SERVICE_NOT_AS_DESCRIBED = 2
    # The customer did not authorize purchase of the merchandise or service.
    UNAUTHORISED = 3
    # The refund or credit was not processed for the customer.
    CREDIT_NOT_PROCESSED = 4
    # The transaction was a duplicate.
    DUPLICATE_TRANSACTION = 5
    # The customer was charged an incorrect amount.
    INCORRECT_AMOUNT = 6
    # The customer paid for the transaction through other means.
    PAYMENT_BY_OTHER_MEANS = 7
    # The customer was being charged for a subscription or a recurring transaction that was canceled.
    CANCELED_RECURRING_BILLING = 8
    # A problem occurred with the remittance.
    PROBLEM_WITH_REMITTANCE = 9
    # Other.
    OTHER = 10

class DisputeChannel(Enum):
    """Enumeration with known dispute channels
    """
    # The customer contacts PayPal to file a dispute with the merchant.
    INTERNAL = 1
    # The customer contacts their card issuer or bank to request a refund.
    EXTERNAL = 2

class DisputeLifeCycleStage(Enum):
    """Enumeration with known dispute life cycle stages
    """
    # A customer and merchant interact in an attempt to resolve a dispute without escalation to PayPal. Occurs when the customer:
    #     Has not received goods or a service.
    #     Reports that the received goods or service are not as described.
    #     Needs more details, such as a copy of the transaction or a receipt.
    INQUIRY = 1
    # A customer or merchant escalates an inquiry to a claim, which authorizes PayPal to investigate the case and make a determination. Occurs only when the dispute channel is INTERNAL. This stage is a PayPal dispute lifecycle stage and not a credit card or debit card chargeback. All notes that the customer sends in this stage are visible to PayPal agents only. The customer must wait for PayPal’s response before the customer can take further action. In this stage, PayPal shares dispute details with the merchant, who can complete one of these actions:
    #         Accept the claim.
    #         Submit evidence to challenge the claim.
    #         Make an offer to the customer to resolve the claim.
    CHARGEBACK = 2
    # The first appeal stage for merchants. A merchant can appeal a chargeback if PayPal's decision is not in the merchant's favor.
    # If the merchant does not appeal within the appeal period, PayPal considers the case resolved.
    PRE_ARBITRATION = 3
    # The second appeal stage for merchants. A merchant can appeal a dispute for a second time if the first appeal was denied. 
    # If the merchant does not appeal within the appeal period, the case returns to a resolved status in pre-arbitration stage.
    ARBITRATION = 4

class Buyer(PayPalEntity):
    """Dispute buyer obj representation
    """

    def __init__(self, name: str, **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.name = name

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        return cls(**json_data, json_response = json_data, response_type = response_type)

class ItemInfo(PayPalEntity):
    """Dispute item info obj representation
    """

    _ENTITY_TYPES = { 'dispute_amount': Money }

    def __init__(
            self, item_id: str = None, item_description: str = None, 
            partner_transaction_id: str = None, reason: str = None, 
            dispute_amount: Money = None, notes: str = None, **kwargs
        ):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.notes = notes
        self.reason = reason
        self.item_id = item_id
        self.dispute_amount = dispute_amount
        self.item_description  = item_description
        self.partner_transaction_id = partner_transaction_id

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        args = super()._build_args(json_data, cls._ENTITY_TYPES)
        return cls(**args, json_response = json_data, response_type = response_type)

class DisputeTransaction(PayPalEntity):
    """Transaction object representation
    """
    
    _ARRAY_TYPES = { 'messages': PaypalMessage, 'items': ItemInfo }
    _ENTITY_TYPES = { 'buyer': Buyer, 'gross_amount': Money, 'seller': PaypalMerchant }

    def __init__(
            self, buyer_transaction_id: str = None, seller_transaction_id: str = None, 
            transaction_status: str = None, buyer: Buyer = None, gross_amount: Money = None,
            seller: PaypalMerchant = None, messages: List[PaypalMessage] = [],
            invoice_number: str = None, custom: str = None, items: List[ItemInfo] = [], **kwargs
        ):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.buyer  = buyer
        self.seller = seller
        self.custom = custom
        self.items = items or []
        self.messages = messages or []
        self.gross_amount = gross_amount
        self.invoice_number = invoice_number
        self.transaction_status = transaction_status
        self.buyer_transaction_id = buyer_transaction_id
        self.seller_transaction_id = seller_transaction_id
        self._create_time = self._json_response.get('create_time', kwargs.get('create_time'))
    
    @property
    def create_time(self) -> datetime:
        try:
            return dateutil.parser.parse(self._create_time) if self._create_time else None
        except:
            return None

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        args = super()._build_args(json_data, cls._ENTITY_TYPES, cls._ARRAY_TYPES)
        return cls(**args, json_response= json_data, response_type = response_type)
 
class DisputeUpdateRequest(PatchUpdateRequest):
    """Update request for PATCH dispute updates
    """
    
    def __init__(self, merchant_email:str, note: str, operation: str='add', path: str='/communication_details'):
        super().__init__(path, {'email': merchant_email, 'note': note}, operation)

class DisputeTracker(PayPalEntity):
    """Dispute tracking info
    """
    def __init__(self, tracking_number: str, carrier_name: str, **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.carrier_name = carrier_name
        self.tracking_number = tracking_number
        self.tracking_url = kwargs.get('tracking_url')
        self.carrier_name_other = kwargs.get('carrier_name_other')

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        return cls(
            json_data['tracking_number'], json_data['carrier_name'],  
            json_response= json_data, response_type = response_type
        )

class RefundId(PayPalEntity):
    """Refund id obj representation
    """
    def __init__(self, refund_id: str, **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.refund_id = refund_id
    
    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        return cls(json_data.get('refund_id'), json_response = json_data, response_type = response_type)

class DisputeEvidenceInfo(PayPalEntity):
    """Dispute evidence info
    """

    _ARRAY_TYPES = { 'trackers': DisputeTracker, 'refund_ids': RefundId }

    def __init__(self, trackers: List[DisputeTracker] = [], refund_ids: List[RefundId]=[], **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.tracking_info = trackers or []
        self.refunds_ids = refund_ids or []

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        args = super()._build_args(json_data, dict(), cls._ARRAY_TYPES)    
        return cls(**args, json_response= json_data, response_type = response_type)

class Document(PayPalEntity):
    """Dispute document obj representation
    """

    def __init__(self, name: str, **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.name = name

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        return cls(**json_data, json_response = json_data, response_type = response_type)

class DisputeEvidence(PayPalEntity):
    """Dispute evidence for requests
    """

    _ENTITY_TYPES = { 'document': Document, 'evidence_info': DisputeEvidenceInfo }

    def __init__(
        self, evidence_type: str = None, notes: str = None, document: Document = None,
        item_id: str = None, evidence_info: DisputeEvidenceInfo = None, **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.notes = notes
        self.item_id = item_id
        self.document = document
        self.evidence_type = evidence_type
        self.evidence_info = evidence_info

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        args = super()._build_args(json_data, cls._ENTITY_TYPES)
        return cls(**args, json_response= json_data, response_type = response_type)

class DisputeOutcome(PayPalEntity):
    """Dispute outcome object representation    
    """
    def __init__(self, outcome_code: str, amount_refunded: Money, **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.outcome_code = outcome_code
        self.amount_refunded = amount_refunded

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        amount = Money.serialize_from_json(json_data['amount_refunded'])
        
        return cls(
            json_data['outcome_code'], amount, json_response= json_data, response_type = response_type
        )

class Dispute(PayPalEntity):
    """Dispute object representation
    """

    _ARRAY_TYPES = { 'messages': PaypalMessage, 'disputed_transactions': DisputeTransaction }
    _ENTITY_TYPES = { 'offer': Money, 'dispute_amount': Money, 'dispute_outcome': DisputeOutcome }

    def __init__(
        self, dispute_id: str = None, reason: str = None, status: str = None, amount: Money = None, 
        offer: Money = None, dispute_outcome: DisputeOutcome = None, messages: List[PaypalMessage] = [], 
        disputed_transactions: List[DisputeTransaction] = [], dispute_channel: str = None, 
        dispute_state: str = None, dispute_life_cycle_stage: str = None, **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.offer = offer
        self.reason = reason
        self.status = status
        self.dispute_id = dispute_id
        self.dispute_amount = amount
        self.messages = messages or []
        self.dispute_state = dispute_state
        self.dispute_channel = dispute_channel
        self.dispute_outcome = dispute_outcome
        self.disputed_transactions = disputed_transactions or []
        self.dispute_life_cycle_stage = dispute_life_cycle_stage
        self.extensions = self._json_response.get('extensions', kwargs.get('extensions')) 
        self._update_time = self._json_response.get('update_time', kwargs.get('update_time')) 
        self._create_time = self._json_response.get('create_time', kwargs.get('create_time')) 
        self.links = [ActionLink(x['href'], x['rel'], x.get('method', 'GET')) for x in self._json_response.get('links', [])]

    @property
    def dispute_state_enum(self) -> DisputeState:
        try:
            return DisputeState[self.dispute_state] if self.dispute_state else None
        except:
            return None
    
    @property
    def reason_enum(self) -> DisputeReason:
        try:
            return DisputeReason[self.reason] if self.reason else None
        except:
            return None

    @property
    def status_enum(self) -> DisputeStatus:
        try:
            return DisputeStatus[self.status] if self.status else None
        except:
            return None

    @property
    def dispute_channel_enum(self) -> DisputeChannel:
        try:
            return DisputeChannel[self.dispute_channel] if self.dispute_channel else None
        except:
            return None       
    
    @property
    def dispute_life_cycle_stage_enum(self) -> DisputeLifeCycleStage:
        try:
            return DisputeLifeCycleStage[self.dispute_life_cycle_stage] if self.dispute_life_cycle_stage else None
        except:
            return None

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

    @property
    def read_link(self) -> ActionLink:
        """Retrieves a link to read this entity details.
        
        Returns:
            ActionLink -- The link for requesting the information to the API.
        """
        return next(filter(lambda x: x.rel == 'self', self.links), None)

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:        
        args = super()._build_args(json_data, cls._ENTITY_TYPES, cls._ARRAY_TYPES)
        return cls(**args, json_response= json_data, response_type = response_type)