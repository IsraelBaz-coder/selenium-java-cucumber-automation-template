"""Prepare and validate the v1.2.0 documentation in the tagged release.

Usage:
    python scripts/finalize_release_docs.py stage --date YYYY-MM-DD
    python scripts/finalize_release_docs.py check --date YYYY-MM-DD
    python scripts/finalize_release_docs.py pretag --date YYYY-MM-DD
    python scripts/finalize_release_docs.py postrelease --date YYYY-MM-DD

The planned date uses the UTC calendar day expected in GitHub's published_at field.
"""

from __future__ import annotations

import argparse
from datetime import date, datetime, timezone
from pathlib import Path
import re
import subprocess
import sys
import urllib.error
import urllib.request
import json

ROOT = Path(__file__).resolve().parents[1]
VERSION = "v1.2.0"
RELEASE_API = (
    "https://api.github.com/repos/IsraelBaz-coder/"
    "selenium-java-cucumber-automation-template/releases/tags/v1.2.0"
)
PDF = ROOT / "docs/Manual_Template_Automatizacion_Selenium_Java_Cucumber.pdf"
EXTERNAL_PDF = ROOT.parent / PDF.name
PLANNED_DATE = date(2026, 10, 8)

SPANISH_MONTHS = (
    "enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto",
    "septiembre", "octubre", "noviembre", "diciembre",
)
ENGLISH_MONTHS = (
    "January", "February", "March", "April", "May", "June", "July", "August",
    "September", "October", "November", "December",
)


def release_date_from_github() -> date:
    request = urllib.request.Request(
        RELEASE_API,
        headers={"Accept": "application/vnd.github+json", "User-Agent": "release-docs-v1.2.0"},
    )
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            release = json.load(response)
    except (urllib.error.URLError, TimeoutError, ValueError) as exc:
        raise RuntimeError("No se pudo confirmar el GitHub Release v1.2.0; no se modificó la documentación.") from exc
    if release.get("tag_name") != VERSION or release.get("draft") or release.get("prerelease"):
        raise RuntimeError("GitHub no confirma un release final publicado de v1.2.0.")
    published_at = release.get("published_at")
    if not isinstance(published_at, str) or not published_at:
        raise RuntimeError("El GitHub Release no tiene published_at; no se puede fijar la fecha.")
    instant = datetime.fromisoformat(published_at.replace("Z", "+00:00"))
    if instant.tzinfo is None:
        raise RuntimeError("La fecha de GitHub no incluye zona horaria.")
    return instant.astimezone(timezone.utc).date()


def spanish_day(day: date) -> str:
    return f"{day.day} de {SPANISH_MONTHS[day.month - 1]} de {day.year}"


def english_day(day: date) -> str:
    return f"{ENGLISH_MONTHS[day.month - 1]} {day.day}, {day.year}"


def replace_once(body: str, old: str, new: str, file_name: str) -> str:
    count = body.count(old)
    if count != 1:
        raise RuntimeError(f"{file_name}: se esperaba una coincidencia, encontradas {count}: {old[:75]!r}")
    return body.replace(old, new)


def replace_line(body: str, starts: str, new: str, file_name: str) -> str:
    matches = [line for line in body.splitlines() if line.startswith(starts)]
    if len(matches) != 1:
        raise RuntimeError(f"{file_name}: se esperaba una línea que comienza {starts!r}.")
    return replace_once(body, matches[0], new, file_name)


