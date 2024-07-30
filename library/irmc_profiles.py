#!/usr/bin/python

# Copyright 2018-2024 Fsas Technologies INC.
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
module: irmc_profiles

short_description: handle iRMC profiles

description:
    - Ansible module to configure the BIOS boot oder via iRMC.
    - Using this module may force server into several reboots.
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
        description: How to handle iRMC profiles.
        required:    false
        default:     list
        choices:     ['list', 'get', 'create', 'delete', 'import']
    profile:
        description: Which iRMC profile to handle.
                     Only relevant for 'get', 'create', 'delete'.
        required:    false
    profile_json:
        description: Direct input of iRMC profile data.
                     Only evaluated for command='import'. When set, 'profile_path' is ignored.
        required:    false
    profile_path:
        description: Path file where to read a profile.
                     Only evaluated for command='import'. Ignored when 'profile_json' is set.
        required:    false
    wait_for_finish:
        description: Wait for 'create profile' or 'import profile' session to finish. Ignored otherwise.
        required:    false
        default:     true

notes:
    - See http://manuals.ts.fujitsu.com/file/13371/irmc-restful-spec-en.pdf
    - See http://manuals.ts.fujitsu.com/file/13372/irmc-redfish-wp-en.pdf
'''

EXAMPLES = '''
# List iRMC profiles
- name: List iRMC profiles
  irmc_profiles:
    irmc_url: "{{ inventory_hostname }}"
    irmc_username: "{{ irmc_user }}"
    irmc_password: "{{ irmc_password }}"
    validate_certs: "{{ validate_certificate }}"
    command: "list"
  delegate_to: localhost

# Get iRMC HWConfigurationIrmc profile
- name: Get iRMC HWConfigurationIrmc profile
  irmc_profiles:
    irmc_url: "{{ inventory_hostname }}"
    irmc_username: "{{ irmc_user }}"
    irmc_password: "{{ irmc_password }}"
    validate_certs: "{{ validate_certificate }}"
    command: "get"
    profile: "HWConfigurationIrmc"
  delegate_to: localhost
'''

RETURN = '''
# profiles returned for command "list":
    <profile_name>:
        description: name of specific profile
        returned: always
        type: dict
        sample: BiosBootOrder
    <profile_name>.Location:
        description: RedFish location of profile
        returned: always
        type: string
        sample: rest/v1/Oem/eLCM/ProfileManagement/BiosBootOrder
    <profile_name>.Name:
        description: name of profile
        returned: always
        type: string
        sample: BiosBootOrder

# profile data returned for command "get":
    profile:
        description: data of requested profile
        returned: always
        type: dict

# For all other commands:
    Default return values:
