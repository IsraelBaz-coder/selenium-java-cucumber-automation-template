package com.automation.template.config;

import java.util.Locale;

/**
 * ES:
 * Enumera los navegadores soportados por la capa de drivers.
 *
 * EN:
 * Lists the browsers supported by the driver layer.
 */
public enum BrowserType {
    CHROME,
    EDGE;

    /**
     * ES: Convierte texto de configuración en un navegador soportado, sin distinguir mayúsculas.
     * EN: Converts configuration text into a supported browser without case sensitivity.
     *
     * @param value ES: nombre configurado. EN: configured name.
     * @return ES: navegador equivalente. EN: matching browser.
     */
    public static BrowserType from(String value) {
        try {
            return valueOf(value.trim().toUpperCase(Locale.ROOT));
        } catch (IllegalArgumentException exception) {
            throw new IllegalArgumentException("Unsupported browser / Navegador no soportado: " + value, exception);
        }
    }
}

