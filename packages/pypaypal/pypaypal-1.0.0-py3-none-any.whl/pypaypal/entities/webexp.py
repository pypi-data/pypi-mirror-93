"""
    Module with all Payment Expirience Web Profiles related entities.
"""

from enum import Enum
from typing import Type, List

from pypaypal.entities.base import (
    T, 
    PayPalEntity, 
    ResponseType
)

class LandingPageType(Enum):
    BILLING = 1
    LOGIN = 2

class UserAction(Enum):
    CONTINUE = 1
    COMMIT = 2

class ShippingOpt(Enum):
    DISPLAY = 0
    REDACT = 1
    GET_FROM_PROFILE = 2

class AddressOverrideOpt(Enum):
    DISPLAY_FROM_FILE = 0
    DISPLAY_FROM_CALL = 1

class FlowConfig(PayPalEntity):
    """Webexp Flow configuration object representation.
    """

    def __init__(
        self, landing_page_type: str, bank_txn_pend_url: str, 
        user_action: str, ret_uri_http_meth: str, **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.landing_page_type = landing_page_type
        self.user_action = user_action
        self.bank_txn_pending_url = bank_txn_pend_url
        self.return_uri_http_method = ret_uri_http_meth
    
    @property
    def user_action_enum(self) -> UserAction:
        try:
            return UserAction[self.user_action] if self.user_action else None
        except:
            return None

    @property
    def landing_page_type_enum(self) -> LandingPageType:
        try:
            return LandingPageType[self.landing_page_type] if self.landing_page_type else None
        except:
            return None

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:        
        return cls(
            json_data.get('landing_page_type'), json_data.get('bank_txn_pending_url'), 
            json_data.get('user_action'), json_data.get('return_uri_http_method'), 
            json_response= json_data, response_type = response_type
        )
    
    @classmethod
    def create(
        cls, *, landing_page_type: LandingPageType = LandingPageType.BILLING, 
        bank_txn_pending_url: str = None, user_action: UserAction = UserAction.CONTINUE, 
        return_uri_http_method: str = None) -> 'FlowConfig':
        ua = 'continue' if user_action == UserAction.CONTINUE else 'commit'
        lpt = 'Login' if landing_page_type == LandingPageType.LOGIN else 'Billing'
        return cls(lpt, bank_txn_pending_url, ua, return_uri_http_method)

class InputField(PayPalEntity):
    """Input field obj representation
    """

    def __init__(self, no_shipping: int, address_override: int, **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.no_shipping = no_shipping
        self.address_override = address_override
    
    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:        
        return cls(
            json_data.get('no_shipping'), json_data.get('address_override'),
            json_response= json_data, response_type = response_type
        )
    
    @classmethod
    def create(cls, no_shipping: ShippingOpt, address_override: AddressOverrideOpt) -> 'InputField':
        return cls(no_shipping.value, address_override.value)

class Presentation(PayPalEntity):
    """WebExp Page Presentation obj representation
    """
    def __init__(self, brand_name: str, logo_image: str, locale_code: str, **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.brand_name = brand_name
        self.logo_image = logo_image
        self.locale_code = locale_code

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        return cls(
            json_data.get('brand_name'), json_data.get('logo_image'), 
            json_data.get('locale_code'), json_response= json_data, 
            response_type = response_type
        )

    @classmethod
    def create(cls, brand_name: str, logo_url: str, locale_code: str) -> 'Presentation':
        return cls(brand_name, logo_url, locale_code)

class WebExpProfile(PayPalEntity):
    """Web Expirience Profile object representation
    """
    def __init__(
        self, name: str, temporary: bool, flow_config: FlowConfig, 
        input_fields: InputField, presentation: Presentation, **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.name = name
        self.temporary = temporary
        self.flow_config  = flow_config
        self.input_fields = input_fields
        self.presentation = presentation
        self.id = self._json_response.get('id', kwargs.get('id'))
    
    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        flow_config, input_fields, presentation = None, None, None

        if 'flow_config' in json_data.keys():
            flow_config = FlowConfig.serialize_from_json(json_data['flow_config'], response_type)
        if 'input_fields' in json_data.keys():
            input_fields = InputField.serialize_from_json(json_data['input_fields'], response_type)
        if 'presentation' in json_data.keys():
            presentation = Presentation.serialize_from_json(json_data['presentation'], response_type)
        
        return cls(json_data.get('name'), json_data.get('temporary'), flow_config, input_fields, presentation)
    
    @classmethod
    def create(
        cls, name: str, temporary: bool, flow_config: FlowConfig = None,
        input_fields: InputField = None, presentation: Presentation = None) -> 'WebExpProfile':
        return cls(name, temporary, flow_config, input_fields, presentation)