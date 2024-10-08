
# Manage Fujitsu PRIMERGY servers via iRMC 

Fujitsu PRIMERGY have been integrated into Fsas Technologies Inc. from April 1, 2024, and the notation will be changed sequentially. Please note Fujitsu notation may be remained in some cases.

The Fujitsu Software Serverview Ansible iRMC Integration features modules to access and manage
Fujitsu PRIMERGY servers via iRMC.

#### Table of Contents

1. [Overview](#overview)
1. [Requirements](#requirements)
1. [Getting Started](#getting-started)
1. [Usage](#usage)
1. [Modules](#modules)
1. [Playbooks](#playbooks)
1. [Change log](#change-log)
1. [License](#license)
1. [Authors](#authors)

## Overview

These modules and examples are intended to provide easy-to-follow and understandable solutions to manage
Fujitsu PRIMERY server settings via iRMC.

## Requirements

- Fujitsu PRIMERGY Server with iRMC S6
- Ansible >= 2.15
- Python >= 3.10
- Python modules 'requests', 'urllib3', 'requests_toolbelt'

## Getting started

- Copy or clone the content of this repo to your playbook directory or to your
  [`ANSIBLE_LIBRARY`](http://docs.ansible.com/ansible/latest/intro_configuration.html#library)
- See [DOCUMENTATION.md](DOCUMENTATION.md), the examples in ```examples``` or the modules in ```library```
  how to use Fujitsu's iRMC modules
- Copy the example playbooks to the main folder and adapt the and the variables in ```group_vars```
  to your environment and run the playbooks.

## Usage

### inventory

Write the IP address and credentials of the target node
in the `iRMC_gruop` group of the `inventory.ini` file:

```ini
[iRMC_group]
10.0.0.1 irmc_user=<username> irmc_password=<password>
10.0.0.2 irmc_user=<username> irmc_password=<password>
```

### group_vars

Set variables that are common to all target nodes into group_vars.

For example, if the target node is operated with a self-signed certificate,
`validate_certificate` must be set to `false`.
Please set the following in `gruop_vars/all` (or `group_vars/iRMC_group`):

```ini
---
# Note: set validate_certificate to false for self-signed certificate
validate_certificate: false
```

### run playbook

The `library` and `module_utils` folders are only auto-detected by Ansible
if they are in the same directory as the `playbook.yml` file.

If the playbook is located in a folder other than the root folder (e.g. `./examples` folder),
need to specify the path to `library` and `module_utiles`.
For example, if you are using the `ansible.cfg` file, please include the following:
For example, write `ansible.cfg` file as follows:

```ini
[defaults]
library = ./library
module_utils = ./module_utils
```

With this setting, playbooks other than the root folder can also be executed:

```shell
ansible-playbook -i inventory.ini ./examples/irmc_facts_examples.yml --tags get
```

## Modules

The following modules are part of this project:

- irmc_biosbootorder - configure iRMC to force next boot to specified option
- irmc_certificate - manage iRMC certificates
- irmc_compare_profiles - compare two iRMC profiles
- irmc_connectvm - connect iRMC Virtual Media Data
- irmc_eventlog - handle iRMC eventlogs
- irmc_facts - get or set Fujitsu PRIMERGY server and iRMC facts
- irmc_fwbios_update - update iRMC Firmware or server BIOS
- irmc_getvm - get iRMC Virtual Media Data
- irmc_idled - get or set server ID LED
- irmc_ldap - manage iRMC LDAP settings
- irmc_license - manage iRMC user accounts
- irmc_ntp - manage iRMC time options
- irmc_powerstate - get or set server power state
- irmc_profiles - handle iRMC profiles
- irmc_scci - execute iRMC remote SCCI commands
- irmc_session - handle iRMC sessions
- irmc_setnextboot - configure iRMC to force next boot to specified option
- irmc_setvm - set iRMC Virtual Media Data
- irmc_task - handle iRMC tasks
- irmc_user - manage iRMC user accounts

For details please refer to the [Module Documentation](DOCUMENTATION.md)

## Playbooks

The following playbooks are part of this package to demonstrate the usage of the modules:

- irmc_biosbootorder_examples.yml
- irmc_cas_examples.yml
- irmc_certificate_examples.yml
- irmc_compare_profiles_examples.yml
- irmc_connectvm_examples.yml
- irmc_eventlog_examples.yml
- irmc_facts_examples.yml
- irmc_fwbios_update_examples.yml
- irmc_getvm_examples.yml
- irmc_idled_examples.yml
- irmc_ldap_examples.yml
- irmc_license_examples.yml
- irmc_ntp_examples.yml
- irmc_powerstate_examples.yml
- irmc_profiles_examples.yml
- irmc_scci_examples.yml
- irmc_session_examples.yml
- irmc_setnextboot_examples.yml
- irmc_setvm_examples.yml
- irmc_task_examples.yml
- irmc_user_examples.yml

The following playbooks are part of this package to demonstrate the solution for common
bare-metal-server provisioning tasks:

- boot_to_virtual_cd.yml
- compare_server_configuration_against_saved_profiles.yml
- create_new_user_and_remove_old_user.yml
- create_user_from_file.yml
- export_ldap_settings_to_file.yml
- export_server_configuration_profiles_to_files.yml
- export_user_data_to_file.yml
- get_server_facts.yml
- import_ldap_settings_from_file.yml
- set_bios_boot_order.yml
- set_bios_boot_order_default.yml

## Change log

- V1.0: Initial version
- V1.1: New: iRMC FW/BIOS update, BIOS boot order, iRMC profile management
- V1.2: New: eLCM Offline/Online Update, RAID configuration
- For later versions, see [CHANGELOG.md](./CHANGELOG.md).

## License

Fsas Technologies Inc.  
Copyright 2018-2024 Fsas Technologies Inc.

GNU General Public License v3.0+ (see [LICENSE.md](LICENSE.md) or https://www.gnu.org/licenses/gpl-3.0.txt)

## Authors

* [Nakamura Takayuki] (https://github.com/nakamura-taka)
