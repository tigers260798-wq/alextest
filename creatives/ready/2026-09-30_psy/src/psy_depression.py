import sys
sys.path.insert(0, "/tmp/claude-0/-home-user-alextest/f5dce882-fce7-5270-9036-ca9a0fe43d5e/scratchpad")
from psy_lib import C, W

NAVY = (24, 44, 84)
TEAL = (18, 140, 132)
RED = (226, 56, 48)
GRAY = (96, 104, 118)
SCALE = [(76, 175, 80), (205, 205, 60), (250, 170, 50), (240, 110, 50), (214, 48, 48)]


def pencil(c, x0, y0, x1, y1, w=26):
    import math
    ang = math.atan2(y1 - y0, x1 - x0)
    nx, ny = -math.sin(ang) * w / 2, math.cos(ang) * w / 2
    L = math.hypot(x1 - x0, y1 - y0)
    ux, uy = (x1 - x0) / L, (y1 - y0) / L

    def pt(t, side):
        return (x0 + ux * t + nx * side, y0 + uy * t + ny * side)
    c.poly([pt(0, 1), pt(40, 1), pt(40, -1), pt(0, -1)], (240, 140, 150))       # ластик
    c.poly([pt(40, 1), pt(58, 1), pt(58, -1), pt(40, -1)], (170, 170, 176))     # обойма
    c.poly([pt(58, 1), pt(L - 70, 1), pt(L - 70, -1), pt(58, -1)], (248, 196, 44))
    c.poly([pt(58, 0.33), pt(L - 70, 0.33), pt(L - 70, -0.33), pt(58, -0.33)], (236, 176, 30))
    c.poly([pt(L - 70, 1), pt(L - 70, -1), (x1, y1)], (236, 204, 160))            # дерево
    c.poly([pt(L - 22, 0.32), pt(L - 22, -0.32), (x1, y1)], (60, 60, 64))         # грифель


def scale_bar(c, x0, x1, y, h=36, labels=True, lab_col=GRAY):
    c.hgrad((x0, y, x1, y + h), SCALE)
    # скругление: маска углов цветом фона не знаем — рисуем «капсулу» поверх контуром
    for v in (0, 5, 10, 15, 20, 27):
        x = x0 + (x1 - x0) * v / 27
        if labels:
            c.text((x, y + h + 26), str(v), "sb", 28, lab_col, anchor="mm")
        if v not in (0, 27):
            c.rect((x - 1.5, y, x + 1.5, y + h), fill=(255, 255, 255), alpha=200)


def a():
    """Иллюстрация: клипборд с опросником из 9 строк + шкала 0–27."""
    c = C((234, 245, 241))
    c.vgrad((0, 0, W, W), (236, 246, 242), (218, 236, 230))
    y = c.block("9 questions doctors use\nto assess mood", "db", 60, 34, 1000, NAVY, max_lines=2)
    # клипборд
    bx = (300, y + 36, 780, 738)
    c.card(bx, fill=(186, 138, 88), r=26, sh_alpha=70, blur=14)
    px = (326, bx[1] + 44, 754, 716)
    c.rect(px, fill=(255, 255, 255), r=8)
    c.rect((460, bx[1] - 18, 620, bx[1] + 34), fill=(160, 166, 176), r=14)
    c.ellipse((526, bx[1] - 10, 554, bx[1] + 12), fill=(186, 138, 88))
    ry = px[1] + 34
    c.rect((356, ry - 12, 560, ry), fill=(200, 206, 214), r=4)
    for col_x in (602, 636, 670, 704):
        c.rect((col_x - 12, ry - 14, col_x + 12, ry - 6), fill=(214, 220, 226), r=3)
    step = (px[3] - ry - 30) / 9
    lens = [190, 150, 175, 130, 160, 185, 140, 170, 155]
    for i in range(9):
        yy = ry + 22 + i * step
        c.text((356, yy), f"{i + 1}.", "sb", 22, NAVY)
        c.rect((392, yy + 6, 392 + lens[i], yy + 14), fill=(206, 212, 220), r=4)
        c.rect((392, yy + 20, 392 + lens[i] * 0.6, yy + 26), fill=(222, 226, 232), r=3)
        for col_x in (602, 636, 670, 704):
            c.rect((col_x - 11, yy + 2, col_x + 11, yy + 24), outline=(140, 150, 166), width=2, r=3)
    c.rect((636 - 11, ry + 22 + 2 * step + 2, 636 + 11, ry + 22 + 2 * step + 24), fill=(140, 150, 166), r=3, alpha=0)
    pencil(c, 842, 400, 700, 668)
    c.block("Score 0–27: what it means", "sb", 42, 756, 980, NAVY, max_lines=1)
    c.shadow((120, 820, 960, 852), r=16, alpha=40, blur=6, off=(0, 3))
    scale_bar(c, 120, 960, 818, h=34)
    c.button("Learn more", W / 2, 984, size=42, fill=RED)
    c.save("psy-depression-multi-0929_a.png")


