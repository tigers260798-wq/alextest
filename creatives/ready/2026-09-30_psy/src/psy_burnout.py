import sys
sys.path.insert(0, "/tmp/claude-0/-home-user-alextest/f5dce882-fce7-5270-9036-ca9a0fe43d5e/scratchpad")
from psy_lib import C, W
import math

RED = (226, 56, 48)
INK = (38, 38, 46)


def a():
    """Иллюстрация: 12 спичек, последние 4 сгорели."""
    c = C((248, 241, 230))
    c.vgrad((0, 0, W, 690), (250, 244, 234), (238, 226, 208))
    c.vgrad((0, 690, W, W), (214, 176, 132), (196, 156, 112))
    c.rect((0, 686, W, 694), fill=(186, 146, 104))
    for gy in (760, 842, 930, 1010):
        c.line([(0, gy), (W, gy + 6)], (190, 150, 108), 2, alpha=120)
    y = c.block("Burnout oder Depression?", "db", 78, 58, 960, INK, max_lines=2)
    y = c.block("12 Fragen, die Ärzte stellen", "db", 52, y + 10, 960, RED)
    c.block("… und wann die Krankenkasse die Klinik oder Kur zahlt", "s", 32, y + 8, 900, (90, 84, 78))
    # спички
    n, x0, step = 12, 125, 75
    base = 880
    for i in range(n):
        x = x0 + i * step
        burnt = i >= 8
        top = 530 if not burnt else 560 + (i - 8) * 22
        # тень
        c.ellipse((x - 26, base - 8, x + 40, base + 12), fill=(90, 60, 30), alpha=70)
        # палочка
        c.rect((x - 9, top + 20, x + 9, base), fill=(238, 206, 158), r=4)
        c.rect((x + 3, top + 20, x + 9, base), fill=(214, 178, 128), r=3)
        if not burnt:
            c.ellipse((x - 17, top - 18, x + 17, top + 40), fill=(206, 44, 36))
            c.ellipse((x - 9, top - 8, x + 1, top + 10), fill=(240, 120, 110), alpha=200)
        else:
            char = top + 20 + 150
            c.vgrad((x - 9, top + 90, x + 9, char), (40, 36, 34), (226, 190, 140))
            c.rect((x - 9, top + 20, x + 9, top + 92), fill=(40, 36, 34), r=4)
            # скрученная обгоревшая головка
            c.ellipse((x - 14, top - 6, x + 12, top + 30), fill=(30, 28, 28))
            c.ellipse((x - 4, top - 14, x + 18, top + 8), fill=(55, 50, 48))
            # дым
            for k in range(3):
                pts = []
                for t in range(0, 60):
                    yy = top - 26 - t * 3.0
                    if yy < 445:
                        break
                    xx = x + 2 + math.sin(t / 7 + k * 2.1 + i) * (8 + t * 0.35) + k * 6
                    pts.append((xx, yy))
                c.line(pts, (150, 150, 155), 3, alpha=90 - k * 20)
        c.text((x, base + 40), str(i + 1), "sb", 26, (120, 86, 52), anchor="mm")
    c.button("Mehr erfahren", W / 2, 1000, size=42, fill=RED)
    c.save("psy-burnout-de-0929_a.png")


