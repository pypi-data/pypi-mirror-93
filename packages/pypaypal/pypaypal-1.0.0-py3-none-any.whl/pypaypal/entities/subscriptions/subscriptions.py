from enum import Enum
from datetime import datetime
from typing import Type, List

import dateutil.parser

from pypaypal.entities.base import (
    T, 
    Money, 
    PaypalName,
    ActionLink, 
    PayPalEntity, 
    ResponseType,
    PaymentMethod,
    AppCtxLandingPage,
    ApplicationContext,
    PaypalPortableAddress,
    AppCtxShippingPreference
)

from pypaypal.entities.subscriptions.common import BillingCycleTenureType

class SubscriptionTransactionStatus(Enum):
    # The funds for this captured payment were credited to the payee's PayPal account.
    COMPLETED = 1
    # The funds could not be captured.
    DECLINED = 2
    # An amount less than this captured payment's amount was partially refunded to the payer.
    PARTIALLY_REFUNDED = 3
    # The funds for this captured payment was not yet credited to the payee's PayPal account.
    PENDING = 4
    # An amount greater than or equal to this captured payment's amount was refunded to the payer.
    REFUNDED = 5

class SubscriptionStatus(Enum):
    # The subscription is created but not yet approved by the buyer.
    APPROVAL_PENDING = 1
    # The buyer has approved the subscription.
    APPROVED = 2
    # The subscription is active.
    ACTIVE = 3
    # The subscription is suspended.
    SUSPENDED = 4
    # The subscription is cancelled.
    CANCELLED = 5
    # The subscription is expired.
    EXPIRED = 6

class SubscriptionUserAction(Enum):
    # After you redirect the customer to the PayPal subscription consent page, a Continue button appears.
    # Use this option when you want to control the activation of the subscription and do not want PayPal to activate the subscription.
    CONTINUE = 1
    # After you redirect the customer to the PayPal subscription consent page, a Subscribe Now button appears. 
    # Use this option when you want PayPal to activate the subscription.
    SUBSCRIBE_NOW = 2

