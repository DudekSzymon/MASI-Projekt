package pl.psk.czaspracy.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import pl.psk.czaspracy.model.StatusWniosku;
import pl.psk.czaspracy.model.Uzytkownik;
import pl.psk.czaspracy.model.WniosekUrlopowy;

import java.util.List;

public interface WniosekUrlopowyRepository extends JpaRepository<WniosekUrlopowy, Long> {

    List<WniosekUrlopowy> findByPracownikOrderByDataOdDesc(Uzytkownik pracownik);

    List<WniosekUrlopowy> findByPracownikDzialIdAndStatus(Long dzialId, StatusWniosku status);
}
