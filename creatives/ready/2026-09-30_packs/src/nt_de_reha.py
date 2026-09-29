"""DE · реабилитационные и психосоматические клиники — 4 статики 1:1 (Pillow).

Без утверждений о состоянии зрителя, без «Sie» в вопросах о здоровье, без логотипов DRV / касс.
"""
import math
import random
import sys
sys.path.insert(0, "/home/user/alextest/creatives/ready/2026-09-30_packs/src")
from nt_lib import C, W, leaf, flower, rotpoly

DOC = "NT-rehab-clinic-de-2026-09-30"
FOREST = (26, 78, 64)
SAGE = (120, 168, 140)
BTN = (226, 84, 50)
GRAY = (92, 102, 110)
INK = (28, 36, 44)
CTA = "Mehr erfahren"


# ---------- иконки
def ic_bone(c, cx, cy, s=1.0, col=(255, 255, 255)):
    k = s
    pts = [(cx - 44 * k, cy - 12 * k), (cx + 44 * k, cy - 12 * k), (cx + 44 * k, cy + 12 * k), (cx - 44 * k, cy + 12 * k)]
    c.poly(rotpoly(pts, cx, cy, -40), col)
    for sx in (-1, 1):
        ex, ey = rotpoly([(cx + sx * 46 * k, cy)], cx, cy, -40)[0]
        nx, ny = rotpoly([(ex, ey - 14 * k), (ex, ey + 14 * k)], ex, ey, -40)
        for px, py in (nx, ny):
            c.ellipse((px - 16 * k, py - 16 * k, px + 16 * k, py + 16 * k), fill=col)


def ic_lotus(c, cx, cy, s=1.0, col=(255, 255, 255)):
    k = s
    leaf(c, cx, cy - 16 * k, 72 * k, 34 * k, -90, col)
    leaf(c, cx - 26 * k, cy - 4 * k, 66 * k, 30 * k, -135, col)
    leaf(c, cx + 26 * k, cy - 4 * k, 66 * k, 30 * k, -45, col)
    c.rect((cx - 46 * k, cy + 22 * k, cx + 46 * k, cy + 30 * k), fill=col, r=4 * k)


def ic_heart(c, cx, cy, s=1.0, col=(255, 255, 255)):
    k = s
    c.ellipse((cx - 42 * k, cy - 36 * k, cx + 2 * k, cy + 8 * k), fill=col)
    c.ellipse((cx - 2 * k, cy - 36 * k, cx + 42 * k, cy + 8 * k), fill=col)
    c.poly([(cx - 40 * k, cy - 4 * k), (cx + 40 * k, cy - 4 * k), (cx, cy + 40 * k)], col)


def ic_brain(c, cx, cy, s=1.0, col=(255, 255, 255), line=None):
    k = s
    for (dx, dy, r) in ((-20, -14, 24), (6, -22, 24), (26, -4, 22), (-26, 10, 22), (4, 8, 26), (24, 18, 18)):
        c.ellipse((cx + (dx - r) * k, cy + (dy - r) * k, cx + (dx + r) * k, cy + (dy + r) * k), fill=col)
    if line:
        c.line([(cx - 2 * k, cy - 40 * k), (cx - 6 * k, cy - 10 * k), (cx + 2 * k, cy + 14 * k), (cx - 4 * k, cy + 34 * k)], line, 4 * k)
        c.arc((cx - 34 * k, cy - 20 * k, cx - 10 * k, cy + 4 * k), 200, 340, line, 4 * k)
        c.arc((cx + 10 * k, cy - 6 * k, cx + 36 * k, cy + 20 * k), 180, 330, line, 4 * k)