def b():
    """Карточка-опросник (фейковая интерактивность) на бирюзовом фоне."""
    c = C((20, 84, 96))
    c.vgrad((0, 0, W, W), (22, 96, 108), (12, 48, 66))
    c.ellipse((760, -120, 1220, 340), fill=(255, 255, 255), alpha=18)
    c.ellipse((-160, 780, 260, 1200), fill=(255, 255, 255), alpha=14)
    y = c.block("Burnout oder Depression?", "db", 62, 46, 980, (255, 255, 255), max_lines=1)
    c.block("12 Fragen, die Ärzte stellen", "sb", 44, y + 4, 980, (255, 214, 102))
    box = (80, 222, 1000, 880)
    c.card(box, r=36, sh_alpha=120, blur=22)
    c.text((130, 262), "SELBSTTEST", "sb", 26, (22, 110, 120))
    c.text((950, 262), "Frage 3 von 12", "s", 28, (110, 116, 124), anchor="ra")
    c.rect((130, 312, 950, 326), fill=(226, 232, 236), r=7)
    c.rect((130, 312, 130 + 820 * 3 / 12, 326), fill=(22, 150, 160), r=7)
    y = c.block("Nach dem Wochenende noch genauso müde – wie oft?", "db", 44, 356, 820, INK, align="left", x=130, max_lines=2)
    opts = ["Nie", "Manchmal", "Oft", "Fast immer"]
    oy = y + 18
    for o in opts:
        c.rect((130, oy, 950, oy + 80), fill=(246, 248, 249), r=40, outline=(206, 214, 220), width=3)
        c.ellipse((160, oy + 22, 196, oy + 58), fill=(255, 255, 255), outline=(150, 160, 170), width=3)
        c.text((222, oy + 40), o, "sb", 36, (48, 52, 60), anchor="lm")
        oy += 94
    c.button("Mehr erfahren", W / 2, 972, size=42, fill=RED)
    c.save("psy-burnout-de-0929_b.png")


def corner(c, x, y, sx, sy, col):
    """Орнамент угла: дуги + ромб + точки. sx, sy = ±1 — направление внутрь."""
    for r_ in (46, 62):
        bx = (x - r_, y - r_, x + r_, y + r_)
        start = {(1, 1): 0, (-1, 1): 90, (-1, -1): 180, (1, -1): 270}[(sx, sy)]
        c.arc(bx, start, start + 90, col, 3)
    d = 22
    cx, cy = x + sx * 4, y + sy * 4
    c.poly([(cx, cy - d), (cx + d, cy), (cx, cy + d), (cx - d, cy)], col)
    c.poly([(cx, cy - d + 8), (cx + d - 8, cy), (cx, cy + d - 8), (cx - d + 8, cy)], (250, 245, 234))
    for k in (1, 2, 3):
        c.ellipse((x + sx * (70 + k * 22) - 5, y - 5, x + sx * (70 + k * 22) + 5, y + 5), fill=col)
        c.ellipse((x - 5, y + sy * (70 + k * 22) - 5, x + 5, y + sy * (70 + k * 22) + 5), fill=col)


def c_():
    """Карточка-объявление в сертификатной рамке: кто платит за клинику / Kur."""
    GOLD = (176, 134, 62)
    GREEN = (28, 70, 58)
    c = C((250, 245, 234))
    c.rect((34, 34, W - 34, W - 34), outline=GOLD, width=5)
    c.rect((52, 52, W - 52, W - 52), outline=GOLD, width=2)
    for x, y, sx, sy in ((52, 52, 1, 1), (W - 52, 52, -1, 1), (52, W - 52, 1, -1), (W - 52, W - 52, -1, -1)):
        corner(c, x, y, sx, sy, GOLD)
    c.text((W / 2, 150), "P S Y C H O S O M A T I K  ·  R E H A  ·  K U R", "sb", 24, GOLD, anchor="mm")
    y = c.block("Psychosomatische Klinik\noder Kur:", "lserb", 62, 190, 900, GREEN, max_lines=2)
    y = c.block("Wann zahlt die\nKrankenkasse 2026?", "lserb", 62, y + 16, 900, (30, 30, 34), max_lines=2, highlight=(255, 222, 110), hl_pad=10)
    c.line([(300, y + 26), (780, y + 26)], GOLD, 2)
    c.poly([(540, y + 14), (552, y + 26), (540, y + 38), (528, y + 26)], GOLD)
    ly = y + 70
    items = ["12 Fragen: Burnout oder Depression?", "Klinik, Tagesklinik oder Kur – der Unterschied", "Wer zahlt – und wie man sie beantragt"]
    for it in items:
        c.ellipse((150, ly - 2, 196, ly + 44), fill=GREEN)
        c.check(161, ly + 11, 24, (255, 255, 255), 5)
        c.block(it, "s", 36, ly, 760, (40, 40, 44), align="left", x=222, max_lines=1)
        ly += 74
    c.button("Mehr erfahren", W / 2, 938, size=42, fill=RED)
    c.save("psy-burnout-de-0929_c.png")


