package pl.psk.czaspracy.dto;

import java.time.LocalDate;
import java.util.List;

/** Czas pracy pracownika z podzialem na dni oraz sumy z calego miesiaca. */
public record PodsumowanieMiesiacaDto(
        int rok,
        int miesiac,
        int normaDziennaGodzin,
        List<DzienDto> dni,
        long sumaMinut,
        long sumaNadgodzinMinut) {

    public record DzienDto(LocalDate data, long czasPracyMinut, long nadgodzinyMinut, List<SesjaDto> sesje) {
    }
}
