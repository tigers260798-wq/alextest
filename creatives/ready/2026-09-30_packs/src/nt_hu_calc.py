"""HU · кредиты · угол «калькулятор: сколько вернёшь за год» — 4 статики 1:1 (Pillow).

Без «Nyugdíjas vagy?», без логотипов банков, без ставок/сумм/платежей (только «? Ft», «? %»),
без «gyors / azonnal / jóváhagyva» рядом с «hitel / kölcsön».
"""
import math
import random
import sys
sys.path.insert(0, "/home/user/alextest/creatives/ready/2026-09-30_packs/src")
from nt_lib import C, W, leaf, flower, rotpoly

DOC = "NT-hu-loans-calculator-2026-09-30"
NAVY = (22, 40, 78)
GREEN = (22, 120, 86)
ORANGE = (240, 128, 40)
RED = (214, 52, 52)
GRAY = (96, 104, 118)
CTA = "Tudjon meg többet"


def calculator(c, x, y, w, h, body=(46, 58, 84), screen=(206, 232, 204), shown="? Ft"):
    c.card((x, y, x + w, y + h), fill=body, r=34, sh_alpha=90, blur=16, off=(0, 10))
    sx0, sy0, sx1, sy1 = x + 30, y + 30, x + w - 30, y + 30 + h * 0.24
    c.rect((sx0, sy0, sx1, sy1), fill=screen, r=14)
    c.text((sx1 - 24, (sy0 + sy1) / 2 + 2), shown, "db", int(h * 0.12), (30, 50, 40), anchor="rm")
    kx0, ky0 = x + 30, sy1 + 26
    cols, rows = 4, 4
    gap = 14
    kw = (w - 60 - gap * (cols - 1)) / cols
    kh = (y + h - 30 - ky0 - gap * (rows - 1)) / rows
    labels = ["7", "8", "9", "÷", "4", "5", "6", "×", "1", "2", "3", "−", "0", ",", "=", "+"]
    for i, lab in enumerate(labels):
        cx0 = kx0 + (i % cols) * (kw + gap)
        cy0 = ky0 + (i // cols) * (kh + gap)
        fill = ORANGE if lab == "=" else ((86, 100, 132) if lab in "÷×−+" else (236, 238, 244))
        tc = (255, 255, 255) if lab in "=÷×−+" else (40, 44, 56)
        c.rect((cx0, cy0, cx0 + kw, cy0 + kh), fill=fill, r=12)
        c.text((cx0 + kw / 2, cy0 + kh / 2), lab, "db", int(kh * 0.42), tc, anchor="mm")


def cal_icon(c, cx, cy, s=1.0, top=RED):
    w, h = 92 * s, 84 * s
    c.rect((cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2), fill=(255, 255, 255), r=12 * s, outline=(200, 206, 218), width=3 * s)
    c.rect((cx - w / 2, cy - h / 2, cx + w / 2, cy - h / 2 + 24 * s), fill=top, r=12 * s)
    c.rect((cx - w / 2, cy - h / 2 + 12 * s, cx + w / 2, cy - h / 2 + 24 * s), fill=top)
    for k in (-1, 1):
        c.rect((cx + k * 22 * s - 5 * s, cy - h / 2 - 10 * s, cx + k * 22 * s + 5 * s, cy - h / 2 + 10 * s), fill=(90, 96, 110), r=4 * s)
    for r_ in range(3):
        for q in range(4):
            gx = cx - w / 2 + 16 * s + q * 20 * s
            gy = cy - h / 2 + 36 * s + r_ * 15 * s
            c.rect((gx, gy, gx + 12 * s, gy + 9 * s), fill=(214, 220, 232), r=2 * s)


def coins(c, x, y, n=4, r=40):
    for k in range(n):
        yy = y - k * 16
        c.ellipse((x - r, yy - r * 0.42, x + r, yy + r * 0.42), fill=(232, 176, 48), outline=(196, 138, 30), width=3)
    c.ellipse((x - r * 0.62, y - (n - 1) * 16 - r * 0.26, x + r * 0.62, y - (n - 1) * 16 + r * 0.26), outline=(250, 214, 110), width=3)


def a():
    """Сетка выбора: калькулятор + 4 срока (12/24/36/48 hónap)."""
    c = C((236, 246, 240))
    c.vgrad((0, 0, W, W), (238, 247, 241), (220, 238, 228))
    c.block("Személyi kölcsön\nkalkulátor 2026", "db", 62, 60, 600, NAVY, align="left", x=56, max_lines=2)
    y = c.block("Mennyit fizet vissza egy év alatt?", "sb", 38, 230, 560, GREEN, align="left", x=56, max_lines=2)
    c.block("Havi részlet · THM · teljes összeg", "s", 30, y + 14, 560, GRAY, align="left", x=56, max_lines=1)
    calculator(c, 690, 50, 330, 420)
    coins(c, 640, 440, n=4, r=44)
    c.text((56, 478), "Válasszon futamidőt:", "sb", 38, (40, 44, 56), anchor="lm")
    terms = ["12", "24", "36", "48"]
    boxes = [(40, 530, 530, 760), (550, 530, 1040, 760), (40, 784, 530, 1014), (550, 784, 1040, 1014)]
    for t, bx in zip(terms, boxes):
        c.card(bx, fill=(255, 255, 255), r=26, sh_alpha=50, blur=10, off=(0, 5), outline=(200, 224, 210), width=2)
        cal_icon(c, bx[0] + 86, bx[1] + 82, 1.0, top=GREEN)
        c.text((bx[0] + 160, bx[1] + 70), t + " hónap", "db", 52, NAVY, anchor="lm")
        c.text((bx[0] + 162, bx[1] + 120), "futamidő", "s", 28, GRAY, anchor="lm")
        c.button(CTA, (bx[0] + bx[2]) / 2, bx[3] - 50, size=30, fill=ORANGE, padx=34, pady=13, shadow=False)
    c.save(f"{DOC}/a.png")


def b():
    """Карточка-опросник / фейковый интерфейс: калькулятор в телефоне, все суммы — «?»."""
    c = C((250, 242, 228))
    c.vgrad((0, 0, W, W), (252, 245, 232), (244, 228, 206))
    c.ellipse((-220, 700, 300, 1220), fill=(255, 255, 255), alpha=70)
    y = c.block("Hitel nyugdíjból:", "db", 52, 220, 480, RED, align="left", x=56, max_lines=1)
    y = c.block("így számolható ki előre, mennyit fizet vissza egy év alatt", "db", 50, y + 4, 480, NAVY, align="left", x=56, max_lines=5)
    y = c.block("Havi részlet, THM és a teljes összeg – 2026", "s", 32, y + 22, 470, GRAY, align="left", x=56, max_lines=2)
    c.button(CTA, 56 + 200, y + 90, size=34, fill=RED, padx=36)
    # телефон
    ph = (560, 50, 1024, 1030)
    c.card(ph, fill=(26, 28, 36), r=70, sh_alpha=110, blur=24, off=(0, 14))
    sc = (576, 66, 1008, 1014)
    c.rect(sc, fill=(255, 255, 255), r=56)
    c.rect((744, 82, 840, 112), fill=(26, 28, 36), r=15)
    c.text((614, 98), "9:41", "sb", 22, (30, 30, 34), anchor="lm")
    x0, x1 = 606, 978
    c.text((x0, 162), "Hitelkalkulátor 2026", "db", 32, NAVY, anchor="lm")
    c.rect((x0, 190, x1, 196), fill=(236, 238, 244), r=3)
    fields = [("Hitelösszeg", "? Ft", False), ("Futamidő", "12 hónap", True), ("Havi törlesztőrészlet", "? Ft", False), ("THM", "? %", False)]
    fy = 222
    for lab, val, dd in fields:
        c.text((x0, fy + 16), lab, "sb", 24, GRAY, anchor="lm")
        c.rect((x0, fy + 38, x1, fy + 108), fill=(246, 247, 251), r=16, outline=(206, 210, 222), width=2)
        c.text((x0 + 24, fy + 73), val, "db", 32, NAVY if val != "? %" else NAVY, anchor="lm")
        if dd:
            c.poly([(x1 - 44, fy + 64), (x1 - 20, fy + 64), (x1 - 32, fy + 80)], GRAY)
        fy += 134
    # итог за год
    rb = (x0, fy + 10, x1, fy + 200)
    c.rect(rb, fill=(255, 240, 214), r=22, outline=(240, 170, 90), width=3)
    c.text((x0 + 26, rb[1] + 44), "Egy év alatt összesen", "sb", 28, (120, 64, 10), anchor="lm")
    c.text((x0 + 26, rb[1] + 82), "visszafizetve:", "sb", 28, (120, 64, 10), anchor="lm")
    c.text((x0 + 26, rb[1] + 146), "12 részlet", "s", 26, (150, 96, 40), anchor="lm")
    c.text((x1 - 30, rb[1] + 142), "? Ft", "db", 64, RED, anchor="rm")
    c.save(f"{DOC}/b.png")


def garland(c, y, flip=False, seed=1):
    """Акварельная цветочная гирлянда (как в доказанном HU 0817-GE01)."""
    random.seed(seed)
    s = -1 if flip else 1
    greens = [(128, 176, 120), (150, 190, 130), (104, 150, 104), (170, 200, 150)]
    pinks = [(246, 196, 186), (240, 178, 170), (250, 214, 204)]
    for side in (0, 1):
        x_start = 30 if side == 0 else W - 30
        dirx = 1 if side == 0 else -1
        for i in range(16):
            t = i / 15
            x = x_start + dirx * t * 430
            yy = y + s * (math.sin(t * math.pi) * 26 - 10)
            ang = (-30 if side == 0 else 210) + random.uniform(-40, 40) + (0 if not flip else 60 * dirx)
            leaf(c, x + random.uniform(-10, 10), yy + random.uniform(-18, 18), random.uniform(40, 70), random.uniform(14, 22), ang + random.choice((0, 180)), random.choice(greens), alpha=200)
        for x_off in (70, 250, 400):
            x = x_start + dirx * x_off
            yy = y + s * (math.sin(x_off / 430 * math.pi) * 26 - 10)
            flower(c, x, yy, random.uniform(38, 48), random.choice(pinks), (236, 150, 140), n=6, rot=random.uniform(0, 60), alpha=210)
            flower(c, x, yy, random.uniform(20, 24), (252, 226, 218), (230, 140, 130), n=5, rot=random.uniform(0, 60), alpha=230)
        for x_off in (150, 330):
            x = x_start + dirx * x_off
            yy = y + s * (math.sin(x_off / 430 * math.pi) * 26 - 10) + random.uniform(-20, 20)
            flower(c, x, yy, 18, (255, 255, 255), (246, 206, 90), n=5, alpha=235)
    # центральный букет
    flower(c, W / 2, y + s * 14, 46, (244, 190, 180), (230, 140, 130), n=6, alpha=215)
    flower(c, W / 2, y + s * 14, 24, (252, 228, 220), (226, 136, 126), n=5, alpha=235)
    for dx in (-80, 80):
        flower(c, W / 2 + dx, y + s * 8, 18, (255, 255, 255), (246, 206, 90), n=5, alpha=235)


def c_():
    """Сколько стоит — макет доказанного HU 0817-GE01: белая карточка, цветы сверху и снизу, «(Tudjon meg többet)»."""
    c = C((242, 242, 242))
    c.rect((0, 0, W, 190), fill=(242, 242, 242))
    garland(c, 96, seed=3)
    c.rect((0, 190, W, 890), fill=(255, 255, 255))
    c.rect((0, 890, W, W), fill=(242, 242, 242))
    garland(c, 980, flip=True, seed=5)
    y = c.block("Hitel nyugdíjból 2026-ban:\nhogyan számolható ki előre,\nmennyit kell visszafizetni\negy év alatt?",
                "d", 60, 300, 900, (20, 20, 20), max_lines=5, gap=1.14)
    c.block("(Tudjon meg többet)", "d", 52, y + 56, 900, (20, 20, 20), max_lines=1)
    c.save(f"{DOC}/c.png")


def d():
    """Сцена-иллюстрация: лупа над мелким шрифтом договора — «что не говорят банки»."""
    c = C((20, 32, 64))
    c.vgrad((0, 0, W, W), (24, 38, 76), (14, 22, 48))
    y = c.block("Amit a bankok nem mondanak el", "db", 58, 40, 1000, (255, 255, 255), max_lines=1)
    y = c.block("a nyugdíjasoknak", "db", 58, y, 1000, (255, 208, 96), max_lines=1)
    # договор
    doc = (130, y + 40, 760, 900)
    c.poly(rotpoly([(doc[0], doc[1]), (doc[2], doc[1]), (doc[2], doc[3]), (doc[0], doc[3])], 445, 700, -5), (0, 0, 0), alpha=90)
    c.rect(doc, fill=(250, 250, 246), r=10)
    c.text(((doc[0] + doc[2]) / 2, doc[1] + 56), "HITELSZERZŐDÉS", "db", 40, NAVY, anchor="mm")
    c.rect((doc[0] + 60, doc[1] + 92, doc[2] - 60, doc[1] + 96), fill=(210, 214, 224))
    random.seed(11)
    yy = doc[1] + 126
    while yy < doc[3] - 20:
        c.rect((doc[0] + 60, yy, doc[0] + 60 + random.uniform(380, 510), yy + 8), fill=(200, 204, 214), r=4)
        yy += 24
    # лупа
    mx, my, mr = 640, y + 380, 200
    c.ellipse((mx - mr - 26, my - mr - 26, mx + mr + 26, my + mr + 26), fill=(60, 64, 76))
    c.poly(rotpoly([(mx + mr + 6, my - 26), (mx + mr + 250, my - 26), (mx + mr + 250, my + 26), (mx + mr + 6, my + 26)], mx, my, 42), (60, 64, 76))
    c.poly(rotpoly([(mx + mr + 90, my - 34), (mx + mr + 260, my - 34), (mx + mr + 260, my + 34), (mx + mr + 90, my + 34)], mx, my, 42), (150, 84, 50))
    c.ellipse((mx - mr, my - mr, mx + mr, my + mr), fill=(255, 252, 236))
    c.text((mx, my - 92), "Teljes", "sb", 40, (60, 64, 80), anchor="mm")
    c.text((mx, my - 42), "visszafizetendő", "sb", 40, (60, 64, 80), anchor="mm")
    c.text((mx, my + 6), "összeg:", "sb", 40, (60, 64, 80), anchor="mm")
    c.text((mx, my + 92), "? Ft", "db", 86, RED, anchor="mm")
    c.arc((mx - mr + 24, my - mr + 24, mx + mr - 24, my + mr - 24), 200, 250, (255, 255, 255), 10, alpha=160)
    # подпись и кнопка
    c.rect((0, 876, W, W), fill=(14, 22, 48))
    c.block("Aláírás előtt: mennyit fizet vissza egy év alatt? – 2026", "sb", 36, 898, 1000, (230, 234, 246), max_lines=1)
    c.button(CTA, W / 2, 1000, size=40, fill=ORANGE, padx=48)
    c.save(f"{DOC}/d.png")


if __name__ == "__main__":
    for f in sys.argv[1:] or ["a", "b", "c", "d"]:
        globals()[f if f != "c" else "c_"]()
