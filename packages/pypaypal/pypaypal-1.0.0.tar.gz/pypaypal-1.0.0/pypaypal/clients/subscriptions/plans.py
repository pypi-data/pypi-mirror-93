"""
    Plan resource clients for the paypal resource group.

    Resource docs & Reference: https://developer.paypal.com/docs/api/subscriptions/v1/
"""
import json

from datetime import datetime
from typing import Type, TypeVar, List, NamedTuple

from pypaypal.clients.base import ClientBase, ActionLink

from pypaypal.http import ( 
    parse_url,
    PayPalSession,
    LEGACY_LIVE_API_BASE_URL,
    LEGACY_SANDBOX_API_BASE_URL
)

from pypaypal.entities.base import ( 
    PaypalPage,
    ResponseType, 
    PaypalApiResponse, 
    PatchUpdateRequest,
    PaypalApiBulkResponse
)

from pypaypal.entities.subscriptions.plans import Plan, PricingScheme

"""
    Base Resource Live URL
"""
_LIVE_RESOURCE_BASE_URL = parse_url(LEGACY_LIVE_API_BASE_URL, 'billing', 'plans')

"""
    Base Resource Sandbox URL
"""
_SANDBOX_RESOURCE_BASE_URL = parse_url(LEGACY_SANDBOX_API_BASE_URL, 'billing', 'plans')

T = TypeVar('T', bound = 'PlanClient')

class UpdatePricingSchemeRequest(NamedTuple):
    """Immutable object to send pricing scheme update requests to the API.
    """
    billing_cycle_sequence: int
    pricing_scheme: PricingScheme

    def to_dict(self) -> dict:
        return { 
            'pricing_scheme': self.pricing_scheme,
            'billing_cycle_sequence': self.billing_cycle_sequence            
        }

