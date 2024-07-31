#!/usr/bin/python

# Copyright 2018-2024 Fsas Technologies Inc.
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
module: irmc_elcm_online_update

short_description: online update a server via iRMC

description:
    - Ansible module to online update a server via iRMC.
    - Using this module may force the server into reboot.
    - See specification [iRMC RESTful API](http://manuals.ts.fujitsu.com/file/13371/irmc-restful-spec-en.pdf).
    - PRIMERGY servers running ESXi are not capable of eLCM Online Update due to missing agent.
      Please run eLCM Offline Update on ESXi servers.
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
        description: How to handle iRMC eLCM Online Update.
        required:    false
        choices:     ['get', 'set', 'check', 'execute', 'delete']
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
    component:
        description: Component whose execution selection is to be changed.
        required:    false
    subcomponent:
        description: Subcomponent whose execution selection is to be changed.
        required:    false
    select:
        description: Execution selection for specified component/subcomponent.
        required:    false


notes:
    - See http://manuals.ts.fujitsu.com/file/13371/irmc-restful-spec-en.pdf
    - See http://manuals.ts.fujitsu.com/file/13372/irmc-redfish-wp-en.pdf
'''

EXAMPLES = '''
# Generate eLCM Online Update List
- name: Generate eLCM Online Update List
  irmc_elcm_online_update:
    irmc_url: "{{ inventory_hostname }}"
    irmc_username: "{{ irmc_user }}"
    irmc_password: "{{ irmc_password }}"
    validate_certs: "{{ validate_certificate }}"
    command: "check"
    skip_hcl_verify: "{{ elcm_skip_hcl_verify }}"
    wait_for_finish: true
  delegate_to: localhost

# Read eLCM Online Update List
- name: Read eLCM Online Update List
  irmc_elcm_online_update:
    irmc_url: "{{ inventory_hostname }}"
    irmc_username: "{{ irmc_user }}"
    irmc_password: "{{ irmc_password }}"
    validate_certs: "{{ validate_certificate }}"
    command: "get"
  delegate_to: localhost

# De-select entry in eLCM Online Update List
- name: De-select entry in eLCM Online Update List
  irmc_elcm_online_update:
    irmc_url: "{{ inventory_hostname }}"
    irmc_username: "{{ irmc_user }}"
    irmc_password: "{{ irmc_password }}"
    validate_certs: "{{ validate_certificate }}"
    command: "set"
    component: "{{ elcm_component }}"
    subcomponent: "{{ elcm_subcomponent }}"
    select: false
    wait_for_finish: true
  delegate_to: localhost

# Execute eLCM Online Update
- name: Execute eLCM Online Update
  irmc_elcm_online_update:
    irmc_url: "{{ inventory_hostname }}"
    irmc_username: "{{ irmc_user }}"
    irmc_password: "{{ irmc_password }}"
    validate_certs: "{{ validate_certificate }}"
    command: "execute"
    wait_for_finish: true

# Delete eLCM Online Update List
- name: Delete eLCM Online Update List
  irmc_elcm_online_update:
    irmc_url: "{{ inventory_hostname }}"
    irmc_username: "{{ irmc_user }}"
    irmc_password: "{{ irmc_password }}"
    validate_certs: "{{ validate_certificate }}"
    command: "delete"
  delegate_to: localhost
'''

RETURN = '''
# online update collection returned for command "get":
    update_collection:
        description: list of components which require update with specific data
                     (component, subcomponent, status, severity, selected, reboot, current, new)
        returned: always
        type: dict

# For all other commands:
    Default return values:
'''


from ansible.module_utils.basic import AnsibleModule

from ansible.module_utils.irmc import irmc_redfish_get, irmc_redfish_put, irmc_redfish_patch, irmc_redfish_post, \
                                      irmc_redfish_delete, get_irmc_json, elcm_check_status, waitForSessionToFinish


# Global
result = dict()
true_false = {False: "deselected", True: "selected"}


def irmc_elcm_online_update(module):
    # initialize result
    result['changed'] = False
    result['status'] = 0

    if module.check_mode:
        result['msg'] = "module was not run"
        module.exit_json(**result)

    # check eLCM status
    status, data, msg = elcm_check_status(module)
    if status > 30 and status < 100:
        module.fail_json(msg=msg, status=status, exception=data)
    elif status < 30 or status not in (200, 202, 204):
        module.fail_json(msg=msg, status=status)

    # Get server power state
    status, sysdata, msg = irmc_redfish_get(module, "redfish/v1/Systems/0/")
    if status < 100:
        module.fail_json(msg=msg, status=status, exception=sysdata)
    elif status != 200:
        module.fail_json(msg=msg, status=status)
    if get_irmc_json(sysdata.json(), "PowerState") == "Off":
        result['msg'] = "Server is powered off. Cannot continue."
        result['status'] = 12
        module.fail_json(**result)

    # preliminary parameter check
    if module.params['command'] == "set":
        if module.params['component'] is None and module.params['subcomponent'] is None:
            result['msg'] = "Command 'set' requires 'component' and 'subcomponent' parameters to be set!"
            result['status'] = 10
            module.fail_json(**result)
        if module.params['select'] is None:
            result['msg'] = "Command 'set' requires 'select' parameter to be set!"
            result['status'] = 11
            module.fail_json(**result)

    # start doing the actual work
    if module.params['command'] == 'set':
        elcm_change_component(module)

    if module.params['command'] in ("get", "delete"):
        elcm_online_collection(module)

    if module.params['command'] in ("check", "execute"):
        elcm_online_update(module)

    module.exit_json(**result)


def elcm_change_component(module):
    uri = "rest/v1/Oem/eLCM/OnlineUpdate/updateCollection/{0}/{1}?Execution={2}". \
          format(module.params['component'], module.params['subcomponent'],
                 true_false.get(module.params['select']))
    status, elcmdata, msg = irmc_redfish_patch(module, uri, "", 0)
    if status < 100:
        module.fail_json(msg=msg, status=status, exception=elcmdata)
    elif status == 400:
        result['msg'] = "Component '{0}/{1}' does not exist in updateCollection". \
                        format(module.params['component'], module.params['subcomponent'])
        result['status'] = status
        module.fail_json(**result)
    elif status not in (200, 202, 204):
        module.fail_json(msg=msg, status=status)

    result['changed'] = True


def elcm_online_update(module):
    if module.params['command'] == "check":
        uri = "rest/v1/Oem/eLCM/OnlineUpdate"
        if module.params['skip_hcl_verify'] is True:
            uri = uri + "?skipHCLVerification=yes"
        status, elcmdata, msg = irmc_redfish_post(module, uri, "")
    else:
        status, elcmdata, msg = irmc_redfish_put(module, "rest/v1/Oem/eLCM/OnlineUpdate/updateCollection", "")
    if status < 100:
        module.fail_json(msg=msg, status=status, exception=elcmdata)
    elif status == 409:
        result['msg'] = "Cannot {0} eLCM update, another session is in progress.".format(module.params['command'])
        result['status'] = status
        module.fail_json(**result)
    elif status not in (200, 202, 204):
        module.fail_json(msg=msg, status=status)

    if module.params['wait_for_finish'] is True:
        # check that current session is terminated
        status, data, msg = waitForSessionToFinish(module, get_irmc_json(elcmdata.json(), ["Session", "Id"]))
        if status > 30 and status < 100:
            module.fail_json(msg=msg, status=status, exception=data)
        elif status not in (200, 202, 204):
            module.fail_json(msg=msg, log=data, status=status)

    result['changed'] = True


def elcm_online_collection(module):
    if module.params['command'] == "get":
        status, elcmdata, msg = irmc_redfish_get(module, "rest/v1/Oem/eLCM/OnlineUpdate/updateCollection")
    else:
        status, elcmdata, msg = irmc_redfish_delete(module, "rest/v1/Oem/eLCM/OnlineUpdate/updateCollection")
    if status < 100:
        module.fail_json(msg=msg, status=status, exception=elcmdata)
    elif status == 404:
        result['msg'] = "updateCollection does not exist."
        if module.params['command'] == "get":
            result['status'] = status
            module.fail_json(**result)
        else:
            result['skipped'] = True
            module.exit_json(**result)
    elif status not in (200, 202, 204):
        module.fail_json(msg=msg, status=status)

    if module.params['command'] == "get":
        result['update_collection'] = []
        for item in get_irmc_json(elcmdata.json(), ["Links", "Contains"]):
            sw = {}
#            sw['link'] = get_irmc_json(item, ["@odata.id"])
#            sw['name'] = sw['link'].replace("rest/v1/Oem/eLCM/OnlineUpdate/updateCollection/PrimSupportPack-Win/", "")

            status, swdata, msg = irmc_redfish_get(module, get_irmc_json(item, ["@odata.id"]))
            if status < 100:
                module.fail_json(msg=msg, status=status, exception=swdata)
            elif status not in (200, 202, 204):
                module.fail_json(msg=msg, status=status)
            sw['component'] = get_irmc_json(swdata.json(), ["Update", "Component"])
            sw['subcomponent'] = get_irmc_json(swdata.json(), ["Update", "SubComponent"])
            sw['current'] = get_irmc_json(swdata.json(), ["Update", "Current"])
            sw['new'] = get_irmc_json(swdata.json(), ["Update", "New"])
            sw['severity'] = get_irmc_json(swdata.json(), ["Update", "Severity"])
            sw['status'] = get_irmc_json(swdata.json(), ["Update", "Status"])
            sw['reboot'] = get_irmc_json(swdata.json(), ["Update", "Reboot"])
            sw['selected'] = get_irmc_json(swdata.json(), ["Update", "Execution"])
            result['update_collection'].append(sw)
    else:
        result['changed'] = True


def main():
    # import pdb; pdb.set_trace()
    module_args = dict(
        irmc_url=dict(required=True, type="str"),
        irmc_username=dict(required=True, type="str"),
        irmc_password=dict(required=True, type="str", no_log=True),
        validate_certs=dict(required=False, type="bool", default=True),
        command=dict(required=False, type="str", default="get",
                     choices=['get', 'set', 'check', 'execute', 'delete']),
        skip_hcl_verify=dict(required=False, type="bool", default=False),
        wait_for_finish=dict(required=False, type="bool", default=True),
        component=dict(required=False, type="str"),
        subcomponent=dict(required=False, type="str"),
        select=dict(required=False, type="bool"),
    )
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    irmc_elcm_online_update(module)


if __name__ == '__main__':
    main()
