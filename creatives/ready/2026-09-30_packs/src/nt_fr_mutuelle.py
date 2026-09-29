"""FR · мутюэль для пенсионеров · угол «2 условия» — 4 статики 1:1 (Pillow)."""
import math
import sys
sys.path.insert(0, "/home/user/alextest/creatives/ready/2026-09-30_packs/src")
from nt_lib import C, W, leaf, rotpoly

DOC = "NT-mutuelle-retraites-fr-2026-09-30"
NAVY = (20, 46, 98)
BLUE = (40, 96, 178)
CORAL = (228, 70, 56)
GRAY = (92, 100, 116)
TEAL = (16, 132, 124)
CTA = "En savoir plus"


# ---------- иконки
def glasses(c, cx, cy, s=1.0, col=NAVY):
    r = 34 * s
    c.ellipse((cx - 2.3 * r, cy - r, cx - 0.3 * r, cy + r), fill=(214, 232, 248), outline=col, width=7 * s)
    c.ellipse((cx + 0.3 * r, cy - r, cx + 2.3 * r, cy + r), fill=(214, 232, 248), outline=col, width=7 * s)
    c.arc((cx - 0.45 * r, cy - 0.55 * r, cx + 0.45 * r, cy + 0.25 * r), 200, 340, col, 7 * s)
    c.line([(cx - 2.3 * r, cy - 0.2 * r), (cx - 3.0 * r, cy - 0.6 * r)], col, 7 * s)
    c.line([(cx + 2.3 * r, cy - 0.2 * r), (cx + 3.0 * r, cy - 0.6 * r)], col, 7 * s)


def tooth(c, cx, cy, s=1.0, col=(255, 255, 255), line=NAVY):
    k = s
    pts = [(cx - 52 * k, cy - 30 * k), (cx - 40 * k, cy - 56 * k), (cx - 14 * k, cy - 60 * k), (cx, cy - 50 * k),
           (cx + 14 * k, cy - 60 * k), (cx + 40 * k, cy - 56 * k), (cx + 52 * k, cy - 30 * k), (cx + 46 * k, cy + 4 * k),
           (cx + 36 * k, cy + 52 * k), (cx + 22 * k, cy + 62 * k), (cx + 12 * k, cy + 30 * k), (cx, cy + 18 * k),
           (cx - 12 * k, cy + 30 * k), (cx - 22 * k, cy + 62 * k), (cx - 36 * k, cy + 52 * k), (cx - 46 * k, cy + 4 * k)]
    c.line(pts + [pts[0]], line, 7 * k)
    c.poly(pts, col)
    c.arc((cx - 34 * k, cy - 46 * k, cx - 6 * k, cy - 18 * k), 190, 280, (190, 214, 240), 5 * k)


def hearing(c, cx, cy, s=1.0, col=NAVY):
    k = s
    c.arc((cx - 40 * k, cy - 56 * k, cx + 40 * k, cy + 44 * k), 150, 390, col, 18 * k)
    c.ellipse((cx - 10 * k, cy + 30 * k, cx + 12 * k, cy + 52 * k), fill=col)
    c.line([(cx + 30 * k, cy + 20 * k), (cx + 6 * k, cy + 40 * k)], col, 6 * k)
    for i, rr in enumerate((62, 86)):
        c.arc((cx - rr * k + 60 * k, cy - rr * k, cx + rr * k + 60 * k, cy + rr * k), -40, 40, (120, 160, 214), 6 * k)


def bed(c, cx, cy, s=1.0, col=NAVY):
    k = s
    c.rect((cx - 80 * k, cy - 40 * k, cx - 64 * k, cy + 50 * k), fill=col, r=4 * k)
    c.rect((cx - 64 * k, cy + 4 * k, cx + 80 * k, cy + 28 * k), fill=col, r=4 * k)
    c.rect((cx + 70 * k, cy + 4 * k, cx + 82 * k, cy + 50 * k), fill=col, r=3 * k)
    c.rect((cx - 60 * k, cy - 16 * k, cx + 76 * k, cy + 6 * k), fill=(214, 232, 248), r=8 * k)
    c.rect((cx - 58 * k, cy - 34 * k, cx - 16 * k, cy - 10 * k), fill=(255, 255, 255), r=10 * k, outline=col, width=3 * k)


