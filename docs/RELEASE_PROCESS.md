# Release Process

This procedure keeps releases repeatable and traceable. It documents future actions; it does not create a release by itself.

## 1. Work on a branch

Create a focused `feature/*`, `fix/*`, `docs/*`, or `refactor/*` branch from the approved base. Do not make release changes directly on `main`.

## 2. Update code and documentation

Implement only the intended scope. Update documentation, supported configuration, and artifact references when behavior changes.

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

## 8. Prepare the v1.2.0 release snapshot

The planned UTC publication date is **October 8, 2026**. Prepare the definitive README files, changelog, technical documents, manual source and PDF in the same branch and PR that will become the release commit:

```powershell
python scripts/finalize_release_docs.py stage --date 2026-10-08
python scripts/finalize_release_docs.py check --date 2026-10-08
git diff --check
git status --short
```

`stage` updates the candidate fields and regenerates the manual once. `check` validates the date, current status, version history, PDF and its external copy without writing files. The prepared snapshot says **v1.2.0 — Stable / Validated / Published**; that wording is conditional on the approved PR and actual release publication. It is not evidence that GitHub has already published the release. The [reporting contract](REPORTING.md) lists expected CI artifacts. The documentation tooling needs Python with `reportlab` and `pypdf`.

If the intended UTC publication day changes, run `stage --date YYYY-MM-DD` again before the tag. It updates the current release dates together and regenerates the PDF. Review the diff and the PDF again. Historical dates of earlier releases remain unchanged.

## 9. Pre-tag gate and publication

Complete review, obtain a passing PR `quality-gate`, merge, and verify the post-merge run on `main`. Immediately before creating the tag, run from a clean `main` checkout:

```powershell
python scripts/finalize_release_docs.py pretag --date 2026-10-08
```

`pretag` checks that the documented date equals the current **UTC** calendar day and that the definitive documentation is present on clean `main`. A mismatch blocks the tag: change the date jointly, review, merge and validate again. A local October 7 can already be October 8 UTC; GitHub's release `published_at` is checked by UTC day.

With explicit publication authorization, create the immutable tag and GitHub Release using the approved release procedure. Neither `finalize_release_docs.py` nor this documentation creates a commit, push, tag, PR or release automatically. Never move or recreate an existing release tag.

## 10. Post-publication verification

After the GitHub Release is published, run:

```powershell
python scripts/finalize_release_docs.py postrelease --date 2026-10-08
```

`postrelease` requires a published, non-draft, non-prerelease GitHub Release tagged `v1.2.0`; its `published_at` UTC day must match the date in the tagged documentation. If it differs, block Hito 4 closure and report the discrepancy. Preserve the tag's history; resolve any mismatch through an approved corrective release decision. Historical candidate audit records may retain their original state. See [VERSIONING.md](VERSIONING.md#version-documentation-closeout-gate).
