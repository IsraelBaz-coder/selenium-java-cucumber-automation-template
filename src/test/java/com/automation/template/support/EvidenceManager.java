package com.automation.template.support;

import io.cucumber.java.Scenario;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardOpenOption;
import java.time.Clock;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.UUID;
import org.openqa.selenium.OutputType;
import org.openqa.selenium.TakesScreenshot;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.remote.RemoteWebDriver;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/** ES: Captura, guarda y adjunta evidencia de fallos. EN: Captures, stores and attaches failure evidence. */
public final class EvidenceManager {
    private static final Logger LOGGER = LoggerFactory.getLogger(EvidenceManager.class);
    private static final DateTimeFormatter TIMESTAMP = DateTimeFormatter.ofPattern("yyyyMMdd_HHmmss_SSS");
    private final Path directory;
    private final Clock clock;

    public EvidenceManager() { this(Path.of("build", "evidence", "screenshots"), Clock.systemDefaultZone()); }

    EvidenceManager(Path directory, Clock clock) {
        this.directory = directory;
        this.clock = clock;
    }

    public void captureFailure(Scenario scenario, WebDriver driver) {
        String name = scenario.getName();
        if (driver == null || driver instanceof RemoteWebDriver remote && remote.getSessionId() == null) {
            LOGGER.warn("Cannot capture failure screenshot because WebDriver is unavailable for scenario '{}'.", name);
            return;
        }
        if (!(driver instanceof TakesScreenshot screenshotDriver)) {
            LOGGER.warn("WebDriver does not support screenshots for failed scenario '{}'.", name);
            return;
        }

        byte[] image;
        try {
            LOGGER.info("Capturing failure screenshot for scenario '{}'.", name);
            image = screenshotDriver.getScreenshotAs(OutputType.BYTES);
            if (image == null || image.length == 0) {
                LOGGER.warn("WebDriver returned an empty screenshot for scenario '{}'.", name);
                return;
            }
        } catch (RuntimeException exception) {
            LOGGER.warn("Screenshot capture failed for scenario '{}': {}", name, exception.getClass().getSimpleName());
            return;
        }

        try {
            Files.createDirectories(directory);
            Path file = directory.resolve(fileName(name, clock));
            Files.write(file, image, StandardOpenOption.CREATE_NEW);
            LOGGER.info("Failure screenshot saved at {}", file.toAbsolutePath());
        } catch (IOException | SecurityException exception) {
            LOGGER.warn("Screenshot file could not be saved for scenario '{}': {}", name, exception.getClass().getSimpleName());
        }

        try {
            scenario.attach(image, "image/png", "failure-screenshot");
            LOGGER.info("Failure screenshot attached to Cucumber scenario '{}'.", name);
        } catch (RuntimeException exception) {
            LOGGER.warn("Screenshot attachment failed for scenario '{}': {}", name, exception.getClass().getSimpleName());
        }
    }

    static String fileName(String scenarioName, Clock clock) {
        String safe = scenarioName.replaceAll("[^A-Za-z0-9._-]+", "_")
                .replaceAll("^[._-]+|[._-]+$", "");
        if (safe.isBlank()) safe = "failed_scenario";
        if (safe.length() > 80) safe = safe.substring(0, 80).replaceAll("[._-]+$", "");
        return safe + "_" + TIMESTAMP.format(LocalDateTime.now(clock)) + "_" + UUID.randomUUID() + ".png";
    }
}
