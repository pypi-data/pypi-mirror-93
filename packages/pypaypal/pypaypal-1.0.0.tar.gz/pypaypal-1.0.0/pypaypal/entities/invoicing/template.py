"""
    Module with invoice templete related entities
"""

from enum import Enum
from datetime import datetime
from typing import Type, List

import dateutil.parser

from pypaypal.entities.base import ( 
    T,
    Item,   
    Money,
    ActionLink,
    PayPalEntity,
    ResponseType,
    RecipientInfo
)

from pypaypal.entities.invoicing.invoice import (
    MetaData,
    InvoicerInfo,
    FileReference,
    PartialPayment
)

class InvoiceListRequestField(Enum):
    ALL = 1
    NONE = 2

class TemplateDetail(PayPalEntity):
    """Template detail object representation.
    """

    def __init__(
        self, reference: str, currency_code: str, note: str, 
        terms_and_conditions: str, memo: str, payment_term: str,
        metadata: MetaData, attachments: List[FileReference] = [],
        **kwargs
    ):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.reference = reference
        self.currency_code = currency_code
        self.note  = note
        self.terms_and_conditions = terms_and_conditions
        self.memo = memo
        self.payment_term = payment_term
        self.metadata = metadata
        self.attachments = attachments or []

    def to_dict(self) -> dict:
        ret = super().to_dict()        
        if self.metadata:
            ret['metadata'] = [ x.to_dict() for x in self.metadata ]
        if self.attachments:
            ret['attachments'] = [ x.to_dict() for x in self.attachments ]
        return ret

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        metadata, attachments = None, []
        
        if 'metadata' in json_data.keys():
            metadata = MetaData.serialize_from_json(json_data, response_type)
        
        if 'attachments' in json_data.keys():
            attachments = [FileReference.serialize_from_json(x, response_type) for x in json_data['attachments']]

        return cls(
            json_data.get('reference'), json_data.get('currency_code'), json_data.get('note'), 
            json_data.get('terms_and_conditions'), json_data.get('memo'), json_data.get('payment_term'),
            metadata, attachments, json_response= json_data, response_type = response_type
        )

    @classmethod
    def create(
        cls, currency_code: str, *, reference: str, note: str, 
        terms_and_conditions: str, memo: str, payment_term: str, 
        metadata: MetaData, attachments: List[FileReference] = []
    ):
        return cls(
            reference, currency_code, note, terms_and_conditions, 
            memo, payment_term, metadata, attachments or []
        )

