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
module: irmc_cas

short_description: manage iRMC CAS settings

description:
    - Ansible module to manage iRMC CAS settings via iRMC remote scripting interface.
    - Module Version V1.2.

requirements:
    - The module needs to run locally.
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
        description: How to handle iRMC CAS data.
        required:    false
        default:     get
        choices:     ['get', 'set']
    enabled:
        description: CAS enabled.
        required:    false
    ssl_verify:
        description: Verify SSL Certificate.
        required:    false
    login_always:
        description: Always Display Login Page.
        required:    false
    server:
        description: CAS Server.
        required:    false
    port:
        description: CAS Port.
        required:    false
    login_uri:
        description: CAS Login URL.
        required:    false
    logout_uri:
        description: CAS Logout URL.
        required:    false
    validate_uri:
        description: CAS Validate URL.
        required:    false
    privilege_level:
        description: Privilege Level.
        required:    false
        choices:     ['Reserved', 'Callback', 'User', 'Operator', 'Administrator', 'OEM', 'NoAccess']
    privilege_source:
        description: Assign CAS permissions from.
        required:    false
        choices:     ['Local', 'LDAP']
    privilege_user:
        description: Configure User Accounts.
        required:    false
    privilege_bmc:
        description: Configure iRMC Settings.
        required:    false
    privilege_avr:
        description: Video Redirection Enabled.
        required:    false
    privilege_storage:
        description: Remote Storage Enable.
        required:    false

notes:
    - See http://manuals.ts.fujitsu.com/file/12563/wp-svs-irmc-remote-scripting-en.pdf
    - See https://sp.ts.fujitsu.com/dmsp/Publications/public/dp-svs-configuration-space-values-en.pdf
'''

EXAMPLES = '''
# Get CAS data
- name: Get CAS data
  irmc_cas:
    irmc_url: "{{ inventory_hostname }}"
    irmc_username: "{{ irmc_user }}"
    irmc_password: "{{ irmc_password }}"
    validate_certs: "{{ validate_certificate }}"
    command: "get"
  register: cas
  delegate_to: localhost
- name: Show iRMC CAS data
  debug:
    msg: "{{ cas.cas }}"

# Set CAS data
- name: Set CAS data
  irmc_cas:
    irmc_url: "{{ inventory_hostname }}"
    irmc_username: "{{ irmc_user }}"
    irmc_password: "{{ irmc_password }}"
    validate_certs: "{{ validate_certificate }}"
    command: "set"
    cas_user: "username"
    cas_password: "password"
  delegate_to: localhost
'''

RETURN = '''
# CAS data returned by command "get":
    enabled:
        description: CAS enabled
        returned: always
        type: bool
        sample: False
    ssl_verify:
        description: verify SSL Certificate
        returned: always
        type: bool
        sample: True
    login_always:
        description: always Display Login Page
        returned: always
        type: bool
        sample: True
    server:
        description: CAS server
        returned: always
        type: string
        sample: cas_server.local
    port:
        description: CAS port
        returned: always
        type: int
        sample: 3170
    login_uri:
        description: CAS Login URL
        returned: always
        type: string
        sample: /cas/login
    logout_uri:
        description: CAS Logout URL
        returned: always
        type: string
        sample: /cas/logout
    validate_uri:
        description: CAS Validate URL
        returned: always
        type: string
        sample: /cas/validate
    privilege_level:
        description: privilege Level
        returned: always
        type: string
        sample: Operator
    privilege_source:
        description: assign CAS permissions from
        returned: always
        type: string
        sample: Local
    privilege_user:
        description: configure User Accounts
        returned: always
        type: bool
        sample: False
    privilege_bmc:
        description: configure iRMC Settings
        returned: always
        type: bool
        sample: False
    privilege_avr:
        description: Video Redirection Enabled
        returned: always
        type: bool
        sample: False
    privilege_storage:
        description: Remote Storage Enable
        returned: always
        type: bool
        sample: False

# For command "set":
    Default return values:
