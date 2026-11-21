"""Generator diagramow UML (SVG) dla KM2.

Uruchomienie:  python generate.py
Wynik:         use_case.svg, class.svg, layers.svg, components.svg, sequence.svg, activity.svg

Korzysta z funkcji pomocniczych generatora KM1 (docs/km1/diagrams/generate.py).
"""
from __future__ import annotations

import sys
from pathlib import Path

OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(OUT.parent.parent / "km1" / "diagrams"))
import generate as km1  # noqa: E402
from generate import Box, INK, LINE, link, polyline, svg_doc, t, text_width  # noqa: E402

PLAN = "#94a3b8"   # elementy planowane (jeszcze niezaimplementowane)


def rect(x, y, w, h, fill="#fff", stroke=LINE, rx=0, dashed=False, sw=1.3):
    dash = ' stroke-dasharray="6,4"' if dashed else ""
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{dash}/>')


def cylinder(cx, y, w, h, label, sub=None):
    rx, ry = w / 2, 10
    x0, x1 = cx - rx, cx + rx
    s = (f'<path d="M{x0},{y + ry} L{x0},{y + h - ry} A{rx},{ry} 0 0 0 {x1},{y + h - ry} '
         f'L{x1},{y + ry}" fill="#eef4fb" stroke="{LINE}" stroke-width="1.3"/>')
    s += f'<ellipse cx="{cx}" cy="{y + ry}" rx="{rx}" ry="{ry}" fill="#eef4fb" stroke="{LINE}" stroke-width="1.3"/>'
    s += t(cx, y + h / 2 + 6, label, 13, weight="bold")
    if sub:
        s += t(cx, y + h / 2 + 22, sub, 11, fill="#475569")
    return s


# ================================================================ KLASY (wg kodu)
def class_diagram():
    C0, C1, C2 = 20, 400, 900
    TOP = 30
    uz = Box("Uzytkownik", C1, TOP, [
        "- id: Long", "- imie: String", "- nazwisko: String", "- email: String",
        "- hasloHash: String", "- rola: Rola", "- aktywny: boolean", "- normaDzienna: int"],
        ["+ dezaktywuj(): void", "+ czasPracy(od: LocalDate, doDnia: LocalDate): Duration"],
        stereo="«entity»")
    dz = Box("Dzial", C0, TOP + 20, ["- id: Long", "- nazwa: String"], stereo="«entity»")
    wn = Box("WniosekUrlopowy", C2, TOP, [
        "- id: Long", "- dataOd: LocalDate", "- dataDo: LocalDate",
        "- status: StatusWniosku", "- komentarz: String"],
        ["+ zatwierdz(kierownik: Uzytkownik): void", "+ odrzuc(kierownik: Uzytkownik, powod: String): void"],
        stereo="«entity»")
    sesja = Box("SesjaPracy", C1, uz.bottom + 80, [
        "- id: Long", "- rozpoczecie: LocalDateTime", "- zakonczenie: LocalDateTime"],
        ["+ czyTrwa(): boolean", "+ zakoncz(czas: LocalDateTime): void",
         "+ rozpocznijPrzerwe(czas: LocalDateTime): Przerwa", "+ zakonczPrzerwe(czas: LocalDateTime): void",
         "+ czasPracy(): Duration", "+ nadgodziny(normaGodzin: int): Duration"],
        stereo="«entity»")
    przerwa = Box("Przerwa", C2, sesja.y, [
        "- id: Long", "- rozpoczecie: LocalDateTime", "- zakonczenie: LocalDateTime"],
        ["+ czyTrwa(): boolean", "+ zakoncz(czas: LocalDateTime): void", "+ czasTrwania(): Duration"],
        stereo="«entity»")
    rola = Box("Rola", C0, dz.bottom + 110, ["PRACOWNIK", "KIEROWNIK", "ADMINISTRATOR"],
               stereo="«enumeration»", enum=True)
    status = Box("StatusWniosku", C0, rola.bottom + 30, ["OCZEKUJACY", "ZATWIERDZONY", "ODRZUCONY"],
                 stereo="«enumeration»", enum=True)
    boxes = [uz, dz, wn, sesja, przerwa, rola, status]
    W = int(max(b.right for b in boxes) + 30)
    H = int(max(b.bottom for b in boxes) + 25)

    b = ""
    y1, y2 = dz.y + 35, dz.y + 70
    b += link([uz.L(y1), dz.R(y1)], "*", "0..1", "należy do", ((uz.x + dz.right) / 2, y1 - 6))
    b += link([uz.L(y2), dz.R(y2)], "0..1", "*", "kieruje", ((uz.x + dz.right) / 2, y2 - 6))
    b += link([uz.B(uz.cx), sesja.T(uz.cx)], "1", "*", "rejestruje",
              (uz.cx + 8, (uz.bottom + sesja.y) / 2 + 4), lanchor="start")
    yp = sesja.y + 60
    b += t(sesja.right + 26, yp - 6, "1", 12, anchor="start")
    b += link([sesja.R(yp), przerwa.L(yp)], None, "0..*", "zawiera",
              ((sesja.right + przerwa.x) / 2, yp - 8), kind="comp")
    w1, w2 = wn.y + 55, wn.y + 115
    b += link([uz.R(w1), wn.L(w1)], "1", "*", "składa", ((uz.right + wn.x) / 2, w1 - 6))
    b += link([uz.R(w2), wn.L(w2)], "0..1", "*", "rozpatruje", ((uz.right + wn.x) / 2, w2 - 6))
    for box in boxes:
        b += box.svg()
    b += t(C0, rola.y - 14, "Typy wyliczeniowe:", 12, anchor="start", style="italic", fill="#475569")
    return svg_doc(W, H, b, "Diagram klas")


