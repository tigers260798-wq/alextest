"""Сцены-иллюстрации (концепция d) и «герои» для сеток. Плоская иллюстрация, без людей с лицами,
без логотипов, гербов, эмблем и знаков различия. Каждая сцена своя — между пакетами кадр не повторяется."""
import math
import random
from PIL import Image, ImageDraw
from p60_lib import W, mix, rotpts
import p60_icons as I

WH = (255, 255, 255)


# ---------- помощники
def masked(c, pts, draw_fn, rr=0):
    """Рисует draw_fn(dd) на отдельном слое и обрезает по многоугольнику pts (rr > 0 — по скруглённому прямоугольнику)."""
    lay = Image.new("RGBA", c.im.size, (0, 0, 0, 0))
    dd = ImageDraw.Draw(lay)
    draw_fn(dd)
    mask = Image.new("L", c.im.size, 0)
    if rr:
        xs = [q[0] for q in pts]
        ys = [q[1] for q in pts]
        ImageDraw.Draw(mask).rounded_rectangle(c.sb((min(xs), min(ys), max(xs), max(ys))), c.s(rr), fill=255)
    else:
        ImageDraw.Draw(mask).polygon(c.sp(pts), fill=255)
    a = lay.getchannel("A")
    from PIL import ImageChops
    lay.putalpha(ImageChops.multiply(a, mask))
    c.im.alpha_composite(lay)


def camo(c, pts, base, blobs, seed=3, n=70, rmin=14, rmax=40, rr=0):
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    rnd = random.Random(seed)

    def fn(dd):
        dd.polygon(c.sp(pts), fill=base + (255,))
        for i in range(n):
            col = blobs[i % len(blobs)]
            x = rnd.uniform(min(xs), max(xs))
            y = rnd.uniform(min(ys), max(ys))
            rx, ry = rnd.uniform(rmin, rmax), rnd.uniform(rmin * 0.6, rmax * 0.7)
            dd.ellipse(c.sb((x - rx, y - ry, x + rx, y + ry)), fill=col + (255,))
    masked(c, pts, fn, rr=rr)


def wood(c, box, c0, c1, lines=10, seed=1, grain=None):
    c.vgrad(box, c0, c1)
    rnd = random.Random(seed)
    x0, y0, x1, y1 = box
    g = grain or mix(c1, (0, 0, 0), 0.12)
    for i in range(lines):
        y = y0 + (i + 0.5) * (y1 - y0) / lines + rnd.uniform(-6, 6)
        pts = [(x, y + math.sin(x / rnd.uniform(60, 140) + i) * 3) for x in range(int(x0), int(x1) + 20, 20)]
        c.line(pts, g, 2, alpha=90)


def plant(c, cx, by, s=1.0, pot=(214, 110, 70), leaf=(64, 140, 90)):
    for k, (ang, L) in enumerate(((-60, 130), (-30, 170), (-5, 190), (20, 160), (50, 120), (-80, 90), (75, 95))):
        a = math.radians(ang - 90)
        tip = (cx + math.cos(a) * L * s, by - 70 * s + math.sin(a) * L * s)
        mid = ((cx + tip[0]) / 2, (by - 70 * s + tip[1]) / 2)
        nx, ny = -math.sin(a) * 22 * s, math.cos(a) * 22 * s
        c.poly([(cx, by - 70 * s), (mid[0] + nx, mid[1] + ny), tip, (mid[0] - nx, mid[1] - ny)], mix(leaf, (0, 0, 0), 0.15 * (k % 2)))
    c.poly([(cx - 58 * s, by - 80 * s), (cx + 58 * s, by - 80 * s), (cx + 44 * s, by), (cx - 44 * s, by)], pot)
    c.rect((cx - 64 * s, by - 92 * s, cx + 64 * s, by - 72 * s), fill=mix(pot, (0, 0, 0), 0.1), r=4)


