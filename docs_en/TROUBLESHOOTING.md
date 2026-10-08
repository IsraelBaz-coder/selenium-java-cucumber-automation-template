# Troubleshooting

[Español](../docs/TROUBLESHOOTING.md) · [English index](README.md)

**Latest published release:** v1.2.0 (October 8, 2026). Stable / Validated / Published.

| Symptom | Likely cause | Action |
|---|---|---|
| `java` not found | JDK or PATH | Install JDK 21 or 17, reopen the terminal, run `java -version`. |
| Wrong Java version | VS Code or Gradle uses another JDK | Set `JAVA_HOME`, inspect `.\gradlew.bat --version`, use `-PjavaVersion=17` or `21`. |
| Wrapper does not run | Directory or permissions | Run `.\gradlew.bat test` at repository root; keep `gradle/wrapper`. |
| Dependencies fail to download | Network, proxy, Maven Central | Inspect connectivity and proxy; try `.\gradlew.bat dependencies --refresh-dependencies`. |
| Chrome or Edge fails to start | Browser or driver | Update the browser and inspect Selenium Manager output. |
| WebDriver error | Missing or closed driver | Inspect hooks and `browser`; do not use a driver after the scenario. |
| Headless execution fails | Restricted environment | Pass `-Dheadless=true`; inspect permissions and window configuration. |
| Feature not discovered | Path, extension, tags | Put `.feature` under `src/test/resources/features`; inspect tags. |
| Step undefined | Text or glue mismatch | Match Gherkin to the annotation; retain `com.automation.template` glue. |
| CI fails but local passes | Different configuration | Compare properties, environment, browser; run headless and inspect artifacts. |
| Tag filter excludes the test | Expression or forwarding | Use `"-Dcucumber.filter.tags=@example"`; the included tag is `@example`. |
| Report missing | Wrong path or early build failure | Inspect Cucumber HTML/JSON, Gradle HTML, and JUnit XML paths in [reporting](REPORTING.md). |
| Log missing | `test` never started or `clean` removed it | Inspect console and `build/logs/automation.log`. |
| Screenshot missing | No eligible failure, disabled option, or unavailable driver | Inspect `screenshotOnFailure`, log, and `build/evidence/screenshots/`. |
| PR `quality-gate` fails | Build, test, or runner setup | Open PR Checks → quality-gate → Details; inspect the failed step and available artifact. |
| `test-evidence` absent | No generated files or upload did not run | Inspect Actions → Upload test evidence; passing runs need no screenshots. |

## Gradle and dependency diagnostics

`.\gradlew.bat --stop` can clear a transient daemon problem. `--offline` isolates cached dependency resolution, but may fail when packages are missing. For `PKIX path building failed`, inspect the JDK trust store, proxy, TLS inspection, network, and daemon. Run `java -version`, `.\gradlew.bat --version`, `.\gradlew.bat --stop`, then the normal test command. Do not disable TLS verification. See [logging](LOGGING.md) and [reporting](REPORTING.md).
