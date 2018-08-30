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
module: irmc_user

short_description: manage iRMC user accounts

description:
    - Ansible module to manage iRMC user accounts via iRMC remote scripting interface.
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
        description: user management to be executed
        required:    false
        default:     get
        choices:     ['get', 'create', 'change', 'delete']
    name:
        description: user account name
        required:    true
    password:
        description: user account password
        required:    false
    description:
        description: user account desciption
        required:    false
    enabled:
        description: user account enabled
        required:    false
    lan_privilege:
        description: IPMI LAN channel privilege
        required:    false
        choices:     ['Reserved', 'Callback', 'User', 'Operator', 'Administrator', 'OEM', 'NoAccess']
    serial_privilege:
        description: IPMI serial channel privilege
        required:    false
        choices:     ['Reserved', 'Callback', 'User', 'Operator', 'Administrator', 'OEM', 'NoAccess']
    config_user_enabled:
        description: user may configure user accounts
        required:    false
    config_bmc_enabled:
        description: user may configure iRMC settings
        required:    false
    avr_enabled:
        description: user may use Advanved Video Redirection (AVR)
        required:    false
    storage_enabled:
        description: user may use Remote Storage
        required:    false
    redfish_enabled:
        description: user may use iRMC Redfish interface
        required:    false
    redfish_role:
        description: user account Redfish role
        required:    false
        choices:     ['NoAccess', 'Operator', 'Administrator', 'ReadOnly']
    shell:
        description: user text access type
        required:    false
        choices:     ['SMASH CLP', 'CLI', 'Remote Manager', 'IPMI basic mode', 'IPMI terminal mode', 'None']
    snmpv3_enabled:
        description: user may use SNMPv3
        required:    false
    snmpv3_access:
        description: user account SNMPV3 access privilege
        required:    false
        choices:     ['ReadOnly', 'ReadWrite', 'Other']
    snmpv3_auth:
        description: user account SNMPv3 authentication
        required:    false
        choices:     ['Undefined', 'SHA', 'MD5', 'None']
    snmpv3_privacy:
        description: user account SNMPv3 privacy type
        required:    false
        choices:     ['Undefined', 'AES', 'DES', 'None']
    ssh_public_key:
        description: user account SSH public key
        required:    false
    ssh_certificate:
        description: user account SSH certificate
        required:    false
    email_enabled:
        description: alert email enabled
        required:    false
    email_encrypted:
        description: alert email is encrypted
        required:    false
    email_type:
        description: alert email format
        required:    false
        choices:     ['Standard', 'ITS-Format', 'REMCS', 'Fixed Subject', 'SMS']
    email_server:
        description: preferred mail server for alert email
        required:    false
        choices:     ['Automatic', 'Primary', 'Secondary']
    email_address:
        description: alert email address
        required:    false
    alert_fans:
        description: define alert level for fan sensors
        required:    false
        choices:     ['None', 'Critical', 'Warning', 'All']
    alert_temperatures:
        description: define alert level for temperature sensors
        required:    false
        choices:     ['None', 'Critical', 'Warning', 'All']
    alert_hwerrors:
        description: define alert level for critical hardware errors
        required:    false
        choices:     ['None', 'Critical', 'Warning', 'All']
    alert_syshang:
        description: define alert level for system hang
        required:    false
        choices:     ['None', 'Critical', 'Warning', 'All']
    alert_posterrors:
        description: define alert level for POST errors
        required:    false
        choices:     ['None', 'Critical', 'Warning', 'All']
    alert_security:
        description: define alert level for security
        required:    false
        choices:     ['None', 'Critical', 'Warning', 'All']
    alert_sysstatus:
        description: define alert level for system status
        required:    false
        choices:     ['None', 'Critical', 'Warning', 'All']
    alert_hderrors:
        description: define alert level for disk drivers & controllers
        required:    false
        choices:     ['None', 'Critical', 'Warning', 'All']
    alert_network:
        description: define alert level for network interface
        required:    false
        choices:     ['None', 'Critical', 'Warning', 'All']
    alert_remote:
        description: define alert level for remote management
        required:    false
        choices:     ['None', 'Critical', 'Warning', 'All']
    alert_power:
        description: define alert level for system power
        required:    false
        choices:     ['None', 'Critical', 'Warning', 'All']
    alert_memory:
        description: define alert level for memory
        required:    false
        choices:     ['None', 'Critical', 'Warning', 'All']
    alert_others:
        description: define alert level for other
        required:    false
        choices:     ['None', 'Critical', 'Warning', 'All']

