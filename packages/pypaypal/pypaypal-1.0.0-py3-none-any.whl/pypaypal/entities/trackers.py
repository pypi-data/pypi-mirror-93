"""
    Module with all tracking related entities 
"""

from typing import Type
from datetime import datetime

import dateutil.parser
from pypaypal.entities.base import T, PayPalEntity, ResponseType, ActionLink

class Tracker(PayPalEntity):
    """
        Object representation of a paypal tracker
    """
    def __init__(self, transaction_id: str, tracking_number: int, status: str, carrier: str, **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.status = status
        self.carrier = carrier
        self.transaction_id = transaction_id
        self.tracking_number = tracking_number
        self.quantity = self._json_response.get('quantity') or kwargs.get('quantity')
        self.notify_buyer = self._json_response.get('notify_buyer') or kwargs.get('notify_buyer')
        self._shipment_date = self._json_response.get('shipment_date') or kwargs.get('shipment_date')
        self._last_updated_time = self._json_response.get('last_updated_time') or kwargs.get('last_updated_time')
        self.carrier_name_other = self._json_response.get('carrier_name_other') or kwargs.get('carrier_name_other')
        self.postage_payment_id = self._json_response.get('postage_payment_id') or kwargs.get('postage_payment_id')
        self.links = [ActionLink(x['href'], x['rel'], x.get('method', 'GET')) for x in self._json_response.get('links', [])]
        self.tracking_number_validated = self._json_response.get('tracking_number_validated') or kwargs.get('tracking_number_validated')

    @property
    def shipment_date(self) -> datetime:
        try:
            return datetime.strptime(self._shipment_date, '%Y-%m-%d') if self._shipment_date else None
        except:
            return None

    @property
    def last_updated_time(self) -> datetime:
        try:
            return dateutil.parser.parse(self._last_updated_time) if self._last_updated_time else None
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
        return next(filter(lambda x: x.rel == 'replace', self.links), None)

    @property
    def create_link(self) -> ActionLink:
        """Retrieves the link to create a tracker or add a tracker to an order
        
        Returns:
            ActionLink -- The link for requesting a create operation in the API.
        """
        return next(filter(lambda x: x.rel == 'create', self.links), None)

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        return cls(
            json_data['transaction_id'], json_data['tracking_number'], json_data['status'],
            json_data['carrier'], json_response= json_data, response_type = response_type
        )
