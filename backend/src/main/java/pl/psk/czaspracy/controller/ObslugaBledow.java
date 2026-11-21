package pl.psk.czaspracy.controller;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;
import pl.psk.czaspracy.service.BladBiznesowyException;
import pl.psk.czaspracy.service.NieZnalezionoException;

import java.util.Map;

/** Zamienia wyjatki z serwisow na odpowiedzi HTTP z czytelnym komunikatem. */
@RestControllerAdvice
public class ObslugaBledow {

    @ExceptionHandler(BladBiznesowyException.class)
    public ResponseEntity<Map<String, String>> bladBiznesowy(BladBiznesowyException e) {
        return ResponseEntity.status(HttpStatus.CONFLICT).body(Map.of("blad", e.getMessage()));
    }

    @ExceptionHandler(NieZnalezionoException.class)
    public ResponseEntity<Map<String, String>> nieZnaleziono(NieZnalezionoException e) {
        return ResponseEntity.status(HttpStatus.NOT_FOUND).body(Map.of("blad", e.getMessage()));
    }
}
