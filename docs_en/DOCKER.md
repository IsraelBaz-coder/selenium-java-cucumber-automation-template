# Docker: Windows user guide

[Español](../docs/DOCKER.md) · [Index](README.md) · [Technical debt](TECHNICAL_DEBT.md)

**Status:** Docker is a development capability for v1.3.0. v1.2.0 remains the latest published release. With the LF rule fixed in the local working tree, Codex ran `docker build --no-cache --progress=plain -t selenium-java-cucumber-template:1.3.0-clone-test .` and `docker run --rm selenium-java-cucumber-template:1.3.0-clone-test`: both succeeded, with Example Domain PASSED and BUILD SUCCESSFUL. This correction has not yet been published to GitHub.

## Download the project from GitHub

1. Install [Git for Windows](https://git-scm.com/download/win). Open **PowerShell** from Start and check the installation:

   ~~~powershell
   git --version
   ~~~

2. Clone the **source code** into the current folder and enter the new directory:

   ~~~powershell
   git clone https://github.com/IsraelBaz-coder/selenium-java-cucumber-automation-template.git
   Set-Location .\selenium-java-cucumber-automation-template
   git fetch origin
   git branch -r
   ~~~

3. Select a **published** ref that includes Docker. When `git branch -r` lists `origin/feature/hito-5-docker-base`, run `git switch --track origin/feature/hito-5-docker-base`. If you select another branch or version, check for all three files before proceeding:

   ~~~powershell
   Test-Path .\Dockerfile
   Test-Path .\gradlew
   Test-Path .\build.gradle
   git check-attr eol -- gradlew
   ~~~

   All three `Test-Path` commands must return `True`, and Git must show `gradlew: eol: lf`. The Docker branch is published, but commit `3ba7245` lacks this rule and may convert `gradlew` to CRLF during a Windows clone. **Until the `.gitattributes` correction is published, a clean clone of that commit may fail to build.** Request a published revision with the LF rule before continuing; a clone of `main` does not provide this workflow either.

4. With Docker Desktop running, **build the image locally** using `docker build --progress=plain -t selenium-java-cucumber-template:1.3.0-dev .`. Then **run the tests** and retain results on Windows:

   ~~~powershell
   New-Item -ItemType Directory -Force .\build | Out-Null
   $out = (Resolve-Path .\build).Path
   $bind = "type=bind,source=$out,target=/home/automation/app/build"
   docker run --rm --mount $bind selenium-java-cucumber-template:1.3.0-dev
   Test-Path .\build\reports\cucumber\cucumber.html
   Invoke-Item .\build\reports\cucumber\cucumber.html
   ~~~

   Expect `BUILD SUCCESSFUL` and `True`; also inspect `build/reports/tests/test/`, `build/logs/automation.log`, and, if failures produced screenshots, `build/evidence/screenshots/`. Detailed steps and troubleshooting follow.

**Three separate operations:** `git clone` downloads source code; `docker build` creates an image on your computer from that source; `docker pull` would download a previously built image from a registry. There is no published and verified prebuilt image for this block, so the documented route is a local build after obtaining a Docker-enabled ref.

## What Docker does and what the image contains

Docker runs the framework in a Linux container isolated from the JDK and browser installed on Windows. It helps reproduce the same test environment across machines. The image contains Temurin Java 21, Chrome and ChromeDriver 155.0.8059.39, Gradle Wrapper 8.14.5, Selenium, Cucumber, JUnit, and POM. The Dockerfile targets Linux amd64, works in /home/automation/app, and runs as user automation (UID 10001). Tests use headless Chrome; Edge is not installed. Neither Selenium Grid nor Docker-based CI is included. Base image and browser versions are pinned; Ubuntu packages downloaded during an uncached build can change with the repository.

~~~text
GitHub (source code) → Windows PowerShell → Docker Desktop / WSL2 → Linux container
                                      → Gradle Wrapper → JUnit/Cucumber
                                      → Selenium WebDriver → Chrome
                                      → build/ (reports, log, evidence)
~~~

*Illustrative architecture diagram; it is not a screenshot of a test run.*

## 1. Prepare Windows and check the engine

- **Goal:** make a Linux Docker engine available.
- **Requirements:** a Docker Desktop compatible Windows system, enabled virtualization, configured WSL2, and installed Docker Desktop. The first build needs network access.
- **Action and PowerShell commands:** open **Docker Desktop** from Start, wait until the engine is running, and select Linux containers. Open PowerShell and run:

~~~powershell
wsl --status
docker version
docker info
~~~

- **Explanation:** wsl --status checks WSL; docker version and info must show both Client and Server. Client alone is insufficient.
- **Expected result:** Server identifies Docker Desktop, linux/amd64, and an available engine.
- **Recognize an error:** “failed to connect to the docker API” or no Server indicates a stopped daemon; WSL errors indicate its distribution or platform is not ready.
- **Resolution:** start or restart Docker Desktop, wait for the running state, confirm Linux mode, and rerun the commands. For WSL2 problems, run `wsl --update`, restart Windows if requested, and consult Docker Desktop/WSL diagnostics.

## 2. Open PowerShell in the repository root

- **Goal:** use this repository's Dockerfile and Gradle Wrapper.
- **Requirements:** a downloaded repository and PowerShell.
- **PowerShell commands:** after cloning and selecting a Docker-enabled ref:

~~~powershell
Get-Location
Test-Path .\Dockerfile
Test-Path .\gradlew
Test-Path .\build.gradle
~~~

- **Explanation:** the final dot in the build command uses this folder as its context.
- **Expected result:** all three Test-Path commands return True.
- **Recognize an error:** False or “path not found” indicates the wrong directory.
- **Resolution:** navigate to the folder containing Dockerfile, gradlew, and build.gradle.

## 3. Build the image

- **Goal:** create the development image from the source.
- **Requirements:** steps 1 and 2, plus access to Temurin, Chrome, ChromeDriver, Gradle, and Maven Central downloads.
- **PowerShell command:**

~~~powershell
docker build --progress=plain -t selenium-java-cucumber-template:1.3.0-dev .
~~~

- **Explanation:** --progress=plain prints full build steps; -t sets the name and tag; the final dot selects the current context. The Dockerfile compiles test classes with the existing Wrapper and does not install another Gradle.
- **Expected result:** the build ends without ERROR and tags selenium-java-cucumber-template:1.3.0-dev. Codex verified an uncached build of the local correction with the 1.3.0-clone-test tag.
- **Recognize an error:** nonzero exit code, ERROR in download, installation, or Gradle, or no daemon connection.
- **Resolution:** check engine, network/proxy, and certificates, then retry. For TLS/PKIX, inspect the JDK trust store and corporate proxy; do not disable TLS. For a download failure, check the logged URL and connection before changing dependencies.

## 4. Verify Java, Chrome, and ChromeDriver

- **Goal:** inspect versions actually included in the image.
- **Requirements:** built image.
- **PowerShell commands:**

~~~powershell
docker run --rm selenium-java-cucumber-template:1.3.0-dev java -version
docker run --rm selenium-java-cucumber-template:1.3.0-dev google-chrome --version
docker run --rm selenium-java-cucumber-template:1.3.0-dev chromedriver --version
docker run --rm selenium-java-cucumber-template:1.3.0-dev ./gradlew --version
~~~

- **Explanation:** docker run creates a temporary container; --rm removes it on exit. The final arguments replace the default test command.
- **Expected result:** Temurin 21.0.12 LTS (21.0.12.1 in the inspected image), Chrome and ChromeDriver 155.0.8059.39, and Gradle 8.14.5. Codex ran all four commands successfully against the existing image.
- **Recognize an error:** image or command not found, or differing Chrome/ChromeDriver versions.
- **Resolution:** rebuild from the repository root with the correct tag; confirm Dockerfile pins CHROME_VERSION and both binaries report the same version. Do not change project dependencies to hide a browser mismatch.

## 5. Run tests and interpret results

- **Goal:** run the suite with headless Chrome.
- **Requirements:** built image; the example scenario uses a local HTML fixture.
- **PowerShell command:**

~~~powershell
docker run --rm selenium-java-cucumber-template:1.3.0-dev
~~~

- **Explanation:** without extra arguments, the image runs ./gradlew --no-daemon test. --rm removes the container on exit; without a mount, its build/ files disappear with it.
- **Expected result:** WebDriver initialized successfully, Example Domain PASSED, and BUILD SUCCESSFUL. The user reported this and Codex reproduced it during mount validation.
- **Recognize an error:** BUILD FAILED, a red Cucumber step, WebDriver exception, or nonzero exit code. WARN alone does not mean failure.
- **Resolution:** inspect the first actual error and Gradle summary. Chrome and ChromeDriver should match. The current CDP and Cucumber selector warnings did not fail the validated smoke test; they remain open as [TECH-001 and TECH-002](TECHNICAL_DEBT.md), with no Selenium or runner change in this block.

## 6. Keep reports, logs, and evidence

- **Goal:** retain build/ output on Windows after --rm.
- **Requirements:** available image, Docker Desktop access to the folder, and write permissions for user automation (UID 10001).
- **PowerShell commands verified by Codex with this image:**

~~~powershell
New-Item -ItemType Directory -Force .\build | Out-Null
docker run --rm --mount "type=bind,source=$((Get-Location).Path)\build,target=/home/automation/app/build" selenium-java-cucumber-template:1.3.0-dev
Test-Path .\build\reports\cucumber\cucumber.html
Test-Path .\build\reports\cucumber\cucumber.json
Test-Path .\build\logs\automation.log
~~~

- **Explanation:** --mount binds host build/ to container build/. --rm removes the container, not host files. Codex verified HTML, JSON, Gradle HTML, JUnit XML, and a log on Windows. The screenshot folder was absent because the scenario passed; persistence of a real failure PNG has not been validated here.
- **Expected result:** BUILD SUCCESSFUL and True from the three Test-Path commands. Also inspect build/reports/tests/test/ and build/test-results/test/. Eligible screenshots would be under build/evidence/screenshots/.
- **Recognize an error:** “permission denied,” --mount failure, or False after a run that produced reports.
- **Resolution:** confirm the path with Get-Location, Docker Desktop folder sharing, and write permissions. Keep the Dockerfile UID; do not switch to root to bypass a permission problem without investigation. Review reports and screenshots for sensitive data before sharing.

## Warnings and common problems

| Symptom | Diagnosis and resolution |
|---|---|
| Docker daemon unavailable / stopped Docker Desktop | Repeat `docker version` and `docker info`; start Docker Desktop, wait for Server, and confirm Linux mode. |
| WSL2 unavailable | Run `wsl --status` and `wsl --update`; check virtualization and restart if Windows requests it. |
| Failed build downloads | Run `docker build --progress=plain -t selenium-java-cucumber-template:1.3.0-dev .`; check the failing step's URL and network/proxy. |
| Gradle TLS/PKIX | Inspect JDK certificates, TLS interception, and proxy; do not disable TLS or change versions without diagnosis. |
| Permission denied in build/ | Check Windows folder access and UID 10001 write permission; rerun the verified mount. |
| Different Chrome/ChromeDriver versions | Run both --version commands, rebuild, and confirm CHROME_VERSION=155.0.8059.39. |
| `./gradlew: not found` on Linux although it exists | Check `git check-attr eol -- gradlew`: it must report `lf`. A CRLF checkout turns `#!/bin/sh` into `#!/bin/sh\r`, so Linux cannot find the interpreter. Use a revision containing `.gitattributes` with `gradlew text eol=lf` and clone again; `chmod +x` alone does not fix line endings. |
| CDP 155 → 152 WARN | See [TECH-001](TECHNICAL_DEBT.md); the smoke test passed, but DevTools features need later regression checks. |
| features selector WARN | See [TECH-002](TECHNICAL_DEBT.md); the current scenario was discovered and passed. |

**States:** implemented = Dockerfile and guides exist; validated here = described image inspection and mounted test; pending = TECH-001/002 resolution and persistence of a real failure screenshot. Block 1 remains open pending authorization to close it.