def teacup(c, cx, cy, s=1.0, col=WH, rim=(200, 80, 60), tea=(170, 110, 60), steam=True):
    c.ellipse((cx - 70 * s, cy + 18 * s, cx + 70 * s, cy + 44 * s), fill=mix(col, (0, 0, 0), 0.08))
    c.poly([(cx - 46 * s, cy - 30 * s), (cx + 46 * s, cy - 30 * s), (cx + 34 * s, cy + 28 * s), (cx - 34 * s, cy + 28 * s)], col)
    c.ellipse((cx - 46 * s, cy - 40 * s, cx + 46 * s, cy - 20 * s), fill=tea, outline=col, width=5 * s)
    c.arc((cx + 30 * s, cy - 20 * s, cx + 70 * s, cy + 16 * s), 270, 90, col, 9 * s)
    c.line([(cx - 40 * s, cy - 8 * s), (cx + 40 * s, cy - 8 * s)], rim, 5 * s)
    if steam:
        for k in (-1, 1):
            pts = [(cx + k * 14 * s + math.sin(t / 5) * 8 * s, cy - 50 * s - t * 3 * s) for t in range(0, 22)]
            c.line(pts, (255, 255, 255), 5 * s, alpha=150)


def glasses(c, cx, cy, s=1.0, col=(40, 36, 34)):
    r = 30 * s
    c.ellipse((cx - 2.3 * r, cy - r * 0.8, cx - 0.3 * r, cy + r * 0.8), fill=(220, 236, 246), outline=col, width=6 * s, alpha=255)
    c.ellipse((cx + 0.3 * r, cy - r * 0.8, cx + 2.3 * r, cy + r * 0.8), fill=(220, 236, 246), outline=col, width=6 * s)
    c.arc((cx - 0.45 * r, cy - 0.5 * r, cx + 0.45 * r, cy + 0.3 * r), 200, 340, col, 6 * s)
    c.line([(cx - 2.3 * r, cy - 0.1 * r), (cx - 3.1 * r, cy - 0.5 * r)], col, 6 * s)
    c.line([(cx + 2.3 * r, cy - 0.1 * r), (cx + 3.1 * r, cy - 0.5 * r)], col, 6 * s)


def pen(c, x0, y0, x1, y1, col=(30, 60, 140), w=14):
    c.line([(x0, y0), (x1, y1)], col, w)
    L = math.hypot(x1 - x0, y1 - y0)
    ux, uy = (x1 - x0) / L, (y1 - y0) / L
    tip = (x1 + ux * 26, y1 + uy * 26)
    nx, ny = -uy * w / 2, ux * w / 2
    c.poly([(x1 + nx, y1 + ny), tip, (x1 - nx, y1 - ny)], (230, 214, 180))
    c.line([(x0 + ux * 20 + nx * 1.4, y0 + uy * 20 + ny * 1.4), (x0 + ux * 90 + nx * 1.4, y0 + uy * 90 + ny * 1.4)], (200, 200, 205), 4)


