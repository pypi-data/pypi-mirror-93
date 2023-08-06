# PyPaypal Client Library

Unofficial python Paypal API client with v1 and v2 endpoint support and strongly type hinted objects.

Currently developed API calls:

* Invoicing
* Orders
* Payment Expirience
* Payments
* Payouts
* Paypal Sync
* Referenced Payouts
* Subscriptions
* Webhooks

Developed based on the available documentation at the [official Paypal API reference][1].

## Basic Usage

### Instalation 

Install from PyPi using pip

```sh
pip install pypaypal
```

### Starting a session

Sessions can be started by importing [**http**][2] module which supports different ways of authentication and session types.

You can start a session using the "**for_token**" method providing a valid access token object and a session mode (LIVE or SANDBOX), for example:

```python
import json

from pypaypal.http import (
    SessionMode, 
    PayPalToken,
    session_from_token
)

token = PayPalToken.serialize(json.loads('A paypal OAuth token'))

# Live session from a token
live_session = session_from_token(
    token=token, 
    session_mode= SessionMode.LIVE
)

# Sandbox session from a token
sandbox_session = session_from_token(
    token=token, 
    session_mode= SessionMode.SANDBOX
)
```

Alternatively you can start a session by authenticating via the client library.

In order to start a session based on authentication you need to specify the following:

* **client**: API client ID.

* **secret**: API client secret.

* **auth_type**: Which authorization type you'll use to communicate with the API. These can be:

    - **BASIC**: Using basic auth for all request.

    - **TOKEN**: Authenticate once and use a token and keep the session until the token expires.

    - **REFRESHABLE**: Mix of BASIC and TOKEN to limit the amount of times the credentials are send back and forth a network. basically you authenticate the first time and get a token and the process will refresh the token logging in again with the credentials for an specified amount of sessions.

* **mode**: Session mode (LIVE or SANDBOX) 

### Authentication samples

Python samples for each auth method.

```python
from pypaypal.http import authenticate, SessionMode

session_mode = SessionMode.SANDBOX

# Starting a session with basic auth
basic_session = authenticate(client, secret, session_mode, AuthType.BASIC)

# Authenticate to start a session with a one time token
token_session = authenticate(client, secret, session_mode, AuthType.TOKEN)

# Starting a session with refreshable tokens (refreshing up to 3 times)
refresh_session = authenticate(
    client, 
    secret, 
    session_mode, 
    AuthType.REFRESHABLE,
    refresh_limit=3
)
```

### Making requests

After the session is stablished you can perform requests by importing the client library of your choice, all requests objects and calls are based on the [official Paypal API reference][1].

Sample request

```python
import json

from pypaypal.http import (
    SessionMode, 
    PayPalToken,
    session_from_token
)

from pypaypal.clients.orders import OrderClient
from pypaypal.entities.base import PaypalApiResponse

order_id = 'some id'
token = PayPalToken.serialize(json.loads('A paypal OAuth token'))

# Sandbox session from a token
sandbox_session = session_from_token(
    token=token, 
    session_mode= SessionMode.SANDBOX
)

client = OrderClient.create(sandbox_session)
response: PaypalApiResponse = client.show_order_details(order_id)
```

[1]:https://developer.paypal.com/docs/api/overview/
[2]:https://github.com/ivcuello/pypaypal/blob/master/pypaypal/http.py