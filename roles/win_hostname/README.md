win_hostname
============

Change the hostname of Windows Server.

Note:  
If computer has joined a domain, hostname cannot be changed by this role.

Requirements
------------

This role depends on the following Ansible collections:

- `ansible.windows` >= 2.5.0

Role Variables
--------------

| Name | Required | Default Value | Choices | Type | Description |
|------|----------|---------------|---------|------|-------------|
| `hostname` | true | | | str | Hostname of Windows Server |

Dependencies
------------

None

Example Playbook
----------------

    ---
    - hosts: windows
      roles:
        - role: fujitsu.primergy.win_hostname
          vars:
            hostname: Hostname

License
-------

GPL-3.0-or-later

Author Information
------------------

- Tomohisa Nakai <nakai.tomohisa@fujitsu.com>
