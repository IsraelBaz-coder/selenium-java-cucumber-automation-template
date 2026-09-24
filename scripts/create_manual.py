from pathlib import Path
from shutil import copy2
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, KeepTogether

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
    data = [[Paragraph('Versión', styles['GlossaryHeader']), Paragraph('Fecha', styles['GlossaryHeader']), Paragraph('Cambios principales', styles['GlossaryHeader'])]]
    data += [[Paragraph(version, styles['GlossaryX']), Paragraph(date, styles['GlossaryX']), Paragraph(changes, styles['GlossaryX'])] for version, date, changes in rows]
    t = Table(data, colWidths=[2.2*cm, 3.4*cm, 10.7*cm], repeatRows=1)
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#152B4E')),('GRID',(0,0),(-1,-1),0.3,colors.HexColor('#CBD5E1')),('VALIGN',(0,0),(-1,-1),'MIDDLE'),('LEFTPADDING',(0,0),(-1,-1),5),('RIGHTPADDING',(0,0),(-1,-1),5),('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4),('BACKGROUND',(0,1),(-1,-1),colors.white)]))
    return t

story=[]
story += [Spacer(1, 5.3*cm), p('Automation Template Selenium Java Cucumber','Cover'), p('Manual de uso profesional', 'CoverSub'), Spacer(1, .4*cm), p('Template reutilizable de automatización Web UI', 'CoverSub'), Spacer(1, 1.7*cm), p('Baseline estable v1.0.0<br/>v1.0.1 en preparación: Hardening + CI/CD Readiness<br/>Java 21 (predeterminado) | Java 17 (compatible)<br/>Selenium 4.48.0 | Cucumber 7.34.7 | JUnit 5.13.4 | Gradle 8.14.5', 'CoverSub'), PageBreak()]
story += [heading('Índice'), p('1. Inicio rápido para primera vez ................................ 3<br/><br/>2. Arquitectura .................................................. 4<br/><br/>3. Stack, requisitos y VS Code ................................... 5<br/><br/>3.1 Configurar Java 17 paso a paso ............................... 6<br/><br/>4. Configuración y comandos ..................................... 7<br/><br/>5. Primera automatización ........................................ 8<br/><br/>6. Reutilización ................................................. 8<br/><br/>7. Contrato CI/CD, buenas prácticas y soporte .................... 9<br/><br/>8. Glosario ..................................................... 10'), Spacer(1,10), heading('Propósito'), p('El manual permite a una persona con conocimientos básicos o intermedios reutilizar el framework sin conocer previamente este repositorio. El ejemplo incluido es neutral y debe sustituirse por la aplicación bajo prueba.'), p('Información del documento', 'H2x'), table([['Campo', 'Valor'], ['Autor / Creador del template', 'Israel Baz'], ['Rol', 'Test Automation / Prompt Engineering / AI Automation'], ['Mantenimiento', 'Israel Baz']], [5.2*cm, 11.1*cm]), Spacer(1,8), p('Estado e historial de release', 'H2x'), version_table([('v1.0.1', 'En preparación', 'Hardening + CI/CD Readiness. Logging, screenshots de fallos, artifacts y contrato de ejecución documentados; no está publicado ni etiquetado.'), ('v1.0.0', '17 de septiembre de 2026', 'First Stable Release. Estado Stable / Validated: baseline reutilizable con Java 21 predeterminado, Java 17 configurable, documentación, ejemplo funcional y manual PDF.')]), PageBreak()]
story += [heading('1. Inicio rápido para primera vez'), p('Siga estos pasos sin modificar ningún archivo. Si un comando termina con BUILD SUCCESSFUL, se ejecutó correctamente. Si termina con BUILD FAILED, conserve el mensaje y consulte Troubleshooting antes de cambiar código.'), p('Paso 1 - Abra PowerShell y navegue a la raíz:', 'H2x'), p('cd C:\\ruta\\automation-template-selenium-java-cucumber', 'CodeX'), p('Paso 2 - Ejecute la prueba de ejemplo sin ventana visible:', 'H2x'), p('.\\gradlew.bat test -Dheadless=true', 'CodeX'), p('Paso 3 - Abra el reporte de ejecución:', 'H2x'), p('Abra build/reports/cucumber/cucumber.html. El escenario exitoso abre example.com y valida el texto Example Domain.'), p('Paso 4 - Ejecute con navegador visible:', 'H2x'), p('Ejecute .\\gradlew.bat test sin el parámetro headless.'), p('Cómo comprobar VS Code', 'H2x'), p('Debe ver src, gradle, build.gradle y settings.gradle. Abra example_domain.feature: debe aparecer coloreado como Gherkin. Abra ExampleDomainPage.java: Java no debe mostrar imports en rojo. Si VS Code solicita un JDK, seleccione Java 21 y espere que termine "Importing Gradle project".'), p('Lista antes de pedir ayuda', 'H2x'), p('Estoy en la raíz del proyecto; java -version muestra Java 21; el navegador está instalado; la URL abre manualmente; la Feature termina en .feature y está bajo src/test/resources/features; cada frase Gherkin coincide con su Step; no guardé credenciales ni tokens en Git.'), PageBreak()]
story += [heading('2. Arquitectura'), p('El template estandariza la automatización Web UI: configuración externa, navegador, ejecución BDD, Page Object Model, evidencia y reportes. Es adecuado para proyectos que operan en Chrome o Edge. La configuración tiene prioridad JVM (-D), variable de entorno y archivo config.properties.'), p('Arquitectura general', 'H2x'), table([['Capa','Responsabilidad'],['Feature','Describe comportamiento en Gherkin.'],['Step Definitions','Traduce intención a llamadas del framework.'],['Page Objects','Encapsula locators, esperas e interacciones.'],['WebDriver','Controla Chrome o Edge.'],['Hooks / reports','Gestiona ciclo de vida, screenshots y resultados.']], [4.1*cm, 12.2*cm]), Spacer(1,10), p('Flujo de ejecución', 'H2x'), p('gradlew test -> Gradle compila -> JUnit Platform descubre el Runner -> Cucumber carga Features -> Hook Before crea WebDriver -> Steps llaman Pages -> Hook After captura evidencia y cierra -> Reporte HTML.'), p('Regla de diseño: Steps no contienen selectores; Pages no contienen aserciones de escenario; Hooks no incluyen lógica de negocio.'), PageBreak()]
story += [heading('3. Stack, requisitos y VS Code'), table([['Tecnología','Versión','Uso'],['Java','21 (pred.) / 17','Lenguaje y toolchain.'],['Gradle Wrapper','8.14.5','Build y dependencias reproducibles.'],['Selenium Java','4.48.0','WebDriver.'],['Cucumber Java/Engine','7.34.7','BDD y Gherkin.'],['JUnit BOM','5.13.4','JUnit Platform y Suite.']], [4.5*cm, 3*cm, 8.8*cm]), Spacer(1,10), p('Prerrequisitos', 'H2x'), p('Instale JDK 21 (recomendado) o JDK 17 (compatible), y Chrome o Edge. Valide con:'), p('java -version<br/>.\\gradlew.bat --version<br/>git --version', 'CodeX'), p('Apertura en Visual Studio Code', 'H2x'), p('Abra PowerShell y ejecute:'), p('cd C:\\ruta\\automation-template-selenium-java-cucumber<br/>code .', 'CodeX'), p('Instale Extension Pack for Java, Gradle for Java, Cucumber (Gherkin) Full Support y GitLens. Espere que VS Code importe Gradle. Las Features están en src/test/resources/features; Pages en src/main/java; Steps, Hooks y Runner en src/test/java.'), p('Selección de versión de Java', 'H2x'), p('Java 21 es el predeterminado de v1.0.1. Java 17 es compatible mediante la propiedad Gradle javaVersion. Java 8 y Java 11 no están soportados; el build los rechaza para evitar compilaciones inconsistentes.'), p('.\\gradlew.bat test<br/>.\\gradlew.bat clean test -PjavaVersion=17<br/>.\\gradlew.bat clean test -PjavaVersion=21', 'CodeX'), p('Gradle debe ejecutarse con JDK 17 o superior y la toolchain seleccionada debe estar instalada o disponible para Gradle.'), PageBreak()]
story += [heading('Sección 3.1 — Configurar Java 17 paso a paso'), p('Use Java 17 solo cuando lo requiera su proyecto. Java 21 continúa siendo el predeterminado de v1.0.1.'), p('1. Instale un JDK 17 aprobado por su equipo. En estos ejemplos, la carpeta se representa como C:\\ruta\\jdk-17.', 'H2x'), p('2. Abra PowerShell en la raíz del proyecto y configure la sesión actual. Esto no modifica permanentemente Windows:', 'H2x'), p("$env:JAVA_HOME = 'C:\\ruta\\jdk-17'<br/>$env:Path = \"$env:JAVA_HOME\\bin;$env:Path\"<br/>java -version", 'CodeX'), p('3. Confirme que java -version indica Java 17. En VS Code, use Ctrl+Shift+P, ejecute Java: Configure Java Runtime, seleccione JDK 17 y espere la importación Gradle.', 'H2x'), p('4. Detenga procesos Gradle anteriores y ejecute las pruebas:', 'H2x'), p('.\\gradlew.bat --stop<br/>.\\gradlew.bat clean test -PjavaVersion=17', 'CodeX'), p('5. Confirme BUILD SUCCESSFUL y abra build/reports/cucumber/cucumber.html. Para volver a Java 21, abra una consola nueva o cambie JAVA_HOME a C:\\ruta\\jdk-21 y ejecute -PjavaVersion=21.', 'H2x'), p('No guarde rutas de JDK ni JAVA_HOME dentro del repositorio. Para CI/CD, configure Java 17 o Java 21 mediante la imagen del agente o variables seguras de la plataforma.'), PageBreak()]

