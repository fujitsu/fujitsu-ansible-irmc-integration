#!/usr/bin/python

# Copyright 2018-2024 Fsas Technologies Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = '''
---
module: irmc_ntp

short_description: manage iRMC time options

description:
    - Ansible module to manage iRMC time options via iRMC remote scripting interface.
    - Module Version V1.3.0.

requirements:
    - The module needs to run locally.
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
        description: NTP management to be executed.
        required:    false
        default:     get
        choices:     ['get', 'set']
    time_mode:
        description: Defines how iRMC synchronizes its real-time clock (RTC).
        required:    false
        choices:     ["System RTC", "NTP", "MMB NTP"]
    rtc_mode:
        description: Defines how iRMC interprets the system's hardware RTC time.
        required:    false
        choices:     ["local time", "UTC/GMT"]
    time_zone_location:
        description: iRMC time zone (e.g. 'Europe/Berlin'; based on Linux 'tzdata').
        required:    false
    ntp_server_primary:
        description: IP address (IPv4 or IPv6) or DNS name of primary NTP server.
        required:    false
    ntp_server_secondary:
        description: IP address (IPv4 or IPv6) or DNS name of secondary NTP server.
        required:    false
'''

EXAMPLES = '''
# Get iRMC time settings
- block:
  - name: Get iRMC time settings
    irmc_ntp:
      irmc_url: "{{ inventory_hostname }}"
      irmc_username: "{{ irmc_user }}"
      irmc_password: "{{ irmc_password }}"
      validate_certs: "{{ validate_certificate }}"
      command: "get"
    register: time
    delegate_to: localhost
  - name: Show iRMC time settings
    debug:
      var: time.time_settings
  tags:
    - get

# Set iRMC time option(s)
- name: Set iRMC time option(s)
  irmc_ntp:
    irmc_url: "{{ inventory_hostname }}"
    irmc_username: "{{ irmc_user }}"
    irmc_password: "{{ irmc_password }}"
    validate_certs: "{{ validate_certificate }}"
    command: "set"
    time_mode: "System RTC"
    time_zone_location: "Asia/Tokyo"
    rtc_mode: "local time"
  delegate_to: localhost
  tags:
    - set
'''

RETURN = '''
details_for_get:
    description: If command is “get”, the following values are returned.
    contains:
        ntp_server_primary:
            description: primary NTP server
            returned: always
            type: string
            sample: pool.ntp.org
        ntp_server_secondary:
            description: secondary NTP server
            returned: always
            type: string
            sample: pool.ntp.org
        rtc_mode:
            description: Defines how iRMC interprets the system's hardware RTC time
            returned: always
            type: string
            sample: local time
        time_mode:
            description: Defines how iRMC synchronizes its real-time clock (RTC)
            returned: always
            type: string
            sample: System RTC
        time_zone_location:
            description: iRMC time zone
            returned: always
            type: string
            sample: Europe/Berlin

details_for_set:
    description: If command is “set”, the default return value of Ansible is returned.

'''


from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.irmc_scci_utils import (
    add_scci_command,
    get_key_for_value,
    get_scciresultlist_oi,
    irmc_scci_post,
    setup_commandlist,
    setup_datadict,
)

time_mode = {'0': 'System RTC', '1': 'NTP', '2': 'MMB NTP'}
rtc_mode = {'0': 'local time', '1': 'UTC/GMT'}
true_false = {'0': 'False', '1': 'True'}
param_scci_map = [
    # Param, SCCI Name, SCCI Code, index, value dict
    ['time_mode', 'ConfBmcTimeSyncSource', 0x00B4, 0, time_mode],            # iRMC: Time Mode
    ['rtc_mode', 'ConfBmcRtcMode', 0x00B6, 0, rtc_mode],                     # iRMC: RTC Mode
    ['time_zone', 'ConfBMCTimeZone', 0x00B2, 0, None],                       # iRMC: -
    ['time_zone_location', 'ConfBmcTimeZoneLocation', 0x00B5, 0, None],      # iRMC: Time Zone Location
    ['ntp_server_primary', 'ConfBmcNtpServer', 0x00B3, 0, None],             # iRMC: Primary NTP Server
    ['ntp_server_secondary', 'ConfBmcNtpServer', 0x00B3, 1, None],           # iRMC: Secondary NTP Server
]


def irmc_ntp(module):
    result = dict(
        changed=False,
        status=0,
    )

    if module.check_mode:
        result['msg'] = 'module was not run'
        module.exit_json(**result)

    module.params['time_zone'] = None
    ntpdata, setparam_count = setup_datadict(module)

    # preliminary parameter checks
    if module.params['command'] == 'set' and setparam_count < 0:
        result['msg'] = "Command 'set' requires at least one parameter to be changed!"
        result['status'] = 10
        module.fail_json(**result)

    # set up command list
    if module.params['command'] == 'get':
        body = setup_commandlist(ntpdata, 'GET', param_scci_map)
    else:
        body = setup_commandlist_for_set(ntpdata, 'SET', param_scci_map)

    # send command list to scripting interface
    status, data, msg = irmc_scci_post(module, body)
    if status < 100:
        module.fail_json(msg=msg, status=status, exception=data)
    elif status not in (200, 202, 204):
        module.fail_json(msg=msg, status=status)

    # evalaute result list
    ntpdata, scciresult, sccicontext = get_scciresultlist_oi(data.content, ntpdata, param_scci_map)
    if scciresult != 0:
        module.fail_json(msg=sccicontext, status=scciresult)

    if module.params['command'] == 'get':
        result['time_settings'] = setup_resultdata(ntpdata)
    else:
        result['changed'] = True

    module.exit_json(**result)


def setup_resultdata(data):
    result = {
        'time_mode': time_mode.get(data['time_mode']),
        'rtc_mode': rtc_mode.get(data['rtc_mode']),
        'time_zone_location': data['time_zone_location'],
        'ntp_server_primary': data['ntp_server_primary'],
        'ntp_server_secondary': data['ntp_server_secondary'],
    }
    return result


def setup_commandlist_for_set(cmdlist, ctype, scci_map):
    body = '''<?xml version="1.0" encoding="UTF-8" standalone="yes" ?><CMDSEQ>\n'''
    data = ''
    for elem in scci_map:
        if elem[0] not in cmdlist:
            continue
        if elem[4] is not None and cmdlist[elem[0]] is not None:
            data = get_key_for_value(cmdlist[elem[0]], elem[4])
        else:
            data = cmdlist[elem[0]]
        if elem[1] == 'ConfBmcNtpServer':
            body += add_scci_command(ctype, scci_map, elem[1], elem[3], data, convert_dtype=False)
        else:
            body += add_scci_command(ctype, scci_map, elem[1], elem[3], data)
    body += '</CMDSEQ>'
    return body


def main():
    # import pdb; pdb.set_trace()
    module_args = dict(
        irmc_url=dict(required=True, type='str'),
        irmc_username=dict(required=True, type='str'),
        irmc_password=dict(required=True, type='str', no_log=True),
        validate_certs=dict(required=False, type='bool', default=True),
        command=dict(required=False, type='str', default='get', choices=['get', 'set']),
        time_mode=dict(required=False, type='str', choices=['System RTC', 'NTP', 'MMB NTP']),
        rtc_mode=dict(required=False, type='str', choices=['local time', 'UTC/GMT']),
        time_zone_location=dict(required=False, type='str'),
        ntp_server_primary=dict(required=False, type='str'),
        ntp_server_secondary=dict(required=False, type='str'),
    )
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False,
    )

    irmc_ntp(module)


if __name__ == '__main__':
    main()
