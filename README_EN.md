# Automation Template Selenium Java Cucumber

Reusable Web UI test template based on Java 21, Selenium WebDriver, Cucumber BDD, JUnit Platform and Gradle. It includes a neutral `https://example.com` test as a reference; replace it with the system under test.

| Release | Value |
|---|---|
| Internal version in preparation | **1.0.1** |
| Status | **In preparation; published baseline: v1.0.0** |
| Type | **Hardening and professional/CI readiness** |
| Stable baseline date | **September 17, 2026** |

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
- Explicit waits, execution logging, failure screenshots and Cucumber HTML reporting.

## Java version selection

Java 21 is the v1.0.1 default. The framework can compile with Java 17 or Java 21 through the Gradle `javaVersion` property:

| Purpose | PowerShell |
|---|---|
| Default Java (21) | `.\gradlew.bat test` |
| Use Java 17 | `.\gradlew.bat test -PjavaVersion=17` |
| Return to Java 21 | Omit `-PjavaVersion` or use `-PjavaVersion=21` |

Java 17 is the minimum supported version. Java 8 and Java 11 are not supported by the current code. Gradle itself must run with JDK 17 or later, and the selected toolchain must be installed or available to Gradle.

For the installation, `JAVA_HOME`, VS Code, validation and Java 21 rollback steps, read [Java version selection](docs/GUIA_USO_TEMPLATE_AUTOMATIZACION.md#selección-de-versión-de-java).

## Architecture and structure

```text
src/main/java/com/automation/template/{config,driver,pages}
src/test/java/com/automation/template/{hooks,runners,steps,support}
src/test/resources/{features,config.properties}
```

Features express Gherkin behavior; Steps translate intent; Page Objects encapsulate Selenium, locators and waits. Hooks manage browser lifecycle and the Runner connects Cucumber to JUnit Platform.

## Configuration and execution

`src/test/resources/config.properties` contains defaults. Priority is `-D`, environment variables (`BASE_URL`, `BROWSER`, `HEADLESS`) then file.

| Purpose | PowerShell |
|---|---|
| Clean | `.\gradlew.bat clean` |
| Run | `.\gradlew.bat test` |
| Clean and run | `.\gradlew.bat clean test` |
| Headless | `.\gradlew.bat test -Dheadless=true` |
| Chrome | `.\gradlew.bat test -Dbrowser=CHROME` |
| Edge | `.\gradlew.bat test -Dbrowser=EDGE` |
| URL | `.\gradlew.bat test -DbaseUrl=https://example.com` |
| Cucumber tags | `.\gradlew.bat test -Dcucumber.filter.tags=@example` |

## Evidence and reports

Each execution creates regenerable Git-ignored artifacts under `build/`:

| Artifact | Path |
|---|---|
| Cucumber HTML | `build/reports/cucumber/cucumber.html` |
| Gradle HTML | `build/reports/tests/test/` |
| JUnit XML | `build/test-results/test/` |
| Failure screenshots | `build/evidence/screenshots/` |
| Execution log | `build/logs/automation.log` |

Hooks log every scenario start and finish, browser, headless mode and driver lifecycle. If a scenario fails and `screenshotOnFailure=true`, they attempt to attach a PNG to the Cucumber scenario and persist it physically. The file name combines a sanitized scenario name, timestamp and UUID to prevent overwrites. If capturing, attaching or persisting evidence fails, the log records the failure and exception while preserving the original scenario failure.

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
| `javaVersion` | Selects Gradle's Java toolchain. | `21` | `17` or `21`; values below 17 fail. | `-PjavaVersion=17` |

## CI/CD execution contract

The standard entry point for a future pipeline is:

```powershell
.\gradlew.bat clean test
```

Gradle exits with code `0` when the build and tests succeed; a non-zero code means a build or test failure and must fail the job. For a displayless agent, use `-Dheadless=true`. It can be combined with `-Dbrowser=CHROME` or `-Dbrowser=EDGE`, the configuration properties above, and `"-Dcucumber.filter.tags=@example"`.

When they exist, a pipeline should collect `build/reports/cucumber/cucumber.html`, `build/reports/tests/test/`, `build/test-results/test/`, `build/logs/automation.log`, and `build/evidence/screenshots/`. The log is initialized during execution and records scenario lifecycle, driver activity, and evidence failures. Screenshots exist only when a scenario fails, the option is enabled, and the driver can capture them. This repository does not yet contain a CI/CD workflow.

## Create and reuse

Create a feature, Page Object and Step Definitions in their respective folders, then run the wrapper. To start a project, clone/copy this template, change `rootProject.name` and `group`, configure `baseUrl`, replace the example and initialize Git. Do not store secrets in files; use environment variables or pipeline secrets.

For architecture, VS Code setup, CI/CD, first test tutorial and troubleshooting, read the Spanish [user guide](docs/GUIA_USO_TEMPLATE_AUTOMATIZACION.md). This repository is distributed under the [Apache License 2.0](LICENSE).

## CI/CD, manual generation and temporary files

Run the Gradle Wrapper headlessly in CI/CD and publish `build/reports`, `build/evidence` and `build/logs` as artifacts. The guide documents the contract a future pipeline must adopt; it contains no workflow, internal runners, URLs, or secrets.

`scripts/create_manual.py` generates the PDF manual with ReportLab. It requires Python with `reportlab`; run `python scripts/create_manual.py` from the project root. It generates `docs/Manual_Template_Automatizacion_Selenium_Java_Cucumber.pdf` and retains an external project-directory copy.

`work/` contains temporary documentation/PDF-generation and validation files. It is ignored by Git, is not part of the final product, must not be versioned, and can be deleted without affecting the framework.

## Governance and release documentation

For the versioning policy and repeatable release procedure, see [Versioning](docs/VERSIONING.md) and the [Release process](docs/RELEASE_PROCESS.md). Before contributing, read [Contributing](CONTRIBUTING.md), the [Security policy](SECURITY.md), the [Code of Conduct](CODE_OF_CONDUCT.md), and the [Changelog](CHANGELOG.md).

## Release history

### v1.0.1 - In preparation

**Hardening + CI/CD Readiness.** Native console/file logging, uniquely named persisted failure evidence, Cucumber screenshot attachment and documented artifact locations. This version has not been published or tagged yet.

### v1.0.0 - September 17, 2026

**First Stable Release - Stable / Validated.** Generalized source project; reusable Web UI architecture with Java, Selenium, Cucumber, Gradle Wrapper and Page Object Model; Chrome/Edge, headless and `baseUrl` configuration; working example; bilingual documentation, diagrams, troubleshooting, migration report, documented CI/CD, manual-generation script and PDF. Docker and Healenium are not part of this template.

The template uses neutral documentation and examples so any team can adapt it to its Web UI application.
