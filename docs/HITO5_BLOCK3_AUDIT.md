# Hito 5, Bloque 3 — diagnóstico y validación local

[English](../docs_en/HITO5_BLOCK3_AUDIT.md) · [Índice](README.md)

Estado al 8 de octubre de 2026: rama `feature/hito-5-docker-hardening`; `v1.3.0` sigue en desarrollo. No se hizo commit, push, PR, merge ni release.

## Diagnóstico previo a cambios

| Archivo | Hallazgo y riesgo | Corrección y efecto | Validación |
|---|---|---|---|
| `Dockerfile`, `.dockerignore` | Temurin estaba fijado sólo por etiqueta; Chrome/ChromeDriver sí por versión; apt puede variar. El contexto ya excluía `.git`, `build`, secretos y docs; UID 10001 y limpieza temporal ya existían. | Fijar la misma imagen Temurin por digest; conservar versiones y exclusiones. La variación de apt queda documentada. | `docker build`, versiones en contenedor, contexto de build. |
| `src/test/java/.../RunCucumberTest.java` | El selector de recurso `features` generaba dos avisos de discovery; riesgo de compatibilidad futura. | Cambiar a selector de paquete sin mover features ni cambiar tags. | Suite local, filtro `@example`, suite Docker, conteo y avisos. |
| `build.gradle`, `gradle/wrapper/gradle-wrapper.properties` | Selenium 4.48.0, Cucumber 7.34.7, JUnit BOM 5.13.4, Gradle 8.14.5, Java 21 predeterminado. No existe `gradle.properties`. El código no invoca CDP; Chrome local observado usa CDP 153 y Docker 155, mientras Selenium selecciona 152. | Mantener dependencias; TECH-001 OPEN. | Inspección de `src/`, logs local/Docker y resultados. |
| `.github/workflows/ci.yml` | `test-evidence` ya elegía reportes; incluía `binary/` interno de Gradle. `docker-test-evidence` copiaba todo `build/`, incluidas clases y temporales. | Excluir `binary/`; copiar sólo reportes, XML, logs y capturas; conservar `container.log`, código de salida y carga `always()`. | Copia local desde contenedor detenido, inspección de rutas y script. Ejecución GitHub pendiente. |
| `README*`, `docs/`, `docs_en/`, manuales PDF | TECH-002 y el alcance del artifact Docker figuraban desactualizados; los manuales se generan desde `scripts/create_manual.py`. | Actualizar estados, límites y comandos en ambos idiomas y regenerar los PDF. | Enlaces de 35 archivos Markdown, extracción y render de páginas Docker en ambos PDF. |

## Resultados y límites

- `.\gradlew.bat clean test -Dheadless=true`: PASS, 6 pruebas, 0 fallos; antes del cambio reprodujo los avisos del selector.
- `.\gradlew.bat clean test -Dheadless=true "-Dcucumber.filter.tags=@example"`: PASS, 6 pruebas, un escenario, sin aviso TECH-002.
- `.\gradlew.bat clean test -Dheadless=false`: PASS, 6 pruebas, un escenario.
- `docker build --progress=plain -t selenium-template:hito5-b3 .`: PASS; reconstruido tras fijar el digest.
- `docker run --rm --mount $bind --shm-size=2g selenium-template:hito5-b3`: PASS, 6 pruebas, un escenario; HTML/JSON, XML y log persistidos. Chrome/ChromeDriver informaron 155.0.8059.39. La advertencia CDP 155 → 152 permanece.
- Una prueba aislada sin `--no-sandbox` falló al crear la sesión Chrome; el flag se restauró y la ejecución Docker posterior pasó. Chrome corre como UID 10001 pero sin su sandbox interno.
- Una copia local con `docker create`, `docker start -a` y `docker cp` encontró los cuatro directorios obligatorios; no hubo capturas por ser PASS. Se excluye `test-results/test/binary/`. Esta copia no sustituye un upload real en Actions.
- `scripts/validate_docs.py`: 35 Markdown, enlaces internos sin errores. `git diff --check`: limpio. Los dos PDF se regeneraron y se revisaron visualmente en sus páginas Docker.

## Criterios de aceptación

| Criterio | Estado | Motivo |
|---|---|---|
| CA-01 Docker build reproducible | BLOCKED | Build local PASS con digest y Chrome fijados; apt sin snapshot impide reproducibilidad estricta. |
| CA-02 Pruebas locales | PASS | Headless y visible: 6/6. |
| CA-03 Pruebas Docker | PASS | 6/6 y un escenario. |
| CA-04 Sin regresiones | PASS | Mismo conteo y filtro; flag restaurado tras la prueba fallida. |
| CA-05 TECH-001 | PASS | Evaluada y OPEN con plan. |
| CA-06 TECH-002 | PASS | CLOSED, aviso ausente. |
| CA-07 Artifacts | BLOCKED | Estructura comprobada localmente; upload real y PNG de fallo pendientes. |
| CA-08 Códigos de salida | BLOCKED | Gradle propagó el fallo en la prueba aislada y script CI conserva códigos; falta ejecución GitHub. |
| CA-09 Secretos/archivos innecesarios | PASS | Exclusiones de contexto y artifacts revisadas; búsqueda de patrones sin secretos reales en evidencias de muestra. |
| CA-10 Documentación ES/EN | PASS | Árboles pares y enlaces válidos. |
| CA-11 PDF | PASS | Ambos regenerados, texto y páginas Docker inspeccionados. |
| CA-12 Diff | PASS | `git diff --check` limpio. |

**Preparación para PR:** cambios locales revisables; el PR permitirá validar Actions, carga de artifacts y códigos de salida en el runner real. No cerrar Hito 5 ni publicar `v1.3.0` con esta validación local.
