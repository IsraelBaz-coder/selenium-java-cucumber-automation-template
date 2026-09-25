# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

Documentation-only post-release state corrections for the future v1.0.2 patch.

## [1.0.1] - 2026-09-25

### Added

- Native execution logging and failure-evidence handling, including Cucumber attachments and documented artifact locations.
- Governance documentation: license, changelog, contribution guide, security policy, code of conduct, versioning policy, and release process.

### Changed

- Documented the CI execution contract based on the supported `browser`, `headless`, `baseUrl`, and `cucumber.filter.tags` properties.
- Consolidated the configuration inventory, artifact collection contract, logging, screenshot behavior, and bilingual execution guidance.
- Aligned the Gradle root project name with the official repository name.

> `1.0.1` is the current stable, validated, and published release.

## [1.0.0] - 2026-09-17

### Added

- Reusable Web UI automation template using Java, Gradle Wrapper, Selenium WebDriver, Cucumber BDD, JUnit Platform, and Page Object Model.
- Chrome and Edge execution, headless mode, configurable base URL, and a neutral `example.com` reference scenario.
- Bilingual usage documentation, architecture guidance, troubleshooting, migration report, and regenerable PDF manual.
