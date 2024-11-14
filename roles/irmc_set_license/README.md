irmc_set_license
================

Set license keys for iRMC.

Requirements
------------

None

Role Variables
--------------

| Name | Required | Default Value | Choices | Type | Description |
|------|----------|---------------|---------|------|-------------|
| `license_keys` | true | | | list | iRMC license keys to be set. |

Dependencies
------------

None

Example Playbook
----------------

playbook.yml:

    ---
    - name: Set iRMC license key
      connection: local
      hosts: iRMC_group
      gather_facts: false
      roles:
        - role: fujitsu.primergy.irmc_set_license
          vars:
            license_keys:
              - "AAAAAA-AAAAAAA-AAAAA"
              - "BBBBBB-BBBBBBB-BBBBB"

License
-------

GPL-3.0-or-later

Author Information
------------------

- Jiajun Guo <guo.jiajun@fujitsu.com>
