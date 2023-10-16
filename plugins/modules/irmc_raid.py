#!/usr/bin/python

# FUJITSU LIMITED
# Copyright 2018 FUJITSU LIMITED
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
module: irmc_raid

short_description: handle iRMC RAID

description:
    - Ansible module to configure a PRIMERGY server's RAID via iRMC.
    - Using this module may force the server into several reboots.
    - See specification [iRMC RESTful API](http://manuals.ts.fujitsu.com/file/13371/irmc-restful-spec-en.pdf).
    - Module Version V1.2.

requirements:
    - The module needs to run locally.
    - The PRIMERGY server needs to be at least a M2 model.
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
        description: How to handle iRMC RAID.
        required:    false
        default:     get
        choices:     ['get', 'create', 'delete']
    adapter:
        description: The logical number of the adapter to create/delete RAID arrays on/from.
        required:    false
    array:
        description: The logical number of the RAID array to delete. Use -1 for all arrays. Ignored for 'create'.
        required:    false
    level:
        description: Raid level of array to be created. Ignored for 'delete'.
        required:    false
    name:
        description: Name of the array to be created. Ignored for 'delete'.
        required:    false
    wait_for_finish:
        description: Wait for raid session to finish.
        required:    false
        default:     true

notes:
    - See http://manuals.ts.fujitsu.com/file/13371/irmc-restful-spec-en.pdf
    - See http://manuals.ts.fujitsu.com/file/13372/irmc-redfish-wp-en.pdf
'''

EXAMPLES = '''
# Get RAID configuration
- name: Get RAID configuration
  irmc_raid:
    irmc_url: "{{ inventory_hostname }}"
    irmc_username: "{{ irmc_user }}"
    irmc_password: "{{ irmc_password }}"
    validate_certs: "{{ validate_certificate }}"
    command: "get"
  register: raid
  delegate_to: localhost
- name: Show RAID configuration
  debug:
    msg: "{{ raid.configuration }}"

# Create RAID array
- name: Create RAID array
  irmc_raid:
    irmc_url: "{{ inventory_hostname }}"
    irmc_username: "{{ irmc_user }}"
    irmc_password: "{{ irmc_password }}"
    validate_certs: "{{ validate_certificate }}"
    command: "create"
    adapter: "{{ adapter }}"
    level: "{{ level }}"
    name: "{{ name }}"
  delegate_to: localhost

# Delete RAID array
- name: Delete RAID array
  irmc_raid:
    irmc_url: "{{ inventory_hostname }}"
    irmc_username: "{{ irmc_user }}"
    irmc_password: "{{ irmc_password }}"
    validate_certs: "{{ validate_certificate }}"
    command: "delete"
    adapter: "{{ adapter }}"
    array: "{{ array }}"
  delegate_to: localhost
'''

RETURN = '''
# data returned for command "get":
    configuration:
        description: list of available RAID adapters with attached logical and physical disks
        returned: always
        type: dict
        sample:
            [{
                "id": "RAIDAdapter0",
                "logical_drives": [{
                    "raid_level": "1",
                    "disks": [{ "slot": 0, "id": "0", "name": "WDC WD5003ABYX-", "size": "465 GB" },
                              { "slot": 1, "id": "1", "name": "WDC WD5003ABYX-", "size": "465 GB" }],
                    "id": 0,
                    "name": "LogicalDrive_0"
                }, {
                    "raid_level": "0",
                    "disks": [{ "slot": 2, "id": "2", "name": "WDC WD5003ABYX-", "size": "465 GB" }],
                    "id": 1,
                    "name": "LogicalDrive_1"
                }],
                "raid_level": "0,1,5,6,10,50,60",
                "name": "RAIDAdapter0",
                "unused_disks": [{ "slot": 3, "id": "3", "name": "WDC WD5003ABYX-", "size": "465 GB" }]
            }]

# For all commands:
    log:
        description: detailed log data of RAID session
        returned: in case of error
        type: dict
        sample:
            "SessionLog": {
                "Entries": {
                    "Entry": [
                        { "#text": "CreateSession: Session 'obtainProfile' created with id 6", "@date": "2018/11/09 09:39:19" },
                        { "#text": "AttachWorkSequence: Attached work sequence 'obtainProfileParameters' to session 6", "@date": "2018/11/09 09:39:19" },
                        { "#text": "ObtainProfileParameters: Finished processing of profile path 'Server/HWConfigurationIrmc/Adapters/RAIDAdapter' with status 'Error'", "@date": "2018/11/09 09:39:45" },
                        { "#text": "TerminateSession: 'obtainProfileParameters' is being terminated", "@date": "2018/11/09 09:39:45" }
                    ]
                },
                "Id": 6,
                "Tag": "",
                "WorkSequence": "obtainProfileParameters"
            }
'''


import json
from ansible.module_utils.basic import AnsibleModule

from ansible_collections.fujitsu.ansible.plugins.module_utils.irmc import irmc_redfish_get, irmc_redfish_post, irmc_redfish_delete, get_irmc_json, \
                                                                          waitForSessionToFinish


# Global
result = dict()


def irmc_raid(module):
    # initialize result
    result['changed'] = False
    result['status'] = 0

    if module.check_mode:
        result['msg'] = "module was not run"
        module.exit_json(**result)

    # preliminary parameter check
    preliminary_parameter_check(module)

    # get current RAID configuration
    irmc_profile = get_raid_data(module)
    raid_configuration = get_raid_configuration(module, irmc_profile)

    if module.params['command'] == "get":
        result['configuration'] = raid_configuration

    if module.params['command'] == "create":
        create_array(module, raid_configuration)

    if module.params['command'] == "delete":
        delete_array(module, raid_configuration)

    module.exit_json(**result)


def preliminary_parameter_check(module):
    if module.params['command'] != "get":
        # Get server power state
        status, sysdata, msg = irmc_redfish_get(module, "redfish/v1/Systems/0/")
        if status < 100:
            module.fail_json(msg=msg, status=status, exception=sysdata)
        elif status != 200:
            module.fail_json(msg=msg, status=status)
        if get_irmc_json(sysdata.json(), "PowerState") == "On":
            result['msg'] = "Server is powered on. Cannot continue."
            result['status'] = 10
            module.fail_json(**result)
    if module.params['command'] == "create" and \
       module.params['adapter'] is None and module.params['level'] is None:
        result['msg'] = "Command 'create' requires 'adapter' and 'level' to be set."
        result['status'] = 10
        module.fail_json(**result)
    if module.params['command'] == "delete" and module.params['adapter'] is None and module.params['array'] is None:
        result['msg'] = "Command 'delete' requires 'adapter' and 'array' to be set."
        result['status'] = 11
        module.fail_json(**result)


def create_array(module, raid_configuration):
    for adapter in raid_configuration:
        if adapter["id"].replace("RAIDAdapter", "") != module.params['adapter']:
            continue
        else:
            disk_data = adapter['unused_disks']
            if not disk_data:
                result['msg'] = "No un-used disks available on controller {0}".format(module.params['adapter'])
                result['status'] = 41
                module.fail_json(**result)

            if module.params['level'] not in adapter['level']:
                result['msg'] = "Adapter {0} does not support RAID level {1}. Supported: {2}". \
                                format(module.params['adapter'], module.params['level'], adapter['level'])
                result['status'] = 42
                module.fail_json(**result)

            if module.params['name'] is not None:
                raid_array = {"@Action": "Create", "Name": module.params['name'],
                              "RaidLevel": module.params['level']}
            else:
                raid_array = {"@Action": "Create", "RaidLevel": module.params['level']}

            body = {
                "Server": {
                    "HWConfigurationIrmc": {
                        "@Processing": "execute",
                        "Adapters": {
                            "RAIDAdapter": [{
                                "@AdapterId": adapter["id"],
                                "@ConfigurationType": "Addressing",
                                "LogicalDrives": {
                                    "LogicalDrive": [raid_array]
                                },
                            }]
                        },
                        "@Version": "1.00"
                    },
                    "@Version": "1.01"
                }
            }

            # Set new configuration
            apply_raid_configuration(module, body)
            return

    result['msg'] = "Specified adapter {0} does not exist.".format(module.params['adapter'])
    result['status'] = 40
    module.fail_json(**result)


def delete_array(module, raid_configuration):
    for adapter in raid_configuration:
        if adapter["id"].replace("RAIDAdapter", "") != module.params['adapter']:
            continue
        else:
            logical_drives = adapter['logical_drives']

            if not logical_drives:
                result['msg'] = "There are no logical drives on adapter {0}.".format(module.params['adapter'])
                if module.params['array'] == "-1":
                    result['skipped'] = True
                    module.exit_json(**result)
                else:
                    result['status'] = 51
                    module.fail_json(**result)

            lds = []
            for array in logical_drives:
                if module.params['array'] != "-1" and "{0}".format(array["id"]) != module.params['array']:
                    ld = {"@Number": array['id'], "@Action": "None"}
                    continue
                else:
                    ld = {"@Number": array['id'], "@Action": "Delete"}
                lds.append(ld)

            if not lds:
                result['msg'] = "Specified array {0} does not exist.".format(module.params['array'])
                result['status'] = 52
                module.fail_json(**result)

            body = {
                "Server": {
                    "HWConfigurationIrmc": {
                        "@Processing": "execute",
                        "Adapters": {
                            "RAIDAdapter": [{
                                "@AdapterId": adapter["id"],
                                "@ConfigurationType": "Addressing",
                                "LogicalDrives": {
                                    "LogicalDrive": lds
                                },
                            }]
                        },
                        "@Version": "1.00"
                    },
                    "@Version": "1.01"
                }
            }

            # Set new configuration
            apply_raid_configuration(module, body)
            return

    result['msg'] = "Specified adapter {0} does not exist.".format(module.params['adapter'])
    result['status'] = 40
    module.fail_json(**result)


def apply_raid_configuration(module, body):
    status, sysdata, msg = irmc_redfish_post(module, "rest/v1/Oem/eLCM/ProfileManagement/set", json.dumps(body))
    if status < 100:
        module.fail_json(msg=msg, status=status, exception=sysdata)
    elif status == 406:
        result['msg'] = "Raid Configuration cannot be {0}d.".format(module.params['command'])
        module.fail_json(msg=msg, status=status)
    elif status not in (200, 202, 204):
        module.fail_json(msg=msg, status=status)

    if module.params['wait_for_finish'] is True:
        # check that current session is terminated
        status, data, msg = waitForSessionToFinish(module, get_irmc_json(sysdata.json(), ["Session", "Id"]))
        if status > 30 and status < 100:
            module.fail_json(msg=msg, status=status, exception=data)
        elif status not in (200, 202, 204):
            module.fail_json(msg=msg, log=data, status=status)

    result['changed'] = True


def get_raid_data(module):
    # make sure RAIDAdapter profile is up-to-date
    status, sysdata, msg = irmc_redfish_delete(module, "/rest/v1/Oem/eLCM/ProfileManagement/RAIDAdapter")
    if status < 100:
        module.fail_json(msg=msg, status=status, exception=sysdata)
    elif status not in (200, 202, 204, 404):
        module.fail_json(msg=msg, status=status)

    url = "rest/v1/Oem/eLCM/ProfileManagement/get?PARAM_PATH=Server/HWConfigurationIrmc/Adapters/RAIDAdapter"
    status, sysdata, msg = irmc_redfish_post(module, url, "")
    if status < 100:
        module.fail_json(msg=msg, status=status, exception=sysdata)
    elif status == 404:
        result['msg'] = "Requested profile 'HWConfigurationIrmc/Adapters/RAIDAdapter' cannot be created."
        module.fail_json(msg=msg, status=status)
    elif status == 409:
        result['msg'] = "Requested profile 'HWConfigurationIrmc/Adapters/RAIDAdapter' already exists."
        module.fail_json(msg=msg, status=status)
    elif status not in (200, 202, 204):
        module.fail_json(msg=msg, status=status)

    if module.params['wait_for_finish'] is True:
        # check that current session is terminated
        status, data, msg = waitForSessionToFinish(module, get_irmc_json(sysdata.json(), ["Session", "Id"]))
        if status > 30 and status < 100:
            module.fail_json(msg=msg, status=status, exception=data)
        elif status not in (200, 202, 204):
            module.fail_json(msg=msg, log=data, status=status)

    status, sysdata, msg = irmc_redfish_get(module, "/rest/v1/Oem/eLCM/ProfileManagement/RAIDAdapter")
    if status < 100:
        module.fail_json(msg=msg, status=status, exception=sysdata)
    elif status == 404:
        module.fail_json(msg="Requested profile 'HWConfigurationIrmc/Adapters/RAIDAdapter' does not exist.",
                         status=status)
    elif status != 200:
        module.fail_json(msg=msg, status=status)

    return sysdata.json()


def get_raid_configuration(module, irmc_profile):
    raid_configuration = []
    for adapter in get_irmc_json(irmc_profile, ["Server", "HWConfigurationIrmc", "Adapters", "RAIDAdapter"]):
        adapter_list = get_adapter(module, adapter)
        disk_data = get_irmc_json(adapter, ["PhysicalDisks", "PhysicalDisk"])
        ld_data = get_irmc_json(adapter, ["LogicalDrives", "LogicalDrive"])
        for pd in disk_data:
            disk_list = get_disk(pd)
            adapter_list['unused_disks'].append(disk_list)
        if "Key" not in ld_data:
            for ld in ld_data:
                array_list = get_logicaldrive(ld)
                for ref in get_irmc_json(ld, ["ArrayRefs", "ArrayRef"]):
                    for array in get_irmc_json(adapter, ["Arrays", "Array"]):
                        if get_irmc_json(ref, ["@Number"]) == get_irmc_json(array, ["@Number"]):
                            for disk in get_irmc_json(array, ["PhysicalDiskRefs", "PhysicalDiskRef"]):
                                for pd in disk_data:
                                    if get_irmc_json(disk, ["@Number"]) == get_irmc_json(pd, ["@Number"]):
                                        break
                                disk_list = get_disk(pd)
                                array_list['disks'].append(disk_list)
                                adapter_list['unused_disks'].remove(disk_list)
                adapter_list['logical_drives'].append(array_list)
        raid_configuration.append(adapter_list)
    return raid_configuration


def get_adapter(module, adapter):
    ctrl = {}
    ctrl['id'] = get_irmc_json(adapter, ["@AdapterId"])
    ctrl['name'] = ctrl['id']
    ctrl['level'] = get_irmc_json(adapter, ["Features", "RaidLevel"])
    ctrl['logical_drives'] = []
    ctrl['unused_disks'] = []
    status, hwdata, msg = irmc_redfish_get(module, "redfish/v1/Systems/0/Storage?$expand=Members")
    if status < 100:
        module.fail_json(msg=msg, status=status, exception=hwdata)
    elif status != 200:
        module.fail_json(msg=msg, status=status)
    for member in get_irmc_json(hwdata.json(), "Members"):
        # iRMC has each StroageController with its own Storage
        for sc in get_irmc_json(member, "StorageControllers"):
            if get_irmc_json(adapter, ["@AdapterId"]).replace("RAIDAdapter", "") == get_irmc_json(sc, ["MemberId"]):
                ctrl['name'] = get_irmc_json(sc, ["Model"])
                ctrl['firmware'] = get_irmc_json(sc, ["FirmwareVersion"])
                ctrl['drives'] = get_irmc_json(sc, ["Oem", "ts_fujitsu", "DriveCount"])
                ctrl['volumes'] = get_irmc_json(sc, ["Oem", "ts_fujitsu", "VolumeCount"])
                break
    return(ctrl)


def get_logicaldrive(ld):
    logicaldrive = {}
    logicaldrive['id'] = get_irmc_json(ld, ["@Number"])
    logicaldrive['level'] = get_irmc_json(ld, ["RaidLevel"])
    logicaldrive['name'] = get_irmc_json(ld, ["Name"])
    logicaldrive['disks'] = []
    return(logicaldrive)


def get_disk(pd):
    disk = {}
    disk['id'] = get_irmc_json(pd, ["@Number"])
    disk['slot'] = get_irmc_json(pd, ["Slot"])
    disk['name'] = get_irmc_json(pd, ["Product"])
    disk['size'] = "{0} {1}".format(get_irmc_json(pd, ["Size", "#text"]), get_irmc_json(pd, ["Size", "@Unit"]))
    return(disk)


def main():
    # import pdb; pdb.set_trace()
    module_args = dict(
        irmc_url=dict(required=True, type="str"),
        irmc_username=dict(required=True, type="str"),
        irmc_password=dict(required=True, type="str", no_log=True),
        validate_certs=dict(required=False, type="bool", default=True),
        command=dict(required=False, type="str", default="list",
                     choices=['get', 'create', 'delete']),
        adapter=dict(required=False, type="str"),
        array=dict(required=False, type="str"),
        level=dict(required=False, type="str"),
        name=dict(required=False, type="str"),
        wait_for_finish=dict(required=False, type="bool", default=True),
    )
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    irmc_raid(module)


if __name__ == '__main__':
    main()
