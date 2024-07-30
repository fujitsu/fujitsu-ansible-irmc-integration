#!/usr/bin/python

# Copyright 2018-2024 Fsas Technologies INC.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division)
__metaclass__ = type


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}


DOCUMENTATION = '''
---
module: irmc_idled

short_description: get or set server ID LED

description:
    - Ansible module to get or set server ID LED via iRMC RedFish interface.
    - Module Version V1.2.

requirements:
    - The module needs to run locally.
    - iRMC S4 needs FW >= 9.04, iRMC S5 needs FW >= 1.25.
    - Python >= 2.6
    - Python modules 'future', 'requests', 'urllib3'

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

notes:
    - See http://manuals.ts.fujitsu.com/file/13371/irmc-restful-spec-en.pdf
    - See http://manuals.ts.fujitsu.com/file/13372/irmc-redfish-wp-en.pdf
'''

EXAMPLES = '''
# Get server ID LED state
- name: Get ID LED state
  irmc_idled:
    irmc_url: "{{ inventory_hostname }}"
    irmc_username: "{{ irmc_user }}"
    irmc_password: "{{ irmc_password }}"
    validate_certs: "{{ validate_certificate }}"
    command: "get"
  register: idled
  delegate_to: localhost
- name: Show iRMC ID LED state
  debug:
    msg: "{{ idled.idled_state }}"

# Set server ID LED state
- name: Set server ID LED state
  irmc_idled:
    irmc_url: "{{ inventory_hostname }}"
    irmc_username: "{{ irmc_user }}"
    irmc_password: "{{ irmc_password }}"
    validate_certs: "{{ validate_certificate }}"
    command: "set"
    state: "Lit"
  delegate_to: localhost
'''

RETURN = '''
# For command "get":
    idled_state:
        description: server ID LED state
        returned: always
        type: string
        sample: Blinking

# For command "set":
    Default return values:
'''


import json
from ansible.module_utils.basic import AnsibleModule

from ansible.module_utils.irmc import irmc_redfish_get, irmc_redfish_patch, get_irmc_json


def irmc_idled(module):
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
        result['status'] = 10
        module.fail_json(**result)

    # get iRMC system data
    status, sysdata, msg = irmc_redfish_get(module, "redfish/v1/Systems/0/")
    if status < 100:
        module.fail_json(msg=msg, status=status, exception=sysdata)
    elif status != 200:
        module.fail_json(msg=msg, status=status)

    idledstate = get_irmc_json(sysdata.json(), "IndicatorLED")
    if module.params['command'] == "get":
        result['idled_state'] = idledstate
        module.exit_json(**result)

    # evaluate function params against iRMC
    if idledstate == module.params['state']:
        result['skipped'] = True
        result['msg'] = "iRMC ID LED is already in state '{0}'".format(module.params['state'])
        module.exit_json(**result)

    allowedparams = get_irmc_json(sysdata.json(), "IndicatorLED@Redfish.AllowableValues")
    if module.params['state'] not in allowedparams:
        result['msg'] = "Invalid parameter '{0}'. Allowed: {1}".format(module.params['state'],
                                                                       json.dumps(allowedparams))
        result['status'] = 11
        module.fail_json(**result)

    # set iRMC system data
    body = {'IndicatorLED': module.params['state']}
    etag = get_irmc_json(sysdata.json(), "@odata.etag")
    status, patch, msg = irmc_redfish_patch(module, "redfish/v1/Systems/0/", json.dumps(body), etag)
    if status < 100:
        module.fail_json(msg=msg, status=status, exception=patch)
    elif status != 200:
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
        state=dict(required=False, type="str", choices=['Off', 'Lit', 'Blinking'])
    )
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    irmc_idled(module)


if __name__ == '__main__':
    main()
