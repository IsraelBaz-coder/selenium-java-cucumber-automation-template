# Automation Template Selenium Java Cucumber

Reusable Web UI test template based on Java 21, Selenium WebDriver, Cucumber BDD, JUnit Platform and Gradle. It includes a smoke test using a local HTML page in `src/test/resources/fixtures/`; the scenario does not depend on external website content. Initial dependency and browser setup may still require network access. Configure your application URL and replace the example when adapting the template.

| Release | Value |
|---|---|
| Published stable version | **v1.1.0** |
| Version in development | **v1.2.0 — Milestone 4, Block 1** |
| Technical status | **Milestone 4 in development; Block 1: base logging** |
| Milestone 3 | **Completed / Validated** |
| v1.2.0 publication date | **Not set** |

v1.1.0 is the published stable version. The `feature/hito-4-logging-observability-base` branch adds Block 1 — Logging base / Observability foundation of Milestone 4 — Reporting + Logging / Observability. v1.2.0 remains in development and has no publication date.

| Document information | Value |
|---|---|
| Author / Template Creator | Israel Baz |
| Role | Test Automation / Prompt Engineering / AI Automation |
| Maintainer | Israel Baz |

The template was validated and can be used as a baseline for new projects. Configure application-specific values through properties, environment variables or `-D` parameters; introduce new capabilities in later versions.

## Highlights

- Java 21 by default, Java 17 compatible, Gradle Wrapper and UTF-8 source encoding.
- Page Object Model, Steps and Hooks kept separate.
- Chrome/Edge, headless mode and URL configured by file, environment or `-D`.
- Explicit waits, execution logging, failure screenshots and Cucumber HTML reporting. The Milestone 4 branch uses SLF4J and Logback for logging.

## Java version selection

Java 21 is the default in the current configuration. The only supported toolchains are Java 17 and Java 21, selected through the Gradle `javaVersion` property:

| Purpose | PowerShell |
|---|---|
| Default Java (21) | `.\gradlew.bat clean test` |
| Use Java 17 | `.\gradlew.bat clean test -PjavaVersion=17` |
| Explicit Java 21 | `.\gradlew.bat clean test -PjavaVersion=21` |

Java 17 is the only supported alternative. `-PjavaVersion=18`, `19`, `20`, `22`, and every value other than `17` or `21` are rejected with a `GradleException`. Gradle itself must run with JDK 17 or later, and the selected toolchain must be installed or available to Gradle.

