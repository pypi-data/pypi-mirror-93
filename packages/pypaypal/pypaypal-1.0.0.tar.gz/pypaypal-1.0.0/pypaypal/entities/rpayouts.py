"""
    Module with all referenced payout related entities.
"""

from enum import Enum
from datetime import datetime
from typing import Type, List

import dateutil.parser

from pypaypal.entities.base import ( 
    T, 
    Money,
    ActionLink, 
    PaypalName,
    PayPalEntity, 
    ResponseType, 
    PaypalPhoneDetail
)

class ProcessingStatus(Enum):
    # The item is pending.
    PENDING = 1
    # The item is processing.
    PROCESSING = 2
    # The item succeeded.
    SUCCESS = 3
    # The item failed.
    FAILED = 4
    # The payout failed for the item.
    PAYOUT_FAILED = 5

class ProcessingStatusReason(Enum):
    # An internal error occurred.
    INTERNAL_ERROR = 1
    # The balance is not enough.
    NOT_ENOUGH_BALANCE = 2
    # The amount check failed.
    AMOUNT_CHECK_FAILED = 3
    # A merchant-partner permissions issue occurred.
    MERCHANT_PARTNER_PERMISSIONS_ISSUE = 4
    # The merchant has restrictions.
    MERCHANT_RESTRICTIONS = 5
    # The transaction is under dispute.
    TRANSACTION_UNDER_DISPUTE = 6
    # The transaction is not valie.
    TRANSACTION_NOT_VALID = 7
    # The currency is not supported.
    UNSUPPORTED_CURRENCY = 8
    # The payout was already initiated.
    PAYOUT_INITIATED = 9
    # The payout was already completed.
    PAYOUT_ALREADY_COMPLETED_FOR_REFERENCE = 10

class ReferenceType(Enum):
    # The reference type is a transaction ID.
    TRANSACTION_ID = 1
    # The reference type is other.
    OTHERS = 2

class ExecutionType(Enum):
    SYNC = 1
    ASYNC = 2

    @property
    def is_sync(self) -> bool:
        return self.value == 1

    @property
    def is_async(self) -> bool:
        return self.value == 2

