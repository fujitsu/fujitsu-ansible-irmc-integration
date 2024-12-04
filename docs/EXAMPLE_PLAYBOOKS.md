# Sample Playbook Documentation

**Note**:
This document may not display properly when viewed on <https://galaxy.ansible.com/>.
Therefore, it is recommended to view it on [github.com](https://github.com/fujitsu/fujitsu-ansible-irmc-integration).

## 1. Playbooks

The `./example/playbooks/` directory contains the following playbooks:

- `update_bios_and_irmc_firmware.yml`
- `primergy_setup_with_os_installation.yml`
- `primergy_setup.yml`

---

## 2. Usage

### 2.1 Common Preparations

#### Inventory File

- An inventory file is required for executing any playbook.
- Please create an inventory file `inventory.ini`
  following the "[Example Inventory File Configuration](./USER_GUIDE.md#example-inventory-file-configuration)"
  in the [User Guide](./USER_GUIDE.md)
  (link to [galaxy.ansible.com](https://galaxy.ansible.com/ui/repo/published/fujitsu/primergy/docs/USER_GUIDE/)).

#### File Sharing Server

- TFTP server is required for updating BIOS and iRMC firmware.
- NFS or SMB server is required for OS installation.

---

### 2.2 Playbook `update_bios_and_irmc_firmware.yml`

#### 2.2.1 Features

- Updates the BIOS of iRMC devices and the firmware of iRMC.

#### 2.2.2 Preparation

- Obtain the firmware appropriate for your model in advance.
  For how to obtain it, refer to the
  "[BIOS Firmware Update](./CONFIGURATION.md#bios-firmware-update)"
  and
  "[iRMC Firmware Update](./CONFIGURATION.md#irmc-firmware-update)"
  sections in the [Configuration Guide](./CONFIGURATION.md)
  (link to [galaxy.ansible.com](https://galaxy.ansible.com/ui/repo/published/fujitsu/primergy/docs/CONFIGURATION/)).
- Set up a TFTP server and place the obtained firmware on it.

#### 2.2.3 Configuration in the Playbook

- Specify the IP address of the TFTP server in `vars.tftp_server`.
- In each role's `bios_firmware_path_mapping` and `irmc_firmware_path_mapping`,
  list the corresponding model names and the paths to the firmware to be applied in key-value format.
  The paths should be relative to the root directory of the TFTP server.
- If you only need to update either the BIOS or iRMC,
  disable (remove or comment out) the `role` directives for the unnecessary part.

#### 2.2.4 Running the Playbook

Execute the following command:

```shell
ansible-playbook -i inventory.ini ./examples/playbooks/update_bios_and_irmc_firmware.yml
```

- Updating the firmware takes more than 10 minutes for both BIOS and iRMC.
- The update is performed in the order of BIOS first, then iRMC.
  After updating the iRMC firmware, the iRMC will reboot.
  There may be cases where detecting the completion of the reboot fails, resulting in an error.
  In such cases, the iRMC firmware update is either completed or in progress.
  Please login to the iRMC and verify the running version under System > Running iRMC Firmware.

---

### 2.3 Playbook `primergy_setup_with_os_installation.yml` (`primergy_setup.yml`)

#### 2.3.1 Features

This is structured as a scenario for the initial setup of PRIMERGY.
If OS installation is not required, use `primergy_setup.yml` instead.
The OS to be installed and configured with this playbook is assumed to be Windows Server 2022.

1. Configuration of iRMC
2. Preparation for OS installation and power-on
   (If OS installation is not performed, only power-on)
3. Waiting for the WinRM service after OS installation (or power-on)
4. Configuration of the OS (Windows Server 2022)

#### 2.3.2 Preparation

Obtain the following information:

- **If installing an OS**:
  - IP address to be applied to the OS to be installed
    (Please specify it in the "Inventory File" before executing the playbook)
  - Password for the `Administrator` account to be applied to the OS to be installed
    (Please specify it in the "Inventory File" before executing the playbook)
  - Installation media ISO file for the OS to be installed (assuming Windows Server 2022 in this scenario)
  - License keys for "Media" and "KVM" (for iRMC devices)
  - Set up a file sharing server and place the installation media on it.
    The file sharing can be either NFS or SMB.
- **As needed**:
  - IP address of the DNS server
  - Hostname or IP address of the SMTP server (mail server),
    and if SMTP authentication is required, the account and password
  - Hostname or IP address of the SNMP manager, community name, etc.
  - Hostname or IP address of the NTP server
  - SSL certificates and CA certificates (for iRMC devices)
  - License keys (for iRMC devices)
  - Domain name of the domain controller and the IP address of the DNS server associated with it

Obtain the following files as needed.
For how to obtain them,
refer to each section in the [Configuration Guide](./CONFIGURATION.md)
(link to [galaxy.ansible.com](https://galaxy.ansible.com/ui/repo/published/fujitsu/primergy/docs/CONFIGURATION/)):

- Installer for ServerView Agents
- Installer for ServerView RAID Manager
- Installer for AdoptOpenJDK (if installing ServerView RAID Manager)
- ISO file for ServerView Suite

#### 2.3.3 Configuration in the Playbook

- Enter the obtained information
  into the playbook `primergy_setup_with_os_installation.yml` (`primergy_setup.yml`).
- Disable (remove or comment out) blocks containing the `import_role` directive
  for sections that do not require configuration.
- Additional notes for particularly important sections:
  - **iRMC User Registration `fujitsu.primergy.irmc_account_admin`**:
    Be cautious not to change permissions
    (such as `role`=`Administrator` or `ipmi.lan_privilege`=`OEM`) carelessly,
    as this may cause subsequent configuration tasks to fail.
  - **SSL Certificate and CA Certificate Configuration `fujitsu.primergy.irmc_set_certificate`**:
    The file specified in the `ssl_private_key_path` parameter will be directly modified
    to have headers and footers in OpenSSL 3.x format.
    If you do not want the original file to be altered, please be careful.
    Additionally, write permissions to the specified file are required.
  - **iRMC License Registration `fujitsu.primergy.irmc_set_license`**:
    Since licenses are issued per device,
    the `license_keys` parameter in `fujitsu.primergy.irmc_set_license` must be specified
    for each iRMC device.
    Please specify the `license_keys` parameter in a file
    named `host_vars/<ipaddress-of-irmc-device>.yml` under the current directory.

    ```yaml
    # ./host_vars/<ipaddress-of-irmc-device>.yml
    license_keys:
      - LICENSE-KEY1
      - LICENSE-KEY2
    ```

  - **DNS Configuration for Windows Server `fujitsu.primergy.win_dns`**:
    If you specify `"*"` for the `adapter_names` parameter,
    the settings will apply to all network adapters.
    If you want to apply settings to specific network adapters, specify the adapter names.
    Adapter names can be found using `Get-NetAdapter` after installing Windows.
  - **Domain Joining `fujitsu.primergy.win_set_membership`**:
    When joining a domain, specify the DNS server that is associated with the domain controller
    as the first DNS server in the Windows server DNS settings `fujitsu.primergy.win_dns`.
  - **Data Drive Configuration `fujitsu.primergy.win_data_drive`**:
    An error will occur if there is no unallocated space on the storage
    specified by the `disk_number` parameter.
    If you specify `0` for `disk_number`
    (i.e., allocating on the storage where the OS is installed),
    you need to configure the partitions to ensure there is unallocated space during OS installation.

#### 2.3.4 Running the Playbook

- **With OS Installation**:

  ```shell
  ansible-playbook -i inventory.ini ./examples/playbooks/primergy_setup_with_os_installation.yml
  ```

  Once OS installation starts, open AVR (Advanced Video Redirection),
  which is the remote console feature on the iRMC WebUI,
  and operate the installer from the console.

- **Without OS Installation**:

  ```shell
  ansible-playbook -i inventory.ini ./examples/playbooks/primergy_setup.yml
  ```

- **Common**:
  - In both cases, after powering on,
    the playbook will wait for a certain period until WinRM becomes enabled
    on the booted Windows server.
    (WinRM is a service required when managing Windows with Ansible)
  - If the playbook does not exit the pausing state even after a few minutes (about 2–3 minutes)
    after the Windows server starts,
    it means that the connection to WinRM could not be established.
    In that case, firewall settings are required.
    Login to the Windows server with administrator privileges and execute the following command:

    ```powershell
    New-NetFirewallRule -Name 'WinRM HTTP' -DisplayName 'Allow WinRM over HTTP' -Enabled True -Direction Inbound -Protocol TCP -LocalPort 5985 -Action Allow
    ```

    By configuring the firewall, connections to WinRM will be allowed,
    and the playbook will exit the waiting state and proceed to the next task.
