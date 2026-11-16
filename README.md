# System rejestracji czasu pracy

Projekt z przedmiotu **Modelowanie i analiza systemów informatycznych** (Politechnika Świętokrzyska, 2026/2027).

Aplikacja webowa do rejestrowania czasu pracy pracowników: rozpoczęcie i zakończenie pracy, przerwy, ewidencja z nadgodzinami, wnioski o korektę i nieobecność, raporty miesięczne oraz dziennik zmian.

## Technologie

- **Backend:** Java 21, Spring Boot 3, Spring Security (JWT), Spring Data JPA
- **Frontend:** React 18, TypeScript, Vite
- **Baza danych:** PostgreSQL 16, Flyway
- **Uruchamianie:** Docker Compose

## Struktura repozytorium

| Katalog | Zawartość |
|---|---|
| `backend/` | Aplikacja Spring Boot *(od KM2)* |
| `frontend/` | Aplikacja React *(od KM2)* |
| `docs/km1/` | Dokumentacja kamienia milowego 1 i diagramy UML |

## Dokumentacja

Budowanie PDF z dokumentacją KM1 (wymaga Pythona i przeglądarki Edge lub Chrome):

```
powershell -ExecutionPolicy Bypass -File docs\km1\build_pdf.ps1
```

Skrypt generuje diagramy SVG z `docs/km1/diagrams/generate.py` i drukuje `docs/km1/dokumentacja_km1.html` do PDF.

## Zasady pracy

- `main` zawiera zawsze działającą wersję. Zmiany trafiają do niej przez pull requesty.
- Każde zadanie realizujemy na osobnej gałęzi, np. `feature/rejestracja-sesji` lub `fix/nadgodziny`.
- Każdy commituje ze swojego konta, żeby historia pokazywała wkład każdej osoby.

## Zespół

- Szymon Dudek
- *[Imię Nazwisko]*
