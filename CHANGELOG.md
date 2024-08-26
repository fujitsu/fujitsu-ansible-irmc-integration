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
  - `irmc_setvm`
