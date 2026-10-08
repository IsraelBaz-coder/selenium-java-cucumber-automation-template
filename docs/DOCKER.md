# Docker: guía de uso en Windows

[English](../docs_en/DOCKER.md) · [Índice](README.md) · [Deuda técnica](TECHNICAL_DEBT.md)

**Estado:** Docker es una capacidad en desarrollo para v1.3.0; la última release oficial sigue siendo v1.2.0. El Bloque 1 está integrado en `main`. El Bloque 2 añade `docker-tests` a GitHub Actions en esta rama de trabajo; aún requiere validación en una ejecución real del workflow.

## Descargar el proyecto desde GitHub

1. Instale [Git para Windows](https://git-scm.com/download/win). Abra **PowerShell** desde Inicio y confirme la instalación:

   ~~~powershell
   git --version
   ~~~

2. Clone el **código fuente** en la carpeta actual y entre en el directorio creado:

   ~~~powershell
   git clone https://github.com/IsraelBaz-coder/selenium-java-cucumber-automation-template.git
   Set-Location .\selenium-java-cucumber-automation-template
   git fetch origin
   git branch -r
   ~~~

3. Seleccione una referencia con Docker, como `main`. Para revisar Bloque 2 antes de integrarlo, seleccione `feature/hito-5-docker-ci` cuando esté disponible en el remoto. Confirme que la referencia elegida contenga los tres archivos antes de continuar:

   ~~~powershell
   Test-Path .\Dockerfile
   Test-Path .\gradlew
   Test-Path .\build.gradle
   git check-attr eol -- gradlew
   ~~~

   Los tres `Test-Path` deben devolver `True` y Git debe mostrar `gradlew: eol: lf`. La corrección desde `d173e7d` forma parte de `main`. Para revisar el trabajo del Bloque 2 antes de integrarlo, use la rama `feature/hito-5-docker-ci` cuando esté disponible en el remoto.

4. Con Docker Desktop activo, **construya la imagen localmente** con `docker build --progress=plain -t selenium-java-cucumber-template:1.3.0-dev .`. Luego **ejecute las pruebas** y conserve los resultados en Windows:

   ~~~powershell
   New-Item -ItemType Directory -Force .\build | Out-Null
   $out = (Resolve-Path .\build).Path
   $bind = "type=bind,source=$out,target=/home/automation/app/build"
   docker run --rm --mount $bind selenium-java-cucumber-template:1.3.0-dev
   Test-Path .\build\reports\cucumber\cucumber.html
   Invoke-Item .\build\reports\cucumber\cucumber.html
   ~~~

   Espere `BUILD SUCCESSFUL` y `True`; revise también `build/reports/tests/test/`, `build/logs/automation.log` y, si hubo fallos con capturas, `build/evidence/screenshots/`. Los pasos detallados y el diagnóstico están más abajo.

**Tres operaciones distintas:** `git clone` descarga el código fuente; `docker build` crea una imagen en su equipo a partir de ese código; `docker pull` descargaría una imagen ya construida desde un registro. No hay una imagen preconstruida publicada y verificada para este bloque, por lo que la vía documentada es construirla localmente después de obtener una referencia con Docker.

## Qué es y qué contiene

Docker ejecuta el framework en un contenedor Linux aislado del JDK y navegador instalados en Windows. Sirve para repetir el mismo entorno de pruebas en distintos equipos. La imagen usa Temurin Java 21, Chrome y ChromeDriver 155.0.8059.39, Gradle Wrapper 8.14.5, Selenium, Cucumber, JUnit y POM. El Dockerfile utiliza Linux amd64, trabaja en /home/automation/app y ejecuta como usuario automation (UID 10001). La prueba usa Chrome headless; Edge no está instalado. El Bloque 2 añade un job Docker al workflow de CI; Selenium Grid no está implementado. Las versiones base y del navegador están fijadas; los paquetes Ubuntu descargados durante un build sin caché pueden variar con el repositorio.

~~~text
GitHub (código fuente) → Windows PowerShell → Docker Desktop / WSL2 → contenedor Linux
                                      → Gradle Wrapper → JUnit/Cucumber
                                      → Selenium WebDriver → Chrome
                                      → build/ (reportes, log y evidencias)
~~~

*Diagrama ilustrativo de la arquitectura; no es una captura de una ejecución.*

## 1. Preparar Windows y comprobar el motor

- **Objetivo:** disponer de un motor Docker Linux funcional.
- **Requisitos:** Windows compatible con Docker Desktop, virtualización habilitada, WSL2 configurado y Docker Desktop instalado. El equipo necesita red para la primera construcción.
- **Acción y comandos PowerShell:** abra **Docker Desktop** desde Inicio, espere a que indique que el motor está activo y seleccione contenedores Linux. Abra PowerShell y ejecute:

~~~powershell
wsl --status
docker version
docker info
~~~

- **Explicación:** wsl --status consulta WSL; docker version e info deben mostrar secciones Client y Server. No basta con que aparezca Client.
- **Resultado esperado:** Server indica Docker Desktop, linux/amd64 y un motor disponible.
- **Cómo reconocer un error:** “failed to connect to the docker API” o ausencia de Server indica daemon detenido; mensajes de WSL indican que su distribución o plataforma no está lista.
- **Cómo resolverlo:** inicie o reinicie Docker Desktop, espere al estado activo, confirme modo Linux y vuelva a ejecutar los comandos. Si WSL2 falla, ejecute `wsl --update`, reinicie Windows si se solicita y consulte el diagnóstico de Docker Desktop/WSL antes de continuar.

## 2. Abrir PowerShell en la raíz correcta

- **Objetivo:** usar el Dockerfile y Gradle Wrapper de este repositorio.
- **Requisitos:** repositorio descargado y PowerShell abierto.
- **Comandos PowerShell:** después de clonar y seleccionar la referencia con Docker:

~~~powershell
Get-Location
Test-Path .\Dockerfile
Test-Path .\gradlew
Test-Path .\build.gradle
~~~

- **Explicación:** el punto final del comando de build usa esta carpeta como contexto.
- **Resultado esperado:** los tres Test-Path muestran True.
- **Cómo reconocer un error:** False o “path not found” significa carpeta incorrecta.
- **Cómo resolverlo:** navegue a la carpeta que contiene Dockerfile, gradlew y build.gradle.

## 3. Construir la imagen

- **Objetivo:** crear la imagen de desarrollo a partir del código.
- **Requisitos:** pasos 1 y 2 completos; acceso a las descargas de Temurin, Chrome, ChromeDriver, Gradle y Maven Central.
- **Comando PowerShell:**

~~~powershell
docker build --progress=plain -t selenium-java-cucumber-template:1.3.0-dev .
~~~

- **Explicación:** --progress=plain imprime los pasos completos; -t asigna el nombre y etiqueta; el punto final indica el contexto actual. El Dockerfile compila las clases de prueba con el Wrapper; no instala otro Gradle.
- **Resultado esperado:** el build termina sin ERROR y la imagen queda etiquetada selenium-java-cucumber-template:1.3.0-dev. El usuario confirmó un build sin caché exitoso desde una clonación limpia de la rama corregida; Codex había verificado antes el build local con la etiqueta 1.3.0-clone-test.
- **Cómo reconocer un error:** código de salida distinto de cero, ERROR en descarga, instalación o Gradle, o incapacidad de conectar al daemon.
- **Cómo resolverlo:** confirme motor, red/proxy y certificados; repita el comando. En TLS/PKIX revise el trust store del JDK y el proxy corporativo. No desactive la validación TLS. Si falla una descarga, compruebe la URL en el log y la conexión antes de cambiar dependencias.

## 4. Verificar Java, Chrome y ChromeDriver

- **Objetivo:** comprobar las versiones realmente incluidas en la imagen.
- **Requisitos:** imagen construida.
- **Comandos PowerShell:**

~~~powershell
docker run --rm selenium-java-cucumber-template:1.3.0-dev java -version
docker run --rm selenium-java-cucumber-template:1.3.0-dev google-chrome --version
docker run --rm selenium-java-cucumber-template:1.3.0-dev chromedriver --version
docker run --rm selenium-java-cucumber-template:1.3.0-dev ./gradlew --version
~~~

- **Explicación:** docker run crea un contenedor temporal; --rm lo elimina al salir. Los argumentos finales sustituyen el comando predeterminado de pruebas.
- **Resultado esperado:** Temurin 21.0.12 LTS (en la imagen examinada: 21.0.12.1), Chrome y ChromeDriver 155.0.8059.39, Gradle 8.14.5. Codex ejecutó estos cuatro comandos con salida correcta en la imagen existente.
- **Cómo reconocer un error:** imagen no encontrada, comando no encontrado, o versiones de Chrome y ChromeDriver distintas.
- **Cómo resolverlo:** reconstruya desde la raíz con la etiqueta correcta; compruebe que Dockerfile fija CHROME_VERSION y que ambos binarios informan la misma versión. No altere dependencias del proyecto para ocultar una discrepancia.

## 5. Ejecutar las pruebas e interpretar resultados

- **Objetivo:** ejecutar la suite en Chrome headless.
- **Requisitos:** imagen construida; el escenario de ejemplo usa una fixture HTML local.
- **Comando PowerShell:**

~~~powershell
docker run --rm selenium-java-cucumber-template:1.3.0-dev
~~~

- **Explicación:** sin comando adicional, la imagen ejecuta ./gradlew --no-daemon test. La opción --rm elimina el contenedor al terminar; sin montaje, sus archivos build/ desaparecen con él.
- **Resultado esperado:** WebDriver initialized successfully, escenario Example Domain PASSED y BUILD SUCCESSFUL. El usuario lo confirmó y Codex lo reprodujo durante la validación del montaje.
- **Cómo reconocer un error:** BUILD FAILED, paso rojo de Cucumber, excepción WebDriver o código de salida no cero. WARN no equivale por sí solo a fallo.
- **Cómo resolverlo:** lea el primer error real y el resumen de Gradle. Chrome/ChromeDriver deben coincidir. Las advertencias actuales de CDP y selector Cucumber son no críticas en el smoke validado; están abiertas como [TECH-001 y TECH-002](TECHNICAL_DEBT.md), sin cambio de Selenium ni del runner en este bloque.

## 6. Conservar reportes, logs y evidencias

- **Objetivo:** mantener las salidas de build/ en Windows después de --rm.
- **Requisitos:** imagen disponible, Docker Desktop con acceso a esta carpeta y permisos de escritura para el usuario automation (UID 10001).
- **Comandos PowerShell verificados por Codex con esta imagen:**

~~~powershell
New-Item -ItemType Directory -Force .\build | Out-Null
docker run --rm --mount "type=bind,source=$((Get-Location).Path)\build,target=/home/automation/app/build" selenium-java-cucumber-template:1.3.0-dev
Test-Path .\build\reports\cucumber\cucumber.html
Test-Path .\build\reports\cucumber\cucumber.json
Test-Path .\build\logs\automation.log
~~~

- **Explicación:** --mount enlaza build/ del host con build/ del contenedor. --rm borra el contenedor, no los archivos del host. Se verificaron HTML, JSON, Gradle HTML, JUnit XML y log en Windows. La carpeta de capturas no apareció porque el escenario pasó; no se ha validado aquí la persistencia de un PNG de fallo.
- **Resultado esperado:** BUILD SUCCESSFUL y True para los tres Test-Path. Revise también build/reports/tests/test/ y build/test-results/test/. Las capturas elegibles se guardarían en build/evidence/screenshots/.
- **Cómo reconocer un error:** “permission denied”, fallo de --mount, o False después de una ejecución que sí produjo reportes.
- **Cómo resolverlo:** confirme la ruta con Get-Location, la carpeta compartida de Docker Desktop y permisos de escritura. Mantenga el UID del Dockerfile; no ejecute como root para sortear permisos sin investigar. Los reportes y capturas pueden contener datos sensibles: revíselos antes de compartirlos.

## Advertencias y problemas frecuentes

| Síntoma | Acción de diagnóstico y resolución |
|---|---|
| Docker daemon unavailable / Docker Desktop detenido | Repita `docker version` y `docker info`; inicie Docker Desktop, espere a Server y confirme motor Linux. |
| WSL2 no disponible | Ejecute `wsl --status` y `wsl --update`; compruebe virtualización y reinicie si Windows lo solicita. |
| Descargas fallidas durante build | Use `docker build --progress=plain -t selenium-java-cucumber-template:1.3.0-dev .`; revise la URL y conectividad/proxy del paso fallido. |
| TLS/PKIX en Gradle | Revise certificados del JDK, inspección TLS y proxy; no desactive TLS ni cambie versiones sin diagnóstico. |
| Permiso denegado en build/ | Revise acceso a la carpeta de Windows y escritura del UID 10001; repita el montaje verificado. |
| Chrome/ChromeDriver diferentes | Ejecute los dos comandos --version, reconstruya y confirme CHROME_VERSION=155.0.8059.39. |
| `./gradlew: not found` en Linux aunque existe | Compruebe `git check-attr eol -- gradlew`: debe indicar `lf`. Un checkout CRLF convierte `#!/bin/sh` en `#!/bin/sh\r` y Linux no encuentra el intérprete. Use una revisión que incluya `.gitattributes` con `gradlew text eol=lf` y vuelva a clonar; `chmod +x` por sí solo no corrige los finales de línea. |
| WARN CDP 155 → 152 | Consulte [TECH-001](TECHNICAL_DEBT.md); el smoke validado pasó, pero funciones DevTools necesitan regresión posterior. |
| WARN selector features | Consulte [TECH-002](TECHNICAL_DEBT.md); el escenario actual se descubrió y pasó. |

## Docker en GitHub Actions

El workflow `.github/workflows/ci.yml` se activa en pull requests hacia `main` y pushes a `main`. `quality-gate` conserva la ejecución Gradle con Java 21. El nuevo job `docker-tests` construye la imagen local con el Dockerfile existente y ejecuta las pruebas Selenium/Cucumber en Chrome headless. Tiene un límite de 35 minutos; la ejecución del contenedor, 15 minutos. El contenedor tiene 2 GiB de memoria compartida para Chrome. No se envía ninguna imagen a un registro.

El job guarda `docker-artifacts/container.log` y copia `build/` desde el contenedor detenido. El artifact `docker-test-evidence` incluye, si se generaron, Cucumber HTML/JSON, Gradle HTML, JUnit XML, `automation.log` y capturas. Se intenta subir con `if: always()` aun si el build o los tests fallan; si no hay archivos, no aparece el artifact. El código de salida de las pruebas se conserva: una suite fallida deja `docker-tests` en Failure. El artifact dura 14 días.

Para consultar el resultado en GitHub: abra **Pull requests → su PR → Checks** y seleccione `quality-gate` o `docker-tests` → **Details**. Expanda **Build test image** o **Run headless tests and collect evidence** para leer el error y el log. También puede abrir **Actions → CI → ejecución**; confirme rama, commit y estado, seleccione cada job y revise sus pasos. En el resumen de esa ejecución, bajo **Artifacts**, descargue `test-evidence` o `docker-test-evidence` cuando existan. Descomprima el ZIP para leer `container.log` y `build/reports/`, `build/test-results/`, `build/logs/` y `build/evidence/`. Un fallo previo a las pruebas puede producir solamente un log o ningún artifact. El nuevo job se validará en GitHub cuando exista una ejecución real del PR; una prueba local no acredita ese resultado.

**Estado:** Docker y CI Docker están implementados para `v1.3.0` en desarrollo. `v1.2.0` sigue siendo la última release publicada. [TECH-001/002](TECHNICAL_DEBT.md) siguen OPEN y se tratarán después de este bloque.
