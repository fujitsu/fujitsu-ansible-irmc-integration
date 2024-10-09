#!/usr/bin/python

# Copyright 2018-2024 Fsas Technologies Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


DOCUMENTATION = r'''
---
module: irmc_fwbios_update

short_description: update iRMC Firmware or server BIOS

description:
    - Ansible module to get current iRMC update settings or update iRMC Firmware or BIOS via iRMC RedFish interface.
    - BIOS or firmware flash can be initiated from TFTP server or local file.
    - Module Version V1.3.0.

requirements:
    - The module needs to run locally.
    - iRMC S6.
    - Python >= 3.10
    - Python modules 'requests', 'urllib3', 'requests_toolbelt'

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
        description: Get settings or run update.
        required:    false
        default:     get
        choices:     ['get', 'update']
    ignore_power_on:
        description: Ignore that server is powered on.
        required:    false
        default:     false
    update_source:
        description: Where to get the FW or BIOS update file.
        required:    false
        choices:     ['tftp', 'file']
    update_type:
        description: Whether to update iRMC FW or server BIOS.
                     In iRMC FW update, ansible task may not finish even after the update is completed on the server.
        required:    false
        choices:     ['irmc', 'bios']
    timeout:
        description: Timeout for BIOS/iRMC FW flash process in minutes.
                     Ansible task can be stopped by timeout, but it can not stop update already running on the server.
        required:    false
        default:     30
    server_name:
        description: TFTP server name or IP.
                     ignored if update_source is set to 'file'
        required:    false
    file_name:
        description: Path to file containing correct iRMC FW or server BIOS image.
        required:    false
    irmc_flash_selector:
        description: Which iRMC image to replace with the new firmware.
        required:    false
        choices:     ['Auto', 'LowFWImage', 'HighFWImage']
    irmc_boot_selector:
        description: Which iRMC FW image is to be started after iRMC reboot.
        required:    false
        choices:     ['Auto', 'LowFWImage', 'HighFWImage']
'''

EXAMPLES = r'''
# Get irmc firmware and BIOS update settings
- block:
  - name: Get irmc firmware and BIOS update settings
    fujitsu.primergy.irmc_fwbios_update:
      irmc_url: "{{ inventory_hostname }}"
      irmc_username: "{{ irmc_user }}"
      irmc_password: "{{ irmc_password }}"
      validate_certs: "{{ validate_certificate }}"
      command: "get"
    register: fw_settings
    delegate_to: localhost
  - name: Show irmc firmware and BIOS update settings
    debug:
      var: fw_settings.fw_update_configuration
  tags:
    - get_fw

# Update server BIOS from local file
- block:
  - name: Update server BIOS from local file
    fujitsu.primergy.irmc_fwbios_update:
      irmc_url: "{{ inventory_hostname }}"
      irmc_username: "{{ irmc_user }}"
      irmc_password: "{{ irmc_password }}"
      validate_certs: "{{ validate_certificate }}"
      command: "update"
      update_source: "file"
      update_type: "bios"
      file_name: "{{ bios_filename }}"
    delegate_to: localhost
    register: bios_update_file
  - name: Show bios update from local file result
    debug:
      var: bios_update_file
  tags:
    - update_bios_file

# Update server BIOS via TFTP
- block:
  - name: Update server BIOS via TFTP
    fujitsu.primergy.irmc_fwbios_update:
      irmc_url: "{{ inventory_hostname }}"
      irmc_username: "{{ irmc_user }}"
      irmc_password: "{{ irmc_password }}"
      validate_certs: "{{ validate_certificate }}"
      command: "update"
      update_source: "tftp"
      update_type: "bios"
      server_name: "{{ tftp_server }}"
      file_name: "{{ bios_filename }}"
    delegate_to: localhost
    register: bios_update_tftp
  - name: Show bios update via TFTP result
    debug:
      var: bios_update_tftp
  tags:
    - update_bios_tftp

# Update iRMC FW via TFTP
- block:
  - name: Update iRMC FW via TFTP
    fujitsu.primergy.irmc_fwbios_update:
      irmc_url: "{{ inventory_hostname }}"
      irmc_username: "{{ irmc_user }}"
      irmc_password: "{{ irmc_password }}"
      validate_certs: "{{ validate_certificate }}"
      command: "update"
      update_source: "tftp"
      update_type: "irmc"
      server_name: "{{ tftp_server }}"
      file_name: "{{ irmc_filename }}"
      irmc_flash_selector: "Auto"
      irmc_boot_selector: "Auto"
    delegate_to: localhost
    register: irmc_update_tftp
  - name: Show irmc update via TFTP result
    debug:
      var: irmc_update_tftp
  tags:
    - update_irmc_tftp
'''

