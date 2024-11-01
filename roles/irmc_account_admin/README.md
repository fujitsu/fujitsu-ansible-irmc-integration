irmc_account_admin
==================

Change admin configurations.

Requirements
------------

None

Role Variables
--------------

| Name | Required | Default Value | Choices | Type | Description |
|------|----------|---------------|---------|------|-------------|
| `password` | false | | | str | User account password. |
| `irmc_account_admin.description` | false | | | str | User account desciption. |
| `irmc_account_admin.access.redfish.enable` | false | | | bool | User may use iRMC Redfish interface. |
| `irmc_account_admin.access.redfish.role` | false | | `Administrator` <br> `Operator` <br> `ReadOnly` | str | User account Redfish role. |
| `irmc_account_admin.access.ipmi.lan_privilege` | false | | `User` <br> `Operator` <br> `Administrator` <br> `OEM` | str | IPMI LAN channel privilege. |
| `irmc_account_admin.access.ipmi.serial_privilege` | false | | `User` <br> `Operator` <br> `Administrator` <br> `OEM` | str | IPMI serial channel privilege. |
| `irmc_account_admin.access.ipmi.enable_user_account_conf` | false | | | bool | User may configure user accounts. |
| `irmc_account_admin.access.ipmi.enable_irmc_settings_conf` | false | | | bool | User may configure iRMC settings. |
| `irmc_account_admin.access.avr.enable_avr` | false | | | bool | User may use Advanved Video Redirection (AVR). |
| `irmc_account_admin.access.avr.enable_remote_storage` | false | | | bool | User may use Remote Storage. |
| `irmc_account_admin.snmpv3.enable` | false | | | bool | User may use SNMPv3. |
| `irmc_account_admin.email.general.enable` | false | | | bool | Alert email enabled. |
| `irmc_account_admin.email.general.format` | false | | `Standard` <br> `Fixed Subject` <br> `ITS-Format` <br> `SMS` | str | Alert email format. |
| `irmc_account_admin.email.general.server` | false | | `Automatic` <br> `Primary` <br> `Secondary` | str | Preferred mail server for alert email. |
| `irmc_account_admin.email.general.address` | false | | | str | Alert email address. |
| `irmc_account_admin.email.alert.fan` | false | | `None` <br> `Critical` <br> `Warning` <br> `All` | str | Define alert level for fan sensors. |
| `irmc_account_admin.email.alert.temperature` | false | | `None` <br> `Critical` <br> `Warning` <br> `All` | str | Define alert level for temperature sensors. |
| `irmc_account_admin.email.alert.hardware_error` | false | | `None` <br> `Critical` <br> `Warning` <br> `All` | str | Define alert level for critical hardware errors. |
| `irmc_account_admin.email.alert.system_hang` | false | | `None` <br> `Critical` <br> `Warning` <br> `All` | str | Define alert level for system hang. |
| `irmc_account_admin.email.alert.post_error` | false | | `None` <br> `Critical` <br> `Warning` <br> `All` | str | Define alert level for POST errors. |
| `irmc_account_admin.email.alert.security` | false | | `None` <br> `Critical` <br> `Warning` <br> `All` | str | Define alert level for security. |
| `irmc_account_admin.email.alert.status` | false | | `None` <br> `Critical` <br> `Warning` <br> `All` | str | Define alert level for system status. |
| `irmc_account_admin.email.alert.disk` | false | | `None` <br> `Critical` <br> `Warning` <br> `All` | str | Define alert level for disk drivers & controllers. |
| `irmc_account_admin.email.alert.network` | false | | `None` <br> `Critical` <br> `Warning` <br> `All` | str | Define alert level for network interface. |
| `irmc_account_admin.email.alert.remote` | false | | `None` <br> `Critical` <br> `Warning` <br> `All` | str | Define alert level for remote management. |
| `irmc_account_admin.email.alert.power` | false | | `None` <br> `Critical` <br> `Warning` <br> `All` | str | Define alert level for system power. |
| `irmc_account_admin.email.alert.memory` | false | | `None` <br> `Critical` <br> `Warning` <br> `All` | str | Define alert level for memory. |
| `irmc_account_admin.email.alert.other` | false | | `None` <br> `Critical` <br> `Warning` <br> `All` | str | Define alert level for other. |

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
        - irmc_account_admin
      vars_files:
        - ./vars/secrets.yml
        - ./vars/vars.yml

secrets.yml

    password: P@ssw0rd

vars.yml:

    irmc_account_admin:
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
