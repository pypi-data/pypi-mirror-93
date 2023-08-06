"""
    Module with all payout related entities 
"""

from enum import Enum
from datetime import datetime
from typing import Type, List

import dateutil.parser
from pypaypal.errors import PayPalErrorDetail

from pypaypal.entities.base import ( 
    T, 
    ActionLink, 
    PaypalName,
    PayPalEntity, 
    ResponseType, 
    PaypalPhoneDetail,
    # Money is imported as currency to follow the docs naming conv.
    Money as Currency
)

class PayoutRecipientType(Enum):
    # Unencrypted email. Value is a string of up to 127 single-byte characters
    EMAIL = 1
    # The unencrypted phone number. Not supported in sandbox mode.
    PHONE = 2
    # Encrypted PayPal account number.
    PAYPAL_ID = 3

class RecipientWallet(Enum):
    # PayPal Wallet.
    PAYPAL = 1
    # Venmo Wallet.
    VENMO = 2

class BatchStatus(Enum):
    # Payout requests was denied, not processed.
    DENIED = 1 
    # Payout requests received and will be processed soon.
    PENDING = 2 
    # Payout requests received and being processed.
    PROCESSING = 3 
    # Payout batch was processed and completed.
    SUCCESS = 4 
    # The payouts file was cancelled by the sender.
    CANCELED = 5 

class TransactionStatus(Enum):
    # Funds have been credited to the recipient’s account.
    SUCCESS = 1
    # This payout request has failed, so funds were not deducted from the sender’s account.
    FAILED = 2
    # The payout request was received and will be processed.
    PENDING = 3
    # The recipient for this payout does not have a PayPal account. 
    # A link to sign up for a PayPal account was sent to the recipient. 
    # However, if the recipient does not claim this payout within 30 days, 
    # the funds are returned to your account.
    UNCLAIMED = 4
    # The recipient has not claimed this payout, 
    # so the funds have been returned to your account.
    RETURNED = 5
    # This payout request is being reviewed and is on hold.
    ONHOLD = 6
    # This payout request has been blocked.
    BLOCKED = 7
    # This payout request was refunded.
    REFUNDED = 8
    # This payout request was reversed.
    REVERSED = 9

