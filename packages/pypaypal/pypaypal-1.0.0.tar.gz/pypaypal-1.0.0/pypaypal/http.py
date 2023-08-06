"""Module with basic http constants & session handling.
"""
import urllib.parse

from enum import Enum
from abc import ABC, abstractmethod

from requests import ( 
    get, post, put, patch, delete 
)

from requests.auth import HTTPBasicAuth

from typing import NamedTuple
from datetime import datetime, timedelta

from pypaypal.errors import IdentityError, ExpiredSessionError

"""
    Live PayPal api base URL.

    This library is intended for paypal integration with the v2 api if possible.
"""
LIVE_API_BASE_URL = 'https://api.paypal.com/v2/'

"""
    Sandbox PayPal api base URL.

    This library is intended for paypal integration with the v2 api if possible.
"""
SANDBOX_API_BASE_URL = 'https://api.sandbox.paypal.com/v2/'

"""Live PayPal api base URL for v1 api requests.
"""
LEGACY_LIVE_API_BASE_URL = 'https://api.paypal.com/v1/'

"""Sandbox PayPal api base URL for v1 api requests.
"""
LEGACY_SANDBOX_API_BASE_URL = 'https://api.sandbox.paypal.com/v1/'

class AuthType(Enum):
    """
        Enumerated constants for the session type
    """
    BASIC = 1
    TOKEN = 2
    REFRESHABLE = 3

class SessionMode(Enum):
    """Session mode
    """
    LIVE = 1
    SANDBOX = 2

    def is_live(self) -> bool:
        """Boolean flag dictating if this instance is a live session mode or not
        
        Returns:
            bool -- true if live false if sandbox
        """
        return self == SessionMode.LIVE

class SessionStatus(Enum):
    ACTIVE = 1
    EXPIRED = 2
    DISPOSED = 3

class PayPalToken(NamedTuple):
    """Paypal access token wrapper.
    """
    scope: str
    access_token: str
    token_type: str
    app_id: str
    expires_in: int
    nonce: str
    requested_at: datetime

    def is_expired(self) -> bool:
        """
            Checks if the token is expired
        """
        return self.requested_at + timedelta(seconds = self.expires_in) < datetime.now()
    
    @classmethod
    def serialize(cls, json_data: dict):
        """Serializes a paypal json OAuthResponse into an instance
        """
        return cls(
            json_data['scope'], json_data['access_token'], json_data['token_type'], 
            json_data['app_id'], json_data['expires_in'], json_data['nonce'], datetime.now()
        )

def parse_url(base: str, *args: str) -> str:
    """Safely parses a web url
    """
    # Making sure the base ends with '/'
    base = base.strip('/') + '/'
    if len(args) > 1:
        arg = args[0].strip('/')
        return parse_url(urllib.parse.urljoin(base, arg), *args[1:])
    return urllib.parse.urljoin(base, args[0].strip('/'))

