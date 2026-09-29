"""ES · обучение профессии для взрослых (плотник, медсестра) — 4 статики 1:1 (Pillow).

Без обещаний работы, зарплаты и диплома.
"""
import math
import random
import sys
sys.path.insert(0, "/home/user/alextest/creatives/ready/2026-09-30_packs/src")
from nt_lib import C, W, leaf, rotpoly

DOC = "NT-adult-trade-training-es-2026-09-30"
NAVY = (26, 44, 84)
TERRA = (192, 88, 50)
WOOD = (196, 146, 96)
BLUE = (40, 104, 176)
BTN = (226, 78, 40)
GRAY = (96, 100, 110)
INK = (34, 34, 40)
CTA = "Más información"


# ---------- иконки
def ic_saw(c, cx, cy, s=1.0):
    k = s
    blade = [(cx - 90 * k, cy - 20 * k), (cx + 60 * k, cy - 34 * k), (cx + 60 * k, cy + 10 * k), (cx - 90 * k, cy + 26 * k)]
    c.poly(blade, (214, 220, 230))
    teeth = []
    for i in range(12):
        x = cx - 88 * k + i * 12.4 * k
        yb = cy + 26 * k - (i * 12.4 * k) * (16 / 150)
        teeth += [(x, yb), (x + 6 * k, yb + 10 * k)]
    teeth += [(cx + 60 * k, cy + 10 * k)]
    c.line(teeth, (150, 158, 172), 3 * k)
    c.rect((cx + 50 * k, cy - 50 * k, cx + 110 * k, cy + 28 * k), fill=TERRA, r=18 * k)
    c.rect((cx + 68 * k, cy - 30 * k, cx + 94 * k, cy + 8 * k), fill=(250, 236, 220), r=10 * k)


def ic_stetho(c, cx, cy, s=1.0, col=NAVY):
    k = s
    c.arc((cx - 60 * k, cy - 80 * k, cx + 20 * k, cy + 20 * k), 0, 180, col, 9 * k)
    c.line([(cx - 60 * k, cy - 30 * k), (cx - 60 * k, cy - 70 * k)], col, 9 * k)
    c.line([(cx + 20 * k, cy - 30 * k), (cx + 20 * k, cy - 70 * k)], col, 9 * k)
    c.arc((cx - 20 * k, cy - 10 * k, cx + 70 * k, cy + 70 * k), 90, 180, col, 9 * k)
    c.line([(cx + 25 * k, cy + 70 * k), (cx + 60 * k, cy + 70 * k)], col, 9 * k)
    c.arc((cx + 30 * k, cy + 10 * k, cx + 90 * k, cy + 70 * k), 270, 450, col, 9 * k)
    c.ellipse((cx + 44 * k, cy - 14 * k, cx + 92 * k, cy + 34 * k), fill=(190, 200, 214), outline=col, width=8 * k)


def ic_talk(c, cx, cy, s=1.0):
    k = s
    c.rect((cx - 90 * k, cy - 60 * k, cx + 20 * k, cy + 10 * k), fill=(255, 255, 255), r=24 * k)
    c.poly([(cx - 60 * k, cy + 6 * k), (cx - 40 * k, cy + 6 * k), (cx - 70 * k, cy + 34 * k)], (255, 255, 255))
    c.rect((cx - 20 * k, cy - 20 * k, cx + 90 * k, cy + 50 * k), fill=(255, 214, 110), r=24 * k)
    c.poly([(cx + 50 * k, cy + 46 * k), (cx + 70 * k, cy + 46 * k), (cx + 80 * k, cy + 74 * k)], (255, 214, 110))
    for i in range(3):
        c.ellipse((cx + 8 * k + i * 26 * k, cy + 6 * k, cx + 22 * k + i * 26 * k, cy + 20 * k), fill=(160, 110, 30))