def transform(day: date) -> dict[Path, str]:
    es, en, iso = spanish_day(day), english_day(day), day.isoformat()
    changed: dict[Path, str] = {}

    def edit(name: str, operations: list[tuple[str, str, str]]) -> None:
        path = ROOT / name
        body = path.read_text(encoding="utf-8")
        for kind, old, new in operations:
            body = replace_line(body, old, new, name) if kind == "line" else replace_once(body, old, new, name)
        changed[path] = body

    edit("README.md", [
        ("exact", "| Versión estable publicada | **v1.1.0** |", "| Versión estable publicada | **v1.2.0** |"),
        ("line", "| Versión candidata |", "| Versión vigente | **v1.2.0 — Stable / Validated / Published** |"),
        ("line", "| Estado de v1.2.0 |", "| Estado de v1.2.0 | **Stable / Validated / Published** |"),
        ("line", "| Fecha de publicación de v1.2.0 |", f"| Fecha de publicación de v1.2.0 | **{es}** |"),
        ("line", "v1.1.0 es la última versión publicada", f"v1.2.0 es la última versión publicada ({es}). Incorpora logging con SLF4J/Logback, evidencias automáticas ante fallos y reportes Cucumber HTML/JSON. Su estado es **Stable / Validated / Published**. Consulte el [informe de auditoría](docs/HITO4_RELEASE_AUDIT.md) para los resultados de validación."),
        ("line", "### v1.2.0 - Release Candidate", f"### v1.2.0 - {es}"),
        ("line", "**Release Candidate / Pending Publication; sin fecha de publicación.", "**Stable / Validated / Published.** Logging, evidencias y reporting integrados; auditoría y pruebas documentadas en el [informe de release](docs/HITO4_RELEASE_AUDIT.md)."),
    ])
    edit("README_EN.md", [
        ("exact", "| Published stable version | **v1.1.0** |", "| Published stable version | **v1.2.0** |"),
        ("line", "| Release candidate |", "| Current release | **v1.2.0 — Stable / Validated / Published** |"),
        ("line", "| v1.2.0 status |", "| v1.2.0 status | **Stable / Validated / Published** |"),
        ("line", "| v1.2.0 publication date |", f"| v1.2.0 publication date | **{en}** |"),
        ("line", "v1.1.0 is the latest published release", f"v1.2.0 is the latest published release ({en}). It includes SLF4J/Logback logging, automatic failure evidence and Cucumber HTML/JSON reports. Its status is **Stable / Validated / Published**. See the [audit report](docs/HITO4_RELEASE_AUDIT.md) for validation results."),
        ("line", "### v1.2.0 - Release Candidate", f"### v1.2.0 - {en}"),
        ("line", "**Release Candidate / Pending Publication; no publication date.", "**Stable / Validated / Published.** Logging, evidence and reporting are integrated. Validation is recorded in the [release audit](docs/HITO4_RELEASE_AUDIT.md)."),
    ])
    edit("CHANGELOG.md", [
        ("line", "## [Unreleased] — v1.2.0", f"## [1.2.0] - {iso}"),
        ("line", "Milestone 4 Block 4 is under validation.", f"The v1.2.0 release snapshot is prepared for {en} with status **Stable / Validated / Published**. PR validation, tagging and GitHub publication still require confirmation. Logging, automatic failure evidence, reporting and release hardening are included. v1.1.0 was the previous published release."),
        ("line", "### Block 4 — release audit and hardening", "### Block 4 — release audit and hardening (publication controls)"),
        ("exact", "Updated bilingual release documentation and regenerated the PDF manual. No tag or release has been published.", "Included definitive bilingual release documentation and the regenerated PDF manual in the v1.2.0 release snapshot."),
        ("exact", "v1.1.0 remains the published stable version.", "v1.1.0 was the latest published release at the time."),
        ("exact", "`v1.1.0` is the current published stable release.", "`v1.1.0` was the latest published release before `v1.2.0`."),
    ])

    for name, prefix in [
        ("docs/ARCHITECTURE.md", "**Última versión publicada:**"),
        ("docs/LOGGING.md", "**Última versión publicada:**"),
        ("docs/TROUBLESHOOTING.md", "**Última versión publicada:**"),
    ]:
        edit(name, [("line", prefix, f"**Última versión publicada:** v1.2.0 ({es}). Estado: Stable / Validated / Published.")])
    edit("docs/EVIDENCE.md", [
        ("line", "**Estado / Status:**", f"**Estado / Status:** v1.2.0 es la última versión publicada / is the latest published release ({es} / {en}). Stable / Validated / Published."),
    ])
    edit("docs/REPORTING.md", [
        ("line", "**ES:** v1.1.0 sigue siendo la última versión publicada", f"**ES:** v1.2.0 es la última versión publicada ({es}); estado Stable / Validated / Published."),
        ("line", "**EN:** v1.1.0 remains the latest published release", f"**EN:** v1.2.0 is the latest published release ({en}); status Stable / Validated / Published."),
    ])
    edit("docs/GUIA_USO_TEMPLATE_AUTOMATIZACION.md", [
        ("line", "<p align=\"center\"><strong>Automation Template", f"<p align=\"center\"><strong>Automation Template Selenium Java Cucumber</strong><br>Template reutilizable de automatización Web UI<br>v1.2.0 · Stable / Validated / Published · {es}<br>Última versión publicada: v1.2.0<br>Java 21 (predeterminado) / Java 17 (compatible) · Selenium 4.48.0 · Cucumber 7.34.7 · JUnit 5.13.4 · Gradle 8.14.5</p>"),
        ("line", "**Estado técnico y documental.**", f"**Estado técnico y documental.** v1.2.0 es Stable / Validated / Published desde el {es}. Reúne logging, [evidencias automáticas](EVIDENCE.md) y [reporting](REPORTING.md). v1.1.0 es la versión publicada anterior."),
        ("exact", "La versión estable publicada actualmente es v1.1.0.", "La versión estable publicada actualmente es v1.2.0."),
        ("line", "| v1.2.0 |", f"| v1.2.0 | {es} | Release estable | Stable / Validated / Published | Logging con SLF4J/Logback, evidencias automáticas y reporting Cucumber HTML/JSON. Véase [Reporting](REPORTING.md). |"),
        ("line", "**v1.1.0:** **Stable / Validated / Published**", f"**v1.1.0:** versión publicada anterior (1 de octubre de 2026). **v1.2.0:** **Stable / Validated / Published** desde el {es}."),
    ])
    edit("docs/VERSIONING.md", [
        ("line", "v1.1.0 = latest published", "v1.1.0 = previous published stable release (October 1, 2026); Milestone 3 and Blocks 1–4 Completed / Validated"),
        ("line", "v1.2.0 = Release Candidate", f"v1.2.0 = latest published release ({en}); Stable / Validated / Published; release snapshot prepared for tag"),
        ("exact", "`v1.1.0` is the current published stable version.", "`v1.2.0` is the current published stable version."),
        ("exact", "The next version, `v1.2.0`, is a Release Candidate / Pending Publication. Milestone 4 Block 4 still requires PR CI validation.", f"The tagged v1.2.0 documentation is prepared as Stable / Validated / Published ({en}); PR CI and GitHub publication require verification."),
        ("exact", "Block 4 is under validation. No publication date is assigned to `v1.2.0`.", f"Block 4 closure requires the release checks. The planned UTC publication date of `v1.2.0` is {en}."),
    ])
    edit("scripts/create_manual.py", [
        ("exact", "v1.2.0 - Release Candidate / Pending Publication<br/>Fecha de publicación: pendiente<br/>Última versión publicada: v1.1.0 (1 de octubre de 2026)", f"v1.2.0 - Stable / Validated / Published<br/>Fecha de publicación: {es}<br/>Última versión publicada: v1.2.0"),
        ("exact", "('v1.2.0', 'Release Candidate; fecha pendiente', 'Pending Publication. Logging con SLF4J/Logback, evidencias automáticas, reportes HTML/JSON y mejoras de estabilidad. Sin publicación oficial.')", f"('v1.2.0', '{es}', 'Stable / Validated / Published. Logging con SLF4J/Logback, evidencias automáticas, reportes HTML/JSON y mejoras de estabilidad.')"),
        ("exact", "Para el estado actual de v1.2.0, consulte el historial de la página inicial y los README; el tag y GitHub Release aún no existen.", "El historial de la página inicial contiene las fechas de v1.1.0 y v1.2.0. Consulte los README para el estado vigente."),
    ])
    return changed