def a():
    """Сетка выбора: мутюэль по возрасту 60+ / 70+ / 75+ / 80+."""
    c = C((245, 247, 251))
    y = c.block("Mutuelle senior : selon l'âge", "db", 66, 40, 1000, NAVY, max_lines=1)
    # баннер с иконками гарантий
    bx = (40, y + 24, 1040, y + 324)
    c.card(bx, fill=(226, 238, 252), r=30, sh_alpha=40, blur=10, off=(0, 5))
    labels = [("Optique", glasses), ("Dentaire", tooth), ("Audition", hearing), ("Hospitalisation", bed)]
    for i, (lab, ic) in enumerate(labels):
        cx = 40 + 125 + i * 250
        c.ellipse((cx - 92, bx[1] + 40, cx + 92, bx[1] + 224), fill=(255, 255, 255))
        ic(c, cx if ic is not hearing else cx - 16, bx[1] + 132, 1.0 if ic is not glasses else 0.9)
        c.text((cx, bx[1] + 262), lab, "sb", 30, NAVY, anchor="mm")
    ty = bx[3] + 56
    c.text((W / 2, ty), "Choisissez une tranche d'âge :", "sb", 38, (40, 44, 56), anchor="mm")
    tiles = ["60", "70", "75", "80"]
    tw, gap, x0 = 235, 20, 40
    for i, t in enumerate(tiles):
        tx = x0 + i * (tw + gap)
        box = (tx, ty + 44, tx + tw, 1034)
        c.card(box, fill=(255, 255, 255), r=24, sh_alpha=55, blur=10, off=(0, 5), outline=(206, 218, 236), width=2)
        cx = tx + tw / 2
        c.text((cx, box[1] + 96), t, "db", 100, BLUE, anchor="mm")
        c.text((cx, box[1] + 178), "ans et +", "sb", 32, NAVY, anchor="mm")
        c.line([(tx + 40, box[1] + 222), (tx + tw - 40, box[1] + 222)], (226, 230, 238), 2)
        c.rect((cx - 104, box[1] + 250, cx + 104, box[1] + 304), fill=(255, 240, 190), r=27)
        c.text((cx, box[1] + 277), "ce qui change", "db", 22, (120, 70, 0), anchor="mm")
        c.button(CTA, cx, box[3] - 62, size=24, fill=CORAL, padx=18, pady=14, arrow=False, shadow=False)
    c.save(f"{DOC}/a.png")


