# Versioning

This project follows [Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html).

## Format

```text
MAJOR.MINOR.PATCH
```

For example, `1.0.2` is the latest published documentation-only hotfix version.

- **MAJOR**: incompatible changes that require consumers to adapt.
- **MINOR**: backward-compatible functionality.
- **PATCH**: backward-compatible fixes and hardening.

## Current release context

```text
v1.0.0 = initial stable baseline
v1.0.1 = Hardening + CI/CD Readiness
v1.0.2 = Documentation-only Hotfix, Stable / Validated / Published; latest published release
v1.1.0 = Stable / Validated; Milestone 3 and Blocks 1–4 Completed / Validated; official publication date October 1, 2026
```

`v1.0.1` was published, tagged, and released on 2026-09-25. `v1.0.2` is the latest published Stable / Validated PATCH containing documentation-only post-release state corrections.

`v1.1.0` completed the technical work and validation for Milestone 3: Block 1 added the base GitHub Actions workflow and a local HTML fixture for the smoke test; Block 2 publishes available reports, results, logs, and screenshots as artifacts; Block 3 added Gradle caching; Block 4 added the stable `quality-gate` check and operational CI/CD documentation. Real GitHub validation covered PASS, controlled FAIL, evidence in both cases, a required check blocking merge, restoration, final PASS, merge, and post-merge PASS on `main`. The active `main` ruleset requires a pull request, an up-to-date branch, and `quality-gate`; it blocks force pushes and deletion. Milestone 3 and Blocks 1–4 are **Completed / Validated**. The current version is **Stable / Validated** with the official publication date **October 1, 2026**. Publication is a separate event: there is no `v1.1.0` tag or GitHub Release yet, so **Published** does not apply. `v1.0.2` remains the latest published release.

## Version documentation closeout gate

Before closing the final block of every milestone, start a mandatory version documentation audit. Technical completion alone does not formally close the milestone. Complete this gate after the technical merge and post-merge CI, before declaring formal documentation closeout:

1. Complete the final technical block and its local validation.
2. Validate the pull request in CI, merge only after required checks pass, and verify a successful post-merge run on `main`.
3. Audit the current version, technical status, milestone status, official publication date, publication status, latest published release, and historical release entries. Check the cover, both README files, usage guide, changelog, this versioning policy, release process, manual source and PDF, and cross references among them.
4. Correct every inconsistent version or status. Regenerate derived documentation, validate links and formatting, review the diff, and merge the documentation closeout through the required pull request process. Verify the final merge and CI result.
5. Complete the documentation gate before creating the tag and GitHub Release. Mark publication **Published** only after both exist; record formal milestone closure after publication and final validation.

### Publication date completeness rule

Before formal closure of a milestone's final block, define its official publication date and show it consistently on the manual cover, version history, changelog, both README files, usage guide, this policy, release process, and generated PDF. The date must be the same calendar day in every language and format. A milestone cannot be formally closed if any required date is absent, replaced by `TBD`, `Pending`, or `Unreleased`, or contradicted by another document. A defined date does not by itself mean the tag or GitHub Release exists.

### Final manual cover rule

After Technical Closeout, Documentation Closeout, and the Version Documentation Audit are complete, the final manual cover, version history, final-state tables, and executive summary show only the current version with **Stable / Validated**, the milestone with **Completed / Validated**, and the official publication date. Remove transitional publication or validation states from these final views, including **In Preparation**, **Pending Validation**, **Ready for Release**, **Pending Release**, and **Pending Publication**. Such states may appear only in operational preparation instructions, not in the final document. The previous published version belongs in the release history, not on the cover. When the tag and GitHub Release exist, update the historical entry to **Stable / Validated / Published**.

**Stable / Validated does not mean Published.** The lifecycle is Development / In Progress → technical work Completed → validation completed → Stable / Validated → Ready for Release → Pending Publication → Published. Ready for Release describes technical readiness; Pending Publication describes the period before the tag and GitHub Release exist. The last two pre-publication states can apply at the same time.

Git release tags use the `v` prefix, for example `v1.0.2`. The internal Gradle build version may omit that prefix, for example `1.0.2`.
