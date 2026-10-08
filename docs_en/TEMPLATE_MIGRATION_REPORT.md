# Template migration report (historical v1.0.0 record)

[Español](../docs/TEMPLATE_MIGRATION_REPORT.md) · [English index](README.md)

This document records the initial v1.0.0 migration; its GitHub Release was published September 18, 2026 UTC. Its pending items and any `example.com` references are historical. For the current state, see [README_EN.md](../README_EN.md) and [versioning](VERSIONING.md).

**Release result:** v1.0.0 — Stable / Validated. **Type:** First Stable Release.

## Origin and scope

The original project was reviewed without modification. It was a compact Gradle framework with Java 21, Selenium, Cucumber, JUnit Platform, and a test tied to a specific web application.

## Migration work

- An independent working copy preserved the Gradle Wrapper and reusable source files.
- The project, Gradle group, and package were generalized to `com.automation.template`.
- Application-specific page objects, features, and steps were replaced with a neutral sample.
- URL, browser, headless mode, timeout, and screenshots became externally configurable.
- Gradle forwards supported properties into the test process; hooks close the per-thread driver.
- Bilingual READMEs, architecture, a user guide, troubleshooting, a migration report, a generation script, and a PDF were added.

The initial sample referenced `example.com`; the current test uses the local HTML fixture. Configuration and driver/pages remain in `src/main`; hooks, runner, steps, and support remain in `src/test`. The initial report deliberately did not claim a working CI workflow; [CI was implemented in a later release](VERSIONING.md).

## Historical closeout and validation

The initial release was considered Stable / Validated as a reusable Web UI baseline. Teams still had to supply their own application, test data, and locators. Its documented user-terminal check was `./gradlew.bat clean test -Dheadless=true`, which reported `BUILD SUCCESSFUL in 3s` with five tasks; the PDF was rendered and inspected. These are historical results, not a new validation claim. License, remote repository, runners, and secrets were owner decisions at the time.
