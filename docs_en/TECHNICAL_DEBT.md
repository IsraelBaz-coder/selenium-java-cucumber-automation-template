# Open technical debt

[Español](../docs/TECHNICAL_DEBT.md) · [Index](README.md)

Warnings observed while running the development v1.3.0 Docker image. The local suite ended with BUILD SUCCESSFUL and the Example Domain scenario PASSED; the warnings did not fail the suite. Both entries remain OPEN during Block 2. A later block must address them; dependencies and the runner stay unchanged here.

## TECH-001 — Selenium CDP compatibility

| Field | Record |
|---|---|
| Status / priority | **OPEN / MEDIUM** |
| Description | Chrome 155 starts, but Selenium 4.48.0 selects a nearby CDP module instead of an exact match for this browser version. |
| Evidence | Stderr: “Unable to find an exact match for CDP version 155, returning the closest version; found: 152”. Reproduced by Codex in the Docker bind-mount run; the user also reported it. WebDriver initialized and the scenario passed. |
| Probable cause | A gap between Chrome 155 and the CDP modules bundled with the current Selenium version. Confirm during dependency evaluation. |
| Potential impact | DevTools/CDP-dependent features may behave differently or fail; the current smoke test does not prove compatibility of all such features. |
| Candidate solution | Evaluate a compatible Selenium version and matching CDP module without changing versions in this block. |
| Regression checks | Run the smoke and full suite with aligned Chrome/ChromeDriver; verify WebDriver startup, local and Docker headless tests, reports/evidence, and any actual CDP use. Confirm the warning disappears without new failures. |
| Proposed later block | A later dependency-compatibility block, subject to authorization and tests; not Block 1. |

## TECH-002 — Cucumber discovery selector

| Field | Record |
|---|---|
| Status / priority | **OPEN / LOW** |
| Description | The runner selects the `features` classpath resource; Cucumber/JUnit recommends a package selector for this case. |
| Evidence | Stderr: “The classpath resource selector 'features' should not be used to select features in a package.” Reported twice during discovery in Codex's Docker run; the user also reported it. The scenario was discovered and passed. |
| Probable cause | `@SelectClasspathResource("features")` in `RunCucumberTest` does not match the current engine's recommendation. |
| Impact | Non-critical warning; possible fragility in future Feature discovery. The current scenario did not fail. |
| Candidate solution | Review runner configuration and the selector recommended by Cucumber/JUnit; do not change the runner in this block. |
| Regression checks | Confirm discovery and count of all Features, tag filters, local and Docker Gradle/JUnit runs, Cucumber HTML/JSON reports, and CI result. |
| Proposed later block | A later runner-maintenance block, subject to authorization and tests; not Block 1. |
