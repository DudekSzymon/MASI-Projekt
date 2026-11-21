package pl.psk.czaspracy.model;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.time.LocalDate;

@Entity
@Table(name = "wniosek_urlopowy")
@Getter
@Setter
@NoArgsConstructor
public class WniosekUrlopowy {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private LocalDate dataOd;

    @Column(nullable = false)
    private LocalDate dataDo;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private StatusWniosku status = StatusWniosku.OCZEKUJACY;

    private String komentarz;

    /** Asocjacja "sklada". */
    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "pracownik_id")
    private Uzytkownik pracownik;

    /** Asocjacja "rozpatruje". Puste, dopoki wniosek czeka na decyzje. */
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "rozpatrujacy_id")
    private Uzytkownik rozpatrujacy;

    public WniosekUrlopowy(Uzytkownik pracownik, LocalDate dataOd, LocalDate dataDo) {
        if (dataDo.isBefore(dataOd)) {
            throw new IllegalArgumentException("Data końca urlopu jest wcześniejsza niż data początku.");
        }
        this.pracownik = pracownik;
        this.dataOd = dataOd;
        this.dataDo = dataDo;
    }

    public void zatwierdz(Uzytkownik kierownik) {
        rozpatrz(kierownik, StatusWniosku.ZATWIERDZONY, null);
    }

    public void odrzuc(Uzytkownik kierownik, String powod) {
        rozpatrz(kierownik, StatusWniosku.ODRZUCONY, powod);
    }

    private void rozpatrz(Uzytkownik kierownik, StatusWniosku nowyStatus, String komentarz) {
        if (status != StatusWniosku.OCZEKUJACY) {
            throw new IllegalStateException("Wniosek został już rozpatrzony.");
        }
        this.status = nowyStatus;
        this.rozpatrujacy = kierownik;
        this.komentarz = komentarz;
    }
}
