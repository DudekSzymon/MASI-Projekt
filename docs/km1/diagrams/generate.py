"""Generator diagramow UML (SVG) dla KM1.

Uruchomienie:  python generate.py
Wynik:         use_case.svg, class.svg (w tym samym katalogu)

Diagramy sa rysowane recznie (bez zewnetrznych bibliotek), wspolrzedne
elementow sa ustawione w funkcjach use_case() i class_diagram().
"""
from __future__ import annotations

import math
from html import escape
from pathlib import Path

OUT = Path(__file__).resolve().parent
FONT = "Arial, Helvetica, sans-serif"
INK = "#1f2933"
LINE = "#334155"


# --------------------------------------------------------------- pomocnicze
def text_width(s: str, size: float) -> float:
    w = 0.0
    for ch in s:
        if ch in "iljtfrł.,:;'!|()[]{} ":
            w += 0.30
        elif ch in "mwMW":
            w += 0.86
        elif ch.isupper():
            w += 0.68
        elif ch.isdigit():
            w += 0.56
        elif ch in "<>«»=*+-_/":
            w += 0.58
        else:
            w += 0.53
    return w * size


def t(x, y, s, size=12, anchor="middle", weight="normal", style="normal", fill=INK, bg=False):
    out = ""
    if bg:
        w = text_width(s, size) + 6
        x0 = x - w / 2 if anchor == "middle" else (x - 3 if anchor == "start" else x - w + 3)
        out += f'<rect x="{x0:.1f}" y="{y - size + 1:.1f}" width="{w:.1f}" height="{size + 3}" fill="#fff"/>'
    out += (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{FONT}" font-size="{size}" '
            f'text-anchor="{anchor}" font-weight="{weight}" font-style="{style}" fill="{fill}">{escape(s)}</text>')
    return out


DEFS = f"""<defs>
<marker id="tri" viewBox="0 0 14 14" refX="14" refY="7" markerWidth="14" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto">
  <path d="M1,1 L14,7 L1,13 z" fill="#fff" stroke="{LINE}" stroke-width="1.2"/></marker>
<marker id="open" viewBox="0 0 12 12" refX="11" refY="6" markerWidth="12" markerHeight="12" markerUnits="userSpaceOnUse" orient="auto">
  <path d="M1,1 L11,6 L1,11" fill="none" stroke="{LINE}" stroke-width="1.3"/></marker>
<marker id="diamond" viewBox="0 0 18 10" refX="0" refY="5" markerWidth="18" markerHeight="10" markerUnits="userSpaceOnUse" orient="auto">
  <path d="M0,5 L9,0 L18,5 L9,10 z" fill="{LINE}"/></marker>
</defs>"""


def svg_doc(w, h, body, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
            f'<title>{escape(title)}</title>{DEFS}<rect width="{w}" height="{h}" fill="#fff"/>{body}</svg>\n')


def polyline(pts, dashed=False, start=None, end=None):
    d = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    attrs = f'fill="none" stroke="{LINE}" stroke-width="1.3"'
    if dashed:
        attrs += ' stroke-dasharray="6,4"'
    if start:
        attrs += f' marker-start="url(#{start})"'
    if end:
        attrs += f' marker-end="url(#{end})"'
    return f'<polyline points="{d}" {attrs}/>'


# ================================================================ USE CASE
class UC:
    def __init__(self, uid, name, cx, cy, size=13):
        self.uid, self.name, self.cx, self.cy, self.size = uid, name, cx, cy, size
        self.lines = [name] if text_width(name, size) < 210 else self._split(name)
        widest = max(text_width(s, size) for s in self.lines)
        self.rx = max(widest / 2 + 26, 78)
        self.ry = 25 if len(self.lines) == 1 else 33

    @staticmethod
    def _split(s):
        words = s.split()
        best = None
        for i in range(1, len(words)):
            a, b = " ".join(words[:i]), " ".join(words[i:])
            score = abs(len(a) - len(b))
            if best is None or score < best[0]:
                best = (score, a, b)
        return [best[1], best[2]]

    def edge_point(self, px, py):
        dx, dy = px - self.cx, py - self.cy
        k = 1 / math.sqrt((dx / self.rx) ** 2 + (dy / self.ry) ** 2)
        return self.cx + dx * k, self.cy + dy * k

    def svg(self):
        s = (f'<ellipse cx="{self.cx}" cy="{self.cy}" rx="{self.rx:.1f}" ry="{self.ry}" '
             f'fill="#eef4fb" stroke="{LINE}" stroke-width="1.3"/>')
        n = len(self.lines)
        y0 = self.cy - (n - 1) * 8 + 11
        s += t(self.cx, y0 - 17, self.uid, 10, fill="#64748b")
        for i, line in enumerate(self.lines):
            s += t(self.cx, y0 + i * 16, line, self.size)
        return s


