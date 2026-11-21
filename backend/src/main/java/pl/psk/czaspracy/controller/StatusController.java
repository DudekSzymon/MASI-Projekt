package pl.psk.czaspracy.controller;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.time.Instant;
import java.util.Map;

/** Prosty endpoint do sprawdzenia, czy backend dziala (uzywa go tez frontend). */
@RestController
@RequestMapping("/api/status")
public class StatusController {

    @GetMapping
    public Map<String, Object> status() {
        return Map.of(
                "aplikacja", "System rejestracji czasu pracy",
                "status", "OK",
                "czasSerwera", Instant.now().toString());
    }
}
