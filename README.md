<p align="center">
  <a href="https://www.inwx.com/en/" target="_blank">
    <img src="https://images.inwx.com/logos/inwx.png">
  </a>
</p>

INWX Domrobot Python 3 Client
=========
You can access all functions of our frontend via our API, which is available via the XML-RPC or JSON-RPC protocol and thus can be easily consumed with all programming languages.

There is also an OT&E test system, which you can access via [ote.inwx.com](https://ote.inwx.com/en/). Here you will find the known web interface which is using a test database. On the OT&E system no actions will be charged. So you can test as much as you like there.

Documentation
------
You can view a detailed description of the API functions in our documentation. You can find the online documentation [by clicking here](https://www.inwx.de/en/help/apidoc).

If you still experience any kind of problems don't hesitate to contact our [support via email](mailto:support@inwx.de).

Installation
-------
The recommended way is via pip:

```bash
pip install inwx-domrobot
```

You can find more information about the package on [pypi.org](https://pypi.org/project/inwx-domrobot).

Example
-------

```python
from INWX.Domrobot import ApiClient

username = ''
password = ''
domain = 'my-test-domain-which-is-definitely-not-registered6737.com'

api_client = ApiClient(api_url=ApiClient.API_OTE_URL, debug_mode=True)

login_result = api_client.login(username, password)

if login_result['code'] == 1000:
    domain_check_result = api_client.call_api(api_method='domain.check', method_params={'domain': domain})

    if domain_check_result['code'] == 1000:
        checked_domain = domain_check_result['resData']['domain'][0]

        if checked_domain['avail']:
            print(domain + ' is still available!')
        else:
            print('Unfortunately, ' + domain + ' is already registered.')

    else:
        raise Exception('Api error while checking domain status. Code: ' + str(domain_check_result['code'])
                        + '  Message: ' + domain_check_result['msg'])
    api_client.logout()
else:
    raise Exception('Api login error. Code: ' + str(login_result['code']) + '  Message: ' + login_result['msg'])
```

You can also have a look at the [example folder](INWX/examples) in the project for even more info.

License
----

MIT