class Actor:
    def __init__(self, name, x, y):
        self.name, self.x, self.y = name, x, y  # (x, y) = srodek tulowia

    @property
    def head_top(self):
        return self.x, self.y - 38

    @property
    def feet(self):
        return self.x, self.y + 30

    def port(self, side):
        return (self.x + 20, self.y - 8) if side == "R" else (self.x - 20, self.y - 8)

    def svg(self):
        x, y = self.x, self.y
        s = f'<g stroke="{INK}" stroke-width="1.6" fill="none">'
        s += f'<circle cx="{x}" cy="{y - 28}" r="10" fill="#fff"/>'
        s += f'<line x1="{x}" y1="{y - 18}" x2="{x}" y2="{y + 8}"/>'
        s += f'<line x1="{x - 16}" y1="{y - 8}" x2="{x + 16}" y2="{y - 8}"/>'
        s += f'<line x1="{x}" y1="{y + 8}" x2="{x - 12}" y2="{y + 28}"/>'
        s += f'<line x1="{x}" y1="{y + 8}" x2="{x + 12}" y2="{y + 28}"/></g>'
        for i, part in enumerate(self.name.split("\n")):
            s += t(x, y + 46 + i * 15, part, 13, weight="bold")
        return s


def assoc(actor: Actor, uc: UC, side):
    p = actor.port(side)
    return polyline([p, uc.edge_point(*p)])


def relation(src: UC, dst: UC, label, label_dx=0, label_dy=0):
    a = src.edge_point(dst.cx, dst.cy)
    b = dst.edge_point(src.cx, src.cy)
    mx, my = (a[0] + b[0]) / 2 + label_dx, (a[1] + b[1]) / 2 + label_dy
    return polyline([a, b], dashed=True, end="open") + t(mx, my + 4, f"«{label}»", 11, style="italic", bg=True)


def use_case():
    W, H = 1100, 760
    A, B = 400, 720  # kolumny przypadkow uzycia
    uc = {u.uid: u for u in [
        UC("UC01", "Zaloguj się", 560, 88),
        UC("UC02", "Rozpocznij pracę", A, 180),
        UC("UC03", "Rozpocznij / zakończ przerwę", A, 245),
        UC("UC04", "Zakończ pracę", A, 310),
        UC("UC05", "Przeglądaj swój czas pracy", A, 375),
        UC("UC06", "Złóż wniosek o urlop", A - 40, 450),
        UC("UC07", "Przeglądaj czas pracy działu", A, 550),
        UC("UC08", "Rozpatrz wniosek o urlop", A, 615),
        UC("UC09", "Generuj raport miesięczny", A, 680),
        UC("UC10", "Zarządzaj kontami użytkowników", B, 180),
        UC("UC11", "Zarządzaj działami", B, 245),
        UC("UC12", "Popraw wpis czasu pracy", B, 310),
    ]}
    prac = Actor("Pracownik", 90, 260)
    kier = Actor("Kierownik", 90, 615)
    admin = Actor("Administrator", 1010, 250)

    body = (f'<rect x="205" y="28" width="700" height="705" rx="6" fill="#fbfdff" '
            f'stroke="{LINE}" stroke-width="1.5"/>')
    body += t(555, 50, "System rejestracji czasu pracy", 15, weight="bold")

    for k in ["UC01", "UC02", "UC03", "UC04", "UC05", "UC06"]:
        body += assoc(prac, uc[k], "R")
    for k in ["UC07", "UC08", "UC09"]:
        body += assoc(kier, uc[k], "R")
    for k in ["UC01", "UC10", "UC11", "UC12"]:
        body += assoc(admin, uc[k], "L")

    # generalizacja aktorow: Kierownik jest Pracownikiem
    body += polyline([kier.head_top, (prac.feet[0], prac.feet[1] + 42)], end="tri")

    for u in uc.values():
        body += u.svg()
    for a in (prac, kier, admin):
        body += a.svg()
    return svg_doc(W, H, body, "Diagram przypadków użycia")


