"""
    Module with subscription plans related entities
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
)

from pypaypal.entities.subscriptions.common import BillingCycleTenureType

class PlanStatus(Enum):
    # The plan was created. You cannot create subscriptions for a plan in this state.
    CREATED = 1
    # The plan is inactive.
    INACTIVE = 2
    # The plan is active. You can only create subscriptions for a plan in this state.
    ACTIVE = 3

class FrequencyIntervalUnit(Enum):
    # A daily billing cycle.
    DAY = 1 
    # A weekly billing cycle.
    WEEK = 2
    # A monthly billing cycle.
    MONTH = 3
    # A yearly billing cycle.
    YEAR = 4

class SetupFeeFailAction(Enum):
    # Cancels the subscription if the initial payment for the setup fails.
    CANCEL = 1
    # Continues the subscription if the initial payment for the setup fails.
    CONTINUE = 2

class PricingScheme(PayPalEntity):
    """Billing cycle pricing scheme obj representation
    """
    def __init__(self, version: int = None, fixed_price: Money = None, **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.version = version
        self.fixed_price = fixed_price
        self._update_time = self._json_response.get('update_time', kwargs.get('update_time'))
        self._create_time = self._json_response.get('create_time', kwargs.get('create_time'))
    
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
    def create(cls, *, version: int = None, fixed_price: Money = None) -> 'PricingScheme':
        return cls(version = version, fixed_price = fixed_price)

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        args = { **json_data }
        if 'fixed_price' in json_data.keys():
            args['fixed_price'] = Money.serialize_from_json(json_data['fixed_price'])
        return cls(**args, json_response= json_data, response_type = response_type)

class Frequency(PayPalEntity):
    """Billing cycle frequency obj representation
    """

    def __init__(self, interval_unit: str, interval_count: int = None, **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.interval_unit = interval_unit
        self.interval_count = interval_count

    @property
    def interval_unit_enum(self) -> FrequencyIntervalUnit:
        try:
            return FrequencyIntervalUnit[self.interval_unit] if self.interval_unit else None
        except:
            return None

    @classmethod
    def create(cls, *, interval_unit: FrequencyIntervalUnit, interval_count: int = 1) -> 'Frequency':
        return cls(interval_unit = interval_unit.name, interval_count = interval_count)

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        return cls(**json_data, json_response = json_data, response_type = response_type)

class BillingCycle(PayPalEntity):
    """Plan billing cycle obj representation.
    """

    # Serializable entity types
    _ENTITY_TYPES = { 'frequency': Frequency, 'pricing_scheme': PricingScheme }

    def __init__(
            self, pricing_scheme: PricingScheme, frequency: Frequency, 
            tenure_type: str, sequence: int, total_cycles: int, **kwargs
        ):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.sequence = sequence
        self.frequency = frequency
        self.tenure_type = tenure_type
        self.total_cycles = total_cycles
        self.pricing_scheme = pricing_scheme
    
    @property
    def tenure_type_enum(self) -> BillingCycleTenureType:
        try:
            return BillingCycleTenureType[self.tenure_type] if self.tenure_type else None
        except:
            return None
    
    @classmethod
    def create(
            cls, *, frequency: Frequency, tenure_type: BillingCycleTenureType, 
            sequence: int, pricing_scheme: PricingScheme = None, total_cycles: int = 1
        ) -> 'BillingCycle':
        return cls(pricing_scheme, frequency, tenure_type.name, sequence, total_cycles)

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        args = super()._build_args(json_data, cls._ENTITY_TYPES)
        return cls(**args, json_response= json_data, response_type = response_type)

class PaymentPreferences(PayPalEntity):
    """Payment preference obj representation
    """

    def __init__(
            self, auto_bill_outstanding: bool, setup_fee: Money, 
            setup_fee_failure_action: str, payment_failure_threshold: int, 
            **kwargs
        ):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.setup_fee = setup_fee
        self.auto_bill_outstanding = auto_bill_outstanding
        self.setup_fee_failure_action = setup_fee_failure_action
        self.payment_failure_threshold = payment_failure_threshold
    
    @property
    def setup_fee_failure_action_enum(self) -> SetupFeeFailAction:
        try:
            return SetupFeeFailAction[self.setup_fee_failure_action] if self.setup_fee_failure_action else None
        except:
            return None
    
    @classmethod
    def create(
            cls, *, auto_bill_outstanding: bool = True, payment_failure_threshold: int = 0,
            setup_fee: Money = None, setup_fee_failure_action: SetupFeeFailAction = SetupFeeFailAction.CANCEL
        ) -> 'PaymentPreferences':
        return cls(auto_bill_outstanding, setup_fee, setup_fee_failure_action.name, payment_failure_threshold)

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        args = { **json_data }
        if 'setup_fee' in json_data.keys():
            args['setup_fee'] = Money.serialize_from_json(json_data['setup_fee'], response_type)
        return cls( **args, json_response= json_data, response_type = response_type)

class Taxes(PayPalEntity):
    """Subscription taxes obj representation
    """

    def __init__(self, percentage: str, inclusive: bool = None, **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.inclusive = inclusive
        self.percentage = percentage
    
    @classmethod
    def create(cls, percentage: str, inclusive: bool = True) -> 'Taxes':
        return cls(percentage, inclusive)
    
    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        return cls(**json_data, json_response = json_data, response_type = response_type)

class Plan(PayPalEntity):
    """Subscription Plan obj representation
    """

    _ARRAY_TYPES = { 'billing_cycles': BillingCycle }
    _ENTITY_TYPES = { 'payment_preferences': PaymentPreferences, 'taxes': Taxes }

    def __init__(
            self, plan_id: str = None, product_id: str = None, 
            name: str = None, status: str = None, description: str = None, 
            billing_cycles: List[BillingCycle] = None, payment_preferences: PaymentPreferences = None,
            taxes:Taxes  = None, quantity_supported: bool = None, **kwargs
        ):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.name = name
        self.id = plan_id
        self.taxes = taxes
        self.status = status
        self.product_id = product_id
        self.description = description
        self.billing_cycles = billing_cycles
        self.quantity_supported = quantity_supported
        self.payment_preferences = payment_preferences
        self._update_time = self._json_response.get('update_time', kwargs.get('update_time'))
        self._create_time = self._json_response.get('create_time', kwargs.get('create_time'))
        self.links = [ActionLink(x['href'], x['rel'], x.get('method', 'GET')) for x in self._json_response.get('links', [])]

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
    def status_enum(self) -> PlanStatus:
        """Status of the plan as an enum constant
        
        Returns:
            PlanStatus -- An enumerated constant representing the plan status or None
        """
        try:
            return PlanStatus[self.status] if self.status else None
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
    def create(
            cls, product_id: str, name: str, billing_cycles: List[BillingCycle],
            payment_preferences: PaymentPreferences = None, description: str = None,
            status: PlanStatus = None, taxes:Taxes  = None, quantity_supported: bool = None
        ) -> 'Plan':
        return cls(
            product_id = product_id, name = name, taxes = taxes,
            description = description, billing_cycles = billing_cycles,
            quantity_supported = quantity_supported, payment_preferences = payment_preferences,
            status = status.name if status else None
        )

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        args = super()._build_args(json_data, cls._ENTITY_TYPES, cls._ARRAY_TYPES)
        args['plan_id'] = args.pop('id', None)
        return cls(**args, json_response= json_data, response_type = response_type)