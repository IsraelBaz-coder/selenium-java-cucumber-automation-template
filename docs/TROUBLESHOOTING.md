# Troubleshooting

[English](../docs_en/TROUBLESHOOTING.md) · [Índice](README.md)

**Última versión publicada:** v1.2.0 (8 de octubre de 2026). Estado: Stable / Validated / Published.

| Síntoma | Causa probable | Solución |
|---|---|---|
| `java` no reconocido | JDK/Path incorrecto | Instale JDK 21 o 17, reinicie PowerShell y valide `java -version`. |
| Java incorrecto | VS Code/Gradle usa otro JDK | Configure `JAVA_HOME` al JDK elegido y revise `./gradlew.bat --version`; sólo se admiten `-PjavaVersion=17` o `-PjavaVersion=21`. |
| Wrapper no ejecuta | Ruta/permisos | Ejecute desde raíz: `.\gradlew.bat test`; preserve `gradle/wrapper`. |
| Dependencias no descargan | Red, proxy o Maven Central bloqueado | Revise red/proxy y ejecute desde la raíz `.\gradlew.bat dependencies --refresh-dependencies`. |
| Chrome/Edge no inicia | Navegador/driver | Actualice navegador y revise salida Selenium Manager. |
| Error WebDriver | Driver no creado/cerrado | Revise Hooks y `browser`; no use driver fuera del escenario. |
| Headless falla | Entorno restringido | Use `-Dheadless=true`; revise permisos y tamaño de ventana. |
| Feature no ejecuta | Ruta/extensión/tags | Use `.feature` bajo `src/test/resources/features`; valide tags. |
| Step no encontrado | Texto/glue no coincide | Haga coincidir Gherkin/anotación y conserve el glue `com.automation.template`. |
| CI falla, local no | Configuración diferente | Compare `-D`, variables de entorno y navegador; ejecute `-Dheadless=true` y recolecte los artifacts documentados. |
| No se ejecuta el tag esperado | Expresión o propagación incorrecta | Verifique el tag en la feature y ejecute `"-Dcucumber.filter.tags=@example"`; el tag incluido actualmente es `@example`. |
| No encuentro un reporte | Se busca una ruta incorrecta o el build falló antes de reportar | Revise `build/reports/cucumber/cucumber.html`, `build/reports/cucumber/cucumber.json`, `build/reports/tests/test/` y `build/test-results/test/`. |
| No aparece el log | La tarea `test` no llegó a ejecutar escenarios, o se consultó una ruta anterior a `clean` | Revise la consola, `build/logs/automation.log` y la [guía de logging](LOGGING.md). |
| No hay screenshot | No ocurrió fallo, la opción está desactivada o el driver no puede capturar | Revise `screenshotOnFailure`, `build/evidence/screenshots/` y `build/logs/automation.log`. |
| `quality-gate` falla en un PR | Compilación, pruebas o preparación del runner fallaron | Abra el PR → **Checks** → `quality-gate` → **Details**; identifique el step fallido y consulte los logs. Descargue `test-evidence` desde **Actions** si existe. Corrija en su rama, pruebe localmente y envíe un nuevo commit para repetir el check. |
| No aparece `test-evidence` | Gradle no generó archivos o la carga no llegó a ejecutarse | Abra la ejecución en **Actions**, revise **Upload test evidence** y las rutas `build/` indicadas en la [guía](GUIA_USO_TEMPLATE_AUTOMATIZACION.md#cómo-descargar-las-evidencias-de-github-actions). Las capturas pueden faltar sin escenarios fallidos. |

## Diagnóstico de Gradle y dependencias

`./gradlew.bat --stop` detiene los Gradle Daemons y puede utilizarse ante problemas transitorios del daemon; no forma parte de la ejecución normal.

Para aislar problemas de resolución puede ejecutar `./gradlew.bat clean test --offline` o `./gradlew.bat clean test -PjavaVersion=21 --offline`. `--offline` obliga a Gradle a usar dependencias que ya estén en caché; sirve para diagnóstico, no sustituye una ejecución normal con acceso a repositorios y puede fallar si faltan dependencias descargadas.

Si la resolución muestra `PKIX path building failed` o `unable to find valid certification path to requested target`, revise el certificado de Java, proxy corporativo, inspección SSL, red o el estado temporal del Gradle Daemon. Como diagnóstico seguro ejecute `java -version`, `./gradlew.bat --version`, `./gradlew.bat --stop` y después `./gradlew.bat clean test`. Puede comprobar conectividad con `Invoke-WebRequest https://repo.maven.apache.org/maven2/ -UseBasicParsing`. No deshabilite SSL, no use HTTP ni ignore certificados.

Consulte [Reporting](REPORTING.md) para el contrato validado de reportes y el diagnóstico de Cucumber JSON.
