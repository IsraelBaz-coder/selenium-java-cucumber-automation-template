package com.automation.template.hooks;

import com.automation.template.config.TestConfiguration;
import com.automation.template.support.DriverManager;
import com.automation.template.support.EvidenceManager;
import io.cucumber.java.After;
import io.cucumber.java.Before;
import io.cucumber.java.Scenario;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/** ES: Gestiona el ciclo del escenario. EN: Manages the scenario lifecycle. */
public final class Hooks {
    private static final Logger LOGGER = LoggerFactory.getLogger(Hooks.class);
    private final EvidenceManager evidence = new EvidenceManager();

    @Before public void startBrowser(Scenario scenario) {
        LOGGER.info("Starting scenario: {}", scenario.getName());
        LOGGER.info("Scenario configuration: browser={}, headless={}",
                TestConfiguration.browser(), TestConfiguration.headless());
        DriverManager.startDriver();
    }

    @After public void finishScenario(Scenario scenario) {
        try {
            LOGGER.info("Finished scenario: {}, status={}", scenario.getName(), scenario.getStatus());
            if (scenario.isFailed()) {
                LOGGER.info("Failure detected for scenario '{}'.", scenario.getName());
                if (TestConfiguration.screenshotOnFailure()) evidence.captureFailure(scenario, DriverManager.currentDriver());
            }
        } finally {
            DriverManager.quitDriver();
        }
    }
}
