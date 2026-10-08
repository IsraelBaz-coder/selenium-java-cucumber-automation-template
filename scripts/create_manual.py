import argparse
from pathlib import Path
from math import atan2, cos, sin, pi
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, KeepTogether, Flowable

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description='Generate the Selenium Java Cucumber user manual.')
parser.add_argument('--output', type=Path, help='Optional PDF path for validation without replacing the repository manual.')
args = parser.parse_args()
OUT = args.output.resolve() if args.output else ROOT / 'docs' / 'Manual_Template_Automatizacion_Selenium_Java_Cucumber.pdf'
EN_OUT = ROOT / 'docs_en' / 'Manual_Selenium_Java_Cucumber_Automation_Template.pdf'

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

def glossary_table(rows, language='es'):
    labels = ('Term', 'Definition') if language == 'en' else ('Término', 'Definición')
    data = [[Paragraph(labels[0], styles['GlossaryHeader']), Paragraph(labels[1], styles['GlossaryHeader'])]]
    data += [[Paragraph(term, styles['GlossaryX']), Paragraph(definition, styles['GlossaryX'])] for term, definition in rows]
    t = Table(data, colWidths=[4.5*cm, 11.8*cm], repeatRows=1)
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#152B4E')),('GRID',(0,0),(-1,-1),0.3,colors.HexColor('#CBD5E1')),('VALIGN',(0,0),(-1,-1),'MIDDLE'),('LEFTPADDING',(0,0),(-1,-1),5),('RIGHTPADDING',(0,0),(-1,-1),5),('TOPPADDING',(0,0),(-1,-1),3),('BOTTOMPADDING',(0,0),(-1,-1),3),('BACKGROUND',(0,1),(-1,-1),colors.white)]))
    return t

def version_table(rows, language='es'):
    labels = ('Version', 'Date / status', 'Main changes') if language == 'en' else ('Versión', 'Fecha / estado', 'Cambios principales')
    data = [[Paragraph(label, styles['GlossaryHeader']) for label in labels]]
    data += [[Paragraph(version, styles['GlossaryX']), Paragraph(date, styles['GlossaryX']), Paragraph(changes, styles['GlossaryX'])] for version, date, changes in rows]
    t = Table(data, colWidths=[2.2*cm, 3.4*cm, 10.7*cm], repeatRows=1)
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#152B4E')),('GRID',(0,0),(-1,-1),0.3,colors.HexColor('#CBD5E1')),('VALIGN',(0,0),(-1,-1),'MIDDLE'),('LEFTPADDING',(0,0),(-1,-1),5),('RIGHTPADDING',(0,0),(-1,-1),5),('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4),('BACKGROUND',(0,1),(-1,-1),colors.white)]))
    return t

class DockerFlowDiagram(Flowable):
    """Original vector overview; illustrative, never presented as a test screenshot."""

    def __init__(self, language='es'):
        super().__init__()
        self.width, self.height = 16.3*cm, 4.5*cm
        self.language = language

    def draw(self):
        c = self.canv
        labels = (['GitHub: código fuente', 'Windows / PowerShell', 'Docker Desktop / WSL2',
                   'Reportes en build/', 'Selenium + Chrome', 'Linux: Gradle + Cucumber']
                  if self.language == 'es' else
                  ['GitHub: source code', 'Windows / PowerShell', 'Docker Desktop / WSL2',
                   'Reports in build/', 'Selenium + Chrome', 'Linux: Gradle + Cucumber'])
        xs = [0, 5.55*cm, 11.1*cm]
        ys = [2.55*cm, 0.25*cm]
        for row, y in enumerate(ys):
            for col, x in enumerate(xs):
                label = labels[row*3+col]
                c.setFillColor(colors.HexColor('#EEF4FA'))
                c.setStrokeColor(colors.HexColor('#40709E'))
                c.roundRect(x, y, 5.2*cm, 1.2*cm, 5, fill=1, stroke=1)
                c.setFont('Helvetica-Bold', 8.1)
                c.setFillColor(colors.HexColor('#152B4E'))
                c.drawCentredString(x+2.6*cm, y+0.52*cm, label)
        c.setStrokeColor(colors.HexColor('#607D98'))
        c.setLineWidth(1.2)
        for a,b in [(5.2*cm,5.55*cm),(10.75*cm,11.1*cm)]:
            c.line(a,3.15*cm,b,3.15*cm)
        c.line(13.7*cm,2.55*cm,13.7*cm,1.45*cm)
        for a,b in [(11.1*cm,10.75*cm),(5.55*cm,5.2*cm)]:
            c.line(a,0.85*cm,b,0.85*cm)
        c.setFont('Helvetica',7.5)
        c.setFillColor(colors.HexColor('#526273'))
        c.drawString(0,0, 'Diagrama ilustrativo; no es evidencia de una ejecución.' if self.language == 'es'
                     else 'Illustrative diagram; not evidence of a test run.')

def docker_step(title, goal, requirements, command, explanation, expected, error, remedy, language):
    labels = (['Objetivo', 'Requisitos', 'Explicación', 'Resultado esperado', 'Cómo reconocer un error', 'Cómo resolverlo']
              if language == 'es' else
              ['Goal', 'Requirements', 'Explanation', 'Expected result', 'Recognize an error', 'Resolution'])
    return [
        p(title, 'H2x'),
        p(f'<b>{labels[0]}:</b> {goal} <b>{labels[1]}:</b> {requirements}'),
        p(escape(command).replace('\n', '<br/>'), 'CodeX'),
        p(f'<b>{labels[2]}:</b> {explanation} <b>{labels[3]}:</b> {expected}'),
        p(f'<b>{labels[4]}:</b> {error} <b>{labels[5]}:</b> {remedy}'),
    ]

