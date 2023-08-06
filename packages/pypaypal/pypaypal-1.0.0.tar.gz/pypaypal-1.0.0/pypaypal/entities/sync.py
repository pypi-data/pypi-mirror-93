"""
    Module with all Paypal Sync (transactions) related entities 
"""
from enum import Enum
from datetime import datetime
from typing import NamedTuple, Type, List

import dateutil.parser

from pypaypal.entities.base import (
    T,
    Money,
    PaypalName,
    ActionLink,
    ResponseType,
    PayPalEntity,
    PaypalPhoneDetail,
    PaypalPortableAddress
)

# Transaction statuses string definitions
# See the enumeration for details.
_TRANSACTION_STATUSES = [ 'D', 'F', 'P', 'S', 'V' ]

class TransactionStatus(Enum):
    # PayPal or merchant rules denied the transaction. ('D')
    DENIED = 1
    # The original recipient partially refunded the transaction. ('F')
    PARTIALLY_REFUNDED = 2
    # The transaction is pending. The transaction was created but waits for another payment process to complete, 
    # such as an ACH transaction, before the status changes to S. ('P')
    PENDING = 3
    # The transaction successfully completed without a denial and after any pending statuses. ('S')
    SUCCESSFUL = 4
    # A successful transaction was reversed and funds were refunded to the original sender. ('V')
    SUCCESSFUL_REVERSAL = 5

    def as_string_parameter(self) -> str:
        return _TRANSACTION_STATUSES[self.value - 1]

# Transaction status mapping for enum conversion
_TRANSACTION_STATUS_MAPPING = {
    'D': TransactionStatus.DENIED,
    'P': TransactionStatus.PENDING,
    'S': TransactionStatus.SUCCESSFUL,
    'F': TransactionStatus.PARTIALLY_REFUNDED,
    'V': TransactionStatus.SUCCESSFUL_REVERSAL
}

# Mapping dictionary for different transaction event types.
_EVENT_TYPE_MAPPINGS = {
    'T00': 'PayPal account-to-PayPal account payment',
    'T01': 'Non-payment-related fees',
    'T02': 'Currency conversion',
    'T03': 'Bank deposit into PayPal account',
    'T04': 'Bank withdrawal from PayPal account',
    'T05': 'Debit card',
    'T06': 'Credit card withdrawal',
    'T07': 'Credit card deposit',
    'T08': 'Bonus',
    'T09': 'Incentive',
    'T10': 'Bill pay',
    'T11': 'Reversal',
    'T12': 'Adjustment',
    'T13': 'Authorization',
    'T14': 'Dividend',
    'T15': 'Hold for dispute or other investigation',
    'T16': 'Buyer credit deposit',
    'T17': 'Non-bank withdrawal',
    'T18': 'Buyer credit withdrawal',
    'T19': 'Account correction',
    'T20': 'Funds transfer from PayPal account to another',
    'T21': 'Reserves and releases',
    'T22': 'Transfers',
    'T30': 'Generic instrument and Open Wallet',
    'T50': 'Collections and disbursements',
    'T97': 'Payables and receivables',
    'T98': 'Display only transaction',
    'T99': 'Other',
}