def a():
    """Сетка-выбор списком: 4 направления реабилитации, у каждого «Mehr erfahren»."""
    c = C((244, 248, 245))
    c.vgrad((0, 0, W, 300), (228, 242, 234), (244, 248, 245))
    y = c.block("Die besten Rehakliniken\nin Deutschland 2026", "db", 60, 40, 1000, FOREST, max_lines=2)
    y = c.block("Nach Fachrichtung vergleichen:", "sb", 36, y + 8, 1000, INK, max_lines=1)
    rows = [("Orthopädie", "Rücken, Hüfte, Knie", ic_bone, (70, 130, 190)),
            ("Psychosomatik", "Körper und Psyche", ic_lotus, (46, 150, 120)),
            ("Kardiologie", "Herz und Kreislauf", ic_heart, (214, 76, 76)),
            ("Neurologie", "Gehirn und Nerven", ic_brain, (150, 100, 190))]
    ry = y + 26
    rh, gap = 170, 20
    for lab, sub, ic, col in rows:
        box = (50, ry, 1030, ry + rh)
        c.card(box, fill=(255, 255, 255), r=28, sh_alpha=45, blur=10, off=(0, 5))
        c.rect((box[0], box[1], box[0] + 14, box[3]), fill=col, r=7)
        cx, cy = box[0] + 110, ry + rh / 2
        c.ellipse((cx - 62, cy - 62, cx + 62, cy + 62), fill=col)
        ic(c, cx, cy + (4 if ic is ic_heart else 0), 0.95, (255, 255, 255)) if ic is not ic_brain else ic(c, cx, cy, 0.95, (255, 255, 255), line=col)
        c.text((box[0] + 204, cy - 22), lab, "db", 44, INK, anchor="lm")
        c.text((box[0] + 206, cy + 30), sub, "s", 30, GRAY, anchor="lm")
        c.button(CTA, box[2] - 162, cy, size=28, fill=BTN, padx=26, pady=14, shadow=False)
        ry += rh + gap
    c.save(f"{DOC}/a.png")


def b():
    """Карточка-опросник: кто оплачивает Reha (знание, а не состояние зрителя)."""
    c = C((226, 238, 230))
    c.vgrad((0, 0, W, W), (232, 243, 236), (206, 226, 214))
    random.seed(4)
    for (x, y_, ang) in ((70, 140, -60), (40, 230, -20), (1010, 860, 120), (1040, 960, 160), (1050, 300, 200)):
        leaf(c, x, y_, 150, 56, ang, SAGE, alpha=110)
    y = c.block("Reha beantragen 2026", "db", 64, 50, 1000, FOREST, max_lines=1)
    y = c.block("Das Quiz, bei dem viele danebenliegen", "s", 36, y + 2, 1000, GRAY, max_lines=1)
    card = (90, y + 36, 990, 890)
    c.card(card, fill=(255, 255, 255), r=34, sh_alpha=70, blur=18, off=(0, 10))
    x0, x1 = card[0] + 50, card[2] - 50
    c.text((x0, card[1] + 60), "REHA-QUIZ", "db", 28, (46, 150, 120), anchor="lm")
    c.text((x1, card[1] + 60), "Frage 1 von 3", "s", 28, GRAY, anchor="rm")
    for k in range(3):
        c.ellipse((x0 + 230 + k * 26, card[1] + 52, x0 + 246 + k * 26, card[1] + 68), fill=(46, 150, 120) if k == 0 else (214, 222, 218))
    qy = c.block("Wer übernimmt die Kosten einer Reha?", "db", 48, card[1] + 108, x1 - x0, INK, align="left", x=x0, max_lines=2)
    opts = ["Die Krankenkasse", "Die Rentenversicherung", "Beide – je nach Fall", "Man zahlt selbst"]
    oy = qy + 22
    for o in opts:
        c.rect((x0, oy, x1, oy + 84), fill=(246, 249, 247), r=42, outline=(196, 212, 204), width=2)
        c.ellipse((x0 + 26, oy + 24, x0 + 62, oy + 60), fill=(255, 255, 255), outline=(130, 150, 140), width=3)
        c.text((x0 + 88, oy + 42), o, "sb", 34, INK, anchor="lm")
        oy += 100
    c.button(CTA, W / 2, 970, size=44, fill=BTN, padx=60)
    c.save(f"{DOC}/b.png")


