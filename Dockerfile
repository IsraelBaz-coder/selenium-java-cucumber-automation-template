FROM eclipse-temurin:21.0.12.1_1-jdk-jammy

# Pin Chrome and ChromeDriver to the same published version.
ARG TARGETARCH
ARG CHROME_VERSION=155.0.8059.39
RUN test "${TARGETARCH:-amd64}" = "amd64" \
    && apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates curl unzip \
    && curl -fsSLo /tmp/google-chrome.deb "https://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_${CHROME_VERSION}-1_amd64.deb" \
    && apt-get install -y --no-install-recommends /tmp/google-chrome.deb \
    && curl -fsSLo /tmp/chromedriver.zip "https://storage.googleapis.com/chrome-for-testing-public/${CHROME_VERSION}/linux64/chromedriver-linux64.zip" \
    && unzip -q /tmp/chromedriver.zip -d /tmp/chromedriver \
    && install -m 0755 /tmp/chromedriver/chromedriver-linux64/chromedriver /usr/local/bin/chromedriver \
    && rm -rf /tmp/google-chrome.deb /tmp/chromedriver.zip /tmp/chromedriver \
    && rm -rf /var/lib/apt/lists/*

ENV HEADLESS=true \
    AUTOMATION_CONTAINER=true \
    GRADLE_USER_HOME=/home/automation/.gradle

RUN useradd --create-home --uid 10001 --shell /bin/bash automation \
    && mkdir -p /home/automation/app \
    && chown automation:automation /home/automation/app
WORKDIR /home/automation/app

COPY --chown=automation:automation gradlew build.gradle settings.gradle ./
COPY --chown=automation:automation gradle ./gradle
COPY --chown=automation:automation src ./src
RUN chmod +x ./gradlew

USER automation
RUN ./gradlew --no-daemon testClasses

CMD ["./gradlew", "--no-daemon", "test"]
