# Automation Template Selenium Java Cucumber

Template reutilizable para pruebas Web UI con Java 21, Selenium WebDriver, Cucumber BDD, JUnit Platform y Gradle. Incluye un smoke test con una página HTML local en `src/test/resources/fixtures/`; el escenario no depende del contenido de una web externa. La primera preparación de dependencias y del navegador puede requerir conexión. Para probar una aplicación real, configure su URL y sustituya el ejemplo.

| Release | Valor |
|---|---|
| Versión estable publicada | **v1.2.0** |
| Versión vigente | **v1.2.0 — Stable / Validated / Published** |
| Estado de v1.2.0 | **Stable / Validated / Published** |
| Fecha de publicación de v1.2.0 | **8 de octubre de 2026** |

v1.2.0 es la última versión publicada (8 de octubre de 2026). Incorpora logging con SLF4J/Logback, evidencias automáticas ante fallos y reportes Cucumber HTML/JSON. Su estado es **Stable / Validated / Published**. Consulte el [informe de auditoría](docs/HITO4_RELEASE_AUDIT.md) para los resultados de validación.

| Información del documento | Valor |
|---|---|
| Autor / Creador del template | Israel Baz |
| Rol | Test Automation / Prompt Engineering / AI Automation |
| Mantenimiento | Israel Baz |

El template fue validado y puede utilizarse como baseline para nuevos proyectos. Configure los valores específicos de cada aplicación mediante propiedades, variables de entorno o parámetros `-D`; las nuevas capacidades deben incorporarse en versiones posteriores.

## Características

- Java 21 predeterminado, Java 17 compatible, Gradle Wrapper y codificación UTF-8.
- Page Object Model, Steps y Hooks separados.
- Chrome/Edge, modo headless y URL configurables por archivo, variable de entorno o `-D`.
- Esperas explícitas, logging de ejecución con SLF4J/Logback, screenshots al fallar y reportes HTML/JSON Cucumber.

## Arquitectura y estructura

```text
Feature -> Step Definitions -> Page Objects -> WebDriver -> Browser
                  ^                 ^
             Hooks/Reports     config.properties
```

Consulte [Architecture](docs/ARCHITECTURE.md), la [guía completa](docs/GUIA_USO_TEMPLATE_AUTOMATIZACION.md), [logging](docs/LOGGING.md) y [Troubleshooting](docs/TROUBLESHOOTING.md).

```text
src/main/java/com/automation/template/{config,driver,pages}
src/test/java/com/automation/template/{hooks,runners,steps,support}
src/test/resources/{features,config.properties}
```

Las Features describen comportamiento en Gherkin; los Steps traducen intención; los Page Objects encapsulan Selenium, locators y esperas. Hooks gestionan el ciclo de vida del navegador y el Runner conecta Cucumber con JUnit Platform.

## Requisitos e instalación

Instale JDK 21 (recomendado) o JDK 17 (compatible), además de Chrome o Edge. Ejecute siempre el Gradle Wrapper incluido: `./gradlew` en entornos Unix o `./gradlew.bat` en Windows; no se requiere una instalación global de Gradle. Compruebe:

```powershell
java -version
.\gradlew.bat --version
git --version
```

Abra el proyecto en VS Code:

```powershell
cd C:\ruta\automation-template-selenium-java-cucumber
code .
```

Instale **Extension Pack for Java**, **Gradle for Java**, **Cucumber (Gherkin) Full Support** y **GitLens**. VS Code detectará el proyecto Gradle e importará dependencias.

## Selección de versión de Java

Java 21 es el valor predeterminado de la configuración actual. Las únicas toolchains admitidas son Java 17 y Java 21, seleccionadas mediante la propiedad Gradle `javaVersion`:

| Objetivo | PowerShell |
|---|---|
| Java predeterminado (21) | `.\gradlew.bat clean test` |
| Usar Java 17 | `.\gradlew.bat clean test -PjavaVersion=17` |
| Declarar Java 21 | `.\gradlew.bat clean test -PjavaVersion=21` |

Java 17 es la única compatibilidad alternativa. `-PjavaVersion=18`, `19`, `20`, `22` y cualquier valor distinto de `17` o `21` se rechazan con `GradleException`. Gradle debe ejecutarse con JDK 17 o superior, y la toolchain seleccionada debe estar instalada o disponible para Gradle.

