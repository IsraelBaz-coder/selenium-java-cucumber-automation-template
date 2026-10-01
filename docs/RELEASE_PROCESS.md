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

The GitHub Actions workflow at `.github/workflows/ci.yml` executes `./gradlew clean test -Dheadless=true`. On Windows, use `.\gradlew.bat clean test -Dheadless=true` for the equivalent local command. The supported framework properties are `browser`, `headless`, `baseUrl`, `timeoutSeconds`, and `screenshotOnFailure`; Cucumber receives `cucumber.filter.tags`. Use their uppercase environment-variable equivalents where supported. `javaVersion` is selected through Gradle with `-PjavaVersion=17` or `-PjavaVersion=21`. The workflow attempts to upload real generated outputs as `test-evidence`: Gradle test report (`build/reports/tests/test/`), JUnit XML (`build/test-results/test/`), Cucumber HTML (`build/reports/cucumber/cucumber.html`), screenshots (`build/evidence/screenshots/`), and logs (`build/logs/automation.log`). The artifact does not change the job result: a `0` exit code is successful; a non-zero exit code fails the job.

## 5. Review the repository

```powershell
git status
git diff
```

Confirm that no secrets, local files, generated artifacts, or unintended changes are included.

## 6. Create a Pull Request

The PR must include its purpose, changes made, tests executed, results, and relevant evidence.

## 7. Merge

Merge only after the required review and validations have been completed.

## 8. Create a tag

After the merge, create the release tag. For example, the following is documentation only and uses a future placeholder version:

```powershell
git tag -a vX.Y.Z -m "Release vX.Y.Z"
```

## 9. Publish the GitHub Release

Create the GitHub Release only after the tag exists. Derive release notes from `CHANGELOG.md`, verify links and artifacts, and never include secrets in release notes or attachments.
