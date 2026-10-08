# Guía de Uso del Template de Automatización

<p align="center"><strong>Automation Template Selenium Java Cucumber</strong><br>Template reutilizable de automatización Web UI<br>v1.2.0 · Stable / Validated / Published · 8 de octubre de 2026<br>Última versión publicada: v1.2.0<br>Java 21 (predeterminado) / Java 17 (compatible) · Selenium 4.48.0 · Cucumber 7.34.7 · JUnit 5.13.4 · Gradle 8.14.5</p>

## Índice

- [Introducción](#introducción)
- [Información del documento](#información-del-documento)
- [Estado e historial de la release](#estado-e-historial-de-la-release)
- [Arquitectura](#arquitectura)
- [Stack tecnológico](#stack-tecnológico)
- [Prerrequisitos y VS Code](#prerrequisitos-y-vs-code)
- [Inicio rápido para primera vez](#inicio-rápido-para-primera-vez)
- [Selección de versión de Java](#selección-de-versión-de-java)
- [Configuración y comandos](#configuración-y-comandos)
- [Primera automatización](#primera-automatización)
- [Reutilizar el template](#reutilizar-el-template)
- [Contrato CI/CD](#contrato-cicd)
- [CI/CD con GitHub Actions](#cicd-con-github-actions)
- [Cómo ejecutar y revisar el CI/CD en GitHub Actions](#cómo-ejecutar-y-revisar-el-cicd-en-github-actions)
- [¿Qué es un Quality Gate?](#qué-es-un-quality-gate)
- [Cómo descargar las evidencias de GitHub Actions](#cómo-descargar-las-evidencias-de-github-actions)
- [Protección de la rama main](#protección-de-la-rama-main)
- [Regeneración del manual](#regeneración-del-manual)
- [Glosario](#glosario)

## Introducción

Este template entrega una base mantenible para pruebas Web UI. Evita que cada equipo reinvente navegador, configuración, BDD, reportes y evidencia. Úselo cuando la aplicación se consume desde Chrome o Edge y se necesitan flujos de negocio en Gherkin. Las secciones de CI/CD explican Git y GitHub Actions desde cero; para modificar pruebas se requieren conocimientos básicos de Java y pruebas funcionales. El escenario incluido valida una fixture HTML local neutral y no representa una regla de negocio.

### Antes de comenzar

No es necesario conocer este repositorio. Para avanzar con seguridad, siga las secciones en orden. Los comandos deben ejecutarse desde la raíz del proyecto; sustituya las rutas y nombres marcados como ejemplos. Si Gradle termina con `BUILD SUCCESSFUL`, la ejecución fue correcta. Si aparece `BUILD FAILED`, conserve el mensaje y consulte [Troubleshooting](TROUBLESHOOTING.md).

**Resultado esperado al terminar:** podrá abrir el proyecto en VS Code, ejecutar el ejemplo, cambiar la URL por la de su ambiente y crear una Feature, un Page Object y sus Steps.

## Información del documento

| Campo | Valor |
|---|---|
| Autor / Creador del template | Israel Baz |
| Rol | Test Automation / Prompt Engineering / AI Automation |
| Mantenimiento | Israel Baz |

## Estado e historial de la release

**Estado técnico y documental.** v1.2.0 es Stable / Validated / Published desde el 8 de octubre de 2026. Reúne logging, [evidencias automáticas](EVIDENCE.md) y [reporting](REPORTING.md). v1.1.0 es la versión publicada anterior.

En el historial, v1.0.2 fue una release publicada: **Documentation-only Hotfix**, Stable / Validated / Published el 25 de septiembre de 2026. Corrige inconsistencias documentales de estado post-release sin cambios funcionales ni de dependencias. La versión estable publicada actualmente es v1.2.0. Los valores propios de cada aplicación —por ejemplo, URL, navegador, datos y secretos administrados externamente— deben configurarse mediante propiedades, variables de entorno o parámetros de JVM.

| Versión | Fecha / publicación | Tipo | Estado | Cambios principales |
|---|---|---|---|---|
| v1.2.0 | 8 de octubre de 2026 | Release estable | Stable / Validated / Published | Logging con SLF4J/Logback, evidencias automáticas y reporting Cucumber HTML/JSON. Véase [Reporting](REPORTING.md). |
| v1.1.0 | 1 de octubre de 2026 | Release estable | Stable / Validated / Published | CI, evidencias, caché Gradle, Quality Gate, Branch Protection y documentación operativa validados. |
| v1.0.2 | 25 de septiembre de 2026 | Documentation-only Hotfix | Stable / Validated / Published | Corrección de inconsistencias de estado post-release; no incluye cambios funcionales, dependencias, CI/CD, Docker, Selenium Grid, Healenium ni Playwright. |
| v1.0.1 | 25 de septiembre de 2026 | Hardening + CI/CD Readiness | Stable / Validated / Published | Logging, screenshots ante fallo, propagación de tags, contrato de artifacts y documentación consolidada para futura integración. No incluye workflow CI/CD. |
| v1.0.0 | 17 de septiembre de 2026 | First Stable Release | Stable / Validated | Generalización del origen, Selenium + Cucumber + POM, Gradle Wrapper, Chrome/Edge, headless, `baseUrl`, ejemplo funcional, documentación técnica, diagramas, troubleshooting, reporte de migración, CI/CD documentado y manual PDF regenerable. |

## Arquitectura

~~~mermaid
flowchart TD
  F[Feature Gherkin] --> S[Step Definitions]
  S --> P[Page Objects]
  P --> D[WebDriver]
  D --> B[Browser]
  CFG[config.properties, -D, variables de entorno] --> D
  H[Hooks] --> D
  H --> REP[Reporte HTML y screenshots]
~~~

~~~mermaid
flowchart LR
  A[gradlew test] --> B[Gradle compila]
  B --> C[JUnit Platform descubre Runner]
  C --> D[Cucumber carga Features]
  D --> E[Hook Before crea WebDriver]
  E --> F[Steps llaman Pages]
  F --> G[Hook After captura y cierra]
  G --> H[Resultado y reporte]
~~~

~~~mermaid
flowchart TB
  ROOT[src] --> MAIN[main/java/com/automation/template]
  MAIN --> CFG[config]
  MAIN --> DRV[driver]
  MAIN --> PAGES[pages]
  ROOT --> TEST[test/java/com/automation/template]
  TEST --> HOOKS[hooks]
  TEST --> STEPS[steps]
  TEST --> RUNNERS[runners]
  TEST --> SUPPORT[support]
  ROOT --> RES[test/resources]
  RES --> FEATURES[features]
  RES --> CONF[config.properties]
~~~

Feature describe comportamiento; Step Definition traduce frases Gherkin; Page Object concentra locators, esperas e interacciones; DriverFactory crea navegador; Hooks administran ciclo de vida. Prioridad de configuración: propiedades JVM, variables de entorno y archivo.

## Stack tecnológico

| Tecnología real | Versión detectada | Uso |
|---|---:|---|
| Java | 21 | Lenguaje, compilación y toolchain. |
| Gradle Wrapper | 8.14.5 | Build, dependencias y ejecución reproducible. |
| Selenium Java | 4.48.0 | WebDriver y automatización de navegador. |
| Cucumber Java/Engine | 7.34.7 | BDD, Gherkin y features. |
| JUnit BOM | 5.13.4 | JUnit Platform y suite. |
| Chrome / Edge | instalación local | Navegadores soportados. |

Git/GitHub Enterprise aportan control de cambios y CI/CD.

## Prerrequisitos y VS Code

En PowerShell valide:

~~~powershell
java -version
.\gradlew.bat --version
git --version
~~~

Debe aparecer Java 21 (predeterminado) o Java 17 si eligió esa toolchain, y Gradle 8.14.5. Abra el proyecto:

~~~powershell
cd C:\ruta\automation-template-selenium-java-cucumber
code .
~~~

Instale Extension Pack for Java, Gradle for Java, Cucumber Gherkin Full Support y GitLens. Espere la importación Gradle. Features: src/test/resources/features; Pages: src/main/java/.../pages; Steps/Hooks/Runner: src/test/java; configuración: src/test/resources/config.properties.

### Cómo comprobar que VS Code quedó listo

1. En el Explorador, confirme que ve las carpetas `src`, `gradle` y los archivos `build.gradle` y `settings.gradle`.
2. Abra `src/test/resources/features/example_domain.feature`; debe ver colores de Gherkin y el escenario de ejemplo.
3. Abra `src/main/java/com/automation/template/pages/ExampleDomainPage.java`; VS Code debe reconocer Java sin subrayados rojos de importación.
4. Abra una terminal integrada con **Terminal > New Terminal** y ejecute `.\gradlew.bat test -Dheadless=true`.
5. Al finalizar, abra `build/reports/cucumber/cucumber.html` con el navegador para revisar el resultado.

Si VS Code muestra “Importing Gradle project”, espere a que termine. Si solicita elegir un JDK, seleccione Java 21 por defecto o Java 17 cuando vaya a ejecutar con `-PjavaVersion=17`.

## Selección de versión de Java

### Compatibilidad de Java

Java 21 es la versión predeterminada y recomendada. El build también admite Java 17 como única compatibilidad alternativa. Java 18, 19, 20, 22 y cualquier otra versión distinta de 17 o 21 no están soportadas: `build.gradle` las rechaza explícitamente.

> Gradle debe ejecutarse con JDK 17 o superior. Además, la toolchain que seleccione debe estar instalada o ser resoluble por Gradle en el equipo o agente CI.

### Cambiar la toolchain sin modificar clases Java

El archivo `build.gradle` define una propiedad llamada `javaVersion`. No cambie los archivos `.java` solo para modificar la versión; seleccione la toolchain al ejecutar:

| Necesidad | Comando PowerShell | Resultado |
|---|---|---|
| Usar el predeterminado | `.\gradlew.bat test` | Compila y ejecuta con Java 21. |
| Usar Java 17 | `.\gradlew.bat clean test -PjavaVersion=17` | Compila y ejecuta con Java 17. |
| Declarar Java 21 explícitamente | `.\gradlew.bat clean test -PjavaVersion=21` | Útil para CI/CD o scripts. |
| Versión no admitida | `.\gradlew.bat clean test -PjavaVersion=18` | El build se detiene: sólo admite Java 17 o Java 21. |

### Paso a paso: configurar Java 17

1. **Instale un JDK 17.** Use la distribución aprobada por su equipo. Identifique la carpeta de instalación; en este documento se representa como `C:\ruta\jdk-17`.
2. **Abra una nueva consola PowerShell** desde la raíz del proyecto y configure la sesión actual. Esto no modifica permanentemente su equipo:

~~~powershell
$env:JAVA_HOME = 'C:\ruta\jdk-17'
$env:Path = "$env:JAVA_HOME\bin;$env:Path"
java -version
~~~

3. **Valide el JDK.** El comando anterior debe indicar Java 17. Si no lo hace, revise la ruta de `JAVA_HOME` antes de continuar.
4. **Seleccione Java 17 en VS Code.** Abra la Paleta de comandos con `Ctrl+Shift+P`, ejecute `Java: Configure Java Runtime`, seleccione el JDK 17 para el proyecto y espere que Gradle termine de importarse. Si la extensión solicita recargar la ventana, acepte.
5. **Ejecute las pruebas.**

~~~powershell
.\gradlew.bat clean test -PjavaVersion=17
~~~

6. **Revise el resultado.** Confirme `BUILD SUCCESSFUL` y abra `build/reports/cucumber/cucumber.html`. Ejecute también en modo headless antes de enviar cambios a CI/CD.

### Volver a Java 21

Abra una consola nueva o reemplace `jdk-17` por la ruta de su JDK 21. Después, ejecute:

~~~powershell
$env:JAVA_HOME = 'C:\ruta\jdk-21'
$env:Path = "$env:JAVA_HOME\bin;$env:Path"
.\gradlew.bat clean test -PjavaVersion=21
~~~

En VS Code, repita `Java: Configure Java Runtime` y seleccione JDK 21. Para una configuración permanente de `JAVA_HOME`, utilice la administración de Variables de entorno de Windows de acuerdo con las políticas de su organización; no guarde rutas de JDK en el repositorio.

Antes de adoptar Java 17 en un proyecto nuevo, ejecute las pruebas locales y de CI/CD. Si alguna dependencia futura exige Java 21, conserve 21 como baseline y documente el cambio en la siguiente versión del manual.

## Inicio rápido para primera vez

Siga esta ruta sin modificar código:

1. Abra PowerShell y ejecute el comando `cd` de la sección anterior.
2. Ejecute `.\gradlew.bat test -Dheadless=true`.
3. Espere el resultado. El ejemplo abre la fixture local `src/test/resources/fixtures/example_page.html` y comprueba el encabezado “Example Domain” sin consultar una web externa. La preparación inicial de dependencias y del navegador puede requerir conexión.
4. Abra el reporte HTML en `build/reports/cucumber/cucumber.html`.
5. Para ver el navegador durante la ejecución, ejecute `.\gradlew.bat clean test` sin `-Dheadless=true`.

Si estos cinco pasos funcionan, el template está listo para su primera automatización. No cambie `gradlew`, `gradle/wrapper`, Hooks, Runner o DriverFactory durante los primeros ejercicios: son componentes compartidos del framework.

## Configuración y comandos

~~~properties
browser=CHROME
headless=false
baseUrl=https://example.com/
timeoutSeconds=15
screenshotOnFailure=true
~~~

El smoke test interno abre la fixture local; `baseUrl` queda disponible para las pruebas de una aplicación real y no modifica este escenario de ejemplo.

| Propósito | Comando compatible |
|---|---|
| Limpiar | .\gradlew.bat clean |
| Ejecutar | .\gradlew.bat test |
| Limpiar y ejecutar | .\gradlew.bat clean test |
| Headless | .\gradlew.bat clean test -Dheadless=true |
| Chrome | .\gradlew.bat clean test -Dbrowser=CHROME |
| Edge | .\gradlew.bat clean test -Dbrowser=EDGE |
| URL de su aplicación | .\gradlew.bat clean test -DbaseUrl=https://su-aplicacion |
| Subconjunto por tag | .\gradlew.bat clean test "-Dcucumber.filter.tags=@example" |
| Subconjunto headless | .\gradlew.bat clean test -Dheadless=true "-Dcucumber.filter.tags=@example" |
| Alias Cucumber | .\gradlew.bat cucumber |
| Dependencias | .\gradlew.bat dependencies |
| Información Gradle | .\gradlew.bat --version |
| Estado Git | git status |

Variables disponibles: BASE_URL, BROWSER, HEADLESS, TIMEOUT_SECONDS y SCREENSHOT_ON_FAILURE. Reporte: `build/reports/cucumber/cucumber.html`; screenshots de fallos: `build/evidence/screenshots/`; log: `build/logs/automation.log`.

## Primera automatización

Cómo crear tu primera prueba utilizando este template:

1. Cree src/test/resources/features/login.feature.

~~~gherkin
# language: es
Característica: Inicio de sesión
  Escenario: Acceso correcto
    Dado que el usuario abre la pantalla de inicio de sesión
    Cuando inicia sesión con "usuario" y "contraseña"
    Entonces se muestra el panel principal
~~~

2. Cree pages/LoginPage.java con locators privados, espera explícita y métodos open(), login(), isDashboardVisible().
3. Cree steps/LoginSteps.java; obtenga driver desde DriverManager, llame a la Page y use una aserción JUnit.
4. Configure baseUrl con -DbaseUrl=...
5. Ejecute .\gradlew.bat test -Dheadless=true y revise el HTML.

Las Steps no deben contener selectores; Pages no deben contener aserciones de escenario. Use WebDriverWait, nunca Thread.sleep.

### Ejemplo completo mínimo

Para evitar dudas sobre qué corresponde a cada archivo, esta es la relación que debe conservar:

| Archivo | Qué escribe el usuario | Qué no debe poner |
|---|---|---|
| `login.feature` | Flujo en lenguaje de negocio. | XPath, CSS o código Java. |
| `LoginSteps.java` | Llamadas a métodos de la página y aserciones. | Selectores o `Thread.sleep`. |
| `LoginPage.java` | Selectores, esperas y acciones de pantalla. | Frases Gherkin o reglas del escenario. |

Al crear una nueva pantalla, copie la estructura de `ExampleDomainPage`, cambie el nombre y sustituya el locator `h1` por locators de su aplicación. Prefiera atributos estables que el equipo de desarrollo haya definido para pruebas, por ejemplo `data-testid`.

### Lista de comprobación antes de pedir ayuda

- Estoy situado en la raíz del proyecto al ejecutar Gradle.
- `java -version` muestra Java 21, o Java 17 cuando se eligió la toolchain compatible.
- El navegador seleccionado está instalado.
- La URL configurada abre manualmente en ese equipo.
- El archivo termina en `.feature` y está dentro de `src/test/resources/features`.
- El texto de cada Step coincide exactamente con su anotación Java.
- No guardé usuario, contraseña, token ni URL corporativa sensible en Git.

## Reutilizar el template

Siga esta secuencia para transformar el template en un proyecto de automatización real:

1. **Copie o clone el template.** Trabaje siempre sobre la copia; conserve el template original como referencia reutilizable.
2. **Cambie el identificador del proyecto.** Actualice `rootProject.name` en `settings.gradle` y `group` en `build.gradle` con el nombre y paquete aprobados por su equipo.
3. **Configure el ambiente.** Ejecute la primera prueba con `-DbaseUrl=https://su-aplicacion`; no guarde URLs internas sensibles, usuarios ni contraseñas en Git.
4. **Compruebe la conexión.** Abra manualmente la URL y ejecute una prueba smoke en headless. Si falla, resuelva conectividad, JDK o navegador antes de crear más escenarios.
5. **Sustituya el ejemplo.** Cuando su smoke funcione, elimine `example_domain.feature`, `ExampleDomainPage` y `ExampleDomainSteps` o consérvelos temporalmente solo como referencia.
6. **Cree el primer flujo de negocio.** Agregue una Feature, su Page Object y sus Steps siguiendo la separación descrita en esta guía.
7. **Organice la ejecución.** Añada tags como `@smoke` y `@regression`; ejecute subconjuntos con `-Dcucumber.filter.tags`.
8. **Prepare el repositorio y CI/CD.** Si creó un repositorio nuevo, inicialice Git y configure su remoto. Revise `.gitignore` y el workflow incluido en `.github/workflows/ci.yml`; cree una rama y abra un Pull Request. El workflow ya ejecuta pruebas headless y publica las evidencias disponibles.

**Criterio de salida:** el equipo puede clonar el repositorio, configurar una URL por variable o `-D`, ejecutar una prueba y consultar el reporte sin editar componentes compartidos del framework.

Genérico: driver, configuración, hooks, runner, reporting y convenciones. Personalizable: URL, datos, pages, features, steps, tags y pipeline.

## Contrato CI/CD

~~~mermaid
flowchart TD
  DEV[Developer] --> PUSH[Git Push / Pull Request]
  PUSH --> GHE[GitHub Enterprise]
  GHE --> CHECKOUT[Checkout]
  CHECKOUT --> JAVA[Java 21 Temurin]
  JAVA --> CACHE[Gradle Setup / Cache]
  CACHE --> WRAPPER[Gradle Wrapper]
  WRAPPER --> TEST[Automated Tests headless]
  TEST --> REPORTS[Reports / Logs / Screenshots]
  REPORTS --> ART[test-evidence]
~~~

El workflow ejecuta `./gradlew clean test -Dheadless=true`; en Windows, el comando equivalente es `.\gradlew.bat clean test "-Dheadless=true"`. Un exit code `0` representa éxito y cualquier código distinto de cero falla el job. El contrato permite seleccionar `CHROME` o `EDGE`, aplicar `cucumber.filter.tags` y recolectar `build/reports/cucumber/` (HTML y JSON), `build/reports/tests/test/`, `build/test-results/test/`, `build/logs/automation.log` y, si un escenario falló, `build/evidence/screenshots/`.

El workflow `.github/workflows/ci.yml` ejecuta `./gradlew clean test -Dheadless=true` con Java 21 de Temurin en Pull Requests dirigidos a `main` y pushes a `main`. Usa el Gradle Wrapper existente y falla si Gradle o las pruebas fallan. Después intenta subir el artifact `test-evidence` con reportes Gradle/Cucumber, resultados JUnit, logs y screenshots disponibles. Se conserva 14 días y se descarga desde **Artifacts** en el resumen de la ejecución de GitHub Actions. Screenshots pueden no existir cuando no hay escenarios fallidos; una ruta ausente no hace fallar la carga. El artifact no altera el resultado PASS/FAIL.

Después de configurar Java, `gradle/actions/setup-gradle@v6` prepara la caché básica de Gradle. Reutiliza dependencias y otros datos del directorio de usuario de Gradle cuando hay una entrada disponible, lo que evita trabajo repetitivo y puede reducir el tiempo de preparación en ejecuciones posteriores. Si no existe caché (cache miss), Gradle descarga lo necesario y las pruebas continúan normalmente; la caché no es requisito para el pipeline. `./gradlew` sigue siendo el mecanismo oficial de CI y `.\gradlew.bat` su equivalente en Windows. Esta optimización no cambia la lógica de Selenium, Cucumber, Page Object Model, features, steps ni del smoke test con fixture local.

## CI/CD con GitHub Actions

**CI** (integración continua) valida automáticamente cambios antes de integrarlos. Permite detectar pronto errores de compilación y pruebas, y da al equipo un resultado compartido. **CD** puede ser entrega continua (dejar una versión lista) o despliegue continuo (publicarla automáticamente). Este proyecto utiliza principalmente CI; no despliega una aplicación.

GitHub Actions es el servicio que ejecuta las instrucciones de `.github/workflows/ci.yml`. Aquí el workflow se inicia automáticamente al abrir o actualizar un Pull Request (PR) hacia `main`, y también con un push a `main`. Un PR es una propuesta de unir una rama de trabajo con otra. Un runner temporal `ubuntu-latest` obtiene el código (checkout), prepara Java 21 Temurin y la caché de Gradle, y usa el Wrapper para ejecutar Selenium y Cucumber sin ventana de navegador.

```text
Developer → feature branch → commit → push → Pull Request hacia main
→ GitHub Actions → quality-gate → Gradle → Selenium + Cucumber
→ PASS/FAIL → evidencias → revisión → merge a main
```

## Cómo ejecutar y revisar el CI/CD en GitHub Actions

Necesita Git instalado, una copia del repositorio conectada a GitHub y permiso para enviar ramas. Ejecute los comandos desde la raíz del proyecto.

1. **Cree una rama:** `git switch -c feature/mi-cambio` (si ya existe: `git switch feature/mi-cambio`). Una rama separa su trabajo de `main`, la línea compartida, para revisarlo antes de integrarlo.
2. **Modifique los archivos** necesarios, por ejemplo un Page Object y sus pruebas.
3. **Revise los cambios:** `git status` muestra archivos cambiados y `git diff` muestra líneas. Compruebe que no incluyó credenciales ni archivos generados.
4. **Ejecute pruebas locales:** Windows PowerShell: `.\gradlew.bat clean test "-Dheadless=true"`; Linux/macOS: `./gradlew clean test -Dheadless=true`. Espere `BUILD SUCCESSFUL`; si ve `BUILD FAILED`, corrija el error.
5. **Guarde el cambio:** `git add ruta/del/archivo` y `git commit -m "Describe mi cambio"`. Un commit es una instantánea del trabajo.
6. **Envíe la rama:** la primera vez use `git push -u origin feature/mi-cambio`; después, `git push`. Push copia los commits a GitHub.
7. **Cree el PR:** en GitHub abra repositorio → **Pull requests** → **New pull request**. Elija `main` como *base* y `feature/mi-cambio` como *compare*. Revise el resumen, escriba título y descripción y pulse **Create pull request**. No haga merge todavía.
8. **Espere Actions:** GitHub detecta el PR y ejecuta `.github/workflows/ci.yml` automáticamente. Cada nuevo commit seguido de push a esa rama actualiza el PR y lanza otra ejecución.
9. **Revise desde el PR:** repositorio → **Pull requests** → su PR → **Checks** (o bloque de checks en **Conversation**). Busque `quality-gate`, pulse **Details** y examine checkout, Java, caché Gradle, pruebas, carga de evidencias y resultado. Expanda el paso fallido para leer su log.
10. **Revise desde Actions:** repositorio → **Actions** → workflow **CI** → ejecución. Identifique rama, PR, commit, fecha, estado y duración; abra la ejecución y el job `quality-gate`. El texto del estado importa además del color: **Success** (verde) = terminó bien; **Failure** (rojo) = falló; **In progress** (amarillo/progreso) = sigue ejecutándose; **Cancelled** = cancelado; **Skipped** = un paso no se ejecutó por una condición.

## ¿Qué es un Quality Gate?

Es una puerta de control: la verificación automática debe terminar bien antes de considerar listo un cambio. El check estable de este proyecto se llama `quality-gate`. Gradle devuelve exit code `0` si compilación y pruebas pasan, y un código distinto de cero si fallan. GitHub muestra **PASS/Success** para continuar a revisión o **FAIL/Failure** para corregir. La carga de artifacts no convierte FAIL en PASS. El ruleset activo de `main` requiere este check y un Pull Request antes del merge.

### ¿Qué hacer si el Quality Gate falla?

1. Abra el PR → **Checks** → `quality-gate` → **Details**.
2. Localice el step **Failure**, expándalo y lea el error y el resumen final.
3. Descargue `test-evidence` si existe. Revise reportes, resultados XML, `automation.log` y screenshots. Si Gradle falló antes de producir archivos, algunos faltarán.
4. Corrija el problema en su rama y repita `.\gradlew.bat clean test "-Dheadless=true"` (Linux/macOS: `./gradlew clean test -Dheadless=true`).
5. Revise `git diff`, haga otro `git add` y `git commit`, y ejecute `git push`. El PR se actualiza automáticamente y Actions vuelve a ejecutar el check. Espere el nuevo resultado.

### Reportes locales

| Ruta | Contenido |
|---|---|
| `build/reports/cucumber/cucumber.html` | Escenarios y pasos funcionales Cucumber. |
| `build/reports/cucumber/cucumber.json` | Resultado estructurado y attachments Cucumber. |
| `build/reports/tests/test/` | Reporte HTML Gradle/JUnit. |
| `build/test-results/test/` | Resultados XML estructurados. |
| `build/logs/automation.log` | Log cronológico de ejecución. |
| `build/evidence/screenshots/` | Capturas de fallos cuando corresponden. |

## Cómo descargar las evidencias de GitHub Actions

Un **artifact** es un archivo descargable producido por una ejecución, separado del código. Abra **Repository → Actions → CI → ejecución del PR → Artifacts → test-evidence**. Descargue y extraiga el ZIP para ver reportes Cucumber, Gradle/JUnit, XML, logs y, si se produjeron, screenshots. Se conserva 14 días. El workflow intenta publicarlo en PASS y FAIL; aparece sólo si hay archivos en las rutas configuradas. Si no aparece, revise el step **Upload test evidence** y si Gradle llegó a generar archivos. Las capturas normalmente faltan cuando ninguna prueba falla.

## Protección de la rama main

Branch Protection es una regla de GitHub que limita cómo se integra código en `main`. Protege la línea compartida ante cambios sin revisión o pruebas fallidas. El flujo recomendado es **feature branch → Pull Request → quality-gate → code review → merge**. Un status check es el resultado visible del job; un Required Status Check bloquea el merge hasta que ese resultado pase.

En este repositorio, `main` ya está protegida mediante un ruleset: exige Pull Request, el status check `quality-gate` y que la rama esté actualizada antes del merge; bloquea force push y restringe la eliminación de `main`. Un administrador puede consultar la regla en **Repository → Settings → Rules → Rulesets** (según la interfaz y sus permisos). El workflow no crea esta regla: es una configuración administrativa ya validada.

### Ejemplo y validación real del Quality Gate

Ana crea `feature/ajuste-page`, modifica un Page Object, prueba localmente, hace commit y push y abre un PR. Actions inicia `quality-gate`. Con Success, otra persona revisa y podrá hacer merge cuando se cumplan las reglas del repositorio. Si una prueba falla, Ana abre Details, descarga `test-evidence`, corrige, vuelve a probar, hace un nuevo commit y push. El PR y el check se actualizan.

La validación de CI realizada para v1.1.0 comprobó la secuencia **PASS inicial → FAIL controlado → bloqueo del merge por `quality-gate` → `test-evidence` disponible → restauración → PASS → merge → PASS post-merge en `main`**. Las evidencias se publicaron tanto en PASS como en FAIL. No quedó el fallo controlado en `main`.

**v1.1.0:** versión publicada anterior (1 de octubre de 2026). **v1.2.0:** **Stable / Validated / Published** desde el 8 de octubre de 2026.

## Regeneración del manual

El script `scripts/create_manual.py` apoya la generación del manual PDF con la información definida por el proyecto. Requiere Python 3 y la dependencia `reportlab`. Desde la raíz del repositorio, ejecute:

~~~powershell
python scripts/create_manual.py
~~~

El resultado se genera en `docs/Manual_Template_Automatizacion_Selenium_Java_Cucumber.pdf` y se copia a la carpeta padre del proyecto con el mismo nombre. La opción `--output` escribe solo en la ruta indicada. Revise visualmente el PDF después de regenerarlo antes de distribuirlo.

La carpeta `work/` se utiliza solo para archivos temporales de generación y validación documental. Está excluida por `.gitignore`, no forma parte de la arquitectura ni del producto final, puede eliminarse sin afectar el framework y se recrea cuando es necesaria.

El manual y los ejemplos usan branding neutral para que puedan reutilizarse en cualquier aplicación Web UI.

## Troubleshooting y buenas prácticas

Consulte [Troubleshooting](TROUBLESHOOTING.md). Chequeos iniciales: JDK 21, Wrapper desde raíz, navegador instalado, Maven Central accesible, URL alcanzable y coincidencia Gherkin/Steps.

- Un Page Object por pantalla/componente; locators privados y nombres descriptivos.
- Configuración externa; secretos solo en ambiente/secret store.
- Esperas explícitas y locators estables por atributos de prueba.
- Datos aislados, screenshots/logs como evidencia y aserciones claras.
- Commits pequeños, ramas, Pull Requests, revisión de código y actualización deliberada de dependencias.

## Glosario

| Término | Definición |
|---|---|
| Automation Testing | Ejecución de pruebas mediante software. |
| Selenium / WebDriver | Biblioteca y API que controlan navegador. |
| Cucumber / BDD / Gherkin | Herramienta, enfoque y lenguaje de comportamiento. |
| Feature / Scenario | Capacidad y caso concreto Gherkin. |
| Step Definition | Código de una frase Gherkin. |
| Page Object Model | Patrón que encapsula UI en objetos. |
| Hooks / Runner | Ciclo de vida y punto de ejecución. |
| Gradle / Gradle Wrapper | Build y lanzador versionado. |
| JUnit / Headless | Plataforma de pruebas y navegador sin ventana. |
| CI/CD / Pipeline | Integración/entrega continua y flujo. |
| Git / GitHub Enterprise | Control de cambios y plataforma corporativa. |
| Locator / XPath / CSS Selector | Estrategias para identificar elementos. |
| Assertions / Test Data | Verificaciones e información de prueba. |
| Environment Variable | Valor externo del proceso. |
| CI | Integración continua: pruebas automáticas para cambios propuestos. |
| CD | Entrega o despliegue continuo; aquí no hay despliegue automático. |
| GitHub Actions | Servicio de GitHub que ejecuta workflows. |
| Workflow | Archivo de instrucciones automáticas, como `ci.yml`. |
| Pipeline | Secuencia de verificaciones automáticas. |
| Job | Grupo de pasos ejecutado en un runner. |
| Step | Instrucción individual de un job. |
| Runner / ubuntu-latest | Equipo temporal; `ubuntu-latest` indica Linux Ubuntu. |
| Pull Request | Propuesta para integrar una rama tras revisión. |
| Branch / Feature Branch | Línea de trabajo separada; la feature branch contiene un cambio. |
| main | Rama principal compartida. |
| Quality Gate | Verificación que debe pasar antes de considerar listo un cambio. |
| Status Check / Required Status Check | Resultado de un job; si es requerido, bloquea el merge al fallar. |
| Branch Protection | Reglas que protegen una rama frente a integraciones indebidas. |
| Artifact | Archivo descargable de una ejecución de Actions. |
| Log / Report | Registro de eventos / resumen legible de resultados. |
| Exit Code | Número de salida: `0` éxito, distinto de `0` fallo. |
| PASS / FAIL | Verificación correcta / fallida. |
| Commit / Push / Merge | Guardar una instantánea / enviarla a GitHub / unir ramas. |
| Checkout | Descargar el código de una revisión en el runner. |

## Generación y consulta de reportes

El runner genera `build/reports/cucumber/cucumber.html` y `build/reports/cucumber/cucumber.json`; ambas salidas están validadas. Gradle mantiene `build/reports/tests/test/` y `build/test-results/test/`; Logback escribe `build/logs/automation.log`; EvidenceManager guarda PNG de fallos bajo `build/evidence/screenshots/`. GitHub Actions incluye toda la carpeta `build/reports/cucumber/` en `test-evidence` con `if: always()`; por tanto incluye el JSON generado. Las salidas actuales son artifacts regenerables bajo `build/`, ignorados por Git. Consulte [Reporting](REPORTING.md) para uso local, CI y diagnóstico.
