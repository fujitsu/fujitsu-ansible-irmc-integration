#!/usr/bin/python

# Copyright 2018-2024 Fsas Technologies Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


DOCUMENTATION = r'''
---
module: irmc_scci

short_description: execute iRMC remote SCCI commands

description:
    - Ansible module to execute iRMC Remote Scripting (SCCI) commands.
    - Module Version V1.3.0.

requirements:
    - The module needs to run locally.
    - iRMC S6.
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
        description: SCCI remote scripting command.
        required:    true
        choices:
            - get_cs            (ConfigSpace Read)
            - set_cs            (ConfigSpace Write)
            - power_on          (Power-On the Server)
            - power_off         (Power-Off the Server)
            - power_cycle       (Power Cycle the Server)
            - reset             (Hard Reset the Server)
            - nmi               (Pulse the NMI (Non Maskable Interrupt))
            - graceful_shutdown (Graceful Shutdown, requires running Agent)
            - graceful_reboot   (Graceful Reboot, requires running Agent)
            - cancel_shutdown   (Cancel a Shutdown Request)
            - reset_firmware    (Perform a BMC Reset)
    opcodeext:
        description: SCCI opcode extension.
        required:    false
    index:
        description: SCCI index.
        required:    false
    cabid:
        description: SCCI cabinet ID.
        default:     -1 (main cabinet)
        required:    false
    data:
        description: Data for commands which require data, ignored otherwise.
        required:    false
'''

EXAMPLES = r'''
# Write server location
- name: Write server location
  fujitsu.primergy.irmc_scci:
    irmc_url: "{{ inventory_hostname }}"
    irmc_username: "{{ irmc_user }}"
    irmc_password: "{{ irmc_password }}"
    validate_certs: "{{ validate_certificate }}"
    command: "set_cs"
    opcodeext: 0x200
    data: "In a galaxy far, far away ..."
  delegate_to: localhost
  tags:
    - write

# Read server location
- block:
  - name: "Read server location"
    fujitsu.primergy.irmc_scci:
      irmc_url: "{{ inventory_hostname }}"
      irmc_username: "{{ irmc_user }}"
      irmc_password: "{{ irmc_password }}"
      validate_certs: "{{ validate_certificate }}"
      command: "get_cs"
      opcodeext: 0x200
    register: read_result
    delegate_to: localhost
  - name: Show server location
    debug:
      var: read_result.data
  tags:
    - read

# Power on the server
- name: "Power on the server"
  fujitsu.primergy.irmc_scci:
    irmc_url: "{{ inventory_hostname }}"
    irmc_username: "{{ irmc_user }}"
    irmc_password: "{{ irmc_password }}"
    validate_certs: "{{ validate_certificate }}"
    command: "power_on"
    opcodeext: 0x200
  delegate_to: localhost
  tags:
    - poweron

# Power off the server
- name: "Power off the server"
  fujitsu.primergy.irmc_scci:
    irmc_url: "{{ inventory_hostname }}"
    irmc_username: "{{ irmc_user }}"
    irmc_password: "{{ irmc_password }}"
    validate_certs: "{{ validate_certificate }}"
    command: "power_off"
    opcodeext: 0x200
  delegate_to: localhost
  tags:
    - poweroff

# Cancel shutdown
- name: "Cancel shutdown"
  fujitsu.primergy.irmc_scci:
    irmc_url: "{{ inventory_hostname }}"
    irmc_username: "{{ irmc_user }}"
    irmc_password: "{{ irmc_password }}"
    validate_certs: "{{ validate_certificate }}"
    command: "cancel_shutdown"
    opcodeext: 0x200
  delegate_to: localhost
  tags:
    - cancel_shutdown

# Reset firmware
- name: "Reset firmware"
  fujitsu.primergy.irmc_scci:
    irmc_url: "{{ inventory_hostname }}"
    irmc_username: "{{ irmc_user }}"
    irmc_password: "{{ irmc_password }}"
    validate_certs: "{{ validate_certificate }}"
    command: "reset_firmware"
    opcodeext: 0x200
  delegate_to: localhost
  tags:
    - reset_firm
'''

