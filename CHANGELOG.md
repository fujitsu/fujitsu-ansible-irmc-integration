# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- Updated supported Python, Ansible, and iRMC versions.
- The copyright has been changed due to organizational changes.

### Fixed

- The following modules have been fixed as not working in the latest environment.
  - `irmc_user`, `irmc_powerstate`
- FD is no longer supported on iRMC S5 and later.
  It can no longer be specified for the following modules.
  - `irmc_connectvm`, `irmc_getvm`, `irmc_setvm`
- The `connect_fd`, `connect_cd`, and `connect_hd` commands are no longer supported.
  - `irmc_scci`
- The type of `profile_json` has been changed from str to json.
  - `irmc_profiles`
- The problem BIOS update not working correctly via TFTP has been fixed.
- The problem ansible task not completing when iRMC update in power-on state has been fixed.
  - `irmc_fwbios_update`
