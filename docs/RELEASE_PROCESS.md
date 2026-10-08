# Proceso de release

[English](../docs_en/RELEASE_PROCESS.md) · [Índice](README.md)

Este proceso describe futuras publicaciones; no ejecuta ninguna acción de Git o GitHub. La versión vigente [v1.2.0](https://github.com/IsraelBaz-coder/selenium-java-cucumber-automation-template/releases/tag/v1.2.0) ya se publicó el **8 de octubre de 2026 a las 06:19:01 UTC**. Su preparación previa se conserva en la [auditoría histórica](HITO4_RELEASE_AUDIT.md). No repita sus comandos de preparación ni cambie su tag.

## 1. Trabajar en una rama

Use una rama enfocada `feature/*`, `fix/*`, `docs/*` o `refactor/*` desde la base aprobada. Documente el alcance y evite archivos locales, secretos o artifacts generados.

## 2. Actualizar código y documentación

Actualice sólo el comportamiento previsto. Mantenga README ES/EN, docs/ y docs_en/ equivalentes; regenere ambos PDF con `python scripts/create_manual.py`. Registre cambios visibles en [CHANGELOG.md](../CHANGELOG.md). No presente una versión sin publicar como publicada.

## 3. Validar

En Windows ejecute `.\gradlew.bat clean test -Dheadless=true` desde la raíz (sin los espacios de presentación). Valide el modo visible si hay escritorio. Cuando afecte tags, ejecute `.\gradlew.bat clean test -Dheadless=true "-Dcucumber.filter.tags=@example"`. Revise `git diff --check` y `git status`.

El workflow `.github/workflows/ci.yml` usa Java 21 y `./gradlew clean test -Dheadless=true`. El job `quality-gate` falla cuando Gradle sale con código distinto de cero. `test-evidence` intenta reunir reportes Cucumber HTML/JSON, Gradle HTML, JUnit XML, logs y capturas disponibles; el artifact no cambia el resultado de las pruebas. Consulte [reportes](REPORTING.md).

## 4. Pull request e integración

Incluya propósito, cambios, pruebas reales y resultados. Para PR hacia `main`, espere el check `quality-gate` y revise **Checks → Details** ante un fallo. Descargue `test-evidence` desde **Actions** si existe. Integre sólo después de revisión y checks obligatorios; el ruleset documentado de `main` exige PR y check satisfactorio.

## 5. Comprobar publicación

Una vez autorizado y publicado un futuro GitHub Release, compare su tag y `published_at` UTC con la documentación y los manuales. Si no coinciden, registre el problema y realice una corrección documental revisada; no mueva un tag histórico. Para v1.2.0, el verificador de sólo lectura admite `python scripts/finalize_release_docs.py check --date 2026-10-08`.
