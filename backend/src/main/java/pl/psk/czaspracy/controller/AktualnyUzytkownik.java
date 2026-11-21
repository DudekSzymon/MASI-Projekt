package pl.psk.czaspracy.controller;

import jakarta.servlet.http.HttpServletRequest;
import org.springframework.stereotype.Component;
import pl.psk.czaspracy.service.BladBiznesowyException;

/**
 * Ustala, kto wysyla zadanie.
 * TYMCZASOWO: id uzytkownika z naglowka X-Uzytkownik-Id. Po dodaniu logowania (Spring Security + JWT)
 * wystarczy zmienic tylko ta klase, zeby brala id z tokenu. Kontrolery i serwisy zostaja bez zmian.
 */
@Component
public class AktualnyUzytkownik {

    static final String NAGLOWEK = "X-Uzytkownik-Id";

    private final HttpServletRequest zadanie;

    public AktualnyUzytkownik(HttpServletRequest zadanie) {
        this.zadanie = zadanie;
    }

    public Long id() {
        String wartosc = zadanie.getHeader(NAGLOWEK);
        if (wartosc == null) {
            throw new BladBiznesowyException("Brak zalogowanego użytkownika.");
        }
        try {
            return Long.valueOf(wartosc);
        } catch (NumberFormatException e) {
            throw new BladBiznesowyException("Niepoprawny identyfikator użytkownika.");
        }
    }
}
