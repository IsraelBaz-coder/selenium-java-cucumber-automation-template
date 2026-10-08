# Versioning

[Español](../docs/VERSIONING.md) · [English index](README.md)

This project follows [Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html).

## Format

```text
MAJOR.MINOR.PATCH
```

For example, `1.0.2` was the published documentation-only hotfix version before v1.1.0.

- **MAJOR**: incompatible changes that require consumers to adapt.
- **MINOR**: backward-compatible functionality.
- **PATCH**: backward-compatible fixes and hardening.

## Current release context

```text
v1.0.0 = initial stable baseline
v1.0.1 = Hardening + CI/CD Readiness
v1.0.2 = Documentation-only Hotfix, Stable / Validated / Published
v1.1.0 = previous published stable release (October 1, 2026); Milestone 3 and Blocks 1–4 Completed / Validated
v1.2.0 = latest published release (October 8, 2026, 06:19:01 UTC); Stable / Validated / Published
```

`v1.0.1` was published on 2026-09-25 UTC. `v1.0.2` was published on 2026-09-26 UTC as a documentation-only PATCH. `v1.0.0` was published on 2026-09-18 UTC. `v1.2.0` is the current published stable version.

`v1.1.0` completed Milestone 3: the GitHub Actions workflow, local smoke-test fixture, evidence artifacts, Gradle caching, and required `quality-gate`. Its historical validation covered PASS, controlled FAIL, evidence, restoration, merge, and post-merge PASS. `v1.1.0` was published on October 1, 2026. Milestone 4 added SLF4J/Logback logging, automatic failure evidence, reporting, and release hardening. The [v1.2.0 GitHub Release](https://github.com/IsraelBaz-coder/selenium-java-cucumber-automation-template/releases/tag/v1.2.0) was published on October 8, 2026 at 06:19:01 UTC.

## Version documentation closeout gate

Before closing a future milestone, audit its documentation and release state. The v1.2.0 release audit is preserved in [HITO4_RELEASE_AUDIT.md](HITO4_RELEASE_AUDIT.md). For a future release:

1. Complete the technical work and local validation; prepare documents and manuals in the release branch.
2. Validate the pull request in CI, merge only after required checks pass, and verify a successful post-merge run on `main`.
3. Verify the documented version and date against the intended release before tagging; if the date changes, update all current documents and PDFs together, then repeat review and CI.
4. Publish the approved tag and GitHub Release. Verify its actual `published_at` UTC day against the documentation.
5. Record formal milestone closure only after the GitHub release and tagged documentation are confirmed. Preserve historical audit entries and the immutable tag.

### Publication date completeness rule

Before formal closure of a milestone's final block, define its official publication date and show it consistently on the manual cover, version history, changelog, both README files, usage guide, this policy, release process, and generated PDF. The date must be the same calendar day in every language and format. A milestone cannot be formally closed if any required date is absent, replaced by `TBD`, `Pending`, or `Unreleased`, or contradicted by another document. A defined date does not by itself mean the tag or GitHub Release exists.

### Final manual cover rule

The published release documentation must show the version, final manual cover, version history, and actual UTC publication date consistently. Remove transitional states from current views. Such states may remain in clearly marked historical audit records and process descriptions. Previous versions belong in release history, not on the current cover. Do not move an existing tag to correct a date mismatch.

**Stable / Validated does not mean Published.** The lifecycle is Development / In Progress → technical work Completed → validation completed → Stable / Validated → Ready for Release → Pending Publication → Published. Ready for Release describes technical readiness; Pending Publication describes the period before the tag and GitHub Release exist. The last two pre-publication states can apply at the same time.

Git release tags use the `v` prefix, for example `v1.0.2`. The internal Gradle build version may omit that prefix, for example `1.0.2`.
