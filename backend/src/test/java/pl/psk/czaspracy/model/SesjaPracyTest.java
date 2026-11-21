package pl.psk.czaspracy.model;

import org.junit.jupiter.api.Test;

import java.time.Duration;
import java.time.LocalDateTime;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

class SesjaPracyTest {

    private static final LocalDateTime START = LocalDateTime.of(2026, 11, 23, 8, 0);

    private SesjaPracy nowaSesja() {
        return new SesjaPracy(new Uzytkownik(), START);
    }

    @Test
    void czasPracyOdejmujePrzerwy() {
        SesjaPracy sesja = nowaSesja();
        sesja.rozpocznijPrzerwe(START.plusHours(4));
        sesja.zakonczPrzerwe(START.plusHours(4).plusMinutes(30));
        sesja.zakoncz(START.plusHours(9));

        assertThat(sesja.czasPracy()).isEqualTo(Duration.ofHours(8).plusMinutes(30));
    }

    @Test
    void nadgodzinyToCzasPonadNorme() {
        SesjaPracy sesja = nowaSesja();
        sesja.zakoncz(START.plusHours(10));

        assertThat(sesja.nadgodziny(8)).isEqualTo(Duration.ofHours(2));
    }

    @Test
    void brakNadgodzinGdyPracaKrotszaNizNorma() {
        SesjaPracy sesja = nowaSesja();
        sesja.zakoncz(START.plusHours(6));

        assertThat(sesja.nadgodziny(8)).isEqualTo(Duration.ZERO);
    }

    @Test
    void zakonczenieSesjiKonczyTrwajacaPrzerwe() {
        SesjaPracy sesja = nowaSesja();
        sesja.rozpocznijPrzerwe(START.plusHours(7));
        sesja.zakoncz(START.plusHours(8));

        assertThat(sesja.getPrzerwy().get(0).czyTrwa()).isFalse();
        assertThat(sesja.czasPracy()).isEqualTo(Duration.ofHours(7));
    }

    @Test
    void nieMoznaRozpoczacDwochPrzerwNaraz() {
        SesjaPracy sesja = nowaSesja();
        sesja.rozpocznijPrzerwe(START.plusHours(1));

        assertThatThrownBy(() -> sesja.rozpocznijPrzerwe(START.plusHours(2)))
                .isInstanceOf(IllegalStateException.class);
    }

    @Test
    void nieMoznaZakonczycSesjiDwaRazy() {
        SesjaPracy sesja = nowaSesja();
        sesja.zakoncz(START.plusHours(8));

        assertThatThrownBy(() -> sesja.zakoncz(START.plusHours(9)))
                .isInstanceOf(IllegalStateException.class);
    }
}