RETURN = r'''
details:
    description:
        If command is “get”, the following values are returned.

        For update command, the default return value of Ansible (changed, failed, etc.) is returned.

    contains:
        bios_file_name:
            description: BIOS file name
            returned: always
            type: string
            sample: D3279-B1x.R1.20.0.UPC
        bios_version:
            description: current BIOS version
            returned: always
            type: string
            sample: V5.0.0.11 R1.20.0 for D3279-B1x
        irmc_boot_selector:
            description: selector for iRMC FW to boot
            returned: always
            type: string
            sample: MostRecentProgrammedFW
        irmc_file_name:
            description: iRMC Firmware image name
            returned: always
            type: string
            sample: D3279_09.09F_sdr03.12.bin
        irmc_flash_selector:
            description: selector for iRMC FW to flash
            returned: always
            type: string
            sample: Auto
        <fw_image>.BooterVersion:
            description: booter version
            returned: always
            type: string
            sample: 8.08
        <fw_image>.FirmwareBuildDate:
            description: firmware build date
            returned: always
            type: string
            sample: "Dec 1 2017 21:36:17 CEST"
        <fw_image>.FirmwareRunningState:
            description: firmware running state
            returned: always
            type: string
            sample: Inactive
        <fw_image>.FirmwareVersion:
            description: iRMC firmware version
            returned: always
            type: string
            sample: 9.04F
        <fw_image>.ImageDescription:
            description: firmware image description
            returned: always
            type: string
            sample: PRODUCTION RELEASE
        <fw_image>.SDRRId:
            description: sensor data record repository id
            returned: always
            type: string
            sample: 0464
        <fw_image>.SDRRVersion:
            description: sensor data record repository version
            returned: always
            type: string
            sample: 3.11
        power_state:
            description: server power state
            returned: always
            type: string
            sample: Off
        tftp_server_name:
            description: TFTP server name
            returned: always
            type: string
            sample: tftpserver.local
'''


import json
import time
from datetime import datetime

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.fujitsu.primergy.plugins.module_utils.irmc import get_irmc_json, irmc_redfish_get, irmc_redfish_patch, irmc_redfish_post
from ansible_collections.fujitsu.primergy.plugins.module_utils.irmc_upload_file import irmc_redfish_post_file

# Global
result = dict()


def irmc_fwbios_update(module):
    # initialize result
    result['changed'] = False
    result['status'] = 0

    if module.check_mode:
        result['msg'] = 'module was not run'
        module.exit_json(**result)

    # preliminary parameter check
    preliminary_parameter_check(module)

    # check that all tasks are finished properly
    check_all_tasks_are_finished(module)

    # Get iRMC basic data
    status, sysdata, msg = irmc_redfish_get(module, 'redfish/v1/Systems/0/')
    if status < 100:
        module.fail_json(msg=msg, status=status, exception=sysdata)
    elif status != 200:
        module.fail_json(msg=msg, status=status)

    # Get iRMC FW Update data
    update_url = 'redfish/v1/Managers/iRMC/Oem/ts_fujitsu/iRMCConfiguration/FWUpdate/'
    status, fwdata, msg = irmc_redfish_get(module, update_url)
    if status < 100:
        module.fail_json(msg=msg, status=status, exception=fwdata)
    elif status != 200:
        module.fail_json(msg=msg, status=status)

    if module.params['command'] == 'get':
        result['fw_update_configuration'] = setup_resultdata(fwdata, sysdata)
        module.exit_json(**result)
    elif module.params['update_source'] == 'tftp':
        patch_update_data(module, update_url, get_irmc_json(fwdata.json(), '@odata.etag'))

    if module.params['update_source'] == 'file':
        status, udata, msg = irmc_redfish_post_file(module, get_update_url(module), module.params['file_name'])
    elif module.params['update_source'] == 'tftp':
        status, udata, msg = irmc_redfish_post(module, get_update_url(module), body='')
    else:
        module.fail_json(msg=f'{module.params["update_source"]}: unknown update_source')

    if status < 100:
        module.fail_json(msg=msg, status=status, exception=udata)
    elif status not in (200, 202, 204):
        if status == 104 and module.params['update_type'] == 'irmc':
            msg = f'{msg} This message might indicate that iRMC needs to reboot before FW update.'
        if status == 400:
            msg = f'{msg} This message might be due to the binary file being invalid for the server.'
        module.fail_json(msg=msg, status=status)

    wait_for_update_to_finish(module, udata.headers['Location'], get_irmc_json(sysdata.json(), 'PowerState'))
    module.exit_json(**result)