# ================================================================ KLASY
class Box:
    PAD, LH, SIZE = 8, 16, 12.5

    def __init__(self, name, x, y, attrs=(), methods=(), stereo=None, abstract=False, enum=False):
        self.name, self.x, self.y = name, x, y
        self.attrs, self.methods = list(attrs), list(methods)
        self.stereo, self.abstract, self.enum = stereo, abstract, enum
        self.head = 26 + (14 if stereo else 0)
        rows = [text_width(s, self.SIZE) for s in self.attrs + self.methods]
        rows.append(text_width(name, 14) + 10)
        if stereo:
            rows.append(text_width(stereo, 11))
        self.w = max(rows) + 2 * self.PAD
        self.ha = len(self.attrs) * self.LH + 10
        self.hm = 0 if enum else (len(self.methods) * self.LH + 10 if self.methods else 10)
        self.h = self.head + self.ha + self.hm

    # punkty zaczepienia
    def L(self, y): return self.x, y
    def R(self, y): return self.x + self.w, y
    def T(self, x=None): return (self.x + self.w / 2 if x is None else x), self.y
    def B(self, x=None): return (self.x + self.w / 2 if x is None else x), self.y + self.h
    @property
    def cx(self): return self.x + self.w / 2
    @property
    def bottom(self): return self.y + self.h
    @property
    def right(self): return self.x + self.w

    def svg(self):
        x, y, w = self.x, self.y, self.w
        fill = "#f3f0fb" if self.enum else "#eef4fb"
        s = f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{self.h:.1f}" fill="#fff" stroke="{LINE}" stroke-width="1.3"/>'
        s += f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{self.head}" fill="{fill}" stroke="{LINE}" stroke-width="1.3"/>'
        ny = y + 18
        if self.stereo:
            s += t(x + w / 2, y + 15, self.stereo, 11, style="italic", fill="#475569")
            ny += 14
        s += t(x + w / 2, ny, self.name, 14, weight="bold", style="italic" if self.abstract else "normal")
        cy = y + self.head + 4
        for a in self.attrs:
            cy += self.LH
            s += t(x + self.PAD, cy - 3, a, self.SIZE, anchor="start")
        if not self.enum:
            sep = y + self.head + self.ha
            s += f'<line x1="{x:.1f}" y1="{sep:.1f}" x2="{x + w:.1f}" y2="{sep:.1f}" stroke="{LINE}" stroke-width="1.1"/>'
            cy = sep + 4
            for m in self.methods:
                cy += self.LH
                s += t(x + self.PAD, cy - 3, m, self.SIZE, anchor="start")
        return s


def mult(p, q, text):
    """Krotnosc przy punkcie p na odcinku p->q."""
    dx, dy = q[0] - p[0], q[1] - p[1]
    if abs(dx) >= abs(dy):
        sx = 1 if dx > 0 else -1
        return t(p[0] + sx * 6, p[1] - 5, text, 12, anchor="start" if sx > 0 else "end")
    sy = 1 if dy > 0 else -1
    return t(p[0] + 6, p[1] + (17 if sy > 0 else -7), text, 12, anchor="start")


def link(pts, m1=None, m2=None, label=None, lpos=None, kind="assoc", lanchor="middle"):
    start = "diamond" if kind == "comp" else None
    end = {"gen": "tri", "dep": "open", "nav": "open"}.get(kind)
    s = polyline(pts, dashed=(kind == "dep"), start=start, end=end)
    if m1:
        s += mult(pts[0], pts[1], m1)
    if m2:
        s += mult(pts[-1], pts[-2], m2)
    if label:
        s += t(lpos[0], lpos[1], label, 12, anchor=lanchor, style="italic", bg=True)
    return s


