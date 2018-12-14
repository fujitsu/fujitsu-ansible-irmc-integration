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
module: irmc_elcm_repository

short_description: configure the eLCM repostory in iRMC

description:
    - Ansible module to configure the eLCM repostory in iRMC.
    - iRMC tests access to specified repository and refuses to accept data in case of failure.
    - See specification [iRMC RESTful API](http://manuals.ts.fujitsu.com/file/13371/irmc-restful-spec-en.pdf).
    - Module Version V1.2.

requirements:
    - The module needs to run locally.
    - The PRIMERGY server needs to be at least a M2 model.
    - eLCM needs to be licensed in iRMC.
    - eLCM SD card needs to be mounted.
    - iRMC S4 needs FW >= 9.04, iRMC S5 needs FW >= 1.25.
    - Python >= 2.6
    - Python modules 'future', 'requests', 'urllib3'

version_added: "2.4"

author:
    - Fujitsu Server PRIMERGY (@FujitsuPrimergy)

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
        description: How to handle iRMC eLCM respository data.
        required:    false
        default:     get
        choices:     ['get', 'set']
    server:
        description: Server where eLCM Update Repository is located.
                     Needs to be set together with 'catalog'.
        required:    false
    catalog:
        description: Path to eLCM Update Repository on server.
                     Needs to be set together with 'server'.
        required:    false
    use_proxy:
        description: Whether to use proxy to access eLCM Update Repository.
        required:    false
    proxy_url:
        description: Proxy server to access eLCM Update Repository.
        required:    false
    proxy_port:
        description: Proxy port to access eLCM Update Repository.
        required:    false
    proxy_user:
        description: Proxy user to access eLCM Update Repository.
        required:    false
    proxy_password:
        description: Proxy password to access eLCM Update Repository.
        required:    false
    wait_for_finish:
        description: Wait for session to finish.
        required:    false
        default:     true

notes:
    - See http://manuals.ts.fujitsu.com/file/13371/irmc-restful-spec-en.pdf
    - See http://manuals.ts.fujitsu.com/file/13372/irmc-redfish-wp-en.pdf
'''

EXAMPLES = '''
# Get eLCM repository data
- name: Get eLCM repository data
  irmc_elcm_repository:
    irmc_url: "{{ inventory_hostname }}"
    irmc_username: "{{ irmc_user }}"
    irmc_password: "{{ irmc_password }}"
    validate_certs: "{{ validate_certificate }}"
    command: "get"
  delegate_to: localhost

# Set eLCM repository data
- name: Set eLCM repository data
  irmc_elcm_repository:
    irmc_url: "{{ inventory_hostname }}"
    irmc_username: "{{ irmc_user }}"
    irmc_password: "{{ irmc_password }}"
    validate_certs: "{{ validate_certificate }}"
    command: "set"
    server: "{{ elcm_server }}"
    catalog: "{{ elcm_catalog }}"
    use_proxy: "{{ elcm_use_proxy }}"
    proxy_url: "{{ elcm_proxy_url }}"
    proxy_port: "{{ elcm_proxy_port }}"
    proxy_user: "{{ elcm_proxy_user }}"
    proxy_password: "{{ elcm_proxy_password }}"
    wait_for_finish: true
'''

RETURN = '''
# eLCM data returned for command "get":
    repository:
        description: eLCM repository data
        returned: always
        type: dict
'''


import json
from ansible.module_utils.basic import AnsibleModule

from ansible.module_utils.irmc import irmc_redfish_get, irmc_redfish_put, get_irmc_json, \
                                      waitForSessionToFinish, elcm_check_status


# Global
result = dict()
true_false = {False: "no", True: "yes"}


def irmc_elcm_repository(module):
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

    # preliminary parameter check
    if module.params['command'] == "set":
        none_count = 0
        plist = ("server", "catalog", "use_proxy", "proxy_url", "proxy_port", "proxy_user", "proxy_password")
        for param in plist:
            if module.params[param] is None:
                none_count += 1
        if none_count == len(plist):
            result['msg'] = "Command 'set' requires at least one parameter to be set!"
            result['status'] = 10
            module.fail_json(**result)
        if (module.params['proxy_url'] is None and module.params['proxy_port'] is not None) or \
           (module.params['proxy_url'] is not None and module.params['proxy_port'] is None):
            result['msg'] = "'proxy_url' and 'proxy_port' need to be set together!"
            result['status'] = 11
            module.fail_json(**result)

    # start doing the actual work
    if module.params['command'] == "get":
        get_elcm_data(module)

    if module.params['command'] == "set":
        set_elcm_data(module)
        result['changed'] = True

    module.exit_json(**result)


def get_elcm_data(module):
    status, elcmdata, msg = irmc_redfish_get(module, "rest/v1/Oem/eLCM/Repository/Update")
    if status < 100:
        module.fail_json(msg=msg, status=status, exception=elcmdata)
    elif status not in (200, 202, 204):
        module.fail_json(msg=msg, status=status)

    result['repository'] = {}
    result['repository']['server'] = get_irmc_json(elcmdata.json(), ["Repository", "Server", "URL"])
    result['repository']['catalog'] = get_irmc_json(elcmdata.json(), ["Repository", "Server", "Catalog"])
    result['repository']['use_proxy'] = get_irmc_json(elcmdata.json(), ["Repository", "Server", "UseProxy"])
    result['repository']['proxy_url'] = get_irmc_json(elcmdata.json(), ["Repository", "Proxy", "URL"])
    result['repository']['proxy_port'] = get_irmc_json(elcmdata.json(), ["Repository", "Proxy", "Port"])
    result['repository']['proxy_user'] = get_irmc_json(elcmdata.json(), ["Repository", "Proxy", "User"])
    result['repository']['proxy_password'] = get_irmc_json(elcmdata.json(), ["Repository", "Proxy", "Password"])


def set_elcm_data(module):
    body = {'Repository': {}}
    if module.params['server'] is not None or module.params['catalog'] is not None or \
       module.params['use_proxy'] is not None:
        body['Repository']['Server'] = {}
        if module.params['server'] is not None:
            body['Repository']['Server']['URL'] = module.params['server']
        if module.params['catalog'] is not None:
            body['Repository']['Server']['Catalog'] = module.params['catalog']
        if module.params['use_proxy'] is not None:
            body['Repository']['Server']['UseProxy'] = true_false.get(module.params['use_proxy'])
    if module.params['proxy_url'] is not None or module.params['proxy_port'] is not None or \
       module.params['proxy_user'] is not None or module.params['proxy_password'] is not None:
        body['Repository']['Proxy'] = {}
        if module.params['proxy_url'] is not None:
            body['Repository']['Proxy']['URL'] = module.params['proxy_url']
        if module.params['proxy_port'] is not None:
            body['Repository']['Proxy']['Port'] = module.params['proxy_port']
        if module.params['proxy_user'] is not None:
            body['Repository']['Proxy']['User'] = module.params['proxy_user']
        if module.params['proxy_password'] is not None and module.params['proxy_password'] != "":
            body['Repository']['Proxy']['Password'] = module.params['proxy_password']

    status, elcmdata, msg = irmc_redfish_put(module, "rest/v1/Oem/eLCM/Repository/Update", json.dumps(body))
    if status < 100:
        module.fail_json(msg=msg, status=status, exception=elcmdata)
    elif status not in (200, 202, 204):
        module.fail_json(msg=msg, status=status)

    if module.params['wait_for_finish'] is True:
        # check that current session is terminated
        status, data, msg = waitForSessionToFinish(module, get_irmc_json(elcmdata.json(), ["Session", "Id"]))
        if status > 30 and status < 100:
            module.fail_json(msg=msg, status=status, exception=data)
        elif status not in (200, 202, 204):
            module.fail_json(msg=msg, log=data, status=status)


def main():
    # import pdb; pdb.set_trace()
    module_args = dict(
        irmc_url=dict(required=True, type="str"),
        irmc_username=dict(required=True, type="str"),
        irmc_password=dict(required=True, type="str", no_log=True),
        validate_certs=dict(required=False, type="bool", default=True),
        command=dict(required=False, type="str", default="get", choices=['get', 'set']),
        server=dict(required=False, type="str"),
        catalog=dict(required=False, type="str"),
        use_proxy=dict(required=False, type="bool"),
        proxy_url=dict(required=False, type="str"),
        proxy_port=dict(required=False, type="str"),
        proxy_user=dict(required=False, type="str"),
        proxy_password=dict(required=False, type="str", no_log=True),
        wait_for_finish=dict(required=False, type="bool", default=True),
    )
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    irmc_elcm_repository(module)


if __name__ == '__main__':
    main()
