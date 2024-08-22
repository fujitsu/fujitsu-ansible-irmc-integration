#!/usr/bin/python

# Copyright 2018-2024 Fsas Technologies Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


DOCUMENTATION = r'''
---
module: irmc_session

short_description: handle iRMC sessions

description:
    - Ansible module to handle iRMC sessions via Restful API.
    - Module Version V1.3.0.

requirements:
    - The module needs to run locally.
    - iRMC S6
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
        description: Handle iRMC sessions.
        required:    false
        default:     list
        choices:     ['list', 'get', 'remove', 'terminate', 'clearall']
    id:
        description: Specific session to get, remove or terminate.
        required:    false
'''

EXAMPLES = r'''
# List iRMC sessions
- name: Get and show iRMC sessions
  tags:
    - list
  block:
    - name: List iRMC sessions
      irmc_session:
        irmc_url: "{{ inventory_hostname }}"
        irmc_username: "{{ irmc_user }}"
        irmc_password: "{{ irmc_password }}"
        validate_certs: "{{ validate_certificate }}"
        command: "list"
      delegate_to: localhost
      register: result
    - name: Show iRMC sessions details
      ansible.builtin.debug:
        var: result.sessions

# Get specific session information
- name: Get specific session information
  tags:
    - get
  block:
    - name: Get specific session information
      irmc_session:
        irmc_url: "{{ inventory_hostname }}"
        irmc_username: "{{ irmc_user }}"
        irmc_password: "{{ irmc_password }}"
        validate_certs: "{{ validate_certificate }}"
        command: "get"
        id: "{{ session_id | int }}"
      delegate_to: localhost
      register: result
    - name: Show specific session information
      ansible.builtin.debug:
        var: result

# Remove specific session information
- name: Remove specific session information
  tags:
    - remove
  block:
    - name: Remove specific session information
      irmc_session:
        irmc_url: "{{ inventory_hostname }}"
        irmc_username: "{{ irmc_user }}"
        irmc_password: "{{ irmc_password }}"
        validate_certs: "{{ validate_certificate }}"
        command: "remove"
        id: "{{ session_id | int }}"
      delegate_to: localhost
      register: result
    - name: Show result of remove session
      ansible.builtin.debug:
        var: result

# Clear all sessions information
- name: Clear all sessions information
  irmc_session:
    irmc_url: "{{ inventory_hostname }}"
    irmc_username: "{{ irmc_user }}"
    irmc_password: "{{ irmc_password }}"
    validate_certs: "{{ validate_certificate }}"
    command: "clearall"
  delegate_to: localhost
  register: result
  tags:
    - clearall

# Terminate specific session
- name: Terminate specific session
  irmc_session:
    irmc_url: "{{ inventory_hostname }}"
    irmc_username: "{{ irmc_user }}"
    irmc_password: "{{ irmc_password }}"
    validate_certs: "{{ validate_certificate }}"
    command: "terminate"
    id: "{{ session_id | int }}"
  delegate_to: localhost
  register: result
  tags:
    - terminate
'''

RETURN = r'''
details_for_list:
    description: If command is “list”, the following values are returned.
    contains:
        Duration:
            description: Session duration in seconds
            returned: always
            type: int
            sample: 226
        Id:
            description: session ID
            returned: always
            type: int
            sample: 4
        Start:
            description: work sequence
            returned: always
            type: string
            sample: 2018/07/31 12:09:25
        Status:
            description: session status
            returned: always
            type: string
            sample: terminated regularly
        Tag:
            description: session tag
            returned: always
            type: string
            sample:
        Text:
            description: work sequence
            returned: always
            type: string
            sample: offlineUpdatePrepare

details_for_get:
    description: If command is “get”, the following values are returned.
    contains:
        session_log.SessionLog.Entries.Entry:
            description: list of individual session log entries
            returned: always
            type: list
        session_log.SessionLog.Id:
            description: Session ID
            returned: always
            type: int
            sample: 4
        session_log.SessionLog.Tag:
            description: session tag
            returned: always
            type: string
            sample:
        session_log.SessionLog.WorkSequence:
            description: work sequence
            returned: always
            type: string
            sample: prepareOfflineUpdate
        session_status:
            description: session status
            returned: always
            type: string
            sample: terminated regularly

otherwise:
    description: >
        For other commands ("remove", "terminate", etc.),
        the default return value of Ansible (changed, failed, etc.) is returned.
'''


from typing import Any

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.irmc import get_irmc_json, irmc_redfish_delete, irmc_redfish_get

# Global
result = dict()


