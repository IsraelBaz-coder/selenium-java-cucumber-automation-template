package com.automation.template.hooks;

import com.automation.template.config.TestConfiguration;
import com.automation.template.support.DriverManager;
import io.cucumber.java.After;
import io.cucumber.java.Before;
import io.cucumber.java.Scenario;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
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
    /** ES: Inicia el navegador antes del escenario. EN: Starts the browser before the scenario. */
    @Before public void startBrowser() { DriverManager.startDriver(); }

    /** ES: Guarda evidencia si falla y cierra el navegador. EN: Saves evidence on failure and closes the browser. */
    @After public void finishScenario(Scenario scenario) {
        try {
            if (scenario.isFailed() && TestConfiguration.screenshotOnFailure() && DriverManager.hasDriver()) capture(scenario);
        } finally { DriverManager.quitDriver(); }
    }

    private void capture(Scenario scenario) {
        byte[] image = ((TakesScreenshot) DriverManager.getDriver()).getScreenshotAs(OutputType.BYTES);
        scenario.attach(image, "image/png", "failure-screenshot");
        try {
            Path folder = Path.of("build", "screenshots");
            Files.createDirectories(folder);
            String safeName = scenario.getName().replaceAll("[^a-zA-Z0-9._-]", "_");
            Files.write(folder.resolve(safeName + ".png"), image);
        } catch (IOException ignored) {
            // ES: La evidencia adjunta a Cucumber sigue disponible aunque falle el archivo local.
            // EN: Evidence attached to Cucumber remains available if local-file writing fails.
        }
    }
}

