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
module: irmc_facts

short_description: get or set PRIMERGY server and iRMC facts

description:
    - Ansible module to get or set basic iRMC and PRIMERGY server data via iRMC RedFish interface.
    - Module Version V1.0.1.

requirements:
    - The module needs to run locally.
    - iRMC S4 needs FW >= 9.04, iRMC S5 needs FW >= 1.25.
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
        description: get or set server facts
        required:    false
        default:     get
        choices:     ['get', 'set']
    asset_tag:
        description: server asset tag
        required:    false
    location:
        description: server location
        required:    false
    description:
        description: server description
        required:    false
    helpdesk_message:
        description: help desk message
        required:    false

notes:
    - See http://manuals.ts.fujitsu.com/file/13371/irmc-restful-spec-en.pdf
    - See http://manuals.ts.fujitsu.com/file/13372/irmc-redfish-wp-en.pdf
'''

EXAMPLES = '''
# Get basic server and iRMC facts
- name: Get basic server and iRMC facts
  irmc_facts:
    irmc_url: "{{ inventory_hostname }}"
    irmc_username: "{{ irmc_user }}"
    irmc_password: "{{ irmc_password }}"
    validate_certs: "{{ validate_certificate }}"
    command: "get"
  register: facts
  delegate_to: localhost
- name: Show server and iRMC facts
  debug:
    msg: "{{ facts.facts }}"

# Set server asset tag
- name: Set server asset tag
  irmc_facts:
    irmc_url: "{{ inventory_hostname }}"
    irmc_username: "{{ irmc_user }}"
    irmc_password: "{{ irmc_password }}"
    validate_certs: "{{ validate_certificate }}"
    command: "set"
    asset_tag: "Ansible test server"
  delegate_to: localhost
'''

RETURN = '''
facts:
    description: basic server and iRMC facts
    returned: always
    type: dict
'''


# pylint: disable=wrong-import-position
import json
from ansible.module_utils.basic import AnsibleModule

from ansible.module_utils.irmc import irmc_redfish_get, irmc_redfish_patch, get_irmc_json
from ansible.module_utils.irmc_scci_utils import setup_datadict


def irmc_facts(module):
    result = dict(
        changed=False,
        status=0
    )

    if module.check_mode:
        result['msg'] = "module was not run"
        module.exit_json(**result)

    facts, count = setup_datadict(module)    # pylint: disable=unused-variable

    # Get iRMC system data
    status, sysdata, msg = irmc_redfish_get(module, "redfish/v1/Systems/0/")
    if status < 100:
        module.fail_json(msg=msg, exception=sysdata)
    elif status != 200:
        module.fail_json(msg=msg, status=status)

    # Get iRMC OEM system data
    status, oemdata, msg = irmc_redfish_get(module, "redfish/v1/Systems/0/Oem/ts_fujitsu/System")
    if status < 100:
        module.fail_json(msg=msg, exception=oemdata)
    elif status != 200:
        module.fail_json(msg=msg, status=status)

    if module.params['command'] == "get":
        result['facts'] = setup_resultdata(sysdata, oemdata)
        module.exit_json(**result)

    # Set iRMC OEM system data
    if module.params['asset_tag'] is not None or module.params['location'] is not None or \
       module.params['description'] is not None or module.params['helpdesk_message'] is not None:
        body = setup_facts(facts)
        etag = get_irmc_json(oemdata.json(), "@odata.etag")
        status, patch, msg = irmc_redfish_patch(module, "redfish/v1/Systems/0/Oem/ts_fujitsu/System/",
                                                json.dumps(body), etag)
        if status < 100:
            module.fail_json(msg=msg, exception=patch)
        elif status != 200:
            module.fail_json(msg=msg, status=status)
        result['changed'] = True

    module.exit_json(**result)


def setup_facts(data):
    body = dict()
    if data['asset_tag'] is not None:
        body['AssetTag'] = data['asset_tag']
    if data['location'] is not None:
        body['Location'] = data['location']
    if data['description'] is not None:
        body['Description'] = data['description']
    if data['helpdesk_message'] is not None:
        body['HelpdeskMessage'] = data['helpdesk_message']
    return body


def setup_resultdata(data, data2):
    data = {
        'asset_tag': get_irmc_json(data2.json(), "AssetTag"),
        'bios_version': get_irmc_json(data.json(), "BiosVersion"),
        'idled_state': get_irmc_json(data.json(), "IndicatorLED"),
        'host_name': get_irmc_json(data.json(), "HostName"),
        'system_manufacturer': get_irmc_json(data.json(), "Manufacturer"),
        'system_model': get_irmc_json(data.json(), "Model"),
        # 'system_name': get_irmc_json(data.json(), "Name"),
        'system_part_number': get_irmc_json(data.json(), "PartNumber"),
        'power_state': get_irmc_json(data.json(), "PowerState"),
        'system_serial_number': get_irmc_json(data.json(), "SerialNumber"),
        'system_uuid': get_irmc_json(data.json(), "UUID"),
        'location': get_irmc_json(data2.json(), "Location"),
        'description': get_irmc_json(data2.json(), "Description"),
        'helpdesk_message': get_irmc_json(data2.json(), "HelpdeskMessage"),
        'system_ip': get_irmc_json(data2.json(), "SystemIP"),
        'mainboard_manufacturer': get_irmc_json(data.json(), ["Oem", "ts_fujitsu", "MainBoard", "Manufacturer"]),
        'mainboard_dnumber': get_irmc_json(data.json(), ["Oem", "ts_fujitsu", "MainBoard", "Model"]),
        'mainboard_part_number': get_irmc_json(data.json(), ["Oem", "ts_fujitsu", "MainBoard", "PartNumber"]),
        'mainboard_serial_number': get_irmc_json(data.json(), ["Oem", "ts_fujitsu", "MainBoard", "SerialNumber"]),
        'mainboard_version': get_irmc_json(data.json(), ["Oem", "ts_fujitsu", "MainBoard", "Version"])
    }
    return data


def main():
    # import pdb; pdb.set_trace()
    module_args = dict(
        irmc_url=dict(required=True, type="str"),
        irmc_username=dict(required=True, type="str"),
        irmc_password=dict(required=True, type="str", no_log=True),
        validate_certs=dict(required=False, type="bool", default=True),
        command=dict(required=False, type="str", default="get", choices=["get", "set"]),
        asset_tag=dict(required=False, type="str"),
        location=dict(required=False, type="str"),
        description=dict(required=False, type="str"),
        helpdesk_message=dict(required=False, type="str"),
    )
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    irmc_facts(module)


if __name__ == '__main__':
    main()
