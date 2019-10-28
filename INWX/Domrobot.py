import base64
import hashlib
import hmac
import json
import struct
import sys
import time
import random
import string
import requests
import xmlrpc.client
from enum import Enum


class ApiType(Enum):
    XML_RPC = '/xmlrpc/'
    JSON_RPC = '/jsonrpc/'


class ApiClient:
    CLIENT_VERSION = '3.0.3'
    API_LIVE_URL = 'https://api.domrobot.com'
    API_OTE_URL = 'https://api.ote.domrobot.com'

    def __init__(self, api_url=API_OTE_URL, api_type=ApiType.XML_RPC, language='en', client_transaction_id=None,
                 debug_mode=False):
        """
        Args:
            api_url: Url of the api.
            api_type: Type of the api. See ApiType class for all types.
            language: Language for api messages and error codes in responses.
            client_transaction_id: Sent with every request to distinguish your api requests in case you need support.
            debug_mode: Whether requests and responses should be printed out.
        """

        self.api_url = api_url
        self.api_type = api_type
        self.language = language
        self.client_transaction_id = client_transaction_id
        self.debug_mode = debug_mode
        self.customer = None
        self.api_session = requests.Session()

    def login(self, username, password, shared_secret=None):
        """Performs a login at the api and saves the session cookie for following api calls.

        Args:
            username: Your username.
            password: Your password.
            shared_secret: A secret used to generate a secret code to solve 2fa challenges when 2fa is enabled. This is
                the code/string encoded in the QR-Code you scanned with your google authenticator app when you enabled 2fa.
                If you don't have this secret anymore, disable and re-enable 2fa for your account but this time save the
                code/string encoded in the QR-Code.
        Returns:
            The api response body parsed as a dict.
        Raises:
            Exception: Username and password must not be None.
            Exception: Api requests two factor challenge but no shared secret is given. Aborting.
        """

        if username is None or password is None:
            raise Exception('Username and password must not be None.')

        params = {
            'lang': self.language,
            'user': username,
            'pass': password
        }

        login_result = self.call_api('account.login', params)
        if login_result['code'] == 1000 and 'tfa' in login_result['resData'] and login_result['resData']['tfa'] != '0':
            if shared_secret is None:
                raise Exception('Api requests two factor challenge but no shared secret is given. Aborting.')
            secret_code = self.get_secret_code(shared_secret)
            unlock_result = self.call_api('account.unlock', {'tan': secret_code})
            if unlock_result['code'] != 1000:
                return unlock_result

        return login_result

    def logout(self):
        """Logs out the user and destroys the session.

        Returns:
            The api response body parsed as a dict.
        """

        logout_result = self.call_api('account.logout')
        self.api_session.close()
        self.api_session = requests.Session()
        return logout_result

    def call_api(self, api_method, method_params=None):
        """Makes an api call.

        Args:
            api_method: The name of the method called in the api.
            method_params: A dict of parameters added to the request.
        Returns:
            The api response body parsed as a dict.
        Raises:
            Exception: Api method must not be None.
            Exception: Invalid ApiType.
        """

        if api_method is None:
            raise Exception('Api method must not be None.')
        if method_params is None:
            method_params = {}

        if self.customer:
            method_params['subuser'] = self.customer
        if self.client_transaction_id is not None:
            method_params['clTRID'] = self.client_transaction_id

        if self.api_type == ApiType.XML_RPC:
            payload = xmlrpc.client.dumps((method_params,), api_method, encoding='UTF-8').replace('\n', '')
        elif self.api_type == ApiType.JSON_RPC:
            payload = str(json.dumps({'method': api_method, 'params': method_params}))
        else:
            raise Exception('Invalid ApiType.')

        headers = {
            'Content-Type': 'text/xml; charset=UTF-8',
            'User-Agent': 'DomRobot/' + ApiClient.CLIENT_VERSION + ' (Python ' + self.get_python_version() + ')'
        }

        response = self.api_session.post(self.api_url + self.api_type.value, data=payload.encode('UTF-8'), headers=headers)

        if self.debug_mode:
            print('Request (' + api_method + '): ' + payload)
            print('Response (' + api_method + '): ' + response.text)

        if self.api_type == ApiType.XML_RPC:
            return xmlrpc.client.loads(response.text)[0][0]
        elif self.api_type == ApiType.JSON_RPC:
            return response.json()

    @staticmethod
    def get_secret_code(shared_secret):
        """Generates a secret code for 2fa with a shared secret.

        Args:
            shared_secret: The shared secret used to generate the secret code.
        Returns:
            A secret code used to solve 2fa challenges.
        Raises:
            Exception: Shared secret must not be None.
        """

        if shared_secret is None:
            raise Exception('Shared secret must not be None.')

        key = base64.b32decode(shared_secret, True)
        msg = struct.pack(">Q", int(time.time()) // 30)
        hmac_hash = hmac.new(key, msg, hashlib.sha1).digest()
        o = hmac_hash[19] & 15
        hmac_hash = (struct.unpack(">I", hmac_hash[o:o + 4])[0] & 0x7fffffff) % 1000000
        return hmac_hash

    @staticmethod
    def get_random_string(size=12):
        return ''.join(random.choice(string.ascii_letters + string.digits) for x in range(size))

    @staticmethod
    def get_python_version():
        return '.'.join(tuple(str(x) for x in sys.version_info))
