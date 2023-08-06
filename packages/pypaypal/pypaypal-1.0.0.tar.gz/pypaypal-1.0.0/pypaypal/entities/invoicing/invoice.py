"""
    Module with invoice related entities
"""

from datetime import datetime
from typing import Type, List

import dateutil.parser

from pypaypal.entities.base import ( 
    T, 
    Tax,
    Item,
    Refund,
    Discount,
    DateRange,
    ActionLink, 
    PaypalName,
    AmountRange, 
    PayPalEntity, 
    ResponseType, 
    Money, 
    RecipientInfo,
    PaypalPhoneDetail,
    PaypalPortableAddress
)

from pypaypal.entities.invoicing.template import Template

class AggregatedDiscount(PayPalEntity):
    """Aggregated discount object representation
    """
    def __init__(self, invoice_discount: Discount, item_discount: Money, **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.item_discount = item_discount
        self.invoice_discount = invoice_discount
    
    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        itm_disc = Discount.serialize_from_json(json_data['item_discount'])
        inv_disc = Discount.serialize_from_json(json_data['invoice_discount'])

        return cls(inv_disc, itm_disc, json_response= json_data, response_type = response_type)

class ShippingCost(PayPalEntity):
    """Shipping Cost object representation
    """
    def __init__(self, tax: Tax, amount: Money, **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.tax = tax
        self.amount = amount

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        tax = Discount.serialize_from_json(json_data['tax'])
        amt = Money.serialize_from_json(json_data['amount'])
        return cls(tax, amt, json_response= json_data, response_type = response_type)

class CustomAmount(PayPalEntity):
    """Custom amount object representation
    """
    def __init__(self, label: str, amount: Money, **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.label = label
        self.amount = amount

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        amt = Money.serialize_from_json(json_data['amount'])
        return cls(json_data['label'], amt, json_response= json_data, response_type = response_type)

class AmountWithBreakdown(PayPalEntity):
    """Amount with breakdown object representation
    """

    def __init__(self, item_total: Money, discount: AggregatedDiscount, tax_total: Money, shipping: ShippingCost, custom: CustomAmount, **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))        
        self.item_total = item_total
        self.discount = discount
        self.tax_total = tax_total
        self.shipping = shipping
        self.custom = custom

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        item_total, discount, tax_total, shipping, custom = None, None, None, None, None
        
        if 'item_total' in json_data.keys():
            item_total = Money.serialize_from_json(json_data['item_total'])
        if 'discount' in json_data.keys():
            discount = AggregatedDiscount.serialize_from_json(json_data['discount'])
        if 'tax_total' in json_data.keys():
            tax_total = Money.serialize_from_json(json_data['tax_total'])
        if 'shipping' in json_data.keys():
            shipping = ShippingCost.serialize_from_json(json_data['shipping'])
        if 'custom' in json_data.keys():
            custom = CustomAmount.serialize_from_json(json_data['custom'])

        return cls(item_total, discount, tax_total, shipping, custom, json_response= json_data, response_type = response_type)

class InvoicePaymentTerm(PayPalEntity):
    """Invoice payment term object representation
    """

    def __init__(self, term_type: str, due_date: str, **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self._due_date = due_date
        self.term_type = term_type
    
    @property
    def due_date(self) -> datetime:
        try:
            return dateutil.parser.parse(self._due_date) if self._due_date else None
        except:
            return None

    def to_dict(self) -> dict:
        ret = super().to_dict()
        ret['due_date'] = ret.pop('_due_date', None)
        return ret

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        return cls(
            json_data['term_type'], json_data['due_date'], json_response= json_data, response_type = response_type
        )

    @classmethod
    def create(cls, term_type: str, due_date: datetime):
        return cls(term_type, due_date.strftime('%Y-%m-%d'))

class FileReference(PayPalEntity):
    """File reference object representation
    """

    def __init__(self, file_id: str, reference_url: str, content_type: str, size: str, **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.id = file_id
        self.reference_url = reference_url
        self.content_type = content_type
        self.size = size
        default_time = datetime.now().strftime('%Y-%m-%dT%H:%M:%s')
        self._create_time = self._json_response.get('create_time', kwargs.get('create_time', default_time))

    @property
    def create_time(self) -> datetime:
        try:
            return dateutil.parser.parse(self._create_time) if self._create_time else None
        except:
            return None

    def to_dict(self) -> dict:
        ret = super().to_dict()
        ret['create_time'] = ret.pop('_create_time', None)
        return ret

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        return cls(
            json_data.get('id'), json_data.get('reference_url'), json_data.get('content_type'),
            json_data.get('size'), json_response= json_data, response_type = response_type
        )
    
    @classmethod
    def create(cls, file_id: str, reference_url: str, content_type: str, size: str, creation: datetime = datetime.now()) -> 'FileReference':
        return cls(file_id, reference_url, content_type, size, create_time = creation.strftime('%Y-%m-%dT%H:%M:%s'))

class MetaData(PayPalEntity):
    """Template audit metadata.
    """

    def __init__(self, created_by: str, last_updated_by: str, **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.created_by = created_by
        self.last_updated_by = last_updated_by
        default_time = datetime.now().strftime('%Y-%m-%dT%H:%M:%s')
        self._create_time = self._json_response.get('create_time', kwargs.get('create_time', default_time))
        self._last_update_time = self._json_response.get('last_update_time', kwargs.get('last_update_time', default_time))

    @property
    def create_time(self) -> datetime:
        try:
            return dateutil.parser.parse(self._create_time) if self._create_time else None
        except:
            return None

    @property
    def last_updated_time(self) -> datetime:
        try:
            return dateutil.parser.parse(self._last_updated_time) if self._last_updated_time else None
        except:
            return None

    def to_dict(self) -> dict:
        ret = super().to_dict()
        ret['create_time'] = ret.pop('_create_time', None)
        ret['last_updated_time'] = ret.pop('_last_updated_time', None)
        return ret

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        return cls(
            json_data.get('created_by'), json_data.get('last_updated_by'), json_response= json_data, response_type = response_type
        )

    @classmethod
    def create(cls, created_by: str, last_updated_by: str) -> 'MetaData':
        creation = datetime.now().strftime('%Y-%m-%dT%H:%M:%s')
        
        return cls(
            created_by, last_updated_by, 
            created_time = creation, last_update_time = creation
        )

class InvoiceDetail(PayPalEntity):
    """Invoice detail object representation
    """

    def __init__(
        self, currency_code: str, invoice_number: str, metadata: MetaData,
        payment_term: InvoicePaymentTerm=None, attachments: List[FileReference]= [],
         **kwargs
    ):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.metadata = metadata
        self.payment_term = payment_term
        self.currency_code = currency_code
        self.invoice_number = invoice_number
        self.attachments = attachments or []
        self.note = self._json_response.get('note', kwargs.get('note'))
        self.memo = self._json_response.get('memo', kwargs.get('memo'))
        self.reference = self._json_response.get('reference', kwargs.get('reference'))        
        self._invoice_date = self._json_response.get('invoice_date', kwargs.get('invoice_date'))
        self.terms_and_conditions = self._json_response.get('terms_and_conditions', kwargs.get('terms_and_conditions'))

    @property
    def invoice_date(self) -> datetime:
        try:
            return dateutil.parser.parse(self._invoice_date) if self._invoice_date else None
        except:
            return None

    def to_dict(self) -> dict:
        ret = super().to_dict()
        ret['invoice_date'] = ret.pop('_invoice_date', None)
        return ret

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        metadata, payment_term, attachments = None, None, []

        if 'metadata' in json_data.keys():
            metadata =  MetaData.serialize_from_json(json_data['metadata'], response_type)        
        if 'payment_term' in json_data.keys():
            payment_term = InvoicePaymentTerm.serialize_from_json(json_data['payment_term'], response_type)
        
        if 'attachments' in json_data.keys():
            attachments = [FileReference.serialize_from_json(x, response_type) for x in json_data['attachments']]

        return cls(
            json_data['currency_code'], json_data['invoice_number'], metadata, 
            payment_term, attachments, json_response= json_data, response_type = response_type
        )
    
    @classmethod
    def create(
        cls, currency_code: str, invoice_number: str, metadata: MetaData, *, 
        payment_term: InvoicePaymentTerm=None, attachments: List[FileReference]= [],
        note:str = None, memo:str = None, reference:str = None, invoice_date: datetime = None, 
        terms_and_conditions: str = None
    ):
        return cls(
            currency_code, invoice_number, metadata, payment_term, 
            attachments or [], note = note, memo = memo, reference = reference, 
            invoice_date = invoice_date, terms_and_conditions = terms_and_conditions
        )

class InvoicerInfo(PayPalEntity):
    """Invoicer info object representation
    """

    def __init__(self, business_name: str, name: PaypalName = None, address : PaypalPortableAddress = None, phones: List[PaypalPhoneDetail] = None, **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.name = name
        self.phones = phones
        self.address = address
        self.business_name = business_name
        self.tax_id = self._json_response.get('tax_id', kwargs.get('tax_id'))
        self.website = self._json_response.get('website', kwargs.get('website'))
        self.logo_url = self._json_response.get('logo_url', kwargs.get('logo_url'))
        self.additional_notes = self._json_response.get('additional_notes', kwargs.get('additional_notes'))

    def to_dict(self) -> dict:
        ret = super().to_dict()        
        if self.phones:
            ret['phones'] = [ x.to_dict() for x in self.phones ]
        return ret

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        address, name, phones = None, None, []
        
        if 'name' in json_data.keys():
            name = PaypalName.serialize_from_json(json_data['name'], response_type)
        
        if 'address' in json_data.keys():
            address = PaypalPortableAddress.serialize_from_json(json_data['address'], response_type)

        if 'phones' in json_data.keys():
            phones = [PaypalPhoneDetail.serialize_from_json(x, response_type) for x in json_data['phones']]
        
        return cls(
            json_data.get('business_name'), name, address, phones, json_response= json_data, response_type = response_type
        )

    @classmethod
    def create(
        cls, business_name, *, name: PaypalName = None, 
        address : PaypalPortableAddress = None, phones: List[PaypalPhoneDetail] = None, 
        tax_id: str = None, website: str = None, logo_url: str = None, additional_notes: str = None 
    ):        
        return cls(
            business_name, name, address, phones, 
            tax_id = tax_id, website = website, logo_url = logo_url, 
            additional_notes = additional_notes
        )
    
class PartialPayment(PayPalEntity):
    """Partial payment object representation
    """
    
    def __init__(self, minimum_amount_due: Money, allow_partial_payment: bool, **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.minimum_amount_due = minimum_amount_due
        self.allow_partial_payment = allow_partial_payment

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        amount = Money.serialize_from_json(json_data['minimum_amount_due'])
        return cls(amount, json_data.get('allow_partial_payment'), json_response= json_data, response_type = response_type)

    @classmethod
    def create(cls, minimum_amount_due: Money, allow_partial_payment: bool = False):
        return cls(minimum_amount_due, allow_partial_payment)

class InvoiceConfiguration(PayPalEntity):
    """Invoice configuration object representation
    """

    def __init__(self, template_id: str, tax_calc_after_discount: bool, tax_inclusive: bool, allow_tip: bool, partial_payment: PartialPayment=None, **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.allow_tip = allow_tip
        self.template_id = template_id
        self.tax_inclusive = tax_inclusive
        self.partial_payment = partial_payment
        self.tax_calc_after_discount = tax_calc_after_discount

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        partial_payment = PartialPayment.serialize_from_json(json_data['partial_payment']) if 'partial_payment' in json_data.keys() else None

        return cls(
            json_data.get('template_id'), json_data.get('tax_calc_after_discount'), json_data.get('tax_inclusive'),
            json_data.get('allow_tip'), partial_payment, json_response= json_data, response_type = response_type
        )
    
    @classmethod
    def create(
        cls, *, template_id: str = None, tax_calc_after_discount: bool = True, 
        tax_inclusive: bool = False, allow_tip: bool = False, partial_payment: PartialPayment=None
    ):
        return cls(template_id, tax_calc_after_discount, tax_inclusive, allow_tip, partial_payment)

class AmountSummaryDetail(PayPalEntity):
    """Amount sumary object representation
    """

    def __init__(self, currency_code: str, value: str, breakdown: AmountWithBreakdown, **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.value = value
        self.currency_code = currency_code
        self.breakdown = breakdown

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        breakdown = AmountWithBreakdown.serialize_from_json(json_data['breakdown'], response_type)
        return cls(json_data['currency_code'], json_data['value'], breakdown, json_response= json_data, response_type = response_type)
    
    @classmethod
    def create(cls, currency_code: str, value: str, breakdown: AmountWithBreakdown) -> 'AmountSummaryDetail':
        return cls(currency_code, value, breakdown)

class PaymentDetail(PayPalEntity):
    """Payment object representation for invoice draft
    """
    def __init__(self, pd_type: str, payment_id: str, method: str, amount: Money = None, shipping_info: ShippingCost= None, **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.type = pd_type
        self.method = method
        self.amount = amount
        self.payment_id = payment_id
        self.shipping_info = shipping_info
        self.note = self._json_response.get('note', kwargs.get('note'))
        self._payment_date = self._json_response.get('payment_date', kwargs.get('payment_date'))

    @property
    def payment_date(self) -> datetime:
        try:
            return dateutil.parser.parse(self._payment_date) if self._payment_date else None
        except:
            return None

    def to_dict(self) -> dict:
        ret = super().to_dict()
        ret['payment_date'] = ret.pop('_payment_date', None)
        return ret

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        amount, shipping = None, None
        
        if 'amount' in json_data.keys():
            amount = Money.serialize_from_json(json_data['amount'])
        if 'shipping_info' in json_data.keys():
            shipping = ShippingCost.serialize_from_json(json_data['shipping_info'])

        return cls(json_data['pd_type'], json_data['payment_id'], json_data['method'], 
                    amount, shipping, json_response= json_data, response_type = response_type
            )
        
    @classmethod
    def create(cls, *, payment_id: str, method: str, note: str, payment_date: datetime, amount: Money, shipping_info: ShippingCost) -> T:
        return cls(None, payment_id, method, amount, shipping_info, note = note, payment_date = payment_date.strftime('%Y-%m-%d'))

class InvoicePayment(PayPalEntity):
    """Payment object representation for invoice draft
    """
    def __init__(self, paid_amount: Money, transactions: List[PaymentDetail], **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.paid_amount = paid_amount
        self.transactions = transactions

    def to_dict(self) -> dict:
        ret = super().to_dict()
        if self.transactions:
            ret['transactions'] = [ x.to_dict() for x in self.transactions ]
        return ret

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        paid_amount, transactions = None, list()

        if 'paid_amount' in json_data.keys():
            paid_amount = Money.serialize_from_json(json_data['paid_amount'], response_type)        
        if 'transactions' in json_data.keys():
            transactions = [PaymentDetail.serialize_from_json(x, response_type) for x in json_data['transactions']]
        
        return cls(paid_amount, transactions, json_response= json_data, response_type = response_type)

class Invoice(PayPalEntity):
    """Object representation for a paypal invoice
    """    
    def __init__(
        self, id:str, detail: InvoiceDetail, invoicer: InvoicerInfo, primary_recipients: List[RecipientInfo], 
        items: List[Item], configuration: InvoiceConfiguration, amount: Money, payments: List[InvoicePayment], 
        refunds: List[Refund], due_amount: Money = None, gratuity: Money = None, **kwargs
    ):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.id = id
        self.detail = detail
        self.invoicer = invoicer
        self.primary_recipients = primary_recipients
        self.items = items
        self.configuration = configuration
        self.amount = amount
        self.payments = payments
        self.refunds = refunds
        self.gratuity = gratuity
        self.due_amount = due_amount
        self.status = self._json_response.get('status', kwargs.get('status'))
        self.additional_recipients = self._json_response.get('additional_recipients', kwargs.get('additional_recipients'))
        self.links = [ActionLink(x['href'], x['rel'], x.get('method', 'GET')) for x in self._json_response.get('links', [])]

    @property
    def read_link(self) -> ActionLink:
        """Retrieves a link to read this entity details.
        
        Returns:
            ActionLink -- The link for requesting the information to the API.
        """
        return next(filter(lambda x: x.rel == 'self', self.links), None)

    @property
    def send_link(self) -> ActionLink:
        """Retrieves a link to send this draft and creating an invoice from it.
        
        Returns:
            ActionLink -- The link to execute the API action.
        """
        return next(filter(lambda x: x.rel == 'send', self.links), None)

    @property
    def replace_link(self) -> ActionLink:
        """Retrieves a link to replace (update) this draft.
        
        Returns:
            ActionLink -- The link to execute the API action.
        """
        return next(filter(lambda x: x.rel == 'replace', self.links), None)

    @property
    def delete_link(self) -> ActionLink:
        """Retrieves a link to delete this draft.
        
        Returns:
            ActionLink -- The link to execute the API action.
        """
        return next(filter(lambda x: x.rel == 'delete', self.links), None)

    @property
    def record_payment_link(self) -> ActionLink:
        """Retrieves a link to record a payment on this draft.
        
        Returns:
            ActionLink -- The link to execute the API action.
        """
        return next(filter(lambda x: x.rel == 'record-payment', self.links), None)

    @property
    def gen_qr_code_link(self) -> ActionLink:
        """Retrieves a link to generate a qr-code for this draft.
        
        Returns:
            ActionLink -- The link to execute the API action.
        """
        return next(filter(lambda x: x.rel == 'qr-code', self.links), None)

    def to_dict(self) -> dict:
        ret = super().to_dict()        
        if self.items:
            ret['items'] = [ x.to_dict() for x in self.items ]
        if self.refunds:
            ret['refunds'] = [ x.to_dict() for x in self.refunds ]
        if self.payments:
            ret['payments'] = [ x.to_dict() for x in self.payments ]
        if self.primary_recipients:
            ret['primary_recipients'] = [ x.to_dict() for x in self.primary_recipients ]
        return ret

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        primary_recipients, items, payments, refunds, templates = [], [], [], [], []
        detail, invoicer, configuration, amount, due_amount, gratuity  = None, None, None, None, None, None

        if 'primary_recipients' in json_data.keys():
            primary_recipients = [RecipientInfo.serialize_from_json(x, response_type) for x in json_data['primary_recipients']]
        if 'items' in json_data.keys():
            items = [Item.serialize_from_json(x, response_type) for x in json_data['items']]
        if 'payments' in json_data.keys():
            payments = [InvoicePayment.serialize_from_json(x, response_type) for x in json_data['payments']]
        if 'refunds' in json_data.keys():
            refunds = [Refund.serialize_from_json(x, response_type) for x in json_data['refunds']]
        
        if 'detail' in json_data.keys():
            detail = InvoiceDetail.serialize_from_json(json_data['detail'], response_type)
        if 'invoicer' in json_data.keys():
            invoicer = InvoicerInfo.serialize_from_json(json_data['invoicer'], response_type)
        if 'configuration' in json_data.keys():
            configuration = InvoiceConfiguration.serialize_from_json(json_data['configuration'], response_type)
        if 'amount' in json_data.keys():
            amount = Money.serialize_from_json(json_data['amount'], response_type)
        if 'gratuity' in json_data.keys():
            gratuity = Money.serialize_from_json(json_data['gratuity'], response_type)
        if 'due_amount' in json_data.keys():
            due_amount = Money.serialize_from_json(json_data['due_amount'], response_type)
        if 'templates' in json_data.keys():
            templates = [ Template.serialize_from_json(x) for x in json_data['templates'] ]
            
        return cls(
            json_data.get('id'), detail, invoicer, primary_recipients, items, configuration, amount,
            payments, refunds, due_amount, gratuity, json_response= json_data, response_type = response_type
        )

    @classmethod
    def create(cls: Type[T], *, detail: InvoiceDetail, invoicer: InvoicerInfo, primary_recipients: List[RecipientInfo], 
        additional_recipients: List[str], items: List[Item], configuration: InvoiceConfiguration, amount: Money, 
        payments: List[InvoicePayment], refunds: List[Refund], due_amount: Money = None, gratuity: Money = None)  -> T:

        add_rep = [{ 'email_address': x} for x in additional_recipients]

        return cls(
            None, detail, invoicer, primary_recipients, items, configuration, amount,
            payments, refunds, due_amount, gratuity, additional_recipients = add_rep
        )

class InvoiceSearchRequest:
    """Search request for invoice queries
    """

    def __init__(
        self, email: str, recipient_first_name: str, recipient_last_name: str,
        recipient_business_name: str, inv_status: List[str], invoice_number: str, reference: str,
        country_code: str, memo: str, total_amount_range: AmountRange, invoice_date_range: DateRange,
        due_date_range: DateRange, payment_date_range: DateRange, creation_date_range: DateRange, archived: bool,
        fields: List[str]
    ):
        self.email = email
        self.recipient_first_name = recipient_first_name
        self.recipient_last_name = recipient_last_name
        self.recipient_business_name = recipient_business_name
        self.inv_status = inv_status
        self.invoice_number = invoice_number
        self.reference = reference
        self.country_code = country_code
        self.memo = memo
        self.total_amount_range = total_amount_range
        self.invoice_date_range     = invoice_date_range
        self.due_date_range = due_date_range
        self.payment_date_range = payment_date_range
        self.creation_date_range = creation_date_range
        self.archived = archived
        self.fields = fields
    
    def to_dict(self) -> dict:
        d = {
            'email' : self.email,
            'recipient_first_name' : self.recipient_first_name,
            'recipient_last_name' : self.recipient_last_name,
            'recipient_business_name' : self.recipient_business_name,
            'inv_status' : self.inv_status,
            'invoice_number' : self.invoice_number,
            'reference' : self.reference,
            'country_code' : self.country_code,
            'memo' : self.memo,
            'total_amount_range' : self.total_amount_range.to_dict(),
            'invoice_date_range' : self.invoice_date_range.to_dict(),
            'due_date_range' : self.due_date_range.to_dict(),
            'payment_date_range' : self.payment_date_range.to_dict(),
            'creation_date_range' : self.creation_date_range.to_dict(),
            'archived' : self.archived,
            'fields' : self.fields
        }

        return { k:v for k,v in d.items() if v != None }
    
    @classmethod
    def create(
        cls, *, email: str = None, recipient_first_name: str = None, recipient_last_name: str = None,
        recipient_business_name: str = None, inv_status: List[str] = None, invoice_number: str = None, reference: str = None,
        country_code: str = None, memo: str = None, total_amount_range: AmountRange = None, invoice_date_range: DateRange = None,
        due_date_range: DateRange = None, payment_date_range: DateRange = None, creation_date_range: DateRange = None, archived: bool = None,
        fields: List[str] = None
    ):
        return cls(
            email, recipient_first_name, recipient_last_name, recipient_business_name, inv_status, invoice_number, reference,
            country_code, memo, total_amount_range, invoice_date_range, due_date_range, payment_date_range, creation_date_range, 
            archived, fields
        )