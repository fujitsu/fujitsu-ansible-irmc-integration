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
module: irmc_getvm

short_description: get iRMC Virtual Media Data

description:
    - Ansible module to get iRMC Virtual Media Data via iRMC RedFish interface.
    - Module Version V1.2.

requirements:
    - The module needs to run locally.
    - iRMC S4 needs FW >= 9.04, iRMC S5 needs FW >= 1.25.
    - Python >= 2.6
    - Python modules 'future', 'requests', 'urllib3'

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
    vm_type:
        description: The virtual media type whose data are to be read.
        required:    false
        default:     CDImage
        choices:     ['CDImage', 'FDImage', 'HDImage']

notes:
    - See http://manuals.ts.fujitsu.com/file/13371/irmc-restful-spec-en.pdf
    - See http://manuals.ts.fujitsu.com/file/13372/irmc-redfish-wp-en.pdf
'''

EXAMPLES = '''
# Get Virtual Media data
- name: Get Virtual Media data
  irmc_getvm:
    irmc_url: "{{ inventory_hostname }}"
    irmc_username: "{{ irmc_user }}"
    irmc_password: "{{ irmc_password }}"
    validate_certs: "{{ validate_certificate }}"
    vm_type: CDImage
  register: vmdata
  delegate_to: localhost
- name: Show Virtual Media data
  debug:
    msg: "{{ vmdata.virtual_media_data }}"
'''

RETURN = '''
# virtual_media_data returned by requesting data for e.g. 'CDImage':
    CDImage:
        description: state of image
        returned: always
        type: string
        sample: Connected
    bootmode:
        description: boot source override mode for the next boot
        returned: always
        type: string
        sample: UEFI
    bootoverride:
        description: boot override type
        returned: always
        type: string
        sample: Once
    bootsource:
        description: boot device override for next boot
        returned: always
        type: string
        sample: BiosSetup
    image_name:
        description: name of the virtual image
        returned: always
        type: string
        sample: mybootimage.iso
    server:
        description: remote server where the image is located
        returned: always
        type: string
        sample: 192.168.2.1
    share_name:
        description: path on the remote server where the image is located
        returned: always
        type: string
        sample: isoimages
    share_type:
        description: share type (NFS or SMB)
        returned: always
        type: string
        sample: NFS
    usb_attach_mode:
        description: remote image attach mode
        returned: always
        type: string
        sample: AutoAttach
    user_domain:
        description: user domain for SMB share
        returned: always
        type: string
        sample: local.net
    user_name:
        description: user name for SM share
        returned: always
        type: string
        sample: test
'''


from ansible.module_utils.basic import AnsibleModule

from ansible_collections.fujitsu.ansible.plugins.module_utils.irmc import irmc_redfish_get, get_irmc_json


def irmc_getvirtualmedia(module):
    result = dict(
        changed=False,
        status=0
    )

    if module.check_mode:
        result['msg'] = "module was not run"
        module.exit_json(**result)

    # get iRMC system data
    status, sysdata, msg = irmc_redfish_get(module, "redfish/v1/Systems/0/")
    if status < 100:
        module.fail_json(msg=msg, status=status, exception=sysdata)
    elif status != 200:
        module.fail_json(msg=msg, status=status)

    # Evaluate VM connection state
    vm_type = module.params['vm_type'].replace("Image", "")
    allowedparams = \
        get_irmc_json(sysdata.json(),
                      ["Actions", "Oem",
                       "http://ts.fujitsu.com/redfish-schemas/v1/FTSSchema.v1_0_0#FTSComputerSystem.VirtualMedia",
                       "VirtualMediaAction@Redfish.AllowableValues"])

    # determine current connection state
    vmdict = dict()
    if "Connect" + vm_type not in allowedparams:
        if "Disconnect" + vm_type not in allowedparams:
            vmdict[module.params['vm_type']] = "NotConfigured"
        else:
            vmdict[module.params['vm_type']] = "Connected"
    else:
        vmdict[module.params['vm_type']] = "Disconnected"

    # eet iRMC Virtual Media data
    status, vmdata, msg = irmc_redfish_get(module, "redfish/v1/Systems/0/Oem/ts_fujitsu/VirtualMedia/")
    if status < 100:
        module.fail_json(msg=msg, status=status, exception=vmdata)
    elif status != 200:
        module.fail_json(msg=msg, status=status)

    # extract specified Virtual Media data
    remotemountenabled = get_irmc_json(vmdata.json(), "RemoteMountEnabled")
    if not remotemountenabled:
        vmdict['remote_mount_disabled'] = "Remote Mount of Virtual Media is not enabled!"
    vmdict['usb_attach_mode'] = get_irmc_json(vmdata.json(), "UsbAttachMode")
    vmdict['bootsource'] = get_irmc_json(sysdata.json(), ["Boot", "BootSourceOverrideTarget"])
    vmdict['bootoverride'] = get_irmc_json(sysdata.json(), ["Boot", "BootSourceOverrideEnabled"])
    vmdict['bootmode'] = get_irmc_json(sysdata.json(), ["Boot", "BootSourceOverrideMode"])
    maxdevno = get_irmc_json(vmdata.json(), [module.params['vm_type'], "MaximumNumberOfDevices"])
    if maxdevno == 0:
        vmdict['no_vm_configured'] = "No Virtual Media of Type '" + module.params['vm_type'] + \
                                     "' is configured!"
    else:
        vmdict['image_name'] = get_irmc_json(vmdata.json(), [module.params['vm_type'], "ImageName"])
        vmdict['server'] = get_irmc_json(vmdata.json(), [module.params['vm_type'], "Server"])
        vmdict['share_name'] = get_irmc_json(vmdata.json(), [module.params['vm_type'], "ShareName"])
        vmdict['share_type'] = get_irmc_json(vmdata.json(), [module.params['vm_type'], "ShareType"])
        vmdict['user_domain'] = get_irmc_json(vmdata.json(), [module.params['vm_type'], "UserDomain"])
        vmdict['user_name'] = get_irmc_json(vmdata.json(), [module.params['vm_type'], "UserName"])
    result['virtual_media_data'] = vmdict
    module.exit_json(**result)


def main():
    # import pdb; pdb.set_trace()
    module_args = dict(
        irmc_url=dict(required=True, type="str"),
        irmc_username=dict(required=True, type="str"),
        irmc_password=dict(required=True, type="str", no_log=True),
        validate_certs=dict(required=False, type="bool", default=True),
        vm_type=dict(required=False, type="str", default="CDImage", choices=['CDImage', 'FDImage', 'HDImage']),
    )
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    irmc_getvirtualmedia(module)


if __name__ == '__main__':
    main()