class SenderBatchHeader(PayPalEntity):
    """ A sender-provided payout header for a payout request.
    """

    def __init__(
        self, sender_batch_id: str, recipient_type: str, 
        email_subject: str, email_message: str, note: str, **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.note = note
        self.email_subject = email_subject
        self.email_message = email_message
        self.recipient_type = recipient_type
        self.sender_batch_id = sender_batch_id

    @property
    def recipient_type_enum(self) -> PayoutRecipientType:
        try:
            return PayoutRecipientType[self.recipient_type] if self.recipient_type else None
        except:
            return None

    @classmethod
    def create(
        cls, sender_batch_id: str, *, email_subject: str, 
        email_message: str, recipient_type: str = None, note: str = None) -> 'SenderBatchHeader':
        return cls(sender_batch_id, recipient_type, email_subject, email_message, note)
    
    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        return cls(
            json_data.get('sender_batch_id'), json_data.get('recipient_type'), json_data.get('email_subject'), 
            json_data.get('email_message'), json_data.get('note'), json_response= json_data, 
            response_type = response_type
        )

class PayoutErrorDetails(PayPalEntity):
    """Payout error details object representation
    """
    def __init__(self, field: str, issue: str, **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.field = field
        self.issue = issue
        self.links = [ActionLink(x['href'], x['rel'], x.get('method', 'GET')) for x in self._json_response.get('links', [])]

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        return cls(json_data.get('field'), json_data.get('issue'), json_response = json_data, response_type= response_type)

class PayoutError(PayPalErrorDetail):
    """Payout error object representation
    """
    
    def __init__(self, name: str, message: str, info_link: str, **kwargs):
        super().__init__(kwargs.get('json_response', dict()), name, message, info_link)
        self._payout_error_details = self._json_response.get('payout_error_details')
    
    @property
    def payout_error_details(self) -> List[PayoutErrorDetails]:
        try:
            return PayoutErrorDetails.serialize_from_json(self._payout_error_details) if self._payout_error_details else []
        except:
            return []

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict) -> T:
        return cls(
            json_data.get('name'), json_data.get('message'), json_data.get('information_link'), 
            json_response = json_data
        )

class PayoutHeader(PayPalEntity):
    """Payout header object representation
    """
    def __init__(
        self, payout_batch_id: str, batch_status: str, 
        sender_batch_header: SenderBatchHeader, errors: PayPalErrorDetail, **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.errors = errors
        self.batch_status = batch_status
        self.payout_batch_id = payout_batch_id
        self.sender_batch_header = sender_batch_header
        self._time_created = self._json_response.get('time_created', kwargs.get('time_created'))

    @property
    def status_enum(self) -> BatchStatus:
        try:
            return BatchStatus[self.status] if self.status else None
        except:
            return None

    @property
    def time_created(self) -> datetime:
        try:
            return dateutil.parser.parse(self._time_created) if self._time_created else None
        except:
            return None
    
    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        errors, sender_batch_header = None, None

        if 'errors' in json_data.keys():
            errors = PayoutError.serialize_from_json(json_data['errors'])
        if 'sender_batch_header' in json_data.keys():
            sender_batch_header = SenderBatchHeader.serialize_from_json(json_data['sender_batch_header'], response_type)
        
        return cls(
            json_data.get('payout_batch_id'), json_data.get('batch_status'), 
            sender_batch_header, errors, json_response = json_data, response_type = response_type
        )

class PayoutItemDetail(PayPalEntity):
    """Payout item detail object representation
    """

    def __init__(
        self, recipient_type: str, amount: Currency, note: str, 
        receiver: str, sender_item_id: str, recipient_name: PaypalName, 
        recipient_wallet: str, **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.note = note
        self.amount = amount
        self.receiver = receiver
        self.recipient_type = recipient_type
        self.sender_item_id = sender_item_id
        self.recipient_name  = recipient_name
        self.recipient_wallet = recipient_wallet
    
    @property
    def recipient_wallet_enum(self) -> RecipientWallet:
        try:
            return RecipientWallet[self.recipient_wallet] if self.recipient_wallet else RecipientWallet.PAYPAL
        except:
            return RecipientWallet.PAYPAL
    
    @classmethod
    def create(
        cls, *, amount: Currency, receiver: str, 
        recipient_type: str = None, note: str = None, 
        sender_item_id: str = None, recipient_name: PaypalName = None, 
        recipient_wallet: RecipientWallet = RecipientWallet.PAYPAL) -> 'PayoutItemDetail':        
        return cls(recipient_type, amount, note, receiver, sender_item_id, recipient_name, recipient_wallet.name)
    
    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        amount, recipient_name = None, None

        if 'amount' in json_data.keys():
            amount = Currency.serialize_from_json(json_data['amount'], response_type)
        if 'recipient_name' in json_data.keys():
            recipient_name = PaypalName.serialize_from_json(json_data['recipient_name'], response_type)

        return cls(
            json_data.get('recipient_type'), amount, json_data.get('note'), 
            json_data.get('receiver'), json_data.get('sender_item_id'), recipient_name,
            json_data.get('recipient_wallet'), json_response = json_data, response_type = response_type
        )

class CurrencyConversion(PayPalEntity):
    """Currency conversion object representation
    """
    def __init__(self, from_amount: Currency, to_amount: Currency, exchange_rate: str, **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.to_amount = to_amount
        self.from_amount = from_amount
        self.exchange_rate = exchange_rate

    @classmethod
    def create(cls, *, from_amount: Currency, to_amount: Currency, exchange_rate: str = None) -> 'CurrencyConversion':
        return cls(from_amount, to_amount, exchange_rate)
    
    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        from_amount, to_amount = None, None

        if 'to_amount' in json_data.keys():
            to_amount = Currency.serialize_from_json(json_data['to_amount'], response_type)
        if 'from_amount' in json_data.keys():
            from_amount = Currency.serialize_from_json(json_data['from_amount'], response_type)

        return cls(from_amount, to_amount, json_data.get('exchange_rate'))

class PayoutItem(PayPalEntity):
    """Payout item object representation
    """

    def __init__(
        self, payout_item_id: str, transaction_id: str, activity_id: str, 
        transaction_status: str, payout_item_fee: Currency, payout_batch_id: str, 
        sender_batch_id: str, payout_item: PayoutItemDetail, currency_conversion: CurrencyConversion, 
        errors: PayoutError, recipient_type: str, amount: Currency, note: str, receiver: str, 
        sender_item_id: str, recipient_wallet: str, alternate_notification_method: PaypalPhoneDetail, **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.note = note
        self.errors = errors
        self.amount = amount
        self.receiver = receiver
        self.activity_id = activity_id
        self.payout_item = payout_item
        self.recipient_type = recipient_type
        self.payout_item_id = payout_item_id
        self.transaction_id = transaction_id
        self.sender_item_id = sender_item_id
        self.payout_item_fee = payout_item_fee
        self.payout_batch_id = payout_batch_id
        self.sender_batch_id = sender_batch_id
        self.recipient_wallet = recipient_wallet
        self.transaction_status = transaction_status
        self.currency_conversion = currency_conversion
        self.alternate_notification_method = alternate_notification_method
        self._time_created = self._json_response.get('time_created', kwargs.get('time_created'))
        self.links = [ActionLink(x['href'], x['rel'], x.get('method', 'GET')) for x in self._json_response.get('links', [])]

    @property
    def time_created(self) -> datetime:
        try:
            return dateutil.parser.parse(self._time_created) if self._time_created else None
        except:
            return None
    
    @classmethod
    def create(
        cls, *, amount: Currency, receiver: str, payout_item_id: str,
        payout_batch_id: str, payout_item: PayoutItemDetail,
        transaction_id: str = None, activity_id: str = None,
        transaction_status: TransactionStatus = None, payout_item_fee: Currency = None,
        sender_batch_id: str = None,  currency_conversion: CurrencyConversion = None,
        recipient_type: PayoutRecipientType = None, note: str = None, sender_item_id: str = None,
        recipient_wallet: RecipientWallet = RecipientWallet.PAYPAL, alternate_notification_method: PaypalPhoneDetail = None) -> 'PayoutItem':

        return cls(
            payout_item_id, transaction_id,activity_id, transaction_status.name, payout_item_fee, payout_batch_id,
            sender_batch_id, payout_item, currency_conversion, None, recipient_type.name, amount, note, receiver, sender_item_id,
            recipient_wallet.name, alternate_notification_method
        )

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        errors, amount, payout_item, payout_item_fee, currency_conversion, alternate_notification_method = None, None, None, None, None, None
        
        if 'errors' in json_data.keys():
            errors = PayoutError.serialize_from_json(json_data['errors'])
        if 'amount' in json_data.keys():
            amount = Currency.serialize_from_json(json_data['amount'], response_type)
        if 'payout_item' in json_data.keys():
            payout_item = PayoutItemDetail.serialize_from_json(json_data['payout_item'], response_type)
        if 'payout_item_fee' in json_data.keys():
            payout_item_fee = Currency.serialize_from_json(json_data['payout_item_fee'], response_type)
        if 'currency_conversion' in json_data.keys():
            currency_conversion = CurrencyConversion.serialize_from_json(json_data['currency_conversion'], response_type)
        if 'alternate_notification_method' in json_data.keys():
            alternate_notification_method = PaypalPhoneDetail.serialize_from_json(json_data['alternate_notification_method'], response_type)
        
        return cls(
            json_data.get('payout_item_id'), json_data.get('transaction_id'), json_data.get('activity_id'), json_data.get('transaction_status'), payout_item_fee,
            json_data.get('payout_batch_id'), json_data.get('sender_batch_id'), payout_item, currency_conversion, errors, json_data.get('recipient_type'), 
            amount, json_data.get('note'), json_data.get('receiver'), json_data.get('sender_item_id'), json_data.get('recipient_wallet'), 
            alternate_notification_method, json_response = json_data, response_type = response_type
        )

class PagedPayout(PayPalEntity):
    """Paged payout information (Payout Header + Paged Items).
    """

    def __init__(self, batch_header: PayoutHeader, items: List[PayoutItem], **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.items = items 
        self.batch_header = batch_header
        self.links = [ActionLink(x['href'], x['rel'], x.get('method', 'GET')) for x in self._json_response.get('links', [])]
    
    @property
    def read_link(self) -> ActionLink:
        """Retrieves a link to read this entity details.
        
        Returns:
            ActionLink -- The link for requesting the information to the API.
        """
        return next(filter(lambda x: x.rel == 'self', self.links), None)

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        batch_header, items = None, None
        
        if 'batch_header' in json_data.keys():
            batch_header = PayoutHeader.serialize_from_json(json_data['batch_header'], response_type)
        if 'items' in json_data.keys():
            items = [ PayoutItem.serialize_from_json(json_data[x]) for x in json_data['items'] ]

        return cls(batch_header, items, json_response = json_data, response_type = response_type)
    