# Milestone 5, Block 4 — v1.3.0 preparation

[Español](../docs/HITO5_BLOCK4_RELEASE_PREPARATION.md) · [Index](README.md)

## Status

- Candidate: **v1.3.0 — Docker & CI Integration**.
- Status: **Release Candidate / Pending Publication**.
- Target date: **12/10/2026 UTC (ISO: 2026-10-12)**. This planning date does not establish publication. It replaces the prior target date; recorded validation dates remain historical evidence.
- From this preparation onward, the official PDFs use the final **Stable / Validated / Published** presentation. Their internal metadata identifies them as prepared-for-distribution artifacts; verify them against the GitHub tag, commit, and `published_at` before attaching them to the release.
- Latest published release: **v1.2.0**, October 8, 2026 at 06:19:01 UTC.

## Prepared scope

The candidate includes the Docker image, the `docker-tests` job, image and execution hardening, and focused evidence collection. `quality-gate` retains the headless Gradle run. The hardening PR and subsequent `main` push recorded both jobs as successful with `test-evidence` and `docker-test-evidence`.

This preparation aligns the Gradle version, README files, changelog, ES/EN technical documentation, PDF manuals, and verifier. It does not create a commit, tag, GitHub Release, push, or merge.

## Debt and limits

- TECH-001 remains OPEN: Selenium 4.48.0 selects CDP 152 against Chrome/CDP 155. Conventional WebDriver tests pass; this does not validate DevTools-dependent features.
- TECH-002 is CLOSED: the runner uses `@SelectPackages("features")` and the recorded validation did not reproduce the former warning.
- apt packages are not pinned through a snapshot; a future uncached build can vary.
- Chrome uses `--no-sandbox` inside the container.

## Preparation validation — 2026-10-09

- `.\gradlew.bat clean test -Dheadless=true --offline`: **PASS — BUILD SUCCESSFUL**. The local Cucumber scenario finished **PASSED**. Chrome/CDP 153 produced the CDP 152 compatibility warning tracked by TECH-001.
- `.\gradlew.bat clean test -Dheadless=false --offline`: **PASS — BUILD SUCCESSFUL**. The local Cucumber scenario finished **PASSED**, with the same CDP 153 → 152 warning.
- `docker build --progress=plain -t selenium-java-cucumber-template:1.3.0-dev .`: **PASS**; `testClasses` completed successfully.
- `docker run --rm --shm-size=2g selenium-java-cucumber-template:1.3.0-dev`: **PASS**; 6/6 tests, one Cucumber scenario, and `BUILD SUCCESSFUL`. The TECH-001 CDP 155 → 152 warning appeared; the former Cucumber selector warning did not.
- Documentation validation: **PASS**, 37 Markdown files, 251 internal links, and zero errors.
- `prepare` verifier: **PASS**.
- `preview` simulation: **PASS**; 26 Markdown documents and both PDFs can transition to published state without writing changes or asserting publication.
- Both PDFs: **PASS**; visual review covered every page.
- The Cucumber/JUnit Platform selector warning did not reappear.

The offline runs establish behavior with dependencies already present in cache; they do not replace a future online dependency-resolution check. Dependencies were not updated.

## Publication

Until the tag and GitHub Release exist, v1.3.0 must remain Release Candidate / Pending Publication and v1.2.0 the latest published release. After authorized publication, `finalize` reads the real `published_at`, updates current documents, and regenerates both PDFs; `postrelease` then compares the tag, UTC date, and documentation state. Candidate PDFs must not be attached to the release. The complete sequence and later diff integration are documented in [RELEASE_PROCESS.md](RELEASE_PROCESS.md).
