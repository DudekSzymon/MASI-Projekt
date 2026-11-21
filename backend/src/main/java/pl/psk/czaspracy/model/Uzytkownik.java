package pl.psk.czaspracy.model;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.time.Duration;
import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;

@Entity
@Table(name = "uzytkownik")
@Getter
@Setter
@NoArgsConstructor
public class Uzytkownik {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String imie;

    @Column(nullable = false)
    private String nazwisko;

    @Column(nullable = false, unique = true)
    private String email;

    @Column(nullable = false)
    private String hasloHash;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private Rola rola = Rola.PRACOWNIK;

    private boolean aktywny = true;

    /** Dzienna norma czasu pracy w godzinach (domyslnie 8). */
    private int normaDzienna = 8;

    /** Asocjacja "nalezy do" z diagramu klas. */
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "dzial_id")
    private Dzial dzial;

    @OneToMany(mappedBy = "uzytkownik")
    private List<SesjaPracy> sesje = new ArrayList<>();

    public Uzytkownik(String imie, String nazwisko, String email, String hasloHash, Rola rola) {
        this.imie = imie;
        this.nazwisko = nazwisko;
        this.email = email;
        this.hasloHash = hasloHash;
        this.rola = rola;
    }

    public void dezaktywuj() {
        this.aktywny = false;
    }

    /** Suma czasu pracy (po odjeciu przerw) z sesji rozpoczetych w podanym okresie. */
    public Duration czasPracy(LocalDate od, LocalDate doDnia) {
        return sesje.stream()
                .filter(s -> !s.getRozpoczecie().toLocalDate().isBefore(od)
                        && !s.getRozpoczecie().toLocalDate().isAfter(doDnia))
                .map(SesjaPracy::czasPracy)
                .reduce(Duration.ZERO, Duration::plus);
    }
}
