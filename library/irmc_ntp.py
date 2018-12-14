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
module: irmc_ntp

short_description: manage iRMC time options

description:
    - Ansible module to manage iRMC time options via iRMC remote scripting interface.
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

notes:
    - See http://manuals.ts.fujitsu.com/file/12563/wp-svs-irmc-remote-scripting-en.pdf
    - See https://sp.ts.fujitsu.com/dmsp/Publications/public/dp-svs-configuration-space-values-en.pdf
'''

EXAMPLES = '''
# Get iRMC time settings
- name: Get iRMC time settingsa
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
    msg: "{{ time.time_settings }}"

# Set iRMC time option(s)
- name: Set iRMC time option(s)
  irmc_ntp:
    irmc_url: "{{ inventory_hostname }}"
    irmc_username: "{{ irmc_user }}"
    irmc_password: "{{ irmc_password }}"
    validate_certs: "{{ validate_certificate }}"
    command: "set"
    time_mode: "System RTC"
  delegate_to: localhost
'''

RETURN = '''
# time_settings returned for command "get":
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

# For command "set":
    Default return values:
'''


from ansible.module_utils.basic import AnsibleModule

from ansible.module_utils.irmc_scci_utils import get_scciresultlist, irmc_scci_post, \
                                                 setup_datadict, setup_commandlist

time_mode = {"0": "System RTC", "1": "NTP", "2": "MMB NTP"}
rtc_mode = {"0": "local time", "1": "UTC/GMT"}
true_false = {"0": "False", "1": "True"}
param_scci_map = [
    # Param, SCCI Name, SCCI Code, index, value dict
    ["time_mode", "ConfBmcTimeSyncSource", 0x00B4, 0, time_mode],            # iRMC: Time Mode
    ["rtc_mode", "ConfBmcRtcMode", 0x00B6, 0, rtc_mode],                     # iRMC: RTC Mode
    ["time_zone", "ConfBMCTimeZone", 0x00B2, 0, None],                       # iRMC: -
    ["time_zone_location", "ConfBmcTimeZoneLocation", 0x00B5, 0, None],      # iRMC: Time Zone Location
    ["ntp_server_primary", "ConfBmcNtpServer", 0x00B3, 0, None],             # iRMC: Primary NTP Server
    ["ntp_server_secondary", "ConfBmcNtpServer", 0x00B3, 1, None],           # iRMC: Secondary NTP Server
    ["mmb_time_sync", "", 0x00B7, 0, true_false],                            # iRMC: -
]


def irmc_ntp(module):
    result = dict(
        changed=False,
        status=0
    )

    if module.check_mode:
        result['msg'] = "module was not run"
        module.exit_json(**result)

    module.params['time_zone'] = None
    module.params['mmb_time_sync'] = None
    ntpdata, setparam_count = setup_datadict(module)

    # preliminary parameter checks
    if module.params['command'] == "set":
        if setparam_count < 0:
            result['msg'] = "Command 'set' requires at least one parameter to be changed!"
            result['status'] = 10
            module.fail_json(**result)

    # set up command list
    if module.params['command'] == "get":
        body = setup_commandlist(ntpdata, "GET", param_scci_map)
    else:
        body = setup_commandlist(ntpdata, "SET", param_scci_map)

    # send command list to scripting interface
    status, data, msg = irmc_scci_post(module, body)
    if status < 100:
        module.fail_json(msg=msg, status=status, exception=data)
    elif status not in (200, 202, 204):
        module.fail_json(msg=msg, status=status)

    # evalaute result list
    ntpdata, scciresult, sccicontext = get_scciresultlist(data.content, ntpdata, param_scci_map)
    if scciresult != 0:
        module.fail_json(msg=sccicontext, status=scciresult)

    if module.params['command'] == "get":
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


def main():
    # import pdb; pdb.set_trace()
    module_args = dict(
        irmc_url=dict(required=True, type="str"),
        irmc_username=dict(required=True, type="str"),
        irmc_password=dict(required=True, type="str", no_log=True),
        validate_certs=dict(required=False, type="bool", default=True),
        command=dict(required=False, type="str", default="get", choices=["get", "set"]),
        time_mode=dict(required=False, type="str", choices=["System RTC", "NTP", "MMB NTP"]),
        rtc_mode=dict(required=False, type="str", choices=["local time", "UTC/GMT"]),
        time_zone_location=dict(required=False, type="str"),
        ntp_server_primary=dict(required=False, type="str"),
        ntp_server_secondary=dict(required=False, type="str")
    )
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    irmc_ntp(module)


if __name__ == '__main__':
    main()
