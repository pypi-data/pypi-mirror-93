"""
    Invoice api client for paypal REST resources.

    Resource docs & Reference: https://developer.paypal.com/docs/api/invoicing/v2/
"""

import json
from typing import Type, TypeVar, List

from pypaypal.clients.base import ClientBase
from pypaypal.errors import PaypalRequestError

from pypaypal.entities.invoicing.template import Template, InvoiceListRequestField
from pypaypal.entities.invoicing.invoice import Invoice, PaymentDetail, InvoiceSearchRequest

from pypaypal.entities.base import ( 
    PaypalPage,
    ActionLink,
    RefundDetail,
    ResponseType,
    PaypalApiResponse,
    PayPalErrorDetail,
    PaypalApiBulkResponse
)

from pypaypal.http import ( 
    parse_url,
    PayPalSession,     
    LIVE_API_BASE_URL,
    SANDBOX_API_BASE_URL     
)

"""
    Base Resource Live URL
"""
_LIVE_RESOURCE_BASE_URL = parse_url(LIVE_API_BASE_URL, 'invoicing')

"""
    Base Resource Sandbox URL
"""
_SANDBOX_RESOURCE_BASE_URL = parse_url(SANDBOX_API_BASE_URL, 'invoicing')

T = TypeVar('T', bound = 'InvoiceClient')

I = TypeVar('T', bound = 'InvoiceTemplateClient')

