package pl.psk.czaspracy.model;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.time.Duration;
import java.time.LocalDateTime;

@Entity
@Table(name = "przerwa")
@Getter
@Setter
@NoArgsConstructor
public class Przerwa {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private LocalDateTime rozpoczecie;

    private LocalDateTime zakonczenie;

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "sesja_id")
    private SesjaPracy sesja;

    public Przerwa(SesjaPracy sesja, LocalDateTime rozpoczecie) {
        this.sesja = sesja;
        this.rozpoczecie = rozpoczecie;
    }

    public boolean czyTrwa() {
        return zakonczenie == null;
    }

    public void zakoncz(LocalDateTime czas) {
        this.zakonczenie = czas;
    }

    /** Czas trwania przerwy. Dla trwajacej przerwy liczony do teraz. */
    public Duration czasTrwania() {
        LocalDateTime koniec = zakonczenie != null ? zakonczenie : LocalDateTime.now();
        return Duration.between(rozpoczecie, koniec);
    }
}
