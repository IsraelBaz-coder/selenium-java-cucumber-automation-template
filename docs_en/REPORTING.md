# Reporting

[Español](../docs/REPORTING.md) · [English index](README.md)

**Latest published release:** v1.2.0 (October 8, 2026). Stable / Validated / Published.

## Purpose and output contract

The JUnit Platform runner uses Cucumber's native `pretty`, `html`, and `json` plugins; Gradle and Logback provide their own output. No external reporting dependency or historical dashboard is implemented.

| Output | Path | Use |
|---|---|---|
| Cucumber HTML | `build/reports/cucumber/cucumber.html` | Scenarios, steps, attachments. |
| Cucumber JSON | `build/reports/cucumber/cucumber.json` | Structured scenarios and attachments. |
| Gradle/JUnit HTML | `build/reports/tests/test/` | Technical test summary. |
| JUnit XML | `build/test-results/test/` | Structured CI results. |
| Logback | `build/logs/automation.log` | Chronological technical events. |
| Screenshots | `build/evidence/screenshots/` | PNGs for eligible failures. |

All paths are generated under ignored `build/`. `pretty` prints to console. Match the scenario name and status across Cucumber HTML/JSON and the log; confirm technical failures in XML or Gradle HTML. With `screenshotOnFailure=true` and an active driver, the PNG and `image/png` attachment appear before browser shutdown. A capture failure does not replace the original test failure. A passing run after `clean` produces no failure PNG.

Run `.\gradlew.bat clean test -Dheadless=true` or `-Dheadless=false`; optionally pass `"-Dcucumber.filter.tags=@example"`. Inspect results before another `clean`. The local HTML fixture avoids reliance on an external test page, although first browser/dependency setup can require network access.

GitHub Actions runs the Java 21 headless `quality-gate` and attempts to upload available results as `test-evidence` with `if: always()`. It excludes `build/test-results/test/binary/`, which contains Gradle internal data. The `docker-tests` job copies only those diagnostic outputs plus `container.log`, also excluding `binary/`. An early compilation failure can leave an artifact incomplete. If a report is absent, inspect whether `test` started, the tag filter, and runner plugins. For missing logs inspect Logback; for missing PNGs inspect scenario status, capture setting, and driver availability. Review screenshots, reports, and exception traces for sensitive application data before sharing.