# ================================================================ WARSTWY
def layers():
    W, X0, LW = 1000, 20, 960

    def layer(y, h, title, sub, fill):
        s = rect(X0, y, LW, h, fill=fill, rx=6)
        s += t(X0 + 14, y + 22, title, 14, anchor="start", weight="bold")
        s += t(X0 + LW - 14, y + 22, sub, 12, anchor="end", style="italic", fill="#475569")
        return s

    def chips(y, items, x0=X0 + 20, plan=()):
        s, x = "", x0
        for it in items:
            w = text_width(it, 12) + 22
            dashed = it in plan
            s += rect(x, y, w, 28, fill="#fff", rx=4, dashed=dashed, stroke=PLAN if dashed else LINE)
            s += t(x + w / 2, y + 18, it, 12, fill=PLAN if dashed else INK)
            x += w + 10
        return s

    def group_label(y, text):
        return t(X0 + 20, y, text, 12, anchor="start", weight="bold", fill="#334155")

    b = ""
    # prezentacja
    b += layer(20, 112, "Warstwa prezentacji", "frontend: React + TypeScript (przeglądarka)", "#f3f7fc")
    b += group_label(66, "Widoki (src/pages)")
    b += chips(74, ["StronaStartowa", "PanelPracownika", "PanelKierownika", "PanelAdministratora"])
    b += chips(74, ["api.ts (wywołania REST)"], x0=X0 + 720)

    b += polyline([(W / 2, 132), (W / 2, 170)], end="open")
    b += t(W / 2 + 10, 156, "HTTP / REST (JSON)", 12, anchor="start", style="italic")

    # logika
    b += layer(172, 262, "Warstwa logiki biznesowej", "backend: Spring Boot (Java 21)", "#f6f9f4")
    b += group_label(218, "Kontrolery REST (controller)")
    b += chips(226, ["SesjaPracyController", "StatusController", "ObslugaBledow", "AktualnyUzytkownik"])
    b += group_label(282, "Serwisy (service)")
    b += chips(290, ["SesjaPracyService", "BladBiznesowyException", "NieZnalezionoException"])
    b += group_label(346, "Model dziedziny (model) i obiekty transferu danych (dto)")
    b += chips(354, ["Uzytkownik", "Dzial", "SesjaPracy", "Przerwa", "WniosekUrlopowy", "SesjaDto",
                     "StatusPracyDto", "PodsumowanieMiesiacaDto"])

    b += polyline([(W / 2, 434), (W / 2, 472)], end="open")
    b += t(W / 2 + 10, 458, "wywołania metod repozytoriów", 12, anchor="start", style="italic")

    # dane
    b += layer(474, 112, "Warstwa dostępu do danych", "Spring Data JPA + Hibernate", "#fbf7f2")
    b += group_label(520, "Repozytoria (repository)")
    b += chips(528, ["UzytkownikRepository", "DzialRepository", "SesjaPracyRepository", "WniosekUrlopowyRepository"])

    b += polyline([(W / 2, 586), (W / 2, 624)], end="open")
    b += t(W / 2 + 10, 610, "JDBC (SQL)", 12, anchor="start", style="italic")
    b += cylinder(W / 2, 626, 240, 80, "Baza danych", "PostgreSQL 16 (H2 w profilu dev)")
    return svg_doc(W, 726, b, "Diagram warstw")


