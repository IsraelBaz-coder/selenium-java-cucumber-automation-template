# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-10-01

Hito 3 — Completed / Validated. Technical status: Stable / Validated. The official publication date is October 1, 2026; Published is recorded only after the tag and GitHub Release exist.

#### Added

- GitHub Actions uploads available Gradle/Cucumber reports, JUnit results, logs, and screenshots as the `test-evidence` artifact, retained for 14 days.
- Base GitHub Actions workflow for pull requests and pushes to `main`, using Temurin Java 21 and the Gradle Wrapper in headless mode.
- Versioned local HTML fixture for the template smoke test.
- Basic Gradle cache setup for GitHub Actions.
- Stable `quality-gate` job/check for pull requests targeting `main`.
- Operational CI/CD documentation covering pull requests, check results, artifacts, and protected merges.

#### Changed

- The example Page Object opens the local fixture, avoiding dependence on external page content.
- Updated usage documentation and regenerated the PDF manual to match the smoke test and CI workflow.
- Aligned the documentation with the validated Hito 3 technical state and the official publication date.
- Documented the beginner workflow for creating a pull request, reading the Quality Gate, downloading evidence, and following the active `main` ruleset.
- Completed and validated the technical work for Hito 3 and Blocks 1–4 after real GitHub validation; formal documentation closeout remains in progress.

#### Validated

- Confirmed a successful `quality-gate`, a controlled failing test with `test-evidence`, the required check blocking merge, restoration followed by another successful check, and a successful post-merge run on `main`.
- Confirmed evidence artifacts in both successful and failing runs and an active `main` ruleset requiring a pull request, an up-to-date branch, and the `quality-gate` check while blocking force pushes and branch deletion.
- v1.1.0 is Stable / Validated, and Hito 3 is Completed / Validated. Publication remains a separate event: add Published only after the v1.1.0 tag and GitHub Release exist. v1.0.2 remains the latest published version.

## [1.0.2] - 2026-09-25 (Stable / Validated / Published)

### Changed

- Finalized the documentation-only hotfix that corrects post-release state inconsistencies after v1.0.1.
- No functional framework changes, dependency changes, CI/CD implementation, Docker, Selenium Grid, Healenium, or Playwright were introduced.

## [1.0.1] - 2026-09-25

### Added

- Native execution logging and failure-evidence handling, including Cucumber attachments and documented artifact locations.
- Governance documentation: license, changelog, contribution guide, security policy, code of conduct, versioning policy, and release process.

### Changed

- Documented the CI execution contract based on the supported `browser`, `headless`, `baseUrl`, and `cucumber.filter.tags` properties.
- Consolidated the configuration inventory, artifact collection contract, logging, screenshot behavior, and bilingual execution guidance.
- Aligned the Gradle root project name with the official repository name.

> Historical note: `1.0.1` was the stable, validated, and published release at the time of this entry. The latest published release is `v1.0.2`.

## [1.0.0] - 2026-09-17

### Added

- Reusable Web UI automation template using Java, Gradle Wrapper, Selenium WebDriver, Cucumber BDD, JUnit Platform, and Page Object Model.
- Chrome and Edge execution, headless mode, configurable base URL, and a neutral `example.com` reference scenario.
- Bilingual usage documentation, architecture guidance, troubleshooting, migration report, and regenerable PDF manual.
