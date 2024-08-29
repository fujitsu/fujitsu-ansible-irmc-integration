# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- Updated supported Python, Ansible, and iRMC versions.
- The note regarding the company name change has been added.
- The copyright has been changed due to organizational changes.
- The type of the parameter `profile_json` was changed from `str` to `json` in the following modules.
  - `irmc_profiles`, `irmc_compare_profiles`

### Fixed

- The following modules have been fixed as not working in the latest environment.
  - `irmc_user`, `irmc_powerstate`, `irmc_biosbootorder`, `irmc_ntp`, `irmc_license`, `irmc_connectvm`, `irmc_scci`, `irmc_profiles`
- The problem BIOS update not working correctly via TFTP has been fixed in the `irmc_fwbios_update` module.
- The `irmc_fwbios_update` module fixes a problem with the ansible task not completing when updating iRMC with power on.
- Secondary NTP incorrect display is fixed in `irmc_ntp` module.

### Removed

- FD is no longer supported as remote mount media in iRMC S5 and later.
  It can no longer be specified for the following modules.
  - `irmc_connectvm`, `irmc_getvm`, `irmc_setvm`
- The `connect_fd`, `connect_cd` and `connect_hd` commands are no longer supported in the `irmc_scci` module.
- `"Floppy"` can no longer be specified for parameter `bootsource` in the `irmc_setnextboot` module.