def docker_manual_section(language):
    es = language == 'es'
    items = [
        heading('4.1. Uso con Docker' if es else '4.1. Using Docker'),
        p(('Docker ejecuta el framework en un contenedor Linux reproducible, separado del Java y navegador de Windows. La imagen en desarrollo para v1.3.0 contiene Temurin 21, Chrome y ChromeDriver 155.0.8059.39, Gradle Wrapper 8.14.5, Selenium, Cucumber, JUnit y POM. La última release publicada sigue siendo v1.2.0.'
           if es else
           'Docker runs the framework in a reproducible Linux container, separate from Windows Java and browser installations. The development v1.3.0 image contains Temurin 21, Chrome and ChromeDriver 155.0.8059.39, Gradle Wrapper 8.14.5, Selenium, Cucumber, JUnit, and POM. v1.2.0 remains the latest published release.')),
        p('Descargar el proyecto desde GitHub' if es else 'Download the project from GitHub', 'H2x'),
        p(('Instale Git para Windows desde git-scm.com/download/win y abra PowerShell. Clone el código fuente, entre al directorio y consulte las ramas remotas:'
           if es else
           'Install Git for Windows from git-scm.com/download/win and open PowerShell. Clone the source, enter the directory, and list remote branches:')),
        p(escape('git --version\ngit clone https://github.com/IsraelBaz-coder/selenium-java-cucumber-automation-template.git\nSet-Location .\\selenium-java-cucumber-automation-template\ngit fetch origin\ngit branch -r').replace('\n', '<br/>'), 'CodeX'),
        p(('Seleccione una referencia publicada con Docker. Sólo cuando aparezca origin/feature/hito-5-docker-base, ejecute git switch --track origin/feature/hito-5-docker-base. Compruebe los tres archivos:'
           if es else
           'Select a published Docker-enabled ref. Only when origin/feature/hito-5-docker-base appears, run git switch --track origin/feature/hito-5-docker-base. Check all three files:')),
        p(escape('Test-Path .\\Dockerfile\nTest-Path .\\gradlew\nTest-Path .\\build.gradle\ngit check-attr eol -- gradlew').replace('\n', '<br/>'), 'CodeX'),
        p(('Los tres Test-Path deben ser True y Git debe mostrar gradlew: eol: lf. La rama Docker está publicada, pero el commit 3ba7245 puede convertir gradlew a CRLF en Windows. Solicite una revisión publicada con la regla LF antes de construir; main no incluye Docker.'
           if es else
           'All three Test-Path results must be True and Git must show gradlew: eol: lf. The Docker branch is published, but commit 3ba7245 may convert gradlew to CRLF on Windows. Request a published revision with the LF rule before building; main does not include Docker.')),
        p(('git clone descarga fuentes; docker build crea la imagen localmente; docker pull requeriría una imagen publicada en un registro. Aún no hay una imagen preconstruida publicada y verificada.'
           if es else
           'git clone downloads source; docker build creates the image locally; docker pull would require an image published in a registry. No published and verified prebuilt image is available yet.')),
        DockerFlowDiagram(language),
        Spacer(1, 8),
        p(('Descripción del diagrama: GitHub entrega el código a Windows; PowerShell solicita a Docker Desktop/WSL2 iniciar el contenedor; Gradle y Cucumber ejecutan Selenium con Chrome; los resultados se escriben bajo build/.'
           if es else
           'Diagram description: GitHub supplies source to Windows; PowerShell asks Docker Desktop/WSL2 to start the container; Gradle and Cucumber run Selenium with Chrome; results are written under build/.')),
    ]
    if es:
        items += docker_step('1. Windows, WSL2 y Docker Engine',
            'Preparar el motor Linux.', 'Docker Desktop instalado, WSL2 y virtualización disponibles.',
            'wsl --status\ndocker version\ndocker info',
            'Abra Docker Desktop desde Inicio y espere a que el motor esté activo; Client y Server deben aparecer.',
            'Server muestra Docker Desktop y Linux.', 'No aparece Server o se informa daemon unavailable.',
            'Inicie o reinicie Docker Desktop, compruebe modo Linux; si WSL falla, ejecute wsl --update y reinicie cuando se solicite.', language)
        items.append(PageBreak())
        items += docker_step('2. PowerShell en la carpeta correcta',
            'Usar este Dockerfile como contexto.', 'Repositorio descargado en Windows.',
            'Get-Location\nTest-Path .\\Dockerfile\nTest-Path .\\gradlew\nTest-Path .\\build.gradle\ngit check-attr eol -- gradlew',
            'Trabaje desde la carpeta clonada después de seleccionar una referencia con Docker.',
            'Los tres Test-Path devuelven True y eol indica lf.', 'False o eol unspecified indica otra carpeta o una revisión sin la corrección.',
            'Abra la carpeta correcta y use una revisión que incluya .gitattributes con gradlew text eol=lf.', language)
        items += docker_step('3. Construir la imagen',
            'Crear la imagen de desarrollo.', 'Docker Engine activo, raíz correcta y red para descargas.',
            'docker build --progress=plain -t selenium-java-cucumber-template:1.3.0-dev .',
            '--progress=plain muestra cada paso, -t asigna nombre y etiqueta, el punto usa la carpeta actual.',
            'El build termina sin ERROR. Codex verificó la corrección local con un build sin caché y pruebas Docker exitosas.',
            'ERROR o código distinto de cero.', 'Revise daemon, red, proxy y certificados. Ante TLS/PKIX no desactive TLS.', language)
        items.append(PageBreak())
        items += docker_step('4. Verificar componentes',
            'Inspeccionar versiones dentro de la imagen.', 'Imagen construida.',
            'docker run --rm selenium-java-cucumber-template:1.3.0-dev java -version\ndocker run --rm selenium-java-cucumber-template:1.3.0-dev google-chrome --version\ndocker run --rm selenium-java-cucumber-template:1.3.0-dev chromedriver --version',
            '--rm elimina cada contenedor temporal; el argumento final reemplaza el comando de pruebas.',
            'Java 21; Chrome y ChromeDriver 155.0.8059.39. Codex verificó estas versiones en una imagen existente.',
            'Imagen ausente o versiones de navegador y driver distintas.',
            'Reconstruya desde la raíz y confirme CHROME_VERSION en Dockerfile.', language)
        items += docker_step('5. Ejecutar e interpretar',
            'Ejecutar el smoke test headless.', 'Imagen disponible.',
            'docker run --rm selenium-java-cucumber-template:1.3.0-dev',
            'Sin otro comando, se ejecuta ./gradlew --no-daemon test. Sin montaje, build/ desaparece con el contenedor.',
            'WebDriver initialized successfully, Example Domain PASSED y BUILD SUCCESSFUL.',
            'BUILD FAILED o paso rojo; WARN por sí solo no es fallo.',
            'Lea el primer error real. Las advertencias CDP y selector están registradas en docs/TECHNICAL_DEBT.md.', language)
        items += docker_step('6. Persistir reportes',
            'Guardar build/ en Windows tras --rm.', 'Carpeta compartida y escritura para UID 10001.',
            r'New-Item -ItemType Directory -Force .\build | Out-Null'+'\n'+r'$out = (Resolve-Path .\build).Path'+'\n'+r'$bind = "type=bind,source=$out,target=/home/automation/app/build"'+'\n'+r'docker run --rm --mount $bind selenium-java-cucumber-template:1.3.0-dev',
            'El bind mount enlaza build/ del host con el contenedor. Codex comprobó HTML, JSON, XML y log en Windows.',
            'BUILD SUCCESSFUL y archivos en build/reports/ y build/logs/. Un PNG de fallo no se validó porque el escenario pasó.',
            'Permission denied o reportes ausentes.',
            'Compruebe la carpeta, Docker Desktop y permisos para UID 10001; consulte docs/DOCKER.md.', language)
    else:
        items += docker_step('1. Windows, WSL2, and Docker Engine',
            'Prepare the Linux engine.', 'Installed Docker Desktop, WSL2, and virtualization.',
            'wsl --status\ndocker version\ndocker info',
            'Open Docker Desktop from Start and wait for the running engine; both Client and Server must appear.',
            'Server shows Docker Desktop and Linux.', 'No Server or daemon unavailable.',
            'Start or restart Docker Desktop and confirm Linux mode; for WSL trouble run wsl --update and restart if requested.', language)
        items.append(PageBreak())
        items += docker_step('2. PowerShell in the correct directory',
            'Use this Dockerfile as the build context.', 'Repository downloaded to Windows.',
            'Get-Location\nTest-Path .\\Dockerfile\nTest-Path .\\gradlew\nTest-Path .\\build.gradle\ngit check-attr eol -- gradlew',
            'Work in the cloned directory after selecting a Docker-enabled ref.',
            'All three Test-Path commands return True and eol reports lf.', 'False or eol unspecified means a wrong directory or revision without the fix.',
            'Use the correct folder and a revision with gradlew text eol=lf in .gitattributes.', language)
        items += docker_step('3. Build the image',
            'Create the development image.', 'Running engine, correct root, and download access.',
            'docker build --progress=plain -t selenium-java-cucumber-template:1.3.0-dev .',
            '--progress=plain shows each step, -t names and tags the image, and the dot selects the current folder.',
            'Build ends without ERROR. Codex verified the local correction with an uncached build and successful Docker tests.',
            'ERROR or nonzero exit code.', 'Check daemon, network, proxy, and certificates. Do not disable TLS for TLS/PKIX.', language)
        items.append(PageBreak())
        items += docker_step('4. Verify components',
            'Inspect image versions.', 'Built image.',
            'docker run --rm selenium-java-cucumber-template:1.3.0-dev java -version\ndocker run --rm selenium-java-cucumber-template:1.3.0-dev google-chrome --version\ndocker run --rm selenium-java-cucumber-template:1.3.0-dev chromedriver --version',
            '--rm removes each temporary container; the final argument replaces the test command.',
            'Java 21; Chrome and ChromeDriver 155.0.8059.39. Codex checked these in an existing image.',
            'Missing image or different browser and driver versions.',
            'Rebuild from the root and confirm CHROME_VERSION in Dockerfile.', language)
        items += docker_step('5. Run and interpret',
            'Run the headless smoke test.', 'Available image.',
            'docker run --rm selenium-java-cucumber-template:1.3.0-dev',
            'Without extra arguments, ./gradlew --no-daemon test runs. Without a mount, build/ disappears with the container.',
            'WebDriver initialized successfully, Example Domain PASSED, and BUILD SUCCESSFUL.',
            'BUILD FAILED or a red step; WARN alone does not mean failure.',
            'Read the first real error. CDP and selector warnings are tracked in docs_en/TECHNICAL_DEBT.md.', language)
        items += docker_step('6. Retain reports',
            'Keep build/ on Windows after --rm.', 'Shared folder and UID 10001 write access.',
            r'New-Item -ItemType Directory -Force .\build | Out-Null'+'\n'+r'$out = (Resolve-Path .\build).Path'+'\n'+r'$bind = "type=bind,source=$out,target=/home/automation/app/build"'+'\n'+r'docker run --rm --mount $bind selenium-java-cucumber-template:1.3.0-dev',
            'The bind mount links host and container build/. Codex verified HTML, JSON, XML, and a log on Windows.',
            'BUILD SUCCESSFUL and files in build/reports/ and build/logs/. No failure PNG was validated because the scenario passed.',
            'Permission denied or missing reports.',
            'Check folder, Docker Desktop, and UID 10001 permissions; see docs_en/DOCKER.md.', language)
    items += [
        p('Errores y advertencias' if es else 'Errors and warnings', 'H2x'),
        p(('Si ./gradlew: not found aunque existe, compruebe git check-attr eol -- gradlew: debe ser lf; chmod +x no corrige CRLF. Use una revisión publicada con la regla LF y vuelva a clonar. Daemon detenido: inicie Docker Desktop. WSL2: wsl --status y wsl --update. Descargas: revise --progress=plain. TLS/PKIX: revise certificados y proxy. Permisos: compruebe UID 10001. WARN CDP y selector: TECH-001/002 siguen OPEN.'
           if es else
           'If ./gradlew: not found although it exists, check git check-attr eol -- gradlew: it must report lf; chmod +x cannot fix CRLF. Use a published revision with the LF rule and clone again. Stopped daemon: start Docker Desktop. WSL2: use wsl --status and wsl --update. Downloads: inspect --progress=plain. TLS/PKIX: check certificates and proxy. Permissions: check UID 10001. CDP and selector WARN: TECH-001/002 remain OPEN.')),
        p(('Implementado localmente: regla LF y guías. Validado por Codex: build Docker sin caché, prueba Docker y prueba Windows, BUILD SUCCESSFUL. La corrección aún no está publicada. TECH-001/002 siguen OPEN; Bloque 1 continúa abierto.'
           if es else
           'Implemented locally: LF rule and guides. Validated by Codex: uncached Docker build, Docker test, and Windows test, BUILD SUCCESSFUL. The correction is not yet published. TECH-001/002 remain OPEN; Block 1 remains open.')),
    ]
    items.append(PageBreak())
    return items

