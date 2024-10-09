#!/usr/bin/python

# Copyright 2018-2024 Fsas Technologies Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = '''
---
module: irmc_license

short_description: manage iRMC user accounts

description:
    - Ansible module to manage iRMC user accounts via iRMC remote scripting interface.
    - Module Version V1.3.0.

requirements:
    - The module needs to run locally.
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
        description: License key management to be executed.
        required:    false
        default:     get
        choices:     ['get', 'set']
    license_key:
        description: iRMC license key to be set.
        required:    false

notes:
    - A license key which was read from an iRMC is 'system-locked'. It can imported to the same iRMC,
      but not to another iRMC.
'''

EXAMPLES = '''
# Get iRMC license key
- block:
  - name: Get iRMC license key
    fujitsu.primergy.irmc_license:
      irmc_url: "{{ inventory_hostname }}"
      irmc_username: "{{ irmc_user }}"
      irmc_password: "{{ irmc_password }}"
      validate_certs: "{{ validate_certificate }}"
      command: "get"
    register: license
    delegate_to: localhost

  - name: show certificates
    debug:
      var: license.license_key
  tags:
    - get

# Set iRMC license key
- name: Set iRMC license key
  fujitsu.primergy.irmc_license:
    irmc_url: "{{ inventory_hostname }}"
    irmc_username: "{{ irmc_user }}"
    irmc_password: "{{ irmc_password }}"
    validate_certs: "{{ validate_certificate }}"
    command: "set"
    license_key: "{{ license_key }}"
  delegate_to: localhost
  tags:
    - set
'''

RETURN = '''
details_for_get:
    description: If command is “get”, the following value is returned.
    contains:
        license_key:
            description: system-locked iRMC license key
            returned: always
            type: string

details_for_set:
    description: If command is “set”, the default return value of Ansible is returned.

'''


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.fujitsu.primergy.plugins.module_utils.irmc_scci_utils import (
    add_scci_command,
    get_scciresult,
    irmc_scci_post,
    scci_body_end,
    scci_body_start,
)

param_scci_map = [
    # Param, SCCI Name, SCCI Code, value dict
    ['license_key', 'ConfBMCLicenseKey', 0x1980],
]


def irmc_license(module):
    result = dict(
        changed=False,
        status=0,
    )

    if module.check_mode:
        result['msg'] = 'module was not run'
        module.exit_json(**result)

    if module.params['command'] == 'set' and module.params['license_key'] is None:
        result['msg'] = "Command 'set' requires 'license_key' to be set!"
        result['status'] = 10
        module.fail_json(**result)

    body = scci_body_start
    if module.params['command'] == 'set':
        body += add_scci_command('SET', param_scci_map, 'ConfBMCLicenseKey', 0, module.params['license_key'])
    else:
        body += add_scci_command('GET', param_scci_map, 'ConfBMCLicenseKey', 0, '')
    body += scci_body_end

    status, data, msg = irmc_scci_post(module, body)
    if status < 100:
        module.fail_json(msg=msg, status=status, exception=data)
    elif status not in (200, 202, 204):
        module.fail_json(msg=msg, status=status)

    licensekey, scciresult, sccicontext = get_scciresult(data.content, 0x1980)
    if scciresult != 0:
        module.fail_json(msg=sccicontext, status=scciresult)

    if module.params['command'] == 'get':
        result['license_key'] = licensekey
    else:
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
        license_key=dict(required=False, type='str'),
    )
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False,
    )

    irmc_license(module)


if __name__ == '__main__':
    main()
