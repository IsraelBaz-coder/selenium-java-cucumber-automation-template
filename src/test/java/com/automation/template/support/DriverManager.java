package com.automation.template.support;

import com.automation.template.driver.DriverFactory;
import org.openqa.selenium.WebDriver;

/**
 * ES:
 * Conserva un WebDriver por hilo para aislar escenarios y delegar su ciclo de vida a los Hooks.
 *
 * EN:
 * Stores one WebDriver per thread to isolate scenarios and delegate lifecycle management to Hooks.
 */
public final class DriverManager {
    private static final ThreadLocal<WebDriver> DRIVERS = new ThreadLocal<>();
    private DriverManager() { }
    /** ES: Crea el driver del escenario. EN: Creates the scenario driver. */
    public static void startDriver() { DRIVERS.set(DriverFactory.createDriver()); }
    /** ES: Devuelve el driver activo. EN: Returns the active driver. */
    public static WebDriver getDriver() {
        WebDriver driver = DRIVERS.get();
        if (driver == null) throw new IllegalStateException("WebDriver was not initialized / WebDriver no fue inicializado.");
        return driver;
    }
    /** ES: Indica si el escenario alcanzó a crear un driver. EN: Indicates whether the scenario created a driver. */
    public static boolean hasDriver() { return DRIVERS.get() != null; }
    /** ES: Cierra y elimina el driver del hilo. EN: Quits and removes the thread driver. */
    public static void quitDriver() {
        WebDriver driver = DRIVERS.get();
        try { if (driver != null) driver.quit(); } finally { DRIVERS.remove(); }
    }
}

