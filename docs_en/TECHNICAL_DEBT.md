# Technical debt — Milestone 5, Block 3

[Español](../docs/TECHNICAL_DEBT.md) · [Index](README.md)

## TECH-001 — Selenium CDP compatibility

**Status: OPEN.** `build.gradle` pins Selenium 4.48.0; Docker pins Chrome and ChromeDriver 155.0.8059.39. The observed local run uses Chrome/CDP 153; Selenium Manager resolves the local driver. In both environments Selenium selects CDP 152 and emits a warning. There are no explicit DevTools, `executeCdpCommand`, or CDP API calls in `src/`; the smoke scenario uses standard WebDriver and passes.

**Impact:** the warning does not block the current scenario, but does not validate future CDP-dependent features. **Decision:** retain the current versions; do not add an arbitrary CDP module or blindly update the browser or Selenium. In a dedicated compatibility task, identify the CDP version supported by a candidate Selenium release, align browser and driver, test any actual DevTools use, and rerun the local and Docker suites until the warning disappears without regression. Do not hide the warning from logs.

## TECH-002 — Cucumber discovery selector

**Status: CLOSED after Block 3 local and Docker validation.** The warning came from `@SelectClasspathResource("features")` in `RunCucumberTest`: Cucumber/JUnit Platform requested a package selector. It was replaced by `@SelectPackages("features")`, retaining `@IncludeEngines("cucumber")`, glue, plugins, and the `src/test/resources/features/` layout.

**Evidence:** before the change, the local run showed two discovery warnings. Afterwards, the local headless, visible, and `@example` filtered suites ran 6/6 tests (one scenario) without that warning. The subsequent Docker run confirmed the same count and no warning. HTML/JSON and XML reports remained available. A GitHub Actions run for this branch awaits a PR.