def verify_transformed(updates: dict[Path, str], day: date) -> None:
    """Check the proposed text before touching any file."""
    names = (
        "README.md", "README_EN.md", "CHANGELOG.md", "docs/ARCHITECTURE.md",
        "docs/EVIDENCE.md", "docs/GUIA_USO_TEMPLATE_AUTOMATIZACION.md",
        "docs/LOGGING.md", "docs/REPORTING.md", "docs/TROUBLESHOOTING.md",
        "scripts/create_manual.py",
    )
    forbidden = re.compile(r"Release Candidate|Pending Publication|fecha pendiente|sin fecha(?: de publicación)?|no publication date|Not set|Sin definir", re.I)
    for name in names:
        body = updates[ROOT / name]
        if forbidden.search(body):
            raise RuntimeError(f"Persistiría un estado provisional en {name}.")
        if "v1.2.0" not in body or "Stable / Validated / Published" not in body:
            raise RuntimeError(f"Falta el estado definitivo en {name}.")
    if spanish_day(day) not in updates[ROOT / "README.md"]:
        raise RuntimeError("Fecha española ausente del README.")
    if english_day(day) not in updates[ROOT / "README_EN.md"]:
        raise RuntimeError("Fecha inglesa ausente del README.")
    if day.isoformat() not in updates[ROOT / "CHANGELOG.md"]:
        raise RuntimeError("Fecha ISO ausente del changelog.")


