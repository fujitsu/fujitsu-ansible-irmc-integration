#!/usr/bin/python

# Copyright 2018-2024 Fsas Technologies Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


DOCUMENTATION = r'''
---
module: irmc_certificate

short_description: manage iRMC certificates

description:
    - Ansible module to manage iRMC certificates via iRMC remote scripting interface.
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
        description: |
            Get or set iRMC certificate(s).
            If you update the certificate with "set", you must restart the iRMC.
        required:    false
        default:     get
        choices:     ['get', 'set']
    private_key_path:
        description: |
            Path to file containing SSL private key.
            This option also requires the SSL certificate.
            Important: Private keys created with openssl 3.x cannot be registered.
            To register, the header and footer must be rewritten to openssl 1.x format.
            (ex. Rewrite header “-----BEGIN PRIVATE KEY-----” to “-----BEGIN RSA PRIVATE KEY-----”)
        required:    false
    ssl_cert_path:
        description: Path to file containing SSL certificate.
                     This option also requires the SSL private key.
        required:    false
    ssl_ca_cert_path:
        description: Path to file containing SSL CA certificate.
        required:    false

notes:
    - See https://sp.ts.fujitsu.com/dmsp/Publications/public/dp-svs-configuration-space-values-en.pdf
'''

EXAMPLES = r'''
- name: Get and show SSL certificates
  tags:
    - get
  block:
    - name: Get SSL certificates
      irmc_certificate:
        irmc_url: "{{ inventory_hostname }}"
        irmc_username: "{{ irmc_user }}"
        irmc_password: "{{ irmc_password }}"
        validate_certs: "{{ validate_certificate }}"
        command: "get"
      register: certificates
      delegate_to: localhost
    - name: Show SSL certificates
      ansible.legacy.debug:
        var: certificates.certificates

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
  tags:
    - set
'''

RETURN = r'''
details:
    description: >
        If command is “get”, the following values are returned.
        For other commands,
        the default return value of Ansible (changed, failed, etc.) is returned.
    type: dict
    contains:
        ssl_certificate:
            description: SSL certificate
            returned: always
            type: string
        ssl_ca_certificate:
            description: SSL CA certificate
            returned: always
            type: string
'''


from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.irmc_scci_utils import get_scciresultlist, irmc_scci_post, setup_commandlist, setup_datadict

param_scci_map = [
    # Param, SCCI Name, SCCI Code, index, value dict
    ['private_key_path', 'ConfBMCSslPrivateKey', 0x1981, 0, None],
    ['ssl_cert_path', 'ConfBMCSslCertificate', 0x1982, 0, None],
    ['ssl_ca_cert_path', 'ConfBMCSslCaCertificate', 0x1983, 0, None],
]


# Global
result = dict()


def irmc_certificate(module: AnsibleModule):
    # initialize result
    result['changed'] = False
    result['status'] = 0

    if module.check_mode:
        result['msg'] = 'module was not run'
        module.exit_json(**result)

    certdata, setparam_count = setup_datadict(module, False)

    # parameter check
    if module.params['command'] == 'set':
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

    if module.params['command'] == 'set':
        body = setup_commandlist(certdata, 'SET', param_scci_map)
    else:
        body = setup_commandlist(certdata, 'GET', param_scci_map)

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

    if module.params['command'] == 'get':
        result['certificates'] = setup_resultdata(certdata)
    else:
        result['changed'] = True

    module.exit_json(**result)


def check_parameters(module: AnsibleModule, certdata, setparam_count) -> None:
    if setparam_count == 0:
        result['msg'] = "Command 'set' requires at least one parameter to be set!"
        result['status'] = 10
        module.fail_json(**result)

    if certdata['private_key_path'] is not None and certdata['ssl_cert_path'] is None or \
       certdata['ssl_cert_path'] is not None and certdata['private_key_path'] is None:
        result['msg'] = "Both 'private_key_path' and 'ssl_cert_path' are required to successfully " + \
                        'import SSL key pair!'
        result['status'] = 11
        module.fail_json(**result)


def read_keyfile(data, param):
    context = cert = ''
    retcode = 0
    if data[param] != '':
        try:
            f = open(data[param])
            cert = f.read()
        except Exception as e:
            retcode = 89
            context = f"Could not read key/certificate file at '{data[param]}': {e!s}"
        data[param] = cert

    return data, retcode, context


def setup_resultdata(data):
    data = {
        'ssl_certificate': data['ssl_cert_path'],
        'ssl_ca_certificate': data['ssl_ca_cert_path'],
    }
    return data


def main() -> None:
    # breakpoint()
    module_args = dict(
        irmc_url=dict(required=True, type='str'),
        irmc_username=dict(required=True, type='str'),
        irmc_password=dict(required=True, type='str', no_log=True),
        validate_certs=dict(required=False, type='bool', default=True),
        command=dict(required=False, type='str', default='get', choices=['get', 'set']),
        private_key_path=dict(required=False, type='str'),
        ssl_cert_path=dict(required=False, type='str'),
        ssl_ca_cert_path=dict(required=False, type='str'),
    )
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False,
    )

    irmc_certificate(module)


if __name__ == '__main__':
    main()