# Mapping dictionary for different transaction event descriptions.
_EVENT_DESC_MAPPINGS = {
    # PayPal account-to-PayPal account payment
    'T0000': 'General: received payment of a type not belonging to the other T00nn categories.',
    'T0001': 'MassPay payment.',
    'T0002': 'Subscription payment. Either payment sent or payment received.',
    'T0003': 'Pre-approved payment (BillUser API). Either sent or received.',
    'T0004': 'eBay auction payment.',
    'T0005': 'Direct payment API.',
    'T0006': 'PayPal Checkout APIs.',
    'T0007': 'Website payments standard payment.',
    'T0008': 'Postage payment to carrier.',
    'T0009': 'Gift certificate payment. Purchase of gift certificate.',
    'T0010': 'Third-party auction payment.',
    'T0011': 'Mobile payment, made through a mobile phone.',
    'T0012': 'Virtual terminal payment.',
    'T0013': 'Donation payment.',
    'T0014': 'Rebate payments.',
    'T0015': 'Third-party payout.',
    'T0016': 'Third-party recoupment.',
    'T0017': 'Store-to-store transfers.',
    'T0018': 'PayPal Here payment.',
    'T0019': 'Generic instrument-funded payment.',

    # Non-payment-related fees
    'T0100': 'General non-payment fee of a type not belonging to the other  T01nn categories.',
    'T0101': 'Website payments. Pro account monthly fee.',
    'T0102': 'Foreign bank withdrawal fee.',
    'T0103': 'WorldLink check withdrawal fee.',
    'T0104': 'Mass payment batch fee.',
    'T0105': 'Check withdrawal.',
    'T0106': 'Chargeback processing fee. Chargeback processing, or handling, fee. Charged against account that received a chargeback for a previous transaction.',
    'T0107': 'Payment fee.',
    'T0108': 'ATM withdrawal.',
    'T0109': 'Auto-sweep from account.',
    'T0110': 'International credit card withdrawal.',
    'T0111': 'Warranty fee for warranty purchase.',
    'T0112': 'Gift certificate expiration fee.',
    'T0113': 'Partner fee.',

    # Currency conversion
    'T0200': 'General currency conversion. Transfer of funds from one currency balance to a different currency balance or Withdrawal of funds from one currency balance that is covered by funds from a different currency balance.',
    'T0201': 'User-initiated currency conversion.',
    'T0202': 'Currency conversion required to cover negative balance. PayPal-system generated.',
    
    # Bank deposit into PayPal account
    'T0300': 'General funding of PayPal account. Deposit to PayPal balance from a bank account.',
    'T0301': 'PayPal balance manager funding of PayPal account.(PayPal-system generated).',
    'T0302': 'ACH funding for funds recovery from account balance.',
    'T0303': 'Electronic funds transfer (EFT) (German banking).',

    # Bank withdrawal from PayPal account
    'T0400': 'General withdrawal from PayPal account. Settlement withdrawal or user-initiated.',
    'T0401': 'AutoSweep.',

    # Debit card
    'T0500': 'General PayPal debit card transaction. Requires a PayPal debit card associated with the PayPal account.',
    'T0501': 'Virtual PayPal debit card transaction.',
    'T0502': 'PayPal debit card withdrawal to ATM.',
    'T0503': 'Hidden virtual PayPal debit card transaction.',
    'T0504': 'PayPal debit card cash advance.',
    'T0505': 'PayPal debit authorization.',

    # Credit card withdrawal
    'T0600': 'General credit card withdrawal. Reversal of purchase with a credit card. Seen only in PayPal account of the credit card owner.',

    # Credit card deposit
    'T0700': 'General credit card deposit. Purchase with a credit card.',
    'T0701': 'Credit card deposit for negative PayPal account balance.',

    # Bonus
    'T0800': 'General bonus of a type not belonging to the other  T08nn categories.',
    'T0801': 'Debit card cash back bonus. Requires a PayPal debit card associated with the PayPal account.',
    'T0802': 'Merchant referral account bonus. Must have created a merchant referral bonus link.',
    'T0803': 'Balance manager account bonus.',
    'T0804': 'PayPal buyer warranty bonus.',
    'T0805': 'PayPal protection bonus, payout for PayPal buyer protection, payout for full protection with PayPal buyer credit.',
    'T0806': 'Bonus for first ACH use.',
    'T0807': 'Credit card security charge refund.',
    'T0808': 'Credit card cash back bonus.',
    
    # Incentive
    'T0900': 'General incentive or certificate redemption.',
    'T0901': 'Gift certificate redemption.',
    'T0902': 'Points incentive redemption.',
    'T0903': 'Coupon redemption.',
    'T0904': 'eBay loyalty incentive.',
    'T0905': 'Offers used as funding source.',

    # Bill pay
    'T1000': 'Bill pay transaction.',

    # Reversal
    'T1100': 'General reversal of a type not belonging to the other  T11nn categories.',
    'T1101': 'Reversal of ACH withdrawal transaction. Reversal of a withdrawal from PayPal balance to a bank account.',
    'T1102': 'Reversal of debit card transaction. Reversal of a debit card payment. Requires a PayPal debit card.',
    'T1103': 'Reversal of points usage.',
    'T1104': 'Reversal of ACH deposit.',
    'T1105': 'Reversal of general account hold.',
    'T1106': 'Payment reversal, initiated by PayPal. Completion of a chargeback.',
    'T1107': 'Payment refund, initiated by merchant.',
    'T1108': 'Fee reversal.',
    'T1109': 'Fee refund.',
    'T1110': 'Hold for dispute investigation (T15nn). To cover possible chargeback.',
    'T1111': 'Cancellation of hold for dispute resolution. Cancellation of temporary hold to cover possible chargeback.',
    'T1112': 'MAM reversal.',
    'T1113': 'Non-reference credit payment.',
    'T1114': 'MassPay reversal transaction.',
    'T1115': 'MassPay refund transaction.',
    'T1116': 'Instant payment review (IPR) reversal.',
    'T1117': 'Rebate or cash back reversal.',
    'T1118': 'Generic instrument/Open Wallet reversals (seller side).',
    'T1119': 'Generic instrument/Open Wallet reversals (buyer side).',

    # Adjustment
    'T1200': 'General account adjustment.',
    'T1201': 'Chargeback.',
    'T1202': 'Chargeback reversal.',
    'T1203': 'Charge-off adjustment.',
    'T1204': 'Incentive adjustment.',
    'T1205': 'Reimbursement of chargeback.',
    'T1207': 'Chargeback re-presentment rejection. Adjustment to PayPal account for reversal of payment based on rejection of the re-presentment for a chargeback in the PayPal system.',
    'T1208': 'Chargeback cancellation. Adjustment to PayPal account for reversal of chargeback reversal based on cancellation of a chargeback in the PayPal system.',

    # Authorization
    'T1300': 'General authorization.',
    'T1301': 'Reauthorization.',
    'T1302': 'Void of authorization.',

    # Dividend
    'T1400': 'General dividend.',

    # Hold for dispute or other investigation
    'T1500': 'General temporary hold of a type not belonging to the other  T15nn categories.',
    'T1501': 'Account hold for open authorization.',
    'T1502': 'Account hold for ACH deposit.',
    'T1503': 'Temporary hold on available balance.',

    # Buyer credit deposit
    'T1600': 'PayPal buyer credit payment funding. Must have signed up for buyer credit.',
    'T1601': 'BML credit. Transfer from BML.',
    'T1602': 'Buyer credit payment.',
    'T1603': 'Buyer credit payment withdrawal. Transfer to BML.',

    # Non-bank withdrawal
    'T1700': 'General withdrawal to non-bank institution.',
    'T1701': 'WorldLink withdrawal.',

    # Buyer credit withdrawal
    'T1800': 'General buyer credit payment. Must have signed up for buyer credit.',
    'T1801': 'BML withdrawal. Transfer to BML.',

    # Account correction
    'T1900': 'General adjustment without business-related event.',

    # Funds transfer from PayPal account to another
    'T2000': 'General intra-account transfer.',
    'T2001': 'Settlement consolidation.',
    'T2002': 'Transfer of funds from payable.',
    'T2003': 'Transfer to external GL entity.',

    # Reserves and releases
    'T2101': 'General hold.',
    'T2102': 'General hold release.',
    'T2103': 'Reserve hold. PayPal holds (n) of funds for (d) days as a condition for processing for you. This amount is part of your total balance and is not available for withdrawal.',
    'T2104': 'Reserve release. A reserve, when released, is now available for withdrawal.',
    'T2105': 'Payment review hold. A payment review hold is used to protect you against unauthorized fraud loss and for seller protection. While a transaction is on payment review hold, we recommend that you do not ship the item. We are reviewing this transaction for up to 24 hours.',
    'T2106': 'Payment review release. A payment review hold, when released, is now available for withdrawal.',
    'T2107': 'Payment hold. Payment holds are funds that belong to you that we set aside, such as a security deposit. This amount is part of your total balance and is not available for withdrawal.',
    'T2108': 'Payment hold release. A payment hold, when released, is now available for withdrawal.',
    'T2109': 'Gift certificate purchase. When a gift certificate is purchased by your buyer, that amount is placed on hold.',
    'T2110': 'Gift certificate redemption. A gift certificate, when redeemed, is available for withdrawal.',
    'T2111': 'Funds not yet available. While you establish a successful sales history on eBay, funds from eBay sales are usually available in 21 or fewer days, based on how you ship the order. You might get your funds faster if you print your shipping labels on eBay or PayPal, upload tracking information, or mark the item as shipped on eBay. If your buyer reports a problem with the sale, it might take longer to get funds.',
    'T2112': 'Funds available. These funds are available for use.',
    'T2113': 'Blocked payments.',

    # Transfers
    'T2201': 'Transfer to and from a credit-card-funded restricted balance.',

    # Generic instrument and Open Wallet
    'T3000': 'Generic instrument/Open Wallet transaction.',

    # Collections and disbursements
    'T5000': 'Deferred disbursement. Funds collected for disbursement.',
    'T5001': 'Delayed disbursement. Funds disbursed.',

    # Payables and receivables
    'T9700': 'Account receivable for shipping.',
    'T9701': 'Funds payable. PayPal-provided funds that must be paid back.',
    'T9702': 'Funds receivable. PayPal-provided funds that are being paid back.',

    # Display only transaction
    'T9800': 'Display only transaction.',

    # Other
    'T9900': 'Other.'
}

