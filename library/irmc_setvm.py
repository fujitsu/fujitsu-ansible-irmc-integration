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
module: irmc_setvm

short_description: set iRMC Virtual Media Data

description:
    - Ansible module to set iRMC Virtual Media Data via iRMC RedFish interface.
    - Module Version V1.1.

requirements:
    - The module needs to run locally.
    - iRMC S4 needs FW >= 9.04, iRMC S5 needs FW >= 1.25.
    - Python >= 2.6
    - Python module 'future'

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
    vm_type:
        description: The virtual media type to be set.
        required:    false
        default:     CDImage
        choices:     ['CDImage', 'FDImage', 'HDImage']
    server:
        description: Remote server (IP or DNS name) where the image is located.
        required:    true
    share:
        description: Path on the remote server where the image is located.
        required:    true
    image:
        description: Name of the remote image.
        required:    true
    share_type:
        description: Share type (NFS share or SMB share).
        required:    false
        choices:     ['NFS', 'SMB']
    vm_domain:
        description: User domain in case of SMB share.
        required:    false
    vm_user:
        description: User account in case of SMB share.
        required:    false
    vm_password:
        description: User password in case of SMB share.
        required:    false
    force_remotemount_enabled:
        description: Forces iRMC to enable the remote mount feature.
        required:    false
    force_mediatype_active:
        description: Forces iRMC to activate one of the required remote media types.
        required:    false

notes:
    - See http://manuals.ts.fujitsu.com/file/13371/irmc-restful-spec-en.pdf
    - See http://manuals.ts.fujitsu.com/file/13372/irmc-redfish-wp-en.pdf
'''

EXAMPLES = '''
# Set Virtual Media Data
- name: Set Virtual Media Data
  irmc_setvm:
    irmc_url: "{{ inventory_hostname }}"
    irmc_username: "{{ irmc_user }}"
    irmc_password: "{{ irmc_password }}"
    validate_certs: "{{ validate_certificate }}"
    server: "{{ server }}"
    share: "{{ share }}"
    image: "{{ image }}"
    share_type: "{{ share_type }}"
  delegate_to: localhost
'''

RETURN = '''
Default return values:
'''


import json
from ansible.module_utils.basic import AnsibleModule

from ansible.module_utils.irmc import irmc_redfish_get, irmc_redfish_patch, get_irmc_json
from ansible.module_utils.irmc_scci_utils import setup_datadict


def irmc_setvirtualmedia(module):
    result = dict(
        changed=False,
        status=0
    )

    if module.check_mode:
        result['msg'] = "module was not run"
        module.exit_json(**result)

    vmparams, count = setup_datadict(module)

    # Get iRMC Virtual Media data
    status, vmdata, msg = irmc_redfish_get(module, "redfish/v1/Systems/0/Oem/ts_fujitsu/VirtualMedia/")
    if status < 100:
        module.fail_json(msg=msg, status=status, exception=vmdata)
    elif status != 200:
        module.fail_json(msg=msg, status=status)

    # Evaluate configured Virtual Media Data
    maxdevno = get_irmc_json(vmdata.json(), [module.params['vm_type'], "MaximumNumberOfDevices"])
    if maxdevno == 0:
        if not module.params['force_mediatype_active']:
            result['warnings'] = "No Virtual Media of Type '" + module.params['vm_type'] + "' is configured!"
            result['status'] = 20
            module.fail_json(**result)
        else:
            new_maxdevno = 1
    else:
        new_maxdevno = maxdevno

    remotemountenabled = get_irmc_json(vmdata.json(), "RemoteMountEnabled")
    if not remotemountenabled and not module.params['force_remotemount_enabled']:
        result['msg'] = "Remote Mount of Virtual Media is not enabled!"
        result['status'] = 30
        module.fail_json(**result)

    # Set iRMC system data
    body = setup_vmdata(vmparams, maxdevno, new_maxdevno)
    etag = get_irmc_json(vmdata.json(), "@odata.etag")
    status, patch, msg = irmc_redfish_patch(module, "redfish/v1/Systems/0/Oem/ts_fujitsu/VirtualMedia/",
                                            json.dumps(body), etag)
    if status < 100:
        module.fail_json(msg=msg, status=status, exception=patch)
    elif status != 200:
        module.fail_json(msg=msg, status=status)

    result['changed'] = True
    module.exit_json(**result)


def setup_vmdata(data, maxdevno, new_maxdevno):
    body = {
        data['vm_type']: {
            "Server": data['server'],
            "ShareName": data['share'],
            "ImageName": data['image']
        }
    }
    if data['force_remotemount_enabled']:
        body['RemoteMountEnabled'] = True
    if maxdevno == 0:
        body[data['vm_type']]['MaximumNumberOfDevices'] = new_maxdevno
    if data['share_type'] is not None:
        body[data['vm_type']]['ShareType'] = data['share_type']
    if data['vm_domain'] is not None:
        body[data['vm_type']]['UserDomain'] = data['vm_domain']
    if data['vm_user'] is not None:
        body[data['vm_type']]['UserName'] = data['vm_user']
    if data['vm_password'] is not None:
        body[data['vm_type']]['Password'] = data['vm_password']
    return body


def main():
    # import pdb; pdb.set_trace()
    module_args = dict(
        irmc_url=dict(required=True, type="str"),
        irmc_username=dict(required=True, type="str"),
        irmc_password=dict(required=True, type="str", no_log=True),
        validate_certs=dict(required=False, type="bool", default=True),
        vm_type=dict(required=False, type="str", default="CDImage", choices=['CDImage', 'FDImage', 'HDImage']),
        server=dict(required=True, type="str"),
        share=dict(required=True, type="str"),
        image=dict(required=True, type="str"),
        share_type=dict(required=False, type="str", choices=['NFS', 'SMB']),
        vm_domain=dict(required=False, type="str"),
        vm_user=dict(required=False, type="str"),
        vm_password=dict(required=False, type="str", no_log=True),
        force_remotemount_enabled=dict(required=False, type="bool", default=False),
        force_mediatype_active=dict(required=False, type="bool", default=False),
    )
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    irmc_setvirtualmedia(module)


if __name__ == '__main__':
    main()
