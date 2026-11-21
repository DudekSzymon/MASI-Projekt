package pl.psk.czaspracy.controller;

import org.springframework.web.bind.annotation.*;
import pl.psk.czaspracy.dto.PodsumowanieMiesiacaDto;
import pl.psk.czaspracy.dto.SesjaDto;
import pl.psk.czaspracy.dto.StatusPracyDto;
import pl.psk.czaspracy.service.SesjaPracyService;

import java.time.LocalDate;

/** REST API rejestrowania czasu pracy zalogowanego pracownika. */
@RestController
@RequestMapping("/api/sesje")
public class SesjaPracyController {

    private final SesjaPracyService serwis;
    private final AktualnyUzytkownik aktualny;

    public SesjaPracyController(SesjaPracyService serwis, AktualnyUzytkownik aktualny) {
        this.serwis = serwis;
        this.aktualny = aktualny;
    }

    @PostMapping("/start")
    public SesjaDto rozpocznijPrace() {
        return serwis.rozpocznijPrace(aktualny.id());
    }

    @PostMapping("/przerwa/start")
    public SesjaDto rozpocznijPrzerwe() {
        return serwis.rozpocznijPrzerwe(aktualny.id());
    }

    @PostMapping("/przerwa/stop")
    public SesjaDto zakonczPrzerwe() {
        return serwis.zakonczPrzerwe(aktualny.id());
    }

    @PostMapping("/stop")
    public SesjaDto zakonczPrace() {
        return serwis.zakonczPrace(aktualny.id());
    }

    @GetMapping("/status")
    public StatusPracyDto status() {
        return serwis.status(aktualny.id());
    }

    /** Czas pracy z miesiaca. Bez parametrow zwraca biezacy miesiac. */
    @GetMapping("/moje")
    public PodsumowanieMiesiacaDto mojCzasPracy(@RequestParam(required = false) Integer rok,
                                                @RequestParam(required = false) Integer miesiac) {
        LocalDate dzis = LocalDate.now();
        return serwis.podsumowanieMiesiaca(aktualny.id(),
                rok != null ? rok : dzis.getYear(),
                miesiac != null ? miesiac : dzis.getMonthValue());
    }
}
