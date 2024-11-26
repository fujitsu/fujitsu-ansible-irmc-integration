irmc_account_admin
==================

Change admin configurations.

Note:  
At least one role variable must be set.

Requirements
------------

None

Role Variables
--------------

| Name | Required | Default Value | Choices | Type | Description |
|------|----------|---------------|---------|------|-------------|
| `password` | false | | | str | User account password. |
| `description` | false | | | str | User account desciption. |
| `access.redfish.enable` | false | | | bool | User may use iRMC Redfish interface. |
| `access.redfish.role` | false | | `Administrator`, <br> `Operator`, <br> `ReadOnly` | str | User account Redfish role. |
| `access.ipmi.lan_privilege` | false | | `User`, <br> `Operator`, <br> `Administrator`, <br> `OEM` | str | IPMI LAN channel privilege. |
| `access.ipmi.serial_privilege` | false | | `User`, <br> `Operator`, <br> `Administrator`, <br> `OEM` | str | IPMI serial channel privilege. |
| `access.ipmi.enable_user_account_conf` | false | | | bool | User may configure user accounts. |
| `access.ipmi.enable_irmc_settings_conf` | false | | | bool | User may configure iRMC settings. |
| `access.avr.enable_avr` | false | | | bool | User may use Advanved Video Redirection (AVR). |
| `access.avr.enable_remote_storage` | false | | | bool | User may use Remote Storage. |
| `snmpv3.enable` | false | | | bool | User may use SNMPv3. |
| `email.general.enable` | false | | | bool | Alert email enabled. |
| `email.general.format` | false | | `Standard`, <br> `Fixed Subject`, <br> `ITS-Format`, <br> `SMS` | str | Alert email format. |
| `email.general.server` | false | | `Automatic`, <br> `Primary`, <br> `Secondary` | str | Preferred mail server for alert email. |
| `email.general.address` | false | | | str | Alert email address. |
| `email.alert.fan` | false | | `None`, <br> `Critical`, <br> `Warning`, <br> `All` | str | Define alert level for fan sensors. |
| `email.alert.temperature` | false | | `None`, <br> `Critical`, <br> `Warning`, <br> `All` | str | Define alert level for temperature sensors. |
| `email.alert.hardware_error` | false | | `None`, <br> `Critical`, <br> `Warning`, <br> `All` | str | Define alert level for critical hardware errors. |
| `email.alert.system_hang` | false | | `None`, <br> `Critical`, <br> `Warning`, <br> `All` | str | Define alert level for system hang. |
| `email.alert.post_error` | false | | `None`, <br> `Critical`, <br> `Warning`, <br> `All` | str | Define alert level for POST errors. |
| `email.alert.security` | false | | `None`, <br> `Critical`, <br> `Warning`, <br> `All` | str | Define alert level for security. |
| `email.alert.status` | false | | `None`, <br> `Critical`, <br> `Warning`, <br> `All` | str | Define alert level for system status. |
| `email.alert.disk` | false | | `None`, <br> `Critical`, <br> `Warning`, <br> `All` | str | Define alert level for disk drivers & controllers. |
| `email.alert.network` | false | | `None`, <br> `Critical`, <br> `Warning`, <br> `All` | str | Define alert level for network interface. |
| `email.alert.remote` | false | | `None`, <br> `Critical`, <br> `Warning`, <br> `All` | str | Define alert level for remote management. |
| `email.alert.power` | false | | `None`, <br> `Critical`, <br> `Warning`, <br> `All` | str | Define alert level for system power. |
| `email.alert.memory` | false | | `None`, <br> `Critical`, <br> `Warning`, <br> `All` | str | Define alert level for memory. |
| `email.alert.other` | false | | `None`, <br> `Critical`, <br> `Warning`, <br> `All` | str | Define alert level for other. |

Dependencies
------------

None

Example Playbook
----------------

playbook.yml:

    ---
    - name: Change admin configurations
      connection: local
      hosts: iRMC_group
      gather_facts: false
      roles:
        - role: fujitsu.primergy.irmc_account_admin
          vars:
            password: P@ssw0rd
            description: my description
            access:
              redfish:
                enable: true
                role: Administrator
              ipmi:
                lan_privilege: OEM
                serial_privilege: Administrator
                enable_user_account_conf: true
                enable_irmc_settings_conf: true
              avr:
                enable_avr: true
                enable_remote_storage: true
            snmpv3:
              enable: true
            email:
              general:
                enable: true
                format: Standard
                server: Automatic
                address: User02@domain.com
              alert:
                fan: Warning
                temperature: Warning
                hardware_error: All
                system_hang: Critical
                post_error: All
                security: Warning
                status: None
                disk: Critical
                network: Warning
                remote: Critical
                power: Warning
                memory: Critical
                other: None

inventory.ini:

    [iRMC_group]
    192.0.2.99 irmc_user=admin irmc_password=SECRET

    [iRMC_group:vars]
    validate_certificate=false  # When iRMC deivce is operated without a server certificate

License
-------

GPL-3.0-or-later

Author Information
------------------

- Tomohisa Nakai <nakai.tomohisa@fujitsu.com>