def get_update_url(module):
    if module.params['update_source'] == 'tftp':
        if module.params['update_type'] == 'irmc':
            url = 'redfish/v1/Managers/iRMC/Actions/FTSManager.FWTFTPUpdate'
        else:
            url = 'redfish/v1/Systems/0/Bios/Actions/Oem/FTSBios.BiosTFTPUpdate'
    elif module.params['update_type'] == 'irmc':
        url = 'redfish/v1/Managers/iRMC/Actions/FTSManager.FWUpdate'
    else:
        url = 'redfish/v1/Systems/0/Bios/Actions/Oem/FTSBios.BiosUpdate'
    return url


def preliminary_parameter_check(module):
    if module.params['command'] == 'update':
        if module.params['update_source'] is None or module.params['update_type'] is None or \
           module.params['file_name'] is None:
            result['msg'] = "Command 'update' requires 'update_source, update_type, file_name' parameters to be set!"
            result['status'] = 10
            module.fail_json(**result)
        if module.params['update_source'] == 'tftp' and module.params['server_name'] is None:
            result['msg'] = "TFTP update requires 'server_name' parameter to be set!"
            result['status'] = 11
            module.fail_json(**result)

        if module.params['ignore_power_on'] is False:
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


def wait_for_update_to_finish(module, location, power_state):
    rebootDone = None
    start_time = time.time()
    while True:
        time.sleep(5)
        elapsed_time = time.time() - start_time
        # make sure the module does not get stuck if anything goes wrong
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if elapsed_time > module.params['timeout'] * 60:
            msg = 'Timeout of {0} minutes exceeded. Abort.'.format(module.params['timeout'])
            module.fail_json(msg=msg, status=20)

        status, sdata, msg = irmc_redfish_get(module, f'{location[1:]}')
        if status == 99:
            time.sleep(55)
            continue
        elif status == 404:
            if rebootDone is True:
                result['changed'] = True
                break
            continue
        elif status == 503:
            if rebootDone is None:
                rebootDone = False      # just in case we miss the 'complete' message
            else:
                rebootDone = True
            time.sleep(25)
            continue
        elif status < 100 or (status not in (200, 202, 204)):
            time.sleep(5)
            continue

        if 'Key' in get_irmc_json(sdata.json(), 'error'):
            rebootDone = False
            oemstate = get_irmc_json(sdata.json(), ['Oem', 'ts_fujitsu', 'StatusOEM'])
            state = get_irmc_json(sdata.json(), 'TaskState')
            # make sure the process ran through
            if power_state == 'On' and oemstate == 'Pending':
                msg = 'A BIOS firmware update has been started and a system reboot is required to continue the update.'
                result['warnings'] = msg
                break
            if power_state == 'On' and oemstate == 'FlashImageDownloadedSuccessfully':
                msg = 'A BIOS firmware update has been started. A system reboot is required to continue the update.'
                result['warnings'] = msg
                break
            if power_state == 'On' and oemstate == 'FlashingFinishedSuccessfullyRebootRequired':
                msg = 'A iRMC firmware update has finished. A system reboot is required to activate the update.'
                result['warnings'] = msg
                break
            if state == 'Exception':
                msg = f'{now}: Update failed.'
                module.fail_json(msg=msg, status=21)
            # for BIOS we are done here, for iRMC we need to wait for iRMC shutdown and reboot
            if module.params['update_type'] == 'bios' and state == 'Completed':
                result['changed'] = True
                break
        else:
            break