class Email(PayPalEntity):
    """Subscription email obj representation
    """
    def __init__(self, email: str, **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.email = email

    @classmethod
    def create(cls, email: str) -> 'Email':
        return cls(email)

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        return cls(**json_data, json_response= json_data, response_type = response_type)

class SubscriptionApplicationContext(ApplicationContext):
    """Paypal subscription app context object representation
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    @property
    def subscription_user_action(self) -> SubscriptionUserAction:
        try:
            return SubscriptionUserAction[self.user_action] if self.user_action else None
        except:
            return None

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        return super().serialize_from_json(json_data, response_type)
            
    @classmethod
    def create(cls, brand_name: str = None, locale: str = None, return_url: str = None, cancel_url: str = None, 
        payment_method: PaymentMethod = None, landing_page: AppCtxLandingPage = AppCtxLandingPage.NO_PREFERENCE,
        shipping_preference: AppCtxShippingPreference = AppCtxShippingPreference.GET_FROM_FILE, 
        user_action: SubscriptionUserAction = SubscriptionUserAction.SUBSCRIBE_NOW) -> 'ApplicationContext':
        return super().create(
            brand_name, locale, landing_page.name, shipping_preference.name,
            user_action.name, payment_method, return_url, cancel_url
        )

class ShippingDetail(PayPalEntity):
    """Shipping detail obj representation
    """
    _ENTITY_TYPES =  {'address': PaypalPortableAddress}

    def __init__(self, name: str = None, address: PaypalPortableAddress = None, **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.name = name
        self.address = address
    
    @classmethod
    def create(cls, name: str, address: PaypalPortableAddress) -> 'ShippingDetail':
        return cls(name, address)

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        args = super()._build_args(json_data, cls._ENTITY_TYPES)
        return cls(**args, json_response= json_data, response_type = response_type)

class Subscriber(PayPalEntity):
    """Subscriber obj representation
    """
    _ENTITY_TYPES =  { 'email_address': Email, 'shipping_address': ShippingDetail }

    def __init__(self, name: str = None, email_address: Email = None, shipping_address: ShippingDetail = None, **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.name = name
        self.email_address = email_address
        self.shipping_address = shipping_address

    @classmethod
    def create(cls, name: str = None, email_address: Email = None, shipping_address: ShippingDetail = None) -> 'Subscriber':
        return cls(name, email_address, shipping_address)

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        args = super()._build_args(json_data, cls._ENTITY_TYPES)
        return cls(**args, json_response= json_data, response_type = response_type)

class CycleExecution(PayPalEntity):
    """Subscription cycle execution obj representation
    """

    def __init__(
            self, tenure_type: str = None, sequence: int = None, cycles_completed: int = None, 
            cycles_remaining: int = None, current_pricing_scheme_version: int = None,
            total_cycles: int = None, **kwargs
        ):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.sequence = sequence
        self.tenure_type = tenure_type
        self.total_cycles = total_cycles
        self.cycles_completed = cycles_completed 
        self.cycles_remaining = cycles_remaining
        self.current_pricing_scheme_version = current_pricing_scheme_version
    

    @property
    def tenure_type_enum(self) -> BillingCycleTenureType:
        try:
            return BillingCycleTenureType[self.tenure_type] if self.tenure_type else None
        except:
            return None
    
    @classmethod
    def create(
            cls, *, tenure_type: BillingCycleTenureType, sequence: int, 
            cycles_completed: int, cycles_remaining: int = None, 
            current_pricing_scheme_version: int = None, total_cycles: int = None
        ) -> 'CycleExecution':
        return cls(
            tenure_type.name, sequence, cycles_completed, cycles_remaining, 
            current_pricing_scheme_version, total_cycles
        )

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:        
        return cls(**json_data, json_response= json_data, response_type = response_type)

class LastPaymentDetails(PayPalEntity):
    """Subscription last payment details obj representation.
    """
    
    _ENTITY_TYPES = { 'amount': Money }

    def __init__(self, amount: Money, time: str, **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.time = time
        self.amount = amount

    @property
    def time_as_date(self) -> datetime:
        try:
            return dateutil.parser.parse(self.time) if self.time else None
        except:
            return None

    @classmethod
    def create(cls, *, amount: Money, time: str) -> 'LastPaymentDetails':
        return cls(amount, time)

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:        
        args = super()._build_args(json_data, cls._ENTITY_TYPES)
        return cls(**args, json_response= json_data, response_type = response_type)

class BillingInfo(PayPalEntity):
    """Subscription billing info obj representation
    """
    
    # Serializable paypal entity arrays
    _ARRAY_TYPES = { 'cycle_executions': CycleExecution }

    # Serializable simple paypal entities
    _ENTITY_TYPES = { 'outstanding_balance': Money, 'last_payment': LastPaymentDetails}
    
    def __init__(self, failed_payments_count: int, outstanding_balance: Money, last_payment: LastPaymentDetails = None, cycle_executions: List[CycleExecution] = [], **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.last_payment = last_payment
        self.cycle_executions = cycle_executions or []
        self.outstanding_balance = outstanding_balance
        self.failed_payments_count = failed_payments_count

    @classmethod
    def create(cls, *, failed_payments_count: int, outstanding_balance: Money, last_payment: LastPaymentDetails = None, cycle_executions: List[CycleExecution] = []) -> 'BillingInfo':
        return cls(failed_payments_count, outstanding_balance, last_payment, cycle_executions or [])

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:        
        args = super()._build_args(json_data, cls._ENTITY_TYPES, cls._ARRAY_TYPES)
        return cls(**args, json_response= json_data, response_type = response_type)

class Subscription(PayPalEntity):
    """Paypal subscription obj representation
    """
    
    _ENTITY_TYPES = { 'subscriber': Subscriber, 'billing_info': BillingInfo, 'shipping_amount': Money }

    def __init__(
            self, subscription_id: str = None, status: str = None, 
            plan_id: str = None, status_change_note: str = None, 
            quantity: str = None, subscriber: Subscriber = None,             
            billing_info: BillingInfo = None, shipping_amount: Money = None,            
            application_context: SubscriptionApplicationContext = None, **kwargs
        ):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.id = subscription_id
        self.status = status
        self.plan_id = plan_id 
        self.quantity = quantity
        self.subscriber = subscriber 
        self.billing_info = billing_info
        self.shipping_amount = shipping_amount 
        self.status_change_note = status_change_note
        self.application_context = kwargs.get('application_context')
        self._update_time = self._json_response.get('update_time', kwargs.get('update_time'))
        self._create_time = self._json_response.get('create_time', kwargs.get('create_time'))
        self._start_time = self._json_response.get('_start_time', kwargs.get('_start_time'))            
        self._status_update_time = self._json_response.get('_status_update_time', kwargs.get('_status_update_time'))
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
    def start_time(self) -> datetime:
        try:
            return dateutil.parser.parse(self._start_time) if self._start_time else None
        except:
            return None

    @property
    def status_update_time(self) -> datetime:
        try:
            return dateutil.parser.parse(self._status_update_time) if self._status_update_time else None
        except:
            return None

    @property
    def status_enum(self) -> SubscriptionStatus:
        """Status of the subscription as an enum constant
        
        Returns:
            PlanStatus -- An enumerated constant representing the subscription status or None
        """
        try:
            return SubscriptionStatus[self.status] if self.status else None
        except:
            return None

    @property
    def read_link(self) -> ActionLink:
        """Retrieves a link to read this entity details.
        
        Returns:
            ActionLink -- The link for requesting the information to the API.
        """
        return next(filter(lambda x: x.rel == 'self', self.links), None)

    def to_dict(self) -> dict:
        ret = super().to_dict()
        if '_start_time' in ret.keys():
            ret['start_time'] = ret.pop('_start_time')
        return ret

    @classmethod
    def create(
            cls, *, plan_id: str, start_time: datetime = datetime.now(), 
            quantity: str = None, shipping_amount: Money = None,
            subscriber: Subscriber = None, application_context: SubscriptionApplicationContext = None
        ) -> 'Subscription':
        return cls(
            plan_id = plan_id, start_time = start_time.strftime('%Y-%m-%dT%H:%M:%S'), quantity = quantity,
            shipping_amount = shipping_amount, subscriber = subscriber, 
            application_context = application_context
        )

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:        
        args = super()._build_args(json_data, cls._ENTITY_TYPES)
        args['subscription_id'] = args.pop('id', None)
        return cls(**args, json_response= json_data, response_type = response_type)


class AmountWithBreakdown(PayPalEntity):
    """Subscription transaction amount with breakdown
    """
    
    _ENTITY_TYPES = { 
        'net_amount': Money, 'gross_amount': Money, 'fee_amount': Money, 
        'shipping_amount': Money, 'tax_amount': Money
    }
    
    def __init__(
            self, net_amount: Money, gross_amount: Money, 
            fee_amount: Money = None, shipping_amount: Money = None, 
            tax_amount: Money = None, **kwargs
        ):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.net_amount = net_amount
        self.fee_amount = fee_amount
        self.tax_amount = tax_amount
        self.gross_amount = gross_amount
        self.shipping_amount = shipping_amount

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:        
        args = super()._build_args(json_data, cls._ENTITY_TYPES)
        return cls(**args, json_response= json_data, response_type = response_type)

class SubscriptionTransaction(PayPalEntity):
    """A subscription transaction for querying purposes
    """

    _ENTITY_TYPES = { 
        'payer_name': PaypalName, 'amount_with_breakdown': AmountWithBreakdown
    }

    def __init__(
            self, status: str = None, transaction_id: str = None, 
            amount_with_breakdown: AmountWithBreakdown = None, 
            payer_name: PaypalName = None, payer_email: str = None, 
            **kwargs
        ):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.status = status 
        self.payer_name = payer_name
        self.payer_email = payer_email
        self.transaction_id = transaction_id
        self.amount_with_breakdown = amount_with_breakdown
        self._time = self._json_response.get('time', kwargs.get('time'))

    @property
    def status_enum(self) -> SubscriptionTransactionStatus:
        """Status of the subscription transaction as an enum constant
        
        Returns:
            PlanStatus -- An enumerated constant representing the subscription status or None
        """
        try:
            return SubscriptionTransactionStatus[self.status] if self.status else None
        except:
            return None

    @property
    def time(self) -> datetime:
        try:
            return dateutil.parser.parse(self._time) if self._time else None
        except:
            return None

    def to_dict(self) -> dict:
        r = super().to_dict()
        r['time'] = r.pop('_time', None)
        r['id'] = r.pop('transaction_id', None)
        return r

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:        
        args = super()._build_args(json_data, cls._ENTITY_TYPES)
        args['transaction_id'] = args.pop('id', None)
        return cls(**args, json_response= json_data, response_type = response_type)