def redate(day: date) -> dict[Path, str]:
    """Change only the prepared v1.2.0 date, keeping older release history intact."""
    old = PLANNED_DATE
    verify_final(old)
    if day == old:
        return {}
    names = (
        "README.md", "README_EN.md", "CHANGELOG.md", "docs/ARCHITECTURE.md",
        "docs/EVIDENCE.md", "docs/GUIA_USO_TEMPLATE_AUTOMATIZACION.md",
        "docs/LOGGING.md", "docs/REPORTING.md", "docs/TROUBLESHOOTING.md",
        "docs/VERSIONING.md", "docs/RELEASE_PROCESS.md", "scripts/create_manual.py",
    )
    dates = (
        (spanish_day(old), spanish_day(day)),
        (english_day(old), english_day(day)),
        (old.isoformat(), day.isoformat()),
    )
    updates = {}
    for name in names:
        path = ROOT / name
        body = path.read_text(encoding="utf-8")
        revised = body
        for previous, replacement in dates:
            revised = revised.replace(previous, replacement)
        if revised == body:
            raise RuntimeError(f"No se encontró la fecha objetivo anterior en {name}.")
        updates[path] = revised
    audit = ROOT / "docs/HITO4_RELEASE_AUDIT.md"
    updates[audit] = replace_once(
        audit.read_text(encoding="utf-8"),
        f"fecha objetivo UTC {old.isoformat()}",
        f"fecha objetivo UTC {day.isoformat()}",
        str(audit),
    )
    tool = Path(__file__).resolve()
    updates[tool] = replace_once(
        tool.read_text(encoding="utf-8"),
        f"PLANNED_DATE = date({old.year}, {old.month}, {old.day})",
        f"PLANNED_DATE = date({day.year}, {day.month}, {day.day})",
        str(tool),
    )
    return updates


