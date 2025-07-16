# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

### Added
- Add upgrade-deps GH Actions workflow
- Add --version flag to show version info
- Add support for Python 3.11 and 3.13

### Changed
- Upgrade deps to latest versions
- Upgrade GH Actions to latest versions

## 1.3.0 - 2024-12-21
### Added
- Add --log-level flag to set custom log level

### Changed
- Use printf to display command description on examples
- Upgrade PieMaker to 1.7.0

### Fixed
- Fix missing aws-assume-role-lib for examples assume role
- Fix dependencies status badge link

## 1.2.0 - 2024-11-24
### Added
- Add --allow-inexisting flag to allow inexisting buckets [#1]

### Changed
- Upgrade PieMaker to 1.5.0

## 1.1.0 - 2024-11-10
### Added
- Add configuration file support

## 1.0.1 - 2024-10-19
### Fixed
- Fix VersionId key name

## 1.0.0 - 2024-10-19
### Added
- Add aws-assume-role-lib and awscli for example testing
- Add buckets with and without versioning to integration testing
- Add assume role to integration testing
- Add response handling with errors and deletions logging

### Changed
- Downgrade Sphinx to 5.3.0 due to awscli compatibility

## 0.10.1 - 2024-09-17
### Fixed
- Fix publish workflow's token syntax

## 0.10.0 - 2024-09-17
### Added
- Initial version