def bed_icon(c, cx, cy, col):
    c.rect((cx - 70, cy - 36, cx - 56, cy + 44), fill=col, r=4)
    c.rect((cx - 56, cy + 4, cx + 70, cy + 24), fill=col, r=4)
    c.rect((cx + 60, cy + 4, cx + 72, cy + 44), fill=col, r=3)
    c.rect((cx - 52, cy - 14, cx + 66, cy + 6), fill=(255, 255, 255), r=8)
    c.rect((cx - 50, cy - 30, cx - 14, cy - 8), fill=(255, 255, 255), r=8)


def house_icon(c, cx, cy, col):
    c.poly([(cx - 70, cy - 4), (cx, cy - 62), (cx + 70, cy - 4)], col)
    c.rect((cx - 52, cy - 8, cx + 52, cy + 48), fill=col)
    c.rect((cx - 14, cy + 12, cx + 14, cy + 48), fill=(255, 255, 255), r=4)
    c.rect((cx + 22, cy + 2, cx + 42, cy + 22), fill=(255, 255, 255), r=3)


def c_():
    """Сравнение: стационарная или амбулаторная Reha."""
    c = C((250, 250, 247))
    y = c.block("Reha 2026:", "db", 60, 40, 1000, INK, max_lines=1)
    y = c.block("stationär oder ambulant?", "db", 64, y, 1000, FOREST, max_lines=1, highlight=(214, 238, 222), hl_pad=12)
    cols = [("STATIONÄR", (46, 110, 160), bed_icon, ["in der Klinik", "Therapie und Erholung vor Ort", "?"]),
            ("AMBULANT", (46, 150, 120), house_icon, ["zu Hause", "Therapie tagsüber, abends daheim", "?"])]
    rows = ["Übernachtung", "Tagesablauf", "Zuzahlung 2026"]
    top = y + 40
    for i, (title, col, ic, vals) in enumerate(cols):
        x0 = 50 + i * 500
        box = (x0, top, x0 + 480, 850)
        c.card(box, fill=(255, 255, 255), r=28, sh_alpha=50, blur=12, off=(0, 6))
        c.rect((box[0], box[1], box[2], box[1] + 176), fill=col, r=28)
        c.rect((box[0], box[1] + 120, box[2], box[1] + 176), fill=col)
        ic(c, x0 + 240, top + 70, (255, 255, 255))
        c.text((x0 + 240, top + 148), title, "db", 36, (255, 255, 255), anchor="mm")
        ry = top + 206
        for lab, v in zip(rows, vals):
            c.text((x0 + 36, ry), lab.upper(), "sb", 22, GRAY, anchor="la")
            if v == "?":
                c.rect((x0 + 36, ry + 34, x0 + 150, ry + 86), fill=(255, 238, 186), r=26)
                c.text((x0 + 93, ry + 60), "? €", "db", 32, (120, 70, 0), anchor="mm")
            else:
                c.block(v, "sb", 32, ry + 34, 410, INK, align="left", x=x0 + 36, max_lines=2)
            ry += 136 if lab == "Tagesablauf" else 116
    c.text((W / 2, 902), "Und welche Klinik ist empfehlenswert?", "sb", 36, INK, anchor="mm")
    c.button(CTA, W / 2, 996, size=42, fill=BTN, padx=56)
    c.save(f"{DOC}/c.png")


def tree(c, x, base, h, col=(70, 130, 90), trunk=(120, 90, 60)):
    c.rect((x - 7, base - h * 0.35, x + 7, base), fill=trunk)
    c.ellipse((x - h * 0.32, base - h, x + h * 0.32, base - h * 0.3), fill=col)


def pine(c, x, base, h, col=(46, 104, 76)):
    c.rect((x - 5, base - 18, x + 5, base), fill=(110, 80, 56))
    for k in range(3):
        w_ = h * (0.42 - k * 0.1)
        yy = base - 14 - k * h * 0.26
        c.poly([(x - w_, yy), (x + w_, yy), (x, yy - h * 0.44)], col)


