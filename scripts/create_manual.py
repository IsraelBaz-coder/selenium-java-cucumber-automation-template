from pathlib import Path
from shutil import copy2
from math import atan2, cos, sin, pi
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, KeepTogether, Flowable

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs' / 'Manual_Template_Automatizacion_Selenium_Java_Cucumber.pdf'
EXTERNAL_OUT = ROOT.parent / 'Manual_Template_Automatizacion_Selenium_Java_Cucumber.pdf'

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='Cover', parent=styles['Title'], fontName='Helvetica-Bold', fontSize=25, leading=31, textColor=colors.HexColor('#152B4E'), alignment=TA_CENTER, spaceAfter=16))
styles.add(ParagraphStyle(name='CoverSub', parent=styles['BodyText'], fontName='Helvetica', fontSize=13, leading=19, alignment=TA_CENTER, textColor=colors.HexColor('#3C4A5A')))
styles.add(ParagraphStyle(name='H1x', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=18, leading=23, textColor=colors.HexColor('#152B4E'), spaceBefore=8, spaceAfter=10))
styles.add(ParagraphStyle(name='H2x', parent=styles['Heading2'], fontName='Helvetica-Bold', fontSize=13, leading=17, textColor=colors.HexColor('#1F4D7A'), spaceBefore=8, spaceAfter=6))
styles.add(ParagraphStyle(name='Bodyx', parent=styles['BodyText'], fontName='Helvetica', fontSize=9.5, leading=14, spaceAfter=7))
styles.add(ParagraphStyle(name='CodeX', parent=styles['BodyText'], fontName='Courier', fontSize=7.7, leading=10, backColor=colors.HexColor('#F2F4F7'), leftIndent=8, rightIndent=8, borderPadding=6, spaceAfter=8))
styles.add(ParagraphStyle(name='GlossaryX', parent=styles['BodyText'], fontName='Helvetica', fontSize=7.5, leading=9, spaceAfter=0))
styles.add(ParagraphStyle(name='GlossaryHeader', parent=styles['BodyText'], fontName='Helvetica-Bold', fontSize=8, leading=9, textColor=colors.white, spaceAfter=0))

def footer(canvas, doc):
    if doc.page > 1:
        canvas.saveState(); canvas.setStrokeColor(colors.HexColor('#D9E1EA')); canvas.line(2*cm, 1.45*cm, A4[0]-2*cm, 1.45*cm)
        canvas.setFont('Helvetica', 8); canvas.setFillColor(colors.HexColor('#526273'))
        canvas.drawString(2*cm, 0.9*cm, 'Automation Template Selenium Java Cucumber')
        canvas.drawRightString(A4[0]-2*cm, 0.9*cm, f'Página {doc.page}')
        canvas.restoreState()

