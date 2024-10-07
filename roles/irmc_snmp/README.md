irmc_snmp
=========

Configure SNMP settings for iRMC devices.

Requirements
------------

None

Role Variables
--------------

| Name | Required | Default Value | Choices | Type | Description |
|------|----------|---------------|---------|------|-------------|
| `snmp.enabled` | false | true | | bool | Enable SNMP |
| `snmp.service_port` | false | | | int | SNMP Port |
| `snmp.protocol` | false | | "All", "V3only" | str | SNMP Protocol<br/> "All" means SNMPv1/v2c/v3|
| `snmp.community_name` | false | | | | SNMPv1/v2c Community name |
| `snmp_trap_destination.community_name` | false | | | str | SNMP Community name|
| `snmp_trap_destination.engine_id` | false | | | str | Engine ID |
| `snmp_trap_destination.servers[].index` | true | | 0 to 6 | int | A total of seven trap destinations can be set. |
| `snmp_trap_destination.servers[].name` | true | | | str | Hostname or IPaddress<br> Disabled if an empty string is specified. |
| `snmp_trap_destination.servers[].protocol` | true | | "SnmpV1", "SnmpV2c" | str | SNMP Protocol |

Dependencies
------------

None

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

    - hosts: iRMC_group
      connection: local
      gather_facts: false
      vars_files:
        - ./vars.yml
      roles:
        - role: irmc_snmp

vars.yml:

      snmp:
        enabled: true
        protocol: "All"  # "All" or "V3only"
        community_name: "public"

      snmp_trap_destination:
        community_name: "trap-public"
        servers:
          - index: 0
            name: "Destination1"
            protocol: "SnmpV2c"
          - index: 1
            name: ""
            protocol: "SnmpV1"

License
-------

GPL-3.0-or-later

Author Information
------------------

- Yutaka Kamioka <yutaka.kamioka@jp.fujitsu.com>
