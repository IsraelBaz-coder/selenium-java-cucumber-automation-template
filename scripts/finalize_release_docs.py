"""Prepare, preview, apply, and verify v1.3.0 release documentation."""
import argparse
import json
import os
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from release_metadata import (
    PREVIOUS_RELEASE,
    PREPARE_STATUS,
    PROJECT_VERSION,
    PUBLISHED_STATUS,
    RELEASE_NAME,
    RELEASE_TAG,
    RELEASE_URL,
    TARGET_DATE,
    TARGET_DISPLAY,
    document_metadata,
)

ROOT = Path(__file__).resolve().parents[1]
CANDIDATE = RELEASE_TAG
PREPUBLICATION_STATUS = PREPARE_STATUS
PDFS = (
    ROOT / "docs/Manual_Template_Automatizacion_Selenium_Java_Cucumber.pdf",
    ROOT / "docs_en/Manual_Selenium_Java_Cucumber_Automation_Template.pdf",
)
PREPARE_DOCS = tuple(ROOT / item for item in (
    "README.md", "README_ES.md", "README_EN.md", "CHANGELOG.md",
    "docs/README.md", "docs_en/README.md", "docs/VERSIONING.md", "docs_en/VERSIONING.md",
    "docs/RELEASE_PROCESS.md", "docs_en/RELEASE_PROCESS.md",
    "docs/HITO5_BLOCK4_RELEASE_PREPARATION.md", "docs_en/HITO5_BLOCK4_RELEASE_PREPARATION.md",
))
FINAL_DOCS = tuple(ROOT / item for item in (
    "README.md", "README_ES.md", "README_EN.md", "CHANGELOG.md",
    "docs/README.md", "docs/ARCHITECTURE.md", "docs/DOCKER.md", "docs/EVIDENCE.md",
    "docs/GUIA_USO_TEMPLATE_AUTOMATIZACION.md", "docs/LOGGING.md", "docs/RELEASE_PROCESS.md",
    "docs/REPORTING.md", "docs/TECHNICAL_DEBT.md", "docs/TROUBLESHOOTING.md", "docs/VERSIONING.md",
    "docs_en/README.md", "docs_en/ARCHITECTURE.md", "docs_en/DOCKER.md", "docs_en/EVIDENCE.md",
    "docs_en/GUIA_USO_TEMPLATE_AUTOMATIZACION.md", "docs_en/LOGGING.md", "docs_en/RELEASE_PROCESS.md",
    "docs_en/REPORTING.md", "docs_en/TECHNICAL_DEBT.md", "docs_en/TROUBLESHOOTING.md", "docs_en/VERSIONING.md",
))
STALE_PHRASES = (
    "still needs a real GitHub Actions run", "Docker job validation on GitHub remains pending",
    "ejecución de GitHub de este job sigue pendiente",
)
FINAL_STALE_PHRASES = (
    PREPUBLICATION_STATUS,
    "No v1.3.0 release has been made", "v1.3.0 is not published", "v1.3.0 is in development",
    "v1.3.0 no está publicada", "v1.3.0 está en desarrollo", "No publicada.",
    "v1.2.0 remains the latest published", "v1.2.0 remains the latest official",
    "v1.2.0 sigue siendo la última", "v1.2.0 continúa siendo la última",
    "La candidata está Pending Publication", "The candidate is Pending Publication",
    "Target publication date", "No es la fecha real de publicación",
    "Not the actual publication date",
)


def github_release(tag):
    request = Request(
        f"https://api.github.com/repos/IsraelBaz-coder/selenium-java-cucumber-automation-template/releases/tags/{tag}",
        headers={"Accept": "application/vnd.github+json", "User-Agent": "selenium-template-release-check"},
    )
    try:
        with urlopen(request, timeout=15) as response:
            return json.load(response)
    except HTTPError as exc:
        if exc.code == 404:
            return None
        raise