class ProcessingState(PayPalEntity):
    """Referenced payout item processing state obj definition
    """
    def __init__(self, status: str = None, reason: str = None, **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.status = status
        self.reason = reason
    
    @property
    def status_enum(self) -> ProcessingStatus:
        try:
            return ProcessingStatus[self.status] if self.status else None
        except:
            return None
    
    @property
    def reason_enum(self) -> ProcessingStatusReason:
        try:
            return ProcessingStatusReason[self.reason] if self.reason else None
        except:
            return None

    @classmethod
    def create(cls, *, status: ProcessingStatus = None, reason: str = ProcessingStatusReason) -> 'ProcessingState':
        return cls(
            status = status.name if status else None, 
            reason = reason.name if reason else None
        )

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        return cls(**json_data, json_response = json_data, response_type = response_type)

class PayoutDirective(PayPalEntity):
    """Payout Directive obj representation
    """
    def __init__(self, financial_instrument_id: str, **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.financial_instrument_id = financial_instrument_id
    
    @classmethod
    def create(cls, financial_instrument_id: str) -> 'PayoutDirective':
        return cls(financial_instrument_id = financial_instrument_id)

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        return cls(**json_data, json_response = json_data, response_type = response_type)

class ReferencedPayoutsItem(PayPalEntity):
    """Referenced Payouts Item obj representation
    """

    # Special entity types
    _ENTITY_TYPES = { 'processing_state': ProcessingState, 'payout_amount': Money }

    def __init__(
            self, item_id: str = None, processing_state: str = None, 
            reference_id: str = None, reference_type: str = None, payout_transaction_id: str = None, 
            disbursement_transaction_id: str = None, external_merchant_id: str = None, 
            payee_email: str = None, payout_amount: Money = None, payout_destination: str = None, 
            invoice_id: str = None, custom: str = None, **kwargs
        ):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.custom = custom
        self.item_id = item_id
        self.invoice_id = invoice_id
        self.payee_email = payee_email
        self.reference_id = reference_id
        self.payout_amount = payout_amount
        self.reference_type = reference_type
        self.processing_state = processing_state
        self.payout_destination = payout_destination
        self.external_merchant_id = external_merchant_id
        self.payout_transaction_id = payout_transaction_id
        self.disbursement_transaction_id = disbursement_transaction_id
        self.links = [ActionLink(x['href'], x['rel'], x.get('method', 'GET')) for x in self._json_response.get('links', [])]

    @property
    def read_link(self) -> ActionLink:
        """Retrieves a link to read this entity details.
        
        Returns:
            ActionLink -- The link for requesting the information to the API.
        """
        return next(filter(lambda x: x.rel == 'self', self.links), None)

    @property
    def reference_type_enum(self) -> ReferenceType:
        try:
            return ReferenceType[self.reference_type] if self.reference_type else None
        except:
            return None

    @classmethod
    def create(
        cls, *, item_id: str = None, processing_state: ProcessingState = None, 
        reference_id: str = None, reference_type: ReferenceType = None,
        disbursement_transaction_id: str = None, external_merchant_id: str = None, 
        payee_email: str = None, payout_amount: Money = None, 
        invoice_id: str = None, custom: str = None
    ) -> 'ReferencedPayoutsItem': 
        return cls(
            reference_type = reference_type.name if reference_type else None, payout_amount = payout_amount, 
            processing_state = processing_state, reference_id = reference_id, payee_email = payee_email,
            disbursement_transaction_id = disbursement_transaction_id, item_id = item_id, custom = custom,
            external_merchant_id = external_merchant_id, invoice_id = invoice_id,
        )

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        args = {
            **json_data,            
            **{ k : cls._ENTITY_TYPES[k].serialize_from_json(v, response_type) for k,v in json_data.items() if k in cls._ENTITY_TYPES.keys() and v }
        }

        return cls(**args, json_response = json_data, response_type = response_type)

class ReferencedPayoutCall(PayPalEntity):
    """ Class to wrap reference payout requests / responses
    """
    def __init__(
            self, payout_directive: PayoutDirective = None, referenced_payouts: List[ReferencedPayoutsItem] = [], **kwargs
        ):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.payout_directive = payout_directive
        self.referenced_payouts = referenced_payouts or []
        self.links = [ActionLink(x['href'], x['rel'], x.get('method', 'GET')) for x in self._json_response.get('links', [])]

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        return None

class ReferencedPayoutRequest(ReferencedPayoutCall):
    """Class to wrap reference payout requests    
    """
    def __init__(
            self, payout_directive: PayoutDirective, referenced_payouts: List[ReferencedPayoutsItem], 
            execution_type: ExecutionType = ExecutionType.SYNC 
        ):
        super().__init__(payout_directive = payout_directive, referenced_payouts = referenced_payouts, execution_type = execution_type)
        self._execution_type = execution_type

    @property
    def execution_type(self) -> ExecutionType:
        return ExecutionType.SYNC if self._execution_type == ExecutionType.SYNC and len(self.referenced_payouts) <= 10 else ExecutionType.ASYNC
    
    @classmethod
    def create(
            cls, payout_directive: PayoutDirective, referenced_payouts: List[ReferencedPayoutsItem], 
            execution_type: ExecutionType = ExecutionType.SYNC
        ) -> 'ReferencedPayoutRequest':
        exec_type = ExecutionType.SYNC if execution_type == ExecutionType.SYNC and len(referenced_payouts) <= 10 else ExecutionType.ASYNC
        return cls(payout_directive, referenced_payouts, exec_type)

class ReferencedPayoutResponse(ReferencedPayoutCall):
    """Class to wrap reference payout requests    
    """
    def __init__(
            self, payout_directive: PayoutDirective,
            referenced_payouts: List[ReferencedPayoutsItem], **kwargs
        ):
        super().__init__(payout_directive = payout_directive, referenced_payouts = referenced_payouts, **kwargs)

    @property
    def read_link(self) -> ActionLink:
        """Retrieves a link to read this entity details.
        
        Returns:
            ActionLink -- The link for requesting the information to the API.
        """
        return next(filter(lambda x: x.rel == 'self', self.links), None)

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        payout_directive, referenced_payouts  = None,  []

        if 'payout_directive'  in json_data.keys():
            payout_directive = PayoutDirective.serialize_from_json(payout_directive, response_type)
        if 'referenced_payouts' in json_data.keys():
            referenced_payouts = [ReferencedPayoutsItem.serialize_from_json(x, response_type) for x in json_data['referenced_payouts']]
        
        return cls(
            payout_directive = payout_directive, referenced_payouts = referenced_payouts, 
            json_response = json_data, response_type = response_type
        )