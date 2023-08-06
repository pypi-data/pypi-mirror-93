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
from sys import stdout, stderr

import click
import json

from auth0_login import fatal, setting
from auth0_login.aws.console import open_aws_console
from auth0_login.aws.credentials import write_aws_credentials
from auth0_login.aws.account import aws_accounts
from auth0_login.aws.saml_assertion import AWSSAMLAssertion
from auth0_login.saml import SAMLGetAccessTokenCommand


class AWSSTSGetCredentialsFromSAMLCommand(SAMLGetAccessTokenCommand):
    """
    get AWS credentials using the obtained SAML token and
    stores then in `~/.aws/credentials`.

    As multiple AWS roles may have been granted to the SAML token,
    the caller has to specify the `account` number and `role` name to
    generate the credentials for. If you are unsure which accounts
    and roles have been granted, use the `--show` option

    The credentials will be stored under the specified `profile` name.
    By specifying `--open-console` it will open the AWS console too.
    """

    def __init__(self, account, role, profile, policy_arns = None, inline_policy = None):
        super(AWSSTSGetCredentialsFromSAMLCommand, self).__init__()
        self.account = account if account else setting.attributes.get('aws_account')
        if not account and self.account:
            self.account = aws_accounts.get_account(self.account).number

        self.role = role if role else setting.attributes.get('aws_role')
        self.profile = profile if profile else setting.attributes.get('aws_profile')
        self.policy_arns = policy_arns if policy_arns else string_to_list(setting.attributes.get('policy_arns', None))
        self.policy = inline_policy if inline_policy else setting.attributes.get('inline_policy', None)
        self.open_console = setting.attributes.get('aws_console', False)
        self.saml_response: AWSSAMLAssertion = None
        if self.policy:
            try:
                p = json.loads(self.policy)
            except Exception as e:
                stderr.write(f"ERROR: policy is invalid json, {e}\n")
                exit(1)



    def set_saml_response(self, saml_response):
        self.saml_response = AWSSAMLAssertion(saml_response)

    def print_roles(self):
        for role in self.saml_response.available_roles():
            account = aws_accounts.get_account(role.account)
            stdout.write(f'[{role.name}@{account.alias}]\n')
            stdout.write(f'idp_url = {setting.IDP_URL}\n')
            stdout.write(f'client_id = {setting.CLIENT_ID}\n')
            stdout.write(f'aws_account = {account.alias}\n')
            stdout.write(f'aws_role = {role.name}\n')
            stdout.write(f'aws_profile = {role.name}@{account.alias}\n\n')

    def show_account_roles(self):
        self.request_authorization()
        self.print_roles()

    @property
    def role_arn(self):
        return f'arn:aws:iam::{self.account}:role/{self.role}'

    def run(self):
        if not (self.account and self.role and self.profile):
            fatal('--account, --role and --profile are required.')

        self.request_authorization()

        credentials = self.saml_response.assume_role(self.role_arn, setting.ROLE_DURATION, self.policy_arns, self.policy)
        write_aws_credentials(credentials, self.profile)
        if self.open_console:
            open_aws_console(self.profile)

def string_to_list(value):
    return list(filter(lambda s: s, map(lambda s: s.strip(), value.split("\n")))) if value else None

@click.command('aws-assume-role', help=AWSSTSGetCredentialsFromSAMLCommand.__doc__)
@click.option('--account', help='aws account number or alias')
@click.option('--role', help='to assume using the token')
@click.option('--profile', help='to store the credentials under')
@click.option('--policy-arn', multiple=True, help='to use in the session')
@click.option('--inline-policy', help='to use in the session')
@click.option('--show', is_flag=True, default=False, help='account roles available to assume')
@click.option('--open-console', '-C', count=True, help=' after credential refresh')
def assume_role_with_saml(account, role, profile, show, open_console, policy_arn, inline_policy):

    aws_account = aws_accounts.get_account(account).number if account else None
    cmd = AWSSTSGetCredentialsFromSAMLCommand(aws_account, role, profile, policy_arn, inline_policy)
    if show:
        cmd.show_account_roles()
    else:
        if open_console:
            cmd.open_console = True
        cmd.run()