class LoggingDiagram(Flowable):
    """Vector diagrams for the Block 1 logging architecture and event flow."""

    def __init__(self, kind, language='es'):
        super().__init__()
        self.kind = kind
        self.language = language
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
            self._box(c, center - 65, 267, 130, ['Cucumber scenario'] if self.language == 'en' else ['Escenario Cucumber'])
            self._box(c, center - 50, 222, 100, ['Hooks'])
            self._box(c, 15, 157, 165, ['Scenario lifecycle', 'start and result'] if self.language == 'en' else ['Ciclo del escenario', 'inicio y resultado'])
            self._box(c, self.width - 180, 157, 165, ['WebDriver lifecycle', 'Factory and Manager'] if self.language == 'en' else ['Ciclo WebDriver', 'Factory y Manager'])
            self._box(c, center - 50, 112, 100, ['SLF4J'])
            self._box(c, center - 50, 67, 100, ['Logback'])
            self._box(c, 50, 7, 105, ['Console'] if self.language == 'en' else ['Consola'])
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
            if self.language == 'en':
                labels = [
                    ['Scenario starts'],
                    ['Name and effective configuration'],
                    ['Browser and headless mode'],
                    ['WebDriver initialization'],
                    ['Test execution'],
                    ['Scenario result'],
                    ['WebDriver shutdown'],
                    ['Console + build/logs/automation.log'],
                ]
            positions = [350 - index * 49 for index in range(len(labels))]
            for y, label in zip(positions, labels):
                self._box(c, center - 117, y, 234, label)
            for previous, following in zip(positions, positions[1:]):
                self._arrow(c, center, previous, center, following + 26)

story=[]
story += [Spacer(1, 5.3*cm), p('Automation Template Selenium Java Cucumber','Cover'), p('Manual de uso', 'CoverSub'), Spacer(1, .4*cm), p('Template reutilizable de automatización Web UI', 'CoverSub'), Spacer(1, 1.7*cm), p('v1.2.0 - Stable / Validated / Published<br/>Fecha de publicación: 8 de octubre de 2026<br/>Última versión publicada: v1.2.0<br/>Java 21 (predeterminado) | Java 17 (compatible)<br/>Selenium 4.48.0<br/>Cucumber 7.34.7<br/>JUnit 5.13.4<br/>Gradle 8.14.5<br/>SLF4J 2.0.20 | Logback 1.6.5', 'CoverSub'), PageBreak()]
story += [
    heading('Índice'),
    p('1. Inicio rápido para primera vez<br/>2. Arquitectura<br/>3. Stack, requisitos y VS Code<br/>3.1 Configurar Java 17 paso a paso<br/>4. Configuración y comandos<br/>4.1 Uso con Docker<br/>5. Primera automatización<br/>6. Reutilización<br/>7. Contrato CI/CD, buenas prácticas y soporte<br/>8. CI/CD con GitHub Actions<br/>9. Cómo ejecutar y revisar el CI/CD<br/>10. Quality Gate, fallos y evidencias<br/>11. Protección de la rama main<br/>12. Logging y observabilidad básica<br/>12.1 Flujo de observabilidad<br/>12.2 Niveles de logging<br/>12.3 Ejecución y seguridad<br/>12.4 Diagnóstico del logging<br/>13. Captura automática de evidencias<br/>14. Generación y consulta de reportes<br/>15. Glosario'),
    Spacer(1, 10),
    heading('Propósito'),
    p('Esta guía permite instalar, configurar, ejecutar y ampliar el template, interpretar resultados y resolver fallos. Explica desde cero el flujo Git, Pull Request y GitHub Actions. Para crear pruebas se necesitan conocimientos básicos de Java. El ejemplo incluido es neutral y usa una página HTML local.'),
    p('Información del documento', 'H2x'),
    table([['Campo', 'Valor'], ['Autor / Creador del template', 'Israel Baz'], ['Rol', 'Test Automation / Prompt Engineering / AI Automation'], ['Mantenimiento', 'Israel Baz']], [5.2*cm, 11.1*cm]),
    Spacer(1, 8),
    p('Estado e historial de versiones', 'H2x'),
    version_table([
        ('v1.2.0', '8 de octubre de 2026', 'Stable / Validated / Published. Logging con SLF4J/Logback, evidencias automáticas, reportes HTML/JSON y mejoras de estabilidad.'),
        ('v1.1.0', '1 de octubre de 2026', 'Stable / Validated / Published. CI con Quality Gate y artifacts de resultados.'),
        ('v1.0.2', '26 de septiembre de 2026', 'Documentation-only Hotfix, Stable / Validated / Published.'),
        ('v1.0.1', '25 de septiembre de 2026', 'Hardening + CI/CD Readiness. Stable / Validated / Published.'),
        ('v1.0.0', '18 de septiembre de 2026', 'Primera versión estable: Java, Selenium, Cucumber, POM y manual PDF.')
    ]),
    PageBreak(),
]