# ================================================================ KOMPONENTY
def component(x, y, w, h, name, inner=(), plan=False):
    stroke = PLAN if plan else LINE
    col = PLAN if plan else INK
    s = rect(x, y, w, h, fill="#fff" if plan else "#f3f7fc", stroke=stroke, rx=4, dashed=plan, sw=1.4)
    # ikona komponentu UML
    ix, iy = x + w - 26, y + 8
    s += rect(ix, iy, 16, 20, fill="#fff", stroke=stroke, sw=1)
    s += rect(ix - 4, iy + 4, 8, 4, fill="#fff", stroke=stroke, sw=1)
    s += rect(ix - 4, iy + 12, 8, 4, fill="#fff", stroke=stroke, sw=1)
    s += t(x + w / 2 - 8, y + 20, "«component»", 11, style="italic", fill=col)
    s += t(x + w / 2 - 8, y + 37, name, 13, weight="bold", fill=col)
    for i, line in enumerate(inner):
        s += t(x + w / 2, y + 58 + i * 15, line, 11, fill="#475569" if not plan else PLAN)
    return s


def lollipop(x, y, label, dir_="up", anchor="start"):
    """Interfejs dostarczany: kolko na koncu krotkiej linii."""
    if dir_ == "up":
        s = f'<line x1="{x}" y1="{y}" x2="{x}" y2="{y - 22}" stroke="{LINE}" stroke-width="1.3"/>'
        s += f'<circle cx="{x}" cy="{y - 29}" r="7" fill="#fff" stroke="{LINE}" stroke-width="1.3"/>'
        s += t(x + 12, y - 26, label, 11, anchor=anchor, style="italic")
        return s, (x, y - 36)
    s = f'<line x1="{x}" y1="{y}" x2="{x + 22}" y2="{y}" stroke="{LINE}" stroke-width="1.3"/>'
    s += f'<circle cx="{x + 29}" cy="{y}" r="7" fill="#fff" stroke="{LINE}" stroke-width="1.3"/>'
    s += t(x + 30, y - 12, label, 11, anchor="middle", style="italic")
    return s, (x + 36, y)


