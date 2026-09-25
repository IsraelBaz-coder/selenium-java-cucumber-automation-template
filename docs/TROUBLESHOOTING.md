# Troubleshooting

**Baseline estable:** v1.0.0 · **Versión en preparación:** v1.0.1 (Hardening + CI/CD Readiness)

| Síntoma | Causa probable | Solución |
|---|---|---|
| `java` no reconocido | JDK/Path incorrecto | Instale JDK 21 o 17, reinicie PowerShell y valide `java -version`. |
| Java incorrecto | VS Code/Gradle usa otro JDK | Configure `JAVA_HOME` al JDK elegido y revise `./gradlew.bat --version`; sólo se admiten `-PjavaVersion=17` o `-PjavaVersion=21`. |
| Wrapper no ejecuta | Ruta/permisos | Ejecute desde raíz: `.\gradlew.bat test`; preserve `gradle/wrapper`. |
| Dependencias no descargan | Red, proxy o Maven bloqueado | Revise red/proxy y ejecute `dependencies --refresh-dependencies`. |
| Chrome/Edge no inicia | Navegador/driver | Actualice navegador y revise salida Selenium Manager. |
| Error WebDriver | Driver no creado/cerrado | Revise Hooks y `browser`; no use driver fuera del escenario. |
| Headless falla | Entorno restringido | Use `-Dheadless=true`; revise permisos y tamaño de ventana. |
| Feature no ejecuta | Ruta/extensión/tags | Use `.feature` bajo `src/test/resources/features`; valide tags. |
| Step no encontrado | Texto/glue no coincide | Haga coincidir Gherkin/anotación y conserve el glue `com.automation.template`. |
| CI falla, local no | Configuración diferente | Compare `-D`, variables de entorno y navegador; ejecute `-Dheadless=true` y recolecte los artifacts documentados. |
| No se ejecuta el tag esperado | Expresión o propagación incorrecta | Verifique el tag en la feature y ejecute `"-Dcucumber.filter.tags=@example"`; el tag incluido actualmente es `@example`. |
| No encuentro un reporte | Se busca una ruta incorrecta o el build falló antes de reportar | Revise `build/reports/cucumber/cucumber.html`, `build/reports/tests/test/` y `build/test-results/test/`. |
| No hay screenshot | No ocurrió fallo, la opción está desactivada o el driver no puede capturar | Revise `screenshotOnFailure`, `build/evidence/screenshots/` y `build/logs/automation.log`. |

## Diagnóstico de Gradle y dependencias

`./gradlew.bat --stop` detiene los Gradle Daemons y puede utilizarse ante problemas transitorios del daemon; no forma parte de la ejecución normal.

Para aislar problemas de resolución puede ejecutar `./gradlew.bat clean test --offline` o `./gradlew.bat clean test -PjavaVersion=21 --offline`. `--offline` obliga a Gradle a usar dependencias que ya estén en caché; sirve para diagnóstico, no sustituye una ejecución normal con acceso a repositorios y puede fallar si faltan dependencias descargadas.

Si la resolución muestra `PKIX path building failed` o `unable to find valid certification path to requested target`, revise el certificado de Java, proxy corporativo, inspección SSL, red o el estado temporal del Gradle Daemon. Como diagnóstico seguro ejecute `java -version`, `./gradlew.bat --version`, `./gradlew.bat --stop` y después `./gradlew.bat clean test`. Puede comprobar conectividad con `Invoke-WebRequest https://repo.maven.apache.org/maven2/ -UseBasicParsing`. No deshabilite SSL, no use HTTP ni ignore certificados.
