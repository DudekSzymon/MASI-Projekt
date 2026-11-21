package pl.psk.czaspracy;

import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.ActiveProfiles;

/** Sprawdza, czy aplikacja startuje i encje mapuja sie na tabele (baza H2). */
@SpringBootTest
@ActiveProfiles("dev")
class CzasPracyApplicationTests {

    @Test
    void kontekstAplikacjiSieUruchamia() {
    }
}