RETURN = r'''
details:
    description:
        If command is “get_cs”, the following value is returned.

        For all other commands, the default return value of Ansible (changed, failed, etc.) is returned.

    contains:
        data:
            description: result of requested SCCI command
            returned: always
            type: string
            sample: In a galaxy far, far away ...
'''


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.fujitsu.primergy.plugins.module_utils.irmc_scci_utils import (
    get_scciresult,
    irmc_scci_post,
    setup_sccirequest,
)

scci_code_map = {
    'get_cs': 'E001',  # ConfigSpace Read
    'set_cs': 'E002',  # ConfigSpace Write
    'power_on': '0111',  # Power-On the Server
    'power_off': '0112',  # Power-Off the Server
    'power_cycle': '0113',  # Power Cycle the Server
    'reset': '0204',  # Hard Reset the Server
    'nmi': '020C',  # Pulse the NMI (Non Maskable Interrupt)
    'graceful_shutdown': '0205',  # Graceful Shutdown, requires running Agent
    'graceful_reboot': '0206',  # Graceful Reboot, requires running Agent
    'cancel_shutdown': '0209',  # Cancel a Shutdown Request
    'reset_firmware': '0203',  # Perform a BMC Reset
    'connect_storage': '0250',  # Connect/Disconnect a standalone Remote Storage Server

    # TODO: The following 3 items will be removed after checking unused.
    'connect_fd': '0251',  # Connect/Disconnect a Floppy image on a Remote Share (NFS/SMB)
    'connect_cd': '0252',  # Connect/Disconnect a CD/DVD image on a Remote Share (NFS/SMB)
    'connect_hd': '0253',  # Connect/Disconnect a HDD image on a Remote Share (NFS/SMB)
}


def irmc_scci(module):
    result = dict(
        changed=False,
        status=0,
    )

    if module.check_mode:
        result['msg'] = 'module was not run'
        module.exit_json(**result)

    if module.params['command'] == 'set_cs' and module.params['data'] is None:
        result['msg'] = "SCCI SET command requires 'data' parameter!"
        result['status'] = 10
        module.fail_json(**result)

    body = setup_sccirequest(module, scci_code_map)

    # send command to scripting interface
    status, data, msg = irmc_scci_post(module, body)
    if status < 100:
        module.fail_json(msg=msg, status=status, exception=data)
    elif status not in (200, 202, 204):
        module.fail_json(msg=msg, status=status)

    # evaluate command result
    sccidata, result['status'], sccicontext = get_scciresult(
        data.content,
        module.params['opcodeext'],
    )
    if result['status'] != 0:
        result['msg'] = (
            "SCCI '{0}' command was not successful. Return code {1}: {2}".format(
                module.params['command'],
                result['status'],
                sccicontext,
            )
        )
        if result['status'] == 95:
            result['exception'] = sccidata
        module.fail_json(**result)

    if module.params['command'] != 'get_cs':
        result['changed'] = True
    else:
        result['data'] = sccidata

    module.exit_json(**result)


def main():
    # import pdb; pdb.set_trace()
    module_args = dict(
        irmc_url=dict(required=True, type='str'),
        irmc_username=dict(required=True, type='str'),
        irmc_password=dict(required=True, type='str', no_log=True),
        validate_certs=dict(required=False, type='bool', default=True),
        command=dict(
            required=True,
            type='str',
            choices=[
                'get_cs',  # ConfigSpace Read
                'set_cs',  # ConfigSpace Write
                'power_on',  # Power-On the Server
                'power_off',  # Power-Off the Server
                'power_cycle',  # Power Cycle the Server
                'reset',  # Hard Reset the Server
                'nmi',  # Pulse the NMI (Non Maskable Interrupt)
                'graceful_shutdown',  # Graceful Shutdown, requires running Agent
                'graceful_reboot',  # Graceful Reboot, requires running Agent
                'cancel_shutdown',  # Cancel a Shutdown Request
                'reset_firmware',  # Perform a BMC Reset
                'connect_storage',  # Connect/Disconnect a standalone Remote Storage Server
            ],
        ),
        opcodeext=dict(required=True, type='int'),
        index=dict(required=False, type='int', default=0),
        cabid=dict(required=False, type='int', default=-1),
        data=dict(required=False, type='str'),
    )
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False,
    )

    irmc_scci(module)


if __name__ == '__main__':
    main()
