package pl.psk.czaspracy.config;

import org.springframework.boot.CommandLineRunner;
import org.springframework.context.annotation.Profile;
import org.springframework.stereotype.Component;
import pl.psk.czaspracy.model.Dzial;
import pl.psk.czaspracy.model.Rola;
import pl.psk.czaspracy.model.Uzytkownik;
import pl.psk.czaspracy.repository.DzialRepository;
import pl.psk.czaspracy.repository.UzytkownikRepository;

/**
 * Przykladowe konta w profilu "dev" (baza H2 tworzona od nowa przy kazdym starcie).
 * Hasla maja prefiks {noop}, zostana zastapione skrotem BCrypt po dodaniu logowania.
 */
@Component
@Profile("dev")
public class DaneTestowe implements CommandLineRunner {

    private final UzytkownikRepository uzytkownicy;
    private final DzialRepository dzialy;

    public DaneTestowe(UzytkownikRepository uzytkownicy, DzialRepository dzialy) {
        this.uzytkownicy = uzytkownicy;
        this.dzialy = dzialy;
    }

    @Override
    public void run(String... args) {
        if (uzytkownicy.count() > 0) {
            return;
        }
        uzytkownicy.save(
                new Uzytkownik("Adam", "Administrator", "admin@firma.pl", "{noop}admin123", Rola.ADMINISTRATOR));
        Uzytkownik kierownik = uzytkownicy.save(
                new Uzytkownik("Katarzyna", "Kierownik", "kierownik@firma.pl", "{noop}kierownik123", Rola.KIEROWNIK));

        Dzial it = new Dzial("Dział IT");
        it.setKierownik(kierownik);
        dzialy.save(it);

        kierownik.setDzial(it);
        Uzytkownik pracownik = new Uzytkownik("Paweł", "Pracownik", "pracownik@firma.pl", "{noop}pracownik123", Rola.PRACOWNIK);
        pracownik.setDzial(it);
        uzytkownicy.save(kierownik);
        uzytkownicy.save(pracownik);
    }
}
