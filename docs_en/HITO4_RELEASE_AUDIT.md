# Milestone 4 release audit

[Español — complete historical audit](../docs/HITO4_RELEASE_AUDIT.md) · [English index](README.md)

**Current confirmed state:** the `v1.2.0` tag and [GitHub Release](https://github.com/IsraelBaz-coder/selenium-java-cucumber-automation-template/releases/tag/v1.2.0) were published on October 8, 2026 at 06:19:01 UTC. Status: **Stable / Validated / Published**.

## Historical audit context

The Spanish source records a local Windows/Java 21 audit performed on October 7 before publication. At that point v1.2.0 was a release candidate and v1.1.0 was the latest published release. Those descriptions are historical evidence and must not be read as the current release state.

The audit covered logging, failure screenshots, Cucumber HTML/JSON reporting, the Gradle version, headless and visible local runs, controlled failure evidence, and documentation checks. It recorded Chrome CDP compatibility and Cucumber feature-selector warnings without test failure; TLS and CI validation limitations were tracked separately. Its acceptance matrix and decision were a prepublication gate, not a postpublication claim.

## Technical findings from October 7

Java, Gradle, Selenium, Cucumber, JUnit Platform and POM remained in place. `RunCucumberTest` produced HTML and JSON; Logback wrote to console and `build/logs/automation.log`; hooks captured evidence before releasing WebDriver. The smoke test used a local fixture. No dependency version changed. The project version was corrected from `1.0.2` to `1.2.0`.

Two driver lifecycle fixes were recorded: `DriverFactory` closes a visible browser if `maximize()` fails while retaining the original exception, and `DriverManager` rejects a second initialization in the same thread. The historical generator also synchronized a parent-directory copy of the Spanish PDF; the current generator writes the Spanish and English manuals inside the repository.

## Reproducible results recorded then

| Check | Historical result | Evidence or limit |
|---|---|---|
| `.\gradlew.bat clean test -Dheadless=true` | BLOCKED | Maven Central metadata for `io.cucumber:query` failed with TLS `PKIX path building failed` before compilation. |
| Headless run with `--offline` | PASS | JUnit/Cucumber smoke and HTML, JSON, XML and logs generated. |
| Visible run with `--offline` | PASS | Chrome visible smoke passed. |
| Controlled `@release-evidence` failure | Mechanism PASS | Expected Gradle exit 1, 13,239-byte PNG, `image/png` JSON attachment, FAILED status and capture logs; temporary feature removed. |
| Final headless suite | PASS | Successful build after temporary feature removal; no failure PNG. |
| PR CI for that candidate | BLOCKED | No authorized PR/push yet at the audit date; workflow inspected statically. |

The audit observed a Chrome CDP 153 versus Selenium-supported CDP 152 warning and a Cucumber warning that the `features` resource selector should be a package selector. Neither failed the local tests. A dependency update was deferred for separate evaluation.

## Historical acceptance matrix

| Criterion | Historical result | Evidence or boundary |
|---|---|---|
| CA-01 Structure | PASS | Main contains config, driver, page; test contains hooks, runner, steps, support, feature and fixture. |
| CA-02 Dependencies/compatibility | BLOCKED | Java 21 worked from cache; Java 17 and fresh Maven resolution were not run. |
| CA-03 Logging | PASS | Logback configuration and generated `automation.log`. |
| CA-04 Automatic evidence | PASS | Controlled failure PNG, attachment, log and driver close. |
| CA-05 Cucumber reporting | PASS | HTML/JSON for smoke and controlled failure in their respective runs. |
| CA-06 Headless | PASS offline | Full cached suite successful; exact online command blocked by TLS. |
| CA-07 Visible browser | PASS offline | Full cached suite successful. |
| CA-08 Security/`.gitignore` | PASS | Tracked source/config review found no embedded credentials; runtime output ignored. |
| CA-09 CI/CD | BLOCKED | Workflow defined headless `quality-gate` and `if: always()` upload; no candidate PR run yet. |
| CA-10 Documentation | PASS | Bilingual README, guide and technical documents reviewed as they stood then. |
| CA-11 Spanish PDF | PASS | A4, 20 pages, key pages visually inspected. |
| CA-12 Candidate | PASS at that time | Gradle version `1.2.0`; tag, release and official date did not yet exist. |

The historical risks were the local Java certificate/proxy chain, missing remote PR check, untested Java 17 runtime, two nonfatal warnings, and an unrelated untracked `output/` directory. The decision was GO to prepare a PR with authorization and NO-GO for publication until the remaining checks. Its checklist showed completed local code/security/logging/reporting and cached tests, while fresh dependency resolution, remote PR checks, post-merge CI and the official date were pending.

## Historical documentation audit

The October 7 audit covered both READMEs, guide, architecture, logging, evidence, reporting, troubleshooting, versioning, release process, changelog, manual and generator. At that time it checked 81 local Markdown links with no missing target or anchor, extracted the 20-page A4 PDF, visually inspected all pages at contact-sheet scale and key pages at readable scale, and kept release-management terms out of the user manual. These results describe the earlier snapshot.

| ID | Historical result | What was checked |
|---|---|---|
| DOC-01 | PASS | Manual explains setup, execution and diagnosis with PowerShell examples. |
| DOC-02 | PASS | Milestone-management terms removed from manual source and extracted PDF. |
| DOC-03 | PASS | Block-management terms removed; chapters 13 and 14 have functional titles. |
| DOC-04 | PASS | No Sprint terminology in manual. |
| DOC-05 | PASS | Chapter 13 covers capture conditions, PNG, attachment, failure and privacy. |
| DOC-06 | PASS | Chapter 14 covers formats, paths, commands, interpretation, CI and limits. |
| DOC-07 | PASS | Index, architecture, stack, CI, logging and troubleshooting reviewed. |
| DOC-08 | PASS then | Candidate cover showed pending date and previous published v1.1.0; now superseded by published v1.2.0 cover. |
| DOC-09 | PASS then | Version history v1.0.0-v1.2.0 checked for that snapshot. |
| DOC-10 | PASS then | Spanish README capabilities and audit link. |
| DOC-11 | PASS then | English README technical contract and candidate status. |
| DOC-12 | PASS then | Architecture, logging, evidence, reporting and diagnosis against code. |
| DOC-13 | PASS | Changelog, versioning and audit preserve older release history. |
| DOC-14 | PASS | Java 17/21, Gradle 8.14.5, Selenium 4.48.0, Cucumber 7.34.7, JUnit 5.13.4, SLF4J 2.0.20, Logback 1.6.5 checked. |
| DOC-15 | PASS | Python generator produced the manual with warnings treated as errors. |
| DOC-16 | PASS | 20-page A4 Spanish PDF generated. |
| DOC-17 | PASS | Contact sheet and enlarged key pages showed no clipping or overflow. |
| DOC-18 | PASS | 81 local links checked; external links were outside that check. |
| DOC-19 | PASS | Glossary retained and GitHub entry corrected. |
| DOC-20 | PASS then | Post-release sequence described; execution still pending on October 7. |
| DOC-21 | PASS then | Candidate date was pending rather than invented; later replaced with official GitHub date. |
| DOC-22 | PASS | Native Cucumber plugins, Logback, EvidenceManager and CI outputs matched the implementation. |

## Historical transition and release integrity

The recorded PowerShell sequence ran headless and visible tests, checked the diff and status, then proposed staging, committing, pushing and opening a PR only after authorization. It subsequently called for `quality-gate`, post-merge CI, publication and a final documentation audit. That sequence was a plan, not proof of publication. The original candidate wording occurred in README, changelog, technical document headers, manual cover/history and versioning; these locations are now normalized for the published release, while the [Spanish source](../docs/HITO4_RELEASE_AUDIT.md) keeps the original audit evidence.

## Release integrity

The published version is `v1.2.0`, matching `build.gradle` version `1.2.0`. The publication timestamp comes from GitHub's `published_at`, rather than the tagger date or a planned date. The original audit remains unchanged below its added current-state banner in Spanish so the prepublication sequence, checks, risks, and decisions stay available for review.