story += [heading('4. Configuración y comandos'), p('config.properties contiene los valores por defecto. Los valores pueden reemplazarse con -D o con variables BASE_URL, BROWSER, HEADLESS, TIMEOUT_SECONDS y SCREENSHOT_ON_FAILURE.'), p('browser=CHROME<br/>headless=false<br/>baseUrl=https://example.com/<br/>timeoutSeconds=15<br/>screenshotOnFailure=true', 'CodeX'), table([['Objetivo','Comando'],['Limpiar','.\\gradlew.bat clean'],['Ejecutar','.\\gradlew.bat test'],['Limpiar y ejecutar','.\\gradlew.bat clean test'],['Headless','.\\gradlew.bat test -Dheadless=true'],['Chrome','.\\gradlew.bat test -Dbrowser=CHROME'],['Edge','.\\gradlew.bat test -Dbrowser=EDGE'],['URL','.\\gradlew.bat test -DbaseUrl=https://example.com'],['Tags','.\\gradlew.bat test -Dcucumber.filter.tags=@example']], [5.2*cm, 11.1*cm]), Spacer(1,10), p('Los reports se generan en build/reports/cucumber/cucumber.html, build/reports/tests/test y build/test-results/test; el log se guarda en build/logs/automation.log y las capturas de fallos en build/evidence/screenshots.'), PageBreak()]
story += [heading('5&#46; Crear la primera automatización'), p('1. Cree src/test/resources/features/login.feature:'), p('# language: en<br/>Feature: Login<br/>&nbsp;&nbsp;Scenario: Successful login<br/>&nbsp;&nbsp;&nbsp;&nbsp;Given the user opens the login page<br/>&nbsp;&nbsp;&nbsp;&nbsp;When the user signs in with "username" and "password"<br/>&nbsp;&nbsp;&nbsp;&nbsp;Then the dashboard is displayed', 'CodeX'), p('2. Cree LoginPage.java en pages. Mantenga locators privados y métodos de intención, por ejemplo open(), login() e isDashboardVisible().'), p('3. Cree LoginSteps.java en steps. Obtenga el driver mediante DriverManager, delegue a LoginPage y use aserciones JUnit.'), p('4. Configure la URL con -DbaseUrl=... y ejecute .\\gradlew.bat test -Dheadless=true.'), p('5. Revise el reporte HTML. Use esperas explícitas WebDriverWait; nunca Thread.sleep.'), Spacer(1,10), heading('6. Reutilización paso a paso'), p('1. Copie o clone el template; conserve la base original sin cambios.'), p('2. Actualice rootProject.name en settings.gradle y group en build.gradle.'), p('3. Configure baseUrl con -DbaseUrl=https://su-aplicacion, sin secretos en Git.'), p('4. Abra la URL manualmente y ejecute una prueba smoke en headless.'), p('5. Cuando el smoke funcione, sustituya el ejemplo por sus Features, Pages y Steps.'), p('6. Añada tags como @smoke y @regression para seleccionar subconjuntos.'), p('7. Inicialice Git, revise .gitignore, cree una rama y abra Pull Request.'), p('8. Conecte CI/CD con ejecución headless y publicación de reportes.'), p('Criterio de salida: el equipo puede configurar URL, ejecutar una prueba y consultar el reporte sin editar componentes compartidos.'), PageBreak()]
story += [Spacer(1, .4*cm), heading('7. Contrato CI/CD, buenas prácticas y soporte'), p('Contrato para integración futura', 'H2x'), p('El entry point estándar es .\\gradlew.bat clean test. Para un agente sin interfaz use .\\gradlew.bat clean test -Dheadless=true. Exit code 0 es éxito; cualquier otro código debe fallar el job. El contrato permite BROWSER, BASE_URL, HEADLESS y filtros cucumber.filter.tags; recolecte build/reports/cucumber/cucumber.html, build/reports/tests/test, build/test-results/test, build/logs/automation.log y, sólo ante fallo, build/evidence/screenshots.'), p('No se incluye workflow, runner, Docker, Grid ni secretos de CI/CD. Esos elementos se definirán en un hito posterior.'), p('Regeneración del manual', 'H2x'), p('scripts/create_manual.py requiere Python 3 y reportlab. Ejecute python scripts/create_manual.py desde la raíz. Genera docs/Manual_Template_Automatizacion_Selenium_Java_Cucumber.pdf y conserva una copia externa. work/ es temporal, está ignorada por Git, no es parte del framework y puede eliminarse.'), p('Buenas prácticas', 'H2x'), p('Un Page Object por pantalla/componente; nombres descriptivos; configuración externa; locators estables; datos aislados; screenshots y logs como evidencia; commits pequeños; ramas, Pull Requests y revisión de código; actualización deliberada de dependencias.'), p('Troubleshooting', 'H2x'), table([['Síntoma','Solución inicial'],['Java no reconocido','Instale/configure JDK 21 o 17 y valide java -version.'],['Wrapper no ejecuta','Ejecute desde la raíz y preserve gradle/wrapper.'],['Browser no inicia','Actualice Chrome/Edge y revise Selenium Manager.'],['Feature/Step no encontrado','Valide ruta .feature, tags, texto y paquete glue.'],['CI falla y local no','Compare variables, navegador, URL y artefactos.']], [5*cm, 11.3*cm]), PageBreak()]

story += [Spacer(1, .4*cm), heading('8. Glosario'), p('Términos clave del template y de la automatización Web UI.'), glossary_table([
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
    ('Runner', 'Clase que configura el descubrimiento y la ejecución de Cucumber.'),
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
    ('Screenshot', 'Captura visual utilizada como evidencia, especialmente ante fallos.')
])]

doc=SimpleDocTemplate(str(OUT), pagesize=A4, rightMargin=2*cm, leftMargin=2*cm, topMargin=1.8*cm, bottomMargin=2*cm, title='Manual Template Automatización Selenium Java Cucumber', author='Automation Template')
doc.build(story, onFirstPage=footer, onLaterPages=footer)
copy2(OUT, EXTERNAL_OUT)
print(OUT)
print(EXTERNAL_OUT)