def briefcase(c, cx, cy, col):
    c.rect((cx - 70, cy - 36, cx + 70, cy + 60), fill=col, r=14)
    c.rect((cx - 30, cy - 62, cx + 30, cy - 30), outline=col, width=9, r=10)
    c.rect((cx - 70, cy - 4, cx + 70, cy + 4), fill=(255, 237, 220))
    c.rect((cx - 14, cy - 12, cx + 14, cy + 14), fill=(255, 237, 220), r=4)


def cloudsun(c, cx, cy, col):
    c.ellipse((cx + 0, cy - 78, cx + 96, cy + 18), fill=(250, 200, 90))
    for bx in ((cx - 90, cy - 20, cx - 10, cy + 60), (cx - 50, cy - 56, cx + 50, cy + 44), (cx + 10, cy - 30, cx + 90, cy + 50)):
        c.ellipse(bx, fill=col)
    c.rect((cx - 50, cy + 10, cx + 50, cy + 60), fill=col)


def d():
    """Сравнение двух вариантов: Burnout против Depression."""
    OR, BL = (232, 106, 40), (46, 86, 158)
    c = C((244, 246, 248))
    y = c.block("Burnout oder Depression?", "db", 62, 48, 980, INK, max_lines=1)
    c.block("Wo der Unterschied liegt – 12 Fragen, die Ärzte stellen", "s", 34, y + 6, 960, (84, 90, 100), max_lines=1)
    L, R = (60, 232, 522, 808), (558, 232, 1020, 808)
    for box, fill, head, col, label in ((L, (255, 238, 222), (232, 106, 40), OR, "BURNOUT"), (R, (226, 236, 250), BL, BL, "DEPRESSION")):
        c.card(box, fill=fill, r=30, sh_alpha=50, blur=12, off=(0, 6))
        c.rect((box[0], box[1], box[2], box[1] + 96), fill=head, r=30)
        c.rect((box[0], box[1] + 60, box[2], box[1] + 96), fill=head)
        c.text(((box[0] + box[2]) / 2, box[1] + 50), label, "db", 42, (255, 255, 255), anchor="mm")
    briefcase(c, (L[0] + L[2]) / 2, 420, OR)
    cloudsun(c, (R[0] + R[2]) / 2, 425, BL)
    rows = [("BETROFFEN", "vor allem der Job", "alle Lebensbereiche"), ("URLAUB", "bringt oft Erholung", "hilft oft nicht")]
    ry = 566
    for lab, lt, rt in rows:
        for box, t, col in ((L, lt, OR), (R, rt, BL)):
            c.text((box[0] + 40, ry), lab, "sb", 24, col)
            c.block(t, "sb", 38, ry + 34, box[2] - box[0] - 80, (36, 38, 44), align="left", x=box[0] + 40, max_lines=1)
        ry += 124
    c.ellipse((W / 2 - 46, 374, W / 2 + 46, 466), fill=(255, 255, 255), outline=(200, 205, 212), width=3)
    c.text((W / 2, 420), "oder", "sb", 30, (90, 96, 106), anchor="mm")
    c.block("Und wann zahlt die Krankenkasse die Klinik?", "sb", 36, 836, 960, INK, max_lines=1)
    c.button("Mehr erfahren", W / 2, 972, size=42, fill=RED)
    c.save("psy-burnout-de-0929_d.png")


if __name__ == "__main__":
    for f in sys.argv[1:]:
        globals()[f if f != 'c' else 'c_']()
