win_organization_owner
======================

Change the organization and owner of Windows Server.

Notes:  
This role sets Windows license organization and owner.  
Lisence information can be viewed by `systeminfo` or `winver` commands in Windows Power Shell.

Requirements
------------

This role depends on the following Ansible collections:

- `community.windows` >= 2.3.0

Role Variables
--------------

| Name | Required | Default Value | Choices | Type | Description |
|------|----------|---------------|---------|------|-------------|
| `organization` | true | | | str | Organization that Windows is licensed to. |
| `owner` | true | | | str | Persona that Windows is licensed to. |

Dependencies
------------

None

Example Playbook
----------------

    ---
    - hosts: windows
      roles:
        - role: win_organization_owner
      vars:
        organization: Fsas Technologies Inc.
        owner: MyOwnerName

License
-------

GPL-3.0-or-later

Author Information
------------------

- Tomohisa Nakai <nakai.tomohisa@fujitsu.com>