def components():
    W, H = 1180, 640
    b = ""
    # frontend
    b += component(380, 20, 420, 92, "Frontend (React)",
                   ["StronaStartowa, PanelPracownika,", "PanelKierownika, PanelAdministratora, api.ts"])
    # backend
    b += rect(20, 170, 1140, 330, fill="#fbfcfe", rx=6, sw=1.5)
    b += t(36, 192, "Backend (Spring Boot)", 14, anchor="start", weight="bold")
    b += component(50, 250, 300, 104, "Czas pracy",
                   ["SesjaPracyController", "SesjaPracyService", "AktualnyUzytkownik"])
    b += component(440, 250, 300, 88, "Status systemu", ["StatusController"])
    b += component(830, 210, 300, 88, "Logowanie (JWT)", ["planowany, KM3"], plan=True)
    b += component(830, 310, 300, 80, "Konta i działy", ["planowany"], plan=True)
    b += component(830, 400, 300, 80, "Wnioski urlopowe", ["planowany"], plan=True)
    b += component(50, 400, 690, 84, "Model i repozytoria",
                   ["encje: Uzytkownik, Dzial, SesjaPracy, Przerwa, WniosekUrlopowy",
                    "repozytoria Spring Data JPA"])
    # interfejsy dostarczane przez komponenty backendu
    s1, p1 = lollipop(200, 250, "REST /api/sesje")
    s2, p2 = lollipop(590, 250, "REST /api/status")
    b += s1 + s2
    # frontend korzysta z interfejsow (zaleznosc)
    b += polyline([(470, 112), (470, 150), (200, 150), (200, p1[1] - 2)], dashed=True, end="open")
    b += polyline([(640, 112), (640, 150), (590, 150), (590, p2[1] - 2)], dashed=True, end="open")
    b += t(335, 145, "«use»", 11, style="italic")
    # frontend skorzysta tez z logowania (planowane)
    b += polyline([(760, 112), (760, 150), (980, 150), (980, 208)], dashed=True, end="open").replace(
        f'stroke="{LINE}"', f'stroke="{PLAN}"')
    # zaleznosci wewnatrz backendu
    b += polyline([(200, 354), (200, 398)], dashed=True, end="open")
    b += t(208, 381, "«use»", 11, anchor="start", style="italic")
    # baza danych
    b += polyline([(395, 484), (395, 548)], dashed=True, end="open")
    b += t(405, 520, "JDBC", 11, anchor="start", style="italic")
    b += cylinder(395, 550, 220, 76, "Baza danych", "PostgreSQL 16")
    # legenda
    b += rect(900, 560, 18, 14, fill="#fff", stroke=PLAN, dashed=True, sw=1.2)
    b += t(926, 572, "komponent planowany (KM3)", 12, anchor="start", fill="#475569")
    return svg_doc(W, H, b, "Diagram komponentów")


# ================================================================ SEKWENCJA
def sequence():
    lifelines = [
        ("Pracownik", "actor"),
        (":Frontend", "obj"),
        (":SesjaPracy\nController", "obj"),
        (":Aktualny\nUzytkownik", "obj"),
        (":SesjaPracy\nService", "obj"),
        (":Uzytkownik\nRepository", "obj"),
        (":SesjaPracy\nRepository", "obj"),
        ("Baza danych", "obj"),
    ]
    GAP, X0, TOP = 168, 80, 20
    xs = [X0 + i * GAP for i in range(len(lifelines))]
    H = 900
    W = xs[-1] + 90
    END = H - 30
    b = ""
    # naglowki i linie zycia
    for (name, kind), x in zip(lifelines, xs):
        if kind == "actor":
            b += km1.Actor(name, x, TOP + 40).svg()
            top = TOP + 100
        else:
            lines = name.split("\n")
            w = max(text_width(l, 12) for l in lines) + 20
            b += rect(x - w / 2, TOP + 10, w, 46, fill="#eef4fb", rx=3)
            y0 = TOP + 37 - (len(lines) - 1) * 7.5
            for i, l in enumerate(lines):
                b += t(x, y0 + i * 15, l, 12, weight="bold")
            top = TOP + 56
        b += (f'<line x1="{x}" y1="{top}" x2="{x}" y2="{END}" stroke="{LINE}" '
              f'stroke-width="1" stroke-dasharray="5,4"/>')

    def act(i, y1, y2):
        return rect(xs[i] - 6, y1, 12, y2 - y1, fill="#fff", sw=1.1)

    def msg(i, j, y, text, ret=False, num=None):
        x1 = xs[i] + (6 if j > i else -6)
        x2 = xs[j] + (-6 if j > i else 6)
        s = polyline([(x1, y), (x2, y)], dashed=ret, end="open")
        label = f"{num}. {text}" if num else text
        s += t((x1 + x2) / 2, y - 6, label, 11.5, style="italic" if ret else "normal")
        return s

    def self_msg(i, y, text, num):
        x = xs[i] + 6
        s = polyline([(x, y), (x + 40, y), (x + 40, y + 18), (x + 2, y + 18)], end="open")
        s += t(x + 46, y + 12, f"{num}. {text}", 11.5, anchor="start")
        return s

    # aktywacje
    b += act(1, 150, 840)
    b += act(2, 185, 800)
    b += act(3, 220, 252)
    b += act(4, 290, 760)
    b += act(5, 325, 357)
    b += act(6, 395, 427)
    b += act(6, 625, 690)
    b += act(7, 640, 675)

    y = 150
    b += msg(0, 1, y, "kliknięcie „Rozpocznij pracę”", num=1)
    b += msg(1, 2, 185, "POST /api/sesje/start", num=2)
    b += msg(2, 3, 220, "id()", num=3)
    b += msg(3, 2, 252, "uzytkownikId", ret=True)
    b += msg(2, 4, 290, "rozpocznijPrace(uzytkownikId)", num=4)
    b += msg(4, 5, 325, "findById(uzytkownikId)", num=5)
    b += msg(5, 4, 357, "uzytkownik", ret=True)
    b += msg(4, 6, 395, "findByUzytkownikAndZakonczenieIsNull(uzytkownik)", num=6)
    b += msg(6, 4, 427, "Optional (trwająca sesja lub pusty)", ret=True)

    # fragment alt
    fx1, fx2, fy1, fy2, fmid = xs[1] - 40, xs[7] + 60, 450, 780, 540
    b += rect(fx1, fy1, fx2 - fx1, fy2 - fy1, fill="none", sw=1.2)
    b += f'<path d="M{fx1},{fy1 + 22} L{fx1 + 46},{fy1 + 22} L{fx1 + 56},{fy1 + 12} L{fx1 + 56},{fy1}" fill="#fff" stroke="{LINE}" stroke-width="1.2"/>'
    b += t(fx1 + 24, fy1 + 16, "alt", 12, weight="bold")
    b += t(fx1 + 66, fy1 + 18, "[praca jest już rozpoczęta]", 11.5, anchor="start", weight="bold")
    b += msg(4, 2, 490, "BladBiznesowyException", ret=True)
    b += msg(2, 1, 515, "409 Conflict (komunikat błędu)", ret=True)
    b += (f'<line x1="{fx1}" y1="{fmid}" x2="{fx2}" y2="{fmid}" stroke="{LINE}" '
          f'stroke-width="1.2" stroke-dasharray="7,4"/>')
    b += t(fx1 + 10, fmid + 18, "[brak trwającej sesji]", 11.5, anchor="start", weight="bold")
    b += self_msg(4, 575, "teraz(): czas z zegara serwera", 7)
    b += msg(4, 6, 625, "save(new SesjaPracy(uzytkownik, teraz))", num=8)
    b += msg(6, 7, 640, "INSERT INTO sesja_pracy", num=9)
    b += msg(7, 6, 675, "id sesji", ret=True)
    b += msg(6, 4, 690, "sesja", ret=True)
    b += msg(4, 2, 730, "SesjaDto", ret=True)
    b += msg(2, 1, 760, "200 OK (SesjaDto w JSON)", ret=True)

    b += msg(1, 0, 830, "status „W pracy” i licznik czasu", ret=True)
    return svg_doc(W, H, b, "Diagram sekwencji")