def _authenticate(client_id: str, secret:str, mode: SessionMode) -> PayPalToken:
    """Basic authentication that returns a PayPalToken
    
    Arguments:
        client_id {str} -- paypal client id
        secret {str} -- paypal client secret
        mode {SessionMode} -- Desired session mode (LIVE or SANDBOX)
    
    Raises:
        IdentityError: If the user fails to authenticate
    
    Returns:
        PayPalToken -- An immutable object with the token information
    """
    base = LEGACY_LIVE_API_BASE_URL if mode == SessionMode.LIVE else LEGACY_SANDBOX_API_BASE_URL
    url = parse_url(base, '/oauth2/token')
    body = { 'grant_type' : 'client_credentials' }

    headers = {        
        'Accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = post(url, body, None, auth=HTTPBasicAuth(client_id, secret), headers=headers)

    if response.status_code != 200:
        raise IdentityError(response)

    return PayPalToken.serialize(response.json())

class PayPalSession(ABC):
    """PayPal session abstraction
    """
    def __init__(self, auth_type: AuthType, session_mode: SessionMode, token: PayPalToken):
        """Constructor
        
        Arguments:
            auth_type {AuthType} -- The instance session type
            session_mode {SessionMode} -- The instance session mode
            token {PayPalToken} -- The instance initial access token
        """
        self._paypal_token = token
        self.auth_type = auth_type
        self.session_mode = session_mode
        self.status = SessionStatus.ACTIVE
    
    @abstractmethod
    def get(self, url: str, params:dict=None, **kwargs):
        """Secured get request
        
        Arguments:
            url {str} -- The request URL
        
        Keyword Arguments:
            params {dict} -- query string parameters (default: {None})
    
        Raises:
            ExpiredSessionError: If the session is in an invalid state

        Returns:
            An http response
        """
        pass

    @abstractmethod
    def post(self, url: str, body, **kwargs):
        """Secured post request
        
        Arguments:
            url {str} -- Request URL
            body {[type]} -- Request body
        """
        pass

    @abstractmethod
    def put(self, url: str, body, **kwargs):
        """Secured put request
        
        Arguments:
            url {str} -- Request URL
            body {[type]} -- Request body
        """
        pass

    @abstractmethod
    def patch(self, url: str, body, **kwargs):
        """Secured patch request
        
        Arguments:
            url {str} -- Request URL
            body {[type]} -- Request body
        """
        pass

    @abstractmethod
    def delete(self, url: str, **kwargs):
        """Secured patch request
        
        Arguments:
            url {str} -- Request URL
        """
        pass

    @abstractmethod
    def _dispose(self):
        """Disposes this instance
        """
        pass

    def _prepare_headers(self, token: PayPalToken, custom_headers:dict=None) -> dict:
        """Gets the headers to be used on every request
        
        Arguments:
            token {PayPalToken} -- access token
        
        Keyword Arguments:
            custom_headers {dict} -- custom headers (default: {None})
        
        Returns:
            dict -- a merged dictionary with basic and custom headers
        """
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'{token.token_type} {token.access_token}'
        }

        return { **headers, **custom_headers } if custom_headers else headers

    def __enter__(self):
        return self
    
    def __exit__(self, type, value, traceback):
        self._dispose()

class _OAuthSession(PayPalSession):
    """PayPal session obj for request with OAuthToken headers.

        A standard session with a finite lifespan,
        once the session is expired this instance will not be valid for further
        requests.
    """
    def __init__(self, session_mode: SessionMode, token: PayPalToken):
        super().__init__(AuthType.TOKEN, session_mode, token)
    
    def _check_token(self) -> PayPalToken:
        if self.status == SessionStatus.ACTIVE and (self._paypal_token == None or self._paypal_token.is_expired()):
            self.status = SessionStatus.EXPIRED
        
        if self.status != SessionStatus.ACTIVE:        
            raise ExpiredSessionError(self)

        return self._paypal_token

    def get(self, url: str, params:dict=None, **kwargs):
        kwargs['headers'] = self._prepare_headers(self._check_token(), kwargs.get('headers'))
        return get(url, params, **kwargs)

    def post(self, url: str, body, **kwargs):
        kwargs['headers'] = self._prepare_headers(self._check_token(), kwargs.get('headers'))
        return post(url, body, None, **kwargs)

    def put(self, url: str, body, **kwargs):
        kwargs['headers'] = self._prepare_headers(self._check_token(), kwargs.get('headers'))
        return put(url, body, **kwargs)

    def patch(self, url: str, body, **kwargs):
        kwargs['headers'] = self._prepare_headers(self._check_token(), kwargs.get('headers'))
        return patch(url, body, **kwargs)

    def delete(self, url: str, **kwargs):
        kwargs['headers'] = self._prepare_headers(self._check_token(), kwargs.get('headers'))
        return delete(url, **kwargs)

    def _dispose(self):
        self._paypal_token = None
        self.status = SessionStatus.DISPOSED

    def __repr__(self):
        return f'_OAuthSession(session_mode={self.session_mode}, status={self.status})'

    def __str__(self):
        return f'_OAuthSession(session_mode={self.session_mode}, status={self.status})'
    