class ReferenceIdType(Enum):
    # An order ID. (ODR)
    ORDER_ID = 1
    # A transaction ID. (TXN)
    TRANSACTION_ID = 2
    # A subscription ID. (SUB)
    SUBSCRIPTION_ID = 3 
    # A pre-approved payment ID. (PAP)
    PREAPPROVED_PAYMENT_ID = 4

_REFERENCE_ID_MAPPINGS = {
    'ODR': ReferenceIdType.ORDER_ID,
    'TXN': ReferenceIdType.TRANSACTION_ID,
    'SUB': ReferenceIdType.SUBSCRIPTION_ID,
    'PAP': ReferenceIdType.PREAPPROVED_PAYMENT_ID
}

class ProtectionElegibility(Enum):
    ELEGIBLE = 1
    NOT_ELEGIBLE = 2
    PARTIALLY_ELEGIBLE = 3

class PayerStatusProperty(Enum):
    VERIFIED = 1
    UNVERIFIED = 2

class TransactionInfo(PayPalEntity):
    """Transaction info object representation
    """

    _MONEY_TYPES = {
        'transaction_amount', 'fee_amount', 'discount_amount', 'insurance_amount',
        'sales_tax_amount', 'shipping_amount', 'shipping_discount_amount',
        'shipping_tax_amount', 'other_amount', 'tip_amount', 'ending_balance',
        'available_balance', 'credit_transactional_fee', 'credit_promotional_fee'
    }

    def __init__(
        self, paypal_account_id: str = None, transaction_id: str = None,
        paypal_reference_id: str = None, paypal_reference_id_type: str = None, 
        transaction_event_code: str = None, transaction_amount: Money = None, fee_amount: Money = None, 
        discount_amount: Money = None, insurance_amount: Money = None, sales_tax_amount: Money = None, 
        shipping_amount: Money = None, shipping_discount_amount: Money = None, shipping_tax_amount: Money = None, 
        other_amount: Money = None, tip_amount: Money = None, transaction_status: str = None, transaction_subject: str = None, 
        transaction_note: str = None, payment_tracking_id: str = None, bank_reference_id: str = None, ending_balance: Money = None, 
        available_balance: Money = None, invoice_id: str = None, custom_field: str = None, protection_eligibility: str = None, 
        credit_term: str = None, credit_transactional_fee: Money = None, credit_promotional_fee: Money = None, 
        annual_percentage_rate: str = None, payment_method_type: str = None, **kwargs
        ):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.fee_amount = fee_amount
        self.tip_amount = tip_amount
        self.invoice_id = invoice_id
        self.credit_term = credit_term
        self.other_amount = other_amount
        self.custom_field = custom_field
        self.ending_balance = ending_balance
        self.transaction_id = transaction_id
        self.discount_amount = discount_amount
        self.shipping_amount = shipping_amount
        self.insurance_amount = insurance_amount
        self.sales_tax_amount = sales_tax_amount
        self.transaction_note = transaction_note
        self.bank_reference_id = bank_reference_id
        self.paypal_account_id = paypal_account_id
        self.available_balance = available_balance
        self.transaction_amount = transaction_amount
        self.transaction_status = transaction_status
        self.transaction_subject = transaction_subject
        self.paypal_reference_id = paypal_reference_id
        self.shipping_tax_amount = shipping_tax_amount
        self.payment_tracking_id = payment_tracking_id
        self.payment_method_type = payment_method_type
        self.protection_eligibility = protection_eligibility
        self.transaction_event_code = transaction_event_code
        self.credit_promotional_fee = credit_promotional_fee
        self.annual_percentage_rate = annual_percentage_rate
        self.paypal_reference_id_type = paypal_reference_id_type
        self.shipping_discount_amount = shipping_discount_amount
        self.credit_transactional_fee = credit_transactional_fee
        self._transaction_updated_date = self._json_response.get('transaction_updated_date', kwargs.get('transaction_updated_date'))
        self._transaction_initiation_date = self._json_response.get('transaction_initiation_date', kwargs.get('transaction_initiation_date'))
    
    @property
    def event_type(self) -> str:
        """Property for the event type based on the code
        
        Returns:
             -- String description of the event type or None
        """
        try:
            return _EVENT_TYPE_MAPPINGS.get(self.transaction_event_code[0:3])
        except:
            return None

    @property
    def event_desc(self) -> str:
        """Property for the event description based on the code
        
        Returns:
             -- String description of the event type or None
        """
        return _EVENT_DESC_MAPPINGS.get(self.transaction_event_code)

    @property
    def transaction_status_enum(self) -> TransactionStatus:
        """Property for the enumeration of this transaction ()
        """
        return _TRANSACTION_STATUS_MAPPING.get(self.transaction_status)

    @property
    def paypal_reference_id_type_enum(self) -> ReferenceIdType:
        """Property for the enumeration of this transaction ()
        """
        return _REFERENCE_ID_MAPPINGS.get(self.paypal_reference_id_type)

    @property
    def protection_eligibility_enum(self) -> ProtectionElegibility:
        """Property for the enumeration of this transaction ()
        """
        try:
            return ProtectionElegibility(int(self.protection_eligibility))
        except:
            return None

    @property
    def transaction_updated_date(self) -> datetime:
        try:
            return dateutil.parser.parse(self._transaction_updated_date) if self._transaction_updated_date else None
        except:
            return None

    @property
    def transaction_initiation_date(self) -> datetime:
        try:
            return dateutil.parser.parse(self._transaction_initiation_date) if self._transaction_initiation_date else None
        except:
            return None

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        args = {**json_data , **{ k : Money.serialize_from_json(v) for k, v in json_data.items() if k in cls._MONEY_TYPES }}
        return cls(**args, json_response = json_data, response_type = response_type)

