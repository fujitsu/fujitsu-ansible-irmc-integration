#!/usr/bin/python

# Copyright 2018-2024 Fsas Technologies Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


DOCUMENTATION = r'''
---
module: irmc_elcm_offline_update

short_description: offline update a server via iRMC

description:
    - This module has not been verified on iRMC S6. Verification is planned for a future version.
    - Ansible module to offline update a server via iRMC.
    - Using this module may force the server into reboot.
    - Module Version V1.2.

requirements:
    - The module needs to run locally.
    - eLCM needs to be licensed in iRMC.
    - eLCM SD card needs to be mounted.
    - The PRIMERGY server needs to be at least a M2 model.
    - iRMC S4 needs FW >= 9.04, iRMC S5 needs FW >= 1.25.
    - The module assumes that the Update Repository is set correctly in iRMC.
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
        description: How to handle iRMC eLCM Offline Update.
        required:    false
        choices:     ['prepare', 'execute']
    ignore_power_on:
        description: Ignore that server is powered on. Server will reboot during update process.
                     Only valid for option 'execute'.
        required:    false
        default:     false
    skip_hcl_verify:
        description: For VMware OS the Hardware Compatibility List (HCL) verification will be skipped and
                     updates will be offered regardless of their compatibility with the current VMware OS version.
                     Irrelevant for other OS.
        required:    false
        default:     false
    wait_for_finish:
        description: Wait for session to finish.
        required:    false
        default:     true
'''

EXAMPLES = r'''
# Prepare eLCM Offline Update
- name: Prepare eLCM Offline Update
  fujitsu.primergy.irmc_elcm_offline_update:
    irmc_url: "{{ inventory_hostname }}"
    irmc_username: "{{ irmc_user }}"
    irmc_password: "{{ irmc_password }}"
    validate_certs: "{{ validate_certificate }}"
    command: "prepare"
    skip_hcl_verify: "{{ elcm_skip_hcl_verify }}"
    ignore_power_on: false
  delegate_to: localhost

# Execute eLCM Offline Update
- name: Execute eLCM Offline Update
  fujitsu.primergy.irmc_elcm_offline_update:
    irmc_url: "{{ inventory_hostname }}"
    irmc_username: "{{ irmc_user }}"
    irmc_password: "{{ irmc_password }}"
    validate_certs: "{{ validate_certificate }}"
    command: "execute"
    ignore_power_on: false
    wait_for_finish: true
'''

RETURN = r'''
details:
    description:
        The default return value of Ansible (changed, failed, etc.) is returned.
'''


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.fujitsu.primergy.plugins.module_utils.irmc import (
    elcm_check_status,
    get_irmc_json,
    irmc_redfish_get,
    irmc_redfish_post,
    irmc_redfish_put,
    waitForSessionToFinish,
)

# Global
result = dict()


def irmc_elcm_offline_update(module):
    # initialize result
    result['changed'] = False
    result['status'] = 0

    if module.check_mode:
        result['msg'] = 'module was not run'
        module.exit_json(**result)

    # check eLCM status
    status, data, msg = elcm_check_status(module)
    if status > 30 and status < 100:
        module.fail_json(msg=msg, status=status, exception=data)
    elif status < 30 or status not in (200, 202, 204):
        module.fail_json(msg=msg, status=status)

    if module.params['command'] == 'execute' and module.params['ignore_power_on'] is False:
        # Get server power state
        status, sysdata, msg = irmc_redfish_get(module, 'redfish/v1/Systems/0/')
        if status < 100:
            module.fail_json(msg=msg, status=status, exception=sysdata)
        elif status != 200:
            module.fail_json(msg=msg, status=status)
        if get_irmc_json(sysdata.json(), 'PowerState') == 'On':
            result['msg'] = 'Server is powered on. Cannot continue.'
            result['status'] = 10
            module.fail_json(**result)

    if module.params['command'] == 'prepare':
        uri = 'rest/v1/Oem/eLCM/OfflineUpdate'
        if module.params['skip_hcl_verify'] is True:
            uri = uri + '?skipHCLVerification=yes'
        status, elcmdata, msg = irmc_redfish_post(module, uri, '')
    else:
        status, elcmdata, msg = irmc_redfish_put(module, 'rest/v1/Oem/eLCM/OfflineUpdate', '')
    if status < 100:
        module.fail_json(msg=msg, status=status, exception=elcmdata)
    elif status == 409:
        result['msg'] = 'Cannot {0} eLCM update, another session is in progress.'.format(module.params['command'])
        result['status'] = status
        module.fail_json(**result)
    elif status not in (200, 202, 204):
        module.fail_json(msg=msg, status=status)

    if module.params['wait_for_finish'] is True:
        # check that current session is terminated
        status, data, msg = waitForSessionToFinish(module, get_irmc_json(elcmdata.json(), ['Session', 'Id']))
        if status > 30 and status < 100:
            module.fail_json(msg=msg, status=status, exception=data)
        elif status not in (200, 202, 204):
            module.fail_json(msg=msg, log=data, status=status)

    result['changed'] = True

    module.exit_json(**result)


def main():
    # import pdb; pdb.set_trace()
    module_args = dict(
        irmc_url=dict(required=True, type='str'),
        irmc_username=dict(required=True, type='str'),
        irmc_password=dict(required=True, type='str', no_log=True),
        validate_certs=dict(required=False, type='bool', default=True),
        command=dict(required=True, type='str', choices=['prepare', 'execute']),
        ignore_power_on=dict(required=False, type='bool', default=False),
        skip_hcl_verify=dict(required=False, type='bool', default=False),
        wait_for_finish=dict(required=False, type='bool', default=True),
    )
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False,
    )

    irmc_elcm_offline_update(module)


if __name__ == '__main__':
    main()