def b():
    """Карточка-опросник: сколько условий нужно для мутюэль на пенсии."""
    c = C((230, 244, 240))
    c.vgrad((0, 0, W, W), (232, 246, 241), (214, 230, 246))
    c.ellipse((760, -160, 1240, 320), fill=(255, 255, 255), alpha=70)
    c.ellipse((-200, 760, 260, 1220), fill=(255, 255, 255), alpha=60)
    y = c.block("Mutuelle à la retraite", "db", 64, 44, 1000, NAVY, max_lines=1)
    y = c.block("Le quiz que peu de gens réussissent", "s", 36, y + 2, 1000, GRAY, max_lines=1)
    card = (60, y + 36, 1020, 812)
    c.card(card, fill=(255, 255, 255), r=34, sh_alpha=70, blur=18, off=(0, 10))
    x0, x1 = card[0] + 50, card[2] - 50
    c.rect((x0, card[1] + 44, x0 + 250, card[1] + 92), fill=(222, 242, 238), r=24)
    c.text((x0 + 125, card[1] + 68), "QUIZ 2026", "sb", 26, TEAL, anchor="mm")
    c.text((x1, card[1] + 68), "Question 1 / 3", "s", 28, GRAY, anchor="rm")
    c.rect((x0, card[1] + 118, x1, card[1] + 130), fill=(228, 232, 240), r=6)
    c.rect((x0, card[1] + 118, x0 + (x1 - x0) / 3, card[1] + 130), fill=TEAL, r=6)
    qy = c.block("Pour demander une mutuelle à la retraite, combien de conditions faut-il remplir ?",
                 "db", 44, card[1] + 162, x1 - x0, NAVY, align="left", x=x0, max_lines=3)
    opts = [("A", "Une seule"), ("B", "Deux"), ("C", "Trois"), ("D", "Aucune")]
    ow = (x1 - x0 - 24) / 2
    oy = qy + 26
    for i, (L, o) in enumerate(opts):
        ox = x0 + (i % 2) * (ow + 24)
        yy = oy + (i // 2) * 112
        c.rect((ox, yy, ox + ow, yy + 92), fill=(246, 248, 252), r=22, outline=(200, 208, 222), width=2)
        c.ellipse((ox + 22, yy + 20, ox + 74, yy + 72), fill=(226, 236, 250))
        c.text((ox + 48, yy + 46), L, "db", 28, BLUE, anchor="mm")
        c.text((ox + 98, yy + 46), o, "sb", 34, (40, 44, 56), anchor="lm")
    c.text((W / 2, 866), "La réponse et ce qui change en 2026", "sb", 34, NAVY, anchor="mm")
    c.button(CTA, W / 2, 962, size=44, fill=CORAL, padx=60)
    c.save(f"{DOC}/b.png")


def c_():
    """Сколько стоит: столбики тарифа по возрасту с «? €»."""
    c = C((250, 245, 236))
    y = c.block("Mutuelle senior :\nce qui change à 60, 70, 75, 80 ans", "db", 58, 40, 1000, NAVY, max_lines=2)
    y = c.block("Le tarif change avec l'âge et le niveau de garanties", "s", 34, y + 6, 980, GRAY, max_lines=1)
    panel = (60, y + 30, 1020, 880)
    c.card(panel, fill=(255, 255, 255), r=30, sh_alpha=50, blur=14, off=(0, 6))
    base = panel[3] - 90
    c.text((panel[0] + 40, panel[1] + 44), "Tarif selon l'âge", "sb", 28, GRAY, anchor="lm")
    for k in range(4):
        gy = base - k * 110
        c.line([(panel[0] + 40, gy), (panel[2] - 40, gy)], (232, 234, 240), 2)
    ages = ["60 ans", "70 ans", "75 ans", "80 ans"]
    hs = [150, 230, 300, 370]
    cols = [(150, 190, 236), (98, 150, 220), (56, 112, 196), (26, 70, 150)]
    bw = 150
    span = (panel[2] - panel[0] - 80)
    for i, (lab, h, col) in enumerate(zip(ages, hs, cols)):
        cx = panel[0] + 40 + span * (i + 0.5) / 4
        c.rect((cx - bw / 2, base - h, cx + bw / 2, base), fill=col, r=14)
        c.rect((cx - bw / 2, base - 20, cx + bw / 2, base), fill=col)
        tag = (cx - 66, base - h - 74, cx + 66, base - h - 16)
        c.rect(tag, fill=(255, 238, 180), r=18)
        c.poly([(cx - 12, tag[3] - 1), (cx + 12, tag[3] - 1), (cx, tag[3] + 14)], (255, 238, 180))
        c.text((cx, (tag[1] + tag[3]) / 2), "?", "db", 34, (120, 70, 0), anchor="mm")
        c.text((cx, base + 44), lab, "sb", 32, NAVY, anchor="mm")
    c.line([(panel[0] + 40, base), (panel[2] - 40, base)], (120, 128, 146), 4)
    c.button(CTA, W / 2, 970, size=44, fill=CORAL, padx=60)
    c.save(f"{DOC}/c.png")


def d():
    """Сцена-иллюстрация: на столе бланк «Demande de mutuelle» с двумя условиями, очки, чай."""
    c = C((244, 232, 214))
    c.vgrad((0, 0, W, 620), (248, 238, 222), (238, 222, 198))
    # стол
    c.vgrad((0, 600, W, W), (196, 146, 98), (170, 120, 78))
    c.rect((0, 596, W, 612), fill=(150, 104, 66))
    y = c.block("Mutuelle à la retraite :", "db", 56, 36, 1000, NAVY, max_lines=1)
    y = c.block("2 conditions à remplir", "db", 70, y + 4, 1000, (30, 30, 36), max_lines=1, highlight=(255, 216, 102), hl_pad=12)
    y = c.block("avant de faire la demande", "db", 52, y + 10, 1000, NAVY, max_lines=1)
    c.block("Ce que peu de gens savent en 2026", "s", 32, y + 6, 1000, GRAY, max_lines=1)
    # растение справа
    c.rect((884, 470, 984, 600), fill=(214, 110, 74), r=10)
    c.rect((876, 462, 992, 490), fill=(196, 96, 62), r=8)
    for (lx, ly, L, ang) in ((934, 400, 120, -100), (906, 420, 110, -130), (960, 420, 110, -55), (894, 384, 100, -115), (970, 386, 100, -70)):
        leaf(c, lx, ly, L, 40, ang, (72, 150, 96))
    # картина на стене
    c.rect((96, 372, 336, 522), fill=(160, 112, 70), r=6)
    c.rect((110, 386, 322, 508), fill=(206, 230, 244))
    c.poly([(110, 508), (180, 430), (236, 480), (272, 450), (322, 500), (322, 508)], (120, 170, 120))
    c.ellipse((268, 400, 300, 432), fill=(255, 214, 110))
    # документ
    CX, CY, ANG = 350, 790, 0
    dx0, dy0, dx1, dy1 = 100, 530, 600, 1050

    def P(x, y_):
        return rotpoly([(x, y_)], CX, CY, ANG)[0]
    doc = rotpoly([(dx0, dy0), (dx1, dy0), (dx1, dy1), (dx0, dy1)], CX, CY, ANG)
    c.poly([(x + 8, y_ + 12) for x, y_ in doc], (120, 80, 50), alpha=90)
    c.poly(doc, (255, 255, 255))
    c.text(P(350, 584), "DEMANDE DE MUTUELLE", "db", 32, NAVY, anchor="mm")
    c.text(P(350, 626), "RETRAITE · 2026", "sb", 26, GRAY, anchor="mm")
    c.line([P(140, 660), P(560, 660)], (220, 224, 232), 3)
    for i, lab in enumerate(("Condition n° 1", "Condition n° 2")):
        yy = 694 + i * 96
        box = rotpoly([(140, yy), (192, yy), (192, yy + 52), (140, yy + 52)], CX, CY, ANG)
        c.line(box + [box[0]], NAVY, 5)
        c.text(P(214, yy + 26), lab, "sb", 36, NAVY, anchor="lm")
        c.text(P(530, yy + 26), "?", "db", 48, CORAL, anchor="mm")
    for i in range(3):
        yy = 912 + i * 36
        c.line([P(140, yy), P(520 - i * 90, yy)], (210, 214, 224), 8)
    glasses(c, 470, 1000, 0.72, (40, 40, 48))
    # чашка чая
    mx, my = 680, 600
    c.ellipse((mx - 26, my + 116, mx + 150, my + 148), fill=(150, 104, 66), alpha=120)
    c.rect((mx, my, mx + 110, my + 128), fill=(255, 255, 255), r=16)
    c.ellipse((mx + 88, my + 26, mx + 146, my + 90), outline=(255, 255, 255), width=14)
    c.ellipse((mx + 6, my - 8, mx + 104, my + 16), fill=(196, 120, 60))
    for k in range(2):
        pts = [(mx + 36 + k * 36 + math.sin(t / 4 + k) * 8, my - 18 - t * 4) for t in range(16)]
        c.line(pts, (255, 255, 255), 5, alpha=170)
    # ручка
    c.poly(rotpoly([(660, 820), (880, 820), (880, 838), (660, 838)], 770, 829, -18), (28, 60, 120))
    c.poly(rotpoly([(880, 820), (906, 829), (880, 838)], 770, 829, -18), (40, 40, 48))
    c.button(CTA, 830, 975, size=40, fill=CORAL, padx=40, pady=18)
    c.save(f"{DOC}/d.png")


if __name__ == "__main__":
    for f in sys.argv[1:] or ["a", "b", "c", "d"]:
        globals()[f if f != "c" else "c_"]()
