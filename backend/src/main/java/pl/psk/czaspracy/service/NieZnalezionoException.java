package pl.psk.czaspracy.service;

/** Brak szukanego obiektu w bazie. Zwracany jako HTTP 404. */
public class NieZnalezionoException extends RuntimeException {

    public NieZnalezionoException(String komunikat) {
        super(komunikat);
    }
}
