#!/usr/bin/python

# FUJITSU Limited
# Copyright (C) FUJITSU Limited 2018
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
module: irmc_ldap

short_description: manage iRMC LDAP settings

description:
    - Ansible module to manage iRMC LDAP settings via iRMC remote scripting interface.
    - Module Version V1.0.1.

requirements:
    - The module needs to run locally.
    - "python >= 2.6"

version_added: "2.4"

author:
    - FujitsuPrimergy (@FujitsuPrimergy)

options:
    irmc_url:
        description: IP address of the iRMC to be requested for data
        required:    true
    irmc_username:
        description: iRMC user for basic authentication
        required:    true
    irmc_password:
        description: password for iRMC user for basic authentication
        required:    true
    validate_certs:
        description: evaluate SSL certificate (set to false for self-signed certificate)
        required:    false
        default:     true
    command:
        description: get or set iRMC LDAP data
        required:    false
        default:     get
        choices:     ['get', 'set']
    enabled:
        description: LDAP enabled
        required:    false
    ssl_enabled:
        description: LDAP SSL enabled
        required:    false
    local_login_disabled:
        description: local login disabled
        required:    false
    always_use_ssl:
        description: always use SSL login
        required:    false
    directory_type:
        description: directory server type
        required:    false
        choices:     ['MS Active Directory', 'Novell eDirector', 'Sun ePlanet', 'OpenLDAP', 'OpenDS / OpenDJ']
    auth_type:
        description: authorization type
        required:    false
        choices:     ['Automatic', 'Settings stored on iRMC', 'Settings stored on LDAP']
    primary_server:
        description: primary LDAP server
        required:    false
    primary_port:
        description: non-SL port of primary LDAP server
        required:    false
    primary_ssl_port:
        description: SSL port of primary LDAP server
        required:    false
    backup_server:
        description: backup LDAP server
        required:    false
    backup_port:
        description: non-SL port of backup LDAP server
        required:    false
    backup_ssl_port:
        description: SSL port of backup LDAP server
        required:    false
    domain_name:
        description: domain name
        required:    false
    department_name:
        description: department name
        required:    false
    base_dn:
        description: base DN
        required:    false
    group_dn:
        description: groups directory as sub-tree from base DN
        required:    false
    user_search_context:
        description: user search context
        required:    false
    ldap_user:
        description: LDAP user name
        required:    false
    ldap_password:
        description: LDAP user password
        required:    false
    user_dn:
        description: principal user DN
        required:    false
    append_base_to_user_dn:
        description: append base DN to principal user DN
        required:    false
    enhanced_user_login:
        description: enhanced user login
        required:    false
    user_login_filter:
        description: user login search filter
        required:    false
    alert_email_enabled:
        description: LDAP email alert enabled
        required:    false
    alert_table_refresh:
        description: LDAP alert table refresh in hours (0 = never)
        required:    false

notes:
    - See http://manuals.ts.fujitsu.com/file/12563/wp-svs-irmc-remote-scripting-en.pdf
    - See https://sp.ts.fujitsu.com/dmsp/Publications/public/dp-svs-configuration-space-values-en.pdf
'''

EXAMPLES = '''
# Get LDAP data
- name: Get LDAP data
  irmc_ldap:
    irmc_url: "{{ inventory_hostname }}"
    irmc_username: "{{ irmc_user }}"
    irmc_password: "{{ irmc_password }}"
    validate_certs: "{{ validate_certificate }}"
    command: "get"
  register: ldap
  delegate_to: localhost
- name: Show iRMC LDAP data
  debug:
    msg: "{{ ldap.ldap }}"

# Set LDAP data
- name: Set LDAP data
  irmc_ldap:
    irmc_url: "{{ inventory_hostname }}"
    irmc_username: "{{ irmc_user }}"
    irmc_password: "{{ irmc_password }}"
    validate_certs: "{{ validate_certificate }}"
    command: "set"
    ldap_user: "username"
    ldap_password: "password"
  delegate_to: localhost
'''

RETURN = '''
ldap:
    description: LDAP information
    returned: always
    type: dict