def local_tag_commit(tag):
    result = subprocess.run(
        ["git", "rev-list", "-n", "1", tag], cwd=ROOT, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, check=False,
    )
    return result.stdout.strip() or None


def local_commit(ref):
    result = subprocess.run(
        ["git", "rev-parse", "--verify", f"{ref}^{{commit}}"], cwd=ROOT, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, check=False,
    )
    return result.stdout.strip() or None


def verify_authorized_commit(expected_commit):
    authorized = local_commit(expected_commit)
    if not authorized:
        raise RuntimeError(f"Authorized commit cannot be resolved locally: {expected_commit}")
    tagged = local_tag_commit(CANDIDATE)
    if not tagged:
        raise RuntimeError("Local v1.3.0 tag is missing; fetch tags before finalization")
    if tagged != authorized:
        raise RuntimeError(
            f"v1.3.0 tag commit {tagged} does not match authorized commit {authorized}"
        )
    return tagged


def parse_day(day):
    return datetime.strptime(day, "%Y-%m-%d")


def release_metadata(release):
    if release is None or release.get("draft") or release.get("prerelease"):
        raise RuntimeError("v1.3.0 is not a published stable GitHub Release")
    if release.get("name") != RELEASE_NAME:
        raise RuntimeError(f"GitHub release name is {release.get('name')!r}, expected {RELEASE_NAME!r}")
    if release.get("tag_name") != CANDIDATE:
        raise RuntimeError(f"GitHub release tag is {release.get('tag_name')!r}, expected {CANDIDATE!r}")
    published_at = release.get("published_at")
    if not published_at:
        raise RuntimeError("GitHub Release does not provide published_at")
    return document_metadata("published", published_at=published_at)


def verify_files_exist(paths):
    for path in paths:
        if not path.is_file():
            raise RuntimeError(f"Required document missing: {path.relative_to(ROOT)}")


def verify_common(day, paths):
    parse_day(day)
    if f"version = '{PROJECT_VERSION}'" not in (ROOT / "build.gradle").read_text(encoding="utf-8"):
        raise RuntimeError("build.gradle does not identify version 1.3.0")
    verify_files_exist(paths)
    for path in paths:
        body = path.read_text(encoding="utf-8")
        if CANDIDATE not in body or day not in body:
            raise RuntimeError(f"Version or date missing: {path.relative_to(ROOT)}")
        for phrase in STALE_PHRASES:
            if phrase.lower() in body.lower():
                raise RuntimeError(f"Obsolete CI state in {path.relative_to(ROOT)}: {phrase}")


def verify_release_ready_pdfs(day):
    from pypdf import PdfReader
    for path in PDFS:
        reader = PdfReader(path)
        text = "\n".join((page.extract_text() or "") for page in reader.pages)
        if len(reader.pages) < 5 or CANDIDATE not in text or day not in text or PUBLISHED_STATUS not in text:
            raise RuntimeError(f"Incomplete release-ready metadata in {path.relative_to(ROOT)}")
        forbidden = (PREPUBLICATION_STATUS, "Fecha objetivo", "Target date", "No es la fecha real de publicación", "Not the actual publication date")
        if any(phrase.lower() in text.lower() for phrase in forbidden):
            raise RuntimeError(f"Candidate metadata remains in release-ready PDF: {path.relative_to(ROOT)}")
        subject = str(reader.metadata.get("/Subject", ""))
        if "Release-ready artifact" not in subject:
            raise RuntimeError(f"Release-ready distribution warning missing in PDF metadata: {path.relative_to(ROOT)}")
        if "Block 3:" in text or "Bloque 3:" in text:
            raise RuntimeError(f"Internal Block 3 status remains in user manual: {path.relative_to(ROOT)}")


