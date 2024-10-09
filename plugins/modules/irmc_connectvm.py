#!/usr/bin/python

# Copyright 2018-2024 Fsas Technologies Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


DOCUMENTATION = r'''
---
module: irmc_connectvm

short_description: connect iRMC Virtual Media Data

description:
    - Ansible module to connect iRMC Virtual Media Data via the iRMC RedFish interface.
    - Module Version V1.3.0.

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
        description: The virtual media connect command to be executed.
        required:    false
        default:     ConnectCD
        choices:     ['ConnectCD', 'ConnectHD', 'DisconnectCD', 'DisconnectHD']
'''

EXAMPLES = r'''
# Disconnect Virtual CD
- name: Disconnect Virtual CD
  fujitsu.primergy.irmc_connectvm:
    irmc_url: "{{ inventory_hostname }}"
    irmc_username: "{{ irmc_user }}"
    irmc_password: "{{ irmc_password }}"
    validate_certs: "{{ validate_certificate }}"
    command: "DisconnectCD"
  delegate_to: localhost
  tags:
    - disconnectCD

# Connect Virtual CD
- name: Connect Virtual CD
  fujitsu.primergy.irmc_connectvm:
    irmc_url: "{{ inventory_hostname }}"
    irmc_username: "{{ irmc_user }}"
    irmc_password: "{{ irmc_password }}"
    validate_certs: "{{ validate_certificate }}"
    command: "ConnectCD"
  delegate_to: localhost
  tags:
    - connectCD

# Disconnect Virtual HD
- name: Disconnect Virtual HD
  fujitsu.primergy.irmc_connectvm:
    irmc_url: "{{ inventory_hostname }}"
    irmc_username: "{{ irmc_user }}"
    irmc_password: "{{ irmc_password }}"
    validate_certs: "{{ validate_certificate }}"
    command: "DisconnectHD"
  delegate_to: localhost
  tags:
    - disconnectHD

# Connect Virtual HD
- name: Connect Virtual HD
  fujitsu.primergy.irmc_connectvm:
    irmc_url: "{{ inventory_hostname }}"
    irmc_username: "{{ irmc_user }}"
    irmc_password: "{{ irmc_password }}"
    validate_certs: "{{ validate_certificate }}"
    command: "ConnectHD"
  delegate_to: localhost
  tags:
    - connectHD
'''

RETURN = r'''
details:
    description:
        The default return value of Ansible (changed, failed, etc.) is returned.
'''


import json

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.fujitsu.primergy.plugins.module_utils.irmc import get_irmc_json, irmc_redfish_get, irmc_redfish_post


def irmc_connectvirtualmedia(module):
    result = dict(
        changed=False,
        status=0,
    )

    if module.check_mode:
        result['msg'] = 'module was not run'
        module.exit_json(**result)

    # Get iRMC system data
    status, sysdata, msg = irmc_redfish_get(module, 'redfish/v1/Systems/0/')
    if status < 100:
        module.fail_json(msg=msg, status=status, exception=sysdata)
    elif status != 200:
        module.fail_json(msg=msg, status=status)

    # Evaluate function params against iRMC
    irmctype = get_irmc_json(sysdata.headers, 'Server')
    vmaction_type = 'VirtualMediaAction' if 'S4' in irmctype else 'FTSVirtualMediaAction'
    vm_type = module.params['command'].replace('Connect', '').replace('Disconnect', '')
    vm_action = module.params['command'].replace(vm_type, '')
    vm_other_state = 'Connect' + vm_type if vm_action == 'Disconnect' else 'Disconnect' + vm_type
    allowedparams = get_irmc_json(
        sysdata.json(),
        ['Actions', 'Oem', '#FTSComputerSystem.VirtualMedia', vmaction_type + '@Redfish.AllowableValues'],
    )
    if module.params['command'] not in allowedparams:
        if vm_other_state in allowedparams:
            result['skipped'] = True
            result['msg'] = 'iRMC vitual ' + vm_type + " is already in state '" + module.params['command'] + "'"
            module.exit_json(**result)
        else:
            result['warnings'] = (
                "Parameter '"
                + module.params['command']
                + "' cannot be used at this time. "
                + 'Allowed: '
                + json.dumps(allowedparams)
            )
            module.exit_json(**result)

    # Get iRMC Virtual Media data
    status, vmdata, msg = irmc_redfish_get(module, 'redfish/v1/Systems/0/Oem/ts_fujitsu/VirtualMedia/')
    if status < 100:
        module.fail_json(msg=msg, status=status, xception=vmdata)
    elif status != 200:
        module.fail_json(msg=msg, status=status)

    # Check Virtual Media Data
    remotemountenabled = get_irmc_json(vmdata.json(), 'RemoteMountEnabled')
    if not remotemountenabled:
        result['msg'] = 'Remote Mount of Virtual Media is not enabled!'
        result['status'] = 20
        module.fail_json(**result)

    # Set iRMC system data
    body = {vmaction_type: module.params['command']}
    status, sysdata, msg = irmc_redfish_post(
        module,
        'redfish/v1/Systems/0/Actions/Oem/FTSComputerSystem.VirtualMedia',
        json.dumps(body),
    )
    if status < 100:
        module.fail_json(msg=msg, status=status, exception=sysdata)
    elif status not in (200, 202, 204):
        module.fail_json(msg=msg, status=status)

    result['changed'] = True
    module.exit_json(**result)


def main():
    # import pdb; pdb.set_trace()
    module_args = dict(
        irmc_url=dict(required=True, type='str'),
        irmc_username=dict(required=True, type='str'),
        irmc_password=dict(required=True, type='str', no_log=True),
        validate_certs=dict(required=False, type='bool', default=True),
        command=dict(
            required=False,
            type='str',
            default='ConnectCD',
            choices=['ConnectCD','ConnectHD', 'DisconnectCD','DisconnectHD'],
        ),
    )
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False,
    )

    irmc_connectvirtualmedia(module)


if __name__ == '__main__':
    main()
