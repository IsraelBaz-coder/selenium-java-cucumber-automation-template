# Versioning

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
v1.2.0 = latest published release (October 8, 2026); Stable / Validated / Published; release snapshot prepared for tag
```

`v1.0.1` was published, tagged, and released on 2026-09-25. `v1.0.2` is a published Stable / Validated PATCH containing documentation-only post-release state corrections. `v1.2.0` is the current published stable version.

`v1.1.0` completed the technical work and validation for Milestone 3: Block 1 added the base GitHub Actions workflow and a local HTML fixture for the smoke test; Block 2 publishes available reports, results, logs, and screenshots as artifacts; Block 3 added Gradle caching; Block 4 added the stable `quality-gate` check and operational CI/CD documentation. Real GitHub validation covered PASS, controlled FAIL, evidence in both cases, a required check blocking merge, restoration, final PASS, merge, and post-merge PASS on `main`. The active `main` ruleset requires a pull request, an up-to-date branch, and `quality-gate`; it blocks force pushes and deletion. Milestone 3 and Blocks 1–4 are **Completed / Validated**. `v1.1.0` is **Stable / Validated / Published** with the official publication date of October 1, 2026. The tagged v1.2.0 documentation is prepared as Stable / Validated / Published (October 8, 2026); PR CI and GitHub publication require verification. Milestone 4 Blocks 1 (SLF4J/Logback logging), 2 (automatic failure evidence), and 3 (reporting consolidation) are **Completed / Validated**; Block 4 closure requires the release checks. The planned UTC publication date of `v1.2.0` is October 8, 2026.

## Version documentation closeout gate

Before closing the final block of every milestone, start a mandatory version documentation audit. Technical completion alone does not formally close the milestone. For v1.2.0, include the definitive documentation in the release PR and tag:

1. Complete the final technical block and local validation; prepare all v1.2.0 documents and the manual in the release branch using `stage --date YYYY-MM-DD`.
2. Validate the pull request in CI, merge only after required checks pass, and verify a successful post-merge run on `main`.
3. Immediately before tagging, run `pretag --date YYYY-MM-DD` on clean `main`. It must match the current UTC day and the complete documentation snapshot. If the day changes, update every current release date and the PDF together before the tag, then repeat review and CI.
4. Publish the approved tag and GitHub Release. Run `postrelease --date YYYY-MM-DD`; its actual `published_at` UTC day and tag must match the tagged documentation.
5. Record formal milestone closure only after the GitHub release and tagged documentation are confirmed. Preserve historical audit entries and the immutable tag.

### Publication date completeness rule

Before formal closure of a milestone's final block, define its official publication date and show it consistently on the manual cover, version history, changelog, both README files, usage guide, this policy, release process, and generated PDF. The date must be the same calendar day in every language and format. A milestone cannot be formally closed if any required date is absent, replaced by `TBD`, `Pending`, or `Unreleased`, or contradicted by another document. A defined date does not by itself mean the tag or GitHub Release exists.

### Final manual cover rule

The release commit and tag must contain the final manual cover, version history, final-state tables, and executive summary showing **Stable / Validated / Published** and the planned UTC publication date. Verify the actual GitHub date after publication. Remove transitional states from current views, including **In Preparation**, **Pending Validation**, **Ready for Release**, **Pending Release**, and **Pending Publication**. Such states may appear in historical audit records and operational instructions. The previous published version belongs in the release history, not on the cover. Do not move an existing tag to correct a date mismatch.

**Stable / Validated does not mean Published.** The lifecycle is Development / In Progress → technical work Completed → validation completed → Stable / Validated → Ready for Release → Pending Publication → Published. Ready for Release describes technical readiness; Pending Publication describes the period before the tag and GitHub Release exist. The last two pre-publication states can apply at the same time.

Git release tags use the `v` prefix, for example `v1.0.2`. The internal Gradle build version may omit that prefix, for example `1.0.2`.
