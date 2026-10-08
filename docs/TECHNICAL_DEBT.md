# Deuda técnica abierta

[English](../docs_en/TECHNICAL_DEBT.md) · [Índice](README.md)

Registro de advertencias observadas durante la ejecución de la imagen Docker de v1.3.0 en desarrollo. La ejecución local de Codex con bind mount terminó con BUILD SUCCESSFUL y el escenario Example Domain PASSED; las advertencias no fallaron la suite. La confirmación previa en Docker Desktop 4.89.0 también fue facilitada por el usuario. Ninguna de estas entradas declara cerrado el Bloque 1 ni cambia dependencias.

## TECH-001 — Compatibilidad Selenium CDP

| Campo | Registro |
|---|---|
| Estado / prioridad | **OPEN / MEDIA** |
| Descripción | Chrome 155 se inicia, pero Selenium 4.48.0 selecciona un módulo CDP cercano en vez de uno exacto para la versión del navegador. |
| Evidencia | En stderr: “Unable to find an exact match for CDP version 155, returning the closest version; found: 152”. Reproducido por Codex en la ejecución Docker con bind mount; el usuario también informó la advertencia. WebDriver se inicializó y el escenario pasó. |
| Causa probable | Desfase entre Chrome 155 y los módulos CDP incluidos por la versión actual de Selenium. Debe confirmarse al evaluar dependencias. |
| Impacto potencial | Funciones que dependan de DevTools/CDP podrían comportarse de manera distinta o fallar; el smoke test actual no demuestra compatibilidad de todas esas funciones. |
| Solución candidata | Evaluar una versión compatible de Selenium y su módulo CDP correspondiente, sin cambiar versiones en este bloque. |
| Regresión necesaria | Ejecutar smoke y suite completa con Chrome/ChromeDriver alineados; verificar inicialización WebDriver, pruebas headless locales y Docker, reportes/evidencias y cualquier uso real de CDP. Confirmar que desaparece la advertencia sin nuevos fallos. |
| Bloque posterior propuesto | Bloque posterior dedicado a compatibilidad de dependencias, sujeto a autorización y pruebas; no Bloque 1. |

## TECH-002 — Selector de descubrimiento Cucumber

| Campo | Registro |
|---|---|
| Estado / prioridad | **OPEN / BAJA** |
| Descripción | El runner selecciona el recurso de classpath `features`; Cucumber/JUnit recomienda un selector de paquete para este caso. |
| Evidencia | En stderr: “The classpath resource selector 'features' should not be used to select features in a package.” Se informó dos veces durante discovery en la ejecución Docker reproducida por Codex; el usuario también la reportó. El escenario fue descubierto y pasó. |
| Causa probable | La anotación `@SelectClasspathResource("features")` en `RunCucumberTest` no coincide con la recomendación del motor actual. |
| Impacto | Advertencia no crítica; posible fragilidad en el descubrimiento futuro de Features. No hubo fallo en el escenario actual. |
| Solución candidata | Revisar la configuración del runner y el selector recomendado por Cucumber/JUnit; no modificar el runner en este bloque. |
| Regresión necesaria | Confirmar descubrimiento y conteo de todas las Features, filtros de tags, ejecución Gradle/JUnit local y Docker, reportes Cucumber HTML/JSON y resultado de CI. |
| Bloque posterior propuesto | Bloque posterior de mantenimiento del runner, sujeto a autorización y pruebas; no Bloque 1. |