class _BasicAuthSession(PayPalSession):
    """PayPal session obj for request with Basic Authorization.

        A session with an indefinite lifespan,
        all requests will use basic authorization which means that
        the client & secret will always travel through the network.
    """
    def __init__(self, session_mode: SessionMode, token: PayPalToken, client: str, secret: str):
        super().__init__(AuthType.BASIC, session_mode, token)
        self._client = client
        self._secret = secret
    
    def _check_token(self) -> PayPalToken:
        if  self._paypal_token != None and self._paypal_token.is_expired():
            self._paypal_token = None
        
        if self.status != SessionStatus.ACTIVE:
            raise ExpiredSessionError(self)

        return self._paypal_token

    def get(self, url: str, params:dict=None, **kwargs):
        token = self._check_token()        
        if token:
            # If there's a valid token we might as well use it
            kwargs['headers'] = self._prepare_headers(token, kwargs.get('headers'))
        else:
            kwargs['auth'] = HTTPBasicAuth(self._client, self._secret)
        
        response = get(url, params, **kwargs)        
        if response.status_code == 401:
            raise IdentityError(response)
        return response

    def post(self, url: str, body, **kwargs):
        token = self._check_token()        
        if token:
            # If there's a valid token we might as well use it
            kwargs['headers'] = self._prepare_headers(token, kwargs.get('headers'))
        else:
            kwargs['auth'] = HTTPBasicAuth(self._client, self._secret)

        response = post(url, body, None, **kwargs)        
        if response.status_code == 401:
            raise IdentityError(response)
        return response

    def put(self, url: str, body, **kwargs):
        token = self._check_token()        
        if token:
            # If there's a valid token we might as well use it
            kwargs['headers'] = self._prepare_headers(token, kwargs.get('headers'))
        else:
            kwargs['auth'] = HTTPBasicAuth(self._client, self._secret)
        
        response = put(url, body, **kwargs)
        if response.status_code == 401:
            raise IdentityError(response)
        return response

    def patch(self, url: str, body, **kwargs):
        token = self._check_token()        
        if token:
            # If there's a valid token we might as well use it
            kwargs['headers'] = self._prepare_headers(token, kwargs.get('headers'))
        else:
            kwargs['auth'] = HTTPBasicAuth(self._client, self._secret)
        
        response = patch(url, body, **kwargs)
        if response.status_code == 401:
            raise IdentityError(response)
        return response

    def delete(self, url: str, **kwargs):
        token = self._check_token()        
        if token:
            # If there's a valid token we might as well use it
            kwargs['headers'] = self._prepare_headers(token, kwargs.get('headers'))
        else:
            kwargs['auth'] = HTTPBasicAuth(self._client, self._secret)

        response = delete(url, **kwargs)
        if response.status_code == 401:
            raise IdentityError(response)
        return response

    def _dispose(self):
        self._client = None
        self._secret = None
        self._paypal_token = None
        self.status = SessionStatus.DISPOSED
    
    def __repr__(self):
        return f'_BasicAuthSession(session_mode={self.session_mode}, status={self.status}, client={self._client})'

    def __str__(self):
        return f'_BasicAuthSession(session_mode={self.session_mode}, status={self.status}, client={self._client})'