class TemplateConfiguration(PayPalEntity):
    """Invoice configuration object representation
    """

    def __init__(self, tax_calc_after_discount: bool, tax_inclusive: bool, allow_tip: bool, partial_payment: PartialPayment=None, **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.allow_tip = allow_tip
        self.tax_inclusive = tax_inclusive
        self.partial_payment = partial_payment
        self.tax_calc_after_discount = tax_calc_after_discount
    
    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        partial_payment = PartialPayment.serialize_from_json(json_data['partial_payment']) if 'partial_payment' in json_data.keys() else None

        return cls(
            json_data.get('tax_calc_after_discount'), json_data.get('tax_inclusive'),
            json_data.get('allow_tip'), partial_payment, json_response= json_data, response_type = response_type
        )

    @classmethod
    def create(
        cls, *, tax_calc_after_discount: bool = True, tax_inclusive: bool = False,
        allow_tip: bool = False, partial_payment: PartialPayment=None
    ):
        return cls(tax_calc_after_discount, tax_inclusive, allow_tip, partial_payment)

class TemplateInfo(PayPalEntity):
    """ Template info object representation. 
        Includes invoicer business information, invoice recipients,
        items, and configuration.
    """
    
    def __init__(
        self, detail: TemplateDetail, invoicer: InvoicerInfo, primary_recipients: RecipientInfo,
        items: List[Item], configuration: TemplateConfiguration, amount: Money, due_amount: Money,
        **kwargs
    ):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.detail = detail
        self.invoicer = invoicer
        self.primary_recipients = primary_recipients
        self.items = items
        self.configuration = configuration
        self.amount = amount
        self.due_amount = due_amount
        self.additional_recipients = self._json_response.get('additional_recipients', kwargs.get('additional_recipients'))
    
    def to_dict(self) -> dict:
        ret = super().to_dict()        
        if self.items:
            ret['items'] = [ x.to_dict() for x in self.items ]
        return ret

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        primary_recipients, items  = [], []
        detail, invoicer, configuration, amount, due_amount  = None, None, None, None, None

        if 'primary_recipients' in json_data.keys():
            primary_recipients = [RecipientInfo.serialize_from_json(x, response_type) for x in json_data['primary_recipients']]
        if 'items' in json_data.keys():
            items = [Item.serialize_from_json(x, response_type) for x in json_data['items']]
        
        if 'detail' in json_data.keys():
            detail = TemplateDetail.serialize_from_json(json_data['detail'], response_type)
        if 'invoicer' in json_data.keys():
            invoicer = InvoicerInfo.serialize_from_json(json_data['invoicer'], response_type)
        if 'configuration' in json_data.keys():
            configuration = TemplateConfiguration.serialize_from_json(json_data['configuration'], response_type)
        if 'amount' in json_data.keys():
            amount = Money.serialize_from_json(json_data['amount'], response_type)
        if 'due_amount' in json_data.keys():
            due_amount = Money.serialize_from_json(json_data['due_amount'], response_type)

        return cls(
            detail, invoicer, primary_recipients, items, configuration, amount, 
            due_amount, json_response= json_data, response_type = response_type
        )

    @classmethod
    def create(
        cls: Type[T], *, detail: TemplateDetail, invoicer: InvoicerInfo, primary_recipients: List[RecipientInfo], 
        additional_recipients: List[str], items: List[Item], configuration: TemplateConfiguration, amount: Money,
        due_amount: Money = None)  -> 'TemplateInfo':

        add_rep = [{ 'email_address': x} for x in additional_recipients]

        return cls(
            detail, invoicer, primary_recipients, items, 
            configuration, amount, due_amount, additional_recipients = add_rep
        )

class DisplayPreference(PayPalEntity):
    """Display preference object representation
    """
    def __init__(self, hidden: bool, **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.hidden = hidden

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        return cls(json_data['hidden'], json_response= json_data, response_type = response_type)

    @classmethod
    def create(cls, hidden: bool) -> 'DisplayPreference':
        return cls(hidden)

class TemplateItemSetting(PayPalEntity):
    """Template item setting object representation
    """
    def __init__(self, field_name: str, display_preference: DisplayPreference, **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.field_name = field_name
        self.display_preference = display_preference

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        pref = None
        
        if 'display_preference' in json_data.keys():
            pref = DisplayPreference.serialize_from_json(json_data['display_preference'], response_type)

        return cls(json_data['field_name'], pref, json_response= json_data, response_type = response_type)

    @classmethod
    def create(cls, field_name: str, hidden: bool = False) -> 'TemplateItemSetting':
        return cls(field_name, DisplayPreference.create(hidden))

class TemplateSubtotalSetting(PayPalEntity):
    """Template subtotal setting object representation
    """
    def __init__(self, field_name: str, display_preference: DisplayPreference, **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.field_name = field_name
        self.display_preference = display_preference

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        pref = None
        
        if 'display_preference' in json_data.keys():
            pref = DisplayPreference.serialize_from_json(json_data['display_preference'], response_type)

        return cls(json_data['field_name'], pref, json_response= json_data, response_type = response_type)

    @classmethod
    def create(cls, field_name: str, hidden: bool = False) -> 'TemplateSubtotalSetting':
        return cls(field_name, DisplayPreference.create(hidden))

class TemplateSettings(PayPalEntity):
    """Template show/hide settings object representation.
    """
    def __init__(self, 
        template_item_settings: List[TemplateItemSetting], 
        template_subtotal_settings: List[TemplateSubtotalSetting], **kwargs
        ):
            super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
            self.template_item_settings = template_item_settings
            self.template_subtotal_settings = template_subtotal_settings
    
    def to_dict(self) -> dict:
        ret = super().to_dict()        
        if self.template_item_settings:
            ret['template_item_settings'] = [ x.to_dict() for x in self.template_item_settings ]
        if self.template_subtotal_settings:
            ret['template_subtotal_settings'] = [ x.to_dict() for x in self.template_subtotal_settings ]
        return ret

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        item_settings, subtotal_settings = [], []
        
        if 'template_item_settings' in json_data.keys():
            item_settings = [TemplateItemSetting.serialize_from_json(x, response_type) for x in json_data['template_item_settings']]

        if 'template_subtotal_settings' in json_data.keys():
            item_settings = [TemplateSubtotalSetting.serialize_from_json(x, response_type) for x in json_data['template_subtotal_settings']]

        return cls(item_settings, subtotal_settings, json_response= json_data, response_type = response_type)

    @classmethod
    def create(cls, field_name: str, hidden: bool = False) -> 'TemplateSubtotalSetting':
        return cls(field_name, DisplayPreference.create(hidden))

class Template(PayPalEntity):
    """Invoice template object representation    
    """
    def __init__(
        self, name: str, default_template: bool, 
        template_info: TemplateInfo, settings: TemplateSettings, 
        unit_of_measure: str, **kwargs
        ):
            super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
            self.name = name
            self.settings = settings
            self.template_info = template_info
            self.unit_of_measure = unit_of_measure
            self.default_template = default_template
            self.id = self._json_response.get('id', kwargs.get('id'))
            self.standard_template = self._json_response.get('standard_template', kwargs.get('standard_template'))
            self.links = [ActionLink(x['href'], x['rel'], x.get('method', 'GET')) for x in self._json_response.get('links', [])]

    @property
    def read_link(self) -> ActionLink:
        """Retrieves a link to read this entity details.
        
        Returns:
            ActionLink -- The link for requesting the information to the API.
        """
        return next(filter(lambda x: x.rel == 'self', self.links), None)

    @property
    def replace_link(self) -> ActionLink:
        """Retrieves a link to replace (update) this template.
        
        Returns:
            ActionLink -- The link to execute the API action.
        """
        return next(filter(lambda x: x.rel == 'replace', self.links), None)

    @property
    def delete_link(self) -> ActionLink:
        """Retrieves a link to delete this template.
        
        Returns:
            ActionLink -- The link to execute the API action.
        """
        return next(filter(lambda x: x.rel == 'delete', self.links), None)

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        template_info, template_settings = None, None
        
        if 'template_info' in json_data.keys():
            template_info = TemplateInfo.serialize_from_json(json_data['template_info'], response_type)
        if 'template_settings' in json_data.keys():
            template_settings = TemplateSettings.serialize_from_json(json_data['template_settings'], response_type)

        return cls(
            json_data.get('name'), json_data.get('default_template'), template_info, 
            template_settings, json_data.get('unit_of_measure'), json_response= json_data,
            response_type = response_type
        )

    @classmethod
    def create(
            cls, name: str, template_info: TemplateInfo, settings: TemplateSettings, 
            unit_of_measure: str, default_template: bool = False
        ) -> 'Template':
            return cls(name, default_template, template_info, settings, unit_of_measure)