def class_diagram():
    C0, C1, C2 = 20, 390, 850
    TOP = 30

    uz = Box("Uzytkownik", C1, TOP, [
        "- id: Long", "- imie: String", "- nazwisko: String", "- email: String",
        "- hasloHash: String", "- rola: Rola", "- aktywny: boolean", "- normaDzienna: int"],
        ["+ dezaktywuj(): void", "+ czasPracy(od: LocalDate, do: LocalDate): Duration"])
    dz = Box("Dzial", C0, TOP + 20, ["- id: Long", "- nazwa: String"])
    wn = Box("WniosekUrlopowy", C2, TOP, [
        "- id: Long", "- dataOd: LocalDate", "- dataDo: LocalDate",
        "- status: StatusWniosku", "- komentarz: String"],
        ["+ zatwierdz(): void", "+ odrzuc(powod: String): void"])
    sesja = Box("SesjaPracy", C1, uz.bottom + 80, [
        "- id: Long", "- rozpoczecie: LocalDateTime", "- zakonczenie: LocalDateTime"],
        ["+ zakoncz(): void", "+ czasPracy(): Duration", "+ nadgodziny(norma: int): Duration"])
    przerwa = Box("Przerwa", C2, sesja.y, [
        "- id: Long", "- rozpoczecie: LocalDateTime", "- zakonczenie: LocalDateTime"],
        ["+ czasTrwania(): Duration"])
    rola = Box("Rola", C0, dz.bottom + 110, ["PRACOWNIK", "KIEROWNIK", "ADMINISTRATOR"],
               stereo="«enumeration»", enum=True)
    status = Box("StatusWniosku", C0, rola.bottom + 30, ["OCZEKUJACY", "ZATWIERDZONY", "ODRZUCONY"],
                 stereo="«enumeration»", enum=True)

    boxes = [uz, dz, wn, sesja, przerwa, rola, status]
    W = int(max(b.right for b in boxes) + 30)
    H = int(max(b.bottom for b in boxes) + 25)

    b = ""
    # Uzytkownik - Dzial
    y1, y2 = dz.y + 25, dz.y + 60
    b += link([uz.L(y1), dz.R(y1)], "*", "1", "należy do", ((uz.x + dz.right) / 2, y1 - 6))
    b += link([uz.L(y2), dz.R(y2)], "1", "0..*", "kieruje", ((uz.x + dz.right) / 2, y2 - 6))
    # Uzytkownik - SesjaPracy
    b += link([uz.B(uz.cx), sesja.T(uz.cx)], "1", "*", "rejestruje",
              (uz.cx + 8, (uz.bottom + sesja.y) / 2 + 4), lanchor="start")
    # SesjaPracy <>- Przerwa (kompozycja)
    yp = sesja.y + 50
    b += link([sesja.R(yp), przerwa.L(yp)], "1", "0..*", "zawiera",
              ((sesja.right + przerwa.x) / 2, yp - 8), kind="comp")
    # Uzytkownik - WniosekUrlopowy
    w1, w2 = wn.y + 45, wn.y + 105
    b += link([uz.R(w1), wn.L(w1)], "1", "*", "składa", ((uz.right + wn.x) / 2, w1 - 6))
    b += link([uz.R(w2), wn.L(w2)], "0..1", "*", "rozpatruje", ((uz.right + wn.x) / 2, w2 - 6))

    for box in boxes:
        b += box.svg()
    b += t(C0, rola.y - 14, "Typy wyliczeniowe:", 12, anchor="start", style="italic", fill="#475569")
    return svg_doc(W, H, b, "Wstępny diagram klas")


if __name__ == "__main__":
    (OUT / "use_case.svg").write_text(use_case(), encoding="utf-8")
    (OUT / "class.svg").write_text(class_diagram(), encoding="utf-8")
    print("OK:", OUT / "use_case.svg", OUT / "class.svg")