def paper(c, box, ang, col=WH, lines=7, head=None, head_col=(40, 40, 50), line_col=(196, 200, 210), shadow=True, head_size=26):
    """Лист бумаги с заголовком и строками, повёрнутый на ang градусов вокруг своего центра."""
    x0, y0, x1, y1 = box
    w_, h_ = c.s(x1 - x0), c.s(y1 - y0)
    K = c.K
    img = Image.new("RGBA", (w_, h_), col + (255,))
    dd = ImageDraw.Draw(img)
    y = 40
    if head:
        dd.text((30 * K, 24 * K), head, font=c.font("sb", head_size), fill=head_col + (255,))
        dd.line([(30 * K, (34 + head_size) * K), (w_ - 30 * K, (34 + head_size) * K)], fill=line_col + (255,), width=2 * K)
        y = 60 + head_size
    rnd = random.Random(int(x0 * 7 + y0))
    step = (y1 - y0 - y - 30) / max(1, lines)
    for k in range(lines):
        lw = (x1 - x0 - 60) * (0.5 + 0.5 * rnd.random())
        dd.rounded_rectangle((30 * K, int(y * K), int((30 + lw) * K), int((y + 9) * K)), 4 * K, fill=line_col + (255,))
        if k % 3 == 1:
            dd.rounded_rectangle((int((x1 - x0 - 150) * K), int(y * K), int((x1 - x0 - 30) * K), int((y + 9) * K)), 4 * K, fill=mix(line_col, head_col, 0.3) + (255,))
        y += step
    rot = img.rotate(-ang, expand=True, resample=Image.BICUBIC)
    cx, cy = c.s((x0 + x1) / 2), c.s((y0 + y1) / 2)
    if shadow:
        sh = Image.new("RGBA", rot.size, (0, 0, 0, 0))
        sh.putalpha(rot.getchannel("A").point(lambda v: v * 50 // 255))
        c.im.alpha_composite(sh, (cx - rot.width // 2 + 8 * K, cy - rot.height // 2 + 12 * K))
    c.im.alpha_composite(rot, (cx - rot.width // 2, cy - rot.height // 2))


# ---------- 1. AA: гостиная с креслом (текст сверху)
def living(c, top=400):
    TEAL = (24, 110, 118)
    c.vgrad((0, 0, W, 800), (252, 246, 236), (242, 230, 212))
    wood(c, (0, 800, W, W), (214, 170, 124), (190, 144, 100), lines=6, seed=4)
    c.rect((0, 790, W, 806), fill=(250, 244, 234))
    # окно
    wx0, wy0, wx1, wy1 = 640, top + 10, 990, 770
    c.rect((wx0 - 14, wy0 - 14, wx1 + 14, wy1 + 14), fill=WH, r=6)
    c.vgrad((wx0, wy0, wx1, wy1), (168, 214, 240), (224, 240, 248))
    for (x, y, r) in ((700, 700, 70), (790, 720, 80), (900, 690, 90), (980, 730, 60)):
        c.circle(x, y, r, fill=(120, 176, 110))
    c.rect((wx0, wy1 - 60, wx1, wy1), fill=(120, 176, 110))
    c.rect(((wx0 + wx1) / 2 - 7, wy0, (wx0 + wx1) / 2 + 7, wy1), fill=WH)
    c.rect((wx0, (wy0 + wy1) / 2 - 7, wx1, (wy0 + wy1) / 2 + 7), fill=WH)
    c.rect((wx0 - 30, wy1 + 10, wx1 + 30, wy1 + 28), fill=(240, 234, 224), r=4)
    # шторы
    for x0, x1 in ((wx0 - 70, wx0 + 30), (wx1 - 30, wx1 + 70)):
        c.rect((x0, wy0 - 40, x1, wy1 + 20), fill=(214, 118, 84), r=10)
        for k in range(1, 4):
            xx = x0 + k * (x1 - x0) / 4
            c.line([(xx, wy0 - 30), (xx, wy1 + 10)], (190, 96, 66), 4)
    c.rect((wx0 - 90, wy0 - 52, wx1 + 90, wy0 - 38), fill=(120, 90, 70), r=6)
    # ковёр
    c.ellipse((40, 900, 800, 1060), fill=(232, 206, 170))
    c.ellipse((90, 920, 750, 1040), outline=(214, 180, 140), width=6)
    # кресло
    c.shadow((110, 820, 540, 910), r=40, alpha=60, blur=14, off=(0, 6))
    c.rect((170, top + 150, 470, 800), fill=TEAL, r=60)
    c.rect((200, top + 180, 440, 760), fill=mix(TEAL, WH, 0.12), r=46)
    c.rect((120, 690, 520, 850), fill=mix(TEAL, (0, 0, 0), 0.08), r=40)
    c.rect((150, 700, 490, 790), fill=mix(TEAL, WH, 0.18), r=30)
    c.rect((100, 620, 200, 860), fill=TEAL, r=40)
    c.rect((440, 620, 540, 860), fill=TEAL, r=40)
    for x in (140, 500):
        c.rect((x - 10, 850, x + 10, 900), fill=(110, 76, 50), r=4)
    # плед
    c.poly([(430, 610), (540, 620), (545, 760), (470, 750)], (236, 184, 64))
    for k in range(4):
        c.line([(440 + k * 25, 615 + k * 2), (478 + k * 20, 752)], (214, 160, 40), 4)
    c.rect((240, 600, 380, 690), fill=(236, 184, 64), r=26)
    # столик с чаем и письмом
    c.ellipse((560, 740, 700, 780), fill=(150, 104, 70))
    c.rect((622, 760, 638, 900), fill=(130, 90, 60))
    c.ellipse((586, 890, 674, 910), fill=(130, 90, 60))
    teacup(c, 612, 718, 0.55, rim=(24, 110, 118))
    c.poly([(640, 752), (700, 740), (708, 766), (648, 778)], WH)
    c.line([(640, 752), (676, 762), (700, 740)], (196, 200, 210), 3)
    # растение
    plant(c, 1010, 1000, 0.9)


# ---------- 2. CTR: улица таунхаусов (текст на небе)
def street(c, top=430):
    c.vgrad((0, 0, W, 900), (196, 226, 244), (238, 246, 250))
    for (x, y, r) in ((120, 360, 60), (190, 350, 70), (260, 368, 52), (820, 300, 50), (880, 290, 64), (950, 304, 48)):
        c.circle(x, y, r, fill=WH, alpha=200)
    bricks = [(176, 84, 62), (196, 120, 84), (150, 78, 70), (204, 146, 96)]
    doors = [(28, 50, 96), (200, 40, 44), (30, 110, 72), (236, 180, 50)]
    hw = W / 4
    for i in range(4):
        x0 = i * hw
        x1 = x0 + hw
        b = bricks[i]
        c.rect((x0, top + 60, x1, 900), fill=b)
        for r_ in range(int(top + 70), 900, 26):
            c.line([(x0, r_), (x1, r_)], mix(b, (0, 0, 0), 0.08), 2)
        c.poly([(x0 - 4, top + 64), (x0 + hw * 0.5, top - 30), (x1 + 4, top + 64)], (70, 76, 90))
        c.rect((x0 + hw * 0.62, top - 40, x0 + hw * 0.62 + 44, top + 20), fill=mix(b, (0, 0, 0), 0.15))
        for k in range(2):
            c.rect((x0 + hw * 0.62 + 4 + k * 20, top - 60, x0 + hw * 0.62 + 18 + k * 20, top - 40), fill=(186, 100, 70))
        # окна
        for (wx, wy) in ((x0 + 36, top + 110), (x0 + hw - 116, top + 110)):
            c.rect((wx - 8, wy - 8, wx + 88, wy + 128), fill=WH)
            c.rect((wx, wy, wx + 80, wy + 120), fill=(150, 196, 222))
            c.rect((wx + 37, wy, wx + 43, wy + 120), fill=WH)
            c.rect((wx, wy + 57, wx + 80, wy + 63), fill=WH)
        # эркер
        c.rect((x0 + 28, top + 300, x0 + 140, top + 440), fill=WH)
        c.rect((x0 + 38, top + 310, x0 + 130, top + 430), fill=(150, 196, 222))
        # дверь
        dx = x0 + hw - 100
        c.pie((dx - 6, top + 270, dx + 76, top + 330), 180, 360, WH)
        c.rect((dx, top + 300, dx + 70, top + 460), fill=doors[i])
        c.rect((dx + 18, top + 380, dx + 52, top + 388), fill=(236, 200, 110))
        c.circle(dx + 58, top + 420, 5, fill=(236, 200, 110))
        c.rect((dx - 10, top + 460, dx + 80, top + 472), fill=(210, 210, 214))
    # письмо в щели
    c.poly([(3 * hw - 100 + 14, top + 368), (3 * hw - 100 + 58, top + 360), (3 * hw - 100 + 60, top + 384), (3 * hw - 100 + 16, top + 390)], WH)
    # тротуар
    c.rect((0, 900, W, W), fill=(206, 208, 212))
    for x in range(0, W, 120):
        c.line([(x, 900), (x - 40, W)], (186, 188, 194), 3)
    c.rect((0, 896, W, 910), fill=(180, 182, 188))
    # ярлык % на второй двери
    tx, ty = hw + 80, top + 230
    c.line([(tx + 60, top + 60), (tx + 44, ty - 40)], (60, 60, 60), 3)
    I.percent_tag(c, tx + 40, ty, 150, (240, 190, 40), bg=WH)


# ---------- 3. Ванная: душ без поддона, поручень, откидное сиденье
def bathroom(c, y_text=560):
    wall = (226, 242, 244)
    c.rect((0, 0, W, 860), fill=wall)
    for x in range(0, W, 90):
        c.line([(x, 0), (x, 860)], (204, 226, 230), 3)
    for y in range(0, 860, 90):
        c.line([(0, y), (W, y)], (204, 226, 230), 3)
    c.rect((0, 860, W, W), fill=(180, 200, 212))
    for x in range(0, W, 110):
        c.line([(x, 860), (x - 60, W)], (164, 186, 200), 3)
    c.line([(0, 960), (W, 960)], (164, 186, 200), 3)
    # душевая зона справа
    sx0, sx1 = 600, 1040
    c.rect((sx0, 860, sx1, 900), fill=(200, 216, 226))
    c.rect((sx0 + 180, 868, sx0 + 260, 880), fill=(140, 150, 160), r=4)
    c.line([(sx1 - 60, 620), (sx1 - 60, 250), (sx1 - 190, 250), (sx1 - 190, 290)], (160, 170, 180), 12)
    c.pie((sx1 - 250, 270, sx1 - 130, 340), 180, 360, (160, 170, 180))
    for i in range(6):
        x = sx1 - 234 + i * 18
        c.line([(x, 312), (x - 18 + i * 6, 560)], (120, 190, 230), 4, alpha=160)
    # откидное сиденье
    c.rect((sx1 - 150, 600, sx1 - 10, 620), fill=(250, 250, 250), r=6)
    c.rect((sx1 - 150, 620, sx1 - 10, 640), fill=(210, 216, 222), r=6)
    c.line([(sx1 - 140, 640), (sx1 - 20, 700)], (170, 176, 184), 6)
    # поручень
    c.circle(sx0 + 70, 540, 14, fill=(170, 176, 184))
    c.circle(sx0 + 260, 540, 14, fill=(170, 176, 184))
    c.rect((sx0 + 64, 530, sx0 + 266, 550), fill=(200, 206, 214), r=10)
    # стекло
    c.rect((sx0, 150, sx0 + 18, 860), fill=(200, 210, 220))
    c.rect((sx0 + 18, 150, sx0 + 150, 860), fill=(200, 236, 250), alpha=110)
    c.line([(sx0 + 40, 200), (sx0 + 120, 120 + 200)], WH, 6, alpha=180)
    # полотенцесушитель и полотенце слева
    c.rect((60, 640, 360, 652), fill=(180, 186, 194), r=6)
    c.rect((90, 646, 250, 820), fill=(242, 140, 110), r=10)
    c.rect((90, 780, 250, 796), fill=(250, 180, 150))
    # коврик
    c.rect((180, 930, 460, 1010), fill=(250, 250, 250), r=20)
    c.rect((196, 944, 444, 996), outline=(210, 220, 230), width=4, r=16)
    plant(c, 480, 860, 0.7, pot=(240, 240, 240), leaf=(70, 150, 110))


# ---------- 4. Кредитки 60+: стол с пенсионным письмом, очками, чаем и картой
def table_card(c, table_y=700):
    c.vgrad((0, 0, W, table_y), (244, 241, 236), (230, 224, 216))
    c.dots((0, 0, W, table_y), 40, 2.5, (200, 190, 180), alpha=60)
    wood(c, (0, table_y, W, W), (186, 130, 86), (160, 108, 70), lines=8, seed=7)
    c.rect((0, table_y - 6, W, table_y + 6), fill=(150, 100, 64))
    paper(c, (60, table_y + 70, 400, table_y + 420), -8, head="PENSION STATEMENT", lines=6)
    glasses(c, 250, table_y + 250, 1.0)
    teacup(c, 900, table_y + 130, 0.9, rim=(20, 40, 90))
    I.card(c, 700, table_y + 270, 260, (22, 40, 96), stripe=None, ang=14)
    I.card(c, 640, table_y + 300, 260, (212, 170, 60), ang=-6)
    pen(c, 470, table_y + 330, 560, table_y + 200, col=(20, 40, 90))


# ---------- 5. Beamte: рабочий стол сверху — лист выплат, калькулятор, ручка, папка
def desk_top(c):
    wood(c, (0, 0, W, W), (196, 150, 104), (176, 128, 86), lines=18, seed=11)
    # папка вверху справа
    c.poly(rotpts([(760, -40), (1120, -40), (1120, 300), (760, 300)], 940, 130, 10), (40, 96, 150))
    c.poly(rotpts([(780, -20), (1100, -20), (1100, 60), (780, 60)], 940, 130, 10), (60, 120, 176))
    # кружка вверху слева
    c.circle(120, 110, 96, fill=(250, 250, 250))
    c.circle(120, 110, 74, fill=(110, 70, 40))
    c.circle(120, 110, 60, fill=(140, 92, 56))
    c.rect((200, 90, 250, 130), fill=(250, 250, 250), r=18)
    # лист выплат снизу слева
    paper(c, (40, 690, 470, 1150), -6, head="Bezügemitteilung", lines=7)
    # калькулятор справа снизу
    cx, cy = 840, 880
    c.shadow((cx - 150, cy - 210, cx + 150, cy + 210), r=24, alpha=70, blur=10, off=(8, 12))
    I.calc(c, cx, cy, 500, (44, 50, 60), screen=(200, 226, 204), txt="2026")
    pen(c, 520, 1040, 640, 760, col=(30, 30, 36))


# ---------- 6. Учителя: доска и стол
def classroom(c, board_bottom=700):
    c.rect((0, 0, W, W), fill=(236, 226, 206))
    c.rect((30, 30, W - 30, board_bottom), fill=(146, 104, 64), r=10)
    c.rect((50, 50, W - 50, board_bottom - 20), fill=(40, 78, 62))
    rnd = random.Random(5)
    for i in range(24):
        x, y = rnd.uniform(70, W - 90), rnd.uniform(70, board_bottom - 60)
        c.line([(x, y), (x + rnd.uniform(40, 140), y + rnd.uniform(-10, 10))], (70, 110, 92), 6, alpha=80)
    c.rect((80, board_bottom - 20, W - 80, board_bottom - 4), fill=(160, 116, 74))
    for x, col in ((150, WH), (200, (250, 220, 90)), (240, (240, 150, 150))):
        c.rect((x, board_bottom - 32, x + 34, board_bottom - 20), fill=col, r=4)
    wood(c, (0, board_bottom + 60, W, W), (206, 156, 104), (184, 134, 88), lines=5, seed=2)
    c.rect((0, board_bottom + 50, W, board_bottom + 66), fill=(160, 112, 70))
    # стопка тетрадей
    by = W - 40
    for k, col in enumerate(((40, 110, 170), (230, 120, 60), (60, 150, 100), (200, 60, 70))):
        y = by - 34 * (k + 1)
        c.rect((60 + k * 6, y, 330 + k * 6, y + 30), fill=col, r=4)
        c.rect((66 + k * 6, y + 4, 324 + k * 6, y + 10), fill=WH, alpha=200)
    # яблоко
    c.circle(220, by - 200, 58, fill=(214, 44, 40))
    c.circle(268, by - 200, 54, fill=(220, 54, 46))
    c.line([(248, by - 254), (256, by - 280)], (100, 64, 36), 7)
    c.poly([(256, by - 270), (300, by - 294), (284, by - 258)], (80, 160, 70))
    # очки и красная ручка справа
    glasses(c, 860, by - 60, 0.9)
    pen(c, 690, by - 20, 1010, by - 120, col=(210, 40, 40), w=12)
    # стакан с карандашами
    c.rect((940, by - 260, 1030, by - 150), fill=(60, 90, 140), r=10)
    for k, col in enumerate(((240, 200, 60), (80, 160, 90), (220, 80, 70))):
        c.line([(955 + k * 28, by - 250), (948 + k * 32, by - 330)], col, 12)


# ---------- 7. Силовики: стул с курткой, кепкой и ботинками (без знаков различия)
def uniform_chair(c, floor_y=880):
    c.vgrad((0, 0, W, floor_y), (236, 230, 214), (222, 214, 194))
    wood(c, (0, floor_y, W, W), (170, 128, 88), (150, 110, 74), lines=4, seed=9)
    c.rect((0, floor_y - 30, W, floor_y), fill=(250, 246, 236))
    # стул
    CH = (126, 84, 52)
    c.rect((700, 360, 730, 1050), fill=CH, r=8)
    c.rect((960, 360, 990, 1050), fill=CH, r=8)
    c.rect((700, 390, 990, 430), fill=mix(CH, WH, 0.1), r=10)
    c.rect((700, 470, 990, 500), fill=mix(CH, WH, 0.1), r=10)
    c.rect((660, 700, 1030, 740), fill=mix(CH, WH, 0.15), r=8)
    c.rect((670, 740, 692, 1050), fill=CH, r=6)
    c.rect((1000, 740, 1022, 1050), fill=CH, r=6)
    # сложенная куртка
    OL = (104, 112, 72)
    blobs = [(70, 80, 50), (140, 130, 90), (60, 56, 40), (120, 124, 84)]
    camo(c, [(640, 610), (1050, 600), (1060, 704), (630, 712)], OL, blobs, seed=4)
    camo(c, [(660, 560), (1030, 552), (1040, 612), (650, 620)], OL, blobs, seed=8)
    c.line([(640, 612), (1050, 602)], (60, 64, 40), 3)
    c.line([(650, 562), (1030, 554)], (60, 64, 40), 3)
    # полевая кепка сверху, без кокарды и знаков
    CAP = (92, 100, 62)
    c.poly([(770, 548), (784, 478), (800, 466), (900, 462), (918, 474), (934, 548)], CAP)
    c.rect((772, 530, 934, 552), fill=mix(CAP, (0, 0, 0), 0.2), r=4)
    c.poly([(772, 544), (700, 556), (704, 570), (790, 562)], mix(CAP, (0, 0, 0), 0.3))
    c.line([(850, 466), (852, 530)], mix(CAP, (0, 0, 0), 0.2), 3)
    # ботинки на полу
    I.boots(c, 470, 950, 230, (46, 44, 40))


# ---------- 8. Робот-мойщик на большом окне в гостиной (без логотипа)
def bay_window(c, top=360):
    c.rect((0, 0, W, W), fill=(246, 242, 236))
    wx0, wy0, wx1, wy1 = 90, top, 990, 900
    c.rect((wx0 - 18, wy0 - 18, wx1 + 18, wy1 + 18), fill=WH, r=8)
    c.vgrad((wx0, wy0, wx1, wy1), (150, 204, 238), (220, 238, 248))
    c.glow((780, wy0 + 10, 960, wy0 + 190), (255, 246, 200), alpha=230, blur=30)
    for (x, y, r) in ((160, 840, 110), (300, 860, 120), (470, 830, 100), (640, 860, 130), (820, 840, 120), (960, 860, 100)):
        c.circle(x, y, r, fill=(118, 172, 112))
    c.rect((wx0, 860, wx1, wy1), fill=(118, 172, 112))
    for x in (390, 690):
        c.rect((x - 9, wy0, x + 9, wy1), fill=WH)
    # чистая полоса-змейка на среднем стекле
    pts = []
    for k in range(6):
        y = wy0 + 50 + k * 70
        pts += [(420, y), (660, y)] if k % 2 == 0 else [(660, y), (420, y)]
    c.line(pts, WH, 30, alpha=70)
    # страховочный шнур и робот
    c.line([(540, wy0), (548, wy0 + 60), (556, 460)], (230, 90, 60), 4)
    I.robot(c, 560, 520, 150, (52, 60, 72), acc=(90, 190, 240))
    c.rect((wx0 - 40, wy1 + 14, wx1 + 40, wy1 + 34), fill=(236, 230, 222), r=4)
    # пол, кресло, растение
    wood(c, (0, 934, W, W), (214, 176, 132), (196, 156, 112), lines=4, seed=3)
    c.rect((0, 924, W, 940), fill=(250, 246, 240))
    plant(c, 990, 1070, 0.8)


# ---------- фоны и «герои» для сеток
def classroom_board_bg(c):
    c.rect((0, 0, W, W), fill=(146, 104, 64))
    c.rect((22, 22, W - 22, W - 22), fill=(40, 78, 62))
    rnd = random.Random(12)
    for i in range(30):
        x, y = rnd.uniform(40, W - 160), rnd.uniform(40, W - 60)
        c.line([(x, y), (x + rnd.uniform(40, 160), y + rnd.uniform(-12, 12))], (70, 110, 92), 7, alpha=70)


def panel(c, box, fill, r=28, fill2=None):
    c.shadow(box, r=r, alpha=50, blur=12, off=(0, 6))
    if fill2:
        lay_c = fill
        c.rect(box, fill=fill, r=r)
        x0, y0, x1, y1 = box
        c.vgrad((x0, y0 + r, x1, y1 - r), fill, fill2)
        c.rect((x0, y1 - r * 2, x1, y1), fill=fill2, r=r)
        c.rect((x0, y0 + r, x1, y1 - r), fill=None)
    else:
        c.rect(box, fill=fill, r=r)


def hero_cc_house(c, box):
    """CTR: дом с ярлыками % и письмо-счёт (без символики советов)."""
    x0, y0, x1, y1 = box
    c.shadow(box, r=28, alpha=50, blur=12, off=(0, 6))
    c.rect(box, fill=(214, 236, 222), r=28)
    c.dots((x0 + 20, y0 + 20, x1 - 20, y1 - 20), 36, 3, (22, 110, 72), alpha=40)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    c.ellipse((cx - 250, y1 - 60, cx + 250, y1 - 20), fill=(22, 110, 72), alpha=40)
    I.house(c, cx, cy + 10, 250, (190, 96, 66), roof=(60, 66, 80), door=(28, 50, 96))
    I.percent_tag(c, cx + 230, cy - 50, 130, (240, 190, 40))
    I.percent_tag(c, cx - 250, cy + 40, 100, (22, 110, 72))
    I.envelope(c, cx - 250, cy - 80, 110, (22, 40, 70))


def hero_bath_crop(c, box):
    """Ванная: кадрированный душ (зеркально сцене d)."""
    from p60_lib import C as _C
    t = _C((255, 255, 255))
    bathroom(t)
    x0, y0, x1, y1 = box
    crop = t.im.crop((t.s(430), t.s(140), t.s(1080), t.s(140 + (650 * (y1 - y0) / (x1 - x0)))))
    crop = crop.transpose(Image.FLIP_LEFT_RIGHT).resize((c.s(x1 - x0), c.s(y1 - y0)), Image.LANCZOS)
    mask = Image.new("L", crop.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, crop.width - 1, crop.height - 1), c.s(28), fill=255)
    c.shadow(box, r=28, alpha=50, blur=12, off=(0, 6))
    c.im.paste(crop, (c.s(x0), c.s(y0)), mask)


def hero_cards(c, box):
    """Кредитки 60+: две карты без логотипов на тёмно-синей панели."""
    x0, y0, x1, y1 = box
    c.shadow(box, r=28, alpha=60, blur=14, off=(0, 8))
    c.rect(box, fill=(20, 34, 78), r=28)
    c.glow((x0 + 260, y0 + 20, x1 - 260, y1 - 20), (236, 190, 80), alpha=110, blur=50)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    I.card(c, cx - 70, cy + 6, 330, (236, 196, 90), chip=(250, 236, 180), ang=-10)
    I.card(c, cx + 80, cy - 4, 330, (240, 244, 250), chip=(236, 196, 90), ang=8)
    for k in range(4):
        pass
    c.text((x0 + 40, y1 - 40), "60+  ·  70+  ·  80+", "sb", 30, (236, 196, 90), anchor="ls")


def hero_camo(c, box):
    """Силовики: камуфляжная полоса, фуражка и ботинки без знаков."""
    x0, y0, x1, y1 = box
    c.shadow(box, r=28, alpha=60, blur=12, off=(0, 6))
    r = 28
    pts = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
    camo(c, pts, (104, 112, 72), [(70, 80, 50), (140, 130, 90), (60, 56, 40), (120, 124, 84)], seed=21, n=90, rmin=20, rmax=60, rr=r)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    c.rect((cx - 300, cy - 70, cx + 300, cy + 70), fill=(250, 246, 234), r=35, alpha=240)
    c.text((cx, cy), "Oferty banków 2026", "db", 46, (60, 66, 40), anchor="mm")


def hero_robot(c, box):
    """Робот против мойщика: два стекла, слева робот, справа склиз с каплями."""
    x0, y0, x1, y1 = box
    c.shadow(box, r=28, alpha=50, blur=12, off=(0, 6))
    c.rect(box, fill=(255, 255, 255), r=28)
    ix0, iy0, ix1, iy1 = x0 + 18, y0 + 18, x1 - 18, y1 - 18
    c.vgrad((ix0, iy0, ix1, iy1), (150, 204, 238), (222, 240, 250))
    for (x, r) in ((ix0 + 80, 90), (ix0 + 250, 110), (ix0 + 470, 100), (ix0 + 700, 120), (ix1 - 40, 90)):
        c.circle(x, iy1 - 10, r, fill=(118, 172, 112))
    c.rect(((ix0 + ix1) / 2 - 10, iy0, (ix0 + ix1) / 2 + 10, iy1), fill=WH)
    c.glow((ix1 - 200, iy0 - 20, ix1 - 40, iy0 + 140), (255, 246, 200), alpha=200, blur=30)
    lx = (ix0 + (ix0 + ix1) / 2) / 2
    rx = ((ix0 + ix1) / 2 + ix1) / 2
    c.line([(lx, iy0), (lx + 6, (iy0 + iy1) / 2 - 90)], (230, 90, 60), 4)
    I.robot(c, lx + 10, (iy0 + iy1) / 2 - 10, 170, (52, 60, 72), acc=(90, 190, 240))
    I.squeegee(c, rx, (iy0 + iy1) / 2, 200, (40, 80, 150))
    c.rect((ix0 + 20, iy0 + 20, ix0 + 170, iy0 + 64), fill=WH, r=22, alpha=230)
    c.text((ix0 + 95, iy0 + 42), "Robot", "sb", 26, (20, 50, 90), anchor="mm")
    c.rect(((ix0 + ix1) / 2 + 30, iy0 + 20, (ix0 + ix1) / 2 + 250, iy0 + 64), fill=WH, r=22, alpha=230)
    c.text(((ix0 + ix1) / 2 + 140, iy0 + 42), "Professionnel", "sb", 26, (20, 50, 90), anchor="mm")
