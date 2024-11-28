win_set_rdp
===========

Enable/disable remote desktop.

Requirements
------------

This role depends on the following Ansible collections:

- `ansible.windows` >= 1.14.0

Role Variables
--------------

| Name | Required | Default Value | Choices | Type | Description |
|------|----------|---------------|---------|------|-------------|
| `enabled` | true | | true<br>false | boolean | Enable/disable remote desktop. |

Dependencies
------------

None

Example Playbook
----------------

playbook.yml:

    ---
    - name: Enable remote desktop
      hosts: windows
      roles:
        - role: fujitsu.primergy.win_set_rdp
          vars:
            enabled: true

License
-------

GPL-3.0-or-later

Author Information
------------------

- Jiajun Guo <guo.jiajun@fujitsu.com>
