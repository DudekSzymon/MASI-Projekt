package pl.psk.czaspracy.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import pl.psk.czaspracy.model.Dzial;

public interface DzialRepository extends JpaRepository<Dzial, Long> {
}
