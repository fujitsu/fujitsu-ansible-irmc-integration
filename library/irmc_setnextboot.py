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
module: irmc_setnextboot

short_description: configure iRMC to force next boot to specified option

description:
    - Ansible module to configure iRMC to force next boot to specified option.
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
    bootsource:
        description: the source for the next boot
        required:    false
        default:     BiosSetup
        choices:     ['None', 'Pxe', 'Floppy', 'Cd', 'Hdd', 'BiosSetup']
    bootoverride:
        description: boot override type
        required:    false
        default:     Once
        choices:     ['Once', 'Continuous']
    bootmode:
        description: the mode for the next boot
        required:    false
        choices:     ['Legacy', 'UEFI']

notes:
    - See http://manuals.ts.fujitsu.com/file/13371/irmc-restful-spec-en.pdf
    - See http://manuals.ts.fujitsu.com/file/13372/irmc-redfish-wp-en.pdf
'''

EXAMPLES = '''
# Set Bios to next boot from Virtual CD
# Note: boot from virtual CD might fail, if a 'real' DVD drive exists
- name: Set Bios to next boot from Virtual CD
  irmc_setnextboot:
    irmc_url: "{{ inventory_hostname }}"
    irmc_username: "{{ irmc_user }}"
    irmc_password: "{{ irmc_password }}"
    validate_certs: "{{ validate_certificate }}"
    bootsource: "Cd"
    bootoverride: "Once"
    bootmode: "Legacy"
  delegate_to: localhost
'''

RETURN = '''
result:
    description: nextboot action result
    returned: always
    type: dict
'''


# pylint: disable=wrong-import-position
import json
from ansible.module_utils.basic import AnsibleModule

from ansible.module_utils.irmc import irmc_redfish_get, irmc_redfish_patch, get_irmc_json


def irmc_setnextboot(module):
    result = dict(
        changed=False,
        status=0
    )

    if module.check_mode:
        result['msg'] = "module was not run"
        module.exit_json(**result)

    # Get iRMC system data
    status, sysdata, msg = irmc_redfish_get(module, "redfish/v1/Systems/0/")
    if status < 100:
        module.fail_json(msg=msg, exception=sysdata)
    elif status != 200:
        module.fail_json(msg=msg, status=status)

    # Evaluate function params against iRMC
    bootsourceallowed = get_irmc_json(sysdata.json(), ["Boot", "BootSourceOverrideTarget@Redfish.AllowableValues"])
    if module.params['bootsource'] not in bootsourceallowed:
        result['msg'] = "Invalid parameter '" + module.params['bootsource'] + "' for function. Allowed: " + \
                        json.dumps(bootsourceallowed)
        module.fail_json(**result)

    # evaluate parameters
    bootoverrideallowed = get_irmc_json(sysdata.json(), ["Boot", "BootSourceOverrideEnabled@Redfish.AllowableValues"])
    if module.params['bootoverride'] not in bootoverrideallowed:
        result['msg'] = "Invalid parameter '" + module.params['bootoverride'] + "' for function. Allowed: " + \
                        json.dumps(bootoverrideallowed)
        module.fail_json(**result)

    # Set iRMC system data
    body = {
        "Boot": {
            "BootSourceOverrideTarget": module.params['bootsource'],
            "BootSourceOverrideEnabled": module.params['bootoverride']
        }
    }
    if module.params['bootmode'] is not None:
        body['Boot']['BootSourceOverrideMode'] = module.params['bootmode']
    etag = get_irmc_json(sysdata.json(), "@odata.etag")
    status, patch, msg = irmc_redfish_patch(module, "redfish/v1/Systems/0/", json.dumps(body), etag)
    if status < 100:
        module.fail_json(msg=msg, exception=patch)
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
        bootsource=dict(required=False, type="str", default="BiosSetup",
                        choices=["None", "Pxe", "Floppy", "Cd", "Hdd", "BiosSetup"]),
        bootoverride=dict(required=False, type="str", default="Once", choices=["Once", "Continuous"]),
        bootmode=dict(required=False, type="str", choices=["UEFI", "Legacy"]),
    )
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    irmc_setnextboot(module)


if __name__ == '__main__':
    main()
