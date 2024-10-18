#!/usr/bin/python  # noqa: EXE001
"""Custom filters for role ./roles/irmc_snmp

Generate a filter from Ansible parameters
to generate structured data to be applied to the SNMP profile of the iRMC.
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


def generate_trap_destination_server(server: dict) -> dict:
    """Generate value of JSON element `Snmp.TrapDestinations.TrapDestination[]`."""
    logger.debug('snmp_trap_destination.server = %s', server)

    def _generator() -> Iterator[tuple[str, Any]]:
        if 'index' in server:
            yield '@TrapDestinationIdx', server.get('index')
            (value := server.get('name')) is not None and (yield 'Name', value)
            (value := server.get('protocol')) is not None and (yield 'Protocol', value)

    return dict(_generator())


def generate_trap_destinations(snmp_trap_destination: dict) -> list:
    """Generate value of JSON element `Snmp.TrapDestinations`."""
    logger.debug('snmp_trap_destination = %s', snmp_trap_destination)

    # The value of key 'servers' may contain None
    servers = snmp_trap_destination.get('servers') or []

    return {'TrapDestination': [generate_trap_destination_server(server) for server in servers]}


def generate_snmp(snmp: dict, snmp_trap_destination: dict) -> dict[str, Any]:
    """Generate value of JSON element `Snmp`."""
    logger.debug('snmp = %s', snmp)

    # The value of key 'snmp' may contain None
    snmp = snmp or {}
    # The value of key 'snmp_trap_destination' may contain None
    snmp_trap_destination = snmp_trap_destination or {}

    def _generate_snmp_v3(_snmp_trap_destination: dict) -> dict:
        """Generate value of JSON element `Snmp.SnmpV3`."""
        if 'engine_id' in _snmp_trap_destination:
            return {'EngineID': snmp_trap_destination.get('engine_id')}
        return {}

    def _generator()  -> Iterator[tuple[str, Any]]:
        (value := snmp.get('enabled')) is not None and (yield 'Enabled', value)
        (value := snmp.get('port')) is not None and (yield 'ServicePort', value)
        (value := snmp.get('protocol')) is not None and (yield 'ServiceVersion', value)
        (value := snmp.get('community_name')) is not None and (yield 'CommunityName', value)

        (value := snmp_trap_destination.get('community_name')) is not None and (yield 'TrapCommunityName', value)

        # NOTE: 'SnmpV3' is required even if empty (without it, 'ServiceVersion' is not applied)
        yield 'SnmpV3', _generate_snmp_v3(snmp_trap_destination)
        yield 'TrapDestinations', generate_trap_destinations(snmp_trap_destination)

    return dict(_generator())

def snmp_profile_filter(data: dict) -> dict:
    """Generate structured data to be applied to the SNMP profile of the iRMC."""
    configure_logging(data.get('ansible_verbosity', 0))

    logger.debug('pid = %d', os.getpid())
    logger.info('Starting SNMP profile generation...')

    # data is `vars` in Ansible
    result = {
        'Server': {
            'SystemConfig': {
                'IrmcConfig': {
                    'NetworkServices': {
                        'Snmp': generate_snmp(data.get('snmp'), data.get('snmp_trap_destination', {})),
                    },
                    '@Version': data['irmc_snmp_profile_irmcconfig_version'],
                },
            },
            '@Version': data['irmc_snmp_profile_server_version'],
        },
    }

    logger.info('SNMP profile generation completed successfully.')

    return result


class FilterModule:  # noqa: D101
    def filters(self) -> dict[str, callable]:  # noqa: D102
        return {
            'snmp_profile_filter': snmp_profile_filter,
        }


# TODO: The section below here is simple test code.
# TODO: Consider reimplementing it as a unit test and recommend deleting it in the future.

def test() -> None:  # noqa: D103
    import json

    import yaml

    def testcases() -> Iterator[str]:
        yield ''
        yield '''
snmp:
snmp_trap_destination:
'''
        yield '''
snmp:
  enabled:
  port:
  protocol:
  community_name:
'''
        yield '''
snmp:
  enabled: ""
  port: 0
  protocol: ""
  community_name: ""
'''
        yield '''
snmp_trap_destination:
  community_name: "trap-public"
  engine_id: "800000e703c47d46c36e4e"
  servers:
'''
        yield '''
snmp_trap_destination:
  servers:
    - index: 0
      name: "10.0.2.1"
      protocol: "SnmpV2c"
    - index: 1
      name: ""
      protocol: ""
    - index: 2
      name: "10.0.2.3"
      ### protocol was not set ###
    - index: 3
      ### hostname was not set ###
      protocol: "SnmpV1"
    - ### index was not set ###
      name: "10.0.2.5"
      protocol: "SnmpV2c"
'''

    for n, testcase in enumerate(testcases(), start=1):
        data = yaml.safe_load(testcase) or {}
        data |= {'irmc_snmp_profile_server_version': '0.0'}
        data |= {'irmc_snmp_profile_irmcconfig_version': '0.0'}

        result = snmp_profile_filter(data)
        print(f'Test[{n}]:')  # noqa: T201
        print(json.dumps(result, indent=2))  # noqa: T201

        # Assertion JSON contents tree
        _snmp = result['Server']['SystemConfig']['IrmcConfig']['NetworkServices']['Snmp']

if __name__ == '__main__':
    configure_logging(ansible_verbosity=4)
    test()
