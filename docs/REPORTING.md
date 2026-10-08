# Reportes

[English](../docs_en/REPORTING.md) · [Índice](README.md)

v1.2.0 es la última versión publicada (8 de octubre de 2026); estado Stable / Validated / Published.


## Propósito

El reporting combina resultados funcionales, resultados técnicos y evidencia para reconstruir un fallo local o de CI. El runner JUnit Platform usa los plugins nativos `pretty`, `html` y `json` de Cucumber. Gradle y Logback conservan sus propias salidas. No se añadió una herramienta ni dependencia de reporting externa.


## Contrato de resultados

| Salida | Ruta | Uso |
|---|---|---|
| Cucumber HTML | `build/reports/cucumber/cucumber.html` | Escenarios, pasos y adjuntos. |
| Cucumber JSON | `build/reports/cucumber/cucumber.json` | Resultados y adjuntos estructurados. |
| Gradle/JUnit HTML | `build/reports/tests/test/` | Resumen técnico de `test`. |
| JUnit XML | `build/test-results/test/` | Resultado estructurado para CI/CD. |
| Logback | `build/logs/automation.log` | Eventos técnicos en orden temporal. |
| Capturas | `build/evidence/screenshots/` | PNG de fallos elegibles. |

Todas estas rutas están bajo `build/`, son regenerables y están ignoradas por Git. `pretty` muestra pasos en consola; no crea otro artifact. Cucumber HTML/JSON describen el escenario y sus pasos; Gradle HTML y JUnit XML describen el resultado de la ejecución de tests. El log registra ciclo del escenario y WebDriver. Cada salida tiene una responsabilidad distinta.


## Correlación y comportamiento PASS/FAIL

Busque el nombre del escenario y su estado en Cucumber HTML/JSON y `automation.log`; confirme el fallo técnico en JUnit XML o Gradle HTML. Ante un FAIL con `screenshotOnFailure=true` y WebDriver disponible, `EvidenceManager` guarda el PNG y lo adjunta al escenario como `image/png` antes de cerrar el navegador. El attachment queda en Cucumber HTML/JSON; el log registra captura, ruta y attachment. Si no se puede capturar, se registra un warning y el error original sigue siendo la causa del FAIL. Un PASS no genera screenshot de fallo tras `clean`.


## Uso local y regeneración

```powershell
.\gradlew.bat clean test -Dheadless=true
.\gradlew.bat clean test -Dheadless=false
.\gradlew.bat clean test -Dheadless=true "-Dcucumber.filter.tags=@example"
```

Abra los HTML en un navegador y use JSON/XML para procesamiento estructurado. `clean` elimina el contenido anterior de `build/`; copie o inspeccione la evidencia de un FAIL antes de repetir la ejecución. Los screenshots sólo aparecen en un fallo elegible, mientras que los reportes y el log se generan cuando los tests llegan a ejecutarse. La fixture HTML incluida permite validar el smoke test sin depender de una web externa; la preparación inicial de navegador o dependencias puede requerir red.


## CI/CD y troubleshooting

`.github/workflows/ci.yml` ejecuta el `quality-gate` headless con Java 21. `Upload test evidence` usa `if: always()` e incluye `build/reports/cucumber/`, por lo que HTML y JSON entran automáticamente en `test-evidence` junto con Gradle HTML, JUnit XML, logs y screenshots disponibles. No se cambió el workflow. Si falta HTML/JSON, compruebe que Gradle alcanzó `test`, el filtro de tags y los plugins del runner. Si falta el log, revise Logback; si falta un PNG, compruebe fallo de escenario, `screenshotOnFailure=true` y WebDriver activo. Un fallo de compilación anterior a `test` puede dejar artifacts incompletos.


## Seguridad y límites

No registre passwords, tokens, cookies, headers de autorización, secretos, variables de entorno completas ni URLs arbitrarias con parámetros sensibles. El framework registra navegador, modo headless, nombre y estado del escenario; no registra `baseUrl` ni bytes del screenshot. Una aplicación real puede mostrar datos sensibles en capturas, reportes o excepciones de terceros: revíselos antes de compartir artifacts. No hay dashboard histórico ni agregación entre ejecuciones; `clean` reemplaza los resultados locales.
