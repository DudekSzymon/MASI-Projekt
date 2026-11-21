package pl.psk.czaspracy.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.time.Clock;
import java.time.ZoneId;

/**
 * Zegar serwera. Godziny rozpoczecia i zakonczenia pracy biora czas wylacznie stad,
 * a nie z urzadzenia pracownika. W testach podmieniany na zegar staly.
 */
@Configuration
public class ZegarConfig {

    @Bean
    public Clock zegar() {
        return Clock.system(ZoneId.of("Europe/Warsaw"));
    }
}
