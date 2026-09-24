package com.automation.template.hooks;

import com.automation.template.config.TestConfiguration;
import com.automation.template.logging.FrameworkLogger;
import com.automation.template.support.DriverManager;
import io.cucumber.java.After;
import io.cucumber.java.Before;
import io.cucumber.java.Scenario;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardOpenOption;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.UUID;
import java.util.logging.Level;
import java.util.logging.Logger;
import org.openqa.selenium.OutputType;
import org.openqa.selenium.TakesScreenshot;

/**
 * ES:
 * Gestiona el ciclo de vida del navegador y adjunta capturas a escenarios fallidos.
 *
 * EN:
 * Manages browser lifecycle and attaches screenshots to failed scenarios.
 */
public final class Hooks {
    private static final Logger LOGGER = FrameworkLogger.getLogger(Hooks.class);
    private static final DateTimeFormatter EVIDENCE_TIMESTAMP = DateTimeFormatter.ofPattern("yyyyMMdd_HHmmss_SSS");

    /** ES: Inicia el navegador antes del escenario. EN: Starts the browser before the scenario. */
    @Before public void startBrowser(Scenario scenario) {
        LOGGER.info("Starting scenario: " + scenarioName(scenario));
        DriverManager.startDriver();
    }

    /** ES: Guarda evidencia si falla y cierra el navegador. EN: Saves evidence on failure and closes the browser. */
    @After public void finishScenario(Scenario scenario) {
        try {
            String state = scenario.isFailed() ? "FAIL" : "PASS";
            LOGGER.info(() -> "Finished scenario: " + scenarioName(scenario) + ", status=" + state);
            if (scenario.isFailed() && TestConfiguration.screenshotOnFailure()) capture(scenario);
        } finally { DriverManager.quitDriver(); }
    }

    private void capture(Scenario scenario) {
        String name = scenarioName(scenario);
        if (!DriverManager.hasDriver()) {
            LOGGER.severe("Cannot capture failure screenshot because WebDriver is unavailable for scenario '" + name + "'.");
            return;
        }
        byte[] image;
        try {
            if (!(DriverManager.getDriver() instanceof TakesScreenshot screenshotDriver)) {
                LOGGER.severe("WebDriver does not support screenshots for failed scenario '" + name + "'.");
                return;
            }
            LOGGER.info("Capturing failure screenshot for scenario '" + name + "'.");
            image = screenshotDriver.getScreenshotAs(OutputType.BYTES);
        } catch (RuntimeException exception) {
            LOGGER.log(Level.SEVERE, "Failed to capture screenshot for scenario '" + name + "'.", exception);
            return;
        }
        attachScreenshot(scenario, name, image);
        persistScreenshot(name, image);
    }

    private void attachScreenshot(Scenario scenario, String name, byte[] image) {
        try {
            scenario.attach(image, "image/png", "failure-screenshot");
            LOGGER.info("Attached failure screenshot to Cucumber scenario '" + name + "'.");
        } catch (RuntimeException exception) {
            LOGGER.log(Level.SEVERE, "Failed to attach screenshot to Cucumber scenario '" + name + "'.", exception);
        }
    }

    private void persistScreenshot(String name, byte[] image) {
        try {
            Path folder = Path.of("build", "evidence", "screenshots");
            Files.createDirectories(folder);
            String filename = safeFileName(name) + "_" + EVIDENCE_TIMESTAMP.format(LocalDateTime.now())
                    + "_" + UUID.randomUUID() + ".png";
            Path evidence = folder.resolve(filename);
            Files.write(evidence, image, StandardOpenOption.CREATE_NEW);
            LOGGER.info("Failure screenshot persisted at " + evidence.toAbsolutePath());
        } catch (IOException | SecurityException exception) {
            LOGGER.log(Level.SEVERE, "Failed to persist screenshot for scenario '" + name + "'.", exception);
        }
    }

    private String scenarioName(Scenario scenario) {
        return scenario.getName();
    }

    private String safeFileName(String name) {
        String sanitized = name.replaceAll("[^a-zA-Z0-9._-]+", "_").replaceAll("^_+|_+$", "");
        return sanitized.isBlank() ? "failed_scenario" : sanitized;
    }
}

