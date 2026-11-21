package pl.psk.czaspracy.model;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.time.Duration;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

@Entity
@Table(name = "sesja_pracy")
@Getter
@Setter
@NoArgsConstructor
public class SesjaPracy {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private LocalDateTime rozpoczecie;

    /** Puste, dopoki sesja trwa. */
    private LocalDateTime zakonczenie;

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "uzytkownik_id")
    private Uzytkownik uzytkownik;

    /** Kompozycja: przerwy istnieja tylko razem z sesja. */
    @OneToMany(mappedBy = "sesja", cascade = CascadeType.ALL, orphanRemoval = true)
    @OrderBy("rozpoczecie")
    private List<Przerwa> przerwy = new ArrayList<>();

    public SesjaPracy(Uzytkownik uzytkownik, LocalDateTime rozpoczecie) {
        this.uzytkownik = uzytkownik;
        this.rozpoczecie = rozpoczecie;
    }

    public boolean czyTrwa() {
        return zakonczenie == null;
    }

    /** Konczy sesje. Trwajaca przerwa jest konczona w tym samym momencie. */
    public void zakoncz(LocalDateTime czas) {
        if (!czyTrwa()) {
            throw new IllegalStateException("Praca jest już zakończona.");
        }
        przerwy.stream().filter(Przerwa::czyTrwa).forEach(p -> p.zakoncz(czas));
        this.zakonczenie = czas;
    }

    public Przerwa rozpocznijPrzerwe(LocalDateTime czas) {
        if (!czyTrwa()) {
            throw new IllegalStateException("Nie można rozpocząć przerwy po zakończeniu pracy.");
        }
        if (przerwy.stream().anyMatch(Przerwa::czyTrwa)) {
            throw new IllegalStateException("Przerwa już trwa.");
        }
        Przerwa przerwa = new Przerwa(this, czas);
        przerwy.add(przerwa);
        return przerwa;
    }

    public void zakonczPrzerwe(LocalDateTime czas) {
        Przerwa trwajaca = przerwy.stream().filter(Przerwa::czyTrwa).findFirst()
                .orElseThrow(() -> new IllegalStateException("Przerwa nie jest rozpoczęta."));
        trwajaca.zakoncz(czas);
    }

    /** Czas sesji po odjeciu przerw. Dla trwajacej sesji liczony do teraz. */
    public Duration czasPracy() {
        LocalDateTime koniec = zakonczenie != null ? zakonczenie : LocalDateTime.now();
        Duration przerwyRazem = przerwy.stream()
                .map(Przerwa::czasTrwania)
                .reduce(Duration.ZERO, Duration::plus);
        return Duration.between(rozpoczecie, koniec).minus(przerwyRazem);
    }

    /** Czas pracy ponad dzienna norme (w godzinach). */
    public Duration nadgodziny(int normaGodzin) {
        Duration ponadNorme = czasPracy().minusHours(normaGodzin);
        return ponadNorme.isNegative() ? Duration.ZERO : ponadNorme;
    }
}