def b():
    """Фейковая интерактивность: вопрос 1 из 9 на экране телефона."""
    c = C((236, 234, 250))
    c.vgrad((0, 0, W, W), (238, 236, 252), (208, 218, 246))
    c.ellipse((-200, 640, 360, 1200), fill=(255, 255, 255), alpha=60)
    # левая колонка
    y = c.block("The 9-question\ntest doctors use\nto assess mood", "db", 56, 300, 470, NAVY, align="left", x=60, max_lines=3)
    y = c.block("About 3 minutes.\nScore from 0 to 27.", "s", 36, y + 24, 450, GRAY, align="left", x=60)
    c.button("Learn more", 60 + 150, y + 90, size=40, fill=RED, padx=46)
    # телефон
    ph = (560, 60, 1016, 1020)
    c.card(ph, fill=(26, 28, 36), r=70, sh_alpha=110, blur=24, off=(0, 14))
    sc = (576, 76, 1000, 1004)
    c.rect(sc, fill=(255, 255, 255), r=56)
    c.rect((740, 92, 836, 122), fill=(26, 28, 36), r=15)
    c.text((614, 108), "9:41", "sb", 22, (30, 30, 34), anchor="lm")
    x0, x1 = 606, 970
    c.text((x0, 168), "Mood check", "db", 30, NAVY, anchor="lm")
    c.rect((x1 - 102, 150, x1, 186), fill=(222, 242, 238), r=18)
    c.text((x1 - 51, 168), "PHQ-9", "sb", 22, TEAL, anchor="mm")
    c.text((x0, 224), "Question 1 of 9", "s", 24, GRAY, anchor="lm")
    c.rect((x0, 248, x1, 258), fill=(228, 230, 238), r=5)
    c.rect((x0, 248, x0 + (x1 - x0) / 9, 258), fill=TEAL, r=5)
    c.text((x0, 300), "Over the last 2 weeks:", "s", 26, GRAY, anchor="lm")
    y = c.block("Little interest or pleasure in doing things", "db", 36, 330, x1 - x0, NAVY, align="left", x=x0, max_lines=3)
    oy = y + 22
    for o in ("Not at all", "Several days", "More than half the days", "Nearly every day"):
        c.rect((x0, oy, x1, oy + 76), fill=(246, 247, 251), r=20, outline=(208, 212, 224), width=2)
        c.ellipse((x0 + 22, oy + 24, x0 + 50, oy + 52), fill=(255, 255, 255), outline=(150, 156, 172), width=3)
        c.block(o, "sb", 26, oy + 21, x1 - x0 - 90, (44, 48, 60), align="left", x=x0 + 70, max_lines=1)
        oy += 92
    for k in range(9):
        c.ellipse((720 + k * 24, 960, 732 + k * 24, 972), fill=TEAL if k == 0 else (210, 214, 224))
    c.save("psy-depression-multi-0929_b.png")


def chair(c, x, y, flip, col):
    s = -1 if flip else 1
    c.rect((x - 36, y - 10, x + 36, y + 22), fill=col, r=8)
    bx = (x - s * 36 - 12, y - 60, x - s * 36 + 12, y + 22) if s == 1 else (x + 36 - 12, y - 60, x + 36 + 12, y + 22)
    c.rect(bx, fill=col, r=8)
    c.rect((x - 30, y + 22, x - 22, y + 48), fill=(60, 70, 90))
    c.rect((x + 22, y + 22, x + 30, y + 48), fill=(60, 70, 90))


def icon_talk(c, cx, cy):
    chair(c, cx - 70, cy + 10, False, (18, 140, 132))
    chair(c, cx + 70, cy + 10, True, (240, 120, 90))
    c.rect((cx - 12, cy + 10, cx + 12, cy + 58), fill=(200, 150, 110), r=4)
    for dx, dy in ((-16, -8), (14, -12), (0, -26)):
        c.ellipse((cx + dx - 12, cy + dy - 8, cx + dx + 12, cy + dy + 22), fill=(90, 170, 110))


def icon_laptop(c, cx, cy):
    c.rect((cx - 86, cy - 62, cx + 86, cy + 42), fill=NAVY, r=10)
    c.rect((cx - 74, cy - 50, cx + 74, cy + 32), fill=(220, 238, 246), r=4)
    c.ellipse((cx - 18, cy - 36, cx + 18, cy), fill=(18, 140, 132))
    c.rect((cx - 34, cy + 4, cx + 34, cy + 32), fill=(18, 140, 132), r=16)
    c.poly([(cx - 110, cy + 46), (cx + 110, cy + 46), (cx + 96, cy + 62), (cx - 96, cy + 62)], (150, 160, 180))


