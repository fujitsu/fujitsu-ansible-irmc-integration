#!/usr/bin/python

# Copyright 2018-2024 Fsas Technologies Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = '''
---
module: irmc_biosbootorder

short_description: configure iRMC to force next boot to specified option

description:
    - Ansible module to configure the BIOS boot oder via iRMC.
    - Using this module will force server into several reboots.
    - The module will abort by default if the PRIMERGY server is powered on.
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
        description: Get, set, or reset BIOS Boot Order.
        required:    false
        default:     get
        choices:     ['get', 'set', 'default']
    ignore_power_on:
        description: Ignore that server is powered on.
        required:    false
        default:     false
    boot_key:
        description: Which key to check for in bios boot order devices.
        required:    false
        default:     StructuredBootString
        choices:     ['DeviceName', 'StructuredBootString']
    boot_device:
        description: String to match with specified key for existing boot devices.
                     Needs to be provided for 'set' command.
        required:    false
    force_new:
        description: Force generation of new BiosBootOrder configuration in iRMC before getting or setting boot order.
        default:     false
        required:    false
    next_boot_device:
        description: Set next boot to specified device.
        required:    false
'''

EXAMPLES = '''
- name: Get and show Bios Boot Order
  tags:
    - get
  block:
    - name: Get Bios Boot Order
      fujitsu.primergy.irmc_biosbootorder:
        irmc_url: "{{ inventory_hostname }}"
        irmc_username: "{{ irmc_user }}"
        irmc_password: "{{ irmc_password }}"
        validate_certs: "{{ validate_certificate }}"
        command: "get"
        force_new: "{{ force_new | default(true) }}"
      register: result
      delegate_to: localhost
    - name: Show Bios Boot Order
      ansible.builtin.debug:
        var: result.boot_order

- name: Reset Bios Boot Order to default
  fujitsu.primergy.irmc_biosbootorder:
    irmc_url: "{{ inventory_hostname }}"
    irmc_username: "{{ irmc_user }}"
    irmc_password: "{{ irmc_password }}"
    validate_certs: "{{ validate_certificate }}"
    command: "default"
    ignore_power_on: "{{ ignore_power_on | default(false) }}"
  delegate_to: localhost
  tags:
    - reset
    - default

- name: Set Bios Boot Order
  fujitsu.primergy.irmc_biosbootorder:
    irmc_url: "{{ inventory_hostname }}"
    irmc_username: "{{ irmc_user }}"
    irmc_password: "{{ irmc_password }}"
    validate_certs: "{{ validate_certificate }}"
    command: "set"
    boot_device: "{{ boot_device }}"
    boot_key: "{{ boot_key | default('StructuredBootString') }}"
    ignore_power_on: "{{ ignore_power_on | default(false) }}"
  delegate_to: localhost
  tags:
    - set
'''

RETURN = '''
details_for_get:
    description: If command is “get”, the following values are returned.
    contains:
        DeviceIdx:
            description: device index
            returned: always
            type: int
            sample: 1
        DeviceName:
            description: device name
            returned: always
            type: string
            sample: (Bus 01 Dev 00)PCI RAID Adapter
        StructuredBootString:
            description: structured boot string
            returned: always
            type: string
            sample: RAID.Slot.1.Legacy
otherwise:
    description:
        For other commands, the default return value of Ansible is returned.
