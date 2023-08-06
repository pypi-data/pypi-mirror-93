# pyoauthbridge

pyoauthbridge is a official python library to communicate with tradelab api.

### Prerequisites

* Please refer the document http://primusapi.tradelab.in/webapi/
* The API uses oauth2 protocol . You will need following to get started -(Please contact your broker team to get these details)
```
base_url
auth_token
```

### Installation

pyoauthbridge requires [python](https://www.python.org/) v3+ to run.

Install the package using pip.

```sh
$ pip install pyoauthbridge
```

### How to use

import package
```sh
from pyoauthbridge import Connect
```
login
```sh
conn = Connect(base_url)
token_json = conn.user_login("JOHN", "password")
twofa_token = token_json['data']['twofa']['twofa_token']
auth_token_json = conn.twofa("22", "answer", twofa_token)
```
set token
```sh
auth_token = auth_token_json['data']['auth_token']
conn.set_token(auth_token)
```

implementation
```sh
payload = {
    'client_id': 'JOHN'
}
res = conn.fetch_profile(payload)
print(res)
```
