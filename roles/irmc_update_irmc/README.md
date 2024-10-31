irmc_update_irmc
================

Update iRMC firmware on iRMC devices.

**WARNING**:
This role turns off the iRMC device.
Please be careful when the OS is running.

**WARNING**:
The iRMC will automatically reboot after the firmware update is complete.
However, the completion of the reboot may not be detected correctly,
which may result in an error due to a timeout.  
It is **NOT RECOMMENDED** to use this role in a playbook with other roles and tasks.

Follow the steps below to get iRMC firmware (`*.bin`, `*.bin_enc`, `*.ima` or `*.ima_enc`) for your model:

1. <https://support.ts.fujitsu.com/index.asp?lng=us>
2. Select a new Product > Automatic Product Detection > Serial-/ident number
3. Serial-/ident number: `<SerialNumber>`(*1)
4. (If this is shown) Downloads > Continue
5. Selected operating system: OS Independent (BIOS, Firmware, etc.)
6. Driver > Server Management Controller > "*** Firmware Update for TFTP Flash" > Direct download

*1: The serial number can be found in the `System Information` at `https://{irmc-ipaddress}/system`.

Requirements
------------

None

Role Variables
--------------

| Name | Required | Default Value | Choices | Type | Description |
|------|----------|---------------|---------|------|-------------|
| `irmc_firmware_path` | false | | | str | Path to the firmware.<br/>Specified as absolute path or relative from the playbook.<br/>If `tftp_server` is specified, it is specified as a path from the root of the TFTP server.<br/>If `irmc_firmware_path_mapping` does not have a key corresponding to the model name, this value is applied. |
| `irmc_firmware_path_mapping` | false | | | dict | Mapping of paths to the firmware with the model name of the target node (e.g. `"PRIMERGY_RX1330_M6S"`) as key.<br/>The specification of the path description is the same as the parameter `irmc_firmware_path`.<br/>If there is no key corresponding to the model name and the parameter `irmc_firmware_path` is not specified, an error is raised. |
| `tftp_server` | false(*2) | | | str | IP address or hostname of the TFTP server from which to download the firmware.<br/>If not specified, the path is assumed to be the file system of the Ansible control node. |
| `timeout` | false | 1800 | | int | Timeout for the update process (seconds).<br/>However, only Ansible tasks are interrupted by timeouts, and update tasks that have started executing on the target node are not stopped. |
| `destination` | true | | "low" or 1, "high" or 2 | str or int | Specify the destination to which the firmware will be written.<br/>After the update is complete, the iRMC will reboot from this destination. |

*2: The parameter `tftp_server` is optional, but if you do not specify it and perform an update from the local file system, the parameter `destination` will not work correctly.

Dependencies
------------

None

Example Playbook
----------------

- **WARNING**: (DOES NOT WORK AS EXPECTED) To update with specified firmware from local file system:

  ```yaml
  ---
  - hosts: iRMC_group
    connection: local
    gather_facts: false
    roles:
      - role: fujitsu.primergy.irmc_update_irmc
        vars:
          irmc_firmware_path: "/any/where/firm/RX1330_M6/irmc/FTS_PRIMERGYRX1330M6iRMC253SSDR227.BIN"
          destination: low
  ```

- To update with specified firmware via tftp server:

  ```yaml
  ---
  - hosts: iRMC_group
    connection: local
    gather_facts: false
    roles:
      - role: fujitsu.primergy.irmc_update_irmc
        vars:
          tftp_server: 192.0.2.1
          irmc_firmware_path: "RX1330_M6/irmc/FTS_PRIMERGYRX1330M6iRMC253SSDR227.BIN"
          destination: low
  ```

- When updating with firmware for each model name via a TFTP server:

  ```yaml
  ---
  - hosts: iRMC_group
    connection: local
    gather_facts: false
    roles:
      - role: fujitsu.primergy.irmc_update_irmc
        vars:
          tftp_server: 192.0.2.1
          irmc_firmware_path_mapping:
            PRIMERGY_RX1330_M5R: "RX1330_M5R/irmc/FTS_PRIMERGYRX1330M5iRMC124SSDR341.BIN"
            PRIMERGY_RX1330_M6S: "RX1330_M6/irmc/FTS_PRIMERGYRX1330M6iRMC253SSDR227.BIN"
          destination: high
  ```

- inventory.ini:

  ```ini
  [iRMC_group]
  192.0.2.101 irmc_user=admin irmc_password=SECRET
  192.0.2.102 irmc_user=admin irmc_password=SECRET

  [iRMC_group:vars]
  validate_certificate=false  # When iRMC deivce is operated without a server certificate
  ```

License
-------

GPL-3.0-or-later

Author Information
------------------

- Yutaka Kamioka <yutaka.kamioka@jp.fujitsu.com>