class InvoiceClient(ClientBase):
    """Invoice v2 API client class
    """

    def __init__(self, base_url: str, session: PayPalSession):
        super().__init__(base_url, session)
    
    def generate_invoice_number(self) -> str:
        """Calls the paypal API to generate the next invoice number that is available to the merchant.
        
        Returns:
            str -- The generated invoice number

        Raises:
            PaypalRequestError -- If there's an error with the API request
        """
        api_response = self._session.post(parse_url(self._base_url, 'generate-next-invoice-number'), None)

        if api_response.status_code != 200:
            raise PaypalRequestError(PayPalErrorDetail.serialize_from_json(api_response.json()))
        
        return api_response.json()['invoice_number']

    def create_draft_invoice(self, invoice: Invoice) -> PaypalApiResponse:
        """Calls the paypal API to generate an invoice draft.
        
        Arguments:            
            invoice {Invoice} -- the invoice information

        Returns:
            PaypalApiResponse -- The paypal API response
        """
        response = self._session.post(parse_url(self._base_url, 'invoices'), json.dumps(invoice.to_dict()))

        if response.status_code != 201:
            return PaypalApiResponse.error(response)
        
        return PaypalApiResponse.success(response)

    def list_invoices(self, page: int, page_size: int, total_required: bool, fields: List[str]) -> PaypalPage[Invoice]:
        """Calls the paypal API to get an invoice page.
        
        Arguments:
            page {int} -- current page
            page_size {int} -- page size 
            total_required {bool} -- total count required
            fields {List[str]} -- fields to be searched

        Returns:
            PaypalPage -- The paged elements in paypal API paged response 
        """
        query_params = { page: page, page_size: page_size, total_required: total_required, fields: ','.join(fields) }

        response = self._session.get(parse_url(self._base_url, 'invoices'), query_params)

        if response.status_code != 200:
            return PaypalPage.error(response)
        
        json_response = response.json()
        items = [ Invoice.serialize_from_json(x) for x in json_response['items']]
        links = [ ActionLink(x['href'], x['rel'], x.get('method', 'GET')) for x in json_response['links'] ]

        return PaypalPage.success(response, json_response.get('total_items'), json_response.get('total_pages'), items, links)

    def delete_invoice(self, invoice_id: str) -> PaypalApiResponse:
        """Calls the paypal API to delete a draft or scheduled invoice, by ID.
           only invoices in the draft or scheduled state can be deleted. 
           For invoices that have already been sent, you can cancel the invoice. 
           After you delete a draft or scheduled invoice, you can no longer use it 
           or show its details. However, its possible to reuse the invoice number.
        
        Arguments:
            invoice_id {str} -- invoice id

        Returns:
            PaypalApiResponse -- Api operation response status containing the response
        """

        response = self._session.delete(parse_url(self._base_url, 'invoices', invoice_id))

        if response.status_code != 204:
            return PaypalApiResponse.error(response)
        
        return PaypalApiResponse.success(response)

    def fully_update_invoice(self, invoice_id: str, invoice: Invoice, send_to_recipient: bool = True, send_to_invoicer: bool = True) -> PaypalApiResponse[Invoice]:
        """Calls the paypal API to fully update an invoice. This call does not support partial updates
        
        Arguments:
            invoice_id {str} -- invoice id
            invoice {Invoice} -- invoice with the updated info
        
        Keyword Arguments:
            send_to_recipient {bool} --  Indicates whether to send the invoice update notification to the recipient. (default: {True})
            send_to_invoicer {bool} --   Indicates whether to send the invoice update notification to the merchant. (default: {True})

        Returns:
            PaypalApiResponse -- Api operation response status with parsed objects within
        """
        params = { 'send_to_recipient': send_to_recipient, 'send_to_invoicer': send_to_invoicer }

        response = self._session.put(
            parse_url(self._base_url, 'invoices', invoice_id),
            json.dumps(invoice.to_dict()),
            params = params
        )

        # There seems to be a copy/paste mistake in the docs
        # It says no content but has a response within it.
        if response.status_code // 100 != 2:
            return PaypalApiResponse.error(response)

        json_response = response.json()

        if json_response:
            return PaypalApiResponse.success(response, Invoice.serialize_from_json(json_response))

        return PaypalApiResponse.success(response)


    def show_invoice_details(self, invoice_id: str) -> PaypalApiResponse[Invoice]:
        """Calls the paypal API to show details for an invoice.
        
        Arguments:
            invoice_id {str} -- invoice id

        Returns:
            PaypalApiResponse -- Api operation response status with parsed objects within
        """
        response = self._session.get(parse_url(self._base_url, 'invoices', invoice_id))

        if response.status_code != 200:
            return PaypalApiResponse.error(response)

        return PaypalApiResponse.success(response, Invoice.serialize_from_json(response.json()))

    def cancel_sent_invoice(
        self, invoice_id: str, subject: str, note: str, send_to_invoicer: bool,
        send_to_recipient: bool, additional_recipients: List[str] = []) -> PaypalApiResponse[Invoice]:
        """Calls the paypal API to cancel a sent invoice, and, optionally, send a notification about the cancellation 
           to the payer, merchant, and CC: emails.
        
        Arguments:
            invoice_id {str} -- invoice id
            subject {str} --  The subject of the email that is sent as a notification to the recipient.
            note {str} -- A note to the payer.
            send_to_invoicer {bool} -- Indicates whether to send a copy of the email to the merchant.
            send_to_recipient {bool} -- Indicates whether to send a copy of the email to the recipient.
            additional_recipients {List[str]} -- An array of one or more CC: emails to which notifications are sent.
             If ignored, a notification is sent to all CC: email addresses that are part of the invoice.

        Returns:
            PaypalApiResponse -- Api operation response status with parsed objects within
        """
        url = parse_url(self._base_url, 'invoices', invoice_id, 'cancel')

        body = json.dumps({
            'subject': subject,
            'note': note,
            'send_to_invoicer': send_to_invoicer,
            'send_to_recipient': send_to_recipient
        })

        if additional_recipients:
            body['additional_recipients'] = [{'email_address': x} for x in additional_recipients]

        response = self._session.post(url, body)

        if response.status_code != 204:
            return PaypalApiResponse.error(response)
        
        return PaypalApiResponse.success(response)

    def generate_qr_code(self, invoice_id: str, width: int = 500, height: int = 500, action: str = 'pay') -> PaypalApiResponse:
        """ Calls the paypal API to generate a QR code for an invoice. 
            The QR code is a PNG image in Base64-encoded format that corresponds to the invoice ID. 
            You can generate a QR code for an invoice and add it to a paper or PDF invoice. 
            When customers use their mobile devices to scan the QR code, they are redirected to the PayPal mobile payment flow where they can view the invoice and pay online with PayPal or a credit card.
            Before you get a QR code, you must create an invoice and send an invoice to move the invoice from a draft to payable state. 
            Do not include an email address if you do not want the invoice emailed.
        
        Arguments:
            invoice_id {str} -- existing invoice id
        
        Keyword Arguments:
            width {int} -- The width, in pixels, of the QR code image. Value is from 150 to 500 (default: {500})
            height {int} -- The height, in pixels, of the QR code image. Value is from 150 to 500 (default: {500})
            action {str} -- The type of URL for which to generate a QR code. Valid values are 'pay' and 'details'. (default: {'pay'})
        
        Returns:
            PaypalApiResponse -- Api operation response status containing the response
        """
        url = parse_url(self._base_url, 'invoices', invoice_id, 'generate-qr-code')
        body = json.dumps({ 'width': width, 'height': height, 'action': action })
        response = self._session.post(url, body)

        if response.status_code != 200:
            return PaypalApiResponse.error(response)
        
        return PaypalApiResponse.success(response)        

    def record_invoice_payment(self, invoice_id: str, payment_detail: PaymentDetail) -> PaypalApiResponse:
        """ Calls the API to record a payment for the invoice.
            If no payment is due, the invoice is marked as PAID. 
            Otherwise, the invoice is marked as PARTIALLY PAID.
        
        Arguments:
            invoice_id {str} -- id of the invoice
            payment_detail {PaymentDetail} -- payment details
        
        Returns:
            PaypalApiResponse -- Api operation response status containing the response
        """
        url = parse_url(self._base_url, 'invoices', invoice_id, 'payments')
        body = json.dumps({ k : v for k,v in payment_detail.to_dict().items() if v != None })

        response = self._session.post(url, body)

        if response.status_code != 204:
            return PaypalApiResponse.error(response)
        
        return PaypalApiResponse.success(response)        

    def delete_external_payment(self, invoice_id: str, transaction_id: str)  -> PaypalApiResponse:
        """ Deletes an external payment, by invoice ID and transaction ID.
        
        Arguments:
            invoice_id {str} -- id of the invoice
            transaction_id {str} --  The ID of the external payment transaction to delete.
        
        Returns:
            PaypalApiResponse -- Api operation response status containing the response
        """
        response = self._session.delete(parse_url(self._base_url, 'invoices', invoice_id, 'payments', transaction_id))

        if response.status_code != 204:
            return PaypalApiResponse.error(response)
        
        return PaypalApiResponse.success(response)

    def record_invoice_refund(self, invoice_id: str, refund_detail: RefundDetail)  -> PaypalApiResponse:
        """Calls the API to record a refund for the invoice.
           If all payments are refunded, the invoice is marked as REFUNDED. 
           Otherwise, the invoice is marked as PARTIALLY REFUNDED.
        
        Arguments:
            invoice_id {str} -- id of the invoice
            payment_detail {RefundDetail} -- payment details
        
        Returns:
            PaypalApiResponse -- Api operation response status containing the response
        """
        url = parse_url(self._base_url, 'invoices', invoice_id, 'refunds')
        body = json.dumps({ k : v for k,v in refund_detail.to_dict().items() if v != None })

        response = self._session.post(url, body)

        if response.status_code != 204:
            return PaypalApiResponse.error(response)
        
        return PaypalApiResponse.success(response)        
        
    def delete_external_refund(self, invoice_id: str, transaction_id: str)  -> PaypalApiResponse:
        """  Deletes an external refund, by invoice ID and transaction ID.
        
        Arguments:
            invoice_id {str} -- id of the invoice
            transaction_id {str} --  The ID of the external payment transaction to delete.
        
        Returns:
            PaypalApiResponse -- Api operation response status containing the response
        """
        response = self._session.delete(parse_url(self._base_url, 'invoices', invoice_id, 'refunds', transaction_id))

        if response.status_code != 204:
            return PaypalApiResponse.error(response)
        
        return PaypalApiResponse.success(response)

    def send_invoice_reminder(
        self, invoice_id: str, subject: str, note: str, send_to_invoicer: bool,
        send_to_recipient: bool, additional_recipients: List[str] = []) -> PaypalApiResponse[Invoice]:
        """Calls the paypal API to sends a reminder to the payer about an invoice, by ID. 
           In the JSON request body, include a notification object that defines the subject 
           of the reminder and other details. 
        
        Arguments:
            invoice_id {str} -- invoice id
            subject {str} --  The subject of the email that is sent as a notification to the recipient.
            note {str} -- A note to the payer.
            send_to_invoicer {bool} -- Indicates whether to send a copy of the email to the merchant.
            send_to_recipient {bool} -- Indicates whether to send a copy of the email to the recipient.
            additional_recipients {List[str]} -- An array of one or more CC: emails to which notifications are sent.
             If ignored, a notification is sent to all CC: email addresses that are part of the invoice.

        Returns:
            PaypalApiResponse -- Api operation response status with parsed objects within
        """
        url = parse_url(self._base_url, 'invoices', invoice_id, 'remind')

        body = json.dumps({
            'subject': subject,
            'note': note,
            'send_to_invoicer': send_to_invoicer,
            'send_to_recipient': send_to_recipient
        })

        if additional_recipients:
            body['additional_recipients'] = [{'email_address': x} for x in additional_recipients]

        response = self._session.post(url, body)

        if response.status_code != 204:
            return PaypalApiResponse.error(response)
        
        return PaypalApiResponse.success(response)

    def send_invoice(
        self, invoice_id: str, subject: str, note: str, send_to_invoicer: bool,
        send_to_recipient: bool, additional_recipients: List[str] = [], paypal_request_id: str = None) -> PaypalApiResponse[Invoice]:
        """Calls the paypal API to send or schedule an invoice, by ID, to be sent to a customer. The action depends on the invoice issue date:
            If the invoice issue date is current or in the past, sends the invoice immediately.
            If the invoice issue date is in the future, schedules the invoice to be sent on that date.
            To suppress the merchant's email notification, set the send_to_invoicer body parameter to false. 
            To send the invoice through a share link and not through PayPal, set the send_to_recipient parameter to false in the notification object. 
            The send_to_recipient parameter does not apply to a future issue date because the invoice is scheduled to be sent through PayPal on that date.
        
        Arguments:
            invoice_id {str} -- invoice id
            subject {str} --  The subject of the email that is sent as a notification to the recipient.
            note {str} -- A note to the payer.
            send_to_invoicer {bool} -- Indicates whether to send a copy of the email to the merchant.
            send_to_recipient {bool} -- Indicates whether to send a copy of the email to the recipient.

        Keyword Arguments:
            paypal_request_id {str} -- Paypal request id for idempotence. (default: {None})
            additional_recipients {List[str]} -- An array of one or more CC: emails to which notifications are sent. (default: {[]})

        Returns:
            PaypalApiResponse -- Api operation response status with parsed objects within
        """
        response = None
        url = parse_url(self._base_url, 'invoices', invoice_id, 'send')

        body = json.dumps({
            'subject': subject,
            'note': note,
            'send_to_invoicer': send_to_invoicer,
            'send_to_recipient': send_to_recipient
        })

        if additional_recipients:
            body['additional_recipients'] = [{'email_address': x} for x in additional_recipients]

        if paypal_request_id:
            response = self._session.post(url, body, headers = { 'PayPal-Request-Id' : paypal_request_id })
        else:
            response = self._session.post(url, body)

        if response.status_code // 100 != 2:
            return PaypalApiResponse.error(response)

        if response.status_code == 200:
            return PaypalApiResponse.success(response, Invoice.serialize_from_json(response.json()))

        return PaypalApiResponse.success(response)

    def search_invoices(self, page: int, page_size: int, total_required: bool, search: InvoiceSearchRequest) -> PaypalPage[Invoice]:
        """Searches for and lists invoices that match search criteria. 
           If you pass multiple criteria, the response lists invoices 
           that match all criteria.

        Arguments:
            page {int} -- current page
            page_size {int} -- page size
            total_required {bool} -- total count required
            search {InvoiceSearchRequest} -- search criteria to be matched
        
        Returns:
            PaypalPage[Invoice] -- The paged elements in paypal API paged response 
        """
        query_params = { page: page, page_size: page_size, total_required: total_required }
        
        response = self._session.post(
            parse_url(self._base_url, 'search-invoices'), 
            json.dumps(search.to_dict()), params = query_params
        )

        if response.status_code != 200:
            return PaypalPage.error(response)
        
        json_response = response.json()
        items = [ Invoice.serialize_from_json(x) for x in json_response['items']]
        links = [ ActionLink(x['href'], x['rel'], x.get('method', 'GET')) for x in json_response['links'] ]

        return PaypalPage.success(response, json_response.get('total_items'), json_response.get('total_pages'), items, links)

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
    
