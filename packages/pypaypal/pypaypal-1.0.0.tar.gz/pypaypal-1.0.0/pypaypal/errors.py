"""
    Module containing the client errors and exceptions
"""

import copy

from typing import Type, TypeVar, List

T = TypeVar('T', bound = 'PayPalErrorDetail')

class PayPalErrorDetail:
    """
        Generic paypal error
    """
    def __init__(self, json_response: dict, name: str, message: str, info_link: str):
        self.name = name
        self.message = message
        self.information_link = info_link
        self._json_response = json_response

    @property
    def as_json_dict(self) -> dict:
        return self._json_response

    @property
    def debug_id(self) -> str:
        return self._json_response.get('debug_id')

    @property
    def additional_details(self) -> List[dict]:
        return self._json_response.get('details')

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict) -> T:
        return cls(json_data, json_data.get('name'), json_data.get('message'), json_data.get('information_link'))

class IdentityError(Exception):
    """
        Authentication errors
    """
    def __init__(self, response):
        super().__init__('Identity error occoured')
        self.response = response
        self.error = response.json().get('error')
        self.error_description = response.json().get('error_description')

class ExpiredSessionError(Exception):
    """
        Errors regarding expired tokens & session
    """
    def __init__(self, data):
        super().__init__('token or session has expired')
        self.data = data

class PaypalRequestError(Exception):
    """
        Non identity errors that may arise from a request to the paypal api
    """
    def __init__(self, details: PayPalErrorDetail):
        super().__init__(details.message)
        self.details = details

# class EntityRefreshError(Exception):
#     """
#       Error raised when there's a failure refreshing an entity  
#     """
#     def __init__(self, entity):
#         super().__init__(f'There was an error refreshing an entity of {type(entity)}')

