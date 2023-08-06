"""
    Paypal Web Expirience Profile resource clients for the paypal resource group.

    Resource docs & Reference: https://developer.paypal.com/docs/api/payment-experience/v1/#definition-presentation
"""

import json

from datetime import datetime
from typing import Type, TypeVar, List

from pypaypal.clients.base import ClientBase, ActionLink

from pypaypal.http import ( 
    parse_url,
    PayPalSession,
    LEGACY_LIVE_API_BASE_URL,
    LEGACY_SANDBOX_API_BASE_URL
)

from pypaypal.entities.base import ( 
    ResponseType, 
    PaypalApiResponse, 
    PatchUpdateRequest,
    PaypalApiBulkResponse
)

from pypaypal.entities.webexp import WebExpProfile, FlowConfig

"""
    Base Resource Live URL
"""
_LIVE_RESOURCE_BASE_URL = parse_url(LEGACY_LIVE_API_BASE_URL, 'payment-experience', 'web-profiles')

"""
    Base Resource Sandbox URL
"""
_SANDBOX_RESOURCE_BASE_URL = parse_url(LEGACY_SANDBOX_API_BASE_URL, 'payment-experience', 'web-profiles')

T = TypeVar('T', bound = 'WebExpClient')

class WebExpClient(ClientBase):
    """Paypal Web Expirience Profile resource group client class
    """
    def __init__(self, url: str, session: PayPalSession):
        super().__init__(url, session)

    def create_profile(self, profile: WebExpProfile, request_id: str = None) -> PaypalApiResponse[WebExpProfile]:
        """Calls the paypal Api to create a WebExp Profile
        
        Arguments:
            profile {WebExpProfile} -- The profile information.
        
        Keyword Arguments:
            request_id {str} -- Paypal request id for idempotency (default: {None})
        
        Returns:
            PaypalApiResponse[WebExpProfile] -- An api response with the profile
        """        
        headers = {'PayPal-Request-Id': request_id} if request_id else dict()
        api_response = self._session.post(self._base_url, json.dumps(profile.to_dict()), headers = headers)

        if api_response.status_code // 100 != 2:
            return PaypalApiResponse(True, api_response)

        return PaypalApiResponse(False, api_response, WebExpProfile.serialize_from_json(api_response.json()))

    def list_profiles(self) -> PaypalApiBulkResponse[WebExpProfile]:
        """Calls the paypal Api to get a list with the latest 20 web experience profiles 
           for a merchant or subject.
        
        Returns:
            PaypalApiBulkResponse[WebExpProfile] -- Latest 20 profiles
        """
        api_response = self._session.get(self._base_url)

        if api_response.status_code != 200:
            return PaypalApiBulkResponse(True, api_response)

        return PaypalApiBulkResponse(False, api_response, [WebExpProfile.serialize_from_json(x) for x in api_response.json()])
    
    def delete_profile(self, profile_id: str) -> PaypalApiResponse:
        """Calls the paypal Api to delete a WebExp Profile
        
        Arguments:
            profile_id {WebExpProfile} -- The profile id.
        
        Returns:
            PaypalApiResponse -- An api response 
        """
        api_response = self._session.delete(parse_url(self._base_url, profile_id))

        if api_response.status_code != 204:
            return PaypalApiBulkResponse(True, api_response)
        return PaypalApiBulkResponse(False, api_response)
    
    def show_profile_details(self, profile_id: str) -> PaypalApiResponse[WebExpProfile]:
        """Calls the paypal Api to delete a WebExp Profile
        
        Arguments:
            profile_id {WebExpProfile} -- The profile id.
        
        Returns:
            PaypalApiResponse[WebExpProfile] -- An api response with the profile info
        """
        api_response = self._session.get(parse_url(self._base_url, profile_id))

        if api_response.status_code != 200:
            return PaypalApiBulkResponse(True, api_response)
        return PaypalApiBulkResponse(False, api_response, WebExpProfile.serialize_from_json(api_response.json()))

    def path_update_profile(self, profile_id: str, updates: List[PatchUpdateRequest]) ->  PaypalApiResponse:
        """Calls the api to partially-update a web experience profile, by ID.
        
        Arguments:
            profile_id {str} -- The profile id
            updates {List[PatchUpdateRequest]} -- list of update operations
        
        Returns:
            PaypalApiResponse -- API response status
        """
        url = parse_url(self._base_url, profile_id)
        body = json.dumps([{ 'op': x.operation, 'path': x.path, 'value': x.value } for x in updates ])

        api_response = self._session.patch(url, body)

        if api_response.status_code != 204:
            return PaypalApiResponse(True, api_response)
        return PaypalApiResponse(False, api_response)

    def fully_update_profile(self, profile_id: str, name: str, temporary: bool, flow_config: FlowConfig) -> PaypalApiResponse:
        """Calls the api to fully update a web experience profile, by ID.
        
        Arguments:
            profile_id {str} -- The profile id
            updates {List[PatchUpdateRequest]} -- list of update operations
        
        Returns:
            PaypalApiResponse -- API response status
        """
        url = parse_url(self._base_url, profile_id)
        body = WebExpProfile.create(name, temporary, flow_config)

        api_response = self._session.put(url, body)

        if api_response.status_code != 204:
            return PaypalApiResponse(True, api_response)
        return PaypalApiResponse(False, api_response)