class _RefreshableSession(PayPalSession):
    """PayPal session obj for request with with OAuthToken headers and Basic Authorization.

        A mixed session using the standard _OAuthSession approach for regular requests
        and a _BasicAuthSession request to perform a token refresh. This gives the session
        and indefinite lifespan and a limited number of Basic Auth requests with a client &
        secret network roundtrips.
        
        This session can receive flags to limit the refresh count.
    """
    def __init__(self, session_mode: SessionMode, token: PayPalToken, client:str, secret: str, refresh_limit:int=None):
        super().__init__(AuthType.REFRESHABLE, session_mode, token)
        self._client = client
        self._secret = secret
        self._refresh_limit = refresh_limit
    
    def _check_token(self) -> PayPalToken:
        if self.status == SessionStatus.ACTIVE and (self._paypal_token == None or self._paypal_token.is_expired()):
            self.status = SessionStatus.EXPIRED
        
        if self.status == SessionStatus.EXPIRED and (self._refresh_limit == None or self._refresh_limit > 0):
            self._refresh_limit-=1
            self._paypal_token = _authenticate(self._client, self._secret, self.session_mode)
            self.status = SessionStatus.ACTIVE

        if self.status != SessionStatus.ACTIVE:
            raise ExpiredSessionError(self)

        return self._paypal_token

    def get(self, url: str, params:dict=None, **kwargs):
        kwargs['headers'] = self._prepare_headers(self._check_token(), kwargs.get('headers'))
        return get(url, params, **kwargs)

    def post(self, url: str, body, **kwargs):
        kwargs['headers'] = self._prepare_headers(self._check_token(), kwargs.get('headers'))
        return post(url, body, None, **kwargs)

    def put(self, url: str, body, **kwargs):
        kwargs['headers'] = self._prepare_headers(self._check_token(), kwargs.get('headers'))
        return put(url, body, **kwargs)

    def patch(self, url: str, body, **kwargs):
        kwargs['headers'] = self._prepare_headers(self._check_token(), kwargs.get('headers'))
        return patch(url, body, **kwargs)

    def delete(self, url: str, **kwargs):
        kwargs['headers'] = self._prepare_headers(self._check_token(), kwargs.get('headers'))
        return delete(url, **kwargs)    

    def _dispose(self):
        self._client = None
        self._secret = None
        self._refresh_limit = 0
        self._paypal_token = None
        self.status = SessionStatus.DISPOSED

    def __repr__(self):
        return f'_RefreshableSession(session_mode={self.session_mode}, status={self.status}, client={self._client})'

    def __str__(self):
        return f'_RefreshableSession(session_mode={self.session_mode}, status={self.status}, client={self._client})'

def session_from_token(token: PayPalToken, mode: SessionMode) -> PayPalSession:
    """Creates a session from a given token
    
    Arguments:
        token {PayPalToken} -- A valid paypal token instance 
        mode {SessionMode} -- Desired session mode (LIVE or SANDBOX)
    
    Returns:
        PayPalSession -- A paypal session for all the api http requests
    """
    return _OAuthSession(mode, token)

def authenticate(client_id: str, secret: str, mode: SessionMode, auth_type: AuthType=AuthType.REFRESHABLE, **kwargs) -> PayPalSession:
    """Creates a session for a given user. If a session handles any kind of 
       flags it can be received as a kwarg. 
       
       Supported flags -> 'refresh_limit' for refreshable sessions.

    Arguments:
        client_id {str} -- paypal client id
        secret {str} -- paypal client secret
        mode {SessionMode} -- Desired session mode (LIVE or SANDBOX)
        auth_type {AuthType} -- Desired session type (BASIC, TOKEN, REFRESHABLE)

    Raises:
        IdentityError: If the user fails to authenticate
    
    Returns:
        PayPalSession -- A paypal session for all the api http requests
    """
    if auth_type == AuthType.TOKEN:
        return session_from_token(_authenticate(client_id, secret, mode), mode)    
    token = _authenticate(client_id, secret, mode)
    if auth_type == AuthType.BASIC:
        return _BasicAuthSession(mode, token, client_id, secret)
    return _RefreshableSession(mode, token, client_id, secret, kwargs.get('refresh_limit'))
