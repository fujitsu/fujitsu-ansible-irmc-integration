irmc_update_bios
================

Update BIOS firmware on iRMC devices.

**WARNING**:
This role turns off the iRMC device.
Please be careful when the OS is running.

Follow the steps below to get BIOS firmware (`*.upc` or `*.upd`) for your model:

1. <https://support.ts.fujitsu.com/index.asp?lng=us>
2. Press "Select a new Product" button > Serial-/ident number
3. Serial-/ident number: `<SerialNumber>`(*1)
4. (If this is shown) Downloads > Continue
5. Selected operating system: OS Independent (BIOS, Firmware, etc.)
6. BIOS > "*** - Admin package - Compressed Flash Files" > Direct download
7. Extract the ZIP file and pick out the `*.upc` or `*.upd` file

*1: The serial number can be found in the `System Information` at `https://{irmc-ipaddress}/system`.

Requirements
------------

None

Role Variables
--------------

| Name | Required | Default Value | Choices | Type | Description |
|------|----------|---------------|---------|------|-------------|
| `bios_firmware_path` | false | | | str | Path to the firmware.<br/>Specified as absolute path or relative from the playbook.<br/>If `tftp_server` is specified, it is specified as a path from the root of the TFTP server.<br/>If `bios_firmware_path_mapping` does not have a key corresponding to the model name, this value is applied. |
| `bios_firmware_path_mapping` | false | | | dict | Mapping of paths to the firmware with the model name of the target node (e.g. `"PRIMERGY_RX1330_M6S"`) as key.<br/>The specification of the path description is the same as the parameter `bios_firmware_path`.<br/>If there is no key corresponding to the model name and the parameter `bios_firmware_path` is not specified, an error is raised. |
| `tftp_server` | false | | | str | IP address or hostname of the TFTP server from which to download the firmware.<br/>If not specified, the path is assumed to be the file system of the Ansible control node. |
| `timeout` | false | 1800 | | int | Timeout for the update process (seconds).<br/>However, only Ansible tasks are interrupted by timeouts, and update tasks that have started executing on the target node are not stopped. |

Dependencies
------------

None

Example Playbook
----------------

To update with specified firmware:

    ---
    - hosts: iRMC_group
      connection: local
      gather_facts: false
      roles:
        - role: fujitsu.primergy.irmc_update_bios
          vars:
            bios_firmware_path: "/any/where/firm/RX1330_M6/bios/D4133-A1x.R1.1.0.UPC"

When updating with firmware for each model name:

    ---
    - hosts: iRMC_group
      connection: local
      gather_facts: false
      roles:
        - role: fujitsu.primergy.irmc_update_bios
          vars:
            bios_firmware_path_mapping:
              PRIMERGY_RX1330_M5R: "/any/where/firm/RX1330_M5R/bios/D3929-A1x.R1.41.0.UPC"
              PRIMERGY_RX1330_M6S: "/any/where/firm/RX1330_M6/bios/D4133-A1x.R1.1.0.UPC"

When updating with firmware for each model name via a TFTP server:

    ---
    - hosts: iRMC_group
      connection: local
      gather_facts: false
      roles:
        - role: fujitsu.primergy.irmc_update_bios
          vars:
            tftp_server: 192.0.2.1
            bios_firmware_path_mapping:
              PRIMERGY_RX1330_M5R: "RX1330_M5R/bios/D3929-A1x.R1.41.0.UPC"
              PRIMERGY_RX1330_M6S: "RX1330_M6/bios/D4133-A1x.R1.1.0.UPC"

inventory.ini:

    [iRMC_group]
    192.0.2.101 irmc_user=admin irmc_password=SECRET
    192.0.2.102 irmc_user=admin irmc_password=SECRET

    [iRMC_group:vars]
    validate_certificate=false  # When iRMC deivce is operated without a server certificate

License
-------

GPL-3.0-or-later

Author Information
------------------

- Yutaka Kamioka <yutaka.kamioka@jp.fujitsu.com>
