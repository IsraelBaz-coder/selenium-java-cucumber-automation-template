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

## 8. Complete the documentation closeout and version audit

Begin the documentation audit before closing the final technical block. After technical completion and a successful post-merge CI run on `main`, perform the mandatory version audit. Define the official publication date, then update the cover, version history, changelog, both README files, guide, versioning policy, release process, manual source, and PDF with the same calendar date. Regenerate the PDF and review it visually. Check the current version, technical and milestone states, publication state, latest published release, and cross references. Validate links and formatting, review the diff, and submit the documentation PR. Merge it only with a passing required check, then verify the final CI result. In the final cover, version history, final-state tables, and manual summary, show **Stable / Validated**, **Completed / Validated**, and the official publication date without transitional release states. During operational preparation, the version may be Ready for Release or Pending Publication; those terms do not mean **Published**. See [VERSIONING.md](VERSIONING.md#version-documentation-closeout-gate).

**Publication date completeness rule:** Do not formally close a milestone when its date is missing, `TBD`, `Pending`, or `Unreleased`, or when the cover, history, changelog, README files, guide, and PDF disagree. For v1.1.0, the official date recorded in documentation is **October 1, 2026**. Defining this date does not create the tag or GitHub Release.

## 9. Create a tag

After the documentation merge and final CI, create the release tag. For example, the following is documentation only and uses a future placeholder version:

```powershell
git tag -a vX.Y.Z -m "Release vX.Y.Z"
```

## 10. Publish the GitHub Release

Create the GitHub Release only after the tag exists. Derive release notes from `CHANGELOG.md`, verify links and artifacts, and never include secrets in release notes or attachments. Mark the version **Published** only after the GitHub Release exists.

## 11. Record formal milestone closure

After publication and final validation, record formal milestone closure. The sequence is technical completion → post-merge CI → documentation closeout → version audit → official publication date → documentation update and PDF visual review → documentation PR and merge → final CI → tag → GitHub Release → Published → formal milestone closure.

For the current v1.2.0 development branch, Milestone 4 and the version remain In Development. Blocks 1, 2 and 3 are Completed / Validated; later blocks are Pending. Cucumber JSON is a validated Block 3 output. No publication date is assigned. See the [reporting contract](REPORTING.md).
