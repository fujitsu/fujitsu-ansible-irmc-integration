#!/usr/bin/python

# Copyright 2018-2024 Fsas Technologies Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


DOCUMENTATION = r'''
---
module: irmc_powerstate

short_description: get or set server power state


description:
    - Ansible module to get or set server power state via iRMC RedFish interface.
    - Module Version V1.2.

requirements:
    - The module needs to run locally.
    - iRMC S6.
    - Python >= 3.10
    - Python modules 'requests', 'urllib3'

version_added: "2.4"

author:
    - Nakamura Takayuki (@nakamura-taka)

options:
    irmc_url:
        description: IP address of the iRMC to be requested for data.
        required:    true
    irmc_username:
        description: iRMC user for basic authentication.
        required:    true
    irmc_password:
        description: Password for iRMC user for basic authentication.
        required:    true
    validate_certs:
        description: Evaluate SSL certificate (set to false for self-signed certificate).
        required:    false
        default:     true
    command:
        description: Get or set server power state.
        required:    false
        default:     get
        choices:     ['get', 'set']
    state:
        description: Desired server power state for command 'set', ignored otherwise.
                     Options 'GracefulPowerOff' and ' GracefulReset' require
                     ServerView Agents running on server.
        required:    false
        choices:     ['PowerOn', 'PowerOff', 'PowerCycle', 'GracefulPowerOff', 'ImmediateReset', 'GracefulReset',
                      'PulseNmi', 'PressPowerButton']
'''

EXAMPLES = r'''
- name: Get and show server power state
  tags:
    - get
  block:
    - name: Get server power state
      fujitsu.primergy.irmc_powerstate:
        irmc_url: "{{ inventory_hostname }}"
        irmc_username: "{{ irmc_user }}"
        irmc_password: "{{ irmc_password }}"
        validate_certs: "{{ validate_certificate }}"
        command: "get"
      register: result
      delegate_to: localhost
    - name: Show server power state
      ansible.builtin.debug:
        var: result.power_state

- name: Set server power state
  fujitsu.primergy.irmc_powerstate:
    irmc_url: "{{ inventory_hostname }}"
    irmc_username: "{{ irmc_user }}"
    irmc_password: "{{ irmc_password }}"
    validate_certs: "{{ validate_certificate }}"
    command: "set"
    state: "{{ state }}"
  delegate_to: localhost
  tags:
    - set
'''

RETURN = r'''
details:
    description: >
        If command is “get”, the following values are returned.

        For other commands ("set"),
        the default return value of Ansible (changed, failed, etc.) is returned.

    contains:
        power_state:
            description: server power state
            returned: always
            type: string
            sample: "On"
'''


import json

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.fujitsu.primergy.plugins.module_utils.irmc import get_irmc_json, irmc_redfish_get, irmc_redfish_post


def irmc_powerstate(module: AnsibleModule) -> None:
    result = dict(
        changed=False,
        status=0,
    )

    if module.check_mode:
        result['msg'] = 'module was not run'
        module.exit_json(**result)

    # preliminary parameter check
    if module.params['command'] == 'set' and module.params['state'] is None:
        result['msg'] = "Command 'set' requires 'state' parameter to be set!"
        result['status'] = 10
        module.fail_json(**result)

    # Get iRMC system data
    status, sysdata, msg = irmc_redfish_get(module, 'redfish/v1/Systems/0/')
    if status < 100:
        module.fail_json(msg=msg, status=status, exception=sysdata)
    elif status != 200:
        module.fail_json(msg=msg, status=status)

    power_state = get_irmc_json(sysdata.json(), 'PowerState')
    if module.params['command'] == 'get':
        result['power_state'] = power_state
        module.exit_json(**result)

    # Evaluate function params against iRMC
    if 'Power' + power_state == module.params['state'].replace('Graceful', ''):
        result['skipped'] = True
        result['msg'] = f"PRIMERGY server is already in state '{power_state}'"
        module.exit_json(**result)

    allowedparams = get_irmc_json(
        sysdata.json(),
        ['Actions', 'Oem', '#FTSComputerSystem.Reset', 'FTSResetType@Redfish.AllowableValues'],
    )
    if module.params['state'] not in allowedparams:
        result['msg'] = (
            f"{module.params['state']!r} is not allowed now. "
            f"Currently allowed: {allowedparams}"
        )
        result['status'] = 11
        module.fail_json(**result)

    # Set iRMC system data
    body = {'FTSResetType': module.params['state']}
    status, sysdata, msg = irmc_redfish_post(
        module,
        'redfish/v1/Systems/0/Actions/Oem/FTSComputerSystem.Reset',
        json.dumps(body),
    )
    if status < 100:
        module.fail_json(msg=msg, status=status, exception=sysdata)
    elif status not in (200, 202, 204):
        module.fail_json(msg=msg, status=status)

    result['changed'] = True
    module.exit_json(**result)


def main() -> None:
    # breakpoint()
    module_args = dict(
        irmc_url=dict(required=True, type='str'),
        irmc_username=dict(required=True, type='str'),
        irmc_password=dict(required=True, type='str', no_log=True),
        validate_certs=dict(required=False, type='bool', default=True),
        command=dict(required=False, type='str', default='get', choices=['get', 'set']),
        state=dict(required=False, type='str', choices=['PowerOn', 'PowerOff', 'PowerCycle', 'GracefulPowerOff',
                                                        'ImmediateReset', 'GracefulReset', 'PulseNmi',
                                                        'PressPowerButton']),
    )
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False,
    )

    irmc_powerstate(module)


if __name__ == '__main__':
    main()
