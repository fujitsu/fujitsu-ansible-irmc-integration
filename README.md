
# Manage Fujitsu PRIMERGY servers via iRMC 

The Fujitsu Software Serverview Ansible iRMC Integration features modules to access and manage
Fujitsu PRIMERGY servers via iRMC.

#### Table of Contents

1. [Overview](#overview)
2. [Requirements](#requirements)
3. [Getting Started](#getting-started)
4. [API Documentation](#documentation)
5. [Usage](#usage)
6. [Modules](#modules)
7. [Playbooks](#playbooks)
8. [History](#history)
9. [License](#license)
10. [Authors](#authors)

## Overview

These modules and examples are intended to provide easy-to-follow and understandable solutions to manage
Fujitsu PRIMERY server settings via iRMC.

##### Version: V1.3

## Requirements

- Fujitsu PRIMERGY Server with iRMC S4 FW >= 9.04 or iRMC S5 FW >= 1.25
- Ansible >= 2.4
- Python >= 2.6
- Python modules 'future', 'requests', 'urllib3', 'requests_toolbelt'

The modules were tested on RHEL 6, RHEL 7, SLES 12, SLES 15.

## Getting started

- Copy or clone the content of this repo to your playbook directory or to your
  [`ANSIBLE_LIBRARY`](http://docs.ansible.com/ansible/latest/intro_configuration.html#library)
- See [DOCUMENTATION.md](DOCUMENTATION.md), the examples in ```examples``` or the modules in ```library```
  how to use Fujitsu's iRMC modules
- Copy the example playbooks to the main folder and adapt the and the variables in ```group_vars```
  to your environment and run the playbooks.

## Documentation

- [Specification: iRMC RESTful API](http://manuals.ts.fujitsu.com/file/13371/irmc-restful-spec-en.pdf)
- [Specification: iRMC Redfish API](http://manuals.ts.fujitsu.com/file/13372/irmc-redfish-wp-en.pdf)
- [Whitepaper: iRMC RESTful Server Management API](http://manuals.ts.fujitsu.com/file/12844/irmc-restful-wp-en.pdf)
- [Whitepaper: iRMC Remote Scripting and Configuration](http://manuals.ts.fujitsu.com/file/12563/wp-svs-irmc-remote-scripting-en.pdf)

## Usage

Examples should be run from the root folder.  

**Example command to run irmc_facts_examples.yml:**

`ansible-playbook irmc_facts_examples.yml`

Run the verbose version with:

`ansible-playbook -vvv irmc_facts_examples.yml`

## Modules

The following modules are part of this project:

  * irmc_biosbootorder - configure iRMC to force next boot to specified option
  * irmc_certificate - manage iRMC certificates
  * irmc_compare_profiles - compare two iRMC profiles
  * irmc_connectvm - connect iRMC Virtual Media Data
  * irmc_eventlog - handle iRMC eventlogs
  * irmc_facts - get or set Fujitsu PRIMERGY server and iRMC facts
  * irmc_fwbios_update - update iRMC Firmware or server BIOS
  * irmc_getvm - get iRMC Virtual Media Data
  * irmc_idled - get or set server ID LED
  * irmc_ldap - manage iRMC LDAP settings
  * irmc_license - manage iRMC user accounts
  * irmc_ntp - manage iRMC time options
  * irmc_powerstate - get or set server power state
  * irmc_profiles - handle iRMC profiles
  * irmc_scci - execute iRMC remote SCCI commands
  * irmc_session - handle iRMC sessions
  * irmc_setnextboot - configure iRMC to force next boot to specified option
  * irmc_setvm - set iRMC Virtual Media Data
  * irmc_task - handle iRMC tasks
  * irmc_user - manage iRMC user accounts

For details please refer to the [Module Documentation](DOCUMENTATION.md)

## Playbooks

The following playbooks are part of this package to demonstrate the usage of the modules:

  * irmc_biosbootorder_examples.yml
  * irmc_cas_examples.yml
  * irmc_certificate_examples.yml
  * irmc_compare_profiles_examples.yml
  * irmc_connectvm_examples.yml
  * irmc_eventlog_examples.yml
  * irmc_facts_examples.yml
  * irmc_fwbios_update_examples.yml
  * irmc_getvm_examples.yml
  * irmc_idled_examples.yml
  * irmc_ldap_examples.yml
  * irmc_license_examples.yml
  * irmc_ntp_examples.yml
  * irmc_powerstate_examples.yml
  * irmc_profiles_examples.yml
  * irmc_scci_examples.yml
  * irmc_session_examples.yml
  * irmc_setnextboot_examples.yml
  * irmc_setvm_examples.yml
  * irmc_task_examples.yml
  * irmc_user_examples.yml

The following playbooks are part of this package to demonstrate the solution for common
bare-metal-server provisioning tasks:

  * boot_to_virtual_cd.yml
  * compare_server_configuration_against_saved_profiles.yml
  * create_new_user_and_remove_old_user.yml
  * create_user_from_file.yml
  * export_ldap_settings_to_file.yml
  * export_server_configuration_profiles_to_files.yml
  * export_user_data_to_file.yml
  * get_server_facts.yml
  * import_ldap_settings_from_file.yml
  * set_bios_boot_order.yml
  * set_bios_boot_order_default.yml

## Change log

* V1.0: Initial version
* V1.1: New: iRMC FW/BIOS update, BIOS boot order, iRMC profile management
* V1.2: New: eLCM Offline/Online Update, RAID configuration
* V1.3: Add new folder structure 

## License

FUJITSU LIMITED
Copyright 2018-2019 FUJITSU LIMITED

GNU General Public License v3.0+ (see [LICENSE.md](LICENSE.md) or https://www.gnu.org/licenses/gpl-3.0.txt)

## Authors

* [Nakamura Takayuki] (https://github.com/nakamura-taka)
