package pl.psk.czaspracy.service;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import pl.psk.czaspracy.dto.PodsumowanieMiesiacaDto;
import pl.psk.czaspracy.dto.PodsumowanieMiesiacaDto.DzienDto;
import pl.psk.czaspracy.dto.SesjaDto;
import pl.psk.czaspracy.dto.StatusPracyDto;
import pl.psk.czaspracy.dto.StatusPracyDto.StanPracy;
import pl.psk.czaspracy.model.Przerwa;
import pl.psk.czaspracy.model.SesjaPracy;
import pl.psk.czaspracy.model.Uzytkownik;
import pl.psk.czaspracy.repository.SesjaPracyRepository;
import pl.psk.czaspracy.repository.UzytkownikRepository;

import java.time.Clock;
import java.time.Duration;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.YearMonth;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.TreeMap;
import java.util.stream.Collectors;

/** Logika rejestrowania czasu pracy (UC02 do UC05). */
@Service
@Transactional
public class SesjaPracyService {

    private final SesjaPracyRepository sesje;
    private final UzytkownikRepository uzytkownicy;
    private final Clock zegar;

    public SesjaPracyService(SesjaPracyRepository sesje, UzytkownikRepository uzytkownicy, Clock zegar) {
        this.sesje = sesje;
        this.uzytkownicy = uzytkownicy;
        this.zegar = zegar;
    }

    /** UC02. Pracownik nie moze miec dwoch rozpoczetych prac naraz. */
    public SesjaDto rozpocznijPrace(Long uzytkownikId) {
        Uzytkownik uzytkownik = pobierzAktywnego(uzytkownikId);
        if (sesje.findByUzytkownikAndZakonczenieIsNull(uzytkownik).isPresent()) {
            throw new BladBiznesowyException("Praca jest już rozpoczęta. Najpierw ją zakończ.");
        }
        SesjaPracy sesja = sesje.save(new SesjaPracy(uzytkownik, teraz()));
        return SesjaDto.z(sesja);
    }

    /** UC03, rozpoczecie przerwy. */
    public SesjaDto rozpocznijPrzerwe(Long uzytkownikId) {
        SesjaPracy sesja = trwajacaSesja(uzytkownikId);
        wykonaj(() -> sesja.rozpocznijPrzerwe(teraz()));
        return SesjaDto.z(sesja);
    }

    /** UC03, zakonczenie przerwy. */
    public SesjaDto zakonczPrzerwe(Long uzytkownikId) {
        SesjaPracy sesja = trwajacaSesja(uzytkownikId);
        wykonaj(() -> sesja.zakonczPrzerwe(teraz()));
        return SesjaDto.z(sesja);
    }

    /** UC04. Trwajaca przerwa konczy sie razem z praca. */
    public SesjaDto zakonczPrace(Long uzytkownikId) {
        SesjaPracy sesja = trwajacaSesja(uzytkownikId);
        sesja.zakoncz(teraz());
        return SesjaDto.z(sesja);
    }

    @Transactional(readOnly = true)
    public StatusPracyDto status(Long uzytkownikId) {
        Uzytkownik uzytkownik = pobierz(uzytkownikId);
        Optional<SesjaPracy> trwajaca = sesje.findByUzytkownikAndZakonczenieIsNull(uzytkownik);
        if (trwajaca.isEmpty()) {
            return new StatusPracyDto(StanPracy.POZA_PRACA, null);
        }
        SesjaPracy sesja = trwajaca.get();
        boolean przerwa = sesja.getPrzerwy().stream().anyMatch(Przerwa::czyTrwa);
        return new StatusPracyDto(przerwa ? StanPracy.PRZERWA : StanPracy.W_PRACY, SesjaDto.z(sesja));
    }

    /** UC05. Czas pracy z kazdego dnia miesiaca, nadgodziny liczone ponad dzienna norme. */
    @Transactional(readOnly = true)
    public PodsumowanieMiesiacaDto podsumowanieMiesiaca(Long uzytkownikId, int rok, int miesiac) {
        Uzytkownik uzytkownik = pobierz(uzytkownikId);
        YearMonth ym = YearMonth.of(rok, miesiac);
        List<SesjaPracy> sesjeMiesiaca = sesje.findByUzytkownikAndRozpoczecieBetweenOrderByRozpoczecie(
                uzytkownik, ym.atDay(1).atStartOfDay(), ym.atEndOfMonth().atTime(23, 59, 59));

        Map<LocalDate, List<SesjaPracy>> poDniach = sesjeMiesiaca.stream()
                .collect(Collectors.groupingBy(s -> s.getRozpoczecie().toLocalDate(), TreeMap::new, Collectors.toList()));

        Duration norma = Duration.ofHours(uzytkownik.getNormaDzienna());
        List<DzienDto> dni = poDniach.entrySet().stream().map(wpis -> {
            Duration czas = wpis.getValue().stream().map(SesjaPracy::czasPracy).reduce(Duration.ZERO, Duration::plus);
            Duration nadgodziny = czas.compareTo(norma) > 0 ? czas.minus(norma) : Duration.ZERO;
            return new DzienDto(wpis.getKey(), czas.toMinutes(), nadgodziny.toMinutes(),
                    wpis.getValue().stream().map(SesjaDto::z).toList());
        }).toList();

        long suma = dni.stream().mapToLong(DzienDto::czasPracyMinut).sum();
        long sumaNadgodzin = dni.stream().mapToLong(DzienDto::nadgodzinyMinut).sum();
        return new PodsumowanieMiesiacaDto(rok, miesiac, uzytkownik.getNormaDzienna(), dni, suma, sumaNadgodzin);
    }

    private SesjaPracy trwajacaSesja(Long uzytkownikId) {
        return sesje.findByUzytkownikAndZakonczenieIsNull(pobierzAktywnego(uzytkownikId))
                .orElseThrow(() -> new BladBiznesowyException("Praca nie jest rozpoczęta."));
    }

    private Uzytkownik pobierz(Long id) {
        return uzytkownicy.findById(id)
                .orElseThrow(() -> new NieZnalezionoException("Nie ma użytkownika o id " + id));
    }

    private Uzytkownik pobierzAktywnego(Long id) {
        Uzytkownik u = pobierz(id);
        if (!u.isAktywny()) {
            throw new BladBiznesowyException("Konto jest zablokowane.");
        }
        return u;
    }

    private LocalDateTime teraz() {
        return LocalDateTime.now(zegar);
    }

    /** Zamienia bledy regul z encji (np. druga przerwa) na blad biznesowy dla API. */
    private void wykonaj(Runnable operacja) {
        try {
            operacja.run();
        } catch (IllegalStateException e) {
            throw new BladBiznesowyException(e.getMessage());
        }
    }
}