Para la instalación, configuración de `JAVA_HOME`, VS Code, validación y regreso a Java 21, siga el paso a paso de [Selección de versión de Java](docs/GUIA_USO_TEMPLATE_AUTOMATIZACION.md#selección-de-versión-de-java).

## Configuración y ejecución

`src/test/resources/config.properties` contiene valores base. Prioridad: `-D`, variables de entorno (`BASE_URL`, `BROWSER`, `HEADLESS`) y archivo.

El smoke test interno usa la fixture local; `baseUrl` queda disponible para los Page Objects de una aplicación real y no cambia esta prueba de ejemplo.

| Objetivo | PowerShell |
|---|---|
| Limpiar | `.\gradlew.bat clean` |
| Ejecutar | `.\gradlew.bat test` |
| Limpiar y ejecutar | `.\gradlew.bat clean test` |
| Headless | `.\gradlew.bat clean test -Dheadless=true` |
| Chrome | `.\gradlew.bat clean test -Dbrowser=CHROME` |
| Edge | `.\gradlew.bat clean test -Dbrowser=EDGE` |
| URL de su aplicación | `.\gradlew.bat clean test -DbaseUrl=https://su-aplicacion` |
| Tags Cucumber | `.\gradlew.bat clean test "-Dcucumber.filter.tags=@example"` |
| Tags Cucumber en headless | `.\gradlew.bat clean test -Dheadless=true "-Dcucumber.filter.tags=@example"` |
| Alias Cucumber | `.\gradlew.bat cucumber` |
| Tareas Gradle | `.\gradlew.bat tasks` |
| Dependencias | `.\gradlew.bat dependencies` |
| Estado Git | `git status` |

## Evidencias y reportes

Cada ejecución genera artifacts bajo `build/`, excluidos por Git y regenerables:

| Artifact | Ruta |
|---|---|
| Cucumber HTML | `build/reports/cucumber/cucumber.html` |
| Cucumber JSON | `build/reports/cucumber/cucumber.json` |
| Gradle HTML | `build/reports/tests/test/` |
| JUnit XML | `build/test-results/test/` |
| Screenshots de fallos | `build/evidence/screenshots/` |
| Log de ejecución | `build/logs/automation.log` |

La salida `build/reports/cucumber/cucumber.json` está implementada y validada. Consulte el [contrato de reporting](docs/REPORTING.md) para su relación con HTML, XML, logs y capturas.

Los Hooks registran inicio, fin y estado; `DriverFactory` y `DriverManager` registran el ciclo del driver. Si un escenario falla y `screenshotOnFailure=true`, el Hook delega a `EvidenceManager` antes de cerrar el navegador. El gestor guarda un PNG con nombre saneado, fecha/hora y UUID, y lo adjunta a Cucumber como `image/png`. La ausencia de WebDriver o un fallo de captura producen warnings sin sustituir el error original. Consulte [Evidencias](docs/EVIDENCE.md) para el flujo, ubicación y validación manual, y [Logging](docs/LOGGING.md) para los eventos de SLF4J/Logback.

## Navegadores, URL y Cucumber

Chrome es el navegador predeterminado. Use `-Dbrowser=EDGE` para Edge y `-DbaseUrl=https://su-aplicacion` para una URL temporal. Para seleccionar escenarios, use tags Cucumber como `@smoke` y `-Dcucumber.filter.tags=@smoke`.

## Inventario de configuración

La prioridad para las cinco propiedades del framework es: propiedad JVM `-D`, variable de entorno y, finalmente, `config.properties`. `cucumber.filter.tags` se entrega directamente a Cucumber mediante `-D`. `javaVersion` es una propiedad Gradle (`-P`), no una propiedad JVM.

| Propiedad | Propósito | Predeterminado | Valores admitidos | Ejemplo |
|---|---|---|---|---|
| `baseUrl` / `BASE_URL` | URL inicial de la aplicación bajo prueba. | `https://example.com/` | URL no vacía. | `-DbaseUrl=https://example.com` o `$env:BASE_URL='https://example.com'` |
| `browser` / `BROWSER` | Navegador WebDriver. | `CHROME` | `CHROME`, `EDGE` (sin distinguir mayúsculas). | `-Dbrowser=EDGE` |
| `headless` / `HEADLESS` | Ejecuta el navegador sin ventana. | `false` | `true`, `false`. | `-Dheadless=true` |
| `timeoutSeconds` / `TIMEOUT_SECONDS` | Tiempo de espera explícita de las páginas. | `15` | Entero positivo utilizable por el framework. | `-DtimeoutSeconds=20` |
| `screenshotOnFailure` / `SCREENSHOT_ON_FAILURE` | Intenta adjuntar y persistir evidencia PNG ante un escenario fallido. | `true` | `true`, `false`. | `-DscreenshotOnFailure=false` |
| `cucumber.filter.tags` | Filtra escenarios que Cucumber debe ejecutar. | Sin filtro: todos. | Expresión de tags Cucumber válida. | `"-Dcucumber.filter.tags=@example"` |
| `javaVersion` | Selecciona la toolchain Java de Gradle. | `21` | Exclusivamente `17` o `21`; cualquier otro valor falla. | `-PjavaVersion=17` |

## Ejecución en CI/CD

GitHub Actions valida automáticamente los Pull Requests hacia `main` antes del merge y los pushes a `main`. El job/check estable `quality-gate` ejecuta las pruebas; si Gradle falla, el check falla. El ruleset de `main` requiere Pull Request y el status check `quality-gate` para integrar cambios. Se validaron PASS, FAIL controlado, evidencias en ambos resultados, recuperación a PASS y una ejecución exitosa después del merge en `main`. El workflow intenta subir el artifact `test-evidence` incluso ante fallo, sin cambiar el resultado, y lo conserva 14 días cuando hay archivos. Consulte el paso a paso para principiantes en la [guía de CI/CD](docs/GUIA_USO_TEMPLATE_AUTOMATIZACION.md#cicd-con-github-actions) y el [manual PDF](docs/Manual_Template_Automatizacion_Selenium_Java_Cucumber.pdf).

El workflow de GitHub Actions ejecuta:

```bash
./gradlew clean test -Dheadless=true
```

El workflow usa Java 21 con Temurin y prepara la caché mediante `gradle/actions/setup-gradle@v6`. Un cache miss no es un error: Gradle descarga lo necesario y continúa. El Wrapper sigue siendo el mecanismo oficial (`./gradlew`; `.\gradlew.bat` en Windows). Gradle devuelve código `0` cuando el build y las pruebas pasan; otro código hace fallar el check. Las evidencias disponibles incluyen reportes Gradle y Cucumber, resultados XML, logs y capturas cuando corresponden. Para una ejecución local sin interfaz, use `-Dheadless=true`.

## Crear y reutilizar

1. Cree una feature en `src/test/resources/features`.
2. Cree un Page Object en `src/main/java/com/automation/template/pages`; deje locators y esperas allí.
3. Implemente Steps en `src/test/java/com/automation/template/steps`; exprese intención, no Selenium.
4. Ejecute el Wrapper y revise el reporte.

Para un nuevo proyecto, copie/clone el template, cambie `rootProject.name` y `group`, configure `baseUrl`, sustituya el ejemplo y cree su repositorio Git. Nunca almacene secretos en configuración; use ambiente o secretos del pipeline. El repositorio se distribuye bajo [Apache License 2.0](LICENSE).

## Documentación adicional

Documentación adicional: [guía de uso](docs/GUIA_USO_TEMPLATE_AUTOMATIZACION.md), [arquitectura](docs/ARCHITECTURE.md), [logging](docs/LOGGING.md), [troubleshooting](docs/TROUBLESHOOTING.md), [reporte de migración](docs/TEMPLATE_MIGRATION_REPORT.md), [versionado](docs/VERSIONING.md) y [proceso de release](docs/RELEASE_PROCESS.md). Revise también el [changelog](CHANGELOG.md), la [guía de contribución](CONTRIBUTING.md), la [política de seguridad](SECURITY.md) y el [código de conducta](CODE_OF_CONDUCT.md).

## Regeneración del manual y archivos temporales

`scripts/create_manual.py` genera el manual PDF con ReportLab. Requiere Python con `reportlab` y se ejecuta desde la raíz con `python scripts/create_manual.py`. Actualiza `docs/Manual_Template_Automatizacion_Selenium_Java_Cucumber.pdf` y una copia idéntica en la carpeta padre del proyecto. La opción `--output` escribe solo en la ruta indicada para validaciones temporales.

`work/` contiene archivos temporales de generación y validación documental. Está excluida por `.gitignore`, no forma parte del producto final, no debe versionarse y puede eliminarse sin afectar el framework; se recrea al regenerar o validar documentación.

## Release history

### v1.2.0 - 8 de octubre de 2026

**Stable / Validated / Published.** Logging, evidencias y reporting integrados; auditoría y pruebas documentadas en el [informe de release](docs/HITO4_RELEASE_AUDIT.md).

### v1.1.0 - 1 de octubre de 2026

**Stable / Validated / Published.** CI base, publicación de evidencias, caché Gradle y Quality Gate validados.

### v1.0.2 - 25 de septiembre de 2026

**Documentation-only Hotfix. Stable / Validated / Published.** Corrige inconsistencias de estado post-release; no introduce cambios funcionales, dependencias, CI/CD, Docker, Selenium Grid, Healenium ni Playwright.

### v1.0.1 - 25 de septiembre de 2026

**Hardening + CI/CD Readiness. Stable / Validated / Published.** Logging nativo en consola y archivo, evidencia de fallos persistida con nombres únicos, attachment de screenshots a Cucumber y rutas de artifacts documentadas.

### v1.0.0 - 17 de septiembre de 2026

**First Stable Release - Stable / Validated.** Generalización del proyecto original; arquitectura Web UI reutilizable con Java, Selenium, Cucumber, Gradle Wrapper y Page Object Model; configuración de Chrome/Edge, headless y `baseUrl`; ejemplo funcional; documentación bilingüe, diagramas, troubleshooting, migration report, CI/CD documentado, script de manual y PDF. Docker y Healenium no forman parte de este template.

El template utiliza documentación y ejemplos neutrales para que cualquier equipo pueda adaptarlo a su aplicación Web UI.
