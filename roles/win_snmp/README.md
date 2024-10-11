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
| `agent_contact` | true | | | str | Contact name of the managed node and information on how to contact. |
| `agent_location` | true | | | str | Physical location of the managed node. |
| `agent_service` | true | | | int | Any combination of up to five SNMP services. <br> The integer value is derived from the following binary values: <br> ● Physical: 0x01 <br> ● DataLink and Subnet: 0x02 <br> ● Internet: 0x04 <br> ● End-to-end: 0x08 <br> ● Application: 0x40 <br> Ex: A combination of "Internet", "End-to-end" and "Application" has a value of 0x4c (76) |
| `security_accepted_community` | true | | | str | Community name from which the computer running SNMP can accept SNMP requests such as GET, SET, GETNEXT, and GETBULK. |
| `security_accepted_community_permission` | true | | 0 <br> 2 <br> 4 <br> 8 <br> 16 | int | Type of permissions that the `security_accepted_community` has. <br> ● 0: no permission <br> ● 2: notify permission <br> ● 4: read-only permission <br> ● 8: read/write permission <br> ● 16: read/create permission |
| `security_accepted_host` | true | | | str | IP address or computer name of the host accepting SNMP packets. |
| `security_send_auth_trap` | true | | true <br> false | bool | Whether to send an authentication trap when an unauthorized community or host requests information. |
| `trap_community` | true | | | str | Community name to which SNMP sends traps. |
| `trap_destination` | true | | | str | IP address or computer name to which SNMP sends traps. |

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
        agent_contact: MyContact
        agent_location: MyLocation
        agent_service: 79
        security_accepted_community: public
        security_accepted_community_permission: 8
        security_accepted_host: MyPermittedManager
        security_send_auth_trap: true
        trap_community: public
        trap_destination: 127.0.0.1

License
-------

GPL-3.0-or-later

Author Information
------------------

- Tomohisa Nakai <nakai.tomohisa@fujitsu.com>
