# Ansible Collection `fujitsu.primergy` User Guide

**Note**:
This document may not display properly when viewed on <https://galaxy.ansible.com/>.
Therefore, it is recommended to view it on [github.com](https://github.com/fujitsu/fujitsu-ansible-irmc-integration).

## 1. Introduction

This document is a guide for users of Ansible collection `fujitsu.primergy`.  
Ansible collections are packages that bundle Ansible playbooks, modules, roles, plugins, documentation, and more.  
Ansible collection `fujitsu.primergy` aims to automate configuration tasks
based on PRIMERGY's "Environment and setting sheet" and provides Ansible roles and modules.

This user guide provides information on setting up the Ansible collection,
usage examples of roles, and troubleshooting.

### Target Audience

This document is intended for users with basic knowledge of Ansible.

## 2. Installation and Setup

### Prerequisites

#### Operating System and Software

- Linux
  (For Windows, refer to "5. Frequently Asked Questions (FAQ)" under
  "[Can I run Ansible on Windows?](#can-i-run-ansible-on-windows))"
- Python 3.10

#### Python Modules

- `ansible` >= 8.0.0
- `pywinrm` >= 0.5.0
- `requests` >= 2.32.0
- `requests_toolbelt` >= 1.0.0
- `urllib3` >= 2.2.0

### Setting Up Ansible Execution Environment

Create and activate a Python virtual environment (venv),
then install the necessary Python modules including Ansible:

```shell
$ mkdir -p ~/ansible/primergy && cd $_  # Create and move to a directory of your choice
$ python -m venv venv && . $_/bin/activate
(venv) $ python -m pip install ansible pywinrm requests requests_toolbelt urllib3
```

Use Ansible installed in the virtual environment (venv)
to install the Ansible collection `fujitsu.primergy` from <https://galaxy.ansible.com/>:

```bash
(venv) $ ansible-galaxy collection install fujitsu.primergy
```

### Example Inventory File Configuration

In Ansible, managed devices are defined in an "inventory file".

- Define two groups: `[iRMC_group]` and `[windows]`.
  These group names align with the examples of how to execute Ansible playbooks
  explained in this "User Guide" and "Configuration Guide".
- In `[iRMC_group]`, specify the IP address of PRIMERGY's remote management interface,
  an account with administrative privileges (if in shipped condition, `admin` is available), and its password.
- In `[windows]`, specify the IP address of the Windows server,
  an account with administrative privileges (usually `Administrator`), and its password.
- Both groups can list multiple devices/servers.
- In `[*:vars]`, you can specify common parameters for each group.
  Here, connection setting parameters are specified.

Name the file `inventory.ini` and include the following content:

```ini
[iRMC_group]
<ipaddress-of-iRMC-device> irmc_user=admin irmc_password=<password>

[windows]
<ipaddress-of-windows> ansible_user=Administrator ansible_password=<password>

[iRMC_group:vars]
validate_certificate=false  # Necessary if SSL server certificates are not registered on iRMC devices

[windows:vars]
ansible_port=5985
ansible_connection=winrm
ansible_winrm_transport=ntlm
ansible_winrm_server_cert_validation=ignore
```

### Connectivity Test

#### Connectivity Test to iRMC Devices

Retrieve and display the configuration and settings of the specified iRMC device:

```shell
$ ansible localhost -m fujitsu.primergy.irmc_facts -a "irmc_url=192.0.2.1 irmc_username=admin irmc_password=P@ssw0rd! validate_certs=false"
localhost | SUCCESS => {
    "changed": false,
    "facts": {
        "hardware": {
            "ethernetinterfaces": {
                ...
            }
        }
    }
}
```

`irmc_url`, `irmc_username`, and `irmc_password` correspond to the entries described
in the `[iRMC_group]` group in the inventory file.

#### Connectivity Test to Windows Servers

Verify the connection to the `[windows]` group specified in the inventory file:

```shell
$ ansible -i inventory.ini windows -m ansible.windows.win_ping
192.0.2.2 | SUCCESS => {
    "changed": false,
    "ping": "pong"
}
```

If multiple servers are listed in `[windows]`, connection verification is performed for all servers.

Ensure that the specified Windows server can receive requests to [WinRM](https://learn.microsoft.com/en-us/windows/win32/winrm/portal).  
It is assumed that WinRM connections over HTTP are enabled immediately after installing the Windows server  
(can be verified via PowerShell with `"winrm enumerate winrm/config/Listener"`).  
If the connectivity test fails, apply the following firewall settings:

```powershell
New-NetFirewallRule -Name "WinRM HTTP" -DisplayName "Allow WinRM over HTTP" -Enabled True -Direction Inbound -Protocol TCP -LocalPort 5985 -Action Allow
```

## 3. Usage

### Overall Structure of the Collection

For a detailed list of modules and roles in this collection,
refer to the [Ansible Galaxy Collection Page](https://galaxy.ansible.com/fujitsu/primergy).

### How to Use Roles

Refer to the [Configuration Guide](./CONFIGURATION.md)
(link to [galaxy.ansible.com](https://galaxy.ansible.com/ui/repo/published/fujitsu/primergy/docs/CONFIGURATION/)).

### Description of Sample Playbooks

Sample playbooks are provided in `examples/playbooks/`.

For usage information,
Refer to the [Sample Playbook Documentation](./EXAMPLE_PLAYBOOKS.md)
(link to [galaxy.ansible.com](https://galaxy.ansible.com/ui/repo/published/fujitsu/primergy/docs/EXAMPLE_PLAYBOOKS/)).

### Troubleshooting

To check the details of errors that occurred during playbook execution,
use the `-vvv` option to obtain debug logs and examine error messages and variable values.

```shell
ansible-playbook -i inventory.ini playbook.yml -vvv
```

## 4. Feedback and Contribution

We welcome feedback and contributions to this project.  
Bug reports, feature requests, and improvement suggestions can be sent to the following contacts.  
We will respond in Japanese or English.

### How to Contact

#### Contact via Email

(For internal use, etc.) For private contacts or inquiries, please send an email to the following addresses:

- Shinya Hamano (<[hamano.shinya@fujitsu.com](mailto:hamano.shinya@fujitsu.com)>)
- Yutaka Kamioka (<[yutaka.kamioka@fujitsu.com](mailto:yutaka.kamioka@fujitsu.com)>)
- Jiajun Guo (<[guo.jiajun@fujitsu.com](mailto:guo.jiajun@fujitsu.com)>)
- Tomohisa Nakai (<[nakai.tomohisa@fujitsu.com](mailto:nakai.tomohisa@fujitsu.com)>)

*Members and email addresses are current as of December 2024.*

#### GitHub Issues

For public feedback or contribution proposals, please use the GitHub "Issues" page.  
GitHub Issues: <https://github.com/fujitsu/fujitsu-ansible-irmc-integration/issues>

#### Request When Providing Feedback

When reporting bugs, including the following information will facilitate smooth handling.

- **Purpose and Operations Performed**:
  Describe the purpose of the setting and the specific operations/settings performed to achieve it.
- **Occurrence Details**:
  Describe specifically what actually happened, such as execution results or unexpected behaviors.
- **Steps or Situation to Reproduce**:
  Describe the steps required to reproduce the problem, and the environment or situation when it occurred.
- **Usage Environment (Equipment and Versions, etc.)**:
  Describe the model name of the equipment used, and BIOS or iRMC versions (if the target is iRMC devices).  
  Obtaining `irmc_facts` using the method described in the section
  "[Connectivity Test to iRMC Devices](#connectivity-test-to-irmc-devices)" of this document is also a good method.
- **Ansible Execution Log**: Including the Ansible execution log will help identify the cause.
  Particularly, having detailed logs using the `-vvv` option makes analysis easier.

## 5. Frequently Asked Questions (FAQ)

### Can I Run Ansible on Windows?

It is not supported on Windows.
Ansible can be run on Windows Subsystem for Linux (WSL),
but it is not officially supported and is not recommended for use in production systems.  
For details, refer to this URL:  
<https://docs.ansible.com/ansible/latest/os_guide/intro_windows.html#using-windows-as-the-control-node>

## 6. Additional Information

### Ansible Galaxy

- <https://galaxy.ansible.com/>
- <https://galaxy.ansible.com/ui/repo/published/fujitsu/primergy/>

### Ansible

- <https://docs.ansible.com/users.html>
- Start writing Ansible playbooks - <https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_intro.html#playbook-syntax>
- Build inventory files to manage multiple hosts - <https://docs.ansible.com/ansible/latest/inventory_guide/intro_inventory.html>
- Start exploring Ansible Galaxy - <https://docs.ansible.com/ansible/latest/galaxy/user_guide.html#finding-collections-on-galaxy>
