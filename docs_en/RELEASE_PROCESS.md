# Release Process

[Español](../docs/RELEASE_PROCESS.md) · [English index](README.md)

This procedure keeps releases repeatable and traceable. It documents future actions; it does not create a release by itself.

The current candidate is **v1.3.0 — Docker & CI Integration**, Release Candidate / Pending Publication, with a **2026-10-12 UTC** target date. The target date does not establish publication; v1.2.0 remains the latest published release.

## 1. Work on a branch

Create a focused `feature/*`, `fix/*`, `docs/*`, or `refactor/*` branch from the approved base. Do not make release changes directly on `main`.

## 2. Update code and documentation

Implement only the intended scope. Update documentation, supported configuration, and artifact references when behavior changes. Before publication, regenerate both official PDFs with `python scripts/create_manual.py --mode release-ready`. That final presentation is marked internally as prepared for distribution and must be checked against GitHub before attachment. The `published` mode is reserved for the verified `finalize_release_docs.py` flow.

## 3. Update `CHANGELOG.md`

Record the relevant, user-visible changes under the version being prepared. Do not describe an unreleased version as published.

## 4. Run validation

Run the baseline validation:

```powershell
.\gradlew.bat clean test
```

Then run the CI-oriented validation:

```powershell
.\gradlew.bat clean test -Dheadless=true
```

When scenario selection is affected, validate the supported filter too:

```powershell
.\gradlew.bat clean test -Dheadless=true "-Dcucumber.filter.tags=@example"
```

The GitHub Actions workflow at `.github/workflows/ci.yml` executes `./gradlew clean test -Dheadless=true`. On Windows, use `.\gradlew.bat clean test -Dheadless=true` for the equivalent local command. The supported framework properties are `browser`, `headless`, `baseUrl`, `timeoutSeconds`, and `screenshotOnFailure`; Cucumber receives `cucumber.filter.tags`. Use their uppercase environment-variable equivalents where supported. `javaVersion` is selected through Gradle with `-PjavaVersion=17` or `-PjavaVersion=21`. The workflow attempts to upload real generated outputs as `test-evidence`: Gradle test report (`build/reports/tests/test/`), JUnit XML (`build/test-results/test/`), Cucumber HTML and JSON (`build/reports/cucumber/`), screenshots (`build/evidence/screenshots/`), and logs (`build/logs/automation.log`). The artifact does not change the job result: a `0` exit code is successful; a non-zero exit code fails the job.

## 5. Review the repository

```powershell
git status
git diff
```

Confirm that no secrets, local files, generated artifacts, or unintended changes are included.

## 6. Create a Pull Request

The PR must include its purpose, changes made, tests executed, results, and relevant evidence.

For a PR targeting `main`, wait for the GitHub Actions `quality-gate` check. A failed check requires a fix and another push before merge. Inspect **Checks → quality-gate → Details** and download `test-evidence` from **Actions** when available. The active `main` ruleset requires a pull request, an up-to-date branch, and a passing `quality-gate` check; it also blocks force pushes and branch deletion.

## 7. Merge

Merge only after the review and validations have been completed, including a successful `quality-gate` check for a PR targeting `main`.

## 8. Prepare and finalize v1.3.0

For an already published version, compare the local tag, Gradle version and GitHub Release `published_at` timestamp. `v1.2.0` was published on October 8, 2026 at 06:19:01 UTC: [official release](https://github.com/IsraelBaz-coder/selenium-java-cucumber-automation-template/releases/tag/v1.2.0). Its original preparation and prepublication checks remain in [the historical audit](HITO4_RELEASE_AUDIT.md). Do not rerun its release staging commands or change its tag.

Before merge, run `python scripts/finalize_release_docs.py prepare --date 2026-10-12` and `python scripts/finalize_release_docs.py preview-final --date 2026-10-12`. `preview-final` transforms the current documents in memory, checks that no active candidate metadata remains, and creates both final PDFs in a temporary directory; it does not write to the repository or establish publication.

Exact post-merge order:

1. Confirm that `main` contains the approved commit and that `quality-gate` and `docker-tests` passed.
2. Create and publish the authorized tag and GitHub Release named `v1.3.0 — Docker & CI Integration`. Do not attach the candidate PDFs.
3. Confirm that GitHub exposes `published_at`, then run `git fetch --tags` so the tag exists locally.
4. Identify the full SHA of the commit authorized by the merge. Run `python scripts/finalize_release_docs.py finalize --date 2026-10-12 --expected-commit <AUTHORIZED_SHA>`. It reads the real GitHub Release, rejects drafts and prereleases, validates the release name and tag, compares `published_at` with October 12 UTC, and checks that the tag points to the authorized commit. It then updates the current README files, changelog, and ES/EN technical documentation, and regenerates both PDFs as Stable / Validated / Published. If GitHub records a different UTC day, it reports the discrepancy and uses the confirmed actual date. It creates no commit, tag, release, or upload.
5. Run `python scripts/validate_docs.py` and `python scripts/finalize_release_docs.py postrelease --date 2026-10-12 --expected-commit <AUTHORIZED_SHA>`. Visually inspect both PDF covers and version histories.
6. Integrate the post-release diff through the mechanism allowed by `main` protection. If `main` requires a Pull Request, this integration requires a PR; do not bypass the ruleset or declare Published before GitHub.
7. Upload only the finalized PDFs: `gh release upload v1.3.0 docs/Manual_Template_Automatizacion_Selenium_Java_Cucumber.pdf docs_en/Manual_Selenium_Java_Cucumber_Automation_Template.pdf --clobber`.
8. Download both release assets, compare them with the local PDFs, and run `postrelease` again before closing Milestone 5.

Because `published_at` exists only after publication, the prepublication commit cannot truthfully contain Published status and the real date. This procedure limits the later correction to one controlled intervention and preserves historical reports.

## 9. Release integrity

Before any future publication, complete PR review, required `quality-gate`, merge and post-merge verification. Publish only through the approved process. After publication, verify tag identity and GitHub `published_at`; record the confirmed date consistently in both languages and PDFs. Keep old audit records and tags intact. See [versioning](VERSIONING.md).