notes:
    - See http://manuals.ts.fujitsu.com/file/12563/wp-svs-irmc-remote-scripting-en.pdf
    - See https://sp.ts.fujitsu.com/dmsp/Publications/public/dp-svs-configuration-space-values-en.pdf
'''

EXAMPLES = '''
# Create new user account
- name: "Create new user account"
  irmc_user:
    irmc_url: "{{ inventory_hostname }}"
    irmc_username: "{{ irmc_user }}"
    irmc_password: "{{ irmc_password }}"
    validate_certs: "{{ validate_certificate }}"
    command: "create"
    name: "ansibleuser"
    password: "password"
  delegate_to: localhost

# Get user account data
- name: Get user account data
  irmc_user:
    irmc_url: "{{ inventory_hostname }}"
    irmc_username: "{{ irmc_user }}"
    irmc_password: "{{ irmc_password }}"
    validate_certs: "{{ validate_certificate }}"
    command: "get"
    name: "ansibleuser"
  register: user
  delegate_to: localhost
- name: Show iRMC user details
  debug:
    msg: "{{ user.user }}"

# Change user account data
- name: Change user account data
  irmc_user:
    irmc_url: "{{ inventory_hostname }}"
    irmc_username: "{{ irmc_user }}"
    irmc_password: "{{ irmc_password }}"
    validate_certs: "{{ validate_certificate }}"
    command: "change"
    name: "ansibleuser"
    description: "ansible user description"
  delegate_to: localhost

# Delete user account
- name: "Delete user account"
  irmc_user:
    irmc_url: "{{ inventory_hostname }}"
    irmc_username: "{{ irmc_user }}"
    irmc_password: "{{ irmc_password }}"
    validate_certs: "{{ validate_certificate }}"
    command: "delete"
    name: "ansibleuser"
  delegate_to: localhost
'''

RETURN = '''
user:
    description: user account information
    returned: always
    type: dict
