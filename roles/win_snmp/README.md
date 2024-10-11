win_snmp
========

Configure the SNMP Service in Windows Server.

Requirements
------------

This role depends on the following Ansible collections:

- `ansible.windows` >= 2.5.0
- `community.windows` >= 2.3.0

Role Variables
--------------

| Name | Required | Default Value | Choices | Type | Description |
|------|----------|---------------|---------|------|-------------|
| `authentication` | true | 1 | 0 <br> 1 | int | Whether to send an authentication trap when an unauthorized community or host requests information. <br> ● 0: false <br> ● 1: true |
| `community` | true | | | str | Name of the community to which SNMP sends traps. |
| `contact` | true | | | str | Contact name of the managed node and information on how to contact. |
| `destination` | true | | | str | IP address or computer name to which SNMP sends traps. |
| `location` | true | | | str | Physical location of the managed node. |
| `permitted_manager` | true | | | str | IP address or computer name of the host accepting SNMP packets. |
| `services` | true | 76 | | int | Any combination of up to five SNMP services. <br> The integer value is derived from the following binary values: <br> ● Physical: 0x01 <br> ● DataLink and Subnet: 0x02 <br> ● Internet: 0x04 <br> ● End-to-end: 0x08 <br> ● Application: 0x40 <br> Ex: A combination of "Internet", "End-to-end" and "Application" has a value of 0x4c (76) |
| `valid_community_name` | true | | | str | Community name from which the computer running SNMP can accept SNMP requests such as GET, SET, GETNEXT, and GETBULK. |
| `valid_community_permission` | true | | 0 <br> 2 <br> 4 <br> 8 <br> 16 | int | Type of permissions that the `valid_community_name` has. <br> ● 0: no permission <br> ● 2: notify permission <br> ● 4: read-only permission <br> ● 8: read/write permission <br> ● 16: read/create permission |

Dependencies
------------

None

Example Playbook
----------------

    ---
    - hosts: windows
      roles:
        - role: win_snmp
      vars:
        authentication: 1
        community: public
        contact: MyContact
        destination: 127.0.0.1
        location: MyLocation
        permitted_manager: MyPermittedManager
        services: 79
        valid_community_name: public
        valid_community_permission: 8

License
-------

GPL-3.0-or-later

Author Information
------------------

- Tomohisa Nakai <nakai.tomohisa@fujitsu.com>
