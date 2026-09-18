package com.automation.template.pages;

import com.automation.template.config.TestConfiguration;
import java.time.Duration;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

/**
 * ES:
 * Page Object de ejemplo neutral para demostrar el patrón POM. Sustitúyalo por páginas de la aplicación bajo prueba.
 *
 * EN:
 * Neutral example Page Object that demonstrates POM. Replace it with pages from the application under test.
 */
public final class ExampleDomainPage {
    private static final By HEADING = By.cssSelector("h1");
    private final WebDriver driver;
    private final WebDriverWait wait;

    /** ES: Asocia el Page Object al driver del escenario. EN: Associates this Page Object with the scenario driver. */
    public ExampleDomainPage(WebDriver driver) {
        this.driver = driver;
        this.wait = new WebDriverWait(driver, Duration.ofSeconds(TestConfiguration.timeoutSeconds()));
    }

    /** ES: Navega a la URL base configurada. EN: Navigates to the configured base URL. */
    public ExampleDomainPage open() {
        driver.get(TestConfiguration.baseUrl());
        wait.until(ExpectedConditions.visibilityOfElementLocated(HEADING));
        return this;
    }

    /** ES: Comprueba el encabezado visible. EN: Checks the visible heading. */
    public boolean hasHeading(String expectedHeading) {
        return wait.until(ExpectedConditions.visibilityOfElementLocated(HEADING))
                .getText().equalsIgnoreCase(expectedHeading);
    }
}