def verify_prepare(day):
    verify_common(day, PREPARE_DOCS)
    if github_release(CANDIDATE) is not None:
        raise RuntimeError("v1.3.0 already has a GitHub Release; run finalize/postrelease instead")
    if local_tag_commit(CANDIDATE):
        raise RuntimeError("Local v1.3.0 tag exists during preparation")
    for path in PREPARE_DOCS:
        if PREPUBLICATION_STATUS not in path.read_text(encoding="utf-8"):
            raise RuntimeError(f"Pre-publication status missing: {path.relative_to(ROOT)}")
    verify_release_ready_pdfs(day)
    print(f"PASS prepare: v1.3.0 release-ready PDFs target {day} UTC; GitHub publication remains unconfirmed")


def finalized_text(path, original, meta):
    day, display, es_date, en_date = meta["day"], meta["display"], meta["es"], meta["en"]
    text = original
    if path.name == "README.md" and path.parent == ROOT:
        old = "Latest published release / Última versión publicada: **v1.2.0** — **8 October 2026 / 8 de octubre de 2026** ([GitHub Release](https://github.com/IsraelBaz-coder/selenium-java-cucumber-automation-template/releases/tag/v1.2.0)).\n\nRelease candidate / Versión candidata: **v1.3.0 — Docker & CI Integration**. Status / Estado: **Release Candidate / Pending Publication**. Target publication date / Fecha objetivo de publicación: **2026-10-12 UTC**. This target is not the actual publication date / Esta fecha objetivo no es la fecha real de publicación."
        new = f"Latest published release / Última versión publicada: **v1.3.0 — Docker & CI Integration** — **{en_date} / {es_date} UTC** ([GitHub Release]({RELEASE_URL})). Status / Estado: **{PUBLISHED_STATUS}**. GitHub `published_at`: **{meta['published_at']}**."
        text = text.replace(old, new).replace("No v1.3.0 release has been made.", f"GitHub confirms v1.3.0 publication at {meta['published_at']}.")
        text = text.replace("Final candidate validation / Validación final de la candidata:", "Final release validation / Validación final del release:")
    if path.name == "README_ES.md":
        old = "| Versión estable publicada | **v1.2.0** |\n| Versión vigente | **v1.2.0 — Stable / Validated / Published** |\n| Estado de v1.2.0 | **Stable / Validated / Published** |\n| Fecha de publicación de v1.2.0 | **8 de octubre de 2026** |\n| Versión candidata | **v1.3.0 — Docker & CI Integration** |\n| Estado de v1.3.0 | **Release Candidate / Pending Publication** |\n| Fecha objetivo | **2026-10-12 UTC; no es fecha real de publicación** |"
        new = f"| Versión estable publicada | **v1.3.0** |\n| Versión vigente | **v1.3.0 — Docker & CI Integration** |\n| Estado de v1.3.0 | **{PUBLISHED_STATUS}** |\n| Fecha de publicación de v1.3.0 | **{es_date} UTC** |\n| GitHub `published_at` | **{meta['published_at']}** |"
        text = text.replace(old, new)
        text = text.replace("v1.2.0 es la última versión publicada (8 de octubre de 2026). Incorpora logging con SLF4J/Logback, evidencias automáticas ante fallos y reportes Cucumber HTML/JSON. Su estado es **Stable / Validated / Published**. Consulte el [informe de auditoría](docs/HITO4_RELEASE_AUDIT.md) para los resultados de validación.", f"v1.3.0 es la última versión publicada desde el {es_date} UTC; su estado es **{PUBLISHED_STATUS}**. v1.2.0 permanece en el historial como la versión publicada anterior.")
        text = text.replace("La validación final de la candidata confirmó", "La validación final del release confirmó")
        text = text.replace("### v1.3.0 — candidata, fecha objetivo 2026-10-12 UTC", f"### v1.3.0 — publicada {day} UTC")
        text = text.replace("**Release Candidate / Pending Publication.** Dockerización, integración `docker-tests`, hardening y recolección selectiva de evidencias. La fecha indicada es objetivo; v1.2.0 sigue siendo la última versión publicada.", f"**{PUBLISHED_STATUS}.** Dockerización, integración `docker-tests`, hardening y recolección selectiva de evidencias. GitHub confirma la publicación en {meta['published_at']}.")
    if path.name == "README_EN.md":
        old = "| Published stable version | **v1.2.0** |\n| Current release | **v1.2.0 — Stable / Validated / Published** |\n| v1.2.0 status | **Stable / Validated / Published** |\n| v1.2.0 publication date | **October 8, 2026** |\n| Release candidate | **v1.3.0 — Docker & CI Integration** |\n| v1.3.0 status | **Release Candidate / Pending Publication** |\n| Target date | **2026-10-12 UTC; not an actual publication date** |"
        new = f"| Published stable version | **v1.3.0** |\n| Current release | **v1.3.0 — Docker & CI Integration** |\n| v1.3.0 status | **{PUBLISHED_STATUS}** |\n| v1.3.0 publication date | **{en_date} UTC** |\n| GitHub `published_at` | **{meta['published_at']}** |"
        text = text.replace(old, new)
        text = text.replace("v1.2.0 is the latest published release (October 8, 2026). It includes SLF4J/Logback logging, automatic failure evidence and Cucumber HTML/JSON reports. Its status is **Stable / Validated / Published**. See the [audit report](docs_en/HITO4_RELEASE_AUDIT.md) for validation results.", f"v1.3.0 is the latest published release as of {en_date} UTC; its status is **{PUBLISHED_STATUS}**. v1.2.0 remains in the history as the previous published release.")
        text = text.replace("Final candidate validation confirmed", "Final release validation confirmed")
        text = text.replace("### v1.3.0 — candidate, target 2026-10-12 UTC", f"### v1.3.0 — published {day} UTC")
        text = text.replace("**Release Candidate / Pending Publication.** Dockerization, `docker-tests` integration, hardening, and focused evidence collection. The date is a target; v1.2.0 remains the latest published release.", f"**{PUBLISHED_STATUS}.** Dockerization, `docker-tests` integration, hardening, and focused evidence collection. GitHub confirms publication at {meta['published_at']}.")
    if path.name == "CHANGELOG.md":
        text = text.replace("## [1.3.0] — Release Candidate / Pending Publication", f"## [1.3.0] - {day}")
        text = text.replace("Target publication date: **2026-10-12 UTC**. This is a planning value and does not assert that v1.3.0 has been published. v1.2.0 remains the latest published release.", f"The v1.3.0 GitHub Release was published at **{meta['published_at']}** with status **{PUBLISHED_STATUS}**. v1.2.0 is the previous published release.")

    relative = path.relative_to(ROOT).as_posix()
    if relative == "docs/ARCHITECTURE.md":
        text = text.replace(
            "Docker no formaba parte de la versión publicada v1.2.0; la imagen incluida en la candidata v1.3.0 se describe en [Docker](DOCKER.md). La candidata está Pending Publication con fecha objetivo 2026-10-12 UTC.",
            f"Docker no formaba parte de la versión publicada v1.2.0; la imagen incluida en la versión publicada v1.3.0 se describe en [Docker](DOCKER.md). v1.3.0 está {PUBLISHED_STATUS} desde el {es_date} UTC (ISO: {day}).",
        )
    if relative == "docs/README.md":
        text = text.replace("Versión publicada: **v1.2.0**, 8 de octubre de 2026, 06:19:01 UTC ([GitHub Release](https://github.com/IsraelBaz-coder/selenium-java-cucumber-automation-template/releases/tag/v1.2.0)).", f"Versión publicada: **v1.3.0 — Docker & CI Integration**, {es_date} UTC ([GitHub Release]({RELEASE_URL})); **{PUBLISHED_STATUS}**; `published_at` {meta['published_at']}.")
    if relative == "docs_en/README.md":
        text = text.replace("Published release: **v1.2.0**, October 8, 2026, 06:19:01 UTC ([GitHub Release](https://github.com/IsraelBaz-coder/selenium-java-cucumber-automation-template/releases/tag/v1.2.0)).", f"Published release: **v1.3.0 — Docker & CI Integration**, {en_date} UTC ([GitHub Release]({RELEASE_URL})); **{PUBLISHED_STATUS}**; `published_at` {meta['published_at']}.")
    if relative == "docs/GUIA_USO_TEMPLATE_AUTOMATIZACION.md":
        text = text.replace("**Estado técnico y documental.** v1.3.0 está en Release Candidate / Pending Publication con fecha objetivo 2026-10-12 UTC e incorpora Docker, integración CI y [evidencias automáticas](EVIDENCE.md). v1.2.0 continúa como última versión publicada desde el 8 de octubre de 2026.", f"**Estado técnico y documental.** v1.3.0 está {PUBLISHED_STATUS} desde el {es_date} UTC (ISO: {day}) e incorpora Docker, integración CI y [evidencias automáticas](EVIDENCE.md). v1.2.0 es la versión publicada anterior.")
        text = text.replace("La versión estable publicada actualmente es v1.2.0.", "La versión estable publicada actualmente es v1.3.0.")
        text = text.replace("| v1.3.0 | Objetivo 12 de octubre de 2026 UTC | Release candidata | Release Candidate / Pending Publication | Docker, integración CI, hardening y evidencias; aún no publicada. |", f"| v1.3.0 | {es_date} UTC | Release estable | {PUBLISHED_STATUS} | Docker, integración CI, hardening y evidencias. |")
        text = text.replace("**v1.1.0:** versión publicada anterior (1 de octubre de 2026). **v1.2.0:** **Stable / Validated / Published** desde el 8 de octubre de 2026.", f"**v1.2.0:** versión publicada anterior (8 de octubre de 2026). **v1.3.0:** **{PUBLISHED_STATUS}** desde el {es_date} UTC.")
    if relative == "docs_en/GUIA_USO_TEMPLATE_AUTOMATIZACION.md":
        text = text.replace("**Current state:** v1.3.0 is Release Candidate / Pending Publication with a 2026-10-12 UTC target date and includes Docker, CI integration, and automatic [evidence](EVIDENCE.md). [v1.2.0](https://github.com/IsraelBaz-coder/selenium-java-cucumber-automation-template/releases/tag/v1.2.0), published October 8, 2026 at 06:19:01 UTC, remains the latest published release.", f"**Current release:** [v1.3.0]({RELEASE_URL}) is {PUBLISHED_STATUS} as of {en_date} UTC (ISO: {day}) and includes Docker, CI integration, and automatic [evidence](EVIDENCE.md). v1.2.0 is the previous published release.")
        text = text.replace("| v1.3.0 | Target October 12, 2026 UTC | Release Candidate / Pending Publication | Docker, CI integration, hardening, and evidence; not published. |", f"| v1.3.0 | {en_date} UTC | {PUBLISHED_STATUS} | Docker, CI integration, hardening, and evidence. |")
        text = text.replace("v1.2.0 has been Stable / Validated / Published since October 8, 2026.", f"v1.2.0 was the previous published release; v1.3.0 has been {PUBLISHED_STATUS} since {en_date} UTC.")
    if relative == "docs/VERSIONING.md":
        text = text.replace("| v1.3.0 | Release Candidate / Pending Publication; fecha objetivo 2026-10-12 UTC. Docker, integración CI y hardening preparados. No publicada. |", f"| v1.3.0 | Última versión publicada; {es_date} UTC (ISO: {day}); {PUBLISHED_STATUS}. Docker, integración CI y hardening. |")
        text = text.replace("| v1.2.0 | Última versión publicada;", "| v1.2.0 | Versión publicada anterior;")
        text = text.replace("La fecha 2026-10-12 es el objetivo de v1.3.0. Sólo el `published_at` de un GitHub Release real podrá convertirse en fecha oficial.", f"El `published_at` {meta['published_at']} del GitHub Release confirma la fecha oficial de v1.3.0.")
    if relative == "docs_en/VERSIONING.md":
        text = text.replace("v1.2.0 = latest published release (October 8, 2026, 06:19:01 UTC); Stable / Validated / Published", "v1.2.0 = previous published release (October 8, 2026, 06:19:01 UTC); Stable / Validated / Published")
        text = text.replace("v1.3.0 = Release Candidate / Pending Publication; target 2026-10-12 UTC; not published", f"v1.3.0 = latest published release ({en_date} UTC; ISO: {day}); {PUBLISHED_STATUS}")
        text = text.replace("`v1.2.0` is the current published stable version.", "`v1.2.0` is the previous published stable version.")
        text = text.replace("The 2026-10-12 value is the v1.3.0 target. Only the `published_at` timestamp of a real GitHub Release can establish its official publication date.", f"The GitHub Release `published_at` value {meta['published_at']} confirms the official v1.3.0 publication date.")
    if relative == "docs/RELEASE_PROCESS.md":
        text = text.replace("La versión vigente [v1.2.0]", "La versión publicada anterior [v1.2.0]")

    standard = {
        "**Última versión publicada:** v1.2.0 (8 de octubre de 2026). Estado: Stable / Validated / Published.": f"**Última versión publicada:** v1.3.0 ({es_date} UTC; ISO: {day}). Estado: {PUBLISHED_STATUS}.",
        "**Última versión publicada:** v1.2.0 (8 de octubre de 2026). Stable / Validated / Published.": f"**Última versión publicada:** v1.3.0 ({es_date} UTC; ISO: {day}). {PUBLISHED_STATUS}.",
        "**Latest published release:** v1.2.0 (October 8, 2026). Stable / Validated / Published.": f"**Latest published release:** v1.3.0 ({en_date} UTC; ISO: {day}). {PUBLISHED_STATUS}.",
        "**Candidata:** v1.3.0 — Release Candidate / Pending Publication; fecha objetivo 2026-10-12 UTC.": f"**Versión publicada:** v1.3.0 — {PUBLISHED_STATUS}; publicada {es_date} UTC (ISO: {day}).",
        "**Candidate:** v1.3.0 — Release Candidate / Pending Publication; target date 2026-10-12 UTC.": f"**Published release:** v1.3.0 — {PUBLISHED_STATUS}; published {en_date} UTC (ISO: {day}).",
        "v1.2.0 es la última versión publicada (8 de octubre de 2026); estado Stable / Validated / Published.\n\nv1.3.0 es la candidata Release Candidate / Pending Publication, con fecha objetivo 2026-10-12 UTC.": f"v1.3.0 es la última versión publicada ({es_date} UTC; ISO: {day}); estado {PUBLISHED_STATUS}.",
        "Registro aplicable a la candidata v1.3.0 — Release Candidate / Pending Publication; fecha objetivo 2026-10-12 UTC.": f"Registro aplicable a v1.3.0 — {PUBLISHED_STATUS}; publicada {es_date} UTC (ISO: {day}).",
        "Register applicable to the v1.3.0 candidate — Release Candidate / Pending Publication; target date 2026-10-12 UTC.": f"Register applicable to v1.3.0 — {PUBLISHED_STATUS}; published {en_date} UTC (ISO: {day}).",
    }
    for old, new in standard.items():
        text = text.replace(old, new)

    text = text.replace(TARGET_DATE, day).replace(TARGET_DISPLAY, display).replace(PREPUBLICATION_STATUS, PUBLISHED_STATUS)
    phrases = {
        "Versión candidata": "Versión publicada", "Release candidate": "Published release",
        "La candidata v1.3.0": "La versión publicada v1.3.0", "la candidata v1.3.0": "la versión publicada v1.3.0",
        "The v1.3.0 candidate": "The published v1.3.0 release", "the v1.3.0 candidate": "the published v1.3.0 release",
        "v1.3.0 candidate": "published v1.3.0 release", "v1.3.0 continúa como candidata": "v1.3.0 está publicada",
        "v1.3.0 remains a candidate": "v1.3.0 is published", "v1.3.0 es la candidata": "v1.3.0 es la versión publicada",
        "v1.3.0 está en desarrollo": f"v1.3.0 está publicada desde el {es_date} UTC",
        "v1.3.0 is in development": f"v1.3.0 was published on {en_date} UTC",
        "v1.3.0 no está publicada": "v1.3.0 está publicada", "v1.3.0 is not published": "v1.3.0 is published",
        "La candidata está Pending Publication con fecha de publicación": "v1.3.0 está publicada con fecha de publicación",
        "The candidate is Pending Publication with a": "v1.3.0 is published with a",
        "v1.2.0 sigue siendo la última release publicada": "v1.3.0 es la última release publicada",
        "v1.2.0 continúa siendo la última release publicada": "v1.3.0 es la última release publicada",
        "v1.2.0 remains the latest published release": "v1.3.0 is the latest published release",
        "v1.2.0 remains the latest published stable release": "v1.3.0 is the latest published stable release",
        "La última release publicada sigue siendo v1.2.0": "La última release publicada es v1.3.0",
        "Latest published release: v1.2.0": "Latest published release: v1.3.0",
        "Última versión publicada: v1.2.0": "Última versión publicada: v1.3.0",
        "fecha objetivo": "fecha de publicación", "Fecha objetivo": "Fecha de publicación",
        "target date": "publication date", "Target date": "Publication date", "Target publication date": "Publication date",
        "Objetivo ": "Publicada ", "Target ": "Published ", "aún no publicada": "publicada", "not published": "published",
    }
    for old, new in phrases.items():
        text = text.replace(old, new)
    return text


