package com.automation.template.driver;

import com.automation.template.config.BrowserType;
import com.automation.template.config.TestConfiguration;
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
    private DriverFactory() { }

    /**
     * ES: Crea el driver para la configuración efectiva del escenario.
     * EN: Creates the driver for the scenario's effective configuration.
     * @return ES: driver listo para la prueba. EN: driver ready for the test.
     */
    public static WebDriver createDriver() {
        WebDriver driver = switch (TestConfiguration.browser()) {
            case CHROME -> createChrome(TestConfiguration.headless());
            case EDGE -> createEdge(TestConfiguration.headless());
        };
        if (!TestConfiguration.headless()) driver.manage().window().maximize();
        return driver;
    }

    private static WebDriver createChrome(boolean headless) {
        ChromeOptions options = new ChromeOptions();
        configure(options, headless);
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