class InvoiceTemplateClient(ClientBase):
    """Client for invoice template resources
    """

    def __init__(self, base_url: str, session: PayPalSession):
            super().__init__(base_url, session)

    def create_template(self, template: Template, *, headers: dict = dict()) -> PaypalApiResponse:
        """Calls the Paypal API to create a template.
        
        Arguments:
            template {Template} -- object with all the required info.
        
        Returns:
            PaypalApiResponse[Template] -- The paypal API response
        """
        response = self._session.post(self._base_url, json.dumps(template.to_dict()), headers)

        if response.status_code != 200:
            return PaypalPage.error(response)

        parsed_data = Template.serialize_from_json(response.json()) if response.json() else None

        return PaypalApiResponse.success(response, parsed_data)
    
    def list_templates(self, page: int = 1, page_size: int = 20, fields: InvoiceListRequestField = InvoiceListRequestField.ALL) -> PaypalApiBulkResponse[Invoice]:
        """ Calls the paypal API to lists merchant-created templates with associated details. The associated details include 
            the emails, addresses, and phone numbers from the user's PayPal profile.
            The user can select which values to show in the business information section of their template.
        
        Keyword Arguments:
            page {int} -- current page index (default: {1})
            page_size {int} -- page size (how many elements per page) (default: {20})
            fields {InvoiceListRequestField} -- The fields to return in the response (default: {InvoiceListRequestField.NONE})
        
        Returns:
            PaypalApiBulkResponse[Invoice] -- A list of invoices
        """
        # TODO: There might be an error in the docs, the most logical response would be 
        # a page of templates, with the desired fields. This response must be tested.
        params = { 'page': page, 'page_size': page_size, 'fields': fields.name.lower() }

        response = self._session.get(self._base_url, params)

        if response.status_code != 200:
            return PaypalApiBulkResponse.error(response)

        return PaypalApiBulkResponse.success(response, Invoice.serialize_from_json(response.json()))
        
    def delete_template(self, template_id: str) -> PaypalApiResponse:
        """Deletes a template by id
        
        Arguments:
            template_id {str} -- The id of the template to be deleted
        
        Returns:
            PaypalApiResponse -- API Response.
        """
        response = self._session.delete(parse_url(self._base_url, template_id))
        return PaypalApiResponse.success(response) if response.status_code == 204 else PaypalApiResponse.error(response)
    
    def update_template(self, template_id: str, template: Template) -> PaypalApiResponse[Template]:
        """Fully updates a template
        
        Arguments:
            template_id {str} -- the template id
            template {Template} -- template info with updates
        
        Returns:
            PaypalApiResponse[Template] -- A response that might contain the template
        """
        response = self._session.put(parse_url(self._base_url, template_id), json.dumps(template.to_dict()))

        # TODO: The docs are inconsistent on this call response. Test manually
        if response.status_code // 100 != 2:
            return PaypalApiResponse.error(response)
        
        parsed_data = Template.serialize_from_json(response.json()) if response.json() else None
        return PaypalApiResponse.success(response, parsed_data)
    
    def show_template_details(self, template_id: str) -> PaypalApiResponse[Template]:
        """Shows the details for a template by it's id
        
        Arguments:
            template_id {str} -- The template id
        
        Returns:
            PaypalApiResponse[Template] -- Response status with a Template object
        """
        response = self._session.get(parse_url(self._base_url, template_id))

        if response.status_code != 200:
            return PaypalApiResponse.error(response)

        return PaypalApiResponse.success(response, Invoice.serialize_from_json(response.json()))

    @classmethod
    def for_session(cls: I, session: PayPalSession) -> I:
        """Creates a client from a given paypal session
        
        Arguments:
            cls {T} -- class reference
            session {PayPalSession} -- the paypal session
        
        Returns:
            T -- an instance of Dispute client with the right configuration by session mode
        """
        base_url = parse_url(_LIVE_RESOURCE_BASE_URL if session.session_mode.is_live() else _SANDBOX_RESOURCE_BASE_URL, 'templates')
        return cls(base_url, session)