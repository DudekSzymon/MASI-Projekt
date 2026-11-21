package pl.psk.czaspracy.dto;

import pl.psk.czaspracy.model.Przerwa;
import pl.psk.czaspracy.model.SesjaPracy;

import java.time.LocalDateTime;
import java.util.List;

/** Sesja pracy zwracana przez API. */
public record SesjaDto(
        Long id,
        LocalDateTime rozpoczecie,
        LocalDateTime zakonczenie,
        long czasPracyMinut,
        List<PrzerwaDto> przerwy) {

    public record PrzerwaDto(LocalDateTime rozpoczecie, LocalDateTime zakonczenie) {
        static PrzerwaDto z(Przerwa p) {
            return new PrzerwaDto(p.getRozpoczecie(), p.getZakonczenie());
        }
    }

    public static SesjaDto z(SesjaPracy s) {
        return new SesjaDto(
                s.getId(),
                s.getRozpoczecie(),
                s.getZakonczenie(),
                s.czasPracy().toMinutes(),
                s.getPrzerwy().stream().map(PrzerwaDto::z).toList());
    }
}
