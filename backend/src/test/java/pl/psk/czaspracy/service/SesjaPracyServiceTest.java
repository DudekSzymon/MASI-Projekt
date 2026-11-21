package pl.psk.czaspracy.service;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import pl.psk.czaspracy.dto.PodsumowanieMiesiacaDto;
import pl.psk.czaspracy.dto.SesjaDto;
import pl.psk.czaspracy.dto.StatusPracyDto.StanPracy;
import pl.psk.czaspracy.model.Rola;
import pl.psk.czaspracy.model.SesjaPracy;
import pl.psk.czaspracy.model.Uzytkownik;
import pl.psk.czaspracy.repository.SesjaPracyRepository;
import pl.psk.czaspracy.repository.UzytkownikRepository;

import java.time.Clock;
import java.time.LocalDateTime;
import java.time.ZoneId;
import java.util.List;
import java.util.Optional;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

class SesjaPracyServiceTest {

    private static final ZoneId STREFA = ZoneId.of("Europe/Warsaw");
    private static final LocalDateTime TERAZ = LocalDateTime.of(2026, 11, 23, 8, 0);

    private final SesjaPracyRepository sesje = mock(SesjaPracyRepository.class);
    private final UzytkownikRepository uzytkownicy = mock(UzytkownikRepository.class);
    private final Clock zegar = Clock.fixed(TERAZ.atZone(STREFA).toInstant(), STREFA);
    private final SesjaPracyService serwis = new SesjaPracyService(sesje, uzytkownicy, zegar);

    private Uzytkownik pracownik;

    @BeforeEach
    void przygotuj() {
        pracownik = new Uzytkownik("Paweł", "Pracownik", "p@firma.pl", "x", Rola.PRACOWNIK);
        pracownik.setId(1L);
        when(uzytkownicy.findById(1L)).thenReturn(Optional.of(pracownik));
        when(sesje.save(any(SesjaPracy.class))).thenAnswer(wywolanie -> wywolanie.getArgument(0));
    }

    @Test
    void rozpoczeciePracyZapisujeCzasSerwera() {
        when(sesje.findByUzytkownikAndZakonczenieIsNull(pracownik)).thenReturn(Optional.empty());

        SesjaDto sesja = serwis.rozpocznijPrace(1L);

        assertThat(sesja.rozpoczecie()).isEqualTo(TERAZ);
        assertThat(sesja.zakonczenie()).isNull();
        verify(sesje).save(any(SesjaPracy.class));
    }

    @Test
    void nieMoznaRozpoczacPracyDwaRazy() {
        when(sesje.findByUzytkownikAndZakonczenieIsNull(pracownik))
                .thenReturn(Optional.of(new SesjaPracy(pracownik, TERAZ.minusHours(1))));

        assertThatThrownBy(() -> serwis.rozpocznijPrace(1L)).isInstanceOf(BladBiznesowyException.class);
        verify(sesje, never()).save(any());
    }

    @Test
    void zablokowaneKontoNieMozeRozpoczacPracy() {
        pracownik.dezaktywuj();

        assertThatThrownBy(() -> serwis.rozpocznijPrace(1L)).isInstanceOf(BladBiznesowyException.class);
    }

    @Test
    void nieMoznaZakonczycPracyKtoraNieTrwa() {
        when(sesje.findByUzytkownikAndZakonczenieIsNull(pracownik)).thenReturn(Optional.empty());

        assertThatThrownBy(() -> serwis.zakonczPrace(1L)).isInstanceOf(BladBiznesowyException.class);
    }

    @Test
    void drugaPrzerwaZwracaBladBiznesowy() {
        SesjaPracy trwajaca = new SesjaPracy(pracownik, TERAZ.minusHours(2));
        trwajaca.rozpocznijPrzerwe(TERAZ.minusMinutes(10));
        when(sesje.findByUzytkownikAndZakonczenieIsNull(pracownik)).thenReturn(Optional.of(trwajaca));

        assertThatThrownBy(() -> serwis.rozpocznijPrzerwe(1L)).isInstanceOf(BladBiznesowyException.class);
    }

    @Test
    void statusPokazujePrzerwe() {
        SesjaPracy trwajaca = new SesjaPracy(pracownik, TERAZ.minusHours(2));
        trwajaca.rozpocznijPrzerwe(TERAZ.minusMinutes(10));
        when(sesje.findByUzytkownikAndZakonczenieIsNull(pracownik)).thenReturn(Optional.of(trwajaca));

        assertThat(serwis.status(1L).stan()).isEqualTo(StanPracy.PRZERWA);
    }

    @Test
    void podsumowanieSumujeSesjeZJednegoDniaILiczyNadgodziny() {
        SesjaPracy rano = new SesjaPracy(pracownik, LocalDateTime.of(2026, 11, 2, 7, 0));
        rano.zakoncz(LocalDateTime.of(2026, 11, 2, 12, 0));          // 5 h
        SesjaPracy popoludnie = new SesjaPracy(pracownik, LocalDateTime.of(2026, 11, 2, 13, 0));
        popoludnie.zakoncz(LocalDateTime.of(2026, 11, 2, 18, 0));    // 5 h
        SesjaPracy kolejnyDzien = new SesjaPracy(pracownik, LocalDateTime.of(2026, 11, 3, 8, 0));
        kolejnyDzien.zakoncz(LocalDateTime.of(2026, 11, 3, 14, 0));  // 6 h
        when(sesje.findByUzytkownikAndRozpoczecieBetweenOrderByRozpoczecie(eq(pracownik), any(), any()))
                .thenReturn(List.of(rano, popoludnie, kolejnyDzien));

        PodsumowanieMiesiacaDto wynik = serwis.podsumowanieMiesiaca(1L, 2026, 11);

        assertThat(wynik.dni()).hasSize(2);
        assertThat(wynik.dni().get(0).czasPracyMinut()).isEqualTo(600);
        assertThat(wynik.dni().get(0).nadgodzinyMinut()).isEqualTo(120);   // 10 h - 8 h normy
        assertThat(wynik.dni().get(1).nadgodzinyMinut()).isZero();
        assertThat(wynik.sumaMinut()).isEqualTo(16 * 60);
        assertThat(wynik.sumaNadgodzinMinut()).isEqualTo(120);
    }
}
