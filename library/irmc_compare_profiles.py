#!/usr/bin/python

# Copyright 2018-2024 Fsas Technologies Inc.
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
module: irmc_compare_profiles

short_description: compare two iRMC profiles

description:
    - Ansible module to compare two iRMC profiles.
    - Module Version V1.2.

requirements:
    - The module needs to run locally.
    - iRMC S4 needs FW >= 9.04, iRMC S5 needs FW >= 1.25.
    - Python >= 2.6
    - Python module 'future'

version_added: "2.4"

author:
    - Nakamura Takayuki (@nakamura-taka)

options:
    profile_json1:
        description: iRMC profile to be compared against another.
                     Takes precedence over profile_path1 when set.
        required:    false
    profile_json2:
        description: iRMC profile to be compared against another.
                     Takes precedence over profile_path2 when set.
        required:    false
    profile_path1:
        description: Path to file with iRMC profile to be compared against another.
                     Ignored if profile1 is set.
        required:    false
    profile_path2:
        description: Path to file with iRMC profile to be compared against another.
                     Ignored if profile2 is set.
        required:    false
'''

EXAMPLES = '''
# Compare iRMC profiles against each other
- name: Compare iRMC profiles
  irmc_compare_profiles:
    profile_path1: "{{ profile1_path }}"
    profile_path2: "{{ profile2_path }}"
  delegate_to: localhost
'''

RETURN = '''
    comparison_result:
        description: profile comparison result
        returned: always
        type: bool
        sample: False
    comparison_list:
        description: rudimentary list of probable comparison differences
        returned: when comparison_result is False
        type: list
'''


from builtins import str

import json
from ansible.module_utils.basic import AnsibleModule

from ansible.module_utils.irmc_utils import compare_irmc_profile


def irmc_compare_profiles(module):
    result = dict(
        changed=False,
        status=0
    )

    if module.check_mode:
        result['msg'] = "module was not run"
        module.exit_json(**result)

    # preliminary parameter check
    if module.params['profile_path1'] is None and module.params['profile_json1'] is None:
        module.fail_json(msg="Either 'profile_json1' or 'profile_path1' needs to be set.", status=10)
    if module.params['profile_path2'] is None and module.params['profile_json2'] is None:
        module.fail_json(msg="Either 'profile_json2' or 'profile_path2' needs to be set.", status=11)

    if module.params['profile_json1'] is not None:
        try:
            profile1 = json.loads(module.params['profile_json1'])
        except ValueError as e:
            module.fail_json(msg="'profile_json1' is invalid JSON: {0}".
                             format(module.params['profile_json1']), status=12)
    else:
        try:
            with open(module.params['profile_path1']) as profile1_str:
                profile1 = json.load(profile1_str)
        except Exception as e:
            module.fail_json(msg="Could not read 'profile_path1' at '{0}': {1}".
                             format(module.params['profile_path1'], str(e)), status=13)

    if module.params['profile_json2'] is not None:
        try:
            profile2 = json.loads(module.params['profile_json2'])
        except ValueError as e:
            module.fail_json(msg="'profile_json2' is invalid JSON: {0}".
                             format(module.params['profile_json2']), status=14)
    else:
        try:
            with open(module.params['profile_path2']) as profile2_str:
                profile2 = json.load(profile2_str)
        except Exception as e:
            module.fail_json(msg="Could not read 'profile_path2 at '{0}': {1}".
                             format(module.params['profile_path2'], str(e)), status=15)

    comparison_result, comparison_list = compare_irmc_profile(profile1, profile2)
    result['comparison_result'] = comparison_result
    if comparison_result is False:
        result['comparison_list'] = comparison_list

    module.exit_json(**result)


def main():
    # import pdb; pdb.set_trace()
    module_args = dict(
        profile_json1=dict(required=False, type="json"),
        profile_json2=dict(required=False, type="json"),
        profile_path1=dict(required=False, type="str"),
        profile_path2=dict(required=False, type="str")
    )
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    irmc_compare_profiles(module)


if __name__ == '__main__':
    main()
