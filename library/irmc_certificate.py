#!/usr/bin/python

# FUJITSU Limited
# Copyright (C) FUJITSU Limited 2018
# GNU General Public License v3.0+ (see LICENSE.md or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division)
__metaclass__ = type


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}


DOCUMENTATION = '''
---
module: irmc_certificate

short_description: manage iRMC certificates

description:
    - Ansible module to manage iRMC certificates via iRMC remote scripting interface.
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
        description: get or set iRMC certificate(s)
        required:    false
        default:     get
        choices:     ['get', 'set']
    private_key_path:
        description: path to file containing SSL private key;
                     this option also requires the SSL certificate
        required:    false
    ssl_cert_path:
        description: path to file containing SSL certificate;
                     this option also requires the SSL private key
        required:    false
    ssl_ca_cert_path:
        description: path to file containing SSL CA certificate
        required:    false

notes:
    - See http://manuals.ts.fujitsu.com/file/12563/wp-svs-irmc-remote-scripting-en.pdf
    - See https://sp.ts.fujitsu.com/dmsp/Publications/public/dp-svs-configuration-space-values-en.pdf
'''

EXAMPLES = '''
# Get SSL certificates
- name: Get SSL certificates
  irmc_certificate:
    irmc_url: "{{ inventory_hostname }}"
    irmc_username: "{{ irmc_user }}"
    irmc_password: "{{ irmc_password }}"
    validate_certs: "{{ validate_certificate }}"
    command: "get"
  register: certificates
  delegate_to: localhost
- name: show certificates
  debug:
    msg: "{{ certificates.certificates }}"

# Set SSL certificates
- name: Set SSL certificates
  irmc_certificate:
    irmc_url: "{{ inventory_hostname }}"
    irmc_username: "{{ irmc_user }}"
    irmc_password: "{{ irmc_password }}"
    validate_certs: "{{ validate_certificate }}"
    command: "set"
    private_key_path: "{{ private_key_path }}"
    ssl_cert_path: "{{ ssl_cert_path }}"
    ssl_ca_cert_path: "{{ ssl_ca_cert_path }}"
  delegate_to: localhost
'''

RETURN = '''
certificates:
    description: SSL certificates
    returned: always
    type: dict
'''


# pylint: disable=wrong-import-position
from ansible.module_utils.basic import AnsibleModule

from ansible.module_utils.irmc_scci_utils import get_scciresultlist, irmc_scci_post, add_scci_command, \
                                                 scci_body_start, scci_body_end


param_scci_map = [
    # Param, SCCI Name, SCCI Code, value dict
    ["private_key_path", "ConfBMCSslPrivateKey", 0x1981, None],
    ["ssl_cert_path", "ConfBMCSslCertificate", 0x1982, None],
    ["ssl_ca_cert_path", "ConfBMCSslCaCertificate", 0x1983, None],
]


def irmc_certificate(module):        # pylint: disable=too-many-branches
    result = dict(
        changed=False,
        status=0
    )

    if module.check_mode:
        result['msg'] = "module was not run"
        module.exit_json(**result)

    certdata, setparam_count = setup_datadict(module)

    # parameter check
    if module.params['command'] == "set":
        if setparam_count == 0:
            result['msg'] = "Command 'set' requires at least one parameter to be set!"
            module.fail_json(**result)

        if certdata['private_key_path'] is not None and certdata['ssl_cert_path'] is None or \
           certdata['ssl_cert_path'] is not None and certdata['private_key_path'] is None:
            result['msg'] = "Both 'private_key_path' and 'ssl_cert_path' are required to successfully " + \
                            "import SSL key pair!"
            module.fail_json(**result)

        certdata, status, msg = read_keyfile(certdata, 'private_key_path')
        if status != 0:
            module.fail_json(msg=msg)
        certdata, status, msg = read_keyfile(certdata, 'ssl_cert_path')
        if status != 0:
            module.fail_json(msg=msg)
        certdata, status, msg = read_keyfile(certdata, 'ssl_ca_cert_path')
        if status != 0:
            module.fail_json(msg=msg)

    if module.params['command'] == "set":
        body = setup_commandlist(certdata, "SET", param_scci_map)
    else:
        body = setup_commandlist(certdata, "GET", param_scci_map)

    # send command list to scripting interface
    status, data, msg = irmc_scci_post(module, body)
    if status < 100:
        module.fail_json(msg=msg, exception=data)
    elif status != 200 and status != 204:
        module.fail_json(msg=msg, status=status)

    # evaluate results list
    certdata, scciresult, sccicontext = get_scciresultlist(data.content, certdata, param_scci_map)
    if scciresult != 0:
        result['msg'] = sccicontext
        module.fail_json(**result)

    if module.params['command'] == "get":
        result['certificates'] = setup_resultdata(certdata)
    else:
        result['changed'] = True

    module.exit_json(**result)


# we need our own function here as empty values are not allowed
def setup_datadict(module):
    spcount = 0
    datadict = dict()
    for key, value in module.params.iteritems():
        if key != "irmc_url" and key != "irmc_username" and key != "irmc_password" and \
           key != "validate_certs" and key != "command":
            if value is not None:
                if value != "":
                    spcount += 1
                else:
                    value = None
            datadict[key] = value

    return datadict, spcount


def read_keyfile(data, param):
    context = cert = ""
    result = 0
    if data[param] != "":
        try:
            f = open(data[param], 'r')
            cert = f.read()
        except Exception as e:    # pylint: disable=broad-except
            result = 89
            context = "Could not read key/certificate file at '{0}': {1}".format(data[param], str(e))
        data[param] = cert

    return data, result, context


def setup_commandlist(cmdlist, ctype, scci_map):
    body = scci_body_start
    for elem in scci_map:
        body += add_scci_command(ctype, scci_map, elem[1], 0, cmdlist[elem[0]])
    body += scci_body_end
    return body


def setup_resultdata(data):
    data = {
        'ssl_certificate': data['ssl_cert_path'],
        'ssl_ca_certificate': data['ssl_ca_cert_path'],
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
        private_key_path=dict(required=False, type="str"),
        ssl_cert_path=dict(required=False, type="str"),
        ssl_ca_cert_path=dict(required=False, type="str"),
    )
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    irmc_certificate(module)


if __name__ == '__main__':
    main()
