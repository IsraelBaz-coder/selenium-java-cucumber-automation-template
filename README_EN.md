# Automation Template Selenium Java Cucumber

[Español](README_ES.md) · [Language selection](README.md)

Reusable Web UI test template based on Java 21, Selenium WebDriver, Cucumber BDD, JUnit Platform and Gradle. It includes a smoke test using a local HTML page in `src/test/resources/fixtures/`; the scenario does not depend on external website content. Initial dependency and browser setup may still require network access. Configure your application URL and replace the example when adapting the template.

| Release | Value |
|---|---|
| Published stable version | **v1.2.0** |
| Current release | **v1.2.0 — Stable / Validated / Published** |
| v1.2.0 status | **Stable / Validated / Published** |
| v1.2.0 publication date | **October 8, 2026** |

v1.2.0 is the latest published release (October 8, 2026). It includes SLF4J/Logback logging, automatic failure evidence and Cucumber HTML/JSON reports. Its status is **Stable / Validated / Published**. See the [audit report](docs_en/HITO4_RELEASE_AUDIT.md) for validation results.

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
- Explicit waits, SLF4J/Logback execution logging, failure screenshots and Cucumber HTML/JSON reporting.

## Java version selection

Java 21 is the default in the current configuration. The only supported toolchains are Java 17 and Java 21, selected through the Gradle `javaVersion` property:

| Purpose | PowerShell |
|---|---|
| Default Java (21) | `.\gradlew.bat clean test` |
| Use Java 17 | `.\gradlew.bat clean test -PjavaVersion=17` |
| Explicit Java 21 | `.\gradlew.bat clean test -PjavaVersion=21` |

Java 17 is the only supported alternative. `-PjavaVersion=18`, `19`, `20`, `22`, and every value other than `17` or `21` are rejected with a `GradleException`. Gradle itself must run with JDK 17 or later, and the selected toolchain must be installed or available to Gradle.

