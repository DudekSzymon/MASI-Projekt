package pl.psk.czaspracy.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import pl.psk.czaspracy.model.SesjaPracy;
import pl.psk.czaspracy.model.Uzytkownik;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;

public interface SesjaPracyRepository extends JpaRepository<SesjaPracy, Long> {

    /** Trwajaca sesja uzytkownika (bez zakonczenia). */
    Optional<SesjaPracy> findByUzytkownikAndZakonczenieIsNull(Uzytkownik uzytkownik);

    List<SesjaPracy> findByUzytkownikAndRozpoczecieBetweenOrderByRozpoczecie(
            Uzytkownik uzytkownik, LocalDateTime od, LocalDateTime doCzasu);
}