def d():
    """Сцена-иллюстрация: клиника у озера среди холмов, скамейка на дорожке."""
    c = C((200, 226, 240))
    c.vgrad((0, 0, W, 640), (170, 208, 236), (226, 240, 246))
    c.ellipse((820, 70, 940, 190), fill=(255, 230, 150))
    c.glow((760, 10, 1000, 250), (255, 240, 190), alpha=120, blur=40)
    # холмы
    c.poly([(0, 560), (180, 420), (380, 520), (560, 400), (760, 500), (920, 430), (1080, 520), (1080, 700), (0, 700)], (150, 190, 160))
    c.poly([(0, 620), (240, 520), (520, 600), (820, 520), (1080, 600), (1080, 760), (0, 760)], (118, 170, 130))
    # озеро
    c.poly([(0, 700), (1080, 660), (1080, 820), (0, 860)], (120, 176, 210))
    for k in range(6):
        yy = 700 + k * 22
        c.line([(120 + k * 90, yy), (260 + k * 90, yy)], (200, 228, 244), 3, alpha=180)
    # клиника
    bx0, by0, bx1, by1 = 420, 470, 860, 690
    c.rect((bx0 - 6, by0 - 30, bx1 + 6, by0 + 4), fill=(170, 90, 70))
    c.rect((bx0, by0, bx1, by1), fill=(250, 248, 242))
    c.rect((bx0 + 150, by0 - 90, bx0 + 300, by0), fill=(246, 244, 236))
    c.rect((bx0 + 144, by0 - 106, bx0 + 306, by0 - 86), fill=(170, 90, 70))
    for r_ in range(3):
        for q in range(9):
            wx = bx0 + 24 + q * 46
            wy = by0 + 22 + r_ * 54
            c.rect((wx, wy, wx + 28, wy + 34), fill=(150, 196, 226), r=3)
    for q in range(3):
        wx = bx0 + 170 + q * 42
        c.rect((wx, by0 - 70, wx + 26, by0 - 36), fill=(150, 196, 226), r=3)
    c.rect((bx0 + 200, by1 - 56, bx0 + 250, by1), fill=(120, 90, 60), r=4)
    # деревья
    for (x, h) in ((360, 160), (320, 120), (900, 170), (960, 130), (1020, 150)):
        pine(c, x, 700, h)
    for (x, h) in ((80, 150), (170, 120), (260, 140)):
        tree(c, x, 710, h)
    # берег, дорожка и скамейка
    c.poly([(0, 850), (1080, 810), (1080, W), (0, W)], (140, 188, 140))
    c.poly([(560, 816), (660, 812), (840, W), (560, W)], (226, 210, 180))
    c.rect((300, 860, 470, 876), fill=(150, 104, 66), r=4)
    c.rect((300, 832, 470, 846), fill=(150, 104, 66), r=4)
    for x in (312, 454):
        c.rect((x, 876, x + 8, 910), fill=(90, 70, 50))
    for (x, y_) in ((120, 940), (220, 980), (940, 900), (1010, 960)):
        flower(c, x, y_, 18, (255, 255, 255), (246, 206, 90), n=5)
    # карточка с текстом
    card = (60, 36, 1020, 330)
    c.card(card, fill=(255, 255, 255), r=30, sh_alpha=70, blur=16, off=(0, 8))
    y = c.block("Welche Rehaklinik ist empfehlenswert?", "db", 50, 64, 900, FOREST, max_lines=2)
    c.block("Orthopädie · Psychosomatik · Kardiologie\nKliniken im Vergleich 2026", "s", 34, y + 8, 900, INK, max_lines=2)
    c.button(CTA, W / 2, 990, size=44, fill=BTN, padx=60)
    c.save(f"{DOC}/d.png")


if __name__ == "__main__":
    for f in sys.argv[1:] or ["a", "b", "c", "d"]:
        globals()[f if f != "c" else "c_"]()
