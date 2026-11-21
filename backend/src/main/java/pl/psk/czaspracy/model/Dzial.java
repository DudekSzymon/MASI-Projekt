package pl.psk.czaspracy.model;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Entity
@Table(name = "dzial")
@Getter
@Setter
@NoArgsConstructor
public class Dzial {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true)
    private String nazwa;

    /** Kierownik dzialu (asocjacja "kieruje" z diagramu klas). */
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "kierownik_id")
    private Uzytkownik kierownik;

    public Dzial(String nazwa) {
        this.nazwa = nazwa;
    }
}