# ================================================================ AKTYWNOSC
def activity():
    W, H = 1000, 960
    LX, SX = 260, 720           # srodki torow
    b = ""
    # tory (partycje)
    b += rect(20, 20, 960, H - 40, fill="none", sw=1.4)
    b += f'<line x1="490" y1="20" x2="490" y2="{H - 20}" stroke="{LINE}" stroke-width="1.4"/>'
    b += f'<line x1="20" y1="56" x2="980" y2="56" stroke="{LINE}" stroke-width="1.4"/>'
    b += t(255, 44, "Pracownik (frontend)", 14, weight="bold")
    b += t(735, 44, "System (backend)", 14, weight="bold")

    def action(x, y, text):
        lines = text.split("\n")
        w = max(text_width(l, 12.5) for l in lines) + 34
        h = 22 + 16 * len(lines)
        s = rect(x - w / 2, y - h / 2, w, h, fill="#eef4fb", rx=14)
        for i, l in enumerate(lines):
            s += t(x, y - (len(lines) - 1) * 8 + i * 16 + 5, l, 12.5)
        return s, w, h

    def node_start(x, y):
        return f'<circle cx="{x}" cy="{y}" r="11" fill="{INK}"/>'

    def node_end(x, y):
        return (f'<circle cx="{x}" cy="{y}" r="13" fill="#fff" stroke="{INK}" stroke-width="1.6"/>'
                f'<circle cx="{x}" cy="{y}" r="8" fill="{INK}"/>')

    def diamond(x, y):
        return f'<path d="M{x},{y - 18} L{x + 22},{y} L{x},{y + 18} L{x - 22},{y} z" fill="#fff" stroke="{LINE}" stroke-width="1.3"/>'

    def arrow(pts, guard=None, gpos=None, ganchor="start"):
        s = polyline(pts, end="open")
        if guard:
            s += t(gpos[0], gpos[1], guard, 11.5, anchor=ganchor, style="italic", bg=True)
        return s

    # wezly
    b += node_start(LX, 90)
    a1, _, h1 = action(LX, 150, "Kliknij „Rozpocznij pracę”")
    a2, _, h2 = action(SX, 215, "Sprawdź, czy pracownik\nma trwającą sesję")
    d1 = diamond(SX, 290)
    a3, w3, _ = action(880, 290, "Zwróć błąd 409")
    a4, _, h4 = action(SX, 365, "Zapisz rozpoczęcie pracy\n(czas serwera)")
    m1 = diamond(LX, 440)
    a5, _, h5 = action(LX, 505, "Wykonuj pracę")
    d2 = diamond(LX, 575)
    a6, w6, h6 = action(SX, 575, "Zapisz przerwę\n(początek i koniec)")
    a7, _, h7 = action(LX, 655, "Kliknij „Zakończ pracę”")
    a8, _, h8 = action(SX, 655, "Zakończ trwającą przerwę\ni zapisz zakończenie pracy")
    a9, _, h9 = action(SX, 745, "Policz czas pracy po odjęciu\nprzerw oraz nadgodziny")
    a10, _, h10 = action(LX, 825, "Zobacz czas pracy z dnia")
    b += a1 + a2 + d1 + a3 + a4 + m1 + a5 + d2 + a6 + a7 + a8 + a9 + a10
    b += node_end(880, 365)
    b += node_end(LX, 900)

    # przeplyw
    b += arrow([(LX, 101), (LX, 150 - h1 / 2)])
    b += arrow([(LX + 90, 150), (SX - 40, 150), (SX - 40, 215 - h2 / 2)])
    b += arrow([(SX, 215 + h2 / 2), (SX, 272)])
    b += arrow([(SX + 22, 290), (880 - w3 / 2, 290)], "[sesja trwa]", (SX + 30, 282))
    b += arrow([(880, 290 + 19), (880, 365 - 14)])
    b += arrow([(SX, 308), (SX, 365 - h4 / 2)], "[brak trwającej sesji]", (SX + 8, 330))
    b += arrow([(SX, 365 + h4 / 2), (SX, 410), (LX, 410), (LX, 422)])
    b += arrow([(LX, 458), (LX, 505 - h5 / 2)])
    b += arrow([(LX, 505 + h5 / 2), (LX, 557)])
    b += arrow([(LX + 22, 575), (SX - w6 / 2, 575)], "[przerwa]", (LX + 30, 567))
    b += arrow([(SX + w6 / 2, 575), (950, 575), (950, 440), (LX + 22, 440)])
    b += arrow([(LX, 593), (LX, 655 - h7 / 2)], "[koniec pracy]", (LX + 8, 618))
    b += arrow([(LX + 90, 655), (SX - 105, 655)])
    b += arrow([(SX, 655 + h8 / 2), (SX, 745 - h9 / 2)])
    b += arrow([(SX, 745 + h9 / 2), (SX, 790), (LX, 790), (LX, 825 - h10 / 2)])
    b += arrow([(LX, 825 + h10 / 2), (LX, 900 - 14)])
    return svg_doc(W, H, b, "Diagram aktywności")


if __name__ == "__main__":
    (OUT / "use_case.svg").write_text(km1.use_case(), encoding="utf-8")
    (OUT / "class.svg").write_text(class_diagram(), encoding="utf-8")
    (OUT / "layers.svg").write_text(layers(), encoding="utf-8")
    (OUT / "components.svg").write_text(components(), encoding="utf-8")
    (OUT / "sequence.svg").write_text(sequence(), encoding="utf-8")
    (OUT / "activity.svg").write_text(activity(), encoding="utf-8")
    print("OK:", ", ".join(p.name for p in sorted(OUT.glob("*.svg"))))
