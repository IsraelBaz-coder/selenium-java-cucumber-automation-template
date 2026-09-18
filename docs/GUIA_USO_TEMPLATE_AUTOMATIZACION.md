# Guía de Uso del Template de Automatización

<p align="center"><strong>Automation Template Selenium Java Cucumber</strong><br>Template reutilizable de automatización Web UI<br>Versión v1.0.0 · Estado: Stable / Validated · First Stable Release<br>17 de septiembre de 2026<br>Java 21 (predeterminado) / Java 17 (compatible) · Selenium 4.48.0 · Cucumber 7.34.7 · JUnit 5.13.4 · Gradle 8.14.5</p>

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
- [CI/CD](#cicd)
- [Regeneración del manual](#regeneración-del-manual)
- [Glosario](#glosario)

## Introducción

Este template entrega una base mantenible para pruebas Web UI. Evita que cada equipo reinvente navegador, configuración, BDD, reportes y evidencia. Úselo cuando la aplicación se consume desde Chrome o Edge y se necesitan flujos de negocio en Gherkin. Requiere conocimientos básicos de Java, terminal, Git y pruebas funcionales. El escenario incluido valida una página pública neutral y no representa una regla de negocio.

### Antes de comenzar

No es necesario conocer este repositorio. Para avanzar con seguridad, basta con seguir las secciones en orden y copiar los comandos exactamente. Si un comando termina con `BUILD SUCCESSFUL`, se ejecutó correctamente. Si aparece `BUILD FAILED`, no continúe cambiando archivos al azar: consulte Troubleshooting y conserve el mensaje de error.

**Resultado esperado al terminar:** podrá abrir el proyecto en VS Code, ejecutar el ejemplo, cambiar la URL por la de su ambiente y crear una Feature, un Page Object y sus Steps.

## Información del documento

| Campo | Valor |
|---|---|
| Autor / Creador del template | Israel Baz |
| Rol | Test Automation / Prompt Engineering / AI Automation |
| Mantenimiento | Israel Baz |

## Estado e historial de la release

**Release Status: Stable / Validated.** La versión v1.0.0 fue validada como baseline para nuevos proyectos de automatización Web UI. Los valores propios de cada aplicación —por ejemplo, URL, navegador, datos y secretos administrados externamente— deben configurarse mediante propiedades, variables de entorno o parámetros de JVM. Las capacidades nuevas deben planearse y validarse en una versión posterior.

| Versión | Fecha | Tipo | Estado | Cambios principales |
|---|---|---|---|---|
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

### Compatibilidad de v1.0.0

Java 21 es la versión predeterminada y recomendada. El build también admite Java 17 porque el código y las dependencias utilizadas son compatibles con esa versión LTS. Java 8 y Java 11 no son compatibles con el código actual: se usan expresiones `switch` modernas y APIs como `String.isBlank()` y `Path.of()`.

> Gradle debe ejecutarse con JDK 17 o superior. Además, la toolchain que seleccione debe estar instalada o ser resoluble por Gradle en el equipo o agente CI.

### Cambiar la toolchain sin modificar clases Java

El archivo `build.gradle` define una propiedad llamada `javaVersion`. No cambie los archivos `.java` solo para modificar la versión; seleccione la toolchain al ejecutar:

| Necesidad | Comando PowerShell | Resultado |
|---|---|---|
| Usar el predeterminado | `.\gradlew.bat test` | Compila y ejecuta con Java 21. |
| Usar Java 17 | `.\gradlew.bat clean test -PjavaVersion=17` | Compila y ejecuta con Java 17. |
| Declarar Java 21 explícitamente | `.\gradlew.bat clean test -PjavaVersion=21` | Útil para CI/CD o scripts. |
| Intentar Java inferior | `.\gradlew.bat test -PjavaVersion=11` | El build se detiene con un mensaje de versión mínima. |

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
5. **Detenga daemons anteriores y ejecute las pruebas.**

~~~powershell
.\gradlew.bat --stop
.\gradlew.bat clean test -PjavaVersion=17
~~~

6. **Revise el resultado.** Confirme `BUILD SUCCESSFUL` y abra `build/reports/cucumber/cucumber.html`. Ejecute también en modo headless antes de enviar cambios a CI/CD.

### Volver a Java 21

Abra una consola nueva o reemplace `jdk-17` por la ruta de su JDK 21. Después, ejecute:

~~~powershell
$env:JAVA_HOME = 'C:\ruta\jdk-21'
$env:Path = "$env:JAVA_HOME\bin;$env:Path"
.\gradlew.bat --stop
.\gradlew.bat clean test -PjavaVersion=21
~~~

En VS Code, repita `Java: Configure Java Runtime` y seleccione JDK 21. Para una configuración permanente de `JAVA_HOME`, utilice la administración de Variables de entorno de Windows de acuerdo con las políticas de su organización; no guarde rutas de JDK en el repositorio.

Antes de adoptar Java 17 en un proyecto nuevo, ejecute las pruebas locales y de CI/CD. Si alguna dependencia futura exige Java 21, conserve 21 como baseline y documente el cambio en la siguiente versión del manual.

## Inicio rápido para primera vez

Siga esta ruta sin modificar código:

1. Abra PowerShell y ejecute el comando `cd` de la sección anterior.
2. Ejecute `.\gradlew.bat test -Dheadless=true`.
3. Espere el resultado. El ejemplo abre `https://example.com` y comprueba el texto “Example Domain”.
4. Abra el reporte HTML en `build/reports/cucumber/cucumber.html`.
5. Para ver el navegador durante la ejecución, repita el comando sin `-Dheadless=true`.

Si estos cinco pasos funcionan, el template está listo para su primera automatización. No cambie `gradlew`, `gradle/wrapper`, Hooks, Runner o DriverFactory durante los primeros ejercicios: son componentes compartidos del framework.

## Configuración y comandos

~~~properties
browser=CHROME
headless=false
baseUrl=https://example.com/
timeoutSeconds=15
screenshotOnFailure=true
~~~

| Propósito | Comando compatible |
|---|---|
| Limpiar | .\gradlew.bat clean |
| Ejecutar | .\gradlew.bat test |
| Limpiar y ejecutar | .\gradlew.bat clean test |
| Headless | .\gradlew.bat test -Dheadless=true |
| Chrome | .\gradlew.bat test -Dbrowser=CHROME |
| Edge | .\gradlew.bat test -Dbrowser=EDGE |
| URL temporal | .\gradlew.bat test -DbaseUrl=https://example.com |
| Subconjunto por tag | .\gradlew.bat test -Dcucumber.filter.tags=@example |
| Dependencias | .\gradlew.bat dependencies |
| Información Gradle | .\gradlew.bat --version |
| Estado Git | git status |

Variables disponibles: BASE_URL, BROWSER, HEADLESS, TIMEOUT_SECONDS y SCREENSHOT_ON_FAILURE. Reporte: build/reports/cucumber/cucumber.html; screenshots: build/screenshots.

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
8. **Prepare el repositorio y CI/CD.** Inicialice Git, valide `.gitignore`, cree una rama, abra Pull Request y conecte el pipeline con ejecución headless y publicación de reportes.

**Criterio de salida:** el equipo puede clonar el repositorio, configurar una URL por variable o `-D`, ejecutar una prueba y consultar el reporte sin editar componentes compartidos del framework.

Genérico: driver, configuración, hooks, runner, reporting y convenciones. Personalizable: URL, datos, pages, features, steps, tags y pipeline.

## CI/CD

~~~mermaid
flowchart TD
  DEV[Developer] --> PUSH[Git Push / Pull Request]
  PUSH --> GHE[GitHub Enterprise]
  GHE --> PIPE[Pipeline]
  PIPE --> BUILD[Gradle Build]
  BUILD --> TEST[Automated Tests headless]
  TEST --> ART[Reports / Artifacts]
~~~

EJEMPLO - REQUIERE ADAPTACIÓN A LA INFRAESTRUCTURA DE LA EMPRESA:

~~~yaml
steps:
  - run: .\gradlew.bat clean test -Dheadless=true
    env:
      BASE_URL: referencia a secreto corporativo
      BROWSER: CHROME
  - publish: build/reports
  - publish: build/screenshots
~~~

Use Wrapper, headless, variables/secrets corporativos y artifacts. La pipeline debe fallar si Gradle devuelve código distinto de cero. Runners, permisos, URLs y secretos se definen con el equipo de plataforma.

## Regeneración del manual

El script `scripts/create_manual.py` apoya la generación del manual PDF con la información definida por el proyecto. Requiere Python 3 y la dependencia `reportlab`. Desde la raíz del repositorio, ejecute:

~~~powershell
python scripts/create_manual.py
~~~

El resultado principal se genera en `docs/Manual_Template_Automatizacion_Selenium_Java_Cucumber.pdf`; el script también conserva una copia en el directorio padre del repositorio. Revise visualmente el PDF después de regenerarlo antes de distribuirlo.

La carpeta `work/` se utiliza solo para archivos temporales de generación y validación documental. Está excluida por `.gitignore`, no forma parte de la arquitectura ni del producto final, puede eliminarse sin afectar el framework y se recrea cuando es necesaria.

El manual y los ejemplos usan branding neutral para que puedan reutilizarse en cualquier aplicación Web UI.

## Troubleshooting y buenas prácticas

Consulte TROUBLESHOOTING.md. Chequeos iniciales: JDK 21, Wrapper desde raíz, navegador instalado, Maven Central accesible, URL alcanzable y coincidencia Gherkin/Steps.

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