story += [heading('1. Inicio rápido para primera vez'), p('Siga estos pasos sin modificar ningún archivo. Si un comando termina con BUILD SUCCESSFUL, se ejecutó correctamente. Si termina con BUILD FAILED, conserve el mensaje y consulte Troubleshooting antes de cambiar código.'), p('Paso 1 - Abra PowerShell y navegue a la raíz:', 'H2x'), p('cd C:\\ruta\\automation-template-selenium-java-cucumber', 'CodeX'), p('Paso 2 - Ejecute la prueba de ejemplo sin ventana visible:', 'H2x'), p('.\\gradlew.bat test -Dheadless=true', 'CodeX'), p('Paso 3 - Abra el reporte de ejecución:', 'H2x'), p('Abra build/reports/cucumber/cucumber.html. El escenario abre la fixture HTML local src/test/resources/fixtures/example_page.html y valida el encabezado Example Domain. La fixture está versionada y no depende del contenido de un sitio externo; el escenario se reproduce en CI.'), p('Paso 4 - Ejecute con navegador visible:', 'H2x'), p('Ejecute .\\gradlew.bat clean test sin el parámetro headless.'), p('Cómo comprobar VS Code', 'H2x'), p('Debe ver src, gradle, build.gradle y settings.gradle. Abra example_domain.feature: debe aparecer coloreado como Gherkin. Abra ExampleDomainPage.java: Java no debe mostrar imports en rojo. Si VS Code solicita un JDK, seleccione Java 21 y espere que termine "Importing Gradle project".'), p('Lista antes de pedir ayuda', 'H2x'), p('Estoy en la raíz del proyecto; java -version muestra Java 21; el navegador está instalado; la fixture local existe; la Feature termina en .feature y está bajo src/test/resources/features; cada frase Gherkin coincide con su Step; no guardé credenciales ni tokens en Git.'), PageBreak()]
story += [heading('2. Arquitectura'), p('El template estandariza la automatización Web UI: configuración externa, navegador, ejecución BDD, Page Object Model, evidencia y reportes. Es adecuado para proyectos que operan en Chrome o Edge. La configuración tiene prioridad JVM (-D), variable de entorno y archivo config.properties.'), p('Arquitectura general', 'H2x'), table([['Capa','Responsabilidad'],['Feature','Describe comportamiento en Gherkin.'],['Step Definitions','Traduce intención a llamadas del framework.'],['Page Objects','Encapsula locators, esperas e interacciones.'],['WebDriver','Controla Chrome o Edge.'],['Hooks / reports','Gestiona ciclo de vida, screenshots y resultados.']], [4.1*cm, 12.2*cm]), Spacer(1,10), p('Flujo de ejecución', 'H2x'), p('gradlew test -> Gradle compila -> JUnit Platform descubre el Runner -> Cucumber carga Features -> Hook Before crea WebDriver -> Steps llaman Pages -> Hook After captura evidencia y cierra -> Reporte HTML.'), p('Regla de diseño: Steps no contienen selectores; Pages no contienen aserciones de escenario; Hooks no incluyen lógica de negocio.'), p('Estructura principal: src/main/java/com/automation/template/{config,driver,pages}; src/test/java/com/automation/template/{hooks,runners,steps,support}; src/test/resources/{features,fixtures,config.properties}. El workflow está en .github/workflows/ci.yml y el manual se genera con scripts/create_manual.py.'), PageBreak()]
story += [heading('3. Stack, requisitos y VS Code'), table([['Tecnología','Versión','Uso'],['Java','21 (pred.) / 17','Lenguaje y toolchain.'],['Gradle Wrapper','8.14.5','Build y dependencias reproducibles.'],['Selenium Java','4.48.0','WebDriver.'],['Cucumber Java/Engine','7.34.7','BDD y Gherkin.'],['JUnit BOM','5.13.4','JUnit Platform y Suite.'],['SLF4J API','2.0.20','Fachada de logging.'],['Logback Classic','1.6.5','Proveedor de logs durante las pruebas.']], [4.5*cm, 3*cm, 8.8*cm]), Spacer(1,10), p('v1.2.0 identifica el template; 17/21 son versiones de Java seleccionables, y las demás cifras son versiones de dependencias fijadas en build.gradle y gradle-wrapper.properties.'), p('Prerrequisitos', 'H2x'), p('Instale JDK 21 (recomendado) o JDK 17 (compatible), y Chrome o Edge. Use siempre el Gradle Wrapper incluido; en Windows, .\\gradlew.bat. No requiere Gradle global. Valide con:'), p('java -version<br/>.\\gradlew.bat --version<br/>git --version', 'CodeX'), p('Apertura en Visual Studio Code', 'H2x'), p('Abra PowerShell y ejecute:'), p('cd C:\\ruta\\automation-template-selenium-java-cucumber<br/>code .', 'CodeX'), p('Instale Extension Pack for Java, Gradle for Java, Cucumber (Gherkin) Full Support y GitLens. Espere que VS Code importe Gradle. Las Features están en src/test/resources/features; Pages en src/main/java; Steps, Hooks y Runner en src/test/java.'), p('Selección de versión de Java', 'H2x'), p('Java 21 es el predeterminado de la configuración actual. Java 17 es la única compatibilidad alternativa mediante la propiedad Gradle javaVersion. Java 18, 19, 20, 22 y cualquier otro valor distinto de 17 o 21 se rechazan explícitamente.'), p('.\\gradlew.bat clean test<br/>.\\gradlew.bat clean test -PjavaVersion=17<br/>.\\gradlew.bat clean test -PjavaVersion=21<br/>.\\gradlew.bat clean test -PjavaVersion=18  # rechazado', 'CodeX'), p('Gradle debe ejecutarse con JDK 17 o superior y la toolchain seleccionada debe estar instalada o disponible para Gradle.'), PageBreak()]
story += [heading('Sección 3.1 — Configurar Java 17 paso a paso'), p('Use Java 17 solo cuando lo requiera su proyecto. Java 21 continúa siendo el predeterminado de la configuración actual.'), p('1. Instale un JDK 17 aprobado por su equipo. En estos ejemplos, la carpeta se representa como C:\\ruta\\jdk-17.'), p('2. Abra PowerShell en la raíz del proyecto y configure la sesión actual. Esto no modifica permanentemente Windows:'), p("$env:JAVA_HOME = 'C:\\ruta\\jdk-17'<br/>$env:Path = \"$env:JAVA_HOME\\bin;$env:Path\"<br/>java -version", 'CodeX'), p('3. Confirme que java -version indica Java 17. En VS Code, use Ctrl+Shift+P, ejecute Java: Configure Java Runtime, seleccione JDK 17 y espere la importación Gradle.'), p('4. Ejecute las pruebas:'), p('.\\gradlew.bat clean test -PjavaVersion=17', 'CodeX'), p('5. Confirme BUILD SUCCESSFUL y abra build/reports/cucumber/cucumber.html. Para volver a Java 21, abra una consola nueva o cambie JAVA_HOME a C:\\ruta\\jdk-21 y ejecute -PjavaVersion=21.'), p('No guarde rutas de JDK ni JAVA_HOME dentro del repositorio. El workflow incluido usa Java 21. Si adopta Java 17 en otro proyecto, adapte y valide su CI antes de usarlo.'), PageBreak()]

story += [heading('4. Configuración y comandos'), p('config.properties contiene los valores por defecto. Los valores pueden reemplazarse con -D o con variables BASE_URL, BROWSER, HEADLESS, TIMEOUT_SECONDS y SCREENSHOT_ON_FAILURE. javaVersion usa -P, no -D.'), p('browser=CHROME<br/>headless=false<br/>baseUrl=https://example.com/<br/>timeoutSeconds=15<br/>screenshotOnFailure=true', 'CodeX'), table([['Objetivo','Comando'],['Limpiar','.\\gradlew.bat clean'],['Limpiar y ejecutar','.\\gradlew.bat clean test'],['Headless','.\\gradlew.bat clean test -Dheadless=true'],['Chrome','.\\gradlew.bat clean test -Dbrowser=CHROME'],['Edge','.\\gradlew.bat clean test -Dbrowser=EDGE'],['URL','.\\gradlew.bat clean test -DbaseUrl=https://su-aplicacion'],['Tags','.\\gradlew.bat clean test -Dcucumber.filter.tags=@example'],['Tags headless','.\\gradlew.bat clean test -Dheadless=true -Dcucumber.filter.tags=@example'],['Alias Cucumber','.\\gradlew.bat cucumber']], [5.2*cm, 11.1*cm]), Spacer(1,10), p('El smoke test incluido usa la fixture HTML local versionada y no depende de un sitio externo. baseUrl sigue disponible para los Page Objects de aplicaciones reales, pero no modifica este escenario de ejemplo. Los reports se generan en build/reports/cucumber/cucumber.html, build/reports/cucumber/cucumber.json, build/reports/tests/test y build/test-results/test; el log se guarda en build/logs/automation.log y las capturas de fallos en build/evidence/screenshots sólo si falla un escenario, screenshotOnFailure está activo y WebDriver permite capturar.'), PageBreak()]
story += docker_manual_section('es')
story += [heading('5&#46; Crear la primera automatización'), p('1. Cree src/test/resources/features/login.feature:'), p('# language: en<br/>Feature: Login<br/>&nbsp;&nbsp;Scenario: Successful login<br/>&nbsp;&nbsp;&nbsp;&nbsp;Given the user opens the login page<br/>&nbsp;&nbsp;&nbsp;&nbsp;When the user signs in with "username" and "password"<br/>&nbsp;&nbsp;&nbsp;&nbsp;Then the dashboard is displayed', 'CodeX'), p('2. Cree LoginPage.java en pages. Mantenga locators privados y métodos de intención, por ejemplo open(), login() e isDashboardVisible().'), p('3. Cree LoginSteps.java en steps. Obtenga el driver mediante DriverManager, delegue a LoginPage y use aserciones JUnit.'), p('4. Configure la URL con -DbaseUrl=... y ejecute .\\gradlew.bat test -Dheadless=true.'), p('5. Revise el reporte HTML. Use esperas explícitas WebDriverWait; nunca Thread.sleep.'), Spacer(1,10), heading('6. Reutilización paso a paso'), p('1. Copie o clone el template; conserve la base original sin cambios.'), p('2. Actualice rootProject.name en settings.gradle y group en build.gradle.'), p('3. Configure baseUrl con -DbaseUrl=https://su-aplicacion, sin secretos en Git.'), p('4. Abra la URL manualmente y ejecute una prueba smoke en headless.'), p('5. Cuando el smoke funcione, sustituya el ejemplo por sus Features, Pages y Steps.'), p('6. Añada tags como @smoke y @regression para seleccionar subconjuntos.'), p('7. Inicialice Git, revise .gitignore, cree una rama y abra Pull Request.'), p('8. Revise el workflow incluido en .github/workflows/ci.yml: ya ejecuta pruebas headless y publica las evidencias disponibles.'), p('Criterio de salida: el equipo puede configurar URL, ejecutar una prueba y consultar el reporte sin editar componentes compartidos.'), PageBreak()]
story += [Spacer(1, .4*cm), heading('7. Contrato CI/CD, buenas prácticas y soporte'), p('Workflow de GitHub Actions', 'H2x'), p('El workflow .github/workflows/ci.yml ejecuta ./gradlew clean test -Dheadless=true con Java 21 de Temurin y el Gradle Wrapper en pull requests y pushes hacia main. En Windows, use .\\gradlew.bat clean test -Dheadless=true para la validación local. Exit code 0 es éxito; cualquier otro código debe fallar el job. El contrato permite BROWSER, BASE_URL, HEADLESS y filtros cucumber.filter.tags; recolecte build/reports/cucumber/ (HTML y JSON), build/reports/tests/test, build/test-results/test, build/logs/automation.log y, sólo ante fallo, build/evidence/screenshots.'), p('Flujo: checkout, Java 21 Temurin, Gradle Setup/Cache, Gradle Wrapper, pruebas headless, reportes y test-evidence. gradle/actions/setup-gradle@v6 usa caché básica para reutilizar dependencias e información de Gradle; puede reducir trabajo repetitivo en ejecuciones posteriores. Si no hay caché (cache miss), Gradle descarga lo necesario y las pruebas continúan. El Wrapper sigue siendo el mecanismo oficial. La caché no cambia Selenium, Cucumber, Page Object Model, features, steps ni el smoke test local.'), p('El workflow usa ubuntu-latest y permisos mínimos de lectura. Intenta publicar las rutas anteriores como test-evidence durante 14 días incluso si Gradle falla. Una ruta vacía, como screenshots en una ejecución sin fallos, se ignora. Descargue el artifact en Artifacts dentro del resumen de GitHub Actions. La evidencia no cambia el estado PASS/FAIL del job. La imagen Docker es independiente del workflow; Grid y secretos de CI/CD no están implementados.'), p('Troubleshooting de Gradle', 'H2x'), p('.\\gradlew.bat --stop detiene Gradle Daemons ante problemas transitorios. Para diagnóstico de dependencias use .\\gradlew.bat clean test --offline o .\\gradlew.bat clean test -PjavaVersion=21 --offline; sólo usa caché y puede fallar si faltan dependencias. Si aparece PKIX path building failed o unable to find valid certification path, revise certificado Java, proxy, inspección SSL, red y daemon; ejecute java -version, .\\gradlew.bat --version, .\\gradlew.bat --stop y .\\gradlew.bat clean test. No deshabilite SSL ni ignore certificados.'), p('Regeneración del manual', 'H2x'), p('scripts/create_manual.py requiere Python 3 y reportlab. Ejecute python scripts/create_manual.py desde la raíz. Genera manuales PDF en docs/ (español) y docs_en/ (inglés). work/ es temporal, está ignorada por Git, no es parte del framework y puede eliminarse.'), p('Buenas prácticas', 'H2x'), p('Un Page Object por pantalla/componente; nombres descriptivos; configuración externa; locators estables; datos aislados; screenshots y logs como evidencia; commits pequeños; ramas, Pull Requests y revisión de código; actualización deliberada de dependencias.'), p('Para problemas de Java, navegador, features o CI, consulte docs/TROUBLESHOOTING.md y conserve el mensaje completo antes de modificar código.'), PageBreak()]