'''


# pylint: disable=wrong-import-position
from ansible.module_utils.basic import AnsibleModule

from ansible.module_utils.irmc_scci_utils import get_scciresult, get_scciresultlist, irmc_scci_post, \
                                                 setup_datadict, get_key_for_value, add_scci_command, \
                                                 scci_body_start, scci_body_end


channel_privilege = {"0": "Reserved", "1": "Callback", "2": "User", "3": "Operator", "4": "Administrator",
                     "5": "OEM", "15": "No Access"}
redfish_role = {"3": "ReadOnly", "1": "Operator", "2": "Administrator", "0": "NoAccess"}
shell_type = {"0": "SMASH CLP", "1": "CLI", "2": "Remote Manager", "3": "IPMI basic mode", "4": "IPMI terminal mode",
              "5": "No shell", "6": "No shell"}
snmpv3_access = {"0": "ReadOnly", "1": "ReadWrite", "2": "Other"}
snmpv3_auth = {"0": "Undefined", "1": "SHA", "2": "MD5", "3": "None"}
snmpv3_priv = {"0": "Undefined", "1": "AES", "2": "DES", "3": "None"}
email_type = {"0": "Standard", "1": "ITS-Format", "2": "REMCS", "3": "Fixed Subject", "4": "SMS"}
email_server = {"0": "Automatic", "1": "Primary", "2": "Secondary"}
alerts = {"0": "None", "1": "Critical", "2": "Warning", "3": "All"}
true_false = {"0": "False", "1": "True"}
param_scci_map = [
    # Param, SCCI Name, SCCI Code, value dict
    ["name", "ConfBMCAcctUserName", 0x1451, None],                                     # iRMC: Name
    ["password", "ConfBMCAcctUserPassword", 0x1452, None],                             # iRMC: Password
    ["description", "ConfBMCAcctUserDescription", 0x1455, None],                       # iRMC: Desciption
    ["enabled", "ConfBMCAcctUserEnable", 0x1457, true_false],                          # iRMC: IPMI User Enabled
    ["lan_privilege", "ConfBMCAcctUserGroup", 0x1454, channel_privilege],              # iRMC: LAN Channel Privilege
    ["serial_privilege", "ConfBMCAcctUserGroupSerial", 0x145B, channel_privilege],     # iRMC: Serial Channel Privilege
    ["config_user_enabled", "ConfBMCAcctUserEnableConfigUser", 0x1453, true_false],    # iRMC: Configure User Accounts
    ["config_bmc_enabled", "ConfBMCAcctUserEnableConfigBMC", 0x145D, true_false],      # iRMC: Configure iRMC Settings
    ["avr_enabled", "ConfBMCAcctUserEnableUseAVR", 0x145E, true_false],                # iRMC: Video Redirection Enabled
    ["storage_enabled", "ConfBMCAcctUserEnableUseRStorage", 0x145F, true_false],       # iRMC: Remote Storage Enabled
    ["redfish_enabled", "ConfBMCAcctUserRedfishEnabled", 0x1D80, true_false],          # iRMC: Redfish Enabled
    ["redfish_role", "ConfBMCAcctUserRedfishRoleId", 0x1D81, redfish_role],            # iRMC: Redfish Role
    # ["redfish_lock_status", "ConfBMCRedfishUserLockStatus", 0x1D82, None],           # iRMC: ---
    ["shell", "ConfBMCAcctUserShell", 0x1459, shell_type],                             # iRMC: User Shell (Text Access)
    ["snmpv3_enabled", "ConfBMCSnmpV3UserServiceEnabled", 0x1415, true_false],         # iRMC: SNMPv3 Enabled
    ["snmpv3_access", "ConfBMCSnmpV3UserAccessType", 0x1418, snmpv3_access],           # iRMC: Access Privilege
    ["snmpv3_auth", "ConfBMCSnmpV3UserAuthType", 0x1416, snmpv3_auth],                 # iRMC: Authentication
    ["snmpv3_privacy", "ConfBMCSnmpV3UserPrivType", 0x1417, snmpv3_priv],              # iRMC: Privacy
    ["ssh_public_key", "ConfBMCAcctUserSshPublicKey", 0x19A1, None],                   # iRMC: SSHv2 public key
    ["ssh_certificate", "ConfBMCAcctUserCertitificate", 0x19A2, None],                 # iRMC: S/MIME certificate file
    ["email_enabled", "ConfBMCAcctUserEnableEmailPaging", 0x145A, true_false],         # iRMC: Email Enabled
    ["email_encrypted", "ConfBMCAcctUserSendEmailAlertsEncrypted", 0x1467, true_false],  # iRMC: Encrypted
    ["email_type", "ConfAlarmMailType", 0x1288, email_type],                           # iRMC: Mail Format
    ["email_server", "ConfBMCAcctUserPreferedMailServer", 0x145C, email_server],       # iRMC: Preferred Mail Server
    ["email_address", "ConfBMCAcctUserEmailAddress", 0x1458, None],                    # iRMC: Email Address
    ["alert_fans", "ConfBMCPagingSeverityFans", 0x1901, alerts],                       # iRMC: Fan Sensors
    ["alert_temperatures", "ConfBMCPagingSeverityTemperature", 0x1900, alerts],        # iRMC: Temperature Sensors
    ["alert_hwerrors", "ConfBMCPagingSeverityHWErrors", 0x1903, alerts],               # iRMC: Critical Hardware Errors
    ["alert_syshang", "ConfBMCPagingSeveritySysHang", 0x1904, alerts],                 # iRMC: System Hang
    ["alert_posterrors", "ConfBMCPagingSeverityPOSTErrors", 0x1905, alerts],           # iRMC: POST Errors
    ["alert_security", "ConfBMCPagingSeveritySecurity", 0x1906, alerts],               # iRMC: Security
    ["alert_sysstatus", "ConfBMCPagingSeveritySysStatus", 0x1907, alerts],             # iRMC: System Status
    ["alert_hderrors", "ConfBMCPagingSeverityHDErrors", 0x1908, alerts],               # iRMC: Disk Driver & Controller
    ["alert_network", "ConfBMCPagingSeverityNetwork", 0x1909, alerts],                 # iRMC: Network Interface
    ["alert_remote", "ConfBMCPagingSeverityRemote", 0x190A, alerts],                   # iRMC: Remote Management
    ["alert_power", "ConfBMCPagingSeverityPower", 0x190B, alerts],                     # iRMC: System Power
    ["alert_memory", "ConfBMCPagingSeverityMemory", 0x1902, alerts],                   # iRMC: Memory
    ["alert_others", "ConfBMCPagingSeverityOthers", 0x193F, alerts],                   # iRMC: Other
]


def irmc_user(module):        # pylint: disable=too-many-branches,too-many-statements
    result = dict(
        changed=False,
        status=0
    )

    if module.check_mode:
        result['msg'] = "module was not run"
        module.exit_json(**result)

    userdata, setparam_count = setup_datadict(module)

    # preliminary parameter checks
    if module.params['command'] == "change":
        if setparam_count <= 1:
            result['msg'] = "Command 'change' requires at least one parameter to be changed!"
            module.fail_json(**result)
    if module.params['command'] == "create":
        if module.params['password'] is None:
            result['msg'] = "Command 'create' requires at least 'password' parameter to be set!"
            module.fail_json(**result)
    if module.params['description'] is not None and len(module.params['description']) > 32:
        result['msg'] = "Description can only be 32 characters long!"
        module.fail_json(**result)

    # determine user ID (free or otherwise)
    usernumber = newuser = 0
    userdata['id'] = None
    while True:
        body = scci_body_start + add_scci_command("GET", param_scci_map, "ConfBMCAcctUserName", usernumber, "") + \
               scci_body_end
        status, data, msg = irmc_scci_post(module, body)
        if status < 100:
            module.fail_json(msg=msg, exception=data)
        elif status != 200 and status != 204:
            module.fail_json(msg=msg, status=status)

        username, sccistatus, sccicontext = get_scciresult(data.content, 0x1451)
        if (sccistatus != 0 or username == "" or username is None) and newuser == 0:
            newuser = usernumber

        if username == module.params['name']:
            userdata['id'] = usernumber
            break

        usernumber += 1
        if usernumber >= 15:
            break

    # more parameter checks
    if module.params['command'] == "create":
        if userdata['id'] is not None:
            result['skipped'] = True
            result['msg'] = "User '{0}' already exists.".format(module.params['name'])
            module.exit_json(**result)
        else:
            userdata['id'] = newuser
    else:
        if userdata['id'] is None:
            if module.params['command'] == "delete":
                result['skipped'] = True
                result['msg'] = "User '{0}' does not exist.".format(module.params['name'])
                module.exit_json(**result)
            else:
                result['msg'] = "Requested user '{0}' could not be found.".format(module.params['name'])
                module.fail_json(**result)

    # set up command list
    if module.params['command'] == "get":
        body = setup_commandlist(userdata, "GET", param_scci_map, userdata['id'])
    elif module.params['command'] == "change":
        body = setup_commandlist(userdata, "SET", param_scci_map, userdata['id'])
    elif module.params['command'] == "create":
        userdata = set_default(userdata)
        body = setup_commandlist(userdata, "CREATE", param_scci_map, userdata['id'])
    elif module.params['command'] == "delete":
        body = scci_body_start
        body += add_scci_command("DELETE", param_scci_map, "ConfBMCAcctUserName", userdata['id'], "")
        body += add_scci_command("DELETE", param_scci_map, "ConfBMCAcctUserDescription", userdata['id'], "")
        body += scci_body_end

    # send command list to scripting interface
    status, data, msg = irmc_scci_post(module, body)
    if status < 100:
        module.fail_json(msg=msg, exception=data)
    elif status != 200 and status != 204:
        module.fail_json(msg=msg, status=status)

    # evalaute result list
    userdata, scciresult, sccicontext = get_scciresultlist(data.content, userdata, param_scci_map)
    if scciresult != 0:
        result['msg'] = sccicontext
        module.fail_json(**result)

    userdata['name'] = module.params['name']
    if module.params['command'] == "get":
        result['user'] = setup_resultdata(userdata)
    else:
        result['changed'] = True

    module.exit_json(**result)


def setup_commandlist(cmdlist, ctype, scci_map, user_id):
    body = scci_body_start
    data = ""
    for elem in scci_map:
        if elem[3] is not None and cmdlist[elem[0]] is not None:
            data = get_key_for_value(cmdlist[elem[0]], elem[3])
        else:
            data = cmdlist[elem[0]]
        body += add_scci_command(ctype, scci_map, elem[1], user_id, data)
    body += scci_body_end
    return body


def set_default(data):
    data['description'] = "User {0} Description".format(format(data['id'], '02d'))
    data['enabled'] = "True"
    data['lan_privilege'] = "User"
    data['serial_privilege'] = "User"
    data['email_address'] = "User{0}@domain.com".format(format(data['id'], '02d'))
    return data


def setup_resultdata(data):
    result = {
        'name': data['name'],
        'id': data['id'],
        # 'password': data['password'],
        'description': data['description'],
        'enabled': true_false.get(data['enabled']),
        'lan_privilege': channel_privilege.get(data['lan_privilege']),
        'serial_privilege': channel_privilege.get(data['serial_privilege']),
        'config_user_enabled': true_false.get(data['config_user_enabled']),
        'config_bmc_enabled': true_false.get(data['config_bmc_enabled']),
        'avr_enabled': true_false.get(data['avr_enabled']),
        'storage_enabled': true_false.get(data['storage_enabled']),
        'redfish_enabled': true_false.get(data['redfish_enabled']),
        'redfish_role': redfish_role.get(data['redfish_role']),
        # 'redfish_lock_state': data['redfish_lock_state'],
        'shell': shell_type.get(data['shell']),
        'snmpv3_enabled': true_false.get(data['snmpv3_enabled']),
        'snmpv3_access': snmpv3_access.get(data['snmpv3_access']),
        'snmpv3_auth': snmpv3_auth.get(data['snmpv3_auth']),
        'snmpv3_privacy': snmpv3_priv.get(data['snmpv3_privacy']),
        'ssh_public_key': data['ssh_public_key'],
        'ssh_certificate': data['ssh_certificate'],
        'email_enabled': true_false.get(data['email_enabled']),
        'email_encrypted': true_false.get(data['email_encrypted']),
        'email_type': email_type.get(data['email_type']),
        'email_server': email_server.get(data['email_server']),
        'email_address': data['email_address'],
        'alert_fans': alerts.get(data['alert_fans']),
        'alert_temperatures': alerts.get(data['alert_temperatures']),
        'alert_hwerrors': alerts.get(data['alert_hwerrors']),
        'alert_syshang': alerts.get(data['alert_syshang']),
        'alert_posterrors': alerts.get(data['alert_posterrors']),
        'alert_security': alerts.get(data['alert_security']),
        'alert_sysstatus': alerts.get(data['alert_sysstatus']),
        'alert_hderrors': alerts.get(data['alert_hderrors']),
        'alert_network': alerts.get(data['alert_network']),
        'alert_remote': alerts.get(data['alert_remote']),
        'alert_power': alerts.get(data['alert_power']),
        'alert_memory': alerts.get(data['alert_memory']),
        'alert_others': alerts.get(data['alert_others']),
    }
    return result


def main():
    # import pdb; pdb.set_trace()
    module_args = dict(
        irmc_url=dict(required=True, type="str"),
        irmc_username=dict(required=True, type="str"),
        irmc_password=dict(required=True, type="str", no_log=True),
        validate_certs=dict(required=False, type="bool", default=True),
        command=dict(required=False, type="str", default="get", choices=["get", "change", "create", "delete"]),
        name=dict(required=True, type="str"),
        password=dict(required=False, type="str", no_log=True),
        description=dict(required=False, type="str"),
        enabled=dict(required=False, type="bool"),
        lan_privilege=dict(required=False, type="str",
                           choices=["Reserved", "Callback", "User", "Operator", "Administrator", "OEM", "NoAccess"]),
        serial_privilege=dict(required=False, type="str",
                              choices=["Reserved", "Callback", "User", "Operator", "Administrator", "OEM", "NoAccess"]),
        config_user_enabled=dict(required=False, type="bool"),
        config_bmc_enabled=dict(required=False, type="bool"),
        avr_enabled=dict(required=False, type="bool"),
        storage_enabled=dict(required=False, type="bool"),
        redfish_enabled=dict(required=False, type="bool"),
        redfish_role=dict(required=False, type="str",
                          choices=["NoAccess", "Operator", "Administrator", "ReadOnly"]),
        # redfish_lock_status=????
        shell=dict(required=False, type="str",
                   choices=["SMASH CLP", "CLI", "Remote Manager", "IPMI basic mode", "IPMI terminal mode", "None"]),
        snmpv3_enabled=dict(required=False, type="bool"),
        snmpv3_access=dict(required=False, type="str", choices=["ReadOnly", "ReadWrite", "Other"]),
        snmpv3_auth=dict(required=False, type="str", choices=["Undefined", "SHA", "MD5", "None"]),
        snmpv3_privacy=dict(required=False, type="str", choices=["Undefined", "AES", "DES", "None"]),
        ssh_public_key=dict(required=False, type="str"),
        ssh_certificate=dict(required=False, type="str"),
        email_enabled=dict(required=False, type="bool"),
        email_encrypted=dict(required=False, type="bool"),
        email_type=dict(required=False, type="str",
                        choices=["Standard", "ITS-Format", "REMCS", "Fixed Subject", "SMS"]),
        email_server=dict(required=False, type="str", choices=["Automatic", "Primary", "Secondary"]),
        email_address=dict(required=False, type="str"),
        alert_fans=dict(required=False, type="str", choices=["None", "Critical", "Warning", "All"]),
        alert_temperatures=dict(required=False, type="str", choices=["None", "Critical", "Warning", "All"]),
        alert_hwerrors=dict(required=False, type="str", choices=["None", "Critical", "Warning", "All"]),
        alert_syshang=dict(required=False, type="str", choices=["None", "Critical", "Warning", "All"]),
        alert_posterrors=dict(required=False, type="str", choices=["None", "Critical", "Warning", "All"]),
        alert_security=dict(required=False, type="str", choices=["None", "Critical", "Warning", "All"]),
        alert_sysstatus=dict(required=False, type="str", choices=["None", "Critical", "Warning", "All"]),
        alert_hderrors=dict(required=False, type="str", choices=["None", "Critical", "Warning", "All"]),
        alert_network=dict(required=False, type="str", choices=["None", "Critical", "Warning", "All"]),
        alert_remote=dict(required=False, type="str", choices=["None", "Critical", "Warning", "All"]),
        alert_power=dict(required=False, type="str", choices=["None", "Critical", "Warning", "All"]),
        alert_memory=dict(required=False, type="str", choices=["None", "Critical", "Warning", "All"]),
        alert_others=dict(required=False, type="str", choices=["None", "Critical", "Warning", "All"]),
    )
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    irmc_user(module)


if __name__ == '__main__':
    main()
