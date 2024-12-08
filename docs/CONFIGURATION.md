# Ansible Collection `fujitsu.primergy` Configuration Guide

**Note**:
This document may not display properly when viewed on <https://galaxy.ansible.com/>.
Therefore, it is recommended to view it on [github.com](https://github.com/fujitsu/fujitsu-ansible-irmc-integration).

## 1. Introduction

This document explains how to use each role provided in Ansible collection `fujitsu.primergy`,
along with examples of playbooks.  
This configuration guide uses Ansible to perform various settings of PRIMERGY's iRMC,
install the OS (Windows Server), and configure Windows Server.

## 2. PRIMERGY

Configure iRMC (remote management feature) of PRIMERGY.

### Environment and setting sheet –Hardware-

**Note**:
"Environment and setting sheet –Hardware-" is only available in Japanese.

Please also refer to "Environment and setting sheet –Hardware-" provided for each PRIMERGY model
(hereinafter referred to as "Environment and setting sheet (PRIMERGY)").  
You can obtain "Environment and setting sheet (PRIMERGY)" using the following steps:

1. <https://www.fsastech.com/products/pcserver/>
2. Select applicable model from
   Product lineup（"製品ラインアップ"） > Manual（"マニュアル"） > Environment and setting sheet（"環境設定シート"）

### iRMC User Guide

For explanations of each iRMC setting item,
please also refer to "iRMC S6 Web Interface User Guide" (hereinafter referred to as "iRMC User Guide").  
You can obtain "iRMC User Guide" using the following steps:

1. <https://support.ts.fujitsu.com/index.asp?ld=us>
2. Select a new Product > Product search > "iRMC"
3. If displayed, click Downloads > Continue
4. Selected operating system: No Operating System Dependencies
5. Documents > User Guide > iRMC S6 - Web Interface 2.x > Download

### iRMC Firmware Update

Update firmware of iRMC.  
This corresponds to
"C.1 Toolsの設定項目 / Setting item for Tools"
in [Environment and setting sheet (PRIMERGY)](#environment-and-setting-sheet-hardware-).

Please download the firmware in advance:

1. <https://support.ts.fujitsu.com/index.asp?ld=us>
2. Select a new Product > Serial-/ident number
3. Serial-/ident number: <Serial Number>(*1)
4. If displayed, click Downloads > Continue
5. Selected operating system: OS Independent (BIOS, Firmware, etc.)
6. Drivers > Server Management Controller > "*** Firmware Update for TFTP Flash" > Download

*1: The serial number is listed in the system information at `https://<iRMC IP Address>/system`.

- For details on parameters, etc.,
  refer to <https://galaxy.ansible.com/ui/repo/published/fujitsu/primergy/content/role/irmc_update_irmc/>
- If applying to different models simultaneously,
  you need to specify firmware corresponding to each model.
  Refer to the parameter `irmc_firmware_path_mapping`.

**CAUTION**:

- When executed, iRMC device will first power off.
  Be aware that operating OS will be forcibly powered off.
- (As of 2024-11-14) Specifying the parameter `tftp_server` is mandatory.
  If you perform an update without going through a TFTP server,
  the update and restart for the side specified by the parameter `destination` may not occur.
- After firmware update, iRMC will automatically restart,
  but Ansible tasks may fail if they cannot detect the completion of the restart.
  Therefore, it is not recommended to execute it as a single playbook combined with other roles or modules.

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

### BIOS Firmware Update

Update BIOS firmware.  
This corresponds to
"C.1 Toolsの設定項目 / Setting item for Tools"
in [Environment and setting sheet (PRIMERGY)](#environment-and-setting-sheet-hardware-).

Please download the firmware in advance:

1. <https://support.ts.fujitsu.com/index.asp?ld=us>
2. Select a new Product > Serial-/ident number
3. Serial-/ident number: <Serial Number>(*1)
4. If displayed, click Downloads > Continue
5. Selected operating system: OS Independent (BIOS, Firmware, etc.)
6. BIOS > "*** Admin package - Compressed Flash Files" > Download
7. Extract the ZIP file and retrieve the `*.upd` or `*.upc` file

*1: The serial number is listed in the system information at `https://<iRMC IP Address>/system`.

- For details on parameters, etc.,
  refer to <https://galaxy.ansible.com/ui/repo/published/fujitsu/primergy/content/role/irmc_update_bios/>
- If applying to different models simultaneously,
  you need to specify firmware corresponding to each model.
  Refer to the parameter `bios_firmware_path_mapping`.

**CAUTION**:

- When executed, iRMC device will first power off.  
  Be aware that the operating OS will be forcibly powered off.

```yaml
---
- hosts: iRMC_group
  connection: local
  gather_facts: false
  roles:
    - role: fujitsu.primergy.irmc_update_bios
      vars:
        bios_firmware_path: "/any/where/firm/RX1330_M6/bios/D4133-A1x.R1.1.0.UPC"
```

### SSL Certificate and CA Certificate

Configure the SSL certificate and CA certificate of iRMC.

- The SSL certificate and CA certificate must be created or obtained in advance.
- For details on parameters, etc.,
  refer to <https://galaxy.ansible.com/ui/repo/published/fujitsu/primergy/content/role/irmc_set_certificate/>

```yaml
---
- hosts: iRMC_group
  connection: local
  gather_facts: false
  roles:
    - role: fujitsu.primergy.irmc_set_certificate
      vars:
        ssl_private_key_path: "/path/to/certs/server.key"
        ssl_cert_path: "/path/to/certs/server.crt"
        ssl_ca_cert_path: "/path/to/certs/ca.crt"
```

### SNMP

This corresponds to
"C.2 Settings の設定項目 / Setting item for Settings" >
"■Services" >
"Simple Network Management Protocol (SNMP)"
in [Environment and setting sheet (PRIMERGY)](#environment-and-setting-sheet-hardware-).

- Also refer to
  "2.4.4 Services" > "Simple Network Management Protocol (SNMP)"
  in [iRMC User Guide](#irmc-user-guide).
- For details on parameters, etc.,
  refer to <https://galaxy.ansible.com/ui/repo/published/fujitsu/primergy/content/role/irmc_snmp/>
- The parameter `irmc_snmp.trap_destination.servers[].index` should be specified with values from 0 to 6,
  corresponding to SNMP trap servers 1 to 7 in the "iRMC Web Interface".
- Parameters that do not need to be changed do not need to be described.

```yaml
---
- hosts: iRMC_group
  connection: local
  gather_facts: false
  roles:
    - role: fujitsu.primergy.irmc_snmp
      vars:
        irmc_snmp:
          enabled: true
          protocol: "All"
          community_name: "test-public"

          trap_destination:
            community_name: "test-trap-public"
            servers:
              - index: 0
                name: 192.0.2.1
                protocol: "SnmpV2c"
              - index: 1
                name: 192.0.2.2
                protocol: "SnmpV1"
```

### Email Alerting

This corresponds to
"C.2 Settings の設定項目 / Setting item for Settings" >
"■Services" >
"E-mail Alerting"
in [Environment and setting sheet (PRIMERGY)](#environment-and-setting-sheet-hardware-).

- Also refer to
  "2.4.4 Services" > "E-mail Alerting"
  in [iRMC User Guide](#irmc-user-guide).
- For details on parameters, etc.,
  refer to <https://galaxy.ansible.com/ui/repo/published/fujitsu/primergy/content/role/irmc_email_alert/>
- Parameters that do not need to be changed do not need to be described.

```yaml
---
- hosts: iRMC_group
  connection: local
  gather_facts: false
  roles:
    - role: fujitsu.primergy.irmc_email_alert
      vars:
        irmc_email_alert:
          enabled: true
          smtp:
            primary_server:
              address: 192.0.2.1
              authentication:
                type: "Smtp"
                username: "AuthUserName"
                password: "AuthPassword"
          email_format:
            from: "MailFrom@domain.example.com"
            subject: "FixedMailSubject"
            message: "FixedMailMessage"
```

### Local User Accounts

#### Configuration of the First User (Default Username `admin`)

This corresponds to
"C.3 Settings の設定項目 / Setting item for Settings" >
"■User Management" >
"iRMC Local User Accounts"
in [Environment and setting sheet (PRIMERGY)](#environment-and-setting-sheet-hardware-).

- Also refer to "2.4.5 User Management"
  in [iRMC User Guide](#irmc-user-guide).
- For details on parameters, etc.,
  refer to <https://galaxy.ansible.com/ui/repo/published/fujitsu/primergy/content/role/irmc_account_admin/>
- If you have changed the initial username `admin` from the default at the time of purchase,
  this role will not work.

```yaml
---
- hosts: iRMC_group
  connection: local
  gather_facts: false
  roles:
    - role: fujitsu.primergy.irmc_account_admin
      vars:
        irmc_account_admin:
          password: P@ssw0rd
          description: This is Administrator
```

#### Configuration of Users 2 to 15

This corresponds to
"C.3 Settings の設定項目 / Setting item for Settings" >
"■User Management" >
"iRMC Local User Accounts"
in [Environment and setting sheet (PRIMERGY)](#environment-and-setting-sheet-hardware-).

- Also refer to "2.4.5 User Management"
  in [iRMC User Guide](#irmc-user-guide).

**Note**:

- This role is not yet provided.

### Time Synchronization

This corresponds to
"C.3 Settings の設定項目 / Setting item for Settings" >
"■Baseboard Management Controller" >
"Time Synchronization"
in [Environment and setting sheet (PRIMERGY)](#environment-and-setting-sheet-hardware-).

- Also refer to
  "2.4.9 Baseboard Management Controller" > "Time Synchronization"
  in [iRMC User Guide](#irmc-user-guide).
- For details on parameters, etc.,
  refer to <https://galaxy.ansible.com/ui/repo/published/fujitsu/primergy/content/role/irmc_set_ntp/>

```yaml
---
- hosts: iRMC_group
  connection: local
  gather_facts: false
  roles:
    - role: fujitsu.primergy.irmc_set_ntp
      vars:
        ntp_server_primary: 192.0.2.1
        ntp_server_secondary: 192.0.2.2
        time_mode: "System RTC"
        time_zone_location: "Asia/Tokyo"
        rtc_mode: "local time"
```

### License Keys

This corresponds to
"C.3 Settings の設定項目 / Setting item for Settings" >
"■Baseboard Management Controller" >
"License Keys"
in [Environment and setting sheet (PRIMERGY)](#environment-and-setting-sheet-hardware-).

- Also refer to
  "2.4.9 Baseboard Management Controller" > "License Keys"
  in [iRMC User Guide](#irmc-user-guide).
- For details on parameters, etc.,
  refer to <https://galaxy.ansible.com/ui/repo/published/fujitsu/primergy/content/role/irmc_set_license/>

```yaml
---
- hosts: iRMC_group
  connection: local
  gather_facts: false
  roles:
    - role: fujitsu.primergy.irmc_set_license
      vars:
        license_keys:
          - "XXX-XXXX-XXXX-XXXX-XXXX-XX-AA"
          - "XXX-XXXX-XXXX-XXXX-XXXX-XX-BB"
```

---

## 3. OS Installation

- Install Windows Server 2022.
- To use iRMC's "Virtual Media" and "AVR",
  licenses for "Media" and "KVM" are required.
- Executing this role performs a series of operations
  including inserting installation media into virtual drive,
  changing boot priority to CD/DVD-ROM,
  and powering on the device.
- Since there is no built-in mechanism for automated installation,
  after powering on the device,
  you need to open iRMC's AVR and operate installer.
- AVR (Advanced Video Redirection) is remote console function provided by iRMC.
  You can log in to iRMC (`https://{iRMC device IP address}/login`) using a web browser
  and open it from the icon in upper right corner (tooltip "Launch AVR").
- After installation,
  when executing Ansible tasks targeting Windows Server as target node,
  you need to wait for the playbook execution until Windows Server becomes usable as an Ansible target node.  
  Refer to example `"ansible.builtin.wait_for_connection"` below
  and control the playbook execution to wait until WinRM is enabled.

```yaml
---
- hosts: iRMC_group
  connection: local
  gather_facts: false
  roles:
    - role: fujitsu.primergy.irmc_install_windows
      vars:
        share_type: NFS
        server: 192.0.2.1
        share: /var/share
        image: iso/windows/ws2022se.iso

# Wait until the Windows server becomes available for Ansible operations
- name: Wait for Windows node to become available
  hosts: windows
  tasks:
    - name: Wait for WinRM to become available on the target Windows node
      ansible.builtin.wait_for_connection:
        timeout: 10800  # Maximum wait time (10800 seconds = 3 hours)
```

### 3.1 Power On (If Not Installing OS)

- If Windows Server 2022 is already installed,
  power on the device and wait until Ansible operations are possible
  (until WinRM is enabled).
- This is mutually exclusive with "3. OS Installation."

```yaml
---
- hosts: iRMC_group
  connection: local
  gather_facts: false
  tasks:
    - name: Turn on the device
      fujitsu.primergy.irmc_powerstate:
        irmc_url: "{{ inventory_hostname }}"
        irmc_username: "{{ irmc_user }}"
        irmc_password: "{{ irmc_password }}"
        validate_certs: "{{ validate_certificate }}"
        command: "set"
        state: "PowerOn"
      delegate_to: localhost
    - name: Show pausing message
      ansible.builtin.debug:
        msg:
          - "Pausing until Windows has booted and is ready for operation by Ansible."
          - "If the pause does not end after Windows finishes booting, follow these steps."
          - ""
          - "1. Login to Windows with Administrator"
          - "2. Run PowerShell and execute the following commands:"
          - ""
          - "New-NetFirewallRule -Name 'WinRM HTTP' -DisplayName 'Allow WinRM over HTTP' -Enabled True -Direction Inbound -Protocol TCP -LocalPort 5985 -Action Allow"

# Wait until Windows server becomes available for Ansible operations
- name: Wait for Windows node to become available
  hosts: windows
  gather_facts: false
  tasks:
    - name: Wait for WinRM to become available on target Windows node
      ansible.builtin.wait_for_connection:
        timeout: 1800  # Maximum wait time (1800 seconds = 30 minutes)
```

---

## 4. Windows Server 2022

### Environment and setting sheet –ServerView Installation Manager-

**Note**:
"Environment and setting sheet –ServerView Installation Manager-" is only available in Japanese.

Please also refer to sheet "Win2K**_Guide"
in "Environment and setting sheet –ServerView Installation Manager-"
(hereinafter referred to as "Environment and setting sheet (Windows Server)").  
Although various roles provided in this project have only been verified on Windows Server 2022,
this document is based on "Win2K19" (Windows Server 2019) guide
in "環境設定シート –ServerView Installation Manager編-" (CA92344-0149-07).

### Data Drive

Allocate unused storage space to a new drive.

- For details on parameters, etc.,
  refer to <https://galaxy.ansible.com/ui/repo/published/fujitsu/primergy/content/role/win_data_drive/>

```yaml
---
- hosts: windows
  roles:
    - role: fujitsu.primergy.win_data_drive
      vars:
        op: "create"
        drive_letter: D
        disk_number: 0
```

### Organization and Owner

This corresponds to
sheet "Win2K19_ガイド(1)" > "基本設定" > "名前" and "組織名"
in [Environment and setting sheet (Windows Server)](#environment-and-setting-sheet-serverview-installation-manager-).

- For details on parameters, etc.,
  refer to <https://galaxy.ansible.com/ui/repo/published/fujitsu/primergy/content/role/win_organization_owner/>

```yaml
---
- hosts: windows
  roles:
    - role: fujitsu.primergy.win_organization_owner
      vars:
        organization: Fsas Technologies Inc.
        owner: Fsas Tarou
```

### Hostname

This corresponds to
sheet "Win2K19_ガイド(1)" > "基本設定" > "コンピュータ名"
in [Environment and setting sheet (Windows Server)](#environment-and-setting-sheet-serverview-installation-manager-).

- For details on parameters, etc.,
  refer to <https://galaxy.ansible.com/ui/repo/published/fujitsu/primergy/content/role/win_hostname/>

```yaml
---
- hosts: windows
  roles:
    - role: fujitus.primergy.win_hostname
      vars:
        hostname: webserver01
```

### Language and Regional Settings

This corresponds to
sheet "Win2K19_ガイド(1)" > "基本設定" > "タイムゾーン", "地域と言語", and "キーボード"
in [Environment and setting sheet (Windows Server)](#environment-and-setting-sheet-serverview-installation-manager-).

- For details on parameters, etc.,
  refer to <https://galaxy.ansible.com/ui/repo/published/fujitsu/primergy/content/role/win_locale/>
- Depending on language you set,
  access to `https://go.microsoft.com/` may occur to download the language pack.
  Therefore, depending on the environment,
  it may be necessary to set up a proxy in advance (Start > Settings > Network & Internet > Proxy).

```yaml
---
- hosts: windows
  roles:
    - role: fujitsu.primergy.win_locale
      vars:
        language: "en-US"
        location: "244"
        timezone: "Eastern Standard Time"
```

### DNS Configuration

This corresponds to
sheet "Win2K19_ガイド(2)" > "TCP/IP パラメータ 詳細設定" > "DNSサーバ"
in [Environment and setting sheet (Windows Server)](#environment-and-setting-sheet-serverview-installation-manager-).

- For details on parameters, etc.,
  refer to <https://galaxy.ansible.com/ui/repo/published/fujitsu/primergy/content/role/win_dns/>
- If [joining a domain](#joining-a-domain),
  you need to specify DNS servers that are linked to domain controller.

```yaml
---
- hosts: windows
  roles:
    - role: fujitsu.primergy.win_dns
      vars:
        adapter_names: Ethernet
        ipv4_addresses:
          - 192.0.2.1
          - 192.0.2.2
```

### Joining a Workgroup

This corresponds to
sheet "Win2K19_ガイド(1)" > "システムの設定" > "参加先" and "ワークグループ名"
in [Environment and setting sheet (Windows Server)](#environment-and-setting-sheet-serverview-installation-manager-).

- For details on parameters, etc.,
  refer to <https://galaxy.ansible.com/ui/repo/published/fujitsu/primergy/content/role/win_set_membership/>

```yaml
---
- hosts: windows
  roles:
    - role: fujitsu.primergy.win_set_membership
      vars:
        state: workgroup
        workgroup: WORKGROUP
```

### Joining a Domain

This corresponds to
sheet "Win2K19_ガイド(1)" > "システムの設定" > "参加先", "ドメイン名", and "ドメインユーザ名・パスワード"
in [Environment and setting sheet (Windows Server)](#environment-and-setting-sheet-serverview-installation-manager-).

- For details on parameters, etc.,
  refer to <https://galaxy.ansible.com/ui/repo/published/fujitsu/primergy/content/role/win_set_membership/>
- When joining a domain,
  you need to [set up DNS servers](#dns-configuration) that are linked to domain controller in advance.

```yaml
---
- hosts: windows
  roles:
    - role: fujitsu.primergy.win_set_membership
      vars:
        state: domain
        domain: fti.ansible.local
        username: FTI\Administrator
        password: P@ssw0rd
```

### SNMP Configuration

This corresponds to
sheet "Win2K19_ガイド(2)" > "SNMPサービス"
and
sheet "Win2K19_ガイド(3)" > "「SNMPサービス」選択時のみ" > "SNMPサービス", "トラップ構成項目", "セキュリティ", and "エージェント"
in [Environment and setting sheet (Windows Server)](#environment-and-setting-sheet-serverview-installation-manager-).

- For details on parameters, etc.,
  refer to <https://galaxy.ansible.com/ui/repo/published/fujitsu/primergy/content/role/win_snmp/>

```yaml
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
```

### Enabling Remote Desktop

This corresponds to
sheet "Win2K19_ガイド(3)" > "追加のパラメータ" > "Remote Desktop"
in [Environment and setting sheet (Windows Server)](#environment-and-setting-sheet-serverview-installation-manager-).

- For details on parameters, etc.,
  refer to <https://galaxy.ansible.com/ui/repo/published/fujitsu/primergy/content/role/win_set_rdp/>

```yaml
---
- hosts: windows
  roles:
    - role: fujitsu.primergy.win_set_rdp
      vars:
        enabled: true
```

### Setting Up ServerView Agents

**CAUTION**:
This explanation applies to ServerView Agents provided in the Japanese region.
ServerView Agents provided in other regions have different components,
and therefore, installation with these procedures is not supported.

This corresponds to
sheet "Win2K19_ガイド(3)" > "アプリケーションウィザード" > "ServerView Suite" > "ServerView Agents"
in [Environment and setting sheet (Windows Server)](#environment-and-setting-sheet-serverview-installation-manager-).

Please download ServerView Agents in advance:

1. <https://support.ts.fujitsu.com/index.asp?ld=jp> (Requires downloading in a **Japanese** environment)
2. 製品を選択する > カテゴリから探す > Software > ServerView > Operation > Agents, Agentless Service & Providers
3. If displayed, click ダウンロード > 次へ
4. 右記OSに関連した情報を表示する: Windows Server 2022
5. アプリケーション > ServerView Agents for Windows > Download（"↓カートに入れず直接ダウンロードする"）
6. Run `FTS_ServerViewAgentsforWindows_<version>_*.exe` to extract
7. Retrieve `ServerView\Agents\ServerViewAgents_Win_x64.exe`

- For details on parameters, etc.,
  refer to <https://galaxy.ansible.com/ui/repo/published/fujitsu/primergy/content/role/win_serverview_agents/>
- Specify the path to the installer on the Ansible control node's file system for the `installer` parameter.  
  Specify an absolute path or a relative path from the playbook.

```yaml
---
- hosts: windows
  roles:
    - role: fujitsu.primergy.win_serverview_agents
      vars:
        password: P@ssw0rd!
        installer: /any/where/ServerView/Agents/ServerViewAgents_Win_x64.exe
```

### Setting Up ServerView RAID Manager

This corresponds to
sheet "Win2K19_ガイド(3)" > "アプリケーションウィザード" > "ServerView Suite" > "ServerView RAID Manager"
in [Environment and setting sheet (Windows Server)](#environment-and-setting-sheet-serverview-installation-manager-).

Please download ServerView RAID Manager in advance:

1. <https://support.ts.fujitsu.com/index.asp?ld=us>
2. Select a new Product > Browse for product > Software > ServerView > Operation > RAID Management
3. If displayed, click Downloads > Continue
4. Selected operating system: Windows Server 2022
5. Applications > ServerView RAID Manager (Windows, 64-bit) > Download
6. Extract `FTS_ServerViewRAIDManagerWindows64bit_<version>_*.zip`
7. Retrieve `Windows\x64\ServerView_RAID_<version>_x64.exe`

Please download AdoptOpenJDK in advance:

1. <https://adoptium.net/temurin/releases/?os=windows&version=8&arch=x64&package=jre>
2. Only AdoptOpenJDK is supported by this role. Other JDKs are not supported.

- For details on parameters, etc.,
  refer to <https://galaxy.ansible.com/ui/repo/published/fujitsu/primergy/content/role/win_serverview_raidmanager/>
- Specify path to the installer and `openjdk_installer` on Ansible control node's file system.  
  Specify an absolute path or a relative path from the playbook.

```yaml
- hosts: windows
  roles:
    - role: fujitsu.primergy.win_serverview_raidmanager
      vars:
        password: P@ssw0rd!
        installer: /any/where/ServerViewRAIDManagerWindows64bit/Windows/x64/ServerView_RAID_7.17.5_x64.exe
        openjdk_installer: /any/where/OpenJDK8U-jre_x64_windows_hotspot_8u422b05.msi
```

### Setting Up DSNAP High-Reliability Tool

This corresponds to
sheet "Win2K19_ガイド(3)" > "アプリケーションウィザード" > "Add-on Packages" > "DSNAP"
in [Environment and setting sheet (Windows Server)](#environment-and-setting-sheet-serverview-installation-manager-).

DSNAP is stored in the ServerView Suite.  
Please download ServerView Suite (ServerView Management and Serviceability DVD) in advance:

1. <https://support.ts.fujitsu.com/index.asp?ld=us>
2. Select a new Product > Serial-/ident number
3. Serial-/ident number: <Serial Number>(*1)
4. If displayed, click Downloads > Continue
5. Selected operating system: Windows Server 2022
6. Applications > Server Management Software > ServerView - ServerView Suite CDs/DVDs/ISO-Images > ServerView Management and Serviceability DVD > Download
7. Extract `FTS_ServerViewManagementandServiceabilityDVD_*.zip` file and retrieve ISO file

*1: Serial number is listed in system information at `https://<iRMC IP Address>/system`.

- For details on parameters, etc.,
  refer to <https://galaxy.ansible.com/ui/repo/published/fujitsu/primergy/content/role/win_dsnap/>
- For the `path` parameter, you can directly specify DSNAP (`*.exe`).  
  Although it increases effort to extract DSNAP from ISO file,
  it reduces time required to transfer files to the target node, thereby reducing the playbook execution time.  
  To extract DSNAP from ISO file,
  (on Windows) right-click ISO file > Open with > Explorer to mount ISO file,
  then retrieve `SVSLocalTools\{LANGUAGE}\DSNAP\{ARCH}\dsnap.exe`.

```yaml
---
- hosts: windows
  roles:
    - role: fujitsu.primergy.win_dsnap
      vars:
        language: Japanese
        path: /path/to/SVS15.24.06.03.iso
```
