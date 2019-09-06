from INWX.Domrobot import ApiClient

username = ''
password = ''
domain = 'my-test-domain-which-is-definitely-not-registered6737.com'

# By default you ApiClient uses the test api (OT&E). If you want to use the production/live api
# we have a constant named API_LIVE_URL in the ApiClient class. Just set api_url=ApiClient.API_LIVE_URL and you're good.
# You can also choose between XML-RPC and JSON-RPC by setting api_type=ApiType.XML_RPC or api_type=ApiType.JSON_RPC
api_client = ApiClient(api_url=ApiClient.API_OTE_URL, debug_mode=True)

# If you have 2fa enabled, take a look at the documentation of the ApiClient#login method to get further
# information about the login, especially the shared_secret parameter.
login_result = api_client.login(username, password)

# login was successful
if login_result['code'] == 1000:

    # Make an api call and save the result in a variable.
    # We want to check if a domain is available, so we call the api method 'domain.check'.
    # ApiClient#call_api returns the api response as a dict.
    domain_check_result = api_client.call_api(api_method='domain.check', method_params={'domain': domain})

    # request was successful
    if domain_check_result['code'] == 1000:

        # get the first domain in the result array 'domain'
        checked_domain = domain_check_result['resData']['domain'][0]

        if checked_domain['avail']:
            print(domain + ' is still available!')
        else:
            print('Unfortunately, ' + domain + ' is already registered.')

    else:
        raise Exception('Api error while checking domain status. Code: ' + str(domain_check_result['code'])
                        + '  Message: ' + domain_check_result['msg'])

    # With or without successful check, we perform a logout.
    api_client.logout()
else:
    raise Exception('Api login error. Code: ' + str(login_result['code']) + '  Message: ' + login_result['msg'])
