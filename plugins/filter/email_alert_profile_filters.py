#!/usr/bin/python  # noqa: EXE001
"""Custom filters for role ./roles/irmc_email_alert

Generate a filter from Ansible parameters
to generate structured data to be applied to the E-mail Alert profile of the iRMC.
"""

import logging
import os
from collections.abc import Iterator
from typing import Any

# TODO: Unit testing is needed (and consideration of how it will be implemented and executed)

logger = logging.getLogger(__name__)


def configure_logging(ansible_verbosity: int) -> None:
    """Output up to `INFO` if '-vvv', `DEBUG` if '-vvvv' or more."""
    match ansible_verbosity:
        case v if v >= 4:  # noqa: PLR2004
            log_level = logging.DEBUG
        case v if v >= 3:  # noqa: PLR2004
            log_level = logging.INFO
        case _:
            log_level = logging.WARNING

    logging.basicConfig(
        level=log_level,
        format='%(levelname)-8s - %(name)s.%(funcName)s - %(message)s',
    )


def generate_email(email_format: dict) -> dict:
    """Generate value of JSON element `Email`."""
    logger.debug('email_format = %s', email_format)

    # The value of key 'email_format' may contain None
    email_format = email_format or {}

    def _generator() -> Iterator[tuple[str, Any]]:
        (value := email_format.get('from')) is not None and (yield 'From', value)
        (value := email_format.get('subject')) is not None and (yield 'Subject', value)
        (value := email_format.get('message')) is not None and (yield 'Message', value)
        (value := email_format.get('admin_name')) is not None and (yield 'AdminName', value)
        (value := email_format.get('admin_phone')) is not None and (yield 'AdminPhone', value)
        (value := email_format.get('country_code')) is not None and (yield 'ITSCountryCode', value)
        (value := email_format.get('customer_id')) is not None and (yield 'ITSCustomerId', value)
        (value := email_format.get('server_url')) is not None and (yield 'ServerUrl', value)
        (value := email_format.get('attach_screenshot')) is not None and (yield 'AttachScreenshotEnabled', value)

    return dict(_generator())


def generate_smtp_authentication(authentication: dict) -> dict:
    """Generate value of JSON element `Smtp.Servers.Server[].Authentication`."""
    logger.debug('authentication = %s', authentication)

    # The value of the key 'authentication' may contain None
    authentication = authentication or {}

    def _generator() -> Iterator[str, Any]:
        (value := authentication.get('type')) is not None and (yield 'Type', value)
        (value := authentication.get('username')) is not None and (yield 'UserName', value)
        if (value := authentication.get('password')) is not None:
            yield 'Password', {'@Encryption': 'None', '#text': value}

    return dict(_generator())


def generate_smtp_server(server: dict, index: int) -> dict:
    """Generate value of JSON element `Smtp.Servers.Server[]`.

    If there is no valid configuration value, return the empty dict.
    """
    logger.debug('index = %d, server = %s', index, server)

    # The value of key 'primary_server' and 'secondary_server' may contain None
    server = server or {}

    def _generator() -> Iterator[tuple[str, Any]]:
        (value := server.get('address')) is not None and (yield 'HostName', value)
        (value := server.get('port')) is not None and (yield 'Port', value)

        if (value := generate_smtp_authentication(server.get('authentication'))):
            yield 'Authentication', value

        # NOTE: 'UseAddressLiteral' is turned *OFF* when set *TRUE*, so the set value is reversed.
        (value := server.get('fqdn_with_ehlo_helo')) is not None and (yield 'UseAddressLiteral', not value)

        (value := server.get('use_ssl_tls')) is not None and (yield 'SslEnabled', value)
        (value := server.get('verify_certificate')) is not None and (yield 'VerifyCertEnabled', value)

    result = dict(_generator())

    if not result:
        return {}

    return result | {'@ServerIdx': index}


def generate_smtp_servers(smtp: dict) -> dict:
    """Generate value of JSON element `Smtp.Servers`."""
    logger.debug('smtp = %s', smtp)

    # The value of key 'smtp' may contain None
    smtp = smtp or {}

    servers = []

    if server := generate_smtp_server(smtp.get('primary_server'), index=0):
        servers.append(server)
    if server := generate_smtp_server(smtp.get('secondary_server'), index=1):
        servers.append(server)

    return {'Server': servers}


