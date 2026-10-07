package com.automation.template.support;

import static org.junit.jupiter.api.Assertions.*;

import io.cucumber.core.backend.TestCaseState;
import io.cucumber.java.Scenario;
import java.lang.reflect.Constructor;
import java.lang.reflect.Proxy;
import java.nio.file.Files;
import java.nio.file.Path;
import java.time.Clock;
import java.time.Instant;
import java.time.ZoneOffset;
import java.util.concurrent.atomic.AtomicInteger;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;
import org.openqa.selenium.TakesScreenshot;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.remote.RemoteWebDriver;

class EvidenceManagerTest {
    @TempDir Path temp;
    private final Clock clock = Clock.fixed(Instant.parse("2026-10-07T02:30:15Z"), ZoneOffset.UTC);

    @Test void safeNameHandlesWindowsCharactersAndLongNames() {
        String name = EvidenceManager.fileName("¿Login: <admin>|*? /" + "x".repeat(120), clock);
        assertTrue(name.matches("[A-Za-z0-9._-]+\\.png"));
        assertTrue(name.contains("20261007_023015"));
        assertTrue(name.length() < 145);
    }

    @Test void missingDriverDoesNotCreateEvidence() throws Exception {
        AtomicInteger attachments = new AtomicInteger();
        new EvidenceManager(temp, clock).captureFailure(scenario(attachments), null);
        assertEquals(0, attachments.get());
        try (var files = Files.list(temp)) {
            assertEquals(0, files.count());
        }
    }

    @Test void closedRemoteDriverDoesNotCreateEvidence() throws Exception {
        AtomicInteger attachments = new AtomicInteger();
        new EvidenceManager(temp, clock).captureFailure(scenario(attachments), new RemoteWebDriver() { });
        assertEquals(0, attachments.get());
        try (var files = Files.list(temp)) {
            assertEquals(0, files.count());
        }
    }

    @Test void captureFailureDoesNotReplaceScenarioFailure() throws Exception {
        AtomicInteger attachments = new AtomicInteger();
        WebDriver driver = fakeDriver(new IllegalStateException("capture unavailable"));
        assertDoesNotThrow(() -> new EvidenceManager(temp, clock).captureFailure(scenario(attachments), driver));
        assertEquals(0, attachments.get());
        try (var files = Files.list(temp)) {
            assertEquals(0, files.count());
        }
    }

    @Test void availableDriverProducesFileAndAttachment() throws Exception {
        AtomicInteger attachments = new AtomicInteger();
        byte[] png = new byte[] {(byte) 137, 80, 78, 71, 13, 10, 26, 10};
        new EvidenceManager(temp, clock).captureFailure(scenario(attachments), fakeDriver(png));
        assertEquals(1, attachments.get());
        try (var files = Files.list(temp)) {
            Path file = files.findFirst().orElseThrow();
            assertArrayEquals(png, Files.readAllBytes(file));
        }
    }

    private static WebDriver fakeDriver(Object result) {
        return (WebDriver) Proxy.newProxyInstance(WebDriver.class.getClassLoader(),
                new Class<?>[] {WebDriver.class, TakesScreenshot.class}, (proxy, method, args) -> {
                    if (method.getName().equals("getScreenshotAs")) {
                        if (result instanceof RuntimeException exception) throw exception;
                        return result;
                    }
                    return null;
                });
    }

    private static Scenario scenario(AtomicInteger attachments) throws Exception {
        TestCaseState state = (TestCaseState) Proxy.newProxyInstance(TestCaseState.class.getClassLoader(),
                new Class<?>[] {TestCaseState.class}, (proxy, method, args) -> {
                    if (method.getName().equals("getName")) return "Login: <admin>?";
                    if (method.getName().equals("attach")) { attachments.incrementAndGet(); return null; }
                    return null;
                });
        Constructor<Scenario> constructor = Scenario.class.getDeclaredConstructor(TestCaseState.class);
        constructor.setAccessible(true);
        return constructor.newInstance(state);
    }
}
