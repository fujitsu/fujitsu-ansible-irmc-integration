# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [2.0.1] - 2024-12-10

### Changed

- Added English version of the documentation.

## [2.0.0] - 2024-11-29

### Added

- Roles and their examples based on operational scenes have been added. See `README.md` for details.
- The user guide and contribution guide have been added in Japanese.

### Fixed

- The problem that prevented setting only numeric strings for `ntp_server_primary` and `ntp_server_secondary` has been fixed in the `irmc_ntp` module.
- The `irmc_biosbootorder` module has been fixed to able the boot order to be reset with the command "default".

### Changed

- The directory structure and documents has been changed for the release to [Ansible Galaxy](https://galaxy.ansible.com/).
- The `irmc_raid` module has been verified with iRMC S6, and updated documentation.
- Python module `pywinrm` add to the requirements.

### Removed

- `DOCUMENTATION.md` is removed.

## [1.3.0] - 2024-08-30

### Changed

- Updated supported Python, Ansible, and iRMC versions.
- The note regarding the company name change has been added.
- The copyright has been changed due to organizational changes.
- The following modules have changed the type of the parameter `profile_json` from `str` to `json`.
  `irmc_profiles` and `irmc_compare_profiles`.

### Fixed

- The following modules have been fixed as not working in the latest environment.
  `irmc_user`, `irmc_powerstate`, `irmc_biosbootorder`, `irmc_ntp`, `irmc_license`, `irmc_connectvm`, `irmc_scci` and `irmc_profiles`.
- The problem BIOS update not working correctly via TFTP has been fixed in the `irmc_fwbios_update` module.
- The `irmc_fwbios_update` module fixes a problem with the ansible task not completing when updating iRMC with power on.
- Secondary NTP incorrect display is fixed in `irmc_ntp` module.

### Removed

- Since iRMC S5, FD is no longer supported as a remote media mount and cannot be specified in the following modules.
  `irmc_connectvm`, `irmc_getvm` and `irmc_setvm`.
- The `connect_fd`, `connect_cd` and `connect_hd` commands are no longer supported in the `irmc_scci` module.
- `"Floppy"` can no longer be specified for parameter `bootsource` in the `irmc_setnextboot` module.
