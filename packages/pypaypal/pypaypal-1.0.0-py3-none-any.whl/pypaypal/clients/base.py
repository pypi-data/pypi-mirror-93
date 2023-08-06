"""
    Base module with common needs for every resource client
"""

from typing import Type

from pypaypal.http import PayPalSession

from pypaypal.entities.base import ( 
    T, 
    ActionLink, 
    PaypalPage, 
    ResponseType,
    RequestMethod, 
    PaypalApiResponse
)

class ClientBase:
    """
        Base client class for every resource client.
    """
    def __init__(self, base_url: str, session: PayPalSession):
        """Class ctor
        
        Arguments:
            base_url {str} -- The base url for the resource group
            session {PayPalSession} -- The paypal session that will perform the requests
        """
        self._session = session
        self._base_url = base_url
    
    def _get_element_details(self, url: str, element_id: str, element_class: Type[T], response_type: ResponseType) -> PaypalApiResponse[T]:
        """Calls the API to get an element detail by it's id
        
        Arguments:
            element_id {str} -- The element identifier
            element_class {[type]} -- serializable class reference
        
        Returns:
            PaypalApiResponse[T] -- A response wrapper with the object & operation result
        """

    def _page_from_link(self, link: ActionLink, element_key: str, element_class: Type[T]) -> PaypalPage[T]:
        """Performs an API call to get a page of elements
        
        Arguments:
            link {ActionLink} -- Page action link (HATEOAS)
            element_key {str} -- The key for the element lists inside the page json
            element_class {T} -- class reference of a PayPalEntity subclass
        Returns:
            PaypalPage[T] -- A page with the desired elements
        """
        api_response = self._execute_action_link(link, None)

        if api_response.status_code != 200:
            return PaypalPage(True, api_response, 0, 0, [], [])
        
        json_response = api_response.json()
        total_items = json_response.get('total_items', 0)
        total_pages = json_response.get('total_pages', 0)
        elements = [ element_class.serialize_from_json(x) for x in json_response[element_key]]
        links = [ActionLink(x['href'], x['rel'], x.get('method', 'GET')) for x in json_response['links']]

        return PaypalPage(False, api_response, total_items, total_pages, elements, links)

    def _remove_null_entries(self, dictionary: dict):
        """Cleans a dictionary removing null entries and invalid keys
        
        Arguments:
            dictionary {dict} -- The dictionary to be checked
            valid_keys {set} -- The keys that should not be deleted
        """
        keys = list(dictionary.keys())
        for k in keys:
            if dictionary.get(k) == None:
                del dictionary[k]

    def _clean_dictionary(self, dictionary: dict, valid_keys: set):
        """Cleans a dictionary removing null entries and invalid keys
        
        Arguments:
            dictionary {dict} -- The dictionary to be checked
            valid_keys {set} -- The keys that should not be deleted
        """
        keys = list(dictionary.keys())
        for k in keys:
            if dictionary.get(k) == None or not k in valid_keys:
                del dictionary[k]

    def _execute_action_link(self, link: ActionLink, body: str, **kwargs):
        """Executes an action link from a given entity
        
        Supported kwargs: 
            params for query string parameters in GET requests
            every other kwarg supported by the requests library

        Arguments:
            link {ActionLink} -- The action link to be executed
            body {str} -- the action link body if needed
        """
        url = link.href
        method = link.method

        if method == RequestMethod.POST:
            return self._session.post(url, body, **kwargs)
        elif method == RequestMethod.PUT:
            return self._session.put(url, body, **kwargs)
        elif method == RequestMethod.PATCH:
            return self._session.patch(url, body, **kwargs)
        elif method == RequestMethod.DELETE:
            return self._session.delete(url, **kwargs)
        else: 
            # Defaulting to get
            return self._session.get(url, kwargs.pop('params',None), **kwargs)