def p(text, style='Bodyx'): return Paragraph(text, styles[style])
def heading(text): return p(text, 'H1x')
def table(rows, widths):
    data = [[Paragraph(str(cell), styles['GlossaryHeader']) for cell in rows[0]]]
    data += [[p(str(cell)) for cell in row] for row in rows[1:]]
    t=Table(data, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#152B4E')),('TEXTCOLOR',(0,0),(-1,0),colors.white),('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),('GRID',(0,0),(-1,-1),0.35,colors.HexColor('#CBD5E1')),('VALIGN',(0,0),(-1,-1),'MIDDLE'),('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),('BACKGROUND',(0,1),(-1,-1),colors.white)]))
    return t

def glossary_table(rows):
    data = [[Paragraph('Término', styles['GlossaryHeader']), Paragraph('Definición', styles['GlossaryHeader'])]]
    data += [[Paragraph(term, styles['GlossaryX']), Paragraph(definition, styles['GlossaryX'])] for term, definition in rows]
    t = Table(data, colWidths=[4.5*cm, 11.8*cm], repeatRows=1)
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#152B4E')),('GRID',(0,0),(-1,-1),0.3,colors.HexColor('#CBD5E1')),('VALIGN',(0,0),(-1,-1),'MIDDLE'),('LEFTPADDING',(0,0),(-1,-1),5),('RIGHTPADDING',(0,0),(-1,-1),5),('TOPPADDING',(0,0),(-1,-1),3),('BOTTOMPADDING',(0,0),(-1,-1),3),('BACKGROUND',(0,1),(-1,-1),colors.white)]))
    return t

def version_table(rows):
    data = [[Paragraph('Versión', styles['GlossaryHeader']), Paragraph('Fecha / estado', styles['GlossaryHeader']), Paragraph('Cambios principales', styles['GlossaryHeader'])]]
    data += [[Paragraph(version, styles['GlossaryX']), Paragraph(date, styles['GlossaryX']), Paragraph(changes, styles['GlossaryX'])] for version, date, changes in rows]
    t = Table(data, colWidths=[2.2*cm, 3.4*cm, 10.7*cm], repeatRows=1)
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#152B4E')),('GRID',(0,0),(-1,-1),0.3,colors.HexColor('#CBD5E1')),('VALIGN',(0,0),(-1,-1),'MIDDLE'),('LEFTPADDING',(0,0),(-1,-1),5),('RIGHTPADDING',(0,0),(-1,-1),5),('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4),('BACKGROUND',(0,1),(-1,-1),colors.white)]))
    return t

class LoggingDiagram(Flowable):
    """Vector diagrams for the Block 1 logging architecture and event flow."""

    def __init__(self, kind):
        super().__init__()
        self.kind = kind
        self.width = 16.3 * cm
        self.height = 10.5 * cm if kind == 'architecture' else 14.0 * cm

    def _box(self, canvas, x, y, width, lines):
        height = 0.9 * cm if len(lines) == 1 else 1.15 * cm
        canvas.setFillColor(colors.HexColor('#EEF4FA'))
        canvas.setStrokeColor(colors.HexColor('#40709E'))
        canvas.roundRect(x, y, width, height, 5, fill=1, stroke=1)
        canvas.setFillColor(colors.HexColor('#152B4E'))
        canvas.setFont('Helvetica-Bold', 8.5)
        for index, line in enumerate(lines):
            canvas.drawCentredString(x + width / 2, y + height / 2 + (len(lines) - 1) * 5 - index * 10 - 3, line)
        return height

    def _arrow(self, canvas, x1, y1, x2, y2):
        canvas.setStrokeColor(colors.HexColor('#607D98'))
        canvas.setFillColor(colors.HexColor('#607D98'))
        canvas.setLineWidth(1.2)
        canvas.line(x1, y1, x2, y2)
        angle = atan2(y2 - y1, x2 - x1)
        for offset in (pi / 6, -pi / 6):
            canvas.line(x2, y2, x2 - 6 * cos(angle + offset), y2 - 6 * sin(angle + offset))

    def draw(self):
        c = self.canv
        center = self.width / 2
        if self.kind == 'architecture':
            self._box(c, center - 65, 267, 130, ['Escenario Cucumber'])
            self._box(c, center - 50, 222, 100, ['Hooks'])
            self._box(c, 15, 157, 165, ['Ciclo del escenario', 'inicio y resultado'])
            self._box(c, self.width - 180, 157, 165, ['Ciclo WebDriver', 'Factory y Manager'])
            self._box(c, center - 50, 112, 100, ['SLF4J'])
            self._box(c, center - 50, 67, 100, ['Logback'])
            self._box(c, 50, 7, 105, ['Consola'])
            self._box(c, self.width - 165, 7, 150, ['build/logs/', 'automation.log'])
            self._arrow(c, center, 267, center, 248)
            self._arrow(c, center - 25, 222, 97, 190)
            self._arrow(c, center + 25, 222, self.width - 97, 190)
            self._arrow(c, 97, 157, center - 25, 138)
            self._arrow(c, self.width - 97, 157, center + 25, 138)
            self._arrow(c, center, 112, center, 93)
            self._arrow(c, center - 25, 67, 102, 33)
            self._arrow(c, center + 25, 67, self.width - 90, 40)
        else:
            labels = [
                ['Inicio del escenario'],
                ['Nombre y configuración efectiva'],
                ['Navegador y modo headless'],
                ['Inicialización de WebDriver'],
                ['Ejecución del test'],
                ['Resultado y fin del escenario'],
                ['Cierre de WebDriver'],
                ['Consola + build/logs/automation.log'],
            ]
            positions = [350 - index * 49 for index in range(len(labels))]
            for y, label in zip(positions, labels):
                self._box(c, center - 117, y, 234, label)
            for previous, following in zip(positions, positions[1:]):
                self._arrow(c, center, previous, center, following + 26)

story=[]
story += [Spacer(1, 5.3*cm), p('Automation Template Selenium Java Cucumber','Cover'), p('Manual de uso', 'CoverSub'), Spacer(1, .4*cm), p('Template reutilizable de automatización Web UI', 'CoverSub'), Spacer(1, 1.7*cm), p('v1.1.0 - Stable / Validated / Published<br/>Hito 3 - Completed / Validated<br/>Publicación v1.1.0: 1 de octubre de 2026<br/>v1.2.0 - Hito 4 en desarrollo, Bloque 1<br/>Sin fecha de publicación de v1.2.0<br/>Java 21 (predeterminado) | Java 17 (compatible)<br/>Selenium 4.48.0<br/>Cucumber 7.34.7<br/>JUnit 5.13.4<br/>Gradle 8.14.5', 'CoverSub'), PageBreak()]
story += [heading('Índice'), p('1. Inicio rápido para primera vez<br/>2. Arquitectura<br/>3. Stack, requisitos y VS Code<br/>3.1 Configurar Java 17 paso a paso<br/>4. Configuración y comandos<br/>5. Primera automatización<br/>6. Reutilización<br/>7. Contrato CI/CD, buenas prácticas y soporte<br/>8. CI/CD con GitHub Actions<br/>9. Cómo ejecutar y revisar el CI/CD<br/>10. Quality Gate, fallos y evidencias<br/>11. Protección de main y validación de Hito 3<br/>12. Logging y observabilidad básica<br/>13. Glosario'), Spacer(1,10), heading('Propósito'), p('El manual explica desde cero el flujo Git, Pull Request y GitHub Actions. Para crear nuevas pruebas se necesitan conocimientos básicos de Java. El ejemplo incluido es neutral y debe sustituirse por la aplicación bajo prueba.'), p('Información del documento', 'H2x'), table([['Campo', 'Valor'], ['Autor / Creador del template', 'Israel Baz'], ['Rol', 'Test Automation / Prompt Engineering / AI Automation'], ['Mantenimiento', 'Israel Baz']], [5.2*cm, 11.1*cm]), Spacer(1,8), p('Estado e historial de release', 'H2x'), version_table([('v1.2.0', 'En desarrollo; sin fecha', 'Hito 4, Bloque 1: logging base con SLF4J y Logback. No publicado.'), ('v1.1.0', '1 de octubre de 2026', 'Stable / Validated / Published. Hito 3 y Bloques 1-4 Completed / Validated. CI y Quality Gate validados.'), ('v1.0.2', '25 de septiembre de 2026', 'Documentation-only Hotfix, Stable / Validated / Published.'), ('v1.0.1', '25 de septiembre de 2026', 'Hardening + CI/CD Readiness. Estado Stable / Validated / Published.'), ('v1.0.0', '17 de septiembre de 2026', 'First Stable Release con Java 21 predeterminado, ejemplo y manual PDF.')]), PageBreak()]
story += [heading('1. Inicio rápido para primera vez'), p('Siga estos pasos sin modificar ningún archivo. Si un comando termina con BUILD SUCCESSFUL, se ejecutó correctamente. Si termina con BUILD FAILED, conserve el mensaje y consulte Troubleshooting antes de cambiar código.'), p('Paso 1 - Abra PowerShell y navegue a la raíz:', 'H2x'), p('cd C:\\ruta\\automation-template-selenium-java-cucumber', 'CodeX'), p('Paso 2 - Ejecute la prueba de ejemplo sin ventana visible:', 'H2x'), p('.\\gradlew.bat test -Dheadless=true', 'CodeX'), p('Paso 3 - Abra el reporte de ejecución:', 'H2x'), p('Abra build/reports/cucumber/cucumber.html. El escenario abre la fixture HTML local src/test/resources/fixtures/example_page.html y valida el encabezado Example Domain. La fixture está versionada y no depende del contenido de un sitio externo; el escenario se reproduce en CI.'), p('Paso 4 - Ejecute con navegador visible:', 'H2x'), p('Ejecute .\\gradlew.bat clean test sin el parámetro headless.'), p('Cómo comprobar VS Code', 'H2x'), p('Debe ver src, gradle, build.gradle y settings.gradle. Abra example_domain.feature: debe aparecer coloreado como Gherkin. Abra ExampleDomainPage.java: Java no debe mostrar imports en rojo. Si VS Code solicita un JDK, seleccione Java 21 y espere que termine "Importing Gradle project".'), p('Lista antes de pedir ayuda', 'H2x'), p('Estoy en la raíz del proyecto; java -version muestra Java 21; el navegador está instalado; la fixture local existe; la Feature termina en .feature y está bajo src/test/resources/features; cada frase Gherkin coincide con su Step; no guardé credenciales ni tokens en Git.'), PageBreak()]
story += [heading('2. Arquitectura'), p('El template estandariza la automatización Web UI: configuración externa, navegador, ejecución BDD, Page Object Model, evidencia y reportes. Es adecuado para proyectos que operan en Chrome o Edge. La configuración tiene prioridad JVM (-D), variable de entorno y archivo config.properties.'), p('Arquitectura general', 'H2x'), table([['Capa','Responsabilidad'],['Feature','Describe comportamiento en Gherkin.'],['Step Definitions','Traduce intención a llamadas del framework.'],['Page Objects','Encapsula locators, esperas e interacciones.'],['WebDriver','Controla Chrome o Edge.'],['Hooks / reports','Gestiona ciclo de vida, screenshots y resultados.']], [4.1*cm, 12.2*cm]), Spacer(1,10), p('Flujo de ejecución', 'H2x'), p('gradlew test -> Gradle compila -> JUnit Platform descubre el Runner -> Cucumber carga Features -> Hook Before crea WebDriver -> Steps llaman Pages -> Hook After captura evidencia y cierra -> Reporte HTML.'), p('Regla de diseño: Steps no contienen selectores; Pages no contienen aserciones de escenario; Hooks no incluyen lógica de negocio.'), PageBreak()]
story += [heading('3. Stack, requisitos y VS Code'), table([['Tecnología','Versión','Uso'],['Java','21 (pred.) / 17','Lenguaje y toolchain.'],['Gradle Wrapper','8.14.5','Build y dependencias reproducibles.'],['Selenium Java','4.48.0','WebDriver.'],['Cucumber Java/Engine','7.34.7','BDD y Gherkin.'],['JUnit BOM','5.13.4','JUnit Platform y Suite.']], [4.5*cm, 3*cm, 8.8*cm]), Spacer(1,10), p('Prerrequisitos', 'H2x'), p('Instale JDK 21 (recomendado) o JDK 17 (compatible), y Chrome o Edge. Use siempre el Gradle Wrapper incluido; en Windows, .\\gradlew.bat. No requiere Gradle global. Valide con:'), p('java -version<br/>.\\gradlew.bat --version<br/>git --version', 'CodeX'), p('Apertura en Visual Studio Code', 'H2x'), p('Abra PowerShell y ejecute:'), p('cd C:\\ruta\\automation-template-selenium-java-cucumber<br/>code .', 'CodeX'), p('Instale Extension Pack for Java, Gradle for Java, Cucumber (Gherkin) Full Support y GitLens. Espere que VS Code importe Gradle. Las Features están en src/test/resources/features; Pages en src/main/java; Steps, Hooks y Runner en src/test/java.'), p('Selección de versión de Java', 'H2x'), p('Java 21 es el predeterminado de la configuración actual. Java 17 es la única compatibilidad alternativa mediante la propiedad Gradle javaVersion. Java 18, 19, 20, 22 y cualquier otro valor distinto de 17 o 21 se rechazan explícitamente.'), p('.\\gradlew.bat clean test<br/>.\\gradlew.bat clean test -PjavaVersion=17<br/>.\\gradlew.bat clean test -PjavaVersion=21<br/>.\\gradlew.bat clean test -PjavaVersion=18  # rechazado', 'CodeX'), p('Gradle debe ejecutarse con JDK 17 o superior y la toolchain seleccionada debe estar instalada o disponible para Gradle.'), PageBreak()]
story += [heading('Sección 3.1 — Configurar Java 17 paso a paso'), p('Use Java 17 solo cuando lo requiera su proyecto. Java 21 continúa siendo el predeterminado de la configuración actual.'), p('1. Instale un JDK 17 aprobado por su equipo. En estos ejemplos, la carpeta se representa como C:\\ruta\\jdk-17.'), p('2. Abra PowerShell en la raíz del proyecto y configure la sesión actual. Esto no modifica permanentemente Windows:'), p("$env:JAVA_HOME = 'C:\\ruta\\jdk-17'<br/>$env:Path = \"$env:JAVA_HOME\\bin;$env:Path\"<br/>java -version", 'CodeX'), p('3. Confirme que java -version indica Java 17. En VS Code, use Ctrl+Shift+P, ejecute Java: Configure Java Runtime, seleccione JDK 17 y espere la importación Gradle.'), p('4. Ejecute las pruebas:'), p('.\\gradlew.bat clean test -PjavaVersion=17', 'CodeX'), p('5. Confirme BUILD SUCCESSFUL y abra build/reports/cucumber/cucumber.html. Para volver a Java 21, abra una consola nueva o cambie JAVA_HOME a C:\\ruta\\jdk-21 y ejecute -PjavaVersion=21.'), p('No guarde rutas de JDK ni JAVA_HOME dentro del repositorio. El workflow incluido usa Java 21. Si adopta Java 17 en otro proyecto, adapte y valide su CI antes de usarlo.'), PageBreak()]

story += [heading('4. Configuración y comandos'), p('config.properties contiene los valores por defecto. Los valores pueden reemplazarse con -D o con variables BASE_URL, BROWSER, HEADLESS, TIMEOUT_SECONDS y SCREENSHOT_ON_FAILURE. javaVersion usa -P, no -D.'), p('browser=CHROME<br/>headless=false<br/>baseUrl=https://example.com/<br/>timeoutSeconds=15<br/>screenshotOnFailure=true', 'CodeX'), table([['Objetivo','Comando'],['Limpiar','.\\gradlew.bat clean'],['Limpiar y ejecutar','.\\gradlew.bat clean test'],['Headless','.\\gradlew.bat clean test -Dheadless=true'],['Chrome','.\\gradlew.bat clean test -Dbrowser=CHROME'],['Edge','.\\gradlew.bat clean test -Dbrowser=EDGE'],['URL','.\\gradlew.bat clean test -DbaseUrl=https://su-aplicacion'],['Tags','.\\gradlew.bat clean test -Dcucumber.filter.tags=@example'],['Tags headless','.\\gradlew.bat clean test -Dheadless=true -Dcucumber.filter.tags=@example'],['Alias Cucumber','.\\gradlew.bat cucumber']], [5.2*cm, 11.1*cm]), Spacer(1,10), p('El smoke test incluido usa la fixture HTML local versionada y no depende de un sitio externo. baseUrl sigue disponible para los Page Objects de aplicaciones reales, pero no modifica este escenario de ejemplo. Los reports se generan en build/reports/cucumber/cucumber.html, build/reports/tests/test y build/test-results/test; el log se guarda en build/logs/automation.log y las capturas de fallos en build/evidence/screenshots sólo si falla un escenario, screenshotOnFailure está activo y WebDriver permite capturar.'), PageBreak()]
story += [heading('5&#46; Crear la primera automatización'), p('1. Cree src/test/resources/features/login.feature:'), p('# language: en<br/>Feature: Login<br/>&nbsp;&nbsp;Scenario: Successful login<br/>&nbsp;&nbsp;&nbsp;&nbsp;Given the user opens the login page<br/>&nbsp;&nbsp;&nbsp;&nbsp;When the user signs in with "username" and "password"<br/>&nbsp;&nbsp;&nbsp;&nbsp;Then the dashboard is displayed', 'CodeX'), p('2. Cree LoginPage.java en pages. Mantenga locators privados y métodos de intención, por ejemplo open(), login() e isDashboardVisible().'), p('3. Cree LoginSteps.java en steps. Obtenga el driver mediante DriverManager, delegue a LoginPage y use aserciones JUnit.'), p('4. Configure la URL con -DbaseUrl=... y ejecute .\\gradlew.bat test -Dheadless=true.'), p('5. Revise el reporte HTML. Use esperas explícitas WebDriverWait; nunca Thread.sleep.'), Spacer(1,10), heading('6. Reutilización paso a paso'), p('1. Copie o clone el template; conserve la base original sin cambios.'), p('2. Actualice rootProject.name en settings.gradle y group en build.gradle.'), p('3. Configure baseUrl con -DbaseUrl=https://su-aplicacion, sin secretos en Git.'), p('4. Abra la URL manualmente y ejecute una prueba smoke en headless.'), p('5. Cuando el smoke funcione, sustituya el ejemplo por sus Features, Pages y Steps.'), p('6. Añada tags como @smoke y @regression para seleccionar subconjuntos.'), p('7. Inicialice Git, revise .gitignore, cree una rama y abra Pull Request.'), p('8. Revise el workflow incluido en .github/workflows/ci.yml: ya ejecuta pruebas headless y publica las evidencias disponibles.'), p('Criterio de salida: el equipo puede configurar URL, ejecutar una prueba y consultar el reporte sin editar componentes compartidos.'), PageBreak()]
story += [Spacer(1, .4*cm), heading('7. Contrato CI/CD, buenas prácticas y soporte'), p('Workflow de GitHub Actions', 'H2x'), p('El workflow .github/workflows/ci.yml ejecuta ./gradlew clean test -Dheadless=true con Java 21 de Temurin y el Gradle Wrapper en pull requests y pushes hacia main. En Windows, use .\\gradlew.bat clean test -Dheadless=true para la validación local. Exit code 0 es éxito; cualquier otro código debe fallar el job. El contrato permite BROWSER, BASE_URL, HEADLESS y filtros cucumber.filter.tags; recolecte build/reports/cucumber/cucumber.html, build/reports/tests/test, build/test-results/test, build/logs/automation.log y, sólo ante fallo, build/evidence/screenshots.'), p('Flujo: checkout, Java 21 Temurin, Gradle Setup/Cache, Gradle Wrapper, pruebas headless, reportes y test-evidence. gradle/actions/setup-gradle@v6 usa caché básica para reutilizar dependencias e información de Gradle; puede reducir trabajo repetitivo en ejecuciones posteriores. Si no hay caché (cache miss), Gradle descarga lo necesario y las pruebas continúan. El Wrapper sigue siendo el mecanismo oficial. La caché no cambia Selenium, Cucumber, Page Object Model, features, steps ni el smoke test local.'), p('El workflow usa ubuntu-latest y permisos mínimos de lectura. Intenta publicar las rutas anteriores como test-evidence durante 14 días incluso si Gradle falla. Una ruta vacía, como screenshots en una ejecución sin fallos, se ignora. Descargue el artifact en Artifacts dentro del resumen de GitHub Actions. La evidencia no cambia el estado PASS/FAIL del job. Docker, Grid y secretos de CI/CD quedan fuera de este bloque.'), p('Troubleshooting de Gradle', 'H2x'), p('.\\gradlew.bat --stop detiene Gradle Daemons ante problemas transitorios. Para diagnóstico de dependencias use .\\gradlew.bat clean test --offline o .\\gradlew.bat clean test -PjavaVersion=21 --offline; sólo usa caché y puede fallar si faltan dependencias. Si aparece PKIX path building failed o unable to find valid certification path, revise certificado Java, proxy, inspección SSL, red y daemon; ejecute java -version, .\\gradlew.bat --version, .\\gradlew.bat --stop y .\\gradlew.bat clean test. No deshabilite SSL ni ignore certificados.'), p('Regeneración del manual', 'H2x'), p('scripts/create_manual.py requiere Python 3 y reportlab. Ejecute python scripts/create_manual.py desde la raíz. Genera docs/Manual_Template_Automatizacion_Selenium_Java_Cucumber.pdf y conserva una copia externa. work/ es temporal, está ignorada por Git, no es parte del framework y puede eliminarse.'), p('Buenas prácticas', 'H2x'), p('Un Page Object por pantalla/componente; nombres descriptivos; configuración externa; locators estables; datos aislados; screenshots y logs como evidencia; commits pequeños; ramas, Pull Requests y revisión de código; actualización deliberada de dependencias.'), p('Troubleshooting', 'H2x'), table([['Síntoma','Solución inicial'],['Java no reconocido','Instale/configure JDK 21 o 17 y valide java -version.'],['Wrapper no ejecuta','Ejecute desde la raíz y preserve gradle/wrapper.'],['Browser no inicia','Actualice Chrome/Edge y revise Selenium Manager.'],['Feature/Step no encontrado','Valide ruta .feature, tags, texto y paquete glue.'],['CI falla y local no','Compare variables, navegador, URL y artefactos.']], [5*cm, 11.3*cm]), PageBreak()]

story += [heading('8. CI/CD con GitHub Actions'), p('CI (integración continua) valida automáticamente cambios antes de integrarlos. Detecta temprano errores de compilación y pruebas y ofrece al equipo un resultado compartido. CD significa entrega continua (preparar una versión para publicar) o despliegue continuo (publicarla automáticamente). Este proyecto utiliza principalmente CI; no despliega aplicaciones.'), p('Qué ejecuta GitHub Actions', 'H2x'), p('GitHub Actions lee .github/workflows/ci.yml cuando se abre o actualiza un Pull Request hacia main y cuando hay un push a main. Un Pull Request o PR es una propuesta de unir una rama de trabajo con otra. El workflow obtiene el código (checkout), prepara Java 21 Temurin y caché Gradle en un runner Linux ubuntu-latest, y ejecuta el Gradle Wrapper con Selenium y Cucumber en modo headless, sin ventana visible.'), p('Flujo para principiantes', 'H2x'), p('Developer -&gt; feature branch -&gt; commit -&gt; push -&gt; Pull Request hacia main -&gt; GitHub Actions -&gt; quality-gate -&gt; Gradle -&gt; Selenium + Cucumber -&gt; PASS/FAIL -&gt; evidencias -&gt; revisión -&gt; merge a main.'), p('El workflow se ejecuta automáticamente. No hay botón de ejecución manual configurado. El merge debe esperar la revisión y un check exitoso; el ruleset activo de main exige un Pull Request, la rama actualizada y quality-gate aprobado; un fallo bloquea el merge.'), p('9. Cómo ejecutar y revisar el CI/CD en GitHub Actions', 'H1x'), p('Necesita Git, acceso al repositorio en GitHub y permiso para enviar ramas. Ejecute desde la raíz del proyecto.'), p('1. Cree una rama separada de main: git switch -c feature/mi-cambio. Si ya existe: git switch feature/mi-cambio. Main es la línea compartida; una feature branch aísla su trabajo.'), p('2. Modifique el proyecto, por ejemplo un Page Object y sus pruebas.'), p('3. Revise git status y git diff. Compruebe que no haya credenciales ni archivos generados.'), p('4. Ejecute las pruebas locales:'), p('Windows PowerShell: .\\gradlew.bat clean test "-Dheadless=true"<br/>Linux/macOS: ./gradlew clean test -Dheadless=true', 'CodeX'), p('Espere BUILD SUCCESSFUL. Si ve BUILD FAILED, corrija el error.'), PageBreak()]
story += [heading('Continuación: Pull Request y revisión de resultados'), p('5. Guarde el cambio en Git: git add ruta/del/archivo y git commit -m "Describe mi cambio". Un commit es una instantánea identificable.'), p('6. Envíe la rama: git push -u origin feature/mi-cambio la primera vez; luego git push. Push copia los commits a GitHub.'), p('7. En el repositorio de GitHub abra Pull requests -&gt; New pull request. Seleccione main como base (destino) y feature/mi-cambio como compare (origen). Revise el contenido, agregue título y descripción y pulse Create pull request. No haga merge todavía.'), p('8. GitHub detecta el PR y ejecuta .github/workflows/ci.yml automáticamente. Cada nuevo commit seguido de push a la misma rama actualiza el PR y inicia otra ejecución.'), p('Desde el Pull Request', 'H2x'), p('Abra Repositorio -&gt; Pull requests -&gt; su PR -&gt; Checks; según la interfaz, los checks también aparecen en Conversation. Busque quality-gate y pulse Details. Allí verá checkout, Java 21, caché Gradle, pruebas, carga de evidencias y resultado final. Expanda un step para ver sus logs.'), p('Desde Actions', 'H2x'), p('Abra Repositorio -&gt; Actions -&gt; workflow CI -&gt; ejecución del PR. Identifique rama, PR, commit, fecha, estado y duración. Abra la ejecución y el job quality-gate para inspeccionar cada step.'), table([['Estado visible', 'Qué significa'], ['Success (verde)', 'Las verificaciones terminaron correctamente.'], ['Failure (rojo)', 'Una verificación falló.'], ['In progress (amarillo/progreso)', 'La ejecución todavía no termina.'], ['Cancelled', 'La ejecución se canceló.'], ['Skipped', 'Un step no se ejecutó por una condición.']], [6.2*cm, 10.1*cm]), p('Lea el texto del estado además del color: así puede interpretar el resultado aun sin distinguir colores.'), PageBreak()]
story += [heading('10. ¿Qué es un Quality Gate?'), p('Es una puerta de control: las verificaciones automáticas deben terminar bien antes de considerar listo un cambio. El job/check estable se llama quality-gate. Gradle devuelve exit code 0 cuando compilación y pruebas pasan; un código distinto de cero indica fallo. GitHub muestra PASS/Success para continuar a revisión o FAIL/Failure para corregir. La carga posterior de artifacts no cambia FAIL a PASS.'), p('¿Qué hacer si el Quality Gate falla?', 'H2x'), p('1. Abra el PR -&gt; Checks -&gt; quality-gate -&gt; Details.'), p('2. Localice el step Failure, expándalo y lea el error y el resumen final.'), p('3. Descargue test-evidence si existe; revise reportes, XML, logs y screenshots. Si Gradle terminó antes de generar archivos, algunos faltarán.'), p('4. Corrija el problema en su rama y repita la prueba local:'), p('.\\gradlew.bat clean test "-Dheadless=true"', 'CodeX'), p('En Linux/macOS use ./gradlew clean test -Dheadless=true.'), p('5. Revise git diff, haga otro git add y git commit, y ejecute git push. El PR se actualiza y Actions ejecuta de nuevo quality-gate. Espere el nuevo resultado.'), p('Cómo descargar las evidencias de GitHub Actions', 'H2x'), p('Un artifact es un archivo descargable creado por una ejecución y separado del código. Abra Repository -&gt; Actions -&gt; CI -&gt; ejecución del PR -&gt; Artifacts -&gt; test-evidence. Descargue y extraiga el ZIP. Se conserva 14 días. Se intenta publicar tanto en PASS como en FAIL, pero sólo aparece cuando existen archivos. Si falta, revise el step Upload test evidence y si Gradle creó resultados. Las capturas suelen faltar cuando no fallan escenarios.'), table([['Ruta local / artifact', 'Qué contiene'], ['build/reports/cucumber/cucumber.html', 'Escenarios y pasos Cucumber.'], ['build/reports/tests/test/', 'Reporte HTML Gradle/JUnit.'], ['build/test-results/test/', 'Resultados XML estructurados.'], ['build/logs/automation.log', 'Log cronológico.'], ['build/evidence/screenshots/', 'Capturas de fallos cuando correspondan.']], [8*cm, 8.3*cm]), PageBreak()]
story += [heading('11. Protección de la rama main'), p('Branch Protection es una regla de GitHub que limita cómo se integra código en main, la línea compartida. El flujo recomendado es feature branch -&gt; Pull Request -&gt; quality-gate -&gt; code review -&gt; merge. Un status check es el resultado visible del job; si es Required Status Check, un fallo o estado pendiente bloquea el merge.'), p('El ruleset activo de main requiere Pull Request, quality-gate aprobado y rama actualizada antes del merge. Bloquea force push y restringe la eliminación de main. Se consulta en Repository -&gt; Settings -&gt; Rules -&gt; Rulesets. El workflow ejecuta el check; el ruleset aplica la protección.'), p('Ejemplo completo', 'H2x'), p('Ana crea feature/ajuste-page, modifica un Page Object, ejecuta pruebas locales, hace commit y push y abre un PR hacia main. Actions inicia quality-gate. Si aparece Success, otra persona revisa el código y se podrá hacer merge cuando se cumplan las reglas. Si falla una prueba, Ana abre Details, descarga test-evidence, corrige, prueba localmente, hace un nuevo commit y push. El PR y el check se actualizan automáticamente.'), p('Validación real del Quality Gate', 'H2x'), p('En GitHub se comprobó la secuencia PASS inicial -&gt; FAIL controlado -&gt; bloqueo del merge por quality-gate requerido -&gt; test-evidence disponible -&gt; restauración de la aserción -&gt; PASS final -&gt; merge -&gt; PASS post-merge en main. Los artifacts se publicaron en ejecuciones PASS y FAIL.'), p('Estado del Hito 3 / v1.1.0', 'H2x'), p('Bloque 1: CI base - Completed / Validated. Bloque 2: evidencias - Completed / Validated. Bloque 3: caché Gradle - Completed / Validated. Bloque 4: Quality Gate, protección de main y documentación CI/CD - Completed / Validated. Hito 3: Completed / Validated. v1.1.0: Stable / Validated / Published. Fecha de publicación: 1 de octubre de 2026.'), p('Auditoría de versionado y release', 'H2x'), p('Antes del cierre formal de cada Hito, defina la fecha oficial de publicación y compruebe que coincida en portada, historial, README bilingües, guía, changelog, versioning, release process y PDF. La portada, el historial y los resúmenes finales muestran versión, Stable / Validated, Hito Completed / Validated y fecha oficial; no deje la fecha vacía, TBD o Pending. La publicación es un evento posterior: tras el tag y GitHub Release, el historial podrá incorporar Published.'), PageBreak()]

story += [
    heading('12. Logging y observabilidad básica'),
    p('Hito 4 - Reporting + Logging / Observability, en desarrollo. v1.2.0 sigue en desarrollo y no tiene fecha de publicación. Este manual incorpora sólo el Bloque 1 - Logging base / Observability foundation.'),
    p('El logging ayuda a reconstruir el inicio, la configuración efectiva, el resultado y el cierre de un escenario cuando una prueba falla o se ejecuta en CI/CD. El código usa SLF4J 2.0.20 como API común para Hooks y driver, evitando configurar salidas en cada clase. Logback 1.6.5 es el proveedor de pruebas que centraliza niveles, formato y destinos en src/test/resources/logback-test.xml.'),
    p('Diagrama A - Arquitectura de logging', 'H2x'),
    LoggingDiagram('architecture'),
    p('Los eventos del framework pasan por SLF4J y Logback. Cada evento se emite a consola y a build/logs/automation.log; no se duplican llamadas de logging en Steps o Page Objects.'),
    PageBreak(),
    heading('12. Flujo de observabilidad'),
    p('Diagrama B - Eventos en orden de ejecución', 'H2x'),
    LoggingDiagram('flow'),
    p('Los Hooks registran inicio, nombre, navegador y headless efectivos antes de crear el driver. DriverFactory registra la inicialización; al finalizar, el Hook registra el estado Cucumber y DriverManager cierra el WebDriver. La consola y el archivo reciben los eventos a medida que ocurren.'),
    p('Niveles de logging', 'H2x'),
    table([['Nivel', 'Uso'], ['DEBUG', 'Detalle técnico de creación del driver; oculto por defecto.'], ['INFO', 'Eventos normales: escenario, configuración segura y WebDriver.'], ['WARN', 'Condición recuperable, como ausencia de soporte para capturas.'], ['ERROR', 'Fallo al cerrar WebDriver o manejar evidencia existente.']], [3*cm, 13.3*cm]),
    PageBreak(),
    heading('12. Ejecución, seguridad y alcance'),
    p('Ejecute .\\gradlew.bat clean test -Dheadless=true en Windows, o ./gradlew clean test -Dheadless=true en GitHub Actions. Gradle muestra los logs de test en consola. Logback guarda el archivo bajo build/, ignorado por Git. gradlew clean elimina el log anterior y la siguiente ejecución crea uno nuevo. El workflow existente ya incluye build/logs/ en el artifact test-evidence; no se modificó el workflow.'),
    p('Extracto abreviado de una ejecución headless real', 'H2x'),
    p('2026-10-01 17:36:35.726 INFO [Test worker] Hooks - Starting scenario: Validar el encabezado de la página de ejemplo<br/>2026-10-01 17:36:35.734 INFO [Test worker] Hooks - Scenario configuration: browser=CHROME, headless=true<br/>2026-10-01 17:36:37.110 INFO [Test worker] Hooks - Finished scenario: Validar el encabezado de la página de ejemplo, status=PASSED<br/>2026-10-01 17:36:37.208 INFO [Test worker] DriverManager - WebDriver closed.', 'CodeX'),
    p('No registre secretos, tokens, contraseñas, cookies, headers confidenciales ni propiedades indiscriminadamente. baseUrl no se registra porque una URL arbitraria puede incluir datos sensibles. Las rutas de error existentes registran excepciones completas; las de herramientas externas podrían contener datos de la aplicación. Revise las trazas antes de compartir logs o artifacts.'),
    p('Si falta automation.log, confirme que test inició el proceso de pruebas y consulte build/logs/. Si falta DEBUG, revise el nivel INFO predeterminado en logback-test.xml. Si hay avisos de proveedores SLF4J, inspeccione el classpath con .\\gradlew.bat dependencies --configuration testRuntimeClasspath. Si falla la descarga por PKIX, revise certificados y proxy del JDK sin desactivar TLS.'),
    p('Límites del Bloque 1', 'H2x'),
    p('El reporte HTML Cucumber, las capturas configurables por fallo y la carga actual de test-evidence ya existían y se conservaron. Este bloque no añade reporting avanzado, nuevas capturas automáticas integradas al reporting, artifacts avanzados ni publicación de evidencias de reporting en CI/CD. Bloques 2 y 3 y la release v1.2.0 siguen pendientes.'),
    PageBreak(),
]

glossary_rows = [
    ('Automation Testing', 'Ejecución de pruebas mediante software para validar una aplicación.'),
    ('Selenium', 'Biblioteca que automatiza navegadores web.'),
    ('WebDriver', 'Interfaz que controla Chrome o Edge desde el código.'),
    ('Cucumber', 'Herramienta BDD que ejecuta escenarios escritos en Gherkin.'),
    ('BDD', 'Enfoque que describe el comportamiento esperado antes de implementarlo.'),
    ('Gherkin', 'Lenguaje legible para escribir Features, Scenarios y Steps.'),
    ('Feature', 'Archivo o capacidad de negocio descrita en Gherkin.'),
    ('Scenario', 'Caso concreto que valida un comportamiento esperado.'),
    ('Step Definition', 'Código Java que implementa una frase de Gherkin.'),
    ('Page Object Model', 'Patrón que encapsula la UI y sus interacciones en clases Page.'),
    ('Hooks', 'Código que prepara y limpia el estado antes o después de escenarios.'),
    ('Runner de Cucumber', 'Clase que configura el descubrimiento y la ejecución de Cucumber.'),
    ('Gradle', 'Herramienta de compilación, dependencias y ejecución de pruebas.'),
    ('Gradle Wrapper', 'Scripts versionados que ejecutan la versión requerida de Gradle.'),
    ('JUnit Platform', 'Plataforma que descubre y coordina la ejecución de pruebas.'),
    ('Headless', 'Ejecución del navegador sin mostrar una ventana gráfica.'),
    ('CI/CD', 'Integración y entrega continua mediante una pipeline automatizada.'),
    ('Pipeline', 'Secuencia automatizada de compilación, pruebas y publicación.'),
    ('Git', 'Sistema de control de versiones distribuido.'),
    ('GitHub Enterprise', 'Plataforma corporativa para repositorios, revisiones y pipelines.'),
    ('Locator', 'Regla que permite identificar un elemento en la interfaz.'),
    ('XPath', 'Sintaxis para ubicar elementos a partir de la estructura del DOM.'),
    ('CSS Selector', 'Sintaxis para ubicar elementos con atributos o clases CSS.'),
    ('Assertion', 'Verificación que confirma el resultado esperado de una prueba.'),
    ('Test Data', 'Datos controlados utilizados durante la ejecución de pruebas.'),
    ('Environment Variable', 'Valor externo al código que configura una ejecución.'),
    ('Explicit Wait', 'Espera controlada hasta que una condición de WebDriver se cumple.'),
    ('Screenshot', 'Captura visual utilizada como evidencia, especialmente ante fallos.'),
    ('CI', 'Integración continua: valida cambios automáticamente antes de integrarlos.'),
    ('CD', 'Entrega o despliegue continuo; aquí no hay despliegue automático.'),
    ('GitHub Actions', 'Servicio de GitHub que ejecuta workflows.'),
    ('Workflow', 'Archivo de instrucciones automáticas, como ci.yml.'),
    ('Job', 'Grupo de pasos ejecutado en un runner.'),
    ('Step', 'Instrucción individual de un job.'),
    ('Runner de GitHub Actions', 'Equipo temporal que ejecuta un job.'),
    ('ubuntu-latest', 'Etiqueta de un runner Linux Ubuntu en GitHub Actions.'),
    ('Pull Request', 'Propuesta de integrar una rama después de revisión.'),
    ('Branch', 'Línea de trabajo separada dentro de Git.'),
    ('main', 'Rama principal compartida del repositorio.'),
    ('Feature Branch', 'Rama dedicada a un cambio concreto.'),
    ('Quality Gate', 'Verificación que debe pasar antes de considerar listo un cambio.'),
    ('Status Check', 'Resultado visible de una verificación de GitHub.'),
    ('Required Status Check', 'Check que debe pasar para permitir el merge.'),
    ('Branch Protection', 'Reglas que protegen una rama ante integraciones indebidas.'),
    ('Artifact', 'Archivo descargable producido por una ejecución.'),
    ('Log', 'Registro cronológico de mensajes de ejecución.'),
    ('Report', 'Resumen legible de resultados de pruebas.'),
    ('Exit Code', 'Número de salida: 0 éxito; otro valor, fallo.'),
    ('PASS', 'La verificación terminó correctamente.'),
    ('FAIL', 'La verificación terminó con un error.'),
    ('Commit', 'Instantánea identificable de cambios en Git.'),
    ('Push', 'Envío de commits locales al repositorio remoto.'),
    ('Merge', 'Unión de cambios de una rama a otra.'),
    ('Checkout', 'Obtención del código de una revisión para ejecutarlo.')
]
story += [Spacer(1, .4*cm), heading('13. Glosario'), p('Términos clave del template y de la automatización Web UI.'), glossary_table(glossary_rows[:27]), PageBreak(), heading('Glosario (continuación)'), glossary_table(glossary_rows[27:])]

doc=SimpleDocTemplate(str(OUT), pagesize=A4, rightMargin=2*cm, leftMargin=2*cm, topMargin=1.8*cm, bottomMargin=2*cm, title='Manual Template Automatización Selenium Java Cucumber', author='Automation Template')
doc.build(story, onFirstPage=footer, onLaterPages=footer)
copy2(OUT, EXTERNAL_OUT)
print(OUT)
print(EXTERNAL_OUT)
