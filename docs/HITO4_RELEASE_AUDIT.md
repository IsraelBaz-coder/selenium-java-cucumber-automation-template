# Hito 4, Bloque 4 — auditoría y preparación de v1.2.0

**Registro histórico de la auditoría local (2026-10-07):** v1.2.0 estaba en Release Candidate / Pending Publication, v1.1.0 era la última versión publicada y aún no se había asignado fecha a v1.2.0. Hito 4 seguía abierto. Entorno: Windows, Java 21.0.12.1.

**Preparación del release:** la documentación definitiva se incorpora al PR y al futuro tag con fecha objetivo UTC 2026-10-08. El estado y la fecha reales de GitHub aún requieren verificación; este informe no declara publicado el release ni cerrado el hito.

La fecha de v1.1.0 se contrastó con el [GitHub Release oficial](https://github.com/IsraelBaz-coder/selenium-java-cucumber-automation-template/releases/tag/v1.1.0), que indica publicación el 1 de octubre de 2026. El repositorio remoto aún no tiene un release v1.2.0 en esta auditoría.

## Resumen técnico

La estructura Java/Gradle conserva Selenium, Cucumber, JUnit Platform y Page Object Model. `RunCucumberTest` produce HTML y JSON; Logback escribe en consola y `build/logs/automation.log`; `Hooks` captura evidencia antes de liberar WebDriver. El smoke test usa una fixture local. No se cambiaron versiones de dependencias. La versión de proyecto se corrigió de `1.0.2` a `1.2.0` para alinear el candidato con el release objetivo.

Se corrigió una fuga potencial: si `maximize()` fallaba tras crear un navegador visible, `DriverFactory` no cerraba la sesión. Ahora la cierra y conserva la excepción original. `DriverManager` rechaza una segunda inicialización en el mismo hilo, evitando reemplazar silenciosamente una sesión activa. La salida versionable del generador PDF es `docs/Manual_Template_Automatizacion_Selenium_Java_Cucumber.pdf`; cada generación normal sincroniza además la copia de la carpeta padre del proyecto.

## Resultados reproducibles

| Validación | Resultado | Evidencia / límite |
|---|---|---|
| `.\gradlew.bat clean test -Dheadless=true` | BLOCKED | Maven Central devolvió `PKIX path building failed` al resolver `io.cucumber:query`. Ocurrió antes de compilar; no equivale a un fallo de tests. |
| `.\gradlew.bat clean test -Dheadless=true --offline` | PASS | `BUILD SUCCESSFUL`, suite JUnit/Cucumber y smoke local; JSON, HTML, XML y log generados. |
| `.\gradlew.bat clean test -Dheadless=false --offline` | PASS | `BUILD SUCCESSFUL`, navegador Chrome visible, mismo smoke. |
| Fallo controlado `@release-evidence` | PASS del mecanismo | Escenario temporal con encabezado incorrecto: Gradle salió 1 como se esperaba; PNG de 13 239 bytes, attachment `image/png` en JSON, `status=FAILED` y eventos de captura en log. Feature temporal eliminada. |
| Suite final headless tras eliminar la feature | PASS | `BUILD SUCCESSFUL`; `cucumber.json` 1 536 bytes, `cucumber.html` 919 747 bytes, `automation.log` 1 986 bytes; cero PNG de fallo en `build/`. |
| CI de este candidato en GitHub | BLOCKED | No existe PR ni commit/push autorizado; no hay check remoto para esta revisión. El workflow se inspeccionó estáticamente. |

Las advertencias observadas son: Chrome CDP 153 frente a la compatibilidad CDP 152 de Selenium 4.48.0, y el selector de recursos `features` que Cucumber recomienda expresar como selector de paquete. No fallaron las pruebas. Una actualización de Selenium/Cucumber necesita evaluación independiente; no se cambió por esta auditoría.

## Matriz de aceptación

| Criterio | Estado | Evidencia |
|---|---|---|
| CA-01 Estructura | PASS | `src/main` contiene configuración, driver y Page Object; `src/test` contiene Hooks, runner, Steps, soporte, feature y fixture. |
| CA-02 Dependencias y compatibilidad | BLOCKED | Java 21 compiló con caché y Gradle Wrapper; Java 17 y resolución fresca de Maven Central no se ejecutaron. Error TLS local. |
| CA-03 Logging | PASS | `logback-test.xml`; `build/logs/automation.log` generado en la suite final. |
| CA-04 Evidencias automáticas | PASS | Fallo controlado: PNG, attachment `image/png`, log y cierre de driver. |
| CA-05 Reportes Cucumber | PASS | HTML y JSON presentes; JSON contiene resultado del smoke y del fallo controlado en sus respectivas ejecuciones. |
| CA-06 Headless | PASS | Suite completa con `--offline`, `BUILD SUCCESSFUL`. La forma exacta sin `--offline` queda bloqueada por TLS. |
| CA-07 Navegador visible | PASS | Suite completa con `--offline`, `BUILD SUCCESSFUL`. |
| CA-08 Seguridad y `.gitignore` | PASS | Revisión de fuentes y configuración versionadas sin credenciales embebidas; `build/`, `.env`, logs y configuración local ignorados. Revisar siempre capturas reales antes de compartirlas. |
| CA-09 CI/CD | BLOCKED | `.github/workflows/ci.yml` define `quality-gate` headless y subida de artifacts con `if: always()`; falta ejecución del PR de v1.2.0. |
| CA-10 Documentación | PASS | README bilingües, guía, arquitectura, reporting, evidencia, logging, versioning, release process, troubleshooting y changelog auditados/actualizados. |
| CA-11 Manual PDF | PASS | Generador regenerado; PDF A4 de 20 páginas; portada, historial y páginas representativas revisadas visualmente. |
| CA-12 Release Candidate | PASS | `build.gradle` usa `1.2.0`; no se creó tag, release ni fecha de publicación; estado Pending Publication. |

## Riesgos y pendientes

1. Resolver la cadena de certificados/proxy de Java y repetir los comandos sin `--offline` en un entorno con descarga limpia. No desactivar TLS.
2. Validar el PR en GitHub y comprobar `quality-gate`, artifacts y política de protección antes del merge.
3. Si Java 17 es requisito de salida para este release, ejecutar una validación con JDK 17 real; esta auditoría sólo verificó la configuración de toolchain y compiló en Java 21.
4. Investigar las dos advertencias de CDP y selector Cucumber en una actualización planificada, sin elevar versiones a ciegas.
5. La carpeta `output/` ya existía sin seguimiento al iniciar esta tarea; no forma parte de los cambios propuestos.

## Checklist y decisión

- [x] Código, dependencias, seguridad, `.gitignore`, logging, evidencia y reporting revisados.
- [x] Pruebas locales headless, visibles y de fallo controlado ejecutadas con caché.
- [x] Estado Release Candidate / Pending Publication y documentación bilingüe preparados.
- [x] Manual regenerado y revisado.
- [ ] Resolución online de dependencias verificada en un entorno limpio.
- [ ] PR creado y `quality-gate` PASS para el commit final.
- [ ] Revisión, merge, CI posterior al merge y auditoría documental final.
- [ ] Fecha oficial decidida y publicada sólo cuando exista el release.

**Recomendación:** GO para preparar el Pull Request con autorización de commit/push. **NO-GO para tag, GitHub Release y cierre del hito** hasta completar los puntos pendientes.

## Secuencia PowerShell después de autorización

```powershell
.\gradlew.bat clean test -Dheadless=true
.\gradlew.bat clean test -Dheadless=false
git diff --check
git status --short
git add build.gradle src README.md README_EN.md CHANGELOG.md docs scripts/create_manual.py
git commit -m "chore(release): prepare v1.2.0 candidate"
git push -u origin feature/hito-4-release-v1.2.0
```

Abrir el PR hacia `main`; verificar `quality-gate`, reportes y `test-evidence`. Tras revisión y merge, comprobar CI de `main`. Sólo con nueva autorización, publicar el tag y GitHub Release. Después ejecutar `python scripts/finalize_release_docs.py finalize`, revisar el diff y el PDF, abrir el PR documental y verificar su CI y merge. Ejecutar `python scripts/finalize_release_docs.py check` sobre el estado definitivo de `main` antes de registrar el cierre formal. La secuencia y el tratamiento del tag inmutable están en [RELEASE_PROCESS.md](RELEASE_PROCESS.md).

## Archivos de este bloque

Código y versión: `build.gradle`, `DriverFactory.java`, `DriverManager.java`. Documentación: `README.md`, `README_EN.md`, `CHANGELOG.md`, documentos de `docs/`, `scripts/create_manual.py` y el PDF regenerado. No se modificaron dependencias, workflow, tags ni remotos.

## Auditoría documental integral

La pasada documental del 2026-10-07 revisó README bilingües, guía de uso, arquitectura, logging, evidencia, reporting, troubleshooting, versioning, release process, changelog, manual y generador. La documentación de producto presenta capacidades y comandos; este informe y los documentos de release conservan la trazabilidad de hitos y bloques. El manual generado tiene 20 páginas A4. Una búsqueda con límite de palabra sobre el generador y la extracción completa del PDF no encontró `Hito`, `Bloque`, `Sprint`, `Milestone` ni `Phase`. Se verificaron 81 enlaces locales entre archivos Markdown: cero destinos o anchors ausentes. Se inspeccionó visualmente una vista de todas las páginas y, en tamaño legible, portada, historial, arquitectura, stack, capítulos 13 y 14. Una página con el resto aislado de una tabla se corrigió antes de la última generación.

| ID | Criterio | Estado | Evidencia | Archivo | Observación |
|---|---|---|---|---|---|
| DOC-01 | Manual orientado al usuario | PASS | Índice y capítulos explican instalación, ejecución y diagnóstico. | PDF, `scripts/create_manual.py` | Con ejemplos PowerShell. |
| DOC-02 | Hitos retirados del manual | PASS | Cero coincidencias en fuente y PDF extraído. | PDF, generador | Historial de gestión conservado aquí. |
| DOC-03 | Bloques retirados del manual | PASS | Cero coincidencias como término independiente. | PDF, generador | Capítulos 13 y 14 usan títulos funcionales. |
| DOC-04 | Sprints revisados | PASS | Cero `Sprint`/`Sprints` en fuente y PDF. | PDF, generador | Sin referencia interna. |
| DOC-05 | Capítulo 13 actualizado | PASS | Condiciones, PNG, attachment, fallos, privacidad y consulta documentados. | PDF, generador | Coincide con `Hooks` y `EvidenceManager`. |
| DOC-06 | Capítulo 14 actualizado | PASS | Formatos, rutas, comandos, interpretación, CI y límites documentados. | PDF, generador | Coincide con runner y workflow. |
| DOC-07 | Otros capítulos revisados | PASS | Índice, arquitectura, stack, CI, logging y troubleshooting verificados. | PDF, generador | Se quitó una tabla duplicada. |
| DOC-08 | Portada corregida | PASS | Muestra v1.2.0 RC, fecha pendiente y v1.1.0 publicada; sin plan interno. | PDF, generador | Sin fecha inventada. |
| DOC-09 | Historial consistente | PASS | v1.0.0–v1.2.0 y estado de v1.2.0 cotejados. | PDF, README, `CHANGELOG.md` | v1.1.0 sigue como última publicada. |
| DOC-10 | README español | PASS | Estado, capacidades y enlace al informe cotejados. | `README.md` | Orientado al producto. |
| DOC-11 | README inglés | PASS | Mismos contratos funcionales y estado que README español. | `README_EN.md` | Terminología equivalente. |
| DOC-12 | Documentación técnica | PASS | Arquitectura, logging, evidencia, reporting y diagnóstico revisados. | `docs/*.md` | Rutas contrastadas con código. |
| DOC-13 | Historia preservada | PASS | Changelog, versioning e informe mantienen trazabilidad. | `CHANGELOG.md`, `VERSIONING.md`, este informe | Sin borrar releases previos. |
| DOC-14 | Stack verificado | PASS | Java 17/21, Gradle 8.14.5, Selenium 4.48.0, Cucumber 7.34.7, JUnit BOM 5.13.4, SLF4J 2.0.20 y Logback 1.6.5 cotejados. | `build.gradle`, wrapper, PDF | No se cambiaron dependencias en esta pasada. |
| DOC-15 | Generador actualizado | PASS | Python ejecutó con `-W error` y produjo el PDF. | `scripts/create_manual.py` | Fuente única del manual. |
| DOC-16 | PDF regenerado | PASS | Archivo A4 de 20 páginas generado. | PDF | Salida dentro del repositorio. |
| DOC-17 | Calidad visual | PASS | Contacto de 20 páginas y revisión ampliada de secciones clave; sin cortes ni desbordes visibles. | PDF | Render de Poppler mostró avisos de fuentes de visualización, sin defectos visibles. |
| DOC-18 | Enlaces internos | PASS | 81 enlaces locales verificados; cero destinos o anchors ausentes. | README y `docs/*.md` | Enlaces externos no probados en esta verificación. |
| DOC-19 | Glosario revisado | PASS | Se conservó el glosario y se corrigió la entrada genérica de GitHub. | PDF, generador | Dos páginas legibles. |
| DOC-20 | Cierre documental preparado | PASS | Secuencia posterior al release y comandos PowerShell descritos. | `RELEASE_PROCESS.md` | Su ejecución está pendiente. |
| DOC-21 | Sin fechas inventadas | PASS | v1.2.0 muestra fecha pendiente; v1.1.0 conserva 2026-10-01. | PDF, README, docs | Verificar fecha real tras GitHub Release. |
| DOC-22 | Capacidades fieles al código | PASS | Plugins `pretty/html/json`, Logback, `EvidenceManager` y CI cotejados con fuente. | PDF, README, código, workflow | Sin dashboard ni despliegue automático. |

**Resultado documental:** GO para presentar el cambio en un Pull Request cuando se autoricen commit y push. La publicación y el cierre formal continúan bloqueados por las verificaciones remotas descritas arriba.

## Control automático del cierre definitivo

`scripts/finalize_release_docs.py` prepara el mismo snapshot documental que formará parte del PR y tag de v1.2.0. `stage --date` actualiza los campos vigentes y regenera el PDF; `check --date` valida la consistencia sin escribir; `pretag --date` exige coincidencia con el día UTC real y un `main` limpio; `postrelease --date` coteja `published_at` y versión con GitHub. El informe conserva los estados anteriores como evidencia histórica. El cierre del hito **no** es PASS hasta confirmar CI, tag, release y fecha real.

Inventario histórico de transición: los estados candidatos aparecían en la portada y tabla de v1.2.0 del manual, `README.md`, `README_EN.md`, encabezado de `CHANGELOG.md`, portada y tabla de la guía, encabezados de arquitectura, logging, evidencias, reporting y troubleshooting, y sección de contexto de `VERSIONING.md`. `RELEASE_PROCESS.md` describe la preparación y los controles de publicación. El script actualiza esos campos de forma localizada y preserva las entradas antiguas de v1.0.0 a v1.1.0. Las referencias a **Release Candidate / Pending Publication** de este informe son evidencia histórica, no el estado del snapshot definitivo.

Validación histórica del procedimiento anterior: la simulación se ejecutó en una copia temporal y rechazó estados provisionales, última versión errónea, fechas contradictorias y PDF desactualizado. La fecha de simulación nunca se escribió en el repositorio. La preparación actual usa la fecha objetivo indicada en el release y requiere una nueva comprobación UTC antes del tag. Estas pruebas no constituyen publicación ni cierre documental.
