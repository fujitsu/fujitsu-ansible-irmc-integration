
# Manage Fujitsu PRIMERGY servers via iRMC

Fujitsu PRIMERGY have been integrated into Fsas Technologies Inc. from April 1, 2024, and the notation will be changed sequentially. Please note Fujitsu notation may be remained in some cases.

The Fujitsu Software Serverview Ansible iRMC Integration features modules to access and manage
Fujitsu PRIMERGY servers via iRMC.

## Overview

These modules and examples are intended to provide easy-to-follow and understandable solutions to manage
Fujitsu PRIMERY server settings via iRMC.

## Requirements

- Fujitsu PRIMERGY Server with iRMC S6
- Ansible >= 2.15
- Python >= 3.10
- Python modules 'requests', 'urllib3', 'requests_toolbelt'

## Modules

The following modules are part of this project:

- [irmc_biosbootorder](https://galaxy.ansible.com/ui/repo/published/fujitsu/primergy/content/module/irmc_biosbootorder/) - configure iRMC to force next boot to specified option
- [irmc_cas](https://galaxy.ansible.com/ui/repo/published/fujitsu/primergy/content/module/irmc_cas/) - manage iRMC CAS settings
- [irmc_certificate](https://galaxy.ansible.com/ui/repo/published/fujitsu/primergy/content/module/irmc_certificate/) - manage iRMC certificates
- [irmc_compare_profiles](https://galaxy.ansible.com/ui/repo/published/fujitsu/primergy/content/module/irmc_compare_profiles/) - compare two iRMC profiles
- [irmc_connectvm](https://galaxy.ansible.com/ui/repo/published/fujitsu/primergy/content/module/irmc_connectvm/) - connect iRMC Virtual Media Data
- [irmc_elcm_offline_update](https://galaxy.ansible.com/ui/repo/published/fujitsu/primergy/content/module/irmc_elcm_offline_update/) - offline update a server via iRMC
- [irmc_elcm_online_update](https://galaxy.ansible.com/ui/repo/published/fujitsu/primergy/content/module/irmc_elcm_online_update/) - online update a server via iRMC
- [irmc_elcm_repository](https://galaxy.ansible.com/ui/repo/published/fujitsu/primergy/content/module/irmc_elcm_repository/) - configure the eLCM repostory in iRMC
- [irmc_eventlog](https://galaxy.ansible.com/ui/repo/published/fujitsu/primergy/content/module/irmc_eventlog/) - handle iRMC eventlogs
- [irmc_facts](https://galaxy.ansible.com/ui/repo/published/fujitsu/primergy/content/module/irmc_facts/) - get or set Fujitsu PRIMERGY server and iRMC facts
- [irmc_fwbios_update](https://galaxy.ansible.com/ui/repo/published/fujitsu/primergy/content/module/irmc_fwbios_update/) - update iRMC Firmware or server BIOS
- [irmc_getvm](https://galaxy.ansible.com/ui/repo/published/fujitsu/primergy/content/module/irmc_getvm/) - get iRMC Virtual Media Data
- [irmc_idled](https://galaxy.ansible.com/ui/repo/published/fujitsu/primergy/content/module/irmc_idled/) - get or set server ID LED
- [irmc_ldap](https://galaxy.ansible.com/ui/repo/published/fujitsu/primergy/content/module/irmc_ldap/) - manage iRMC LDAP settings
- [irmc_license](https://galaxy.ansible.com/ui/repo/published/fujitsu/primergy/content/module/irmc_license/) - manage iRMC user accounts
- [irmc_ntp](https://galaxy.ansible.com/ui/repo/published/fujitsu/primergy/content/module/irmc_ntp/) - manage iRMC time options
- [irmc_powerstate](https://galaxy.ansible.com/ui/repo/published/fujitsu/primergy/content/module/irmc_powerstate/) - get or set server power state
- [irmc_profiles](https://galaxy.ansible.com/ui/repo/published/fujitsu/primergy/content/module/irmc_profiles/) - handle iRMC profiles
- [irmc_raid](https://galaxy.ansible.com/ui/repo/published/fujitsu/primergy/content/module/irmc_raid/) - handle iRMC RAID
- [irmc_scci](https://galaxy.ansible.com/ui/repo/published/fujitsu/primergy/content/module/irmc_scci/) - execute iRMC remote SCCI commands
- [irmc_session](https://galaxy.ansible.com/ui/repo/published/fujitsu/primergy/content/module/irmc_session/) - handle iRMC sessions
- [irmc_setnextboot](https://galaxy.ansible.com/ui/repo/published/fujitsu/primergy/content/module/irmc_setnextboot/) - configure iRMC to force next boot to specified option
- [irmc_setvm](https://galaxy.ansible.com/ui/repo/published/fujitsu/primergy/content/module/irmc_setvm/) - set iRMC Virtual Media Data
- [irmc_task](https://galaxy.ansible.com/ui/repo/published/fujitsu/primergy/content/module/irmc_task/) - handle iRMC tasks
- [irmc_user](https://galaxy.ansible.com/ui/repo/published/fujitsu/primergy/content/module/irmc_user/) - manage iRMC user accounts

## Change log

- V1.0: Initial version
- V1.1: New: iRMC FW/BIOS update, BIOS boot order, iRMC profile management
- V1.2: New: eLCM Offline/Online Update, RAID configuration
- For later versions, see [CHANGELOG.md](https://galaxy.ansible.com/ui/repo/published/fujitsu/primergy/docs/CHANGELOG).

## License

Fsas Technologies Inc.  
Copyright 2018-2024 Fsas Technologies Inc.

GNU General Public License v3.0+ (see [LICENSE.md](https://galaxy.ansible.com/ui/repo/published/fujitsu/primergy/docs/LICENSE) or <https://www.gnu.org/licenses/gpl-3.0.txt>)

## Authors

- Shinya Hamano (<hamano.shinya@fujitsu.com>)
- Yutaka Kamioka (<yutaka.kamioka@fujitsu.com>)
- Jiajun Guo (<guo.jiajun@fujitsu.com>)
- Tomohisa Nakai (<nakai.tomohisa@fujitsu.com>)
