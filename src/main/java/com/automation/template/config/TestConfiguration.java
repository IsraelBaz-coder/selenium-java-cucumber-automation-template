package com.automation.template.config;

import java.io.IOException;
import java.io.InputStream;
import java.util.Properties;

/**
 * ES:
 * Centraliza la configuración del framework. El orden de prioridad es JVM (-D), variable de entorno y archivo de configuración.
 *
 * EN:
 * Centralizes framework configuration. Priority is JVM (-D), environment variable, then configuration file.
 */
public final class TestConfiguration {
    private static final Properties DEFAULTS = loadDefaults();

    private TestConfiguration() { }

    /** ES: Devuelve el navegador efectivo. EN: Returns the effective browser. */
    public static BrowserType browser() { return BrowserType.from(read("browser")); }
    /** ES: Indica la ejecución sin interfaz. EN: Indicates headless execution. */
    public static boolean headless() { return Boolean.parseBoolean(read("headless")); }
    /** ES: Devuelve la URL inicial. EN: Returns the initial URL. */
    public static String baseUrl() { return read("baseUrl"); }
    /** ES: Devuelve el tiempo de espera explícito. EN: Returns the explicit wait timeout. */
    public static long timeoutSeconds() { return Long.parseLong(read("timeoutSeconds")); }
    /** ES: Activa capturas al fallar. EN: Enables screenshots on failure. */
    public static boolean screenshotOnFailure() { return Boolean.parseBoolean(read("screenshotOnFailure")); }

    private static String read(String key) {
        String value = System.getProperty(key);
        if (value == null || value.isBlank()) value = System.getenv(toEnvironmentKey(key));
        if (value == null || value.isBlank()) value = DEFAULTS.getProperty(key);
        if (value == null || value.isBlank()) throw new IllegalStateException("Missing configuration / Falta configuración: " + key);
        return value;
    }

    private static String toEnvironmentKey(String key) {
        return key.replaceAll("([a-z])([A-Z])", "$1_$2").toUpperCase();
    }

    private static Properties loadDefaults() {
        Properties properties = new Properties();
        try (InputStream stream = TestConfiguration.class.getClassLoader().getResourceAsStream("config.properties")) {
            if (stream == null) throw new IllegalStateException("config.properties was not found / no se encontró config.properties.");
            properties.load(stream);
            return properties;
        } catch (IOException exception) {
            throw new IllegalStateException("Unable to load config.properties / no fue posible cargar config.properties.", exception);
        }
    }
}