story += [heading('8. CI/CD con GitHub Actions'), p('CI (integración continua) valida automáticamente cambios antes de integrarlos. Detecta temprano errores de compilación y pruebas y ofrece al equipo un resultado compartido. CD significa entrega continua (preparar una versión para publicar) o despliegue continuo (publicarla automáticamente). Este proyecto utiliza principalmente CI; no despliega aplicaciones.'), p('Qué ejecuta GitHub Actions', 'H2x'), p('GitHub Actions lee .github/workflows/ci.yml cuando se abre o actualiza un Pull Request hacia main y cuando hay un push a main. Un Pull Request o PR es una propuesta de unir una rama de trabajo con otra. El workflow obtiene el código (checkout), prepara Java 21 Temurin y caché Gradle en un runner Linux ubuntu-latest, y ejecuta el Gradle Wrapper con Selenium y Cucumber en modo headless, sin ventana visible.'), p('Flujo para principiantes', 'H2x'), p('Developer -&gt; feature branch -&gt; commit -&gt; push -&gt; Pull Request hacia main -&gt; GitHub Actions -&gt; quality-gate -&gt; Gradle -&gt; Selenium + Cucumber -&gt; PASS/FAIL -&gt; evidencias -&gt; revisión -&gt; merge a main.'), p('El workflow se ejecuta automáticamente. No hay botón de ejecución manual configurado. El merge debe esperar la revisión y un check exitoso; el ruleset activo de main exige un Pull Request, la rama actualizada y quality-gate aprobado; un fallo bloquea el merge.'), p('9. Cómo ejecutar y revisar el CI/CD en GitHub Actions', 'H1x'), p('Necesita Git, acceso al repositorio en GitHub y permiso para enviar ramas. Ejecute desde la raíz del proyecto.'), p('1. Cree una rama separada de main: git switch -c feature/mi-cambio. Si ya existe: git switch feature/mi-cambio. Main es la línea compartida; una feature branch aísla su trabajo.'), p('2. Modifique el proyecto, por ejemplo un Page Object y sus pruebas.'), p('3. Revise git status y git diff. Compruebe que no haya credenciales ni archivos generados.'), p('4. Ejecute las pruebas locales:'), p('Windows PowerShell: .\\gradlew.bat clean test "-Dheadless=true"<br/>Linux/macOS: ./gradlew clean test -Dheadless=true', 'CodeX'), p('Espere BUILD SUCCESSFUL. Si ve BUILD FAILED, corrija el error.'), PageBreak()]
story += [heading('Continuación: Pull Request y revisión de resultados'), p('5. Guarde el cambio en Git: git add ruta/del/archivo y git commit -m "Describe mi cambio". Un commit es una instantánea identificable.'), p('6. Envíe la rama: git push -u origin feature/mi-cambio la primera vez; luego git push. Push copia los commits a GitHub.'), p('7. En el repositorio de GitHub abra Pull requests -&gt; New pull request. Seleccione main como base (destino) y feature/mi-cambio como compare (origen). Revise el contenido, agregue título y descripción y pulse Create pull request. No haga merge todavía.'), p('8. GitHub detecta el PR y ejecuta .github/workflows/ci.yml automáticamente. Cada nuevo commit seguido de push a la misma rama actualiza el PR y inicia otra ejecución.'), p('Desde el Pull Request', 'H2x'), p('Abra Repositorio -&gt; Pull requests -&gt; su PR -&gt; Checks; según la interfaz, los checks también aparecen en Conversation. Busque quality-gate y pulse Details. Allí verá checkout, Java 21, caché Gradle, pruebas, carga de evidencias y resultado final. Expanda un step para ver sus logs.'), p('Desde Actions', 'H2x'), p('Abra Repositorio -&gt; Actions -&gt; workflow CI -&gt; ejecución del PR. Identifique rama, PR, commit, fecha, estado y duración. Abra la ejecución y el job quality-gate para inspeccionar cada step.'), table([['Estado visible', 'Qué significa'], ['Success (verde)', 'Las verificaciones terminaron correctamente.'], ['Failure (rojo)', 'Una verificación falló.'], ['In progress (amarillo/progreso)', 'La ejecución todavía no termina.'], ['Cancelled', 'La ejecución se canceló.'], ['Skipped', 'Un step no se ejecutó por una condición.']], [6.2*cm, 10.1*cm]), p('Lea el texto del estado además del color: así puede interpretar el resultado aun sin distinguir colores.'), PageBreak()]
story += [heading('10. ¿Qué es un Quality Gate?'), p('Es una puerta de control: las verificaciones automáticas deben terminar bien antes de considerar listo un cambio. El job/check estable se llama quality-gate. Gradle devuelve exit code 0 cuando compilación y pruebas pasan; un código distinto de cero indica fallo. GitHub muestra PASS/Success para continuar a revisión o FAIL/Failure para corregir. La carga posterior de artifacts no cambia FAIL a PASS.'), p('¿Qué hacer si el Quality Gate falla?', 'H2x'), p('1. Abra el PR -&gt; Checks -&gt; quality-gate -&gt; Details.'), p('2. Localice el step Failure, expándalo y lea el error y el resumen final.'), p('3. Descargue test-evidence si existe; revise reportes, XML, logs y screenshots. Si Gradle terminó antes de generar archivos, algunos faltarán.'), p('4. Corrija el problema en su rama y repita la prueba local:'), p('.\\gradlew.bat clean test "-Dheadless=true"', 'CodeX'), p('En Linux/macOS use ./gradlew clean test -Dheadless=true.'), p('5. Revise git diff, haga otro git add y git commit, y ejecute git push. El PR se actualiza y Actions ejecuta de nuevo quality-gate. Espere el nuevo resultado.'), p('Cómo descargar las evidencias de GitHub Actions', 'H2x'), p('Un artifact es un archivo descargable creado por una ejecución y separado del código. Abra Repository -&gt; Actions -&gt; CI -&gt; ejecución del PR -&gt; Artifacts -&gt; test-evidence. Descargue y extraiga el ZIP. Se conserva 14 días. Se intenta publicar tanto en PASS como en FAIL, pero sólo aparece cuando existen archivos. Si falta, revise el step Upload test evidence y si Gradle creó resultados. Las capturas suelen faltar cuando no fallan escenarios.'), table([['Ruta local / artifact', 'Qué contiene'], ['build/reports/cucumber/cucumber.html', 'Escenarios y pasos Cucumber.'], ['build/reports/cucumber/cucumber.json', 'Resultado estructurado Cucumber y attachments.'], ['build/reports/tests/test/', 'Reporte HTML Gradle/JUnit.'], ['build/test-results/test/', 'Resultados XML estructurados.'], ['build/logs/automation.log', 'Log cronológico.'], ['build/evidence/screenshots/', 'Capturas de fallos cuando correspondan.']], [8*cm, 8.3*cm]), PageBreak()]
story += [
    heading('11. Protección de la rama main'),
    p('Las reglas de GitHub controlan cómo se integra código en main. El flujo recomendado es rama de trabajo, Pull Request, quality-gate, revisión y merge. Un status check fallido o pendiente impide el merge cuando está configurado como obligatorio.'),
    p('El ruleset de main documentado para este repositorio requiere Pull Request, quality-gate aprobado y rama actualizada; también bloquea force push y eliminación de main. Consulte el estado actual en Repository &gt; Settings &gt; Rules &gt; Rulesets antes de integrar cambios.'),
    p('Si un PR falla, abra Checks &gt; quality-gate &gt; Details, revise el paso fallido y descargue test-evidence cuando exista. Corrija el cambio en la rama, repita las pruebas locales y envíe otro commit. GitHub vuelve a ejecutar el workflow.'),
    p('La versión v1.1.0 se publicó el 1 de octubre de 2026. El historial de la página inicial contiene las fechas de v1.1.0 y v1.2.0. Consulte los README para el estado vigente.'),
    PageBreak(),
]

