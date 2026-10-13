# Hito 5, Bloque 4 — preparación de v1.3.0

[English](../docs_en/HITO5_BLOCK4_RELEASE_PREPARATION.md) · [Índice](README.md)

## Estado

- Candidata: **v1.3.0 — Docker & CI Integration**.
- Estado: **Release Candidate / Pending Publication**.
- Fecha objetivo: **12/10/2026 UTC (ISO: 2026-10-12)**. Es una fecha de planificación y no acredita publicación. Sustituye la fecha objetivo anterior; las fechas de validación registradas se conservan como evidencia histórica.
- Los PDF oficiales usan desde esta preparación la presentación final **Stable / Validated / Published**. Sus metadatos internos los identifican como artefactos preparados para distribución; deben contrastarse con el tag, commit y `published_at` de GitHub antes de adjuntarlos al release.
- Última versión publicada: **v1.2.0**, 8 de octubre de 2026, 06:19:01 UTC.

## Alcance preparado

La candidata incorpora la imagen Docker, el job `docker-tests`, hardening de imagen y ejecución, y recolección selectiva de evidencias. El job `quality-gate` conserva la ejecución Gradle headless. El PR del hardening y el push posterior a `main` registraron ambos jobs exitosos con `test-evidence` y `docker-test-evidence`.

La preparación actual alinea versión Gradle, README, changelog, documentación técnica ES/EN, manuales PDF y verificador. No crea commit, tag, GitHub Release, push ni merge.

## Deuda y límites

- TECH-001 continúa OPEN: Selenium 4.48.0 selecciona CDP 152 frente a Chrome/CDP 155. Las pruebas WebDriver convencionales pasan; esto no valida funciones dependientes de DevTools.
- TECH-002 está CLOSED: el runner usa `@SelectPackages("features")` y la validación registrada no reprodujo la advertencia anterior.
- Los paquetes apt no están fijados mediante snapshot; un build futuro sin caché puede variar.
- Chrome usa `--no-sandbox` dentro del contenedor.

## Validación de preparación — 2026-10-09

- `.\gradlew.bat clean test -Dheadless=true --offline`: **PASS — BUILD SUCCESSFUL**. El escenario Cucumber local terminó **PASSED**. Chrome/CDP 153 produjo la advertencia de compatibilidad con CDP 152 registrada en TECH-001.
- `.\gradlew.bat clean test -Dheadless=false --offline`: **PASS — BUILD SUCCESSFUL**. El escenario Cucumber local terminó **PASSED** y se conservó la misma advertencia CDP 153 → 152.
- `docker build --progress=plain -t selenium-java-cucumber-template:1.3.0-dev .`: **PASS**; `testClasses` terminó correctamente.
- `docker run --rm --shm-size=2g selenium-java-cucumber-template:1.3.0-dev`: **PASS**; 6/6 pruebas, un escenario Cucumber y `BUILD SUCCESSFUL`. Se observó la advertencia CDP 155 → 152 registrada en TECH-001; no apareció la advertencia anterior del selector Cucumber.
- Validación documental: **PASS**, 37 archivos Markdown, 251 enlaces internos y cero errores.
- Verificador `prepare`: **PASS**.
- Simulación `preview`: **PASS**; 26 documentos Markdown y ambos PDF pueden pasar al estado publicado sin escribir cambios ni afirmar publicación.
- Ambos PDF: **PASS**; la revisión visual cubrió todas las páginas.
- No se reprodujo la advertencia del selector Cucumber/JUnit Platform.

Las ejecuciones offline acreditan el comportamiento con las dependencias ya disponibles en caché; no sustituyen una comprobación futura de resolución online. No se actualizaron dependencias.

## Publicación

Mientras no existan el tag y el GitHub Release, v1.3.0 debe permanecer como Release Candidate / Pending Publication y v1.2.0 como última publicada. Tras la publicación autorizada, `finalize` obtiene el `published_at` real, actualiza los documentos vigentes y regenera ambos PDF; `postrelease` contrasta después el tag, la fecha UTC y el estado documental. Los PDF candidatos no deben adjuntarse al release. La secuencia completa y la integración del diff posterior están en [RELEASE_PROCESS.md](RELEASE_PROCESS.md).
