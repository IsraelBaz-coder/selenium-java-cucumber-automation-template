"""Single source of truth for v1.3.0 release-document metadata."""

from datetime import datetime, timezone

PROJECT_VERSION = "1.3.0"
RELEASE_TAG = "v1.3.0"
RELEASE_TITLE = "Docker & CI Integration"
RELEASE_NAME = f"{RELEASE_TAG} — {RELEASE_TITLE}"
PREVIOUS_RELEASE = "v1.2.0"
TARGET_DATE = "2026-10-12"
TARGET_DISPLAY = "12/10/2026"
PREPARE_STATUS = "Release Candidate / Pending Publication"
PUBLISHED_STATUS = "Stable / Validated / Published"
RELEASE_URL = (
    "https://github.com/IsraelBaz-coder/"
    "selenium-java-cucumber-automation-template/releases/tag/v1.3.0"
)

MONTHS_ES = (
    "enero", "febrero", "marzo", "abril", "mayo", "junio",
    "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre",
)
MONTHS_EN = (
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
)


def document_metadata(mode, *, publication_date=None, published_at=None):
    """Return normalized prepare or published metadata.

    preview-final accepts a planned date for read-only artifacts. published
    accepts only a confirmed GitHub timestamp supplied by the verified finalizer.
    """
    if mode not in ("prepare", "release-ready", "preview-final", "published"):
        raise ValueError(f"Unsupported documentation mode: {mode}")
    if mode == "prepare":
        if publication_date or published_at:
            raise ValueError("prepare mode does not accept publication metadata")
        instant = datetime.strptime(TARGET_DATE, "%Y-%m-%d").replace(tzinfo=timezone.utc)
        status = PREPARE_STATUS
        confirmed_at = None
    elif mode == "release-ready":
        if publication_date or published_at:
            raise ValueError("release-ready mode uses the centrally configured launch date")
        instant = datetime.strptime(TARGET_DATE, "%Y-%m-%d").replace(tzinfo=timezone.utc)
        status = PUBLISHED_STATUS
        confirmed_at = None
    elif mode == "preview-final":
        if not publication_date or published_at:
            raise ValueError("preview-final mode requires publication_date only")
        instant = datetime.strptime(publication_date, "%Y-%m-%d").replace(tzinfo=timezone.utc)
        status = PUBLISHED_STATUS
        confirmed_at = None
    else:
        if publication_date:
            raise ValueError("published mode accepts confirmed published_at only")
        if published_at:
            instant = datetime.fromisoformat(published_at.replace("Z", "+00:00"))
            if instant.tzinfo is None:
                raise ValueError("published_at must include a timezone")
            instant = instant.astimezone(timezone.utc)
            confirmed_at = instant.strftime("%Y-%m-%dT%H:%M:%SZ")
        else:
            raise ValueError("published mode requires confirmed published_at")
        status = PUBLISHED_STATUS

    return {
        "mode": mode,
        "version": PROJECT_VERSION,
        "tag": RELEASE_TAG,
        "release_title": RELEASE_TITLE,
        "release_name": RELEASE_NAME,
        "status": status,
        "day": instant.date().isoformat(),
        "display": instant.strftime("%d/%m/%Y"),
        "es": f"{instant.day} de {MONTHS_ES[instant.month - 1]} de {instant.year}",
        "en": f"{MONTHS_EN[instant.month - 1]} {instant.day}, {instant.year}",
        "published_at": confirmed_at,
    }
