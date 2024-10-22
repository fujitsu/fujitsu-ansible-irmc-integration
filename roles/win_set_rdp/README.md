win_set_rdp
===========

Enable/disable remote desktop.

Requirements
------------

None

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
      gather_facts: false
      vars:
        enabled: true
      roles:
        - role: win_set_rdp

License
-------

GPL-3.0-or-later

Author Information
------------------

- Jiajun Guo <guo.jiajun@fujitsu.com>
