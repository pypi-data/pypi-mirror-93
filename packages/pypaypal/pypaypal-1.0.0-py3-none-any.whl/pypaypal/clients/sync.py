"""
    Sync (Transaction) resource clients for the paypal resource group.

    Resource docs & Reference: https://developer.paypal.com/docs/api/sync/v1/

    It seems that paypal renamed this endpoint in the docs to: https://developer.paypal.com/docs/api/transaction-search/v1/
"""

import json

from enum import Enum
from datetime import datetime
from typing import TypeVar, Set

from pypaypal.clients.base import ClientBase, ActionLink

from pypaypal.http import ( 
    parse_url,
    PayPalSession,
    LEGACY_LIVE_API_BASE_URL, 
    LEGACY_SANDBOX_API_BASE_URL 
)

from pypaypal.entities.base import ( 
    Money, 
    DateRange,
    AmountRange,
    ResponseType,
    PaypalApiResponse
)

from pypaypal.entities.sync import TransactionStatus, TransactionResponse

"""
    Base Resource Live URL
"""
_LIVE_RESOURCE_BASE_URL = parse_url(LEGACY_LIVE_API_BASE_URL, 'reporting', 'transactions')

"""
    Base Resource Sandbox URL
"""
_SANDBOX_RESOURCE_BASE_URL = parse_url(LEGACY_SANDBOX_API_BASE_URL, 'reporting', 'transactions')

T = TypeVar('T', bound = 'SyncClient')

_TRANSACTION_STRING_VALUES = [ 
    'transaction_info', 'payer_info', 'shipping_info', 'auction_info', 
    'cart_info', 'incentive_info', 'store_info', 'all' 
]

class TransactionField(Enum):
    #  The transaction information. 
    TRANSACTION_INFO = 1
    #  The payer information. 
    PAYER_INFO = 2
    #  The shipping information.
    SHIPPING_INFO = 3
    #  The auction information.
    AUCTION_INFO = 4
    #  The cart information.
    CART_INFO = 5
    #  An array of incentive detail objects.
    INCENTIVE_INFO = 6
    #  The store information.
    STORE_INFO = 7
    # All
    ALL = 8

    def as_parameter(self) -> str:
        return _TRANSACTION_STRING_VALUES[self.value - 1]

class PaymentInsrtumentType(Enum):
    # To query for a debit card transaction with a corresponding value.
    DEBITCARD = 1
    # To query for a direct credit card transaction with a corresponding value.
    CREDITCARD = 2

class SyncClient(ClientBase):
    """Sync (Transactio reporting) resource client
    """
    def __init__(self, base_url: str, session: PayPalSession):
        super().__init__(base_url, session)
    
    def list_transactions(
        self, *, page: int = 1, page_size: int = 100,  fields: Set[TransactionField] = { TransactionField.TRANSACTION_INFO },
        transaction_id: str = None, transaction_type: str = None, transaction_status: TransactionStatus = None, 
        transaction_amount: AmountRange = None, date: DateRange = None, payment_instrument_type: PaymentInsrtumentType = None, 
        store_id: str = None, terminal_id: str = None, balance_affecting_records_only: bool = True
    ) -> PaypalApiResponse[TransactionResponse]:
        """[summary]
        
        Keyword Arguments:
            page {int} -- Curent page (default: {1})
            page_size {int} -- page size max 500 (default: {100})
            fields {Set[TransactionField]} -- fields to include in the report (default: {{ TransactionField.TRANSACTION_INFO }})
            transaction_id {str} -- transaction ids (note: they are not unique) (default: {None})
            transaction_type {str} -- transaction event code (default: {None})
            transaction_status {TransactionStatus} -- transaction status for the query (default: {None})
            transaction_amount {AmountRange} -- transaction amount range filter (default: {None})
            date {DateRange} -- transaction date range filter (default: {None})
            payment_instrument_type {PaymentInsrtumentType} -- creditcard or debitcard payment (None for both) (default: {None})
            store_id {str} --  Filters the transactions in the response by a store ID.  (default: {None})
            terminal_id {str} -- Filters the transactions in the response by a terminal ID.  (default: {None})
            balance_affecting_records_only {bool} --  flag to include only balance-impacting or all transactions (default: {True})
        
        Returns:
            PaypalApiResponse[TransactionResponse] -- Page with all the desired transaction info
        """
        parameters = {
            'page': page, 'store_id': store_id, 'page_size': page_size,
            'terminal_id': terminal_id, 'transaction_id': transaction_id,
            'transaction_type': transaction_type, 'transaction_status': transaction_status,            
            'balance_affecting_records_only': balance_affecting_records_only
        }

        parameters = { k:v for k,v in parameters.items() if v != None }

        if date:
            parameters['end_date'] = date.end
            parameters['start_date'] = date.start
            
        if payment_instrument_type:
            parameters['payment_instrument_type'] = payment_instrument_type.name
        
        if transaction_amount:
            # Both currency codes should be equal in this request
            parameters['transaction_currency'] = transaction_amount.lower_amount.currency_code            
            parameters['transaction_amount'] = f'{transaction_amount.lower_amount} TO {transaction_amount.upper_amount}'\
                .replace('.', '')
            
        if fields:
            f = ','.join([x.as_parameter() for x in fields])
            if TransactionField.ALL in fields or len(fields) == 7:
                f = TransactionField.ALL.as_parameter()
            parameters['fields'] = f

        api_response = self._session.get(self._base_url, parameters)

        if api_response.status_code // 100 != 2:
            return PaypalApiResponse.error(api_response)

        return PaypalApiResponse.success(api_response, TransactionResponse.serialize_from_json(api_response.json()))

    @classmethod
    def for_session(cls: T, session: PayPalSession) -> T:
        """Creates a client from a given paypal session
        
        Arguments:
            cls {T} -- class reference
            session {PayPalSession} -- the paypal session
        
        Returns:
            T -- an instance of Dispute client with the right configuration by session mode
        """
        base_url = _LIVE_RESOURCE_BASE_URL if session.session_mode.is_live() else _SANDBOX_RESOURCE_BASE_URL
        return cls(base_url, session)