def verify_final(day: date, expected_pdf_hash: bytes | None = None) -> None:
    es, en, iso = spanish_day(day), english_day(day), day.isoformat()
    if not re.search(r"(?m)^version\s*=\s*['\"]1\.2\.0['\"]\s*$", (ROOT / "build.gradle").read_text(encoding="utf-8")):
        raise RuntimeError("build.gradle no identifica la versión 1.2.0.")
    current_files = [
        "README.md", "README_EN.md", "CHANGELOG.md", "docs/ARCHITECTURE.md",
        "docs/EVIDENCE.md", "docs/GUIA_USO_TEMPLATE_AUTOMATIZACION.md",
        "docs/LOGGING.md", "docs/REPORTING.md", "docs/TROUBLESHOOTING.md",
        "scripts/create_manual.py",
    ]
    forbidden = re.compile(r"Release Candidate|Pending Publication|fecha pendiente|sin fecha(?: de publicación)?|no publication date|Not set|Sin definir", re.I)
    stale_latest = re.compile(r"(?:última versión publicada|latest published release|published stable version)[^\n]{0,60}v1\.1\.0|v1\.1\.0 (?:is|es) (?:the |la )?(?:latest|última)", re.I)
    for name in current_files:
        body = (ROOT / name).read_text(encoding="utf-8")
        if forbidden.search(body):
            raise RuntimeError(f"Estado provisional en documento vigente: {name}")
        if stale_latest.search(body):
            raise RuntimeError(f"v1.1.0 figura como última versión publicada en {name}")
        if "v1.2.0" not in body or "Stable / Validated / Published" not in body:
            raise RuntimeError(f"Versión o estado definitivo ausente: {name}")
    checks = {
        "README.md": [es, "| Versión estable publicada | **v1.2.0** |"],
        "README_EN.md": [en, "| Published stable version | **v1.2.0** |"],
        "CHANGELOG.md": [iso, "## [1.2.0]"],
        "docs/GUIA_USO_TEMPLATE_AUTOMATIZACION.md": [es, "Última versión publicada: v1.2.0"],
        "docs/VERSIONING.md": [en, "v1.2.0 = latest published release"],
        "docs/RELEASE_PROCESS.md": [en, "planned UTC publication date"],
        "scripts/create_manual.py": [es, "Última versión publicada: v1.2.0"],
        "docs/ARCHITECTURE.md": [es, "**Última versión publicada:** v1.2.0"],
        "docs/LOGGING.md": [es, "**Última versión publicada:** v1.2.0"],
        "docs/TROUBLESHOOTING.md": [es, "**Última versión publicada:** v1.2.0"],
        "docs/EVIDENCE.md": [es, en],
        "docs/REPORTING.md": [es, en],
    }
    for name, expected in checks.items():
        body = (ROOT / name).read_text(encoding="utf-8")
        if any(item not in body for item in expected):
            raise RuntimeError(f"Fecha/estado inconsistente en {name}: {expected}")
    versioning = (ROOT / "docs/VERSIONING.md").read_text(encoding="utf-8")
    current_context = versioning.split("## Current release context", 1)[1].split("## Version documentation closeout gate", 1)[0]
    if forbidden.search(current_context) or stale_latest.search(current_context):
        raise RuntimeError("El contexto vigente de VERSIONING.md conserva un estado provisional.")
    changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    if "## [Unreleased]" in changelog.split("## [1.1.0]", 1)[0]:
        raise RuntimeError("CHANGELOG.md conserva una sección Unreleased para v1.2.0.")
    line_expectations = {
        "README.md": [
            ("| Fecha de publicación de v1.2.0 |", es),
            ("v1.2.0 es la última versión publicada", es),
            ("### v1.2.0 -", es),
        ],
        "README_EN.md": [
            ("| v1.2.0 publication date |", en),
            ("v1.2.0 is the latest published release", en),
            ("### v1.2.0 -", en),
        ],
        "CHANGELOG.md": [("## [1.2.0] -", iso)],
        "docs/GUIA_USO_TEMPLATE_AUTOMATIZACION.md": [
            ("<p align=\"center\"><strong>Automation Template", es),
            ("**Estado técnico y documental.**", es),
            ("| v1.2.0 |", es),
            ("**v1.1.0:** versión publicada anterior", es),
        ],
        "docs/VERSIONING.md": [("v1.2.0 = latest published release", en)],
        "scripts/create_manual.py": [("story += [Spacer(1, 5.3*cm)", es),
                                     ("        ('v1.2.0',", es)],
    }
    for name, requirements in line_expectations.items():
        lines = (ROOT / name).read_text(encoding="utf-8").splitlines()
        for prefix, expected in requirements:
            matching = [line for line in lines if line.startswith(prefix)]
            if len(matching) != 1 or expected not in matching[0]:
                raise RuntimeError(f"Fecha contradictoria o ausente en {name}, línea {prefix!r}.")
    if not PDF.exists() or not PDF.read_bytes().startswith(b"%PDF-"):
        raise RuntimeError("Falta el manual PDF regenerado.")
    if not EXTERNAL_PDF.exists() or EXTERNAL_PDF.read_bytes() != PDF.read_bytes():
        raise RuntimeError(f"La copia externa del manual no coincide con el PDF versionado: {EXTERNAL_PDF}")
    if expected_pdf_hash is not None and PDF.read_bytes() == expected_pdf_hash:
        raise RuntimeError("El PDF no cambió después de la actualización documental.")
    try:
        from pypdf import PdfReader
    except ImportError as exc:
        raise RuntimeError("Instale pypdf para validar el PDF: python -m pip install pypdf") from exc
    reader = PdfReader(PDF)
    if len(reader.pages) < 15:
        raise RuntimeError("El manual tiene menos páginas de las esperadas.")
    cover = reader.pages[0].extract_text() or ""
    history = reader.pages[1].extract_text() or ""
    if any(term in cover for term in ("Release Candidate", "Pending Publication", "v1.1.0", "pendiente")):
        raise RuntimeError("La portada aún muestra un estado provisional o la versión anterior.")
    if "v1.2.0" not in cover or "Stable / Validated / Published" not in cover:
        raise RuntimeError("La portada del PDF no muestra el release definitivo.")
    if es not in " ".join(cover.split()):
        raise RuntimeError("La portada del PDF no contiene la fecha oficial de publicación.")
    if "v1.2.0" not in history or "Stable / Validated / Published" not in history:
        raise RuntimeError("El historial del PDF no muestra el release definitivo.")
    if "Release Candidate" in history or "Pending Publication" in history:
        raise RuntimeError("El historial del PDF conserva el estado provisional.")
    if es not in " ".join(history.split()):
        raise RuntimeError("El historial del PDF no contiene la fecha oficial de publicación.")
    all_text = "\n".join(page.extract_text() or "" for page in reader.pages)
    for heading in ("13. Captura autom", "14. Generaci", "15. Glosario"):
        if heading not in all_text:
            raise RuntimeError(f"Sección ausente del PDF: {heading}")