'''


import copy
import json

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.fujitsu.primergy.plugins.module_utils.irmc import (
    get_irmc_json,
    irmc_redfish_delete,
    irmc_redfish_get,
    irmc_redfish_post,
    waitForSessionToFinish,
)
from ansible_collections.fujitsu.primergy.plugins.module_utils.irmc_scci_utils import (
    add_scci_command,
    get_scciresultlist,
    irmc_scci_post,
    scci_body_end,
    scci_body_start,
)
from ansible_collections.fujitsu.primergy.plugins.module_utils.irmc_utils import compare_irmc_profile

# Global
result = dict()


def irmc_biosbootorder(module):
    # initialize result
    result['changed'] = False
    result['status'] = 0

    if module.check_mode:
        result['msg'] = 'module was not run'
        module.exit_json(**result)

    # preliminary parameter check
    preliminary_parameter_check(module)

    # check that all iRMC Profile processing states are terminated
    waitForIrmcSessionsInactive(module)

    if module.params['command'] == 'default':
        set_default_bootorder(module)
        result['changed'] = True
        module.exit_json(**result)

    if module.params['force_new'] is True:
        force_new_boot_profile(module)

    # Get Boot Profile Data
    boot_profile_data = get_boot_profile_data(module)
    devices = get_irmc_json(boot_profile_data, ['Server', 'SystemConfig', 'BiosConfig', 'BiosBootOrder', 'Devices'])

    if module.params['command'] == 'get':
        for status, devicelist in devices.items():
            result['boot_order'] = []
            for device in devicelist:
                bo = {}
                bo['DeviceIdx'] = device['@DeviceIdx']
                bo['DeviceName'] = device['DeviceName']
                bo['StructuredBootString'] = device['StructuredBootString']
                result['boot_order'].append(bo)
        module.exit_json(**result)

    # setup new boot order
    new_profile = setup_new_boot_profile(module, boot_profile_data)

    comparison_list = []
    comparison_result, comparison_list = compare_irmc_profile(boot_profile_data, new_profile, '', '', comparison_list)
    if comparison_result is True:
        result['skipped'] = True
        result['msg'] = 'Bios boot order is already as requested.'
        module.exit_json(**result)

    # activate the new profile
    new_profile['Server']['SystemConfig']['BiosConfig']['BiosBootOrder']['BootOrderApply'] = True
    new_profile['Server']['SystemConfig']['BiosConfig']['@Processing'] = 'execute'

    # Set new boot profile
    status, sysdata, msg = irmc_redfish_post(module, 'rest/v1/Oem/eLCM/ProfileManagement/set', json.dumps(new_profile))
    if status < 100:
        module.fail_json(msg=msg, status=status, exception=sysdata)
    elif status not in (200, 202, 204):
        module.fail_json(msg=msg, status=status)

    # check that current session is terminated
    status, data, msg = waitForSessionToFinish(module, get_irmc_json(sysdata.json(), ['Session', 'Id']))
    if status > 30 and status < 100:
        module.fail_json(msg=msg, status=status, exception=data)
    elif status not in (200, 202, 204):
        module.fail_json(msg=msg, log=data, status=status)

    result['changed'] = True
    module.exit_json(**result)


def get_boot_profile_data(module):
    status, sysdata, msg = irmc_redfish_get(module, 'rest/v1/Oem/eLCM/ProfileManagement/BiosBootOrder')
    if status < 100:
        module.fail_json(msg=msg, status=status, exception=sysdata)
    elif status == 404:     # Boot Profile does not yet exist, create
        result['msg'] = "Boot Profile does not yet exist. Create manually or restart with 'force_new' set to 'True'."
        result['status'] = status
        module.fail_json(**result)
    elif status != 200:
        module.fail_json(msg=msg, status=status)

    return sysdata.json()


def preliminary_parameter_check(module):
    if module.params['command'] == 'set' and module.params['boot_device'] is None:
        result['msg'] = "Command 'set' requires 'boot_device' parameter to be set!"
        result['status'] = 10
        module.fail_json(**result)

    if module.params['command'] in ('set', 'default') and module.params['ignore_power_on'] is False:
        # Get server power state
        status, sysdata, msg = irmc_redfish_get(module, 'redfish/v1/Systems/0/')
        if status < 100:
            module.fail_json(msg=msg, status=status, exception=sysdata)
        elif status != 200:
            module.fail_json(msg=msg, status=status)

        if get_irmc_json(sysdata.json(), 'PowerState') == 'On':
            result['skipped'] = True
            result['warnings'] = 'Server is powered on. Cannot continue.'
            module.exit_json(**result)


def setup_new_boot_profile(module, profile):
    index = 0
    boot_devices = ''
    new_profile = copy.deepcopy(profile)
    devices = get_irmc_json(new_profile, ['Server', 'SystemConfig', 'BiosConfig', 'BiosBootOrder', 'Devices'])

    new_bootorder = []
    for msg, devicelist in devices.items():
        for item in devicelist:
            for ikey, value in item.items():
                if ikey == module.params['boot_key'] and value == module.params['boot_device']:
                    index += 1
                    item['@DeviceIdx'] = index
                    if boot_devices != '':
                        boot_devices += ', '
                    boot_devices += item[module.params['boot_key']]
                    new_bootorder.append(item)
        for item in devicelist:
            for ikey, value in item.items():
                if ikey == module.params['boot_key'] and value != module.params['boot_device']:
                    index += 1
                    item['@DeviceIdx'] = index
                    if boot_devices != '':
                        boot_devices += ', '
                    boot_devices += str(item[module.params['boot_key']])
                    new_bootorder.append(item)

    if module.params['boot_device'] not in boot_devices:
        msg = "'boot_device' '{}' cannot be found in existing boot devices: '{}'". \
              format(module.params['boot_device'], boot_devices)
        module.fail_json(msg=msg, status=20)

    if module.params['next_boot_device'] is not None and module.params['next_boot_device'] not in boot_devices:
        msg = "'next_boot_device' '{}' cannot be found in existing boot devices: '{}'". \
              format(module.params['next_boot_device'], boot_devices)
        module.fail_json(msg=msg, status=21)

    # add new boot order to profile
    del new_profile['Server']['SystemConfig']['BiosConfig']['BiosBootOrder']['Devices']['Device']
    new_profile['Server']['SystemConfig']['BiosConfig']['BiosBootOrder']['Devices']['Device'] = new_bootorder
    if module.params['next_boot_device'] is not None:
        new_profile['Server']['SystemConfig']['BiosConfig']['BiosBootOrder']['NextBootDevice'] = \
            module.params['next_boot_device']

    return new_profile


def force_new_boot_profile(module):
    # check whether 'Automatic BiosParameter Backup' is set
    scci_map = [        # Param, SCCI Name, SCCI Code, value
        ['bios_backup_enabled', 'ConfPermanentBiosConfigStorageEnabled', 0x1CC0, None],
        ['bios_config_active', 'ConfPermanentBiosConfigActive', 0x2721, None],
    ]
    datadict = dict()
    datadict['bios_backup_enabled'] = None
    datadict['bios_config_active'] = None

    body = scci_body_start
    for elem in scci_map:
        body += add_scci_command('GET', scci_map, elem[1], 0, '')
    body += scci_body_end

    # send command list to scripting interface
    status, data, msg = irmc_scci_post(module, body)
    if status < 100:
        module.fail_json(msg=msg, status=status, exception=data)
    elif status not in (200, 202, 204, 404):
        module.fail_json(msg=msg, status=status)

    # evaluate results list
    datadict, scciresult, sccicontext = get_scciresultlist(data.content, datadict, scci_map)
    if scciresult != 0:
        module.fail_json(msg=sccicontext, status=status)

    # we only need to generate a new profile if 'Automatic BiosParameter Backup' is not set and active
    if datadict['bios_backup_enabled'] == '0' or datadict['bios_config_active'] == '0':
        # Delete current Boot Profile Data (if it exists)
        status, sysdata, msg = irmc_redfish_delete(module, 'rest/v1/Oem/eLCM/ProfileManagement/BiosBootOrder')
        if status < 100:
            module.fail_json(msg=msg, status=status, exception=sysdata)
        elif status not in (200, 202, 204, 404):
            module.fail_json(msg=msg, status=status)

        # Generate new Boot Profile Data
        url = 'rest/v1/Oem/eLCM/ProfileManagement/get?PARAM_PATH=Server/SystemConfig/BiosConfig/BiosBootOrder'
        status, sysdata, msg = irmc_redfish_post(module, url, '')
        if status < 100:
            module.fail_json(msg=msg, status=status, exception=sysdata)
        elif status not in (200, 202, 204):
            module.fail_json(msg=msg, status=status)

        # check that current session is terminated
        status, data, msg = waitForSessionToFinish(module, get_irmc_json(sysdata.json(), ['Session', 'Id']))
        if status > 30 and status < 100:
            module.fail_json(msg=msg, status=status, exception=data)
        elif status not in (200, 202, 204):
            module.fail_json(msg=msg, log=data, status=status)


def waitForIrmcSessionsInactive(module):
    # Get iRMC Profile processing state
    status, sessiondata, msg = irmc_redfish_get(module, 'sessionInformation')
    if status < 100:
        module.fail_json(msg=msg, status=status, exception=sessiondata)
    elif status not in (200, 202, 204):
        module.fail_json(msg=msg, status=status)

    sessions = get_irmc_json(sessiondata.json(), ['SessionList'])
    for status, session in sessions.items():
        for item in session:
            for ikey, value in item.items():
                if ikey == '#text' and 'Profile' in value:
                    status, sessiondata, msg = waitForSessionToFinish(module, item['@Id'])
        continue


def set_default_bootorder(module):
    new_profile = {
        'Server': {
            '@Version': '1.01',
            'SystemConfig': {
                'BiosConfig': {
                    '@Processing': 'execute',
                    'BiosBootOrder': {
                        'BootOrderReset': True,
                    },
                    '@Version': '1.03',
                },
            },
        },
    }

    if module.params['next_boot_device'] is not None:
        new_profile['Server']['SystemConfig']['BiosConfig']['BiosBootOrder']['NextBootDevice'] = \
            module.params['next_boot_device']

    # Set new boot profile
    status, data, msg = irmc_redfish_post(module, 'rest/v1/Oem/eLCM/ProfileManagement/set', json.dumps(new_profile))
    if status < 100:
        module.fail_json(msg=msg, status=status, exception=data)
    elif status not in (200, 202, 204):
        module.fail_json(msg=msg, status=status)

    # check that current session is terminated
    status, data, msg = waitForSessionToFinish(module, get_irmc_json(data.json(), ['Session', 'Id']))
    if status > 30 and status < 100:
        module.fail_json(msg=msg, status=status, exception=data)
    elif status not in (200, 202, 204):
        module.fail_json(msg=msg, log=data, status=status)


def main():
    # import pdb; pdb.set_trace()
    module_args = dict(
        irmc_url=dict(required=True, type='str'),
        irmc_username=dict(required=True, type='str'),
        irmc_password=dict(required=True, type='str', no_log=True),
        validate_certs=dict(required=False, type='bool', default=True),
        command=dict(required=False, type='str', default='get', choices=['get', 'set', 'default']),
        ignore_power_on=dict(required=False, type='bool', default=False),
        boot_key=dict(required=False, type='str', default='StructuredBootString',
                      choices=['DeviceName', 'StructuredBootString']),
        boot_device=dict(required=False, type='str'),
        force_new=dict(required=False, type='bool', default=False),
        next_boot_device=dict(required=False, type='str'),
    )
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False,
    )

    irmc_biosbootorder(module)


if __name__ == '__main__':
    main()
