package pl.psk.czaspracy.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import pl.psk.czaspracy.model.Dzial;
import pl.psk.czaspracy.model.Uzytkownik;

import java.util.List;
import java.util.Optional;

public interface UzytkownikRepository extends JpaRepository<Uzytkownik, Long> {

    Optional<Uzytkownik> findByEmail(String email);

    List<Uzytkownik> findByDzial(Dzial dzial);
}