def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("stage", "check", "pretag", "postrelease"))
    parser.add_argument("--date", required=True, help="Fecha UTC prevista para published_at (YYYY-MM-DD)")
    args = parser.parse_args()
    planned = date.fromisoformat(args.date)
    if args.command != "stage":
        if planned != PLANNED_DATE:
            raise RuntimeError(f"La fecha solicitada {planned} no coincide con la preparada ({PLANNED_DATE}).")
        verify_final(planned)
        if args.command == "check":
            print(f"Consistencia documental PASS: v1.2.0, {planned} UTC; publicación aún por confirmar.")
            return 0
        if args.command == "pretag":
            today_utc = datetime.now(timezone.utc).date()
            if today_utc != planned:
                raise RuntimeError(f"NO-GO: hoy es {today_utc} UTC, pero la documentación indica {planned}. Actualice fecha y PDF antes del tag.")
            branch = subprocess.check_output(["git", "branch", "--show-current"], cwd=ROOT, text=True).strip()
            if branch != "main" or subprocess.check_output(["git", "status", "--porcelain"], cwd=ROOT):
                raise RuntimeError("NO-GO: pretag exige main limpio con la documentación definitiva integrada.")
            print(f"Pre-tag PASS: documentación definitiva y día UTC {planned} en main limpio.")
            return 0
        official = release_date_from_github()
        if official != planned:
            raise RuntimeError(f"NO-GO: GitHub publicó v1.2.0 el {official} UTC; la documentación indica {planned}.")
        print(f"Post-release PASS: GitHub confirma v1.2.0 publicado el {official} UTC y documentación consistente.")
        return 0
    candidate = "Release Candidate" in (ROOT / "README.md").read_text(encoding="utf-8")
    updates = transform(planned) if candidate else redate(planned)
    if candidate:
        verify_transformed(updates, planned)
    if not updates:
        print(f"Documentación ya preparada para {planned} UTC; no se regeneró el PDF.")
        return 0
    if planned != PLANNED_DATE and candidate:
        tool = Path(__file__).resolve()
        updates[tool] = replace_once(
            tool.read_text(encoding="utf-8"),
            f"PLANNED_DATE = date({PLANNED_DATE.year}, {PLANNED_DATE.month}, {PLANNED_DATE.day})",
            f"PLANNED_DATE = date({planned.year}, {planned.month}, {planned.day})",
            str(tool),
        )
    original = {path: path.read_bytes() for path in updates}
    original[PDF] = PDF.read_bytes() if PDF.exists() else b""
    original[EXTERNAL_PDF] = EXTERNAL_PDF.read_bytes() if EXTERNAL_PDF.exists() else b""
    try:
        for path, body in updates.items():
            path.write_text(body, encoding="utf-8", newline="\n")
        subprocess.run([sys.executable, str(ROOT / "scripts/create_manual.py")], cwd=ROOT, check=True)
        verify_final(planned, original[PDF])
    except Exception:
        for path, content in original.items():
            if path in (PDF, EXTERNAL_PDF) and not content:
                path.unlink(missing_ok=True)
            else:
                path.write_bytes(content)
        raise
    print(f"Snapshot v1.2.0 preparado para {planned} UTC. Revise el PDF y abra el PR del release; GitHub aún debe confirmar la publicación.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (RuntimeError, ValueError, subprocess.CalledProcessError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(1)
