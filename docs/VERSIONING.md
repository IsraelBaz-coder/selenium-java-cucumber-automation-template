# Versionado

[English](../docs_en/VERSIONING.md) · [Índice](README.md)

Este proyecto sigue [Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html): `MAJOR.MINOR.PATCH`. MAJOR corresponde a cambios incompatibles; MINOR, a funcionalidad compatible; PATCH, a correcciones compatibles. Los tags Git usan el prefijo `v`; `build.gradle` omite ese prefijo.

## Estado actual e historia

| Versión | Estado documentado |
|---|---|
| v1.2.0 | Última versión publicada; 8 de octubre de 2026, 06:19:01 UTC; Stable / Validated / Published. Hito 4: logging, evidencias, reporting y cierre de release. |
| v1.1.0 | Publicada el 1 de octubre de 2026; Hito 3: CI/CD, artifacts y `quality-gate`. |
| v1.0.2 | Hotfix de documentación publicado el 26 de septiembre de 2026. |
| v1.0.1 | Hardening y preparación CI/CD, publicado el 25 de septiembre de 2026. |
| v1.0.0 | Base estable inicial, publicada el 18 de septiembre de 2026. |

El [GitHub Release v1.2.0](https://github.com/IsraelBaz-coder/selenium-java-cucumber-automation-template/releases/tag/v1.2.0) confirma tag, versión, estado y fecha. El [changelog](../CHANGELOG.md) conserva los cambios históricos. La [auditoría del Hito 4](HITO4_RELEASE_AUDIT.md) contiene estados de candidato como evidencia del periodo anterior a la publicación.

## Cierre documental de una versión futura

1. Completar trabajo técnico, pruebas locales y documentación en ambos idiomas, incluida la generación de PDF.
2. Validar el pull request en CI; integrar sólo después de la revisión y los checks obligatorios.
3. Antes de publicar, comprobar versión, fechas previstas y contenido del tag. Una fecha prevista no demuestra publicación.
4. Tras el GitHub Release, comprobar `published_at` en UTC, tag y versión; reflejar la fecha real de forma consistente en README, guía, changelog y manuales.
5. Registrar el cierre formal sólo tras verificar el release. Conservar informes históricos y tags existentes.

**Stable / Validated** no implica **Published**. Use **Stable / Validated / Published** sólo cuando el tag y el GitHub Release sean reales. Los estados provisionales pueden permanecer en un informe histórico claramente identificado, pero no en la portada o el resumen vigente. No mueva un tag existente para corregir documentación.
