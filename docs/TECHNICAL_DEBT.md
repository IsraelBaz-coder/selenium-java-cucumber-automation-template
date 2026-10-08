# Deuda técnica — Hito 5, Bloque 3

[English](../docs_en/TECHNICAL_DEBT.md) · [Índice](README.md)

## TECH-001 — Compatibilidad Selenium CDP

**Estado: OPEN.** `build.gradle` fija Selenium 4.48.0; Docker fija Chrome y ChromeDriver 155.0.8059.39. La ejecución local observada usa Chrome/CDP 153; el driver local lo resuelve Selenium Manager. En ambos entornos Selenium elige CDP 152 y emite una advertencia. No hay llamadas explícitas a DevTools, `executeCdpCommand` ni APIs CDP en `src/`; el smoke usa WebDriver convencional y pasa.

**Impacto:** la advertencia no impide el escenario actual, pero no acredita funciones futuras dependientes de CDP. **Decisión:** conservar las versiones actuales; no añadir un módulo CDP sin una necesidad funcional ni actualizar navegador o Selenium a ciegas. En una tarea de compatibilidad, identificar la versión CDP soportada por la versión candidata de Selenium, alinear navegador y driver, probar cualquier uso real de DevTools y repetir la suite local y Docker hasta eliminar la advertencia sin regresión. No ocultar la advertencia en logs.

## TECH-002 — Selector de descubrimiento Cucumber

**Estado: CLOSED tras validación local y Docker del Bloque 3.** El aviso procedía de `@SelectClasspathResource("features")` en `RunCucumberTest`: Cucumber/JUnit Platform pedía el selector de paquete. Se sustituyó por `@SelectPackages("features")`, manteniendo `@IncludeEngines("cucumber")`, glue, plugins y estructura `src/test/resources/features/`.

**Evidencia:** antes del cambio, la ejecución local mostró dos avisos de discovery. Después, la suite local headless, visible y filtrada por `@example` ejecutó 6/6 pruebas (un escenario) sin ese aviso. La ejecución Docker posterior confirmó el mismo conteo y ausencia del aviso. Los reportes HTML/JSON y XML permanecieron disponibles. La ejecución de GitHub Actions de esta rama queda pendiente del PR.