'''


from ansible.module_utils.basic import AnsibleModule

from ansible.module_utils.irmc_scci_utils import get_scciresultlist, irmc_scci_post, setup_datadict, \
                                                 setup_commandlist


cas_priv = {"0": "Reserved", "1": "Callback", "2": "User", "3": "Operator", "4": "Administrator", "5": "OEM", "15": "NoAccess"}
cas_priv_src = {"0": "Local", "1": "LDAP"}
cas_login = {"0": "Automatic", "1": "Login page"}
true_false = {"0": "False", "1": "True"}
param_scci_map = [
    # Param, SCCI Name, SCCI Code, index, value dict
    ["enabled", "ConfBmcCasEnable", 0x1941, 0, true_false],                             # iRMC: CAS Enabled
    ["ssl_verify", "ConfBmcCasVerifyServerCert", 0x1948, 0, true_false],                # iRMC: Verify SSL Certificate
    ["login_always", "ConfBmcCasAlwaysDisplayLogin", 0x194F, 0, cas_login],             # iRMC: Always Display Login Page
    ["server", "ConfBmcCasServer", 0x1942, 0, None],                                    # iRMC: CAS Server
    ["port", "ConfBmcCasPort", 0x1943, 0, None],                                        # iRMC: CAS Port
    ["login_uri", "ConfBmcCasLoginUri", 0x1944, 0, None],                               # iRMC: CAS Login URL
    ["logout_uri", "ConfBmcCasLogoutUri", 0x1945, 0, None],                             # iRMC: CAS Logout URL
    ["validate_uri", "ConfBmcCasValidateUri", 0x1946, 0, None],                         # iRMC: CAS Validate URL
    ["privilege_level", "ConfBmcCasAssignConfiguredPermissions", 0x194E, 0, cas_priv], # iRMC: Privilege Level
    ["privilege_source", "ConfBmcCasNetworkPrivilege", 0x1949, 0, cas_priv_src],        # iRMC: Assign permissions from
    ["privilege_user", "ConfBmcCasConfigureUsers", 0x194B, 0, true_false],              # iRMC: Configure User Accounts
    ["privilege_bmc", "ConfBmcCasPermissionConfigureBmc", 0x194A, 0, true_false],       # iRMC: Configure iRMC Settings
    ["privilege_avr", "ConfBmcCasPermissionAvrEnabled", 0x194C, 0, true_false],         # iRMC: Video Redirection Enabled
    ["privilege_storage", "ConfBmcCasRemoteStorageEnabled", 0x194D, 0, true_false],     # iRMC: Remote Storage Enable
]


def irmc_cas(module):
    result = dict(
        changed=False,
        status=0
    )

    if module.check_mode:
        result['msg'] = "module was not run"
        module.exit_json(**result)

    casdata, setparam_count = setup_datadict(module)

    # preliminary parameter check
    if module.params['command'] == "set" and setparam_count == 0:
        result['msg'] = "Command 'set' requires at least one parameter to be set!"
        result['status'] = 10
        module.fail_json(**result)

    if module.params['command'] == "set":
        body = setup_commandlist(casdata, "SET", param_scci_map)
    else:
        body = setup_commandlist(casdata, "GET", param_scci_map)

    # send command list to scripting interface
    status, data, msg = irmc_scci_post(module, body)
    if status < 100:
        module.fail_json(msg=msg, status=status, exception=data)
    elif status not in (200, 202, 204):
        module.fail_json(msg=msg, status=status)

    # evaluate results list
    casdata, scciresult, sccicontext = get_scciresultlist(data.content, casdata, param_scci_map)
    if scciresult != 0:
        module.fail_json(msg=sccicontext, status=scciresult)

    if module.params['command'] == "get":
        result['cas'] = setup_resultdata(casdata)
    else:
        result['changed'] = True

    module.exit_json(**result)


def setup_resultdata(data):
    data = {
        'enabled': true_false.get(data['enabled']),
        'ssl_verify': true_false.get(data['ssl_verify']),
        'login_always': cas_login.get(data['login_always']),
        'server': data['server'],
        'port': data['port'],
        'login_uri': data['login_uri'],
        'logout_uri': data['logout_uri'],
        'validate_uri': data['validate_uri'],
        'privilege_level': cas_priv.get(data['privilege_level']),
        'privilege_source': cas_priv_src.get(data['privilege_source']),
        'privilege_user': true_false.get(data['privilege_user']),
        'privilege_bmc': true_false.get(data['privilege_bmc']),
        'privilege_avr': true_false.get(data['privilege_avr']),
        'privilege_storage': true_false.get(data['privilege_storage']),
    }
    return data


def main():
    # import pdb; pdb.set_trace()
    module_args = dict(
        irmc_url=dict(required=True, type="str"),
        irmc_username=dict(required=True, type="str"),
        irmc_password=dict(required=True, type="str", no_log=True),
        validate_certs=dict(required=False, type="bool", default=True),
        command=dict(required=False, type="str", default="get", choices=['get', 'set']),
        enabled=dict(required=False, type="bool"),
        ssl_verify=dict(required=False, type="bool"),
        login_always=dict(required=False, type="str", choices=['Automatic', 'Login page']),
        server=dict(required=False, type="str"),
        port=dict(required=False, type="int"),
        login_uri=dict(required=False, type="str"),
        logout_uri=dict(required=False, type="str"),
        validate_uri=dict(required=False, type="str"),
        privilege_level=dict(required=False, type="str", choices=['Reserved', 'Callback', 'User', 'Operator', 'Administrator', 'OEM', 'NoAccess']),
        privilege_source=dict(required=False, type="str", choices=['Local', 'LDAP']),
        privilege_user=dict(required=False, type="bool"),
        privilege_bmc=dict(required=False, type="bool"),
        privilege_avr=dict(required=False, type="bool"),
        privilege_storage=dict(required=False, type="bool"),
    )
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    irmc_cas(module)


if __name__ == '__main__':
    main()
