package com.automation.template.steps;

import static org.junit.jupiter.api.Assertions.assertTrue;

import com.automation.template.pages.ExampleDomainPage;
import com.automation.template.support.DriverManager;

import io.cucumber.java.es.Dado;
import io.cucumber.java.es.Entonces;

/**
 * ES:
 * Steps de ejemplo que muestran cómo mantener Gherkin separado de Selenium y de los localizadores.
 *
 * EN:
 * Example steps that show how to keep Gherkin separate from Selenium and locators.
 */
public final class ExampleDomainSteps {

    private ExampleDomainPage page;

    /**
     * ES: Abre la aplicación configurada.
     * EN: Opens the configured application.
     */
    @Dado("que el usuario abre la aplicación de ejemplo")
    public void openApplication() {
        page = new ExampleDomainPage(DriverManager.getDriver());
        page.open();
    }

    /**
     * ES: Verifica un encabezado funcional.
     * EN: Verifies a functional heading.
     */
    @Entonces("se muestra el encabezado {string}")
    public void verifyHeading(String heading) {
        assertTrue(
            page.hasHeading(heading),
            () -> "Expected heading was not displayed / No se mostró el encabezado esperado: " + heading
        );
    }
}