class PlanClient(ClientBase):
    """Plans resource group client class.
    """
    def __init__(self, url: str, session: PayPalSession):
        super().__init__(url, session)

    def create_plan(self, plan: Plan, request_id: str = None, response_type: ResponseType = ResponseType.MINIMAL) -> PaypalApiResponse[Plan]:
        """Calls the paypal API to create a plan
        
        Arguments:
            plan {Plan} -- The plan to be made (use the create factory method)
        
        Keyword Arguments:
            request_id {str} -- Paypal request id for idempotence (default: {None})
            response_type {ResponseType} -- Peferred response type (default: {ResponseType.MINIMAL})
        
        Returns:
            PaypalApiResponse[Plan] -- an API response object with the plan info
        """
        url = self._base_url
        body = json.dumps(plan.to_dict())
        headers = { 'Prefer': response_type.as_header_value() }

        if request_id:
            headers['PayPal-Request-Id'] = request_id
        
        api_response = self._session.post(url, body, headers = headers)

        if api_response.status_code // 100 != 2:
            return PaypalApiResponse.error(api_response)
        
        return PaypalApiResponse.success(api_response, Plan.serialize_from_json(api_response.json(), response_type))

    def list_plans(
            self, product_id: str = None, plan_ids: List[str] = [], 
            page_size: int = 10, page: int = 1, total_required: bool = True, 
            response_type: ResponseType = ResponseType.MINIMAL
        ) -> PaypalPage[Plan]:
        """Calls the Paypal API to list different plan details in a page
        
        Keyword Arguments:
            product_id {str} -- product id to query (default: {None})
            plan_ids {List[str]} -- list of desired plan ids (10 supported) (default: {[]})
            page_size {int} -- size of the page (default: {10})
            page {int} -- desired page (default: {1})
            total_required {bool} -- flag to show the total count in the response (default: {True})
            response_type {ResponseType} -- response type (default: {ResponseType.MINIMAL})
        
        Returns:
            PaypalPage[Plan] -- Page with plan details
        """
        url = self._base_url
        params = { 'page_size': page_size, 'page': page, 'total_required': total_required }

        if product_id:
            params['product_id'] = product_id
        if plan_ids:
            params['plan_ids'] = ','.join(plan_ids)

        api_response = self._session.get(url, params, headers = { 'Prefer': response_type.as_header_value() })

        if api_response.status_code // 100 != 2:
            return PaypalPage.error(api_response)
        
        return PaypalPage.full_parse_success(api_response, Plan, 'plans', response_type)

    def list_plans_from_link(self, link: ActionLink, response_type: ResponseType = ResponseType.MINIMAL) -> PaypalPage[Plan]:
        """Calls the Paypal API to list different plan details in a page

        Arguments:
            link {ActionLink} -- Page link

        Keyword Arguments:
            response_type {ResponseType} -- response type (default: {ResponseType.MINIMAL})
        
        Returns:
            PaypalPage[Plan] -- Page with plan details
        """
        url = link.href
        api_response = self._session.get(url, headers = { 'Prefer': response_type.as_header_value() })

        if api_response.status_code // 100 != 2:
            return PaypalPage.error(api_response)
        
        return PaypalPage.full_parse_success(api_response, Plan, 'plans', response_type)

    def update_plan(self, plan_id: str, update_request: List[PatchUpdateRequest]) -> PaypalApiResponse:
        """Patch request to update a plan. See the docs for details 
        
        Arguments:
            plan_id {str} -- id of the plan to be updated.
            update_request {PatchUpdateRequest} -- request object with update info.
        
        Returns:
            PaypalApiResponse -- Response obj with operation status
        """
        url = parse_url(self._base_url, plan_id) 
        body = json.dumps([ {'op': x.operation, 'value': x.value, 'path': x.path } for x in update_request ])

        api_response = self._session.patch(url, body)

        if api_response.status_code // 100 != 2:
            return PaypalPage.error(api_response)
        
        return PaypalApiResponse.success(api_response)

    def show_plan_details(self, plan_id: str) -> PaypalApiResponse[Plan]:
        """Calls the paypal API to get the plan details
        
        Arguments:
            plan_id {str} -- The plan identifier
        
        Returns:
            PaypalApiResponse[Plan] -- Api response obj with the plan info.
        """
        api_response = self._session.get(parse_url(self._base_url, plan_id))

        if api_response.status_code // 100 != 2:
            return PaypalPage.error(api_response)
        
        return PaypalApiResponse.success(api_response, Plan.serialize_from_json(api_response.json()))

    def activate_plan(self, plan_id: str) -> PaypalApiResponse:
        """Calls the API to activate a plan
        
        Arguments:
            plan_id {str} -- The id of the plan to activate
        
        Returns:
            PaypalApiResponse -- Response with the operation status
        """
        api_response = self._session.post(parse_url(self._base_url, plan_id, 'activate'))

        if api_response.status_code // 100 != 2:
            return PaypalPage.error(api_response)
        
        return PaypalApiResponse.success(api_response)

    def deactivate_plan(self, plan_id: str) -> PaypalApiResponse:
        """Calls the API to deactivate a plan
        
        Arguments:
            plan_id {str} -- The id of the plan to deactivate
        
        Returns:
            PaypalApiResponse -- Response with the operation status
        """
        api_response = self._session.post(parse_url(self._base_url, plan_id, 'deactivate'))

        if api_response.status_code // 100 != 2:
            return PaypalPage.error(api_response)
        
        return PaypalApiResponse.success(api_response)

    def update_pricing(self, plan_id: str, pricing_schemes: List[UpdatePricingSchemeRequest]) -> PaypalApiResponse:
        """Calls the API to update a plan's pricing scheme
        
        Arguments:
            plan_id {str} -- The id of the plan to deactivate
            pricing_schemes List[UpdatePricingSchemeRequest] -- The pricing scheme updates
        
        Returns:
            PaypalApiResponse -- Response with the operation status
        """
        body = json.dumps([ x.to_dict() for x in pricing_schemes ])
        url = parse_url(self._base_url, plan_id, 'update-pricing-schemes')
        
        api_response = self._session.post(url, body)

        if api_response.status_code // 100 != 2:
            return PaypalPage.error(api_response)
        
        return PaypalApiResponse.success(api_response)

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
