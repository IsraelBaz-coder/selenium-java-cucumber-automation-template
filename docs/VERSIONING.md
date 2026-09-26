# Versioning

This project follows [Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html).

## Format

```text
MAJOR.MINOR.PATCH
```

For example, `1.0.2` is the current documentation-only hotfix version.

- **MAJOR**: incompatible changes that require consumers to adapt.
- **MINOR**: backward-compatible functionality.
- **PATCH**: backward-compatible fixes and hardening.

## Current release context

```text
v1.0.0 = initial stable baseline
v1.0.1 = Hardening + CI/CD Readiness
v1.0.2 = Documentation-only Hotfix, Stable / Validated
```

`v1.0.1` was published, tagged, and released on 2026-09-25. `v1.0.2` is the current Stable / Validated PATCH containing documentation-only post-release state corrections.

Git release tags use the `v` prefix, for example `v1.0.2`. The internal Gradle build version may omit that prefix, for example `1.0.2`.
