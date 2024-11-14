win_organization_owner
======================

Change the description, organization and owner of Windows Server.

Requirements
------------

This role depends on the following Ansible collections:

- `community.windows` >= 2.3.0

Role Variables
--------------

| Name | Required | Default Value | Choices | Type | Description |
|------|----------|---------------|---------|------|-------------|
| `description` | false | | | str | Description of your machine. <br> It can be viewed by `net config server` command in Windows Power Shell. |
| `organization` | false | | | str | Organization that Windows is licensed to. <br> It can be viewed by `systeminfo` or `winver` commands in Windows Power Shell. |
| `owner` | false | | | str | Persona that Windows is licensed to. <br> It can be viewed by `systeminfo` or `winver` commands in Windows Power Shell. |

Dependencies
------------

None

Example Playbook
----------------

    ---
    - hosts: windows
      roles:
        - role: fujitsu.primergy.win_organization_owner
          vars:
            description: This is my Windows Server.
            organization: Fsas Technologies Inc.
            owner: MyOwnerName

License
-------

GPL-3.0-or-later

Author Information
------------------

- Tomohisa Nakai <nakai.tomohisa@fujitsu.com>
