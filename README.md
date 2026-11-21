# System rejestracji czasu pracy

Projekt z przedmiotu **Modelowanie i analiza systemów informatycznych** (Politechnika Świętokrzyska, 2026/2027).

Aplikacja webowa do rejestrowania czasu pracy: rozpoczęcie i zakończenie pracy, przerwy, podgląd czasu pracy z nadgodzinami, wnioski urlopowe, raport miesięczny oraz zarządzanie kontami i działami.

## Technologie

- **Backend:** Java 21, Spring Boot 3.5, Spring Data JPA
- **Frontend:** React 19, TypeScript, Vite, React Router
- **Baza danych:** PostgreSQL 16 (Docker), H2 w pamięci w profilu `dev`

## Struktura repozytorium

| Katalog | Zawartość |
|---|---|
| `backend/` | Aplikacja Spring Boot (`pl.psk.czaspracy`: `model`, `repository`, `service`, `controller`) |
| `frontend/` | Aplikacja React (`src/pages` – widoki, `src/api.ts` – wywołania API) |
| `docs/km1/` | Dokumentacja kamienia milowego 1 i diagramy UML |
| `docker-compose.yml` | Baza PostgreSQL |

## Uruchomienie

Wymagane: Java 21, Node.js 20+. Maven nie jest potrzebny (jest wrapper `mvnw`).

**Backend bez Dockera** (baza H2 w pamięci, dane znikają po wyłączeniu):

```
cd backend
mvnw spring-boot:run -Dspring-boot.run.profiles=dev
```

**Backend z PostgreSQL** (wymaga uruchomionego Docker Desktop):

```
docker compose up -d
cd backend
mvnw spring-boot:run
```

**Frontend:**

```
cd frontend
npm install
npm run dev
```

Aplikacja: http://localhost:5173 (zapytania `/api` są przekazywane do backendu na porcie 8080).

**Testy backendu:** `cd backend` i `mvnw test`

## Dokumentacja

Budowanie PDF z dokumentacją KM1 (wymaga Pythona i przeglądarki Edge lub Chrome):

```
powershell -ExecutionPolicy Bypass -File docs\km1\build_pdf.ps1
```

## Zasady pracy

- `main` zawiera zawsze działającą wersję. Zmiany trafiają do niej przez pull requesty.
- Każde zadanie realizujemy na osobnej gałęzi, np. `feature/sesje-pracy` lub `fix/nadgodziny`.
- Każdy commituje ze swojego konta, żeby historia pokazywała wkład każdej osoby.

## Podział prac

| Osoba | Zakres |
|---|---|
| Szymon Dudek | Backend: sesje pracy, przerwy, nadgodziny, raporty |
| Bartosz Fijołek | Frontend: panele pracownika, kierownika i administratora |
| Bartłomiej Łukasiewicz | Logowanie i uprawnienia (Spring Security, JWT), konta, działy, wnioski urlopowe |
