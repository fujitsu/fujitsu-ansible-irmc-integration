#!/usr/bin/python

# FUJITSU Limited
# Copyright (C) FUJITSU Limited 2018
# GNU General Public License v3.0+ (see LICENSE.md or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division)
__metaclass__ = type


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}


DOCUMENTATION = '''
---
module: irmc_powerstate

short_description: get or set server power state


description:
    - Ansible module to get or set server power state via iRMC RedFish interface.
    - Module Version V1.0.1.

requirements:
    - The module needs to run locally.
    - iRMC S4 needs FW >= 9.04, iRMC S5 needs FW >= 1.25.
    - "python >= 2.6"

version_added: "2.4"

author:
    - FujitsuPrimergy (@FujitsuPrimergy)

options:
    irmc_url:
        description: IP address of the iRMC to be requested for data
        required:    true
    irmc_username:
        description: iRMC user for basic authentication
        required:    true
    irmc_password:
        description: password for iRMC user for basic authentication
        required:    true
    validate_certs:
        description: evaluate SSL certificate (set to false for self-signed certificate)
        required:    false
        default:     true
    command:
        description: get or set server power state
        required:    false
        default:     get
        choices:     ['get', 'set']
    state:
        description: desired server power state for command 'set', ignored otherwise;
                     options 'GracefulPowerOff' and ' GracefulReset' require
                     ServerView Agents running on server
        required:    false
        choices:     ['PowerOn', 'PowerOff', 'PowerCycle', 'GracefulPowerOff', 'ImmediateReset', 'GracefulReset',
                      'PulseNmi', 'PressPowerButton']

notes:
    - See http://manuals.ts.fujitsu.com/file/13371/irmc-restful-spec-en.pdf
    - See http://manuals.ts.fujitsu.com/file/13372/irmc-redfish-wp-en.pdf
'''

EXAMPLES = '''
# Get server power state
- name: Get server power state
  irmc_powerstate:
    irmc_url: "{{ inventory_hostname }}"
    irmc_username: "{{ irmc_user }}"
    irmc_password: "{{ irmc_password }}"
    validate_certs: "{{ validate_certificate }}"
    command: "get"
  register: powerstate
  delegate_to: localhost
- name: Show server power state
  debug:
    msg: "{{ powerstate.power_state }}"

# set server power state
- name: set server power state
  irmc_powerstate:
    irmc_url: "{{ inventory_hostname }}"
    irmc_username: "{{ irmc_user }}"
    irmc_password: "{{ irmc_password }}"
    validate_certs: "{{ validate_certificate }}"
    command: "set"
    state: "PowerOn"
  delegate_to: localhost
'''

RETURN = '''
power_state:
    description: server power state
    returned: always
    type: str
'''


# pylint: disable=wrong-import-position
import json
from ansible.module_utils.basic import AnsibleModule

from ansible.module_utils.irmc import irmc_redfish_get, irmc_redfish_post, get_irmc_json


def irmc_powerstate(module):
    result = dict(
        changed=False,
        status=0
    )

    if module.check_mode:
        result['msg'] = "module was not run"
        module.exit_json(**result)

    # preliminary parameter check
    if module.params['command'] == "set" and module.params['state'] is None:
        result['msg'] = "Command 'set' requires 'state' parameter to be set!"
        module.fail_json(**result)

    # Get iRMC system data
    status, sysdata, msg = irmc_redfish_get(module, "redfish/v1/Systems/0/")
    if status < 100:
        module.fail_json(msg=msg, exception=sysdata)
    elif status != 200:
        module.fail_json(msg=msg, status=status)

    power_state = get_irmc_json(sysdata.json(), "PowerState")
    if module.params['command'] == "get":
        result['power_state'] = power_state
        module.exit_json(**result)

    # Evaluate function params against iRMC
    if "Power" + power_state == module.params['state']:
        result['skipped'] = True
        result['msg'] = "PRIMERGY server is already in state '{0}'".format(module.params['state'])
        module.exit_json(**result)

    allowedparams = \
        get_irmc_json(sysdata.json(),
                      ["Actions", "Oem",
                       "http://ts.fujitsu.com/redfish-schemas/v1/FTSSchema.v1_0_0#FTSComputerSystem.Reset",
                       "FTSResetType@Redfish.AllowableValues"])
    if module.params['state'] not in allowedparams:
        result['msg'] = "Invalid parameter '{0}'. Allowed: {1}". \
                        format(module.params['state'], json.dumps(allowedparams))
        module.fail_json(**result)

    # Set iRMC system data
    body = {'FTSResetType': module.params['state']}
    status, sysdata, msg = irmc_redfish_post(module, "redfish/v1/Systems/0/Actions/Oem/FTSComputerSystem.Reset",
                                             json.dumps(body))
    if status < 100:
        module.fail_json(msg=msg, exception=sysdata)
    elif status != 200 and status != 204:
        module.fail_json(msg=msg, status=status)

    result['changed'] = True
    module.exit_json(**result)


def main():
    # import pdb; pdb.set_trace()
    module_args = dict(
        irmc_url=dict(required=True, type="str"),
        irmc_username=dict(required=True, type="str"),
        irmc_password=dict(required=True, type="str", no_log=True),
        validate_certs=dict(required=False, type="bool", default=True),
        command=dict(required=False, type="str", default="get", choices=['get', 'set']),
        state=dict(required=False, type="str", choices=['PowerOn', 'PowerOff', 'PowerCycle', 'GracefulPowerOff',
                                                        'ImmediateReset', 'GracefulReset', 'PulseNmi',
                                                        'PressPowerButton'])
    )
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    irmc_powerstate(module)


if __name__ == '__main__':
    main()
