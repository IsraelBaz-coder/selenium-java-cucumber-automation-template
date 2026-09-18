# Troubleshooting

**Release:** v1.0.0 · **Estado:** Stable / Validated · **Fecha:** 17 de septiembre de 2026

| Síntoma | Causa probable | Solución |
|---|---|---|
| `java` no reconocido | JDK/Path incorrecto | Instale JDK 21 o 17, reinicie PowerShell y valide `java -version`. |
| Java incorrecto | VS Code/Gradle usa otro JDK | Configure `JAVA_HOME` al JDK elegido y revise `./gradlew.bat --version`; ejecute con `-PjavaVersion=17` o `-PjavaVersion=21`. |
| Wrapper no ejecuta | Ruta/permisos | Ejecute desde raíz: `.\gradlew.bat test`; preserve `gradle/wrapper`. |
| Dependencias no descargan | Red, proxy o Maven bloqueado | Revise red/proxy y ejecute `dependencies --refresh-dependencies`. |
| Chrome/Edge no inicia | Navegador/driver | Actualice navegador y revise salida Selenium Manager. |
| Error WebDriver | Driver no creado/cerrado | Revise Hooks y `browser`; no use driver fuera del escenario. |
| Headless falla | Entorno restringido | Use `-Dheadless=true`; revise permisos y tamaño de ventana. |
| Feature no ejecuta | Ruta/extensión/tags | Use `.feature` bajo `src/test/resources/features`; valide tags. |
| Step no encontrado | Texto/glue no coincide | Haga coincidir Gherkin/anotación y conserve el glue `com.automation.template`. |
| CI falla, local no | Configuración diferente | Compare variables, use headless y publique artifacts. |
| Puerto ocupado | Servicio existente | Identifique proceso/contenedor y ajuste mapeo según política. |
| Docker o Healenium no responde | Se intentó aplicar una integración que no pertenece al template | Docker y Healenium no forman parte de v1.0.0; no son requisito para ejecutar las pruebas. |