For the installation, `JAVA_HOME`, VS Code, validation and Java 21 rollback steps, read [Java version selection](docs/GUIA_USO_TEMPLATE_AUTOMATIZACION.md#selección-de-versión-de-java).

## Architecture and structure

```text
src/main/java/com/automation/template/{config,driver,pages}
src/test/java/com/automation/template/{hooks,runners,steps,support}
src/test/resources/{features,config.properties}
```

Features express Gherkin behavior; Steps translate intent; Page Objects encapsulate Selenium, locators and waits. Hooks manage browser lifecycle and the Runner connects Cucumber to JUnit Platform.

See [architecture](docs/ARCHITECTURE.md), the [usage guide](docs/GUIA_USO_TEMPLATE_AUTOMATIZACION.md), [logging and its diagrams](docs/LOGGING.md), and [troubleshooting](docs/TROUBLESHOOTING.md).

## Configuration and execution

`src/test/resources/config.properties` contains defaults. Priority is `-D`, environment variables (`BASE_URL`, `BROWSER`, `HEADLESS`) then file.

The built-in smoke test uses the local fixture; `baseUrl` remains available for real application Page Objects and does not change this example test.

| Purpose | PowerShell |
|---|---|
| Clean | `.\gradlew.bat clean` |
| Run | `.\gradlew.bat test` |
| Clean and run | `.\gradlew.bat clean test` |
| Headless | `.\gradlew.bat clean test -Dheadless=true` |
| Chrome | `.\gradlew.bat clean test -Dbrowser=CHROME` |
| Edge | `.\gradlew.bat clean test -Dbrowser=EDGE` |
| Application URL | `.\gradlew.bat clean test -DbaseUrl=https://your-application` |
| Cucumber tags | `.\gradlew.bat clean test "-Dcucumber.filter.tags=@example"` |
| Headless Cucumber tags | `.\gradlew.bat clean test -Dheadless=true "-Dcucumber.filter.tags=@example"` |
| Cucumber alias | `.\gradlew.bat cucumber` |

## Evidence and reports

Each execution creates regenerable Git-ignored artifacts under `build/`:

| Artifact | Path |
|---|---|
| Cucumber HTML | `build/reports/cucumber/cucumber.html` |
| Gradle HTML | `build/reports/tests/test/` |
| JUnit XML | `build/test-results/test/` |
| Failure screenshots | `build/evidence/screenshots/` |
| Execution log | `build/logs/automation.log` |

Hooks log each scenario's start, finish and status, along with the effective browser and headless mode. `DriverFactory` and `DriverManager` log driver initialization and shutdown. Logging is configured in `src/test/resources/logback-test.xml`; see [Logging](docs/LOGGING.md) for levels, excluded data, CI/CD and troubleshooting. If a scenario fails and `screenshotOnFailure=true`, the existing Hooks attempt to attach a PNG to the Cucumber scenario and persist it physically. The file name combines a sanitized scenario name, timestamp and UUID to prevent overwrites. If capturing, attaching or persisting evidence fails, the log records the failure and exception while preserving the original scenario failure.

## Browsers, URL and Cucumber

Chrome is the default browser. Use `-Dbrowser=EDGE` for Edge and `-DbaseUrl=https://your-application` for a temporary URL. Use Cucumber tags such as `@smoke` with `-Dcucumber.filter.tags=@smoke` to select scenarios.

## Configuration inventory

For the five framework properties, precedence is JVM `-D` property, environment variable, then `config.properties`. `cucumber.filter.tags` is passed directly to Cucumber through `-D`. `javaVersion` is a Gradle (`-P`) property, not a JVM property.

| Property | Purpose | Default | Supported values | Example |
|---|---|---|---|---|
| `baseUrl` / `BASE_URL` | Initial URL of the system under test. | `https://example.com/` | Any non-blank URL. | `-DbaseUrl=https://example.com` or `$env:BASE_URL='https://example.com'` |
| `browser` / `BROWSER` | WebDriver browser. | `CHROME` | `CHROME`, `EDGE` (case-insensitive). | `-Dbrowser=EDGE` |
| `headless` / `HEADLESS` | Runs the browser without a window. | `false` | `true`, `false`. | `-Dheadless=true` |
| `timeoutSeconds` / `TIMEOUT_SECONDS` | Explicit page-wait timeout. | `15` | Integer usable by the framework. | `-DtimeoutSeconds=20` |
| `screenshotOnFailure` / `SCREENSHOT_ON_FAILURE` | Attempts to attach and persist PNG evidence for failed scenarios. | `true` | `true`, `false`. | `-DscreenshotOnFailure=false` |
| `cucumber.filter.tags` | Filters scenarios Cucumber executes. | No filter: all. | Valid Cucumber tag expression. | `"-Dcucumber.filter.tags=@example"` |
| `javaVersion` | Selects Gradle's Java toolchain. | `21` | Only `17` or `21`; every other value fails. | `-PjavaVersion=17` |

## CI/CD execution contract

GitHub Actions automatically validates pull requests targeting `main` before merge and pushes to `main`. The stable job/check is named `quality-gate`. A Gradle failure fails the check. The `main` ruleset requires a pull request and the `quality-gate` status check before merge. PASS, controlled FAIL, evidence in both outcomes, recovery to PASS, and a successful post-merge run on `main` have been validated. The workflow attempts to upload `test-evidence` even when tests fail, without changing the check result. See the [step-by-step CI/CD guide](docs/GUIA_USO_TEMPLATE_AUTOMATIZACION.md#cicd-con-github-actions) and [PDF manual](docs/Manual_Template_Automatizacion_Selenium_Java_Cucumber.pdf).

The GitHub Actions workflow runs:

```bash
./gradlew clean test -Dheadless=true
```

The workflow uses Temurin Java 21 and `gradle/actions/setup-gradle@v6` for caching. A cache miss is not an error: Gradle downloads the required dependencies and continues. The repository's Gradle Wrapper remains the execution method (`./gradlew`; `.\gradlew.bat` on Windows). Gradle exits with code `0` when the build and tests pass; any other code fails the check. Available evidence includes Gradle and Cucumber reports, JUnit XML results, logs, and screenshots when applicable. Use `-Dheadless=true` for local headless execution.

## Create and reuse

Create a feature, Page Object and Step Definitions in their respective folders, then run the wrapper. To start a project, clone/copy this template, change `rootProject.name` and `group`, configure `baseUrl`, replace the example and initialize Git. Do not store secrets in files; use environment variables or pipeline secrets.

For architecture, VS Code setup, CI/CD, first test tutorial and troubleshooting, read the Spanish [user guide](docs/GUIA_USO_TEMPLATE_AUTOMATIZACION.md). This repository is distributed under the [Apache License 2.0](LICENSE).

## Manual generation and temporary files

`scripts/create_manual.py` generates the PDF manual with ReportLab. It requires Python with `reportlab`; run `python scripts/create_manual.py` from the project root. It generates `docs/Manual_Template_Automatizacion_Selenium_Java_Cucumber.pdf` and retains an external project-directory copy.

`work/` contains temporary documentation/PDF-generation and validation files. It is ignored by Git, is not part of the final product, must not be versioned, and can be deleted without affecting the framework.

## Governance and release documentation

For the versioning policy and repeatable release procedure, see [Versioning](docs/VERSIONING.md) and the [Release process](docs/RELEASE_PROCESS.md). Before contributing, read [Contributing](CONTRIBUTING.md), the [Security policy](SECURITY.md), the [Code of Conduct](CODE_OF_CONDUCT.md), and the [Changelog](CHANGELOG.md).

## Release history

### v1.1.0 - October 1, 2026

**Milestone 3 Completed / Validated. Stable / Validated / Published.** Base CI, evidence artifacts, Gradle cache, and Quality Gate have been validated.

### v1.0.2 - September 25, 2026

**Documentation-only Hotfix. Stable / Validated / Published.** It corrects post-release state inconsistencies; it introduces no functional changes, dependency changes, CI/CD, Docker, Selenium Grid, Healenium, or Playwright.

### v1.0.1 - September 25, 2026

**Hardening + CI/CD Readiness. Stable / Validated / Published.** Native console/file logging, uniquely named persisted failure evidence, Cucumber screenshot attachment and documented artifact locations.

### v1.0.0 - September 17, 2026

**First Stable Release - Stable / Validated.** Generalized source project; reusable Web UI architecture with Java, Selenium, Cucumber, Gradle Wrapper and Page Object Model; Chrome/Edge, headless and `baseUrl` configuration; working example; bilingual documentation, diagrams, troubleshooting, migration report, documented CI/CD, manual-generation script and PDF. Docker and Healenium are not part of this template.

The template uses neutral documentation and examples so any team can adapt it to its Web UI application.