def assert_final_text(path, body, meta):
    if CANDIDATE not in body or PUBLISHED_STATUS not in body or meta["day"] not in body:
        raise RuntimeError(f"Final metadata incomplete in {path.relative_to(ROOT)}")
    for phrase in FINAL_STALE_PHRASES:
        if phrase.lower() in body.lower():
            raise RuntimeError(f"Pre-publication text remains in {path.relative_to(ROOT)}: {phrase}")


def plan_finalization(meta):
    verify_files_exist(FINAL_DOCS)
    changes = {}
    for path in FINAL_DOCS:
        final = finalized_text(path, path.read_text(encoding="utf-8"), meta)
        assert_final_text(path, final, meta)
        changes[path] = final
    return changes


def run_manual_generator(meta, es_output=None, en_output=None, mode="published"):
    command = [sys.executable, str(ROOT / "scripts/create_manual.py"), "--mode", mode]
    if mode == "preview-final":
        command.extend(("--publication-date", meta["day"]))
    else:
        command.extend(("--published-at", meta["published_at"]))
    if es_output:
        command.extend(("--output", str(es_output)))
    if en_output:
        command.extend(("--en-output", str(en_output)))
    environment = None
    if mode == "published":
        environment = os.environ.copy()
        environment["RELEASE_DOCS_VERIFIED"] = "1"
    if subprocess.run(command, cwd=ROOT, env=environment, check=False).returncode:
        raise RuntimeError("PDF manual generation failed")


