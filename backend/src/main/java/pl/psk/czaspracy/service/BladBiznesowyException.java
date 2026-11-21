package pl.psk.czaspracy.service;

/** Operacja niezgodna z regulami systemu, np. druga rozpoczeta praca. Zwracana jako HTTP 409. */
public class BladBiznesowyException extends RuntimeException {

    public BladBiznesowyException(String komunikat) {
        super(komunikat);
    }
}
