package com.automation.template.logging;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.logging.ConsoleHandler;
import java.util.logging.FileHandler;
import java.util.logging.Formatter;
import java.util.logging.Handler;
import java.util.logging.Level;
import java.util.logging.LogRecord;
import java.util.logging.Logger;

/** Configures concise console and artifact logging for the template. */
public final class FrameworkLogger {
    private static final Object LOCK = new Object();
    private static volatile boolean configured;

    private FrameworkLogger() { }

    public static Logger getLogger(Class<?> type) {
        configure();
        return Logger.getLogger(type.getName());
    }

    private static void configure() {
        if (configured) return;
        synchronized (LOCK) {
            if (configured) return;
            Logger root = Logger.getLogger("");
            for (Handler handler : root.getHandlers()) root.removeHandler(handler);
            Formatter formatter = new CompactFormatter();
            ConsoleHandler console = new ConsoleHandler();
            console.setFormatter(formatter);
            console.setLevel(Level.INFO);
            root.addHandler(console);
            root.setLevel(Level.INFO);
            try {
                Path logDirectory = Path.of("build", "logs");
                Files.createDirectories(logDirectory);
                FileHandler file = new FileHandler(logDirectory.resolve("automation.log").toString(), true);
                file.setFormatter(formatter);
                file.setLevel(Level.INFO);
                root.addHandler(file);
            } catch (IOException | SecurityException exception) {
                root.log(Level.SEVERE, "Failed to initialize execution log artifact at build/logs/automation.log", exception);
            }
            configured = true;
        }
    }

    private static final class CompactFormatter extends Formatter {
        @Override
        public String format(LogRecord record) {
            String message = formatMessage(record);
            StringBuilder output = new StringBuilder()
                    .append(java.time.LocalDateTime.now())
                    .append(" ").append(record.getLevel())
                    .append(" [").append(record.getLoggerName()).append("] ")
                    .append(message).append(System.lineSeparator());
            if (record.getThrown() != null) {
                java.io.StringWriter trace = new java.io.StringWriter();
                record.getThrown().printStackTrace(new java.io.PrintWriter(trace));
                output.append(trace);
            }
            return output.toString();
        }
    }
}
