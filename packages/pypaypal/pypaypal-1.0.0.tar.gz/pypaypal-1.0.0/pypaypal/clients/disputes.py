"""
    Dispute resource clients for the paypal resource group.

    Resource docs & Reference: https://developer.paypal.com/docs/api/customer-disputes/v1/#disputes
"""

import json

from datetime import datetime
from typing import Type, TypeVar, List

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

from pypaypal.clients.base import ClientBase, ActionLink
from pypaypal.entities.dispute import Dispute, DisputeUpdateRequest, DisputeEvidence

from pypaypal.entities.base import ( 
    ResponseType, 
    PaypalApiResponse, 
    PaypalPage, 
    PaypalApiBulkResponse, 
    Money, 
    PaypalPortableAddress 
)

from pypaypal.http import ( 
    parse_url,
    PayPalSession,
    LEGACY_LIVE_API_BASE_URL, 
    LEGACY_SANDBOX_API_BASE_URL 
)

"""
    Base Resource Live URL
"""
_LIVE_RESOURCE_BASE_URL = parse_url(LEGACY_LIVE_API_BASE_URL, 'disputes')

"""
    Base Resource Sandbox URL
"""
_SANDBOX_RESOURCE_BASE_URL = parse_url(LEGACY_SANDBOX_API_BASE_URL, 'disputes')

T = TypeVar('T', bound = 'DisputeClient')

class _SandboxExclusiveDisputeClient(ClientBase):
    """Disputes resource group client class for API calls 
       that should only be accesed in sandbox mode.
    """
    def __init__(self, url: str, session: PayPalSession):
        super().__init__(url, session)

