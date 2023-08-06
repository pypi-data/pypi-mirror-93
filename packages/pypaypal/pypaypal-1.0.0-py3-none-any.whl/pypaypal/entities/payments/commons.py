"""Common entities in payment resources
"""

from enum import Enum
from typing import Type, List

from pypaypal.entities.base import (
    T,
    ResponseType,    
    PayPalEntity
)

class DisputeCategoryReason(Enum):
    ITEM_NOT_RECEIVED = 1
    UNAUTHORIZED_TRANSACTION = 2

class SellerProtectionStatus(Enum):
    ELIGIBLE = 1 # Seller PayPal balance remains intact if a customer claims not receiving an item or an account holder claims not authorizing the payment.
    PARTIALLY_ELIGIBLE = 2 # PayPal balance remains intact if a customer claims not receiving an item.
    NOT_ELIGIBLE = 3 # transaction not eligible for seller protection.

class DisputeCategory(PayPalEntity):
    """Dispute Category obj representation
    """
    def __init__(self, dispute_category: str, **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.dispute_category = dispute_category

    @property
    def dispute_category_reason(self) -> DisputeCategoryReason:
        try:
            return DisputeCategoryReason[self.dispute_category] if self.dispute_category else None
        except:
            return None

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        return cls(json_data, json_response = json_data, response_type = response_type)

    @classmethod
    def create(cls, reason: DisputeCategoryReason) -> 'DisputeCategory':
        return cls(reason.name)

class SellerProtection(PayPalEntity):
    """Authorization seller protection details
    """
    def __init__(self, status: str, dispute_categories: List[DisputeCategory],**kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.status = status
        self.dispute_categories = dispute_categories

    @property
    def Status_enum(self) -> SellerProtectionStatus:
        try:
            return SellerProtectionStatus[self.status] if self.status else None
        except:
            return None

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        dispute_categories = []
        
        if 'dispute_categories' in json_data.keys():
            dispute_categories = [DisputeCategory.serialize_from_json(x, response_type) for x in json_data['dispute_categories']]

        return cls(json_data.get('status'), dispute_categories, json_response = json_data, response_type = response_type)

    @classmethod
    def create(cls, status: SellerProtectionStatus, dispute_categories: List[DisputeCategory]) -> 'SellerProtection':
        return cls(status.name, dispute_categories)

class ExchangeRate(PayPalEntity):
    """Capture exchange rate
    """
    def __init__(self, source_currency: str, target_currency: str, value: str, **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.value = value
        self.source_currency = source_currency
        self.target_currency = target_currency

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:        
        return cls(
            json_data.get('source_currency'), json_data.get('target_currency'), 
            json_data.get('value'), json_response = json_data, response_type = response_type
        )
