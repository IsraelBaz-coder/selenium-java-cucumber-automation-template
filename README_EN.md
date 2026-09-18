# Automation Template Selenium Java Cucumber

Reusable Web UI test template based on Java 21, Selenium WebDriver, Cucumber BDD, JUnit Platform and Gradle. It includes a neutral `https://example.com` test as a reference; replace it with the system under test.

| Release | Value |
|---|---|
| Version | **v1.0.0** |
| Status | **Stable / Validated** |
| Type | **First Stable Release** |
| Date | **September 17, 2026** |

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
- Explicit waits, failure screenshots and Cucumber HTML reporting.

## Java version selection

Java 21 is the v1.0.0 default. The framework can compile with Java 17 or Java 21 through the Gradle `javaVersion` property:

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

Reports are at `build/reports/cucumber/cucumber.html`; failure screenshots are in `build/screenshots`.

## Browsers, URL and Cucumber

Chrome is the default browser. Use `-Dbrowser=EDGE` for Edge and `-DbaseUrl=https://your-application` for a temporary URL. Use Cucumber tags such as `@smoke` with `-Dcucumber.filter.tags=@smoke` to select scenarios.

## Create and reuse

Create a feature, Page Object and Step Definitions in their respective folders, then run the wrapper. To start a project, clone/copy this template, change `rootProject.name` and `group`, configure `baseUrl`, replace the example and initialize Git. Do not store secrets in files; use environment variables or pipeline secrets.

For architecture, VS Code setup, CI/CD, first test tutorial and troubleshooting, read the Spanish [user guide](docs/GUIA_USO_TEMPLATE_AUTOMATIZACION.md). No license was added because ownership must define it.

## CI/CD, manual generation and temporary files

Run the Gradle Wrapper headlessly in CI/CD and publish `build/reports` and `build/screenshots` as artifacts. The guide provides an example that needs corporate-infrastructure adaptation; it contains no internal runners, URLs or secrets.

`scripts/create_manual.py` generates the PDF manual with ReportLab. It requires Python with `reportlab`; run `python scripts/create_manual.py` from the project root. It generates `docs/Manual_Template_Automatizacion_Selenium_Java_Cucumber.pdf` and retains an external project-directory copy.

`work/` contains temporary documentation/PDF-generation and validation files. It is ignored by Git, is not part of the final product, must not be versioned, and can be deleted without affecting the framework.

## Release history

### v1.0.0 - September 17, 2026

**First Stable Release - Stable / Validated.** Generalized source project; reusable Web UI architecture with Java, Selenium, Cucumber, Gradle Wrapper and Page Object Model; Chrome/Edge, headless and `baseUrl` configuration; working example; bilingual documentation, diagrams, troubleshooting, migration report, documented CI/CD, manual-generation script and PDF. Docker and Healenium are not part of this template.

The template uses neutral documentation and examples so any team can adapt it to its Web UI application.