def ic_hourglass(c, cx, cy, s=1.0):
    k = s
    c.rect((cx - 56 * k, cy - 78 * k, cx + 56 * k, cy - 64 * k), fill=(120, 80, 50), r=6 * k)
    c.rect((cx - 56 * k, cy + 64 * k, cx + 56 * k, cy + 78 * k), fill=(120, 80, 50), r=6 * k)
    c.poly([(cx - 44 * k, cy - 64 * k), (cx + 44 * k, cy - 64 * k), (cx + 6 * k, cy), (cx + 44 * k, cy + 64 * k), (cx - 44 * k, cy + 64 * k), (cx - 6 * k, cy)], (230, 240, 250))
    c.poly([(cx - 26 * k, cy - 40 * k), (cx + 26 * k, cy - 40 * k), (cx, cy - 6 * k)], (240, 190, 90))
    c.poly([(cx - 36 * k, cy + 64 * k), (cx + 36 * k, cy + 64 * k), (cx, cy + 34 * k)], (240, 190, 90))
    c.line([(cx, cy - 4 * k), (cx, cy + 40 * k)], (240, 190, 90), 3 * k)


def a():
    """Сетка выбора 2×2: плотник / медсестра / психология / короткие программы."""
    c = C((250, 246, 240))
    y = c.block("¿Qué estudiar siendo\nadulto en 2026?", "db", 58, 36, 1000, NAVY, max_lines=2)
    y = c.block("Elige un área:", "sb", 36, y + 4, 1000, GRAY, max_lines=1)
    tiles = [("Carpintería", ic_saw, (246, 222, 196)), ("Enfermería", ic_stetho, (216, 234, 246)),
             ("Psicología", ic_talk, (222, 214, 244)), ("Carreras cortas", ic_hourglass, (220, 238, 222))]
    top = y + 24
    th = (1040 - top - 20) / 2
    for i, (lab, ic, bg) in enumerate(tiles):
        x0 = 40 + (i % 2) * 510
        y0 = top + (i // 2) * (th + 20)
        box = (x0, y0, x0 + 490, y0 + th)
        c.card(box, fill=(255, 255, 255), r=26, sh_alpha=50, blur=10, off=(0, 5))
        c.rect((box[0], box[1], box[2], box[1] + th * 0.5), fill=bg, r=26)
        c.rect((box[0], box[1] + 40, box[2], box[1] + th * 0.5), fill=bg)
        ic(c, x0 + 245 - (20 if ic is ic_saw else 0), y0 + th * 0.25, 0.95)
        c.text((x0 + 245, y0 + th * 0.5 + 52), lab, "db", 40, NAVY, anchor="mm")
        c.button(CTA, x0 + 245, y0 + th - 54, size=28, fill=BTN, padx=30, pady=13, shadow=False)
    c.save(f"{DOC}/a.png")


def b():
    """Карточка-опросник на планшете-клипборде: когда есть время учиться."""
    c = C((216, 232, 244))
    c.vgrad((0, 0, W, W), (226, 238, 248), (200, 220, 238))
    y = c.block("Estudiar un oficio de adulto", "db", 56, 36, 1000, NAVY, max_lines=1)
    y = c.block("Test: ¿qué modalidad encaja mejor?", "sb", 38, y + 2, 1000, TERRA, max_lines=1)
    # клипборд
    board = (110, y + 40, 970, 900)
    c.card(board, fill=(170, 118, 72), r=30, sh_alpha=80, blur=16, off=(0, 10))
    paper = (140, board[1] + 58, 940, 872)
    c.rect(paper, fill=(255, 255, 255), r=10)
    c.rect((430, board[1] - 22, 650, board[1] + 42), fill=(170, 176, 188), r=18)
    c.ellipse((522, board[1] - 12, 558, board[1] + 22), fill=(170, 118, 72))
    x0, x1 = paper[0] + 44, paper[2] - 44
    c.text((x0, paper[1] + 50), "Pregunta 1 de 4", "sb", 28, GRAY, anchor="lm")
    for k in range(4):
        c.rect((x1 - 200 + k * 52, paper[1] + 44, x1 - 160 + k * 52, paper[1] + 56), fill=TERRA if k == 0 else (224, 226, 232), r=6)
    qy = c.block("¿Cuándo hay tiempo para estudiar?", "db", 46, paper[1] + 96, x1 - x0, INK, align="left", x=x0, max_lines=2)
    opts = ["Por la mañana", "Por la tarde", "Los fines de semana", "Solo online, a distancia"]
    oy = qy + 20
    for i, o in enumerate(opts):
        c.rect((x0, oy + 8, x0 + 52, oy + 60), fill=(255, 255, 255), r=8, outline=NAVY, width=4)
        c.text((x0 + 78, oy + 34), o, "sb", 38, INK, anchor="lm")
        if i < 3:
            c.line([(x0 + 78, oy + 76), (x1, oy + 76)], (230, 232, 238), 2)
        oy += 90
    c.button(CTA, W / 2, 976, size=44, fill=BTN, padx=58)
    c.save(f"{DOC}/b.png")


def workbench_icon(c, cx, cy, col=(255, 255, 255)):
    c.rect((cx - 90, cy - 10, cx + 90, cy + 10), fill=col, r=4)
    c.rect((cx - 80, cy + 10, cx - 66, cy + 70), fill=col)
    c.rect((cx + 66, cy + 10, cx + 80, cy + 70), fill=col)
    c.rect((cx - 60, cy - 36, cx + 10, cy - 10), fill=col, r=4)
    c.poly([(cx + 30, cy - 10), (cx + 50, cy - 60), (cx + 58, cy - 56), (cx + 42, cy - 10)], col)


def laptop_icon(c, cx, cy, col=(255, 255, 255), screen=BLUE):
    c.rect((cx - 80, cy - 60, cx + 80, cy + 40), fill=col, r=10)
    c.rect((cx - 68, cy - 48, cx + 68, cy + 28), fill=screen, r=4)
    c.poly([(cx - 104, cy + 44), (cx + 104, cy + 44), (cx + 90, cy + 62), (cx - 90, cy + 62)], col)
    c.ellipse((cx - 16, cy - 34, cx + 16, cy - 2), fill=col)
    c.rect((cx - 30, cy + 2, cx + 30, cy + 26), fill=col, r=12)


def c_():
    """Сравнение «VS»: очно или дистанционно."""
    c = C((255, 255, 255))
    c.rect((0, 0, W / 2, W), fill=TERRA)
    c.rect((W / 2, 0, W, W), fill=BLUE)
    c.rect((0, 0, W, 214), fill=(250, 246, 240))
    y = c.block("Estudiar de adulto en 2026:", "db", 48, 34, 1000, NAVY, max_lines=1)
    c.block("¿presencial o a distancia?", "db", 64, y + 2, 1000, INK, max_lines=1)
    workbench_icon(c, 270, 300)
    laptop_icon(c, 810, 300, screen=(30, 70, 130))
    c.text((270, 420), "PRESENCIAL", "db", 44, (255, 255, 255), anchor="mm")
    c.text((810, 420), "A DISTANCIA", "db", 44, (255, 255, 255), anchor="mm")
    rows = [("Horario", "fijo", "flexible"), ("Dónde", "en el aula o el taller", "desde casa"), ("Ritmo", "el del grupo", "el propio")]
    ry = 480
    for lab, l, r in rows:
        c.text((270, ry), lab.upper(), "sb", 26, (255, 226, 206), anchor="mm")
        c.text((810, ry), lab.upper(), "sb", 26, (206, 226, 255), anchor="mm")
        c.block(l, "sb", 38, ry + 22, 440, (255, 255, 255), cx=270, max_lines=1)
        c.block(r, "sb", 38, ry + 22, 440, (255, 255, 255), cx=810, max_lines=1)
        ry += 118
    c.ellipse((W / 2 - 64, 560, W / 2 + 64, 688), fill=(255, 255, 255))
    c.text((W / 2, 624), "VS", "db", 50, INK, anchor="mm")
    c.rect((0, 840, W, W), fill=(250, 246, 240))
    c.block("Carpintería, enfermería y más: requisitos y duración de cada opción", "sb", 32, 858, 1000, NAVY, max_lines=1)
    c.button(CTA, W / 2, 990, size=42, fill=BTN, padx=56)
    c.save(f"{DOC}/c.png")


def d():
    """Сцена-иллюстрация: столярная мастерская — верстак, доска, рубанок, стружка, инструменты на стене."""
    random.seed(3)
    c = C((236, 222, 200))
    c.vgrad((0, 0, W, 800), (240, 228, 208), (226, 208, 182))
    D = 70
    # окно со светом
    c.rect((730, 250 + D, 1000, 560 + D), fill=(150, 110, 70), r=6)
    c.vgrad((746, 266 + D, 984, 544 + D), (200, 228, 246), (236, 244, 250))
    c.line([(865, 266 + D), (865, 544 + D)], (150, 110, 70), 8)
    c.line([(746, 405 + D), (984, 405 + D)], (150, 110, 70), 8)
    c.glow((620, 400 + D, 1080, 900), (255, 246, 220), alpha=90, blur=60)
    # перфорированная панель с инструментами
    pb = (80, 250 + D, 660, 560 + D)
    c.rect(pb, fill=(214, 184, 140), r=10)
    for q in range(12):
        for r_ in range(7):
            x, y_ = pb[0] + 26 + q * 48, pb[1] + 24 + r_ * 44
            c.ellipse((x - 3, y_ - 3, x + 3, y_ + 3), fill=(176, 146, 104))
    ic_saw(c, 230, 340 + D, 0.9)
    c.rect((390, 300 + D, 406, 470 + D), fill=(150, 100, 60))
    c.rect((360, 290 + D, 436, 322 + D), fill=(90, 96, 110), r=6)
    c.poly([(470, 300 + D), (500, 300 + D), (500, 480 + D), (600, 480 + D), (600, 510 + D), (470, 510 + D)], (80, 110, 150))
    for k in range(6):
        c.line([(476, 320 + D + k * 28), (490, 320 + D + k * 28)], (240, 240, 240), 3)
    for x in (140, 180):
        c.rect((x, 430 + D, x + 16, 480 + D), fill=(150, 100, 60), r=4)
        c.rect((x + 3, 480 + D, x + 13, 540 + D), fill=(180, 186, 196))
    # верстак
    top = 690 + D
    c.rect((0, top, W, top + 50), fill=(150, 98, 58))
    c.rect((0, top + 50, W, W), fill=(120, 80, 50))
    c.rect((0, top + 46, W, top + 56), fill=(104, 68, 40))
    for x in (60, 1000):
        c.rect((x, top + 50, x + 30, W), fill=(96, 62, 38))
    # доска
    c.rect((120, top - 90, 820, top), fill=(222, 178, 120), r=4)
    for k in range(5):
        yy = top - 78 + k * 16
        c.line([(130, yy), (500 + k * 40, yy + 3), (810, yy)], (206, 160, 104), 3)
    # рубанок
    c.poly([(560, top - 90), (760, top - 90), (740, top - 150), (590, top - 150)], (200, 110, 60))
    c.rect((550, top - 100, 770, top - 84), fill=(90, 96, 110), r=4)
    c.ellipse((600, top - 184, 660, top - 134), fill=(200, 110, 60))
    # стружка
    for x, y_ in ((470, top - 104), (510, top - 110), (440, top - 98)):
        c.arc((x - 20, y_ - 16, x + 20, y_ + 16), 150, 390, (240, 208, 160), 7)
    # заголовок
    c.rect((0, 0, W, 250), fill=(30, 44, 80))
    y = c.block("Cómo estudiar carpintería\nsiendo adulto", "db", 56, 30, 1000, (255, 255, 255), max_lines=2)
    c.block("Cursos 2026: requisitos, duración y modalidades", "s", 34, y + 6, 1000, (255, 214, 150), max_lines=1)
    c.button(CTA, W / 2, 960, size=46, fill=BTN, padx=62)
    c.save(f"{DOC}/d.png")


if __name__ == "__main__":
    for f in sys.argv[1:] or ["a", "b", "c", "d"]:
        globals()[f if f != "c" else "c_"]()
