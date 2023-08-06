"""
    Product resource clients for the paypal resource group.

    Resource docs & Reference: https://developer.paypal.com/docs/api/catalog-products/v1/
"""

import json
from typing import Type, TypeVar, List

from pypaypal.clients.base import ClientBase, ActionLink
from pypaypal.entities.base import ResponseType, PaypalApiResponse, PaypalPage

from pypaypal.entities.product import Product, ProductType, ProductUpdateRequest

from pypaypal.http import ( 
    parse_url,
    PayPalSession,
    LEGACY_LIVE_API_BASE_URL, 
    LEGACY_SANDBOX_API_BASE_URL 
)

"""
    Base Resource Live URL
"""
_LIVE_RESOURCE_BASE_URL = parse_url(LEGACY_LIVE_API_BASE_URL, 'catalogs/products')

"""
    Base Resource Sandbox URL
"""
_SANDBOX_RESOURCE_BASE_URL = parse_url(LEGACY_SANDBOX_API_BASE_URL, 'catalogs/products')

"""
    Supported product properties for product creation
"""
_PRODUCT_PROPERTIES = { 
    'name', 'product_type', 'id', 'category', 'home_url',
    'image_url', 'description', 'update_time', 'create_time'
}

T = TypeVar('T', bound = 'ProductsClient')


class ProductsClient(ClientBase):
    """Products resource group client class
    """

    def __init__(self, url: str, session: PayPalSession):
        """Client ctor
        
        Arguments:
            session {PayPalSession} -- The http session 
        """
        super().__init__(url, session)

    def create_product(self, product: Product, response_type: ResponseType = ResponseType.MINIMAL) -> PaypalApiResponse[Product]:
        """Performs an API call to create a new product
        
        Arguments:
            product_name {str} -- The product info
            product_type {ProductType} -- the response type (Minimal or Representation)
        """
        url = self._base_url
        headers = { 'Prefer': response_type.as_header_value() }
        
        body = product.to_dict()
        body['create_time'] = body.pop('_create_time', None)
        body['update_time'] = body.pop('_update_time', None)
        self._clean_dictionary(body, _PRODUCT_PROPERTIES)

        api_response = self._session.post(url, json.dumps(body), headers = headers)
        
        if api_response.status_code != 201:
            return PaypalApiResponse(True, api_response)
        return PaypalApiResponse(False, api_response, Product.serialize_from_json(api_response.json(), response_type))

    def list_products(self, page_size: int, page: int) -> PaypalPage[Product]:
        """Performs an API call to get a page of products
        
        Arguments:
            page_size {int} -- Amount of elements in the page
            page {int} -- current page index
        
        Returns:
            PaypalPage[Product] -- A page with product elements
        """
        url = self._base_url
        params = { 'page_size': page_size, 'page': page, 'total_required': True }

        api_response = self._session.get(url, params)
        
        if api_response.status_code != 200:
            return PaypalPage(True, api_response, 0, 0, [], [])
        
        json_response = api_response.json()
        products = [ Product.serialize_from_json(x) for x in json_response['products']]
        links = [ActionLink(x['href'], x['rel'], x.get('method', 'GET')) for x in json_response['links']]

        return PaypalPage(False, api_response, json_response['total_items'], json_response['total_pages'], products, links)

    def list_products_from_page_link(self, page_link: ActionLink) -> PaypalPage[Product]:
        """Performs an API call to get a page of products
        
        Arguments:
            page_size {int} -- Amount of elements in the page
            page {int} -- current page index
        
        Returns:
            PaypalPage[Product] -- A page with product elements
        """
        return self._page_from_link(page_link, 'products', Product)

    def show_product_details(self, product_id: str, response_type = ResponseType.MINIMAL) -> PaypalApiResponse[Product]:
        """Calls the API to get the details for a given product
        
        Arguments:
            product_id {str} -- The product identifier
        
        Keyword Arguments:
            response_type {[type]} -- Response representation (default: {ResponseType.MINIMAL})
        
        Returns:
            PaypalApiResponse[Product] -- Response status with data
        """
        url = parse_url(self._base_url, product_id)
        headers = { 'Prefer': response_type.as_header_value() }        
        api_response = self._session.get(url, None, headers = headers)

        if api_response.status_code != 200:
            return PaypalApiResponse(True, api_response)

        return PaypalApiResponse(False, api_response, Product.serialize_from_json(api_response.json(), response_type))
    
    def product_details_from_entity(self, product: Product, response_type: ResponseType=ResponseType.MINIMAL) -> PaypalApiResponse[Product]:
        """Calls the API to get the details for a given product
        
        Arguments:
            product {Product} -- The product entity with the HATEOAS link
        
        Keyword Arguments:
            response_type {[type]} -- Response representation (default: {ResponseType.MINIMAL})
        
        Returns:
            PaypalApiResponse[Product] -- Response status with data
        """
        url = product.read_link
        headers = { 'Prefer': response_type.as_header_value() }        
        api_response = self._session.get(url, None, headers = headers)

        if api_response.status_code != 200:
            return PaypalApiResponse(True, api_response)

        return PaypalApiResponse(False, api_response, Product.serialize_from_json(api_response.json(), response_type))

    def update_product(self, product_id: str, updates: List[ProductUpdateRequest]) -> PaypalApiResponse:
        """Updates a product
        
        Arguments:
            product_id {str} -- [description]
            updates {List[ProductUpdateRequest]} -- [description]
        
        Returns:
            PaypalApiResponse -- [description]
        """
        url = parse_url(self._base_url, product_id)
        body = [ {'op': x.operation, 'path': x.path, 'value': x.value} for x in updates ]
        api_response = self._session.patch(url, json.dumps(body))

        return PaypalApiResponse(api_response.status_code != 204, api_response)

    @classmethod
    def for_session(cls: T, session: PayPalSession) -> T:
        """Creates a product client from a given paypal session
        
        Arguments:
            cls {T} -- class reference
            session {PayPalSession} -- the paypal session
        
        Returns:
            T -- an instance of TrackersClient with the right configuration by session mode
        """
        base_url = _LIVE_RESOURCE_BASE_URL if session.session_mode.is_live() else _SANDBOX_RESOURCE_BASE_URL
        return cls(base_url, session)