'''


import json
import os.path
from ansible.module_utils.basic import AnsibleModule

from ansible.module_utils.irmc import irmc_redfish_get, irmc_redfish_post, irmc_redfish_delete, get_irmc_json, \
                                      waitForSessionToFinish


# Global
result = dict()


def irmc_profiles(module):
    # initialize result
    result['changed'] = False
    result['status'] = 0

    if module.check_mode:
        result['msg'] = "module was not run"
        module.exit_json(**result)

    # preliminary parameter check
    if module.params['command'] == "import":
        if module.params['profile_json'] is None and not os.path.isfile(module.params['profile_path']):
            module.fail_json(msg="Got no profile to import.", status=10)
    if module.params['command'] not in ('list', 'import') and module.params['profile'] is None:
        result['msg'] = "Command '{0}' requires parameter 'profile' to be set.".format(module.params['command'])
        result['status'] = 11
        module.fail_json(**result)

    # start doing the actual work
    if module.params['command'] == "list":
        list_profiles(module)

    if module.params['command'] == "get":
        get_profile(module)

    if module.params['command'] == "create":
        create_profile(module)

    if module.params['command'] == "delete":
        delete_profile(module)

    if module.params['command'] == "import":
        import_profile(module)

    module.exit_json(**result)


def import_profile(module):
    if module.params['profile_json'] is None:
        try:
            with open(module.params['profile_path']) as infile:
                irmc_profile = json.load(infile)
        except Exception:
            result['msg'] = "Could not read JSON profile data from file '{0}'".format(module.params['profile_path'])
            result['status'] = 20
            module.fail_json(**result)
    else:
        try:
            irmc_profile = json.loads(module.params['profile_json'])
        except Exception:
            result['msg'] = "Profile data are not proper JSON '{0}'.".format(module.params['profile_json'])
            result['status'] = 21
            module.fail_json(**result)

    irmc_profile = checkandupdate_irmc_profile(module, irmc_profile)

    # Set new profile
    status, sysdata, msg = irmc_redfish_post(module, "rest/v1/Oem/eLCM/ProfileManagement/set",
                                             json.dumps(irmc_profile))
    if status < 100:
        module.fail_json(msg=msg, status=status, exception=sysdata)
    elif status == 404:
        result['msg'] = "Requested profile '{0}' cannot be imported.".format(module.params['profile'])
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


def delete_profile(module):
    status, sysdata, msg = irmc_redfish_delete(module, "/rest/v1/Oem/eLCM/ProfileManagement/{0}".
                                               format(module.params['profile']))
    if status < 100:
        module.fail_json(msg=msg, status=status, exception=sysdata)
    elif status == 404:
        result['msg'] = "Profile '{0}' does not exist.".format(module.params['profile'])
        result['skipped'] = True
        module.exit_json(**result)
    elif status not in (200, 202, 204):
        module.fail_json(msg=msg, status=status)

    # 'delete' does not create a session, no need to wait
    result['changed'] = True


def create_profile(module):
    url = "rest/v1/Oem/eLCM/ProfileManagement/get?PARAM_PATH=Server/{0}".format(module.params['profile'])
    status, sysdata, msg = irmc_redfish_post(module, url, "")
    if status < 100:
        module.fail_json(msg=msg, status=status, exception=sysdata)
    elif status == 404:
        result['msg'] = "Requested profile '{0}' cannot be created.".format(module.params['profile'])
        module.fail_json(msg=msg, status=status)
    elif status == 409:
        result['msg'] = "Requested profile '{0}' already exists.".format(module.params['profile'])
        result['skipped'] = True
        module.exit_json(**result)
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


def list_profiles(module):
    status, sysdata, msg = irmc_redfish_get(module, "/rest/v1/Oem/eLCM/ProfileManagement")
    if status < 100:
        module.fail_json(msg=msg, status=status, exception=sysdata)
    elif status != 200:
        module.fail_json(msg=msg, status=status)

    result['profiles'] = {}
    for profile in get_irmc_json(sysdata.json(), ["Links", "profileStore"]):
        for status, value in profile.items():
            profile = {}
            profile['Name'] = value.replace("rest/v1/Oem/eLCM/ProfileManagement/", "")
            profile['Location'] = value
            result['profiles'][value.replace("rest/v1/Oem/eLCM/ProfileManagement/", "")] = profile


def get_profile(module):
    status, sysdata, msg = irmc_redfish_get(module, "/rest/v1/Oem/eLCM/ProfileManagement/{0}".
                                            format(module.params['profile']))
    if status < 100:
        module.fail_json(msg=msg, status=status, exception=sysdata)
    elif status == 404:
        module.fail_json(msg="Requested profile '{0}' does not exist.".
                         format(module.params['profile']), status=status)
    elif status != 200:
        module.fail_json(msg=msg, status=status)

    result['profile'] = sysdata.json()


def checkandupdate_irmc_profile(module, profile):
    server = get_irmc_json(profile, ['Server'])
    if "Key does not exist" in server:
        module.fail_json(msg="Invalid iRMC JSON: '{0}'.".format(profile), status=30)
    else:
        sysconfig = get_irmc_json(profile, ['Server', 'SystemConfig'])
        if "Key does not exist" in sysconfig:
            adapterconfig = get_irmc_json(profile, ['Server', 'AdapterConfigIrmc'])
            if "Key does not exist" in adapterconfig:
                hwconfig = get_irmc_json(profile, ['Server', 'HWConfigurationIrmc'])
                if "Key does not exist" in hwconfig:
                    module.fail_json(msg="Invalid iRMC JSON: '{0}'.".format(profile), status=31)
                else:
                    profile['Server']['HWConfigurationIrmc']['@Processing'] = "execute"
            else:
                profile['Server']['AdapterConfigIrmc']['@Processing'] = "execute"
        else:
            biosconfig = get_irmc_json(profile, ['Server', 'SystemConfig', 'BiosConfig'])
            irmcconfig = get_irmc_json(profile, ['Server', 'SystemConfig', 'IrmcConfig'])
            if "Key does not exist" in biosconfig and "Key does not exist" in irmcconfig:
                msg = "Invalid iRMC JSON: '{0}'.".format(profile)
                return 3, msg
            if "Key does not exist" not in biosconfig:
                biosbootorder = get_irmc_json(profile, ['Server', 'SystemConfig', 'BiosConfig', 'BiosBootOrder'])
                if "Key does not exist" not in biosbootorder:
                    profile['Server']['SystemConfig']['BiosConfig']['BiosBootOrder']['BootOrderApply'] = True
                profile['Server']['SystemConfig']['BiosConfig']['@Processing'] = "execute"
            if "Key does not exist" not in irmcconfig:
                profile['Server']['SystemConfig']['IrmcConfig']['@Processing'] = "execute"
    return profile


def main():
    # import pdb; pdb.set_trace()
    module_args = dict(
        irmc_url=dict(required=True, type="str"),
        irmc_username=dict(required=True, type="str"),
        irmc_password=dict(required=True, type="str", no_log=True),
        validate_certs=dict(required=False, type="bool", default=True),
        command=dict(required=False, type="str", default="list",
                     choices=['list', 'get', 'create', 'delete', 'import']),
        profile=dict(required=False, type="str"),
        profile_json=dict(required=False, type="str"),
        profile_path=dict(required=False, type="str"),
        wait_for_finish=dict(required=False, type="bool", default=True),
    )
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    irmc_profiles(module)


if __name__ == '__main__':
    main()