def icon_tms(c, cx, cy):
    # голова в профиль (без лица) + катушка-«восьмёрка» на кронштейне
    c.ellipse((cx - 30, cy - 36, cx + 50, cy + 44), fill=(240, 196, 160))
    c.rect((cx - 6, cy + 30, cx + 26, cy + 64), fill=(240, 196, 160))
    c.rect((cx - 40, cy + 58, cx + 60, cy + 70), fill=(18, 140, 132), r=6)
    c.line([(cx + 110, cy + 64), (cx + 110, cy - 76), (cx + 30, cy - 76), (cx + 30, cy - 58)], (150, 160, 180), 8)
    c.ellipse((cx - 16, cy - 66, cx + 22, cy - 34), fill=(240, 120, 90))
    c.ellipse((cx + 18, cy - 66, cx + 56, cy - 34), fill=(240, 120, 90))
    c.ellipse((cx - 4, cy - 58, cx + 10, cy - 42), fill=(253, 238, 232))
    c.ellipse((cx + 30, cy - 58, cx + 44, cy - 42), fill=(253, 238, 232))


def icon_card(c, cx, cy):
    c.rect((cx - 96, cy - 50, cx + 56, cy + 44), fill=(18, 140, 132), r=12)
    c.rect((cx - 96, cy - 30, cx + 56, cy - 16), fill=(12, 100, 96))
    c.rect((cx - 80, cy + 10, cx - 20, cy + 20), fill=(200, 236, 230), r=4)
    for k in range(4):
        c.ellipse((cx + 40, cy + 40 - k * 16, cx + 104, cy + 60 - k * 16), fill=(246, 190, 60), outline=(206, 150, 40), width=2)
    c.poly([(cx - 30, cy - 70), (cx + 6, cy - 58), (cx + 6, cy - 30), (cx - 30, cy - 10), (cx - 66, cy - 30), (cx - 66, cy - 58)], (240, 120, 90))


def c_():
    """Сетка выбора: 4 варианта лечения, у каждого одинаковое «Learn more»."""
    c = C((247, 249, 251))
    y = c.block("Depression treatment in 2026", "db", 60, 42, 1000, NAVY, max_lines=1)
    c.block("From talk therapy to TMS: how the options compare", "s", 34, y + 4, 980, GRAY, max_lines=1)
    tiles = [("Talk therapy", icon_talk, (228, 244, 241)), ("Online therapy", icon_laptop, (232, 238, 250)),
             ("TMS", icon_tms, (253, 238, 232)), ("Cost & insurance", icon_card, (246, 242, 226))]
    boxes = [(50, 196, 525, 566), (555, 196, 1030, 566), (50, 590, 525, 960), (555, 590, 1030, 960)]
    for (lab, ic, fill), bx in zip(tiles, boxes):
        c.card(bx, fill=fill, r=28, sh_alpha=45, blur=10, off=(0, 5))
        cx = (bx[0] + bx[2]) / 2
        ic(c, cx, bx[1] + 110)
        c.text((cx, bx[1] + 232), lab, "db", 38, NAVY, anchor="mm")
        c.button("Learn more", cx, bx[1] + 312, size=28, fill=TEAL, padx=36, pady=14, shadow=False)
    c.text((W / 2, 1012), "Plus: the 9-question mood test doctors use, score 0–27", "s", 28, GRAY, anchor="mm")
    c.save("psy-depression-multi-0929_c.png")


def d():
    """Только крупный текст на тёмном фоне."""
    c = C((18, 28, 56))
    c.vgrad((0, 0, W, W), (22, 34, 68), (12, 20, 42))
    c.text((80, 96), "T H E   M O O D   T E S T   D O C T O R S   U S E", "sb", 26, (110, 214, 196))
    y = 160
    for t, col in (("3 minutes.", (255, 255, 255)), ("9 questions.", (255, 255, 255)), ("Score 0–27.", (255, 206, 92))):
        c.text((76, y), t, "db", 118, col)
        y += 150
    c.hgrad((82, y + 12, 1000, y + 30), SCALE)
    y = c.block("What each score range means – and which treatment options exist in 2026", "s", 40, y + 70, 900, (206, 214, 232), align="left", x=80, max_lines=3)
    c.button("Learn more", 80 + 170, 968, size=42, fill=(236, 84, 64), padx=52)
    c.save("psy-depression-multi-0929_d.png")


if __name__ == "__main__":
    for f in sys.argv[1:]:
        globals()[f if f != "c" else "c_"]()
