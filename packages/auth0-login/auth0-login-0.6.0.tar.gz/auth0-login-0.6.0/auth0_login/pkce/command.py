#
# Copyright 2019 - binx.io B.V.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import hashlib
import json
import logging
import webbrowser
from base64 import urlsafe_b64encode
from http.server import HTTPServer
from random import getrandbits
from sys import stdout
from urllib.parse import urlencode
from uuid import uuid4

import click

from auth0_login import fatal, setting
from auth0_login.pkce.callback import PKCEAccessTokenCallbackHandler
from auth0_login.util import assert_listen_port_is_available, get_listen_port_from_url


class PKCEGetIdTokenCommand(object):
    """
    requests an JWT id token using the PKCE authorization flow and prints
    all the returned data to standard output.

    The request is sent  `{idp_url}/authorize`, the callback
    defaults to `http://localhost:{listen_port}/callback`, but may be
    explicitly set using the `pcke_callback_url` property.

    """

    def __init__(self):
        self.client_id = setting.CLIENT_ID
        self.scope = "openid profile"
        self.tokens = {}
        self.state = str(uuid4())
        self.verifier = self.b64encode(bytearray(getrandbits(8) for _ in range(32)))
        self.challenge = self.b64encode(hashlib.sha256(self.verifier.encode('ascii')).digest())
        self.callback_url = setting.attributes.get('pkce_callback_url',
                                                   f'http://localhost:{setting.LISTEN_PORT}/callback')

    @property
    def token_url(self):
        return f'{setting.IDP_URL}/oauth/token'

    @property
    def authorize_url(self):
        return f'{setting.IDP_URL}/authorize'

    @property
    def listen_port(self):
        return get_listen_port_from_url(self.callback_url)

    def set_tokens(self, tokens):
        self.tokens = tokens

    def accept_access_code(self):
        PKCEAccessTokenCallbackHandler.client_id = setting.CLIENT_ID
        PKCEAccessTokenCallbackHandler.token_url = self.token_url
        PKCEAccessTokenCallbackHandler.callback_url = self.callback_url
        PKCEAccessTokenCallbackHandler.verifier = self.verifier
        PKCEAccessTokenCallbackHandler.state = self.state
        PKCEAccessTokenCallbackHandler.handler = (lambda tokens: self.set_tokens(tokens))
        httpd = HTTPServer(('0.0.0.0', self.listen_port), PKCEAccessTokenCallbackHandler)
        try:
            httpd.handle_request()
        finally:
            httpd.server_close()

    @property
    def query_parameters(self):
        return {
            "response_type": "code",
            "scope": self.scope,
            "client_id": self.client_id,
            "code_challenge": self.challenge,
            "code_challenge_method": "S256",
            "redirect_uri": self.callback_url,
            "state": self.state
        }

    @property
    def url(self):
        return self.authorize_url + '?' + urlencode(self.query_parameters)

    def request_authorization(self):
        logging.debug('url = %s', self.url)
        webbrowser.open(self.url)
        self.accept_access_code()

    @staticmethod
    def b64encode(s):
        return urlsafe_b64encode(s).decode('ascii').strip("=")

    def run(self):
        assert_listen_port_is_available(self.listen_port)
        self.request_authorization()
        if self.tokens:
            json.dump(self.tokens, stdout)
        else:
            fatal('no token retrieved')


class PKCEGetAccessTokenCommand(PKCEGetIdTokenCommand):
    """
    requests an JWT access token using the PKCE authorization flow for the
    specified `audience` and `scope`. All returned data to printed to
    standard output.

    Both `audience` and `scope` can be specified as a command line option
    or in the .oauth-cli.ini.

    The request is sent  `{idp_url}/authorize`, the callback
    defaults to `http://localhost:{listen_port}/callback, but may be
    explicitly set using the `pcke_callback_url` property.

    """

    def __init__(self):
        super(PKCEGetAccessTokenCommand, self).__init__()
        self.audience = setting.attributes.get('audience')
        self.scope = setting.attributes.get('scope', 'openid profile')

    @property
    def query_parameters(self):
        result = super(PKCEGetAccessTokenCommand, self).query_parameters
        result.update({"audience": self.audience, "scope": self.scope})
        return result

    def run(self):
        if not self.audience:
            fatal('audience is required')
        super(PKCEGetAccessTokenCommand, self).run()


@click.command('get-access-jwt', help=PKCEGetAccessTokenCommand.__doc__)
@click.option('--audience', help='to obtain an access token for. default from ~/.oauth-cli.ini')
@click.option('--scope', help='of the access token')
def get_access_token(audience, scope):
    cmd = PKCEGetAccessTokenCommand()
    if audience:
        cmd.audience = audience
    if scope:
        cmd.scope = scope
    cmd.run()


@click.command('get-id-jwt', help=PKCEGetIdTokenCommand.__doc__)
def get_id_token():
    cmd = PKCEGetIdTokenCommand()
    cmd.run()