story += [
    heading('12. Logging y observabilidad básica'),
    p('Los eventos técnicos permiten reconstruir la configuración efectiva, el resultado del escenario y el cierre de WebDriver. Consulte el archivo de log junto con los reportes para diagnosticar un fallo.'),
    p('El logging ayuda a reconstruir el inicio, la configuración efectiva, el resultado y el cierre de un escenario cuando una prueba falla o se ejecuta en CI/CD. El código usa SLF4J 2.0.20 como API común para Hooks y driver, evitando configurar salidas en cada clase. Logback 1.6.5 es el proveedor de pruebas que centraliza niveles, formato y destinos en src/test/resources/logback-test.xml.'),
    p('Diagrama A - Arquitectura de logging', 'H2x'),
    LoggingDiagram('architecture'),
    p('Los eventos del framework pasan por SLF4J y Logback. Cada evento se emite a consola y a build/logs/automation.log; no se duplican llamadas de logging en Steps o Page Objects.'),
    PageBreak(),
    p('12.1 Flujo de observabilidad', 'H2x'),
    p('Diagrama B - Eventos en orden de ejecución', 'H2x'),
    LoggingDiagram('flow'),
    p('Los Hooks registran inicio, nombre, navegador y headless efectivos antes de crear el driver. DriverFactory registra la inicialización; al finalizar, el Hook registra el estado Cucumber y DriverManager cierra el WebDriver. La consola y el archivo reciben los eventos a medida que ocurren.'),
    p('12.2 Niveles de logging', 'H2x'),
    table([['Nivel', 'Uso'], ['DEBUG', 'Detalle técnico de creación del driver; oculto por defecto.'], ['INFO', 'Eventos normales: escenario, configuración segura y WebDriver.'], ['WARN', 'Condición recuperable, como ausencia de soporte para capturas.'], ['ERROR', 'Fallo al cerrar WebDriver o manejar evidencia existente.']], [3*cm, 13.3*cm]),
    PageBreak(),
    p('12.3 Ejecución y seguridad', 'H2x'),
    p('Ejecute .\\gradlew.bat clean test -Dheadless=true en Windows, o ./gradlew clean test -Dheadless=true en GitHub Actions. Gradle muestra los logs de test en consola. Logback guarda el archivo bajo build/, ignorado por Git. gradlew clean elimina el log anterior y la siguiente ejecución crea uno nuevo. El workflow existente ya incluye build/logs/ en el artifact test-evidence; no se modificó el workflow.'),
    p('Extracto abreviado de una ejecución headless real', 'H2x'),
    p('2026-10-01 17:36:35.726 INFO [Test worker] Hooks - Starting scenario: Validar el encabezado de la página de ejemplo<br/>2026-10-01 17:36:35.734 INFO [Test worker] Hooks - Scenario configuration: browser=CHROME, headless=true<br/>2026-10-01 17:36:37.110 INFO [Test worker] Hooks - Finished scenario: Validar el encabezado de la página de ejemplo, status=PASSED<br/>2026-10-01 17:36:37.208 INFO [Test worker] DriverManager - WebDriver closed.', 'CodeX'),
    p('No registre secretos, tokens, contraseñas, cookies, headers confidenciales ni propiedades indiscriminadamente. baseUrl no se registra porque una URL arbitraria puede incluir datos sensibles. Las rutas de error existentes registran excepciones completas; las de herramientas externas podrían contener datos de la aplicación. Revise las trazas antes de compartir logs o artifacts.'),
    p('Si falta automation.log, confirme que test inició el proceso de pruebas y consulte build/logs/. Si falta DEBUG, revise el nivel INFO predeterminado en logback-test.xml. Si hay avisos de proveedores SLF4J, inspeccione el classpath con .\\gradlew.bat dependencies --configuration testRuntimeClasspath. Si falla la descarga por PKIX, revise certificados y proxy del JDK sin desactivar TLS.'),
    p('12.4 Diagnóstico del logging', 'H2x'),
    p('Si el archivo no aparece, confirme que la tarea test alcanzó la ejecución de escenarios y que src/test/resources/logback-test.xml está en el classpath. clean elimina logs anteriores. El nivel raíz INFO oculta DEBUG; un fallo de compilación previo a test puede impedir la creación del archivo.'),
    PageBreak(),
]

