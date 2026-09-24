# Automation Template Selenium Java Cucumber

Template reutilizable para pruebas Web UI con Java 21, Selenium WebDriver, Cucumber BDD, JUnit Platform y Gradle. Incluye una prueba neutral contra `https://example.com` solo como referencia: reemplácela por la aplicación bajo prueba.

| Release | Valor |
|---|---|
| Versión | **v1.0.1** |
| Estado | **Stable / Validated** |
| Tipo | **First Stable Release** |
| Fecha | **17 de septiembre de 2026** |

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
- Esperas explícitas, logging de ejecución, screenshots al fallar y reporte HTML Cucumber.

## Arquitectura y estructura

```text
Feature -> Step Definitions -> Page Objects -> WebDriver -> Browser
                  ^                 ^
             Hooks/Reports     config.properties
```

Consulte [Architecture](docs/ARCHITECTURE.md), la [guía completa](docs/GUIA_USO_TEMPLATE_AUTOMATIZACION.md) y [Troubleshooting](docs/TROUBLESHOOTING.md).

```text
src/main/java/com/automation/template/{config,driver,pages}
src/test/java/com/automation/template/{hooks,runners,steps,support}
src/test/resources/{features,config.properties}
```

Las Features describen comportamiento en Gherkin; los Steps traducen intención; los Page Objects encapsulan Selenium, locators y esperas. Hooks gestionan el ciclo de vida del navegador y el Runner conecta Cucumber con JUnit Platform.

## Requisitos e instalación

Instale JDK 21 (recomendado) o JDK 17 (compatible), además de Chrome o Edge. Compruebe:

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

Java 21 es el valor predeterminado de v1.0.1. El código puede compilarse con Java 17 o Java 21 mediante la propiedad Gradle `javaVersion`:

| Objetivo | PowerShell |
|---|---|
| Java predeterminado (21) | `.\gradlew.bat test` |
| Usar Java 17 | `.\gradlew.bat test -PjavaVersion=17` |
| Volver a Java 21 | Omita `-PjavaVersion` o use `-PjavaVersion=21` |

Java 17 es la versión mínima compatible. Java 8 y Java 11 no están soportados por el código actual. Gradle debe ejecutarse con JDK 17 o superior, y la toolchain seleccionada debe estar instalada o disponible para Gradle.

Para la instalación, configuración de `JAVA_HOME`, VS Code, validación y regreso a Java 21, siga el paso a paso de [Selección de versión de Java](docs/GUIA_USO_TEMPLATE_AUTOMATIZACION.md#selección-de-versión-de-java).

## Configuración y ejecución

`src/test/resources/config.properties` contiene valores base. Prioridad: `-D`, variables de entorno (`BASE_URL`, `BROWSER`, `HEADLESS`) y archivo.

| Objetivo | PowerShell |
|---|---|
| Limpiar | `.\gradlew.bat clean` |
| Ejecutar | `.\gradlew.bat test` |
| Limpiar y ejecutar | `.\gradlew.bat clean test` |
| Headless | `.\gradlew.bat test -Dheadless=true` |
| Chrome | `.\gradlew.bat test -Dbrowser=CHROME` |
| Edge | `.\gradlew.bat test -Dbrowser=EDGE` |
| URL | `.\gradlew.bat test -DbaseUrl=https://example.com` |
| Tags Cucumber | `.\gradlew.bat test -Dcucumber.filter.tags=@example` |
| Tareas Gradle | `.\gradlew.bat tasks` |
| Dependencias | `.\gradlew.bat dependencies` |
| Estado Git | `git status` |

## Evidencias y reportes

Cada ejecución genera artifacts bajo `build/`, excluidos por Git y regenerables:

| Artifact | Ruta |
|---|---|
| Cucumber HTML | `build/reports/cucumber/cucumber.html` |
| Gradle HTML | `build/reports/tests/test/` |
| JUnit XML | `build/test-results/test/` |
| Screenshots de fallos | `build/evidence/screenshots/` |
| Log de ejecución | `build/logs/automation.log` |

Los Hooks registran el inicio y fin de cada escenario, navegador, modo headless y ciclo de vida del driver. Si un escenario falla y `screenshotOnFailure=true`, intentan adjuntar una imagen PNG al escenario Cucumber y guardarla físicamente. El archivo usa un nombre saneado del escenario, fecha/hora y UUID para evitar sobrescrituras. Si capturar, adjuntar o persistir evidencia falla, el detalle y la excepción quedan en el log; el error original del escenario se conserva.

## Navegadores, URL y Cucumber

Chrome es el navegador predeterminado. Use `-Dbrowser=EDGE` para Edge y `-DbaseUrl=https://su-aplicacion` para una URL temporal. Para seleccionar escenarios, use tags Cucumber como `@smoke` y `-Dcucumber.filter.tags=@smoke`.

## Crear y reutilizar

1. Cree una feature en `src/test/resources/features`.
2. Cree un Page Object en `src/main/java/com/automation/template/pages`; deje locators y esperas allí.
3. Implemente Steps en `src/test/java/com/automation/template/steps`; exprese intención, no Selenium.
4. Ejecute el Wrapper y revise el reporte.

Para un nuevo proyecto, copie/clone el template, cambie `rootProject.name` y `group`, configure `baseUrl`, sustituya el ejemplo y cree su repositorio Git. Nunca almacene secretos en configuración; use ambiente o secretos del pipeline. No se incluyó licencia porque debe definirla el propietario.

## CI/CD y documentación

Ejecute el Gradle Wrapper en modo headless dentro de CI/CD y publique `build/reports`, `build/evidence` y `build/logs` como artefactos. La guía contiene un ejemplo que requiere adaptación a la infraestructura corporativa; no incluye runners, URLs ni secretos internos.

Documentación adicional: [guía de uso](docs/GUIA_USO_TEMPLATE_AUTOMATIZACION.md), [arquitectura](docs/ARCHITECTURE.md), [troubleshooting](docs/TROUBLESHOOTING.md) y [reporte de migración](docs/TEMPLATE_MIGRATION_REPORT.md).

## Regeneración del manual y archivos temporales

`scripts/create_manual.py` genera el manual PDF con ReportLab. Requiere Python con `reportlab`, se ejecuta desde la raíz con `python scripts/create_manual.py` y genera `docs/Manual_Template_Automatizacion_Selenium_Java_Cucumber.pdf`; también conserva una copia externa en el directorio padre de proyectos.

`work/` contiene archivos temporales de generación y validación documental. Está excluida por `.gitignore`, no forma parte del producto final, no debe versionarse y puede eliminarse sin afectar el framework; se recrea al regenerar o validar documentación.

## Release history

### v1.0.1 - 24 de septiembre de 2026

**Hardening + CI/CD Readiness.** Logging nativo en consola y archivo, evidencia de fallos persistida con nombres únicos, attachment de screenshots a Cucumber y rutas de artifacts documentadas.

### v1.0.0 - 17 de septiembre de 2026

**First Stable Release - Stable / Validated.** Generalización del proyecto original; arquitectura Web UI reutilizable con Java, Selenium, Cucumber, Gradle Wrapper y Page Object Model; configuración de Chrome/Edge, headless y `baseUrl`; ejemplo funcional; documentación bilingüe, diagramas, troubleshooting, migration report, CI/CD documentado, script de manual y PDF. Docker y Healenium no forman parte de este template.

El template utiliza documentación y ejemplos neutrales para que cualquier equipo pueda adaptarlo a su aplicación Web UI.
