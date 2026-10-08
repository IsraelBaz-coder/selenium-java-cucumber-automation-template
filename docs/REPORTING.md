# Reporting / Reportes — Hito 4, Bloque 3 (Completed / Validated)

**ES:** v1.1.0 sigue Stable / Validated / Published (1 de octubre de 2026) y Hito 3 Completed / Validated. v1.2.0 y Hito 4 siguen In Development, no publicados y sin fecha oficial. Bloques 1, 2 y 3 Completed / Validated; bloques posteriores Pending.

**EN:** v1.1.0 remains Stable / Validated / Published (October 1, 2026) and Milestone 3 Completed / Validated. v1.2.0 and Milestone 4 remain In Development, unpublished and without an official date. Blocks 1, 2 and 3 Completed / Validated; later blocks Pending.

## Propósito / Purpose

**ES:** El reporting combina resultados funcionales, resultados técnicos y evidencia para reconstruir un fallo local o de CI. El runner JUnit Platform usa los plugins nativos `pretty`, `html` y `json` de Cucumber. Gradle y Logback conservan sus propias salidas. No se añadió una herramienta ni dependencia de reporting externa.

**EN:** Reporting combines functional results, technical results and evidence to reconstruct a local or CI failure. The JUnit Platform runner uses Cucumber's native `pretty`, `html` and `json` plugins. Gradle and Logback retain their own outputs. No external reporting tool or dependency was added.

## Contrato de resultados / Output contract

| Salida / Output | Ruta / Path | Uso / Use |
|---|---|---|
| Cucumber HTML | `build/reports/cucumber/cucumber.html` | Vista de Features, Scenarios, Steps y attachments / visual feature, scenario, step and attachment report. |
| Cucumber JSON | `build/reports/cucumber/cucumber.json` | Resultado estructurado y attachments para procesamiento futuro / structured result and attachments for future processing; complementa el HTML / complements HTML. |
| Gradle/JUnit HTML | `build/reports/tests/test/` | Resumen técnico de la tarea `test` / technical `test` task summary. |
| JUnit XML | `build/test-results/test/` | Resultado estructurado para CI/CD / structured CI/CD result. |
| Logback | `build/logs/automation.log` | Eventos técnicos en orden temporal / chronological technical events. |
| Screenshots | `build/evidence/screenshots/` | PNG visual de fallos elegibles / visual PNG for eligible failures. |

**ES:** Todas estas rutas están bajo `build/`, son regenerables y están ignoradas por Git. `pretty` muestra pasos en consola; no crea otro artifact. Cucumber HTML/JSON describen el escenario y sus pasos; Gradle HTML y JUnit XML describen el resultado de la ejecución de tests. El log registra ciclo del escenario y WebDriver. Cada salida tiene una responsabilidad distinta.

**EN:** All paths are under `build/`, regenerable and Git-ignored. `pretty` prints steps to the console; it creates no extra artifact. Cucumber HTML/JSON describe scenario and steps; Gradle HTML and JUnit XML describe test execution. The log records scenario and WebDriver lifecycle. Each output serves a separate purpose.

## Correlación y comportamiento PASS/FAIL / Correlation and PASS/FAIL behavior

**ES:** Busque el nombre del escenario y su estado en Cucumber HTML/JSON y `automation.log`; confirme el fallo técnico en JUnit XML o Gradle HTML. Ante un FAIL con `screenshotOnFailure=true` y WebDriver disponible, `EvidenceManager` guarda el PNG y lo adjunta al escenario como `image/png` antes de cerrar el navegador. El attachment queda en Cucumber HTML/JSON; el log registra captura, ruta y attachment. Si no se puede capturar, se registra un warning y el error original sigue siendo la causa del FAIL. Un PASS no genera screenshot de fallo tras `clean`.

**EN:** Match scenario name and status across Cucumber HTML/JSON and `automation.log`; confirm the technical failure in JUnit XML or Gradle HTML. On FAIL with `screenshotOnFailure=true` and an available WebDriver, `EvidenceManager` saves a PNG and attaches it to the scenario as `image/png` before closing the browser. The attachment appears in Cucumber HTML/JSON; the log records capture, path and attachment. If capture fails, a warning is logged and the original error remains the failure cause. A PASS creates no failure screenshot after `clean`.

## Uso local y regeneración / Local use and regeneration

```powershell
.\gradlew.bat clean test -Dheadless=true --offline
.\gradlew.bat clean test -Dheadless=false --offline
.\gradlew.bat clean test -Dheadless=true "-Dcucumber.filter.tags=@example" --offline
```

**ES:** Abra los HTML en un navegador y use JSON/XML para procesamiento estructurado. `clean` elimina el contenido anterior de `build/`; copie o inspeccione la evidencia de un FAIL antes de repetir la ejecución. Los screenshots sólo aparecen en un fallo elegible, mientras que los reportes y el log se generan cuando los tests llegan a ejecutarse. La fixture HTML incluida permite validar el smoke test sin depender de una web externa; la preparación inicial de navegador o dependencias puede requerir red.

**EN:** Open HTML reports in a browser and use JSON/XML for structured processing. `clean` deletes prior `build/` contents; copy or inspect FAIL evidence before rerunning. Screenshots appear only for eligible failures, while reports and log are generated when tests run. The included HTML fixture validates the smoke test without an external website; initial browser or dependency setup may require network access.

## CI/CD y troubleshooting / CI/CD and troubleshooting

**ES:** `.github/workflows/ci.yml` ejecuta el `quality-gate` headless con Java 21. `Upload test evidence` usa `if: always()` e incluye `build/reports/cucumber/`, por lo que HTML y JSON entran automáticamente en `test-evidence` junto con Gradle HTML, JUnit XML, logs y screenshots disponibles. No se cambió el workflow. Si falta HTML/JSON, compruebe que Gradle alcanzó `test`, el filtro de tags y los plugins del runner. Si falta el log, revise Logback; si falta un PNG, compruebe fallo de escenario, `screenshotOnFailure=true` y WebDriver activo. Un fallo de compilación anterior a `test` puede dejar artifacts incompletos.

**EN:** `.github/workflows/ci.yml` runs the headless `quality-gate` with Java 21. `Upload test evidence` uses `if: always()` and includes `build/reports/cucumber/`, so HTML and JSON automatically enter `test-evidence` with available Gradle HTML, JUnit XML, logs and screenshots. The workflow was unchanged. If HTML/JSON is missing, check whether Gradle reached `test`, the tag filter and runner plugins. If the log is missing, inspect Logback; if a PNG is missing, check scenario failure, `screenshotOnFailure=true` and an active WebDriver. A compilation failure before `test` may leave incomplete artifacts.

## Seguridad y límites / Security and limits

**ES:** No registre passwords, tokens, cookies, headers de autorización, secretos, variables de entorno completas ni URLs arbitrarias con parámetros sensibles. El framework registra navegador, modo headless, nombre y estado del escenario; no registra `baseUrl` ni bytes del screenshot. Una aplicación real puede mostrar datos sensibles en capturas, reportes o excepciones de terceros: revíselos antes de compartir artifacts. No hay dashboard histórico ni agregación entre ejecuciones; `clean` reemplaza los resultados locales.

**EN:** Do not log passwords, tokens, cookies, authorization headers, secrets, full environment variables or arbitrary URLs with sensitive parameters. The framework logs browser, headless mode, scenario name and status; it does not log `baseUrl` or screenshot bytes. A real application may expose sensitive data in screenshots, reports or third-party exceptions: review artifacts before sharing. There is no historical dashboard or aggregation across runs; `clean` replaces local results.
