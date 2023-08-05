# Pureport Python SDK

![test](https://github.com/pureport/pureport-python/workflows/test/badge.svg) [![Documentation Status](https://readthedocs.org/projects/pureport-python/badge/?version=latest)](https://pureport-python.readthedocs.io/en/latest/?badge=latest)


The Pureport Python Client provides a Python programmatic interface to the 
Pureport REST API.  The Pureport Python Client is predominately a session and 
transport library designed to making interfacing with the API simple.  For 
more information about Pureport or to sign up for an account please visit the
[website](http://www.pureport.com).

## Installing

You can install the Pureport Python Client using `pip`.

```
   $ pip install pureport-python
```

This project can be run directly from source as well using `pipenv`.  To 
get started with running this from source, be sure you have `pipenv` 
installed on your local system.  For information about `pipenv` please see 
their website [here](https://pipenv.pypa.io/en/latest/)

```
   $ git clone https://github.com/pureport/pureport-python
   $ cd pureport-python
   $ pipenv shell
   $ pipenv install -d
   $ python setup.py develop
```

### Supported Python Versions

The Pureport Python Client supports Python 3.5+

## Getting Started

In order to use this SDK, you must first have a valid Pureport acccount 
and have created and downloaded API keys.  Once you have obtained your
Pureport API keys, simply create environment variables for the API
key and API secret.

To get started, either sign up or login to your existing Pureport account at 
https://console.pureport.com and generate your API keys.

Once the keys are generated, set the required environment variables.


```
   export PUREPORT_API_KEY="<your api key here>"
   export PUREPORT_API_SECRET="<your api secret here>"
```

This implementation provides a class for interfacing with the Pureport API.
The session class handles authenticating to the API and provides 
convenience methods for sending requests to the server.

```
   from pureport.session import Session
   from pureport.credentials import default

   session = Session(*default())
   response = session.get("/accounts")
   print(response.json)
```

The library also provides a set of functional bindings to the Pureport
API using the OpenAPI spec file.  Bindings are not enabled by default 
when you create a new instance of `Sesssion`.  To add bindings to a
`Session` object, call `make_bindings()`. 

```
   from pureport.session import Session
   from pureport.credentials import default

   session = Session(*default())
   session.make_bindings()
 
   session.find_all_accounts()
```

Alternatively you can also enable bindings to be created at session
initialization.

```
   from pureport.session import Session
   from pureport.credentials import default

   session = Session(*default(), automake_bindings=True)
   session.find_all_accounts()
```

For details and documentation of the Pureport Fabric API, please check 
the API section of the [Pureport Console](https://console.pureport.com)

## Contributing

This project provides an easy to use implementation for consuming the 
Pureport Fabric API for building and managing multicloud networks.  We 
gladly accept contributions to this project from open source community
contributors. 

There are many ways to contribute to this project from opening issues, 
providing documentation updates and, of course, providing code.  If you 
are considering contributing to this project, please review the 
guidlines for contributing to this project found [here](CONTRIBUTING.md).

Also please be sure to review our open source community Code of Conduct
found [here](CODE_OF_CONDUCT.md).

## License

This project is licenses under the MIT open source license.
