#!/usr/bin/python

# Copyright 2018-2024 Fsas Technologies Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


DOCUMENTATION = r'''
---
module: irmc_idled

short_description: get or set server ID LED

description:
    - Ansible module to get or set server ID LED via iRMC RedFish interface.
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
        description: Get or set server ID LED state.
        required:    false
        default:     get
        choices:     ['get', 'set']
    state:
        description: Desired server ID LED state for command 'set', ignored otherwise.
        required:    false
        choices:     ['Off', 'Lit', 'Blinking']
'''

EXAMPLES = r'''
# Get server ID LED state
- block:
  - name: Get ID LED state
    fujitsu.primergy.irmc_idled:
      irmc_url: "{{ inventory_hostname }}"
      irmc_username: "{{ irmc_user }}"
      irmc_password: "{{ irmc_password }}"
      validate_certs: "{{ validate_certificate }}"
      command: "get"
    register: idled
    delegate_to: localhost
  - name: Show iRMC ID LED state
    debug:
      var: idled.idled_state
  tags:
    - get

# Set server ID LED state
- name: Set server ID LED state
  fujitsu.primergy.irmc_idled:
    irmc_url: "{{ inventory_hostname }}"
    irmc_username: "{{ irmc_user }}"
    irmc_password: "{{ irmc_password }}"
    validate_certs: "{{ validate_certificate }}"
    command: "set"
    state: "Lit"
  delegate_to: localhost
  tags:
    - set
'''

RETURN = r'''
details:
    description:
        If command is “get”, the following values are returned.

        If command is "set", the default return value of Ansible (changed, failed, etc.) is returned.

    contains:
        idled_state:
            description: server ID LED state
            returned: always
            type: string
            sample: Blinking
'''


import json

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.fujitsu.primergy.plugins.module_utils.irmc import get_irmc_json, irmc_redfish_get, irmc_redfish_patch


def irmc_idled(module):
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

    # get iRMC system data
    status, sysdata, msg = irmc_redfish_get(module, 'redfish/v1/Systems/0/')
    if status < 100:
        module.fail_json(msg=msg, status=status, exception=sysdata)
    elif status != 200:
        module.fail_json(msg=msg, status=status)

    idledstate = get_irmc_json(sysdata.json(), 'IndicatorLED')
    if module.params['command'] == 'get':
        result['idled_state'] = idledstate
        module.exit_json(**result)

    # evaluate function params against iRMC
    if idledstate == module.params['state']:
        result['skipped'] = True
        result['msg'] = "iRMC ID LED is already in state '{0}'".format(module.params['state'])
        module.exit_json(**result)

    allowedparams = get_irmc_json(sysdata.json(), 'IndicatorLED@Redfish.AllowableValues')
    if module.params['state'] not in allowedparams:
        result['msg'] = "Invalid parameter '{0}'. Allowed: {1}".format(module.params['state'],
                                                                       json.dumps(allowedparams))
        result['status'] = 11
        module.fail_json(**result)

    # set iRMC system data
    body = {'IndicatorLED': module.params['state']}
    etag = get_irmc_json(sysdata.json(), '@odata.etag')
    status, patch, msg = irmc_redfish_patch(module, 'redfish/v1/Systems/0/', json.dumps(body), etag)
    if status < 100:
        module.fail_json(msg=msg, status=status, exception=patch)
    elif status != 200:
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
        command=dict(required=False, type='str', default='get', choices=['get', 'set']),
        state=dict(required=False, type='str', choices=['Off', 'Lit', 'Blinking']),
    )
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False,
    )

    irmc_idled(module)


if __name__ == '__main__':
    main()
