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
| `agent.contact` | true | | | str | Contact name of the managed node and information on how to contact. |
| `agent.location` | true | | | str | Physical location of the managed node. |
| `agent.service` | true | | | int | Any combination of up to five SNMP services. <br> The integer value is derived from the following binary values: <br> <ul> <li>Physical: 0x01</li> <li>DataLink and Subnet: 0x02</li> <li>Internet: 0x04</li> <li>End-to-end: 0x08</li> <li>Application: 0x40</li> </ul> Ex: A combination of "Internet", "End-to-end" and "Application" has a value of 0x4c (76) |
| `security.accepted_community` | true | | | str | Community name from which the computer running SNMP can accept SNMP requests such as GET, SET, GETNEXT, and GETBULK. <br> This parameter can be specified multiple in the Windows GUI, but only one can be specified in this role. |
| `security.accepted_community_permission` | true | | 0 <br> 2 <br> 4 <br> 8 <br> 16 | int | Type of permissions that the `security.accepted_community` has. <br> <ul> <li>0: no permission</li> <li>2: notify permission</li> <li>4: read-only permission</li> <li>8: read/write permission</li> <li>16: read/create permission</li> </ul> |
| `security.accepted_host` | false | | | str | IP address or computer name of the host accepting SNMP packets. <br> This parameter can be specified multiple in the Windows GUI, but only one can be specified in this role.  |
| `security.send_auth_trap` | true | | true <br> false | bool | Whether to send an authentication trap when an unauthorized community or host requests information. |
| `trap.community` | true | | | str | Community name to which SNMP sends traps. <br> This parameter can be specified multiple in the Windows GUI, but only one can be specified in this role. |
| `trap.destination` | true | | | str | IP address or computer name to which SNMP sends traps. <br> This parameter can be specified multiple in the Windows GUI, but only one can be specified in this role. |

Dependencies
------------

None

Example Playbook
----------------

    ---
    - hosts: windows
      roles:
        - role: fujitsu.primergy.win_snmp
          vars:
            agent:
              contact: MyContact
              location: MyLocation
              service: 76
            security:
              accepted_community: public
              accepted_community_permission: 8
              send_auth_trap: true
            trap:
              community: public
              destination: 192.0.2.1

License
-------

GPL-3.0-or-later

Author Information
------------------

- Tomohisa Nakai <nakai.tomohisa@fujitsu.com>
