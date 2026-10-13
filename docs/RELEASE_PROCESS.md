# Proceso de release

[English](../docs_en/RELEASE_PROCESS.md) · [Índice](README.md)

Este proceso describe futuras publicaciones; no ejecuta ninguna acción de Git o GitHub. La versión publicada anterior [v1.2.0](https://github.com/IsraelBaz-coder/selenium-java-cucumber-automation-template/releases/tag/v1.2.0) ya se publicó el **8 de octubre de 2026 a las 06:19:01 UTC**. Su preparación previa se conserva en la [auditoría histórica](HITO4_RELEASE_AUDIT.md). No repita sus comandos de preparación ni cambie su tag.

La versión **v1.3.0 — Docker & CI Integration** está oficialmente publicada con estado **Stable / Validated / Published** desde el **2026-10-13T04:56:27Z**, según GitHub Release.

## 1. Trabajar en una rama

Use una rama enfocada `feature/*`, `fix/*`, `docs/*` o `refactor/*` desde la base aprobada. Documente el alcance y evite archivos locales, secretos o artifacts generados.

## 2. Actualizar código y documentación

Actualice sólo el comportamiento previsto. Mantenga README ES/EN, docs/ y docs_en/ equivalentes; antes de publicar, regenere ambos PDF oficiales con `python scripts/create_manual.py --mode release-ready`. Esa presentación final queda marcada internamente como preparada para distribución y debe verificarse contra GitHub antes de adjuntarla. El modo `published` queda reservado al flujo verificado de `finalize_release_docs.py`. Registre cambios visibles en [CHANGELOG.md](../CHANGELOG.md).

## 3. Validar

En Windows ejecute `.\gradlew.bat clean test -Dheadless=true` desde la raíz (sin los espacios de presentación). Valide el modo visible si hay escritorio. Cuando afecte tags, ejecute `.\gradlew.bat clean test -Dheadless=true "-Dcucumber.filter.tags=@example"`. Revise `git diff --check` y `git status`.

El workflow `.github/workflows/ci.yml` usa Java 21 y `./gradlew clean test -Dheadless=true`. El job `quality-gate` falla cuando Gradle sale con código distinto de cero. `test-evidence` intenta reunir reportes Cucumber HTML/JSON, Gradle HTML, JUnit XML, logs y capturas disponibles; el artifact no cambia el resultado de las pruebas. Consulte [reportes](REPORTING.md).

## 4. Pull request e integración

Incluya propósito, cambios, pruebas reales y resultados. Para PR hacia `main`, espere el check `quality-gate` y revise **Checks → Details** ante un fallo. Descargue `test-evidence` desde **Actions** si existe. Integre sólo después de revisión y checks obligatorios; el ruleset documentado de `main` exige PR y check satisfactorio.

## 5. Preparar y finalizar v1.3.0

Antes del merge, ejecute `python scripts/finalize_release_docs.py prepare --date 2026-10-13` y `python scripts/finalize_release_docs.py preview-final --date 2026-10-13`. `preview-final` transforma en memoria los documentos vigentes, comprueba que no queden metadatos activos de candidata y genera ambos PDF definitivos en un directorio temporal; no escribe el repositorio ni acredita publicación.

Orden exacto posterior al merge:

1. Confirmar que `main` contiene el commit aprobado y que `quality-gate` y `docker-tests` finalizaron correctamente.
2. Crear y publicar el tag y el GitHub Release autorizados con nombre `v1.3.0 — Docker & CI Integration`. No adjuntar todavía los PDF candidatos.
3. Confirmar que GitHub expone `published_at` y ejecutar `git fetch --tags` para disponer del tag local.
4. Identificar el SHA completo del commit autorizado por el merge. Ejecutar `python scripts/finalize_release_docs.py finalize --date 2026-10-13 --expected-commit <SHA_AUTORIZADO>`. El comando consulta el GitHub Release real, rechaza draft/prerelease, valida nombre y tag, verifica la fecha real de `published_at` frente a la fecha originalmente planificada del 12 de octubre UTC y comprueba que el tag apunte al commit autorizado. Después actualiza README, changelog y documentación técnica vigente, y regenera ambos PDF como Stable / Validated / Published. Si GitHub registra otro día UTC, informa la discrepancia y utiliza la fecha real confirmada. No crea commits, tags, releases ni uploads.
5. Ejecutar `python scripts/validate_docs.py` y `python scripts/finalize_release_docs.py postrelease --date 2026-10-13 --expected-commit <SHA_AUTORIZADO>`. Revisar visualmente las portadas y los historiales de ambos PDF.
6. Integrar el diff post-release mediante el mecanismo permitido por la protección de `main`. Si `main` exige Pull Request, esta integración requiere un PR; no se debe eludir el ruleset ni declarar Published antes de GitHub.
7. Adjuntar exclusivamente los PDF ya finalizados: `gh release upload v1.3.0 docs/Manual_Template_Automatizacion_Selenium_Java_Cucumber.pdf docs_en/Manual_Selenium_Java_Cucumber_Automation_Template.pdf --clobber`.
8. Descargar ambos assets del release, comprobar que coinciden con los PDF locales y ejecutar nuevamente `postrelease` antes de cerrar el Hito 5.

La dependencia de `published_at` hace imposible incorporar el estado Published al commit previo a la publicación sin inventar una fecha o afirmar anticipadamente el release. El procedimiento reduce la corrección posterior a una sola intervención controlada y conserva intactos los informes históricos.