class PayerInfo(PayPalEntity):
    """Payer info object representation
    """
    
    _PAYPAL_ENTITY_TYPES = { 'payer_name': PaypalName, 'address': PaypalPortableAddress, 'phone_number': PaypalPhoneDetail }

    def __init__(
        self, account_id: str = None, email_address: str = None, 
        phone_number: PaypalPhoneDetail = None, address_status: str = None, 
        payer_status: str = None, payer_name: PaypalName = None, country_code: str = None,
        address: PaypalPortableAddress = None, **kwargs
        ):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.address = address
        self.payer_name = payer_name
        self.account_id = account_id
        self.country_code = country_code
        self.payer_status = payer_status
        self.phone_number = phone_number
        self.email_address = email_address
        self.address_status = address_status

    @property
    def payer_status_enum(self) -> PayerStatusProperty:
        """Payer status enumeration
        
        Returns:
            PayerStatusProperty -- A descriptive enumeration for the payers status.
        """
        stat = None
        if self.payer_status:
            stat = PayerStatusProperty.VERIFIED if self.payer_status == 'Y' else PayerStatusProperty.UNVERIFIED
        return stat

    @property
    def address_status_enum(self) -> PayerStatusProperty:
        """Address status enumeration
        
        Returns:
            PayerStatusProperty -- A descriptive enumeration for the payers address status.
        """
        stat = None
        if self.address_status:
            stat = PayerStatusProperty.VERIFIED if self.address_status == 'Y' else PayerStatusProperty.UNVERIFIED
        return stat

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        special_types = { k : cls._PAYPAL_ENTITY_TYPES[k].serialize_from_json(v) for k,v in json_data.items() if k in cls._PAYPAL_ENTITY_TYPES.keys() }
        args = { **json_data, **special_types }
        return cls(**args, json_response = json_data, response_type = response_type)

