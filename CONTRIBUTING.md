# Contributing

Thank you for helping improve `selenium-java-cucumber-automation-template`. Keep contributions focused, documented, and reproducible.

## Requirements

- Java 21 (default) or Java 17 (minimum supported version).
- The repository's Gradle Wrapper; do not require a globally installed Gradle version.
- Chrome or Edge for browser execution.
- Git.

## Recommended Git flow

```text
main
 |
 +-- feature/*
 +-- fix/*
 +-- docs/*
 +-- refactor/*
```

Create a branch from the current approved base, make a focused change, and open a Pull Request (PR). Avoid direct changes to `main`.

## Commit convention

Use concise Conventional Commit-style messages:

```text
feat(scope): description
fix(scope): description
docs(scope): description
test(scope): description
refactor(scope): description
chore(scope): description
```

Examples:

```text
feat(config): support a configurable timeout
fix(hooks): preserve the original scenario failure
docs(release): explain the versioning policy
test(example): add a tagged smoke scenario
```

## Before opening a Pull Request

Run the required validation from the repository root:

```powershell
.\gradlew.bat clean test
```

Also run the recommended CI-oriented validation:

```powershell
.\gradlew.bat clean test -Dheadless=true
```

Where the change affects scenario selection, validate the relevant tag, for example:

```powershell
.\gradlew.bat clean test -Dheadless=true "-Dcucumber.filter.tags=@example"
```

In the PR, describe the purpose, changes made, commands executed, results, and any relevant evidence. Update documentation whenever behavior, configuration, generated artifacts, or supported execution commands change.

## Repository hygiene and security

- Never commit secrets, credentials, tokens, private URLs, or local environment files.
- Do not add generated reports, screenshots, logs, caches, or other temporary files.
- Keep application-specific test data and configuration outside this reusable template unless it is intentionally neutral and versionable.
- Follow [SECURITY.md](SECURITY.md) for vulnerability reporting and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) for community standards.
