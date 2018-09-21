#!/usr/bin/python

# FUJITSU Limited
# Copyright 2018 FUJITSU LIMITED
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
module: irmc_license

short_description: manage iRMC user accounts

description:
    - Ansible module to manage iRMC user accounts via iRMC remote scripting interface.
    - Module Version V1.0.1.

requirements:
    - The module needs to run locally.
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
        description: license key management to be executed
        required:    false
        default:     get
        choices:     ['get', 'set']
    license_key:
        description: iRMC license key to be set
        required:    false

notes:
    - A license key which was read from an iRMC is 'system-locked'. It can imported to the same iRMC,
      but not to another iRMC.
    - See http://manuals.ts.fujitsu.com/file/12563/wp-svs-irmc-remote-scripting-en.pdf
    - See https://sp.ts.fujitsu.com/dmsp/Publications/public/dp-svs-configuration-space-values-en.pdf
'''

EXAMPLES = '''
# Get iRMC license key
- name: Get iRMC license key
  irmc_license:
    irmc_url: "{{ inventory_hostname }}"
    irmc_username: "{{ irmc_user }}"
    irmc_password: "{{ irmc_password }}"
    validate_certs: "{{ validate_certificate }}"
    command: "get"
  register: license
  delegate_to: localhost
- name: show certificates
  debug:
    msg: "{{ license.license_key }}"

# Set iRMC license key
- name: Set iRMC license key
  irmc_license:
    irmc_url: "{{ inventory_hostname }}"
    irmc_username: "{{ irmc_user }}"
    irmc_password: "{{ irmc_password }}"
    validate_certs: "{{ validate_certificate }}"
    command: "set"
    license_key: "{{ license_key }}"
  delegate_to: localhost
'''

RETURN = '''
license_key:
    description: iRMC license key
    returned: always
    type: string
'''


# pylint: disable=wrong-import-position
from ansible.module_utils.basic import AnsibleModule

from ansible.module_utils.irmc_scci_utils import get_scciresult,irmc_scci_post, add_scci_command, \
                                                 scci_body_start, scci_body_end


param_scci_map = [
    # Param, SCCI Name, SCCI Code, value dict
    ["license_key", "ConfBMCLicenseKey", 0x1980],
]


def irmc_license(module):
    result = dict(
        changed=False,
        status=0
    )

    if module.check_mode:
        result['msg'] = "module was not run"
        module.exit_json(**result)

    if module.params['command'] == "set" and module.params['license_key'] is None:
        result['msg'] = "Command 'set' requires 'license_key' to be set!"
        module.fail_json(**result)

    body = scci_body_start
    if module.params['command'] == "set":
        body += add_scci_command("SET", param_scci_map, "ConfBMCLicenseKey", 0, module.params['license_key'])
    else:
        body += add_scci_command("GET", param_scci_map, "ConfBMCLicenseKey", 0, "")
    body += scci_body_end

    status, data, msg = irmc_scci_post(module, body)
    if status < 100:
        module.fail_json(msg=msg, exception=data)
    elif status != 200 and status != 204:
        module.fail_json(msg=msg, status=status)

    licensekey, scciresult, sccicontext = get_scciresult(data.content, 0x1980)
    if scciresult != 0:
        result['msg'] = sccicontext
        module.fail_json(**result)

    if module.params['command'] == "get":
        result['license_key'] = licensekey
    else:
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
        license_key=dict(required=False, type="str"),
    )
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    irmc_license(module)


if __name__ == '__main__':
    main()
