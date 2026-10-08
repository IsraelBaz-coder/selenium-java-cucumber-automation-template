"""Read-only verifier for the published v1.2.0 documentation snapshot."""
import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
TAG = "v1.2.0"
PDFS = (
    ROOT / "docs/Manual_Template_Automatizacion_Selenium_Java_Cucumber.pdf",
    ROOT / "docs_en/Manual_Selenium_Java_Cucumber_Automation_Template.pdf",
)


def verify(day: str) -> None:
    request = Request(
        "https://api.github.com/repos/IsraelBaz-coder/selenium-java-cucumber-automation-template/releases/tags/v1.2.0",
        headers={"Accept": "application/vnd.github+json", "User-Agent": "selenium-template-doc-check"},
    )
    with urlopen(request, timeout=15) as response:
        release = json.load(response)
    if release["tag_name"] != TAG or release["draft"] or release["prerelease"]:
        raise RuntimeError("v1.2.0 is not a published stable GitHub Release")
    actual = datetime.fromisoformat(release["published_at"].replace("Z", "+00:00")).astimezone(timezone.utc).date().isoformat()
    if actual != day:
        raise RuntimeError(f"GitHub published_at is {actual}, expected {day}")
    tagged_commit = subprocess.check_output(["git", "rev-list", "-n", "1", TAG], cwd=ROOT, text=True).strip()
    if not tagged_commit:
        raise RuntimeError("Local v1.2.0 tag is missing")
    if "version = '1.2.0'" not in (ROOT / "build.gradle").read_text(encoding="utf-8"):
        raise RuntimeError("Gradle version differs from the release")
    for path in (ROOT / "README.md", ROOT / "README_ES.md", ROOT / "README_EN.md", ROOT / "docs/VERSIONING.md", ROOT / "docs_en/VERSIONING.md", ROOT / "CHANGELOG.md"):
        body = path.read_text(encoding="utf-8")
        if "v1.2.0" not in body or "2026" not in body:
            raise RuntimeError(f"Release version or year missing: {path}")
    from pypdf import PdfReader
    for path in PDFS:
        if not path.is_file():
            raise RuntimeError(f"Missing PDF: {path}")
        reader = PdfReader(path)
        if len(reader.pages) < 5:
            raise RuntimeError(f"PDF seems incomplete: {path}")
        cover = reader.pages[0].extract_text() or ""
        if "v1.2.0" not in cover or "Stable / Validated / Published" not in cover:
            raise RuntimeError(f"Release status missing from cover: {path}")
    print(f"PASS: GitHub {TAG} published {release['published_at']}; local tag {tagged_commit[:7]}; both manuals valid")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("check", "postrelease", "stage", "pretag"))
    parser.add_argument("--date", required=True, help="Expected GitHub publication day in UTC (YYYY-MM-DD)")
    args = parser.parse_args()
    if args.command in {"stage", "pretag"}:
        parser.error("v1.2.0 is already published; stage/pretag are no longer applicable")
    verify(args.date)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (RuntimeError, OSError, ValueError, KeyError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