def patch_update_data(module, update_url, etag):
    body = {}
    if module.params['update_source'] == 'tftp':
        body['ServerName'] = module.params['server_name']
        if module.params['update_type'] == 'irmc':
            body['iRMCFileName'] = module.params['file_name']
        else:
            body['BiosFileName'] = module.params['file_name']
    if module.params['irmc_flash_selector'] is not None:
        body['iRMCFlashSelector'] = module.params['irmc_flash_selector']
    if module.params['irmc_boot_selector'] is not None:
        body['iRMCBootSelector'] = module.params['irmc_boot_selector']

    if body != {}:
        status, patch, msg = irmc_redfish_patch(module, update_url, json.dumps(body), etag)
        if status < 100:
            module.fail_json(msg=msg, status=status, exception=patch)
        elif status != 200:
            module.fail_json(msg=msg, status=status)


def check_all_tasks_are_finished(module):
    status, taskdata, msg = irmc_redfish_get(module, 'redfish/v1/TaskService/Tasks')
    if status < 100:
        module.fail_json(msg=msg, status=status, exception=taskdata)
    elif status not in (200, 202, 204):
        module.fail_json(msg=msg, status=status)
    tasks = get_irmc_json(taskdata.json(), ['Members'])
    for task in tasks:
        url = get_irmc_json(task, '@odata.id')
        status, sdata, msg = irmc_redfish_get(module, f'{url[1:]}')
        if status < 100:
            module.fail_json(msg=msg, status=status, exception=sdata)
        elif status not in (200, 202, 204):
            module.fail_json(msg=msg, status=status)

        task_state = get_irmc_json(sdata.json(), ['Oem', 'ts_fujitsu', 'StatusOEM'])
        if task_state in ('Pending', 'FlashImageDownloadedSuccessfully'):
            msg = 'Firmware update has already been started, system reboot is required. Cannot continue new update.'
            module.fail_json(msg=msg, status=30)
        task_progress = get_irmc_json(sdata.json(), ['Oem', 'ts_fujitsu', 'TotalProgressPercent'])
        if str(task_progress) != '100':
            msg = "Task '{0}' is still in progress. Cannot continue new update.". \
                  format(get_irmc_json(sdata.json(), 'Name'))
            module.fail_json(msg=msg, status=31)


def setup_resultdata(data, sysdata):
    configuration = {
        'tftp_server_name': get_irmc_json(data.json(), 'ServerName'),
        'irmc_file_name': get_irmc_json(data.json(), 'iRMCFileName'),
        'irmc_flash_selector': get_irmc_json(data.json(), 'iRMCFlashSelector'),
        'irmc_boot_selector': get_irmc_json(data.json(), 'iRMCBootSelector'),
        'irmc_fw_low': get_irmc_json(data.json(), 'iRMCFwImageLow'),
        'irmc_fw_high': get_irmc_json(data.json(), 'iRMCFwImageHigh'),
        'bios_file_name': get_irmc_json(data.json(), 'BiosFileName'),
        'bios_version': get_irmc_json(sysdata.json(), 'BiosVersion'),
        'power_state': get_irmc_json(sysdata.json(), 'PowerState'),
    }
    return configuration


def main():
    # import pdb; pdb.set_trace()
    module_args = dict(
        irmc_url=dict(required=True, type='str'),
        irmc_username=dict(required=True, type='str'),
        irmc_password=dict(required=True, type='str', no_log=True),
        validate_certs=dict(required=False, type='bool', default=True),
        command=dict(required=False, type='str', default='get', choices=['get', 'update']),
        ignore_power_on=dict(required=False, type='bool', default=False),
        update_source=dict(required=False, type='str', choices=['tftp', 'file']),
        update_type=dict(required=False, type='str', choices=['irmc', 'bios']),
        timeout=dict(required=False, type='int', default=30),
        server_name=dict(required=False, type='str'),
        file_name=dict(required=False, type='str'),
        irmc_flash_selector=dict(required=False, type='str', choices=['Auto', 'LowFWImage', 'HighFWImage']),
        irmc_boot_selector=dict(required=False, type='str', choices=['Auto', 'LowFWImage', 'HighFWImage']),
    )
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False,
    )

    irmc_fwbios_update(module)


if __name__ == '__main__':
    main()