def verify_published_pdfs(meta, pdfs=PDFS):
    from pypdf import PdfReader
    for path in pdfs:
        reader = PdfReader(path)
        text = "\n".join((page.extract_text() or "") for page in reader.pages)
        if len(reader.pages) < 5 or CANDIDATE not in text or meta["day"] not in text or PUBLISHED_STATUS not in text:
            raise RuntimeError(f"Incomplete published metadata in {path}")
        required = (
            f"Fecha de lanzamiento: {meta['display']}" if path.name.startswith("Manual_Template")
            else f"Release date: {meta['en']}"
        )
        if required not in text:
            raise RuntimeError(f"Published-version label missing in {path}")
        if PREPUBLICATION_STATUS in text or "Latest published release: v1.2.0" in text or "Última versión publicada: v1.2.0" in text:
            raise RuntimeError(f"Candidate metadata remains in {path}")


def preview_finalization(day):
    parse_day(day)
    meta = release_metadata({"tag_name": CANDIDATE, "draft": False, "prerelease": False, "name": RELEASE_NAME, "published_at": f"{day}T00:00:00Z"})
    changes = plan_finalization(meta)
    with tempfile.TemporaryDirectory(prefix="v1.3.0-release-preview-") as folder:
        folder = Path(folder)
        es_pdf, en_pdf = folder / PDFS[0].name, folder / PDFS[1].name
        run_manual_generator(meta, es_pdf, en_pdf, mode="preview-final")
        verify_published_pdfs(meta, (es_pdf, en_pdf))
    print(f"PASS preview-final (read-only): {len(changes)} Markdown files and 2 PDFs can be finalized for {day} UTC; this does not assert publication")


