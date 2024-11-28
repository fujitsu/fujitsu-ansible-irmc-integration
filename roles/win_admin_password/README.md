win_admin_password
==================

Change the password for Administrator in Windows Server.

Requirements
------------

This role depends on the following Ansible collections:

- `ansible.windows` >= 1.14.0

Role Variables
--------------

| Name | Required | Default Value | Choices | Type | Description |
|------|----------|---------------|---------|------|-------------|
| `password` | true | | | str | Administrator password |

Dependencies
------------

None

Example Playbook
----------------

    ---
    - hosts: windows
      roles:
        - role: fujitsu.primergy.win_admin_password
          vars:
            password: NewP@ssw0rd

License
-------

GPL-3.0-or-later

Author Information
------------------

- Yutaka Kamioka <yutaka.kamioka@jp.fujitsu.com>