def irmc_session(module: AnsibleModule) -> None:
    # initialize result
    result['changed'] = False
    result['status'] = 0

    if module.check_mode:
        result['msg'] = 'module was not run'
        module.exit_json(**result)

    # preliminary parameter check
    preliminary_parameter_check(module)

    sessions = get_irmc_sessions(module)
    if module.params['command'] == 'list':
        result['sessions'] = {}
    id_found = 0

    for _key, session in sessions.items():
        for item in session:
            if module.params['command'] == 'clearall':
                id_found += 1
                if 'Profile' not in item['#text']:
                    continue
                handle_irmc_session(module, 'remove', item)
            elif module.params['command'] == 'list':
                id_found += 1
                result['sessions']['session{0}'.format(item['@Id'])] = get_irmc_session_info(module, item)
            elif item['@Id'] == module.params['id']:
                id_found += 1
                if module.params['command'] in ('terminate', 'remove') and \
                   'Profile' not in item['#text'] and 'Update' not in item['#text'] and \
                   'Configuration' not in item['#text']:
                    result['msg'] = "Session '{0}/{1}' is owned by iRMC. It cannot be {2}d.".format(item['@Id'], item['#text'], module.params['command'])
                    result['status'] = 11
                    module.fail_json(**result)
                handle_irmc_session(module, module.params['command'], item)

    if id_found == 0 and module.params['command'] != 'list':
        result['msg'] = "Session with ID '{0}' does not exist.".format(module.params['id'])
        if module.params['command'] in ('get'):
            result['status'] = 12
            module.fail_json(**result)
        else:
            result['skipped'] = True

    module.exit_json(**result)


def preliminary_parameter_check(module: AnsibleModule) -> None:
    if (module.params['command'] in ('get', 'remove', 'terminate')) and module.params['id'] is None:
        result['msg'] = "Command '{0}' requires 'id' parameter to be set!".format(module.params['command'])
        result['status'] = 10
        module.fail_json(**result)


def get_irmc_sessions(module: AnsibleModule):
    status, sessiondata, msg = irmc_redfish_get(module, 'sessionInformation')
    if status < 100:
        module.fail_json(msg=msg, status=status, exception=sessiondata)
    elif status not in (200, 202, 204):
        module.fail_json(msg=msg, status=status)
    return get_irmc_json(sessiondata.json(), ['SessionList'])


def get_irmc_session_info(module: AnsibleModule, item) -> dict[str, Any]:
    status, sdata, msg = irmc_redfish_get(module, 'sessionInformation/{0}/status'.format(item['@Id']))
    if status < 100:
        module.fail_json(msg=msg, status=status, exception=sdata)
    elif status not in (200, 202, 204):
        module.fail_json(msg=msg, status=status)

    session = {}
    session['Id'] = item['@Id']
    session['Text'] = item['#text']
    session['Tag'] = item['@Tag']
    session['Status'] = get_irmc_json(sdata.json(), ['Session', 'Status'])
    session['Start'] = get_irmc_json(sdata.json(), ['Session', 'Start'])
    session['Duration'] = get_irmc_json(sdata.json(), ['Session', 'Duration'])
    return session


def handle_irmc_session(module: AnsibleModule, command, item) -> None:
    status, sdata, msg = irmc_redfish_get(module, 'sessionInformation/{0}/status'.format(item['@Id']))
    if status < 100:
        module.fail_json(msg=msg, status=status, exception=sdata)
    elif status not in (200, 202, 204):
        module.fail_json(msg=msg, status=status)

    sstatus = get_irmc_json(sdata.json(), ['Session', 'Status'])
    if command == 'get':
        status, sdata, msg = irmc_redfish_get(module, 'sessionInformation/{0}/log'.format(item['@Id']))
        if status < 100:
            module.fail_json(msg=msg, status=status, exception=sdata)
        elif status not in (200, 202, 204):
            module.fail_json(msg=msg, status=status)
        result['session_status'] = sstatus
        result['session_log'] = sdata.json()
        module.exit_json(**result)
    elif command == 'terminate' and 'terminat' in sstatus:
        result['msg'] = "Session '{0}'/'{1}' is already terminated.".format(item['@Id'], item['#text'])
        result['skipped'] = True
    elif command == 'remove' and 'terminated' not in sstatus:
        if module.params['command'] != 'clearall':
            result['msg'] = "Session '{0}'/'{1}' is not yet terminated and cannot be removed.".format(item['@Id'], item['#text'])
            module.exit_json(**result)
    else:
        status, sdata, msg = irmc_redfish_delete(module, 'sessionInformation/{0}/{1}'.format(item['@Id'], command))
        if status < 100:
            module.fail_json(msg=msg, status=status, exception=sdata)
        elif status not in (200, 202, 204):
            module.fail_json(msg=msg, status=status)
        result['changed'] = True


def main() -> None:
    # breakpoint()
    module_args = dict(
        irmc_url=dict(required=True, type='str'),
        irmc_username=dict(required=True, type='str'),
        irmc_password=dict(required=True, type='str', no_log=True),
        validate_certs=dict(required=False, type='bool', default=True),
        command=dict(required=False, type='str', default='list',
                     choices=['list', 'get', 'remove', 'terminate', 'clearall']),
        id=dict(required=False, type='int'),
    )
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False,
    )

    irmc_session(module)


if __name__ == '__main__':
    main()
