"""
    Module with all product related entities 
"""

from enum import Enum
from typing import Type
from datetime import datetime

import dateutil.parser
from pypaypal.entities.base import T, PayPalEntity, ResponseType, ActionLink, PatchUpdateRequest

class ProductType(Enum):
    PHYSICAL = 1
    DIGITAL = 2
    SERVICE = 3

class UpdateAction(Enum):
    ADD = 1
    REMOVE = 2
    REPLACE = 3

class UpdateField(Enum):
    DESCRIPTION = 1
    CATEGORY = 2
    IMAGE_URL = 3
    HOME_URL = 4

class ProductUpdateRequest(PatchUpdateRequest):
    """Request object for updating a product
    """

    def __init__(self, field: UpdateField, action: UpdateAction, value: str):
        super().__init__('/{}'.format(field.name.lower()), value, action.name.lower())
            
class Product(PayPalEntity):
    """
        Object representation of a paypal product
    """
    def __init__(self, name: str, product_type: ProductType, **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.name = name
        self.product_type = product_type
        self.id = self._json_response.get('id', kwargs.get('id')) 
        self.category = self._json_response.get('category', kwargs.get('category'))
        self.home_url = self._json_response.get('home_url', kwargs.get('home_url'))
        self.image_url = self._json_response.get('image_url', kwargs.get('image_url'))
        self.description = self._json_response.get('description', kwargs.get('description'))
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
    def read_link(self) -> ActionLink:
        """Retrieves a link to read this entity details.
        
        Returns:
            ActionLink -- The link for requesting the information to the API.
        """
        return next(filter(lambda x: x.rel == 'self', self.links), None)

    @property
    def update_link(self) -> ActionLink:
        """Retrieves the update link for this entity
        
        Returns:
            ActionLink -- The link for requesting an update in the API.
        """
        return next(filter(lambda x: x.rel == 'edit', self.links), None)

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        return cls(
            json_data['name'], ProductType[json_data['type']], json_response= json_data, response_type = response_type
        )