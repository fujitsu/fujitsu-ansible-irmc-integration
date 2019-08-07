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
module: irmc_task

short_description: handle iRMC tasks

description:
    - Ansible module to handle iRMC tasks via Restful API.
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
        description: Handle iRMC tasks.
        required:    false
        default:     list
        choices:     ['list', 'get']
    id:
        description: Specific task to get.
        required:    false

notes:
    - See http://manuals.ts.fujitsu.com/file/13371/irmc-restful-spec-en.pdf
    - See http://manuals.ts.fujitsu.com/file/13372/irmc-redfish-wp-en.pdf
'''

EXAMPLES = '''
# List iRMC tasks
- name: List iRMC tasks
  irmc_task:
    irmc_url: "{{ inventory_hostname }}"
    irmc_username: "{{ irmc_user }}"
    irmc_password: "{{ irmc_password }}"
    validate_certs: "{{ validate_certificate }}"
    command: "list"
  delegate_to: localhost

# Get specific task information
- name: Get specific task information
  irmc_task:
    irmc_url: "{{ inventory_hostname }}"
    irmc_username: "{{ irmc_user }}"
    irmc_password: "{{ irmc_password }}"
    validate_certs: "{{ validate_certificate }}"
    command: "get"
    id: 3
  delegate_to: localhost
'''

RETURN = '''
# task data returned for command "get":
    Id:
        description: task ID
        returned: always
        type: int
        sample: 3
    Name:
        description: task name
        returned: always
        type: string
        sample: ProfileParametersApply
    StartTime:
        description: start time
        returned: always
        type: string
        sample: "2018-07-31 12:23:02"
    EndTime:
        description: end time
        returned: always
        type: string
        sample: "2018-07-31 12:26:44"
    State:
        description: task state
        returned: always
        type: string
        sample: Completed
    StateOem:
        description: Oem task state
        returned: always
        type: string
        sample: LcmSessFinished
    StateProgressPercent:
        description: state progress in %
        returned: always
        type: string
        sample: 100
    TotalProgressPercent:
        description: overall progress in %
        returned: always
        type: string
        sample: 100

# tasks data returned for command "list":
    List of individual task entries (see above):
'''


from ansible.module_utils.basic import AnsibleModule

from ansible.module_utils.irmc import irmc_redfish_get, get_irmc_json


# Global
result = dict()


def irmc_task(module):
    # initialize result
    result['changed'] = False
    result['status'] = 0

    if module.check_mode:
        result['msg'] = "module was not run"
        module.exit_json(**result)

    # preliminary parameter check
    if (module.params['command'] in ("get", "remove", "terminate")) and module.params['id'] is None:
        result['msg'] = "Command '{0}' requires 'id' parameter to be set!".format(module.params['command'])
        result['status'] = 10
        module.fail_json(**result)

    id_found = 0
    if module.params['command'] == "get":
        id_found = 1
        result['task'] = get_irmc_task_info(module, "/redfish/v1/TaskService/Tasks/{0}".
                                            format(module.params['id']), module.params['id'])

    if module.params['command'] == "list":
        status, taskdata, msg = irmc_redfish_get(module, "redfish/v1/TaskService/Tasks")
        if status < 100:
            module.fail_json(msg=msg, status=status, exception=taskdata)
        elif status not in (200, 202, 204):
            module.fail_json(msg=msg, status=status)
        tasks = get_irmc_json(taskdata.json(), ["Members"])

        result['tasks'] = []
        for task in tasks:
            id_found += 1
            task_url = get_irmc_json(task, "@odata.id")
            myID = task_url.replace("/redfish/v1/TaskService/Tasks/", "")
            task_info = get_irmc_task_info(module, task_url, myID)
            result['tasks'].append(task_info)

    module.exit_json(**result)


def get_irmc_task_info(module, url, task_id):
    status, sdata, msg = irmc_redfish_get(module, "{0}".format(url[1:]))
    if status < 100:
        module.fail_json(msg=msg, status=status, exception=sdata)
    elif status not in (200, 202, 204):
        module.fail_json(msg=msg, status=status)

    task = {}
    task['Id'] = task_id
    task['Name'] = get_irmc_json(sdata.json(), "Name")
    task['State'] = get_irmc_json(sdata.json(), "TaskState")
    task['StateOem'] = get_irmc_json(sdata.json(), ["Oem", "ts_fujitsu", "StatusOEM"])
    task['StateProgressPercent'] = get_irmc_json(sdata.json(), ["Oem", "ts_fujitsu", "StateProgressPercent"])
    task['TotalProgressPercent'] = get_irmc_json(sdata.json(), ["Oem", "ts_fujitsu", "TotalProgressPercent"])
    task['StartTime'] = get_irmc_json(sdata.json(), "StartTime")
    task['EndTime'] = get_irmc_json(sdata.json(), "EndTime")
    return task


def main():
    # import pdb; pdb.set_trace()
    module_args = dict(
        irmc_url=dict(required=True, type="str"),
        irmc_username=dict(required=True, type="str"),
        irmc_password=dict(required=True, type="str", no_log=True),
        validate_certs=dict(required=False, type="bool", default=True),
        command=dict(required=False, type="str", default="list", choices=['list', 'get']),
        id=dict(required=False, type="int")
    )
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    irmc_task(module)


if __name__ == '__main__':
    main()
