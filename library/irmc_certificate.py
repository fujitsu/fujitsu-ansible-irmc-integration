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
module: irmc_certificate

short_description: manage iRMC certificates

description:
    - Ansible module to manage iRMC certificates via iRMC remote scripting interface.
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
        description: Get or set iRMC certificate(s).
        required:    false
        default:     get
        choices:     ['get', 'set']
    private_key_path:
        description: Path to file containing SSL private key.
                     This option also requires the SSL certificate.
        required:    false
    ssl_cert_path:
        description: Path to file containing SSL certificate.
                     This option also requires the SSL private key.
        required:    false
    ssl_ca_cert_path:
        description: Path to file containing SSL CA certificate.
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
# Certificates returned by command "get":
    ssl_certificate:
        description: SSL certificate
        returned: always
        type: string
    ssl_ca_certificate:
        description: SSL CA certificate
        returned: always
        type: string

# For command "set":
    Default return values:
'''


from builtins import str

from ansible.module_utils.basic import AnsibleModule

from ansible.module_utils.irmc_scci_utils import get_scciresultlist, irmc_scci_post, setup_datadict, \
                                                 setup_commandlist


param_scci_map = [
    # Param, SCCI Name, SCCI Code, index, value dict
    ["private_key_path", "ConfBMCSslPrivateKey", 0x1981, 0, None],
    ["ssl_cert_path", "ConfBMCSslCertificate", 0x1982, 0, None],
    ["ssl_ca_cert_path", "ConfBMCSslCaCertificate", 0x1983, 0, None],
]


# Global
result = dict()


def irmc_certificate(module):
    # initialize result
    result['changed'] = False
    result['status'] = 0

    if module.check_mode:
        result['msg'] = "module was not run"
        module.exit_json(**result)

    certdata, setparam_count = setup_datadict(module, False)

    # parameter check
    if module.params['command'] == "set":
        check_parameters(module, certdata, setparam_count)

        certdata, status, msg = read_keyfile(certdata, 'private_key_path')
        if status != 0:
            module.fail_json(msg=msg, status=status)
        certdata, status, msg = read_keyfile(certdata, 'ssl_cert_path')
        if status != 0:
            module.fail_json(msg=msg, status=status)
        certdata, status, msg = read_keyfile(certdata, 'ssl_ca_cert_path')
        if status != 0:
            module.fail_json(msg=msg, status=status)

    if module.params['command'] == "set":
        body = setup_commandlist(certdata, "SET", param_scci_map)
    else:
        body = setup_commandlist(certdata, "GET", param_scci_map)

    # send command list to scripting interface
    status, data, msg = irmc_scci_post(module, body)
    if status < 100:
        module.fail_json(msg=msg, status=status, exception=data)
    elif status not in (200, 202, 204):
        module.fail_json(msg=msg, status=status)

    # evaluate results list
    certdata, scciresult, sccicontext = get_scciresultlist(data.content, certdata, param_scci_map)
    if scciresult != 0:
        module.fail_json(msg=sccicontext, status=scciresult)

    if module.params['command'] == "get":
        result['certificates'] = setup_resultdata(certdata)
    else:
        result['changed'] = True

    module.exit_json(**result)


def check_parameters(module, certdata, setparam_count):
    if setparam_count == 0:
        result['msg'] = "Command 'set' requires at least one parameter to be set!"
        result['status'] = 10
        module.fail_json(**result)

    if certdata['private_key_path'] is not None and certdata['ssl_cert_path'] is None or \
       certdata['ssl_cert_path'] is not None and certdata['private_key_path'] is None:
        result['msg'] = "Both 'private_key_path' and 'ssl_cert_path' are required to successfully " + \
                        "import SSL key pair!"
        result['status'] = 11
        module.fail_json(**result)


def read_keyfile(data, param):
    context = cert = ""
    retcode = 0
    if data[param] != "":
        try:
            f = open(data[param], 'r')
            cert = f.read()
        except Exception as e:
            retcode = 89
            context = "Could not read key/certificate file at '{0}': {1}".format(data[param], str(e))
        data[param] = cert

    return data, retcode, context


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
