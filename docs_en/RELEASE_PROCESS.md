# Release Process

[Español](../docs/RELEASE_PROCESS.md) · [English index](README.md)

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

## 8. Verify publication state

For an already published version, compare the local tag, Gradle version and GitHub Release `published_at` timestamp. `v1.2.0` was published on October 8, 2026 at 06:19:01 UTC: [official release](https://github.com/IsraelBaz-coder/selenium-java-cucumber-automation-template/releases/tag/v1.2.0). Its original preparation and prepublication checks remain in [the historical audit](HITO4_RELEASE_AUDIT.md). Do not rerun its release staging commands or change its tag.

For a future version, prepare both language versions, changelog and generated manuals in the release branch. Confirm the actual date after GitHub publishes the release. A planned date alone never establishes publication. The documentation verifier can inspect v1.2.0 read-only with `python scripts/finalize_release_docs.py check --date 2026-10-08`.

## 9. Release integrity

Before any future publication, complete PR review, required `quality-gate`, merge and post-merge verification. Publish only through the approved process. After publication, verify tag identity and GitHub `published_at`; record the confirmed date consistently in both languages and PDFs. Keep old audit records and tags intact. See [versioning](VERSIONING.md).