class ShippingInfo(PayPalEntity):
    """Shipping info object representation
    """
    _ADDRESS_TYPES = {'address', 'secondary_shipping_address'}

    def __init__(
        self, name: str = None, method: str = None, 
        address: PaypalPortableAddress = None, 
        secondary_shipping_address: PaypalPortableAddress = None,
        **kwargs
        ):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.name = name
        self.method = method
        self.address = address
        self.secondary_shipping_address = secondary_shipping_address
    
    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        args = {**json_data , **{ k : PaypalPortableAddress.serialize_from_json(v) for k, v in json_data.items() if k in cls._ADDRESS_TYPES }}
        return cls(**args, json_response = json_data, response_type = response_type)

class TaxAmount(PayPalEntity):
    """Tax amount object representation.
    """

    def __init__(self, tax_amount: Money, **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.tax_amount = tax_amount
    
    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        return cls(Money.serialize_from_json(json_data['tax_amount']), json_response = json_data, response_type = response_type)

class CheckoutOption(PaypalName):
    """Checkout option object representation.
    """

    def __init__(self, checkout_option_name: str, checkout_option_value: str, **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.checkout_option_name = checkout_option_name
        self.checkout_option_value = checkout_option_value

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        return cls(**json_data, json_response = json_data, response_type = response_type)

class ItemDetail(PayPalEntity):
    """Item detail object representation.
    """

    _MONEY_TYPES = {
        'item_unit_price', 'item_amount', 'discount_amount', 'adjustment_amount', 
        'gift_wrap_amount', 'basic_shipping_amount', 'extra_shipping_amount', 
        'handling_amount', 'insurance_amount', 'total_item_amount'
    }

    _PAYPAL_TYPE_ARRAYS = {
        'tax_amounts': TaxAmount,
        'checkout_options': CheckoutOption
    }

    def __init__(
        self, item_code: str = None, item_name: str = None, item_description: str = None, 
        item_options: str = None, item_quantity: str = None, item_unit_price: Money = None, 
        item_amount: Money = None, discount_amount: Money = None, adjustment_amount: Money = None, 
        gift_wrap_amount: Money = None, tax_percentage: str = None, tax_amounts: List[TaxAmount] = [], 
        basic_shipping_amount: Money = None, extra_shipping_amount: Money = None, handling_amount: Money = None, 
        insurance_amount: Money = None, total_item_amount: Money = None, invoice_number: str = None, 
        checkout_options: List[CheckoutOption] = [], **kwargs
        ):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.item_code = item_code
        self.item_name = item_name
        self.item_description = item_description
        self.item_options = item_options
        self.item_quantity = item_quantity
        self.item_unit_price = item_unit_price
        self.item_amount = item_amount
        self.discount_amount = discount_amount
        self.adjustment_amount = adjustment_amount
        self.gift_wrap_amount = gift_wrap_amount
        self.tax_percentage = tax_percentage
        self.tax_amounts = tax_amounts or []
        self.basic_shipping_amount = basic_shipping_amount
        self.extra_shipping_amount = extra_shipping_amount
        self.handling_amount = handling_amount
        self.insurance_amount = insurance_amount
        self.total_item_amount = total_item_amount
        self.invoice_number = invoice_number
        self.checkout_options = checkout_options or []
        
    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        args = {
            # Regular (primitive) arguments
            **json_data,
            # Serialized Money arguments
            **{ k : Money.serialize_from_json(v) for k, v in json_data.items() if k in cls._MONEY_TYPES },
            # Serialized array arguments
            **{ k : [cls._PAYPAL_TYPE_ARRAYS[k].serialize_from_json(v) for v in json_data[k]] for k in json_data.keys() if k in cls._PAYPAL_TYPE_ARRAYS }
        }
        return cls(**args, json_response = json_data, response_type = response_type)

class CartInfo(PayPalEntity):
    """Cart info object representation
    """
    
    def __init__(self, tax_inclusive: bool = None, paypal_invoice_id: str = None, item_details: List[ItemDetail] = [], **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.tax_inclusive = tax_inclusive
        self.item_details = item_details or []
        self.paypal_invoice_id = paypal_invoice_id
    
    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        items = []
        if 'item_details' in json_data.keys():
            items = [ItemDetail.serialize_from_json(v) for v in json_data['item_details']]        
        return cls(json_data.get('tax_inclusive'), json_data.get('tax_inclusive'), items)

class StoreInfo(PayPalEntity):
    """Store info object representation.
    """

    def __init__(self, store_id: str = None, terminal_id: str = None, **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.store_id = store_id
        self.terminal_id = terminal_id
    
    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        return cls(**json_data, json_response = json_data, response_type = response_type)

class AuctionInfo(PayPalEntity):
    """Auction info object representation
    """

    def __init__(
        self, auction_site: str = None, auction_item_site: str = None, 
        auction_buyer_id: str = None, **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.auction_site = auction_site
        self.auction_item_site = auction_item_site
        self.auction_buyer_id = auction_buyer_id
        self._auction_closing_date = self._json_response.get('auction_closing_date', kwargs.get('auction_closing_date'))
    
    @property
    def auction_closing_date(self) -> datetime:
        try:
            return dateutil.parser.parse(self._auction_closing_date) if self._auction_closing_date else None
        except:
            return None
    
    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        return cls(**json_data, json_response = json_data, response_type = response_type)

class IncentiveDetail(PayPalEntity):
    """Incentive detail object representation
    """

    def __init__(
        self, incentive_type: str = None, incentive_code: str = None, 
        incentive_amount: Money = None, incentive_program_code: str = None, **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.incentive_type = incentive_type
        self.incentive_code  = incentive_code 
        self.incentive_amount = incentive_amount
        self.incentive_program_code = incentive_program_code
    
    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        args = { **json_data }
        if 'incentive_amount' in json_data.keys():
            args['incentive_amount'] = Money.serialize_from_json(json_data['incentive_amount'])
        return cls(**args, json_response = json_data, response_type = response_type)

class TransactionDetails(PayPalEntity):
    """Transaction details obj representation
    """

    _PAYPAL_TYPES = { 
        # The transaction information.
        'transaction_info' : TransactionInfo,

        # The payer information.
        'payer_info' : PayerInfo,

        # The shipping information.
        'shipping_info' : ShippingInfo,

        # The cart information.
        'cart_info' : CartInfo,

        # The store information.
        'store_info' : StoreInfo,

        # The auction information.   
        'auction_info' : AuctionInfo
    }

    def __init__(
        self, transaction_info: TransactionInfo, 
        payer_info: PayerInfo, shipping_info: ShippingInfo, 
        cart_info: CartInfo, store_info: StoreInfo, 
        auction_info: AuctionInfo, **kwargs
        ):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.cart_info = cart_info
        self.store_info = store_info
        self.payer_info = payer_info
        self.auction_info = auction_info
        self.shipping_info = shipping_info
        self.transaction_info = transaction_info

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        args = { k : cls._PAYPAL_TYPES[k].serialize_from_json(v) for k,v in json_data.items() if k in cls._PAYPAL_TYPES and v }
        return cls(**args, json_response = json_data, response_type = response_type)

class TransactionResponse(PayPalEntity):
    """Transaction query response with the main info and details    
    """

    def __init__(self, account_number: str = None, 
    transaction_details: List[TransactionDetails] = [], **kwargs):
        self.account_number = account_number
        self.transaction_details = transaction_details or []
        self.page = self._json_response.get('page', kwargs.get('page'))
        self._end_date = self._json_response.get('end_date', kwargs.get('end_date'))
        self._start_date = self._json_response.get('start_date', kwargs.get('start_date'))
        self.total_pages = self._json_response.get('total_pages', kwargs.get('total_pages'))
        self.total_items = self._json_response.get('total_items', kwargs.get('total_items'))
        self.links = [ActionLink(x['href'], x['rel'], x.get('method', 'GET')) for x in self._json_response.get('links', [])]
        self._last_refreshed_datetime = self._json_response.get('last_refreshed_datetime', kwargs.get('last_refreshed_datetime'))

    @property
    def end_date(self) -> datetime:
        try:
            return dateutil.parser.parse(self._end_date) if self._end_date else None
        except:
            return None

    @property
    def start_date(self) -> datetime:
        try:
            return dateutil.parser.parse(self._start_date) if self._start_date else None
        except:
            return None

    @property
    def last_refreshed_datetime(self) -> datetime:
        try:
            return dateutil.parser.parse(self._last_refreshed_datetime) if self._last_refreshed_datetime else None
        except:
            return None

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        args = { **json_data }
        if 'transaction_details' in json_data.keys():
            args['transaction_details'] = [ TransactionDetails.serialize_from_json(v) for v in json_data['transaction_details'] ]
        return cls(**args, json_response = json_data, response_type = response_type)
