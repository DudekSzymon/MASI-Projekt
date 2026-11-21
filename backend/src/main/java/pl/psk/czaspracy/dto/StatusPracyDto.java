package pl.psk.czaspracy.dto;

/** Biezacy stan pracownika pokazywany na stronie glownej. */
public record StatusPracyDto(StanPracy stan, SesjaDto sesja) {

    public enum StanPracy {
        POZA_PRACA,
        W_PRACY,
        PRZERWA
    }
}
