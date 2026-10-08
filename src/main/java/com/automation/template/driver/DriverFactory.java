package com.automation.template.driver;

import com.automation.template.config.BrowserType;
import com.automation.template.config.TestConfiguration;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;
import org.openqa.selenium.chromium.ChromiumOptions;
import org.openqa.selenium.edge.EdgeDriver;
import org.openqa.selenium.edge.EdgeOptions;

/**
 * ES:
 * Crea WebDriver con opciones consistentes para los navegadores soportados.
 *
 * EN:
 * Creates WebDriver with consistent options for supported browsers.
 */
public final class DriverFactory {
    private static final Logger LOGGER = LoggerFactory.getLogger(DriverFactory.class);
    private DriverFactory() { }

    /**
     * ES: Crea el driver para la configuración efectiva del escenario.
     * EN: Creates the driver for the scenario's effective configuration.
     * @return ES: driver listo para la prueba. EN: driver ready for the test.
     */
    public static WebDriver createDriver() {
        BrowserType browser = TestConfiguration.browser();
        boolean headless = TestConfiguration.headless();
        LOGGER.debug("Creating {} WebDriver with headless={}", browser, headless);
        WebDriver driver = switch (browser) {
            case CHROME -> createChrome(headless);
            case EDGE -> createEdge(headless);
        };
        try {
            if (!headless) driver.manage().window().maximize();
        } catch (RuntimeException exception) {
            try {
                driver.quit();
            } catch (RuntimeException closeException) {
                exception.addSuppressed(closeException);
            }
            throw exception;
        }
        LOGGER.info("WebDriver initialized successfully.");
        return driver;
    }

    private static WebDriver createChrome(boolean headless) {
        ChromeOptions options = new ChromeOptions();
        configure(options, headless);
        // ES: Los flags del contenedor no alteran la ejecución local.
        // EN: Container flags do not change local execution.
        if (Boolean.parseBoolean(System.getenv("AUTOMATION_CONTAINER"))) {
            options.addArguments("--no-sandbox", "--disable-dev-shm-usage");
        }
        return new ChromeDriver(options);
    }

    private static WebDriver createEdge(boolean headless) {
        EdgeOptions options = new EdgeOptions();
        configure(options, headless);
        return new EdgeDriver(options);
    }

    private static void configure(ChromiumOptions<?> options, boolean headless) {
        options.addArguments("--disable-notifications");
        if (headless) {
            options.addArguments("--headless=new", "--window-size=1920,1080");
        }
    }

}