def generate_smtp(email_alert: dict, smtp: dict) -> dict:
    """Generate value of JSON element `Smtp`."""
    logger.debug('email_alert = %s', email_alert)
    logger.debug('smtp = %s', smtp)

    # The value of key 'email_alert' may contain None
    email_alert = email_alert or {}

    def _generator() -> Iterator[tuple[str, Any]]:
        (value := email_alert.get('enabled')) is not None and (yield 'Enabled', value)
        (value := email_alert.get('retries')) is not None and (yield 'SmtpRetries', value)
        (value := email_alert.get('retry_delay')) is not None and (yield 'SmtpRetryDelay', value)
        (value := email_alert.get('response_timeout')) is not None and (yield 'ResponseTimeout', value)

        yield 'Servers', generate_smtp_servers(smtp)

    return dict(_generator())


def email_alert_profile_filter(data: dict) -> dict:
    """Generate structured data to be applied to the Email and Smtp profile of the iRMC."""
    configure_logging(data.get('ansible_verbosity', 0))

    logger.debug('pid = %d', os.getpid())
    logger.info('Starting Email and SMTP profile generation...')

    # data is `vars` in Ansible
    result = {
        'Server': {
            'SystemConfig': {
                'IrmcConfig': {
                    'Email': generate_email(data.get('email_format')),
                    'Smtp': generate_smtp(data.get('email_alert'), data.get('smtp')),
                    '@Version': data['irmc_email_alert_profile_irmcconfig_version'],
                },
            },
            '@Version': data['irmc_email_alert_profile_server_version'],
        },
    }

    logger.info('Email and SMTP profile generation completed successfully.')

    return result


class FilterModule:  # noqa: D101
    def filters(self) -> dict[str, callable]:  # noqa: D102
        return {
            'email_alert_profile_filter': email_alert_profile_filter,
        }


# TODO: The section below here is simple test code.
# TODO: Consider reimplementing it as a unit test and recommend deleting it in the future.

def test() -> None:  # noqa: D103
    import json

    import yaml

    def testcases() -> Iterator[str]:
        yield ''
        yield '''
email_alert:
email_format:
smtp:
'''
        yield '''
email_alert:
  enabled:
  retries:
  retry_delay:
  response_timeout:
'''
        yield '''
email_alert:
  enabled: false
  retries: 3
  retry_delay: 30
  response_timeout: 45
'''
        yield '''
email_format:
  from:
  subject:
  message:
  admin_name:
  admin_phone:
  country_code:
  customer_id:
  server_url:
  attach_screenshot_enabled:
'''
        yield '''
email_format:
  from: MailFrom@example.com
  subject: FixedMailSubject
  message: FixedMailMessage
  admin_name: ITS_UserInfo0
  admin_phone: ITS_UserInfo1
  country_code: "JP"
  customer_id: "example"
  server_url: http://www.server.example.com
  attach_screenshot_enabled: true
'''
        yield '''
smtp:
  primary_server:
  secondary_server:
    authentication:
'''
        yield '''
smtp:
  primary_server:
    address: 10.0.2.1
    port: 25
    authentication:
      type: "Smtp"
      username: "AuthUserName"
      password: "AuthPassword"
    fqdn_with_ehlo_helo: true
    use_ssl_tls: true
    verify_certificate: true
'''
        yield '''
smtp:
  secondary_server:
    address: 10.0.2.2
    port: 25
    authentication:
      type: "None"
      username: ""
      password: ""
    fqdn_with_ehlo_helo: false
    use_ssl_tls: false
    verify_certificate: false
'''

    for n, testcase in enumerate(testcases(), start=1):
        data = yaml.safe_load(testcase) or {}
        data |= {'irmc_email_alert_profile_server_version': '0.0'}
        data |= {'irmc_email_alert_profile_irmcconfig_version': '0.0'}

        result = email_alert_profile_filter(data)
        print(f'Test[{n}]:')  # noqa: T201
        print(json.dumps(result, indent=2))  # noqa: T201

        # Assertion JSON contents tree
        _email = result['Server']['SystemConfig']['IrmcConfig']['Email']
        _smtp = result['Server']['SystemConfig']['IrmcConfig']['Smtp']

if __name__ == '__main__':
    configure_logging(ansible_verbosity=4)
    test()
