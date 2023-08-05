# Bearer Agent

[![Build Status](https://build.bearer.tech/api/badges/Bearer/python-agent/status.svg)](https://build.bearer.tech/Bearer/python-agent)

Observe, control and receive alerts on your third-party APIs by adding the
[Bearer agent](https://www.bearer.sh) to your Python application.

## Documentation

The documentation is hosted at https://python.docs.bearer.sh/

## Installation

The Bearer agent requires **Python 3.x >= 3.5**.

Install from PyPI:

```sh
$ pip install bearer-agent
```

Then set up the Bearer agent with your Secret Key (available on the
[Bearer dashboard](https://app.bearer.sh/keys)):

```python
import bearer_agent

bearer_agent.init(secret_key="YOUR_BEARER_SECRET_KEY")
```

## Keeping your data protected

We recommend you sanitize your data before sending it to the Bearer dashboard.
We think it's best to  setup the sanitization level that best suits your needs.
An example using the default values is as follows:

```python
bearer_agent.init(
    strip_sensitive_data=True,
    strip_sensitive_keys=(
        "^authorization$|"
        "^password$|"
        "^secret$|"
        "^passwd$|"
        "^api.?key$|"
        "^access.?token$|"
        "^auth.?token$|"
        "^credentials$|"
        "^mysql_pwd$|"
        "^stripetoken$|"
        "^card.?number.?$|"
        "^secret$|"
        "^client.?id$|"
        "^client.?secret$"
    ),
    strip_sensitive_regex=(
        r"[a-zA-Z0-9]{1}[a-zA-Z0-9.!#$%&’*+=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*|"
        r"(?:\d[ -]*?){13,16}"
    )
)
```

## Compatibility matrix

### Python3 :

On Python 3.x (>= 3.5) bearer support the following:

* [http.client](https://docs.python.org/3/library/http.client.html) for Python >= 3.6
* [urllib3](https://github.com/urllib3/urllib3) : 
* [requests](https://requests.readthedocs.io/en/master/) 
* [httpcore](https://www.encode.io/httpcore/) >= 0.9 (both HTTP 1.1 and HTTP 2)
* [httpx](https://www.python-httpx.org) >= 0.12
* [Twisted](https://twistedmatrix.com/trac/) >= 19.2
* [aiohttp](https://docs.aiohttp.org/en/stable/) >= 3.6.2

On Python 2.7, bearer support the following client Library or application based on:

* [httplib](https://docs.python.org/2/library/httplib.html?highlight=httplib)
* [urllib3](https://github.com/urllib3/urllib3) : 
* [requests](https://requests.readthedocs.io/en/master/) 
* [Twisted](https://twistedmatrix.com/trac/) >= 19.2


## Development

### Running tests

To run a format check (black), the linter (flake8) and tests (pytest):

```sh
$ tox
```

To only run the tests:

```sh
$ tox -e py37
```

### Git hooks

There are Git hooks to format the code and run the linter when committing.

Install https://pre-commit.com/ and then run:

```sh
$ pre-commit install
```