class DisputeClient(ClientBase):
    """Disputes resource group client class
    """
    
    def __init__(self, url: str, session: PayPalSession):
        """Client ctor
        
        Arguments:
            session {PayPalSession} -- The http session 
        """
        super().__init__(url, session)
        self.sandbox_exclusive = None if session.session_mode.is_live() else _SandboxExclusiveDisputeClient(url, session)

    def list_disputes(self, start_time: datetime, page_size:int=2) -> PaypalPage[Dispute]:
        """Performs an API call to lists disputes
        
        Arguments:
            start_time {datetime} -- Start date
        
        Keyword Arguments:
            page_size {int} -- size of the page (default: {2})
        
        Returns:
            PaypalPage[Dispute] -- Page with a lists of disputes
        """
        url = self._base_url
        params = { 'page_size' : page_size, 'start_time': start_time.strftime('%Y-%m-%dT%H:%M:%S.000Z') }

        api_response = self._session.get(url, params)

        if api_response.status_code != 200:
            return PaypalPage(True, api_response, 0, 0, [], [])
        
        json_response = api_response.json()
        items = [ Dispute.serialize_from_json(x) for x in json_response['items']]
        links = [ActionLink(x['href'], x['rel'], x.get('method', 'GET')) for x in json_response['links']]

        return PaypalPage(False, api_response, json_response.get('total_items'), json_response.get('total_pages'), items, links)

    def list_disputes_from_link(self, link: ActionLink) -> PaypalPage[Dispute]:
        """Performs an API call to lists disputes inside a page
        
        Arguments:
            link {ActionLink} -- page link
                
        Returns:
            PaypalPage[Dispute] -- Page with a lists of disputes
        """
        return self._page_from_link(link, 'items', Dispute)
    
    def partial_dispute_update(self, dispute_id: str, update_request: DisputeUpdateRequest) -> PaypalApiResponse[Dispute]:
        """Calls the Paypal API to  Partially update a dispute, by ID.            
            Right now it's only possible to update the communication_detail value.
        
        Arguments:
            dispute_id {str} -- The dispute identifier
            update_request {DisputeUpdateRequest} -- Update request with the details
        
        Returns:
            PaypalApiResponse[Dispute] -- Operation response status
        """
        url = parse_url(self._base_url, dispute_id)
        body = { 'op': update_request.operation, 'path': update_request.path, 'value': update_request.value }

        api_response = self._session.patch(url, json.dumps(body))

        return PaypalApiResponse(api_response.status_code != 204, api_response)

    def show_dispute_details(self, dispute_id: str, response_type: ResponseType=ResponseType.MINIMAL) -> PaypalApiResponse[Dispute]:
        """Performs an API call to show the details for a dispute, by ID. 
        
        Arguments:
            dispute_id {str} -- Dispute identifier
        
        Keyword Arguments:
            response_type {ResponseType} -- The preferred response type (default: {ResponseType.MINIMAL})
        
        Returns:
            PaypalApiResponse[Dispute] -- [description]
        """        
        return self._get_element_details(parse_url(self._base_url, dispute_id), dispute_id, Dispute, response_type)

    def dispute_details_from_entity(self, dispute: Dispute, response_type: ResponseType=ResponseType.MINIMAL) -> PaypalApiResponse[Dispute]:
        """Performs an API call to show the details for a dispute, by ID. 
        
        Arguments:
            dispute_id {str} -- Dispute identifier
        
        Keyword Arguments:
            response_type {ResponseType} -- The preferred response type (default: {ResponseType.MINIMAL})
        
        Returns:
            PaypalApiResponse[Dispute] -- [description]
        """        
        url = dispute.read_link
        headers = { 'Prefer': response_type.as_header_value() }
        api_response = self._execute_action_link(url, None, headers = headers)

        if api_response.status_code != 200:
            return PaypalApiResponse(True, api_response)

        return PaypalApiResponse(False, api_response, Dispute.serialize_from_json(api_response.json(), response_type))
    
    def _execute_basic_dispute_action(self, url: str, body: dict) -> PaypalApiBulkResponse[ActionLink]:
        """Executes a standard simple dispute action
        
        Arguments:
            url {str} -- The action URL
            note {str} -- Notes & comments
        
        Returns:
            PaypalApiBulkResponse[ActionLink] -- action links related to the dispute
        """
        response = self._session.post(url, json.dumps(body))

        if response.status_code != 200:
            return PaypalApiBulkResponse(True, response)
        
        return PaypalApiBulkResponse(False, response, ActionLink.serialize_from_json(response['links']))

    def _execute_evidence_multipart_request(self, url: str, json_part: dict, files: MIMEApplication) -> PaypalApiBulkResponse[ActionLink]:
        """Calls the API to provide evidence on a multipart request
        
        Arguments:
            dispute_id {str} -- dispute identifier
            json_part {dict} -- Json part of the multipart request
            files {MIMEApplication} -- files to be appended
        
        Keyword Arguments:
            return_addr {PaypalPortableAddress} -- [description] (default: {None})
        
        Returns:
            PaypalApiBulkResponse[ActionLink] -- [description]
        """
        multipart = MIMEMultipart('related')        
        text = 'input={};type=application/json'.format(json.dumps(json_part))

        json_part = MIMEText(text, 'json')
        # json_part = MIMEApplication(json_part,'json')

        multipart.attach(json_part)

        for f in files:
            multipart.attach(f)

        body = multipart.as_string()
        headers = dict(multipart.items())
        response = self._session.post(url, body, headers = headers)

        if response.status_code != 200:
            return PaypalApiBulkResponse(True, response)
        
        return PaypalApiBulkResponse(False, response, ActionLink.serialize_from_json(response['links']))

    def accept_claim(self, dispute_id: str, refund_amount: Money= None, **kwargs) -> PaypalApiBulkResponse[ActionLink]:
        """Calls the paypal API to accept a claim & close the dispute in favor of the customer
        
        Arguments:
            dispute_id {str} -- [description]

        Keyword Arguments:
            note {str} -- Notes & comments
            accept_claim_reason {str} -- Reason to accept the claim (default REASON_NOT_SET)
            invoice_id {str} -- The merchant-provided ID of the invoice for the refund. 
            return_shipping_address {PaypalPortableAddress} --  The return address for the item.
            refund_amount {Money} -- To accept a customer's claim, the amount that the merchant agrees to refund the customer.
        Returns:
            PaypalApiBulkResponse[ActionLink] -- action links related to the dispute
        """
        if refund_amount:
            kwargs['refund_amount'] = refund_amount.to_dict()
            self._remove_null_entries(kwargs['refund_amount'])
        
        if 'return_shipping_address' in kwargs.keys() and isinstance(kwargs['return_shipping_address'], PaypalPortableAddress):
            kwargs['return_shipping_address'] = kwargs['return_shipping_address'].to_dict()
            self._remove_null_entries(kwargs['return_shipping_address'])

        return self._execute_basic_dispute_action(parse_url(self._base_url, dispute_id, 'accept-claim'), kwargs)

    def accept_offer(self, dispute_id: str, note: str) -> PaypalApiBulkResponse[ActionLink]:
        """Performs an API call to execute a customer acceptance of an offer from the merchant to resolve a dispute.
        
        Arguments:
            dispute_id {str} -- The dispute identifier 
            note {str} -- The customer notes about accepting of offer.
        
        Returns:
            PaypalApiBulkResponse[ActionLink] -- action links related to the dispute
        """
        return self._execute_basic_dispute_action(parse_url(self._base_url, dispute_id, 'accept-offer'), {'note': note})

    def acknowledge_returned_item(self, dispute_id: str, note: str) -> PaypalApiBulkResponse[ActionLink]:
        """Performs an API call to acknowledge that the customer returned an item for a dispute.
        
        Arguments:
            dispute_id {str} -- The dispute identifier 
            note {str} -- Merchant provided notes.
        
        Returns:
            PaypalApiBulkResponse[ActionLink] -- action links related to the dispute
        """
        return self._execute_basic_dispute_action(parse_url(self._base_url, dispute_id, 'acknowledge-return-item'), {'note': note})

    def appeal_dispute(self, dispute_id: str, evidence: DisputeEvidence, files: MIMEApplication, return_addr: PaypalPortableAddress=None) -> PaypalApiBulkResponse[ActionLink]:
        """Appeals a dispute
        
        Arguments:
            dispute_id {str} -- Dispute identifier
            evidence {DisputeEvidence} -- Appeal evidence 
            files {List[bytes]} -- files to be uploaded (current limit 10MB, 5 max per file)
        
        Returns:
            PaypalApiBulkResponse[ActionLink] -- [description]
        """
        url = parse_url(self._base_url, dispute_id, 'appeal')

        json_part = dict()
        json_part['evidences'] = evidence.to_dict()
        
        if return_addr: 
            json_part['return_address'] = return_addr.to_dict()
            self._remove_null_entries(json_part['return_address'])

        return self._execute_evidence_multipart_request(url, json_part, files)

    def deny_offer(self, dispute_id: str, note: str) -> PaypalApiBulkResponse[ActionLink]:
        """Calls the API to deny an offer that the merchant proposes for a dispute.
        
        Arguments:
            dispute_id {str} -- The dispute identifier
            note {str} -- Customer notes about the denial of offer
        
        Returns:
            PaypalApiBulkResponse[ActionLink] -- action links related to the dispute
        """
        return self._execute_basic_dispute_action(parse_url(self._base_url, dispute_id,'deny-offer'), {'note':note})

    def escalate_to_claim(self, dispute_id: str, note: str) -> PaypalApiBulkResponse[ActionLink]:
        """Calls the API to escalate the dispute, by ID, to a PayPal claim.
        
        Arguments:
            dispute_id {str} -- The dispute identifier
            note {str} -- Customer notes about the escalation
        
        Returns:
            PaypalApiBulkResponse[ActionLink] -- action links related to the dispute
        """
        return self._execute_basic_dispute_action(parse_url(self._base_url, dispute_id,'deny-offer'), {'note':note})

    def make_return_offer(self, dispute_id: str, note: str, offer_type: str, invoice_id: str=None, offer_amt: Money=None, return_addr: PaypalPortableAddress=None) -> PaypalApiBulkResponse[ActionLink]:
        """Calls the API to make an offer to the other party to resolve a dispute
        
        Arguments:
            dispute_id {str} -- The dispute identifier
            note {str} -- Customer notes about the escalation
            offer_type {str} -- The merchant-proposed offer type for the dispute

        Keyword Arguments:
            offer_amt {Money} --  The amount proposed to resolve the dispute. 
            invoice_id {str} -- The merchant-provided ID of the invoice for the refund. 
            return_shipping_address {PaypalPortableAddress} --  The return address for the item.
            refund_amount {Money} -- To accept a customer's claim, the amount that the merchant agrees to refund the customer.

        Returns:
            PaypalApiBulkResponse[ActionLink] -- action links related to the dispute
        """
        body = { 'note': note, 'offer_type' : offer_type }

        if invoice_id:
            body['invoice_id'] = invoice_id
        
        if offer_amt:
            body['offer_amount'] = offer_amt.to_dict()
            self._remove_null_entries(body['offer_amount'])
        
        if return_addr:
            body['return_address'] = return_addr.to_dict()
            self._remove_null_entries(body['return_address'])

        return self._execute_basic_dispute_action(parse_url(self._base_url, dispute_id,'make-offer'), body)

    def provide_evidence(self, dispute_id: str, evidence: DisputeEvidence, files: MIMEApplication, return_addr: PaypalPortableAddress=None) -> PaypalApiBulkResponse[ActionLink]:
        """Calls the API to provide evidence 
        
        Arguments:
            dispute_id {str} -- The dispute identifier
            evidence {DisputeEvidence} -- The evidence to be supported
            files {MIMEApplication} -- Files regarding the evidence as MIMEApplication
        
        Keyword Arguments:
            return_addr {PaypalPortableAddress} -- Portable return addr if needed (default: {None})
        
        Returns:
            PaypalApiBulkResponse[ActionLink] -- action links related to the dispute
        """
        url = parse_url(self._base_url, dispute_id, 'provide-evidence')

        json_part = dict()
        json_part['evidences'] = evidence.to_dict()
        
        if return_addr: 
            json_part['return_address'] = return_addr.to_dict()
            self._remove_null_entries(json_part['return_address'])

        return self._execute_evidence_multipart_request(url, json_part, files)

    def provide_supporting_info(self, dispute_id: str, notes: str, supporting_doc: MIMEApplication) -> PaypalApiBulkResponse[ActionLink]:
        """Calls the API to provide supporting information on a dispute
        
        Arguments:
            dispute_id {str} -- The dispute identifier
            notes {str} -- Merchant notes
            supporting_doc {MIMEApplication} -- Supporting document
                
        Returns:
            PaypalApiBulkResponse[ActionLink] -- action links related to the dispute
        """
        url = parse_url(self._base_url, dispute_id, 'provide-supporting-info')
        return self._execute_evidence_multipart_request(url, {'notes': notes}, supporting_doc)

    def send_message_to_third_party(self, dispute_id: str, message: str) -> PaypalApiBulkResponse[ActionLink]:
        """Calls the api to send a message about a dispute, by ID, to the other party in the dispute
        
        Arguments:
            dispute_id {str} -- The dispute id
            message {str} -- Message to be sent
        
        Returns:
            PaypalApiBulkResponse[ActionLink] -- action links related to the dispute
        """
        url = parse_url(self._base_url, dispute_id, 'send-message')
        return self._execute_basic_dispute_action(url, {'message': message})

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