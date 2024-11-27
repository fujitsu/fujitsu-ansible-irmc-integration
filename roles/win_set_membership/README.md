win_set_membership
====================

Join host to workgroup or Domain.

Requirements
------------

This role depends on the following Ansible collections:

- `microsoft.ad` >= 1.4.1

Domain controller exists when joining host to Domain.

Role Variables
--------------

| Name | Required | Default Value | Choices | Type | Description |
|------|----------|---------------|---------|------|-------------|
| `state` | true | | `workgroup`, `domain` | str | Whether the target host should be a member of a domain or workgroup. |
| `workgroup` | false | | | str | This is the name of the workgroup that the Windows host should be in.<br> When `state`=`workgroup`, this must be set. |
| `domain` | false | | | str | This is the dns name of the domain to which the targeted Windows host should be joined.<br> When `state`=`domain`, this must be set. |
| `username` | false | | | str | Username of a domain user for the target domain.<br> When `state`=`domain` or to join workgroup from a domain, this must be set.  |
| `password` | false | | | str | Password for the specified `username`.<br> When `state`=`domain` or to join workgroup from a domain, this must be set. |

Dependencies
------------

None

Example Playbook
----------------

playbook.yml(join workgroup):

    ---
    - name: Join a workgroup
      hosts: windows
      roles:
        - role: fujitsu.primergy.win_set_membership
          vars:
            state: workgroup
            workgroup: WORKGROUP

playbook.yml(join a domain):

    ---
    - name: Join a domain
      hosts: windows
      roles:
        - role: fujitsu.primergy.win_set_membership
          vars:
            state: domain
            domain: fti.test
            username: FTI\Administrator
            password: Admin000

License
-------

GPL-3.0-or-later

Author Information
------------------

- Jiajun Guo <guo.jiajun@fujitsu.com>
