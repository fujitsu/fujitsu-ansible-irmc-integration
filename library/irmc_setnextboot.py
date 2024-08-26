#!/usr/bin/python

# Copyright 2018-2024 Fsas Technologies Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


DOCUMENTATION = r'''
---
module: irmc_setnextboot

short_description: configure iRMC to force next boot to specified option

description:
    - Ansible module to configure iRMC to force next boot to specified option.
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
    bootsource:
        description: The source for the next boot.
        required:    false
        default:     BiosSetup
        choices:     ['None', 'Pxe', 'Floppy', 'Cd', 'Hdd', 'BiosSetup']
    bootoverride:
        description: Boot override type.
        required:    false
        default:     Once
        choices:     ['Once', 'Continuous']
    bootmode:
        description: The mode for the next boot.
        required:    false
        choices:     ['Legacy', 'UEFI']
'''

EXAMPLES = r'''
# Set Bios to boot from the specified device.
# Note: boot from virtual CD might fail, if a 'real' DVD drive exists
- name: Set Bios to boot from the specified device.
  irmc_setnextboot:
    irmc_url: "{{ inventory_hostname }}"
    irmc_username: "{{ irmc_user }}"
    irmc_password: "{{ irmc_password }}"
    validate_certs: "{{ validate_certificate }}"
    bootsource: "{{ bootsource }}"
    bootoverride: "{{ bootoverride | default('Once') }}"
    bootmode: "UEFI"
  delegate_to: localhost
'''

RETURN = r'''
details:
    description: The default return value of Ansible (changed, failed, etc.) is returned.
'''


import json

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.irmc import get_irmc_json, irmc_redfish_get, irmc_redfish_patch


def irmc_setnextboot(module: AnsibleModule) -> None:
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
    bootsourceallowed = get_irmc_json(sysdata.json(), ['Boot', 'BootSourceOverrideTarget@Redfish.AllowableValues'])
    if module.params['bootsource'] not in bootsourceallowed:
        result['msg'] = "Invalid parameter '" + module.params['bootsource'] + "' for function. Allowed: " + \
                        json.dumps(bootsourceallowed)
        result['status'] = 10
        module.fail_json(**result)

    # evaluate parameters
    bootoverrideallowed = get_irmc_json(sysdata.json(), ['Boot', 'BootSourceOverrideEnabled@Redfish.AllowableValues'])
    if module.params['bootoverride'] not in bootoverrideallowed:
        result['msg'] = "Invalid parameter '" + module.params['bootoverride'] + "' for function. Allowed: " + \
                        json.dumps(bootoverrideallowed)
        result['status'] = 11
        module.fail_json(**result)

    # Set iRMC system data
    body = {
        'Boot': {
            'BootSourceOverrideTarget': module.params['bootsource'],
            'BootSourceOverrideEnabled': module.params['bootoverride'],
        },
    }
    if module.params['bootmode'] is not None:
        body['Boot']['BootSourceOverrideMode'] = module.params['bootmode']
    etag = get_irmc_json(sysdata.json(), '@odata.etag')
    status, patch, msg = irmc_redfish_patch(module, 'redfish/v1/Systems/0/', json.dumps(body), etag)
    if status < 100:
        module.fail_json(msg=msg, status=status, exception=patch)
    elif status != 200:
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
        bootsource=dict(required=False, type='str', default='BiosSetup',
                        choices=['None', 'Pxe', 'Floppy', 'Cd', 'Hdd', 'BiosSetup']),
        bootoverride=dict(required=False, type='str', default='Once', choices=['Once', 'Continuous']),
        bootmode=dict(required=False, type='str', choices=['UEFI', 'Legacy']),
    )
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False,
    )

    irmc_setnextboot(module)


if __name__ == '__main__':
    main()