'''


# pylint: disable=wrong-import-position
from ansible.module_utils.basic import AnsibleModule

from ansible.module_utils.irmc_scci_utils import get_scciresultlist, irmc_scci_post, setup_datadict, \
                                                 get_key_for_value, add_scci_command, \
                                                 scci_body_start, scci_body_end


ldap_dir = {"0": "MS Active Directory", "1": "Novell eDirectory", "2": "Sun ePlanet", "3": "OpenLDAP",
            "4": "OpenDS / OpenDJ"}
ldap_auth = {"0": "Automatic", "1": "Settings stored on iRMC", "2": "Settings stored on LDAP"}
true_false = {"0": "False", "1": "True"}
param_scci_map = [
    # Param, SCCI Name, SCCI Code, index, value dict
    ["enabled", "ConfBMCLDAPEnable", 0x1971, 0, true_false],                            # iRMC: LDAP Enabled
    ["ssl_enabled", "ConfBMCLDAPSSLEnable", 0x1972, 0, true_false],                     # iRMC: LDPA SSL Enabled
    ["local_login_disabled", "ConfBMCLDAPLocalLoginDisabled", 0x197B, 0, true_false],   # iRMC: Disable Local Login
    ["always_use_ssl", "ConfBMCLDAPBrowserLoginDisabled", 0x197C, 0, true_false],       # iRMC: always use SSL Login
    ["directory_type", "ConfBMCLDAPDirectoryType", 0x1974, 0, ldap_dir],                # iRMC: Directory Server Type
    ["auth_type", "ConfBMCLdapPreferedMailServer", 0x1990, 0, ldap_auth],               # iRMC: Authorization Type
    ["primary_server", "ConfBMCLDAPServerName", 0x1976, 0, None],                       # iRMC: Primary LDAP Server
    ["primary_port", "ConfBmcLDAPNonSecurePort", 0x1996, 0, None],                      # iRMC: Primary LDAP Port
    ["primary_ssl_port", "ConfBmcLDAPSecurePort", 0x1997, 0, None],                     # iRMC: Primary LDAP SSL Port
    ["backup_server", "ConfBMCLDAPServerName", 0x1976, 1, None],                        # iRMC: Backup LDAP Server
    ["backup_port", "ConfBmcLDAPNonSecurePort", 0x1996, 1, None],                       # iRMC: Backup LDAP Port
    ["backup_ssl_port", "ConfBmcLDAPSecurePort", 0x1997, 1, None],                      # iRMC: Backup LDAP SSL Port
    ["domain_name", "ConfBMCLDAPDomainName", 0x1977, 0, None],                          # iRMC: ???
    ["department_name", "ConfBMCLDAPDepartmentName", 0x1978, 0, None],                  # iRMC: Department Name
    ["base_dn", "ConfBMCLdapBaseDN", 0x197D, 0, None],                                  # iRMC: Base DN
    ["group_dn", "ConfLdapGroupDN", 0x1992, 0, None],                                   # iRMC: Groups directory
    ["user_search_context", "ConfLdapUserBase", 0x1993, 0, None],                       # iRMC: User Search context
    ["ldap_user", "ConfBMCLDAPgroupsUserName", 0x1979, 0, None],                        # iRMC: ????
    ["ldap_password", "ConfBMCLDAPgroupsUserPasswd", 0x197A, 0, None],                  # iRMC: LDAP Auth Password
    ["user_dn", "ConfBMCLDAPLdapUserDN", 0x197E, 0, None],                              # iRMC: Principal User DN
    ["append_base_to_user_dn", "ConfBMCLdapAppendBaseDNtoUserDN", 0x197F, 0, true_false],  # iRMC: Append Base DN
    ["enhanced_user_login", "ConfLDAPUseUserFilter", 0x1995, 0, true_false],            # iRMC: Enhanced User Login
    ["user_login_filter", "ConfLdapUserFilter", 0x1994, 0, None],                       # iRMC: User Login Search filter
    ["alert_email_enabled", "ConfBMCLDAPAlertEnable", 0x1973, 0, true_false],                 # iRMC: Email Alert Enable
    ["alert_table_refresh", "ConfBMCLdapAlertRefreshTime", 0x1991, 0, None],             # iRMC: Alert Table Refresh
]


def irmc_ldap(module):
    result = dict(
        changed=False,
        status=0
    )

    if module.check_mode:
        result['msg'] = "module was not run"
        module.exit_json(**result)

    ldapdata, setparam_count = setup_datadict(module)

    # preliminary parameter check
    if module.params['command'] == "set" and setparam_count == 0:
        result['msg'] = "Command 'set' requires at least one parameter to be set!"
        module.fail_json(**result)

    if module.params['command'] == "set":
        body = setup_commandlist(ldapdata, "SET", param_scci_map)
    else:
        body = setup_commandlist(ldapdata, "GET", param_scci_map)

    # send command list to scripting interface
    status, data, msg = irmc_scci_post(module, body)
    if status < 100:
        module.fail_json(msg=msg, exception=data)
    elif status != 200 and status != 204:
        module.fail_json(msg=msg, status=status)

    # evaluate results list
    ldapdata, scciresult, sccicontext = get_scciresultlist(data.content, ldapdata, param_scci_map)
    if scciresult != 0:
        result['msg'] = sccicontext
        module.fail_json(**result)

    if module.params['command'] == "get":
        result['ldap'] = setup_resultdict(ldapdata)
    else:
        result['changed'] = True

    module.exit_json(**result)


def setup_commandlist(cmdlist, ctype, scci_map):
    body = scci_body_start
    data = ""
    for elem in scci_map:
        if elem[4] is not None and cmdlist[elem[0]] is not None:
            data = get_key_for_value(cmdlist[elem[0]], elem[4])
        else:
            data = cmdlist[elem[0]]
        body += add_scci_command(ctype, scci_map, elem[1], elem[3], data)
    body += scci_body_end
    return body


def setup_resultdict(data):
    data = {
        'enabled': true_false.get(data['enabled']),
        'ssl_enabled': true_false.get(data['ssl_enabled']),
        'local_login_disabled': true_false.get(data['local_login_disabled']),
        'always_use_ssl': true_false.get(data['always_use_ssl']),
        'directory_type': ldap_dir.get(data['directory_type']),
        'auth_type': ldap_auth.get(data['auth_type']),
        'primary_server': data['primary_server'],
        'primary_port': data['primary_port'],
        'primary_ssl_port': data['primary_ssl_port'],
        'backup_server': data['backup_server'],
        'backup_port': data['backup_port'],
        'backup_ssl_port': data['backup_ssl_port'],
        'domain_name': data['domain_name'],
        'department_name': data['department_name'],
        'base_dn': data['base_dn'],
        'group_dn': data['group_dn'],
        'user_search_context': data['user_search_context'],
        'ldap_user': data['ldap_user'],
        'ldap_password': data['ldap_password'],
        'user_dn': data['user_dn'],
        'append_base_to_user_dn': true_false.get(data['append_base_to_user_dn']),
        'enhanced_user_login': true_false.get(data['enhanced_user_login']),
        'user_login_filter': data['user_login_filter'],
        'alert_email_enabled': true_false.get(data['alert_email_enabled']),
        'alert_table_refresh': data['alert_table_refresh'],
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
        ssl_enabled=dict(required=False, type="bool"),
        local_login_disabled=dict(required=False, type="bool"),
        always_use_ssl=dict(required=False, type="bool"),
        directory_type=dict(required=False, type="str",
                            choices=["MS Active Directory", "Novell eDirectory", "Sun ePlanet", "OpenLDAP",
                                     "OpenDS / OpenDJ"]),
        auth_type=dict(required=False, type="str",
                       choices=["Automatic", "Settings stored on iRMC", "Settings stored on LDA"]),
        primary_server=dict(required=False, type="str"),
        primary_port=dict(required=False, type="int"),
        primary_ssl_port=dict(required=False, type="int"),
        backup_server=dict(required=False, type="str"),
        backup_port=dict(required=False, type="int"),
        backup_ssl_port=dict(required=False, type="int"),
        domain_name=dict(required=False, type="str"),
        department_name=dict(required=False, type="str"),
        base_dn=dict(required=False, type="str"),
        group_dn=dict(required=False, type="str"),
        user_search_context=dict(required=False, type="str"),
        ldap_user=dict(required=False, type="str"),
        ldap_password=dict(required=False, type="str", no_log=True),
        user_dn=dict(required=False, type="str"),
        append_base_to_user_dn=dict(required=False, type="bool"),
        enhanced_user_login=dict(required=False, type="bool"),
        user_login_filter=dict(required=False, type="str"),
        alert_email_enabled=dict(required=False, type="bool"),
        alert_table_refresh=dict(required=False, type="int"),
    )
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    irmc_ldap(module)


if __name__ == '__main__':
    main()