story += [
    heading('13. Captura automática de evidencias'),
    p('Una evidencia visual conserva el estado de la página cuando falla un escenario Cucumber. Ayuda a investigar un error que no puede reconstruirse sólo con el mensaje de la aserción. La captura se intenta únicamente si el escenario falló y screenshotOnFailure=true; un escenario exitoso no crea un PNG de fallo.'),
    p('Cómo se genera', 'H2x'),
    p('El Hook @After consulta el estado del escenario y entrega el WebDriver activo a EvidenceManager antes de cerrarlo. El gestor verifica que el driver exista, que una sesión RemoteWebDriver siga activa y que soporte TakesScreenshot. Captura bytes PNG, crea build/evidence/screenshots/, guarda el archivo y adjunta los mismos bytes mediante Scenario.attach(..., "image/png", "failure-screenshot").'),
    table([['Paso', 'Resultado'], ['Escenario fallido', 'Activa la captura cuando screenshotOnFailure=true.'], ['WebDriver disponible', 'Comprueba sesión activa y soporte de screenshots.'], ['PNG local', 'Guarda en build/evidence/screenshots/.'], ['Attachment', 'Incluye image/png en el resultado Cucumber.'], ['Cierre', 'El Hook libera WebDriver incluso si la captura falla.']], [5.2*cm, 11.1*cm]),
    p('Consulta y correlación', 'H2x'),
    p('Abra build/reports/cucumber/cucumber.html y busque el escenario fallido y su attachment. El JSON en build/reports/cucumber/cucumber.json conserva la misma evidencia para procesamiento automatizado. Compare el nombre y estado del escenario con build/logs/automation.log y el PNG en build/evidence/screenshots/. El nombre del archivo usa un nombre seguro de hasta 80 caracteres, fecha/hora y UUID.'),
    p('Si la captura falla', 'H2x'),
    p('Si falta el driver, la sesión está cerrada o la captura devuelve bytes vacíos, se registra un warning y se conserva el fallo original. Si no puede guardarse el archivo, todavía se intenta adjuntar la imagen al escenario; si falla el attachment, el escenario sigue fallido. La ausencia de PNG en un PASS es normal.'),
    p('Ejemplo y privacidad', 'H2x'),
    p('Ejecute .\\gradlew.bat clean test -Dheadless=true y consulte el HTML. Para comprobar una captura, use una prueba controlada que falle y restáurela antes de volver a ejecutar la suite. clean elimina la evidencia anterior: inspecciónela antes de repetir. Las capturas y excepciones pueden incluir datos visibles de la aplicación; revíselas antes de compartir artifacts. build/ está ignorado por Git.'),
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
    ('GitHub', 'Plataforma para repositorios, revisiones y workflows de CI.'),
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
story += [
    heading('14. Generación y consulta de reportes'),
    p('Los reportes muestran qué escenarios y pasos se ejecutaron, cuáles pasaron o fallaron y qué evidencia se adjuntó. El runner JUnit Platform configura los plugins nativos de Cucumber pretty, HTML y JSON; Gradle produce HTML y JUnit XML. No hay dashboard histórico ni agregación entre ejecuciones.'),
    p('Generar y abrir resultados', 'H2x'),
    p('Desde la raíz, ejecute .\\gradlew.bat clean test -Dheadless=true en PowerShell o ./gradlew clean test -Dheadless=true en Linux/macOS. Después abra build/reports/cucumber/cucumber.html y build/reports/tests/test/index.html en un navegador. Use cucumber.json y los XML de build/test-results/test/ para procesamiento o CI. pretty muestra los pasos en consola.'),
    table([['Salida', 'Ruta y uso'], ['Cucumber HTML', 'build/reports/cucumber/cucumber.html - escenarios, pasos y attachments.'], ['Cucumber JSON', 'build/reports/cucumber/cucumber.json - resultados estructurados y attachments.'], ['Gradle HTML', 'build/reports/tests/test/ - resultado técnico de la tarea test.'], ['JUnit XML', 'build/test-results/test/ - resultados estructurados para CI/CD.'], ['Logback', 'build/logs/automation.log - eventos técnicos.'], ['Screenshot PNG', 'build/evidence/screenshots/ - imagen de un fallo elegible.']], [4.4*cm, 11.9*cm]),
    p('Interpretar un fallo', 'H2x'),
    p('Busque el escenario y el paso fallido en Cucumber HTML/JSON. Compare su nombre y estado con el log y el resultado JUnit XML. Si el navegador estaba disponible y la captura estaba activada, abra el attachment image/png o el PNG local. Un error previo a test puede dejar reportes ausentes; una captura fallida no reemplaza el resultado del escenario.'),
    p('GitHub Actions y límites', 'H2x'),
    p('El job quality-gate ejecuta pruebas headless. Upload test evidence usa if: always() y recoge los archivos disponibles bajo build/reports/, build/test-results/, build/logs/ y build/evidence/screenshots/ en el artifact test-evidence durante 14 días. Un artifact puede estar incompleto si el build falló temprano. clean reemplaza resultados locales; conserve lo necesario antes de repetir y revise datos sensibles antes de compartir.'),
    PageBreak(),
]

story += [Spacer(1, .4*cm), heading('15. Glosario'), p('Términos clave del template y de la automatización Web UI.'), glossary_table(glossary_rows[:27]), PageBreak(), heading('Glosario (continuación)'), glossary_table(glossary_rows[27:])]

doc=SimpleDocTemplate(str(OUT), pagesize=A4, rightMargin=2*cm, leftMargin=2*cm, topMargin=1.8*cm, bottomMargin=2*cm, title='Manual Template Automatización Selenium Java Cucumber', author='Automation Template')
doc.build(story, onFirstPage=footer, onLaterPages=footer)
print(OUT)
if args.output is None:
    english = [
        Spacer(1, 5*cm),
        p('SELENIUM JAVA CUCUMBER', 'Cover'),
        p('Automation Template - User Manual', 'CoverSub'),
        p('v1.2.0 - Stable / Validated / Published<br/>Published: October 8, 2026, 06:19:01 UTC<br/>Latest published release: v1.2.0', 'CoverSub'),
        Spacer(1, 2*cm),
        p('Java 21 default / Java 17 supported - Selenium 4.48.0 - Cucumber 7.34.7 - JUnit 5.13.4 - Gradle 8.14.5', 'CoverSub'),
        PageBreak(),
        heading('Contents'),
        p('1. First run<br/>2. Architecture<br/>3. Stack, prerequisites and VS Code<br/>3.1 Configure Java 17<br/>4. Configuration and commands<br/>4.1 Using Docker<br/>5. First automation<br/>6. Reuse<br/>7. CI/CD contract and support<br/>8. GitHub Actions workflow<br/>9. Run and inspect CI<br/>10. Quality gate and evidence<br/>11. Main branch protection<br/>12. Logging and observability<br/>12.1 Event flow<br/>12.2 Levels<br/>12.3 Execution and privacy<br/>12.4 Diagnostics<br/>13. Automatic failure evidence<br/>14. Generate and inspect reports<br/>15. Glossary'),
        p('Purpose', 'H2x'),
        p('This manual covers setup, configuration, execution, extension, CI, evidence, reporting and diagnosis for the Web UI automation template. The included example uses a local HTML fixture. Basic Java knowledge is needed to create new tests.'),
        PageBreak(),
        heading('Version history'),
        version_table([
            ('v1.2.0', 'Oct 8, 2026', 'Stable / Validated / Published. Logging, failure evidence, Cucumber HTML/JSON reporting.'),
            ('v1.1.0', 'Oct 1, 2026', 'Stable / Validated / Published. CI quality gate and test artifacts.'),
            ('v1.0.2', 'Sep 26, 2026', 'Published documentation-only hotfix.'),
            ('v1.0.1', 'Sep 25, 2026', 'Published hardening and CI/CD readiness.'),
            ('v1.0.0', 'Sep 18, 2026', 'First stable template release.'),
        ], 'en'),
        p('The release date above is GitHub Release published_at in UTC. The original Milestone 4 candidate audit remains a historical record, not the current release status.'),
        PageBreak(),
        heading('1. First run'),
        p('Install JDK 21 and Chrome or Edge. Open PowerShell at the repository root and run the Gradle Wrapper. Global Gradle is not needed.'),
        p('.\\gradlew.bat clean test -Dheadless=true', 'CodeX'),
        p('A visible run uses -Dheadless=false and requires a graphical desktop. On Linux/macOS use ./gradlew. Open build/reports/cucumber/cucumber.html after the run. The sample scenario checks the local HTML fixture, so it does not rely on the content of an external website.'),
        heading('2. Architecture'),
        p('Gradle -> JUnit Platform runner -> Cucumber feature -> Before hook -> Steps -> Page objects -> WebDriver -> After hook -> evidence and reports. Configuration precedence: JVM -D, environment, then config.properties.'),
        table([['Layer', 'Responsibility'], ['Features', 'Gherkin scenarios under src/test/resources/features.'], ['Steps', 'Map Gherkin to page actions and assertions.'], ['Pages', 'Hold locators, explicit waits and UI interactions.'], ['Driver / Hooks', 'Create and close a per-thread Chrome or Edge session.'], ['Support', 'Manage the driver reference and failure evidence.']], [4.5*cm, 11.8*cm]),
        p('Keep locators out of steps, scenario assertions out of pages, and business logic out of hooks.'),
        PageBreak(),
        heading('3. Stack, prerequisites and VS Code'),
        table([['Component', 'Version and use'], ['Java', '21 default, 17 supported toolchain.'], ['Gradle Wrapper', '8.14.5 build and dependencies.'], ['Selenium Java', '4.48.0 browser control.'], ['Cucumber Java/Engine', '7.34.7 BDD/Gherkin.'], ['JUnit BOM', '5.13.4 JUnit Platform.'], ['SLF4J / Logback', '2.0.20 / 1.6.5 test logging.']], [5*cm, 11.3*cm]),
        p('Check java -version, .\\gradlew.bat --version, and git --version. In VS Code open the root with code ., install Java/Gradle and Gherkin support, and wait for Gradle import.'),
        heading('3.1. Configure Java 17'),
        p('Only 17 and 21 are accepted by -PjavaVersion. Set JAVA_HOME to an installed JDK 17 for the current shell, add its bin directory to PATH, confirm java -version, then run .\\gradlew.bat clean test -PjavaVersion=17. In VS Code, select JDK 17 in Java: Configure Java Runtime. Restore JDK 21 and use -PjavaVersion=21 to return to the default. CI uses Java 21.'),
        PageBreak(),
        heading('4. Configuration and commands'),
        p('config.properties defaults: browser=CHROME, headless=false, baseUrl=https://example.com/, timeoutSeconds=15, screenshotOnFailure=true. Override them with JVM -D properties or BROWSER, HEADLESS, BASE_URL, TIMEOUT_SECONDS and SCREENSHOT_ON_FAILURE environment variables. javaVersion is a Gradle -P property.'),
        table([['Goal', 'Command'], ['Headless suite', '.\\gradlew.bat clean test -Dheadless=true'], ['Visible suite', '.\\gradlew.bat clean test -Dheadless=false'], ['Edge', '.\\gradlew.bat clean test -Dbrowser=EDGE'], ['Java 17', '.\\gradlew.bat clean test -PjavaVersion=17'], ['Tag @example', '.\\gradlew.bat test "-Dcucumber.filter.tags=@example"'], ['Alias', '.\\gradlew.bat cucumber']], [4*cm, 12.3*cm]),
        p('The sample uses a local fixture regardless of baseUrl. A derived project can use baseUrl in its own page objects.'),
        PageBreak(),
        *docker_manual_section('en'),
        heading('5. First automation'),
        p('Add a .feature under src/test/resources/features, Java step definitions under steps, and a page object under pages. Place stable locators and explicit waits in the page, and scenario assertions in steps. Start with the included example_domain.feature and ExampleDomainPage.'),
        p('Example feature', 'H2x'),
        p('# language: en<br/>Feature: Login<br/>  Scenario: Successful login<br/>    Given the user opens the login page<br/>    When the user signs in with valid credentials<br/>    Then the dashboard is displayed', 'CodeX'),
        p('Create LoginPage.java with private locators and intention-revealing open(), login() and isDashboardVisible() methods. Create LoginSteps.java using DriverManager, delegate UI actions to the page and assert the expected outcome with JUnit. Set the target URL through -DbaseUrl. Prefer WebDriverWait over Thread.sleep.'),
        heading('6. Reuse'),
        p('Replace the sample with the target application, externalize test data, run the tagged scenario, then the full suite. Keep credentials, generated build output, and screenshots out of Git.'),
        p('For a derived repository, update rootProject.name in settings.gradle and group in build.gradle. Replace sample features, pages and steps only after the smoke test works. Use tags such as @smoke and @regression to select suites. Review the included CI workflow before relying on it for a new application.'),
        PageBreak(),
        heading('7. CI/CD contract and support'),
        p('.github/workflows/ci.yml runs on pull requests to main and pushes to main. It uses ubuntu-latest, Temurin Java 21, Gradle cache, and ./gradlew clean test -Dheadless=true. A nonzero Gradle exit code fails the job. The Docker image is separate from this workflow; Selenium Grid and automated deployment are not implemented.'),
        heading('8. GitHub Actions workflow'),
        p('Workflow: checkout -> Java 21 -> Gradle setup/cache -> headless test -> upload available test-evidence. The artifact includes Cucumber HTML/JSON, Gradle HTML, JUnit XML, logs and eligible failure screenshots; it is retained for 14 days. Upload runs with if: always() and cannot turn FAIL into PASS.'),
        heading('9. Run and inspect CI'),
        p('For a pull request, open Checks -> quality-gate -> Details. Inspect the failed step and download test-evidence from Actions when available. Fix the branch and rerun. An early compilation failure may leave incomplete artifacts.'),
        p('Step-by-step PR review', 'H2x'),
        p('Create a focused branch, edit and test locally, then inspect git status and git diff for secrets and generated files. Commit the change and push the branch. On GitHub select main as the PR base and your branch as compare. Open Checks to see checkout, Java setup, Gradle cache, tests and evidence upload. Every new pushed commit reruns the check. In Actions, open the workflow run and its quality-gate job; read the status text, not only its color.'),
        p('When quality-gate fails, expand the failed step, keep the full error, download test-evidence if present, fix the branch, rerun .\\gradlew.bat clean test -Dheadless=true locally, then commit and push. Wait for the new check. The artifact may contain fewer files if compilation stopped before tests.'),
        heading('10. Quality gate and evidence'),
        p('The main ruleset documented by the project requires a pull request and passing quality-gate. A passing scenario produces no failure screenshot; an eligible failed scenario can produce a PNG and Cucumber image/png attachment.'),
        heading('11. Main branch protection'),
        p('Review and CI validation precede merge. A required check that fails or remains pending blocks integration. Do not move an existing release tag to correct documentation.'),
        PageBreak(),
        heading('12. Logging and observability'),
        p('SLF4J 2.0.20 in hooks and driver code delegates to Logback 1.6.5, configured by src/test/resources/logback-test.xml. Logback writes console output and build/logs/automation.log.'),
        p('Diagram A - logging architecture', 'H2x'),
        LoggingDiagram('architecture', 'en'),
        heading('12.1. Event flow'),
        p('Scenario start and effective browser/headless setting -> WebDriver initialization -> test execution -> scenario result -> optional failure capture -> driver shutdown. Logs record events throughout.'),
        PageBreak(),
        p('Diagram B - observability flow', 'H2x'),
        LoggingDiagram('flow', 'en'),
        heading('12.2. Levels'),
        p('DEBUG: technical driver detail (hidden by default). INFO: normal scenario and driver lifecycle. WARN: recoverable capture issue. ERROR: evidence or shutdown error. Root level is INFO.'),
        heading('12.3. Execution and privacy'),
        p('The framework does not log baseUrl, screenshot bytes or Base64. Never add passwords, tokens, cookies or full environment dumps. Third-party exception traces, screenshots and reports can contain application data; review them before sharing.'),
        heading('12.4. Diagnostics'),
        p('If no log appears, check that test started and that clean did not remove prior output. To inspect dependencies use .\\gradlew.bat dependencies --configuration testRuntimeClasspath. For PKIX errors inspect the JDK trust store and proxy; do not disable TLS.'),
        PageBreak(),
        heading('13. Automatic failure evidence'),
        p('On failed scenarios with screenshotOnFailure=true, the After hook passes WebDriver to EvidenceManager before shutdown. An active screenshot-capable session saves a PNG under build/evidence/screenshots/ and attaches image/png to Cucumber. The filename contains a sanitized scenario name, timestamp and UUID. Capture errors generate warnings without replacing the original test failure.'),
        heading('14. Generate and inspect reports'),
        table([['Output', 'Path'], ['Cucumber HTML', 'build/reports/cucumber/cucumber.html'], ['Cucumber JSON', 'build/reports/cucumber/cucumber.json'], ['Gradle HTML', 'build/reports/tests/test/'], ['JUnit XML', 'build/test-results/test/'], ['Logback', 'build/logs/automation.log'], ['Failure PNG', 'build/evidence/screenshots/']], [4.4*cm, 11.9*cm]),
        p('Match scenario name and status across Cucumber HTML/JSON and the log, then inspect XML/Gradle HTML. clean removes prior results; inspect evidence before rerunning. No historical dashboard or cross-run aggregation is implemented.'),
        p('To diagnose a failure, open the Cucumber HTML and locate the failed step and image attachment. Compare scenario name and status with automation.log and JUnit XML. If capture was enabled and a driver was active, inspect the PNG. A missing PNG on a PASS is expected. A screenshot capture failure must not hide the original scenario failure. Review reports and images for sensitive application data before sharing.'),
        PageBreak(),
        heading('15. Glossary'),
        glossary_table([
            ('BDD', 'Behavior-driven development; scenarios describe expected behavior.'),
            ('Gherkin', 'Readable language for features, scenarios and steps.'),
            ('Page Object Model', 'Pattern that encapsulates UI locators and interactions.'),
            ('WebDriver', 'Selenium interface that controls Chrome or Edge.'),
            ('Hook', 'Code that prepares or cleans up a scenario.'),
            ('Gradle Wrapper', 'Versioned scripts that run the required Gradle version.'),
            ('Headless', 'Browser execution without a visible window.'),
            ('Quality gate', 'Required check used before integrating a change.'),
            ('Artifact', 'Downloadable files produced by a CI run.'),
            ('Screenshot', 'PNG image saved as evidence on an eligible failure.'),
            ('Automation testing', 'Tests executed by software to verify an application.'),
            ('Selenium', 'Library for automating web browsers.'),
            ('Cucumber', 'BDD tool that runs Gherkin scenarios.'),
            ('Feature', 'Business capability described in a Gherkin file.'),
            ('Scenario', 'Concrete example that verifies expected behavior.'),
            ('Step definition', 'Java code that implements a Gherkin sentence.'),
            ('JUnit Platform', 'Platform that discovers and coordinates tests.'),
            ('Gradle', 'Build, dependency and test execution tool.'),
            ('Locator', 'Rule that identifies a UI element.'),
            ('CSS selector', 'Rule that selects elements by CSS attributes or classes.'),
            ('XPath', 'Syntax to locate elements in a DOM.'),
            ('Assertion', 'Check of an expected test result.'),
            ('Test data', 'Controlled data used by a test run.'),
            ('Environment variable', 'External value that configures a run.'),
            ('Explicit wait', 'Wait until a WebDriver condition holds.'),
            ('CI', 'Continuous integration of changes through automated checks.'),
            ('CD', 'Continuous delivery or deployment; this template does not deploy.'),
        ], 'en'),
        PageBreak(),
        heading('Glossary (continued)'),
        glossary_table([
            ('CI/CD', 'Continuous integration and delivery processes.'),
            ('Pipeline', 'Automated sequence of build and validation steps.'),
            ('Git', 'Distributed version control system.'),
            ('GitHub', 'Repository hosting and CI platform.'),
            ('GitHub Actions', 'Service that runs repository workflows.'),
            ('Workflow', 'Instructions in a file such as ci.yml.'),
            ('Job', 'Group of steps run by a CI runner.'),
            ('Step', 'Individual instruction in a CI job.'),
            ('Runner', 'Temporary machine executing a CI job.'),
            ('ubuntu-latest', 'GitHub Actions Ubuntu runner label.'),
            ('Pull request', 'Proposal to integrate branch changes after review.'),
            ('Branch', 'Separate line of Git development.'),
            ('main', 'Shared primary repository branch.'),
            ('Feature branch', 'Branch dedicated to a specific change.'),
            ('Status check', 'Visible result of a GitHub verification.'),
            ('Required check', 'Check that must pass before merging.'),
            ('Branch protection', 'Rules restricting changes to a branch.'),
            ('Log', 'Chronological record of execution events.'),
            ('Report', 'Readable summary of test results.'),
            ('Exit code', 'Process result: zero success; nonzero failure.'),
            ('PASS', 'Verification completed successfully.'),
            ('FAIL', 'Verification ended with an error.'),
            ('Commit', 'Identifiable snapshot of Git changes.'),
            ('Push', 'Transfer of local commits to a remote repository.'),
            ('Merge', 'Integration of one branch into another.'),
            ('Checkout', 'Retrieval of a revision for execution.'),
        ], 'en'),
    ]
    def footer_en(canvas, document):
        if document.page > 1:
            canvas.saveState()
            canvas.setStrokeColor(colors.HexColor('#D9E1EA'))
            canvas.line(2*cm, 1.45*cm, A4[0]-2*cm, 1.45*cm)
            canvas.setFont('Helvetica', 8)
            canvas.setFillColor(colors.HexColor('#526273'))
            canvas.drawString(2*cm, 0.9*cm, 'Selenium Java Cucumber Automation Template')
            canvas.drawRightString(A4[0]-2*cm, 0.9*cm, f'Page {document.page}')
            canvas.restoreState()
    EN_OUT.parent.mkdir(parents=True, exist_ok=True)
    doc_en = SimpleDocTemplate(str(EN_OUT), pagesize=A4, rightMargin=2*cm, leftMargin=2*cm, topMargin=1.8*cm, bottomMargin=2*cm, title='Selenium Java Cucumber Automation Template - User Manual', author='Automation Template')
    doc_en.build(english, onFirstPage=footer_en, onLaterPages=footer_en)
    print(EN_OUT)