def finalize_from_github(expected_day, expected_commit):
    meta = release_metadata(github_release(CANDIDATE))
    if meta["day"] != expected_day:
        print(
            f"WARNING: GitHub published_at day is {meta['day']}, planned {expected_day}; "
            "using the confirmed GitHub UTC date"
        )
    tagged_commit = verify_authorized_commit(expected_commit)
    changes = plan_finalization(meta)
    for path, body in changes.items():
        path.write_text(body, encoding="utf-8", newline="")
    run_manual_generator(meta)
    verify_published_pdfs(meta)
    subprocess.run([sys.executable, str(ROOT / "scripts/validate_docs.py")], cwd=ROOT, check=True)
    print(f"PASS finalize: documentation and PDFs updated from GitHub published_at {meta['published_at']}; authorized tag commit {tagged_commit[:7]}; no commit, tag, release, or upload was created")


def verify_postrelease(expected_day, expected_commit):
    meta = release_metadata(github_release(CANDIDATE))
    if meta["day"] != expected_day:
        print(
            f"WARNING: GitHub published_at day is {meta['day']}, planned {expected_day}; "
            "verifying the confirmed GitHub UTC date"
        )
    tagged_commit = verify_authorized_commit(expected_commit)
    verify_common(meta["day"], FINAL_DOCS)
    for path in FINAL_DOCS:
        assert_final_text(path, path.read_text(encoding="utf-8"), meta)
    verify_published_pdfs(meta)
    print(f"PASS postrelease: v1.3.0 published {meta['published_at']}; local tag {tagged_commit[:7]}; final PDFs verified")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("prepare", "preview-final", "finalize", "postrelease"))
    parser.add_argument("--date", help="Target/expected UTC day (YYYY-MM-DD)")
    parser.add_argument("--expected-commit", help="Authorized commit SHA or ref; required for finalize/postrelease")
    args = parser.parse_args()
    if not args.date:
        parser.error(f"--date is required for {args.command}")
    if args.command in ("finalize", "postrelease") and not args.expected_commit:
        parser.error(f"--expected-commit is required for {args.command}")
    if args.command in ("prepare", "preview-final") and args.expected_commit:
        parser.error(f"--expected-commit is not valid for {args.command}")
    if args.command == "prepare":
        verify_prepare(args.date)
    elif args.command == "preview-final":
        preview_finalization(args.date)
    elif args.command == "finalize":
        parse_day(args.date)
        finalize_from_github(args.date, args.expected_commit)
    else:
        parse_day(args.date)
        verify_postrelease(args.date, args.expected_commit)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (RuntimeError, OSError, ValueError, KeyError, subprocess.CalledProcessError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