For the installation, `JAVA_HOME`, VS Code, validation and Java 21 rollback steps, read [Java version selection](docs_en/GUIA_USO_TEMPLATE_AUTOMATIZACION.md#java-version-selection).

## Architecture and structure

```text
src/main/java/com/automation/template/{config,driver,pages}
src/test/java/com/automation/template/{hooks,runners,steps,support}
src/test/resources/{features,config.properties}
```

Features express Gherkin behavior; Steps translate intent; Page Objects encapsulate Selenium, locators and waits. Hooks manage browser lifecycle and the Runner connects Cucumber to JUnit Platform.

See [architecture](docs_en/ARCHITECTURE.md), the [usage guide](docs_en/GUIA_USO_TEMPLATE_AUTOMATIZACION.md), [logging and its diagrams](docs_en/LOGGING.md), and [troubleshooting](docs_en/TROUBLESHOOTING.md).

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
| Cucumber JSON | `build/reports/cucumber/cucumber.json` |
| Gradle HTML | `build/reports/tests/test/` |
| JUnit XML | `build/test-results/test/` |
| Failure screenshots | `build/evidence/screenshots/` |
| Execution log | `build/logs/automation.log` |

The `build/reports/cucumber/cucumber.json` output is implemented and validated. See the [reporting contract](docs_en/REPORTING.md) for its relationship to HTML, XML, logs and screenshots.

Hooks log scenario start, finish and status; `DriverFactory` and `DriverManager` log the driver lifecycle. On failure with `screenshotOnFailure=true`, the Hook delegates to `EvidenceManager` before quitting the browser. The manager saves a PNG with a sanitized name, timestamp and UUID, and attaches it to Cucumber as `image/png`. A missing driver or capture failure produces a warning without replacing the original failure. See [Evidence](docs_en/EVIDENCE.md) for the flow, location and manual validation, and [Logging](docs_en/LOGGING.md) for SLF4J/Logback events.

## Browsers, URL and Cucumber

The development v1.3.0 Docker base image includes Java 21, Chrome and ChromeDriver 155 for Linux amd64, and uses the Gradle Wrapper. On Windows, start Docker Desktop with WSL2 and its Linux engine; from the repository root run `docker build --progress=plain -t selenium-java-cucumber-template:1.3.0-dev .` and `docker run --rm selenium-java-cucumber-template:1.3.0-dev`. See the [step-by-step Docker guide](docs_en/DOCKER.md) for version checks, interpreting BUILD SUCCESSFUL, troubleshooting, and retaining reports with a verified mount. The user confirmed the build and run; Codex verified a mounted run. Non-critical warnings are tracked in [TECH-001/002](docs_en/TECHNICAL_DEBT.md). v1.2.0 remains the latest published release.

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

GitHub Actions automatically validates pull requests targeting `main` before merge and pushes to `main`. The stable job/check is named `quality-gate`. A Gradle failure fails the check. The `main` ruleset requires a pull request and the `quality-gate` status check before merge. PASS, controlled FAIL, evidence in both outcomes, recovery to PASS, and a successful post-merge run on `main` have been validated. The workflow attempts to upload `test-evidence` even when tests fail, without changing the check result. See the [step-by-step CI/CD guide](docs_en/GUIA_USO_TEMPLATE_AUTOMATIZACION.md#cicd-and-quality-gate) and [PDF manual](docs_en/Manual_Selenium_Java_Cucumber_Automation_Template.pdf).

The GitHub Actions workflow runs:

```bash
./gradlew clean test -Dheadless=true
```

The workflow uses Temurin Java 21 and `gradle/actions/setup-gradle@v6` for caching. A cache miss is not an error: Gradle downloads the required dependencies and continues. The repository's Gradle Wrapper remains the execution method (`./gradlew`; `.\gradlew.bat` on Windows). Gradle exits with code `0` when the build and tests pass; any other code fails the check. Available evidence includes Gradle and Cucumber reports, JUnit XML results, logs, and screenshots when applicable. Use `-Dheadless=true` for local headless execution.

The same workflow adds `docker-tests`: it builds the existing Dockerfile, runs `./gradlew --no-daemon test -Dheadless=true` in the container, and retains its log and `build/` through `docker cp`. The test exit code determines the job result. When files exist, `docker-test-evidence` uploads even on failure and is retained for 14 days. See [Docker in CI](docs_en/DOCKER.md#docker-in-github-actions) for the workflow, both jobs, logs, and artifacts. This Block 2 job needs a real GitHub Actions run before it can be called validated. `v1.3.0` is a development target, not a published release.

## Create and reuse

Create a feature, Page Object and Step Definitions in their respective folders, then run the wrapper. To start a project, clone/copy this template, change `rootProject.name` and `group`, configure `baseUrl`, replace the example and initialize Git. Do not store secrets in files; use environment variables or pipeline secrets.

For architecture, VS Code setup, CI/CD, first test tutorial and troubleshooting, read the English [user guide](docs_en/GUIA_USO_TEMPLATE_AUTOMATIZACION.md). This repository is distributed under the [Apache License 2.0](LICENSE).

## Manual generation and temporary files

`scripts/create_manual.py` generates the PDF manual with ReportLab. It requires Python with `reportlab`; run `python scripts/create_manual.py` from the project root. It updates `docs_en/Manual_Selenium_Java_Cucumber_Automation_Template.pdf` and the Spanish manual in `docs/Manual_Template_Automatizacion_Selenium_Java_Cucumber.pdf`. The `--output` option writes only to the specified path for temporary validation.

`work/` contains temporary documentation/PDF-generation and validation files. It is ignored by Git, is not part of the final product, must not be versioned, and can be deleted without affecting the framework.

## Governance and release documentation

For the versioning policy and repeatable release procedure, see [Versioning](docs_en/VERSIONING.md) and the [Release process](docs_en/RELEASE_PROCESS.md). Before contributing, read [Contributing](CONTRIBUTING.md), the [Security policy](SECURITY.md), the [Code of Conduct](CODE_OF_CONDUCT.md), and the [Changelog](CHANGELOG.md).

## Release history

### v1.2.0 - October 8, 2026

**Stable / Validated / Published.** Logging, evidence and reporting are integrated. Validation is recorded in the [release audit](docs_en/HITO4_RELEASE_AUDIT.md).

### v1.1.0 - October 1, 2026

**Stable / Validated / Published.** Base CI, evidence artifacts, Gradle cache, and Quality Gate have been validated.

### v1.0.2 - September 26, 2026

**Documentation-only Hotfix. Stable / Validated / Published.** It corrects post-release state inconsistencies; it introduces no functional changes, dependency changes, CI/CD, Docker, Selenium Grid, Healenium, or Playwright.

### v1.0.1 - September 25, 2026

**Hardening + CI/CD Readiness. Stable / Validated / Published.** Native console/file logging, uniquely named persisted failure evidence, Cucumber screenshot attachment and documented artifact locations.

### v1.0.0 - September 18, 2026

**First Stable Release - Stable / Validated / Published.** Generalized source project; reusable Web UI architecture with Java, Selenium, Cucumber, Gradle Wrapper and Page Object Model; Chrome/Edge, headless and `baseUrl` configuration; working example; bilingual documentation, diagrams, troubleshooting, migration report, documented CI/CD, manual-generation script and PDF. Docker and Healenium were not part of v1.0.0.

The template uses neutral documentation and examples so any team can adapt it to its Web UI application.
