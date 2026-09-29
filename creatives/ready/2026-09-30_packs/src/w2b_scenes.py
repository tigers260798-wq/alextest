"""Сцены-иллюстрации и «герои» пакетов волны 2 (w2b, 30.09). Плоская иллюстрация Pillow: без лиц,
без логотипов, гербов, флагов и эмблем. Каждая сцена своя — между пакетами кадр не повторяется."""
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import p60_lib
from p60_lib import W, mix, rotpts
import p60_icons as I
import p60_scenes as S
import w2b_icons  # noqa: F401  (регистрирует новые иконки)

p60_lib.F.setdefault("sbi", "/usr/share/fonts/truetype/liberation/LiberationSans-BoldItalic.ttf")
p60_lib.F.setdefault("dbo", "/usr/share/fonts/truetype/dejavu/DejaVuSans-BoldOblique.ttf")
WH = (255, 255, 255)


# ------------------------------------------------------------------ помощники
def note(c, cx, cy, w, h, ang, col, lines, ink=(40, 40, 50), size=34, font="sbi"):
    """Стикер-записка, повёрнутая на ang, с текстом (строки списком)."""
    from PIL import Image, ImageDraw
    K = c.K
    img = Image.new("RGBA", (int(w * K), int(h * K)), col + (255,))
    dd = ImageDraw.Draw(img)
    dd.rectangle((0, 0, img.width, int(18 * K)), fill=mix(col, (0, 0, 0), 0.08) + (255,))
    fnt = c.font(font, size)
    asc, desc = fnt.getmetrics()
    lh = (asc + desc) * 1.05
    y = (img.height - lh * len(lines)) / 2 + 6 * K
    for ln in lines:
        tw = dd.textbbox((0, 0), ln, font=fnt)[2]
        dd.text(((img.width - tw) / 2, y), ln, font=fnt, fill=ink + (255,))
        y += lh
    rot = img.rotate(-ang, expand=True, resample=Image.BICUBIC)
    sh = Image.new("RGBA", rot.size, (0, 0, 0, 0))
    sh.putalpha(rot.getchannel("A").point(lambda v: v * 60 // 255))
    X, Y = c.s(cx), c.s(cy)
    c.im.alpha_composite(sh, (X - rot.width // 2 + 6 * K, Y - rot.height // 2 + 10 * K))
    c.im.alpha_composite(rot, (X - rot.width // 2, Y - rot.height // 2))


def senior_back(c, cx, by, s, coat, hair=(226, 226, 230), hat=None, bun=False):
    """Пожилой человек со спины, сидит (голова, плечи, спина). by — линия сиденья."""
    c.rect((cx - 70 * s, by - 190 * s, cx + 70 * s, by + 10 * s), fill=coat, r=60 * s)
    c.rect((cx - 70 * s, by - 90 * s, cx + 70 * s, by + 10 * s), fill=coat, r=20 * s)
    c.rect((cx - 22 * s, by - 222 * s, cx + 22 * s, by - 180 * s), fill=(226, 180, 150), r=10 * s)
    c.circle(cx, by - 250 * s, 50 * s, fill=hair)
    if bun:
        c.circle(cx, by - 292 * s, 22 * s, fill=hair)
    if hat:
        c.pie((cx - 54 * s, by - 314 * s, cx + 54 * s, by - 210 * s), 180, 360, hat)
        c.rect((cx - 66 * s, by - 266 * s, cx + 66 * s, by - 254 * s), fill=hat, r=6 * s)
    c.ellipse((cx - 60 * s, by - 262 * s, cx - 42 * s, by - 232 * s), fill=(220, 172, 142))
    c.ellipse((cx + 42 * s, by - 262 * s, cx + 60 * s, by - 232 * s), fill=(220, 172, 142))


def tree(c, cx, by, s, trunk=(120, 84, 56), leaves=((226, 128, 50), (240, 170, 60), (200, 90, 40)), seed=1):
    rnd = random.Random(seed)
    c.poly([(cx - 16 * s, by), (cx + 16 * s, by), (cx + 9 * s, by - 200 * s), (cx - 9 * s, by - 200 * s)], trunk)
    c.line([(cx, by - 150 * s), (cx - 60 * s, by - 230 * s)], trunk, 12 * s)
    c.line([(cx, by - 170 * s), (cx + 70 * s, by - 250 * s)], trunk, 12 * s)
    for k in range(16):
        a = rnd.uniform(0, 2 * math.pi)
        r = rnd.uniform(0, 110 * s)
        x, y = cx + math.cos(a) * r * 1.2, by - 280 * s + math.sin(a) * r * 0.8
        rr = rnd.uniform(55, 85) * s
        c.circle(x, y, rr, fill=leaves[k % len(leaves)])


def shelf_books(c, x0, y, x1, seed=2, cols=((196, 80, 60), (60, 110, 160), (230, 180, 60), (90, 140, 100), (130, 90, 150), (220, 220, 210))):
    rnd = random.Random(seed)
    x = x0
    while x < x1 - 20:
        w = rnd.uniform(18, 34)
        h = rnd.uniform(70, 110)
        if rnd.random() < 0.12:
            c.poly(rotpts([(x, y), (x + w, y), (x + w, y - h), (x, y - h)], x, y, 14), cols[rnd.randrange(len(cols))])
            x += w + 26
            continue
        c.rect((x, y - h, x + w, y), fill=cols[rnd.randrange(len(cols))], r=3)
        c.rect((x + 3, y - h + 12, x + w - 3, y - h + 18), fill=WH, alpha=120)
        x += w + 3


def window(c, box, sky0=(176, 216, 240), sky1=(226, 240, 250), frame=(250, 250, 248), bars=True):
    x0, y0, x1, y1 = box
    c.rect((x0 - 14, y0 - 14, x1 + 14, y1 + 14), fill=frame, r=6)
    c.vgrad(box, sky0, sky1)
    if bars:
        c.line([((x0 + x1) / 2, y0), ((x0 + x1) / 2, y1)], frame, 12)
        c.line([(x0, (y0 + y1) / 2), (x1, (y0 + y1) / 2)], frame, 12)


def plant_small(c, cx, by, s=1.0, pot=(214, 110, 70), leaf=(64, 140, 90)):
    S.plant(c, cx, by, s, pot, leaf)


# ================================================================== 1. ES · paga extra: календарь на кухне
def cal_month(c, box, title, first_wd, ndays, head_col, ink=(40, 40, 50), mark=None, week=("L", "M", "X", "J", "V", "S", "D"), paper=WH):
    """Лист настенного календаря: шапка, дни недели, сетка чисел. first_wd — 0=пн."""
    x0, y0, x1, y1 = box
    c.shadow(box, r=10, alpha=80, blur=14, off=(0, 10))
    c.rect(box, fill=paper, r=10)
    c.rect((x0, y0, x1, y0 + 120), fill=head_col, r=10)
    c.rect((x0, y0 + 90, x1, y0 + 120), fill=head_col)
    for k in range(6):
        xx = x0 + 40 + k * (x1 - x0 - 80) / 5
        c.circle(xx, y0 + 16, 9, fill=mix(head_col, (0, 0, 0), 0.4))
        c.rect((xx - 4, y0 - 12, xx + 4, y0 + 16), fill=(150, 150, 160), r=3)
    c.text(((x0 + x1) / 2, y0 + 66), title, "db", c.fit(title, "db", x1 - x0 - 60, 1, 50), WH, anchor="mm")
    cw = (x1 - x0 - 40) / 7
    gy = y0 + 150
    for i, wd in enumerate(week):
        c.text((x0 + 20 + cw * (i + 0.5), gy), wd, "sb", 26, mix(ink, WH, 0.35) if i < 5 else head_col, anchor="mm")
    rh = (y1 - gy - 40) / 6
    for d in range(1, ndays + 1):
        pos = first_wd + d - 1
        col_i, row_i = pos % 7, pos // 7
        cx = x0 + 20 + cw * (col_i + 0.5)
        cy = gy + 44 + row_i * rh
        c.text((cx, cy), str(d), "sb", 30, head_col if col_i >= 5 else ink, anchor="mm")
    return gy, cw, rh


def scene_calendar(c, top=330):
    """Кухня: плитка, полка, настенный календарь «NOVIEMBRE 2026» со стикером «¿paga extra?»."""
    c.vgrad((0, 0, W, 880), (252, 240, 222), (244, 226, 200))
    # плитка-фартук
    for r_ in range(5):
        for q in range(12):
            x = q * 90 + (45 if r_ % 2 else 0) - 45
            y = 650 + r_ * 46
            c.rect((x + 3, y + 3, x + 87, y + 43), fill=(236, 244, 240), r=6)
    # столешница
    c.rect((0, 880, W, 906), fill=(150, 110, 76))
    S.wood(c, (0, 906, W, W), (196, 150, 104), (170, 124, 84), lines=5, seed=7)
    # полка с банками слева
    c.rect((60, top + 150, 420, top + 166), fill=(150, 110, 76), r=4)
    for k, (x, h, col) in enumerate(((100, 110, (220, 120, 70)), (180, 80, (240, 200, 90)), (250, 130, (120, 170, 130)), (330, 96, (200, 90, 80)))):
        y = top + 150
        c.rect((x - 30, y - h, x + 30, y), fill=col, r=12)
        c.rect((x - 32, y - h - 16, x + 32, y - h + 4), fill=mix(col, (0, 0, 0), 0.25), r=6)
        c.rect((x - 20, y - h + 30, x + 20, y - h + 60), fill=WH, alpha=200, r=4)
    # чайник и чашка на столешнице
    c.ellipse((110, 790, 320, 890), fill=(210, 70, 60))
    c.rect((120, 770, 310, 840), fill=(210, 70, 60), r=40)
    c.rect((185, 740, 245, 770), fill=(60, 60, 70), r=10)
    c.line([(310, 810), (380, 770)], (210, 70, 60), 22)
    c.arc((70, 780, 160, 860), 90, 270, (60, 60, 70), 14)
    S.teacup(c, 440, 858, 0.7, rim=(40, 110, 150))
    # календарь справа
    box = (540, top + 10, 1010, 860)
    cx = (box[0] + box[2]) / 2
    c.circle(cx, top - 10, 10, fill=(90, 90, 100))
    c.line([(cx - 90, top + 10), (cx, top - 10), (cx + 90, top + 10)], (90, 90, 100), 4)
    cal_month(c, box, "NOVIEMBRE 2026", 6, 30, (190, 50, 50))
    # обвести название месяца «от руки»
    c.arc((box[0] + 20, box[1] + 18, box[2] - 20, box[1] + 116), 190, 530, (255, 214, 70), 7)
    note(c, 930, 790, 210, 160, -8, (255, 226, 90), ["¿paga", "extra?"], size=40)


# ================================================================== 2. ES · свет: кухня вечером, лампа и счёт
def scene_power(c, top=300):
    NIGHT = (22, 34, 66)
    c.vgrad((0, 0, W, W), (38, 52, 92), (20, 28, 56))
    # окно с луной
    window(c, (70, top + 40, 380, top + 330), sky0=(20, 30, 70), sky1=(50, 64, 120), frame=(70, 84, 124))
    c.circle(300, top + 110, 34, fill=(250, 240, 200))
    c.circle(314, top + 100, 30, fill=(30, 42, 88))
    for (x, y) in ((120, top + 90), (170, top + 220), (330, top + 250), (230, top + 70)):
        c.circle(x, y, 3, fill=WH, alpha=200)
    # подвесная лампа со светом
    c.line([(760, top - 10), (760, top + 60)], (180, 180, 190), 5)
    c.glow((520, top + 60, 1000, top + 640), (255, 214, 120), alpha=90, blur=70)
    c.poly([(690, top + 130), (830, top + 130), (800, top + 60), (720, top + 60)], (240, 190, 70))
    c.ellipse((730, top + 118, 790, top + 158), fill=(255, 246, 210))
    # розетка с вилкой
    c.rect((450, top + 300, 530, top + 380), fill=(236, 236, 240), r=12)
    c.circle(475, top + 340, 7, fill=(80, 80, 90))
    c.circle(505, top + 340, 7, fill=(80, 80, 90))
    # стол
    c.rect((0, top + 520, W, top + 548), fill=(150, 106, 70))
    S.wood(c, (0, top + 548, W, W), (120, 84, 56), (96, 66, 44), lines=5, seed=5)
    # счёт на столе
    S.paper(c, (560, top + 330, 900, top + 610), -6, head="FACTURA DE LUZ", lines=6, head_size=28, head_col=(30, 40, 70))
    c.rect((640, top + 548, 860, top + 596), fill=(255, 236, 150), r=8, alpha=230)
    c.text((750, top + 572), "TOTAL:  ? €", "db", 30, (180, 40, 40), anchor="mm")
    # лампочка и калькулятор
    I.calc(c, 400, top + 470, 150, (60, 70, 96), screen=(200, 236, 210))
    S.glasses(c, 170, top + 505, 0.8, col=(30, 30, 34))


# ================================================================== 3. ES · вид: оптика
def scene_optica(c, top=330):
    c.vgrad((0, 0, W, W), (240, 246, 250), (222, 234, 242))
    # стеллаж с оправами
    sx0, sx1 = 420, 1040
    c.rect((sx0, top, sx1, top + 460), fill=(250, 250, 252), r=14)
    c.rect((sx0, top, sx1, top + 460), outline=(200, 210, 220), width=3, r=14)
    frames = [(40, 40, 40), (170, 60, 50), (40, 90, 160), (150, 110, 60), (120, 120, 130), (30, 120, 110), (200, 140, 40), (90, 60, 120), (50, 50, 60)]
    k = 0
    for r_ in range(3):
        y = top + 110 + r_ * 150
        c.rect((sx0 + 20, y + 44, sx1 - 20, y + 54), fill=(200, 206, 214), r=3)
        for q in range(3):
            x = sx0 + 110 + q * 200
            I.ICONS["specs"](c, x, y + 10, 160, frames[k % len(frames)], lens=(232, 242, 250))
            k += 1
    # таблица для проверки зрения слева
    c.shadow((70, top + 10, 360, top + 420), r=8, alpha=60, blur=10, off=(0, 6))
    c.rect((70, top + 10, 360, top + 420), fill=WH, r=8)
    rows = [("E", 96), ("F P", 64), ("T O Z", 46), ("L P E D", 34), ("P E C F D", 26)]
    y = top + 70
    for t, sz in rows:
        c.text((215, y), t, "db", sz, (30, 30, 36), anchor="mm")
        y += sz + 20
    # стойка-прилавок
    c.rect((0, top + 520, W, top + 560), fill=(60, 110, 150))
    c.rect((0, top + 560, W, W), fill=(44, 84, 120))
    c.rect((0, top + 556, W, top + 566), fill=(30, 60, 90))
    # подставка с прогрессивными очками на прилавке
    c.rect((205, top + 470, 225, top + 520), fill=(150, 156, 166))
    c.rect((165, top + 510, 265, top + 522), fill=(150, 156, 166), r=4)
    I.ICONS["specs_prog"](c, 215, top + 468, 170, (30, 40, 60))
    # футляр и салфетка
    c.rect((760, top + 470, 940, top + 520), fill=(190, 60, 50), r=24)
    c.line([(770, top + 494), (930, top + 494)], mix((190, 60, 50), (0, 0, 0), 0.25), 4)
    c.poly([(480, top + 520), (640, top + 520), (660, top + 500), (500, top + 500)], (250, 214, 90))


# ================================================================== 4. IT · стоматология: кабинет
def scene_dental(c, h=620):
    c.vgrad((0, 0, W, h), (232, 244, 246), (214, 232, 236))
    # окно с жалюзи
    window(c, (620, 90, 980, 400), sky0=(170, 214, 236), sky1=(220, 238, 248), bars=False)
    for k in range(9):
        c.rect((620, 96 + k * 34, 980, 116 + k * 34), fill=(245, 246, 248), alpha=210)
    # шкафчик
    c.rect((60, 250, 330, h - 40), fill=(250, 250, 250), r=10)
    c.rect((60, 250, 330, h - 40), outline=(200, 214, 220), width=3, r=10)
    for k in range(3):
        y = 280 + k * 90
        c.rect((80, y, 310, y + 70), outline=(200, 214, 220), width=3, r=6)
        c.rect((170, y + 30, 220, y + 40), fill=(170, 186, 196), r=4)
    I.ICONS["toothbrush"](c, 150, 214, 90, (40, 150, 170))
    c.rect((220, 186, 280, 250), fill=(200, 236, 244), r=8)
    # кресло
    BL = (0, 136, 156)
    c.rect((360, h - 60, 900, h - 30), fill=(160, 170, 180), r=10)
    c.rect((600, 470, 640, h - 50), fill=(160, 170, 180))
    c.poly(rotpts([(440, 430), (840, 430), (840, 490), (440, 490)], 640, 460, -8), BL)
    c.poly(rotpts([(400, 330), (470, 330), (470, 470), (400, 470)], 435, 400, -32), BL)
    c.ellipse((330, 300, 420, 360), fill=mix(BL, WH, 0.2))
    c.poly(rotpts([(820, 450), (930, 470), (930, 510), (820, 500)], 870, 480, 18), BL)
    c.rect((520, 400, 560, 440), fill=mix(BL, (0, 0, 0), 0.2), r=8)
    # лампа на кронштейне
    c.line([(900, 0), (900, 120), (720, 190)], (170, 180, 190), 14)
    c.ellipse((640, 170, 790, 250), fill=(240, 244, 246), outline=(170, 180, 190), width=8)
    c.glow((600, 200, 820, 380), (255, 250, 210), alpha=80, blur=40)
    # столик с инструментами (без острых деталей)
    c.rect((880, 360, 1040, 376), fill=(170, 180, 190), r=4)
    c.rect((952, 376, 966, 520), fill=(170, 180, 190))
    for k in range(3):
        c.rect((900 + k * 40, 340, 930 + k * 40, 358), fill=(214, 220, 228), r=6)
    c.rect((0, h - 30, W, h), fill=(196, 214, 220))


# ================================================================== 5. PL · осенний парк, двое на скамейке со спины
def scene_park(c):
    c.vgrad((0, 0, W, 720), (250, 226, 190), (246, 206, 160))
    c.circle(860, 170, 80, fill=(255, 236, 190), alpha=200)
    # холмы
    c.ellipse((-300, 600, 700, 1000), fill=(196, 170, 110))
    c.ellipse((400, 620, 1400, 1020), fill=(180, 156, 100))
    c.rect((0, 760, W, W), fill=(170, 146, 94))
    # деревья
    tree(c, 170, 780, 1.1, seed=3)
    tree(c, 960, 770, 1.25, seed=5, leaves=((214, 110, 40), (236, 160, 50), (190, 70, 36)))
    tree(c, 600, 700, 0.7, seed=8, leaves=((236, 180, 70), (220, 140, 50)))
    # дорожка
    c.poly([(420, W), (700, W), (620, 760), (560, 760)], (226, 206, 170))
    # листья на земле
    rnd = random.Random(4)
    for k in range(40):
        x, y = rnd.uniform(0, W), rnd.uniform(790, 1070)
        c.ellipse((x - 10, y - 5, x + 10, y + 5), fill=((214, 110, 40), (236, 170, 60), (190, 80, 40))[k % 3])
    # скамейка
    bx0, bx1, seat = 440, 1000, 900
    senior_back(c, 620, seat - 30, 1.0, (60, 90, 130), hair=(170, 172, 180))
    senior_back(c, 810, seat - 30, 0.94, (170, 60, 70), hair=(236, 236, 240), bun=True)
    c.rect((bx0 - 10, seat - 12, bx1 + 10, seat + 16), fill=(110, 72, 44), r=6)
    for k in range(3):
        c.rect((bx0, seat - 150 + k * 40, bx1, seat - 122 + k * 40), fill=(126, 84, 52), r=6)
    for x in (bx0 + 20, bx1 - 40):
        c.rect((x, seat - 160, x + 20, seat), fill=(100, 66, 40), r=4)
    for x in (bx0 + 30, bx1 - 50):
        c.rect((x, seat + 16, x + 20, seat + 110), fill=(60, 60, 64))
    # падающие листья
    for (x, y, a) in ((360, 260, 30), (520, 420, -20), (300, 520, 60), (720, 330, 10)):
        c.poly(rotpts([(x - 14, y), (x, y - 8), (x + 14, y), (x, y + 8)], x, y, a), (226, 120, 40))


# ================================================================== 6. FR · две кружки и карточка «15»
def mug(c, cx, by, s, col, handle="right", inner=(90, 60, 40)):
    w, h = 150 * s, 170 * s
    c.ellipse((cx - w * 0.62, by - 16 * s, cx + w * 0.62, by + 16 * s), fill=(0, 0, 0), alpha=40)
    if handle == "right":
        c.arc((cx + w * 0.3, by - h * 0.78, cx + w * 0.86, by - h * 0.22), 270, 450, col, 22 * s)
    else:
        c.arc((cx - w * 0.86, by - h * 0.78, cx - w * 0.3, by - h * 0.22), 90, 270, col, 22 * s)
    c.rect((cx - w / 2, by - h, cx + w / 2, by), fill=col, r=26 * s)
    c.ellipse((cx - w / 2, by - h - 18 * s, cx + w / 2, by - h + 18 * s), fill=mix(col, (0, 0, 0), 0.15))
    c.ellipse((cx - w / 2 + 12 * s, by - h - 10 * s, cx + w / 2 - 12 * s, by - h + 12 * s), fill=inner)
    c.rect((cx - w / 2 + 14 * s, by - h + 30 * s, cx - w / 2 + 30 * s, by - 30 * s), fill=WH, alpha=70, r=8)
    for k in (-1, 1):
        pts = [(cx + k * 18 * s + math.sin(t / 4) * 8 * s, by - h - 30 * s - t * 4 * s) for t in range(0, 20)]
        c.line(pts, WH, 5 * s, alpha=150)


def scene_mugs(c, table_y=700):
    c.vgrad((0, 0, W, table_y), (248, 232, 222), (240, 214, 200))
    window(c, (660, 470, 940, 668), sky0=(190, 220, 236), sky1=(236, 244, 248), frame=(255, 250, 244))
    S.plant(c, 180, table_y - 4, 0.9, pot=(90, 140, 160), leaf=(70, 140, 100))
    c.rect((0, table_y, W, W), fill=(214, 170, 130))
    S.wood(c, (0, table_y, W, W), (220, 178, 138), (196, 150, 108), lines=7, seed=9)
    c.rect((0, table_y, W, table_y + 10), fill=(180, 136, 96))
    mug(c, 330, 930, 1.35, (226, 96, 80), handle="left")
    mug(c, 780, 930, 1.35, (60, 120, 160), handle="right")
    # карточка «15»
    card = (470, 760, 640, 950)
    c.shadow(card, r=14, alpha=80, blur=8, off=(0, 6))
    c.rect(card, fill=WH, r=14)
    c.text((555, 836), "15", "db", 96, (40, 44, 60), anchor="mm")
    c.text((555, 910), "questions", "sb", 24, (120, 120, 130), anchor="mm")


# ================================================================== 7. ES · кресло психолога, блокнот «10 preguntas», шапочка
def scene_armchair(c, floor_y=860):
    c.vgrad((0, 0, W, floor_y), (236, 232, 244), (222, 216, 236))
    # книжный стеллаж
    c.rect((60, 330, 420, floor_y), fill=(160, 120, 84), r=6)
    for k in range(3):
        y = 440 + k * 140
        c.rect((74, y - 4, 406, y + 8), fill=(120, 86, 56))
        shelf_books(c, 84, y - 4, 400, seed=k + 3)
    # торшер
    c.line([(930, floor_y - 10), (930, 420)], (60, 60, 70), 10)
    c.poly([(870, 420), (990, 420), (960, 330), (900, 330)], (240, 200, 110))
    c.glow((820, 380, 1040, 620), (255, 230, 160), alpha=70, blur=50)
    c.ellipse((880, floor_y - 20, 980, floor_y), fill=(60, 60, 70))
    # пол и ковёр
    c.rect((0, floor_y, W, W), fill=(176, 140, 104))
    c.ellipse((360, floor_y + 20, 940, floor_y + 150), fill=(200, 110, 90))
    c.ellipse((390, floor_y + 34, 910, floor_y + 136), outline=(236, 200, 160), width=6)
    # кресло
    AC = (70, 90, 150)
    c.rect((470, 470, 820, 760), fill=AC, r=70)
    c.rect((430, 610, 530, 860), fill=mix(AC, (0, 0, 0), 0.18), r=40)
    c.rect((760, 610, 860, 860), fill=mix(AC, (0, 0, 0), 0.18), r=40)
    c.rect((500, 700, 790, 830), fill=mix(AC, WH, 0.18), r=30)
    for x in (470, 800):
        c.rect((x, 860, x + 20, 900), fill=(90, 64, 44))
    # шапочка на спинке
    I.ICONS["cap"](c, 645, 452, 190, (30, 30, 40))
    # блокнот на подлокотнике
    nb = (360, 560, 580, 680)
    c.shadow(nb, r=6, alpha=70, blur=8, off=(0, 8))
    c.poly(rotpts([(nb[0], nb[1]), (nb[2], nb[1]), (nb[2], nb[3]), (nb[0], nb[3])], 470, 620, -4), (250, 246, 236))
    c.text((470, 604), "10", "db", 50, (190, 60, 50), anchor="mm")
    c.text((470, 652), "preguntas", "sbi", 28, (40, 40, 50), anchor="mm")
    S.pen(c, 590, 690, 640, 600, col=(40, 40, 50), w=10)
    S.plant(c, 1000, floor_y + 4, 0.7, pot=(230, 230, 236), leaf=(60, 130, 90))


# ================================================================== 8. PT · дом для пожилых: фасад и сад
def scene_lar(c, top=380):
    c.vgrad((0, 0, W, W), (206, 232, 246), (238, 246, 250))
    c.circle(150, top - 60, 60, fill=(255, 230, 150))
    # здание
    bx0, bx1, by0, by1 = 180, 900, top + 40, top + 470
    c.rect((bx0, by0, bx1, by1), fill=(250, 244, 230))
    c.poly([(bx0 - 30, by0 + 4), ((bx0 + bx1) / 2, by0 - 110), (bx1 + 30, by0 + 4)], (196, 90, 60))
    c.rect((bx0 - 30, by0 - 4, bx1 + 30, by0 + 12), fill=(170, 74, 50))
    for r_ in range(2):
        for q in range(6):
            x = bx0 + 50 + q * 115
            y = by0 + 60 + r_ * 170
            if r_ == 1 and q in (2, 3):
                continue
            c.rect((x, y, x + 70, y + 100), fill=(150, 196, 226), r=6)
            c.rect((x - 6, y + 100, x + 76, y + 110), fill=(220, 214, 200))
            c.line([(x + 35, y), (x + 35, y + 100)], WH, 5)
            c.rect((x, y, x + 70, y + 100), outline=(120, 90, 70), width=4, r=6)
    # вход с навесом
    dx = (bx0 + bx1) / 2
    c.rect((dx - 70, by1 - 170, dx + 70, by1), fill=(120, 80, 56), r=8)
    c.rect((dx - 60, by1 - 160, dx - 4, by1), fill=(150, 196, 226))
    c.rect((dx + 4, by1 - 160, dx + 60, by1), fill=(150, 196, 226))
    c.poly([(dx - 120, by1 - 170), (dx + 120, by1 - 170), (dx + 100, by1 - 214), (dx - 100, by1 - 214)], (0, 120, 110))
    # сад
    c.rect((0, by1, W, W), fill=(120, 176, 100))
    c.poly([(dx - 70, by1), (dx + 70, by1), (dx + 200, W), (dx - 200, W)], (232, 220, 190))
    for x, s_ in ((80, 0.9), (990, 1.0)):
        c.rect((x - 12, by1 - 160 * s_, x + 12, by1 + 20), fill=(120, 84, 56))
        c.circle(x, by1 - 200 * s_, 90 * s_, fill=(70, 140, 80))
        c.circle(x - 50 * s_, by1 - 150 * s_, 70 * s_, fill=(84, 156, 90))
        c.circle(x + 50 * s_, by1 - 150 * s_, 70 * s_, fill=(60, 128, 74))
    # кусты с цветами
    for x in (250, 380, 720, 850):
        c.ellipse((x - 70, by1 - 40, x + 70, by1 + 40), fill=(80, 150, 80))
        for k in range(4):
            c.circle(x - 40 + k * 26, by1 - 16 + (k % 2) * 16, 9, fill=((240, 120, 140), (250, 220, 90))[k % 2])
    # скамейка сбоку
    c.rect((80, by1 + 120, 300, by1 + 140), fill=(140, 96, 60), r=4)
    c.rect((80, by1 + 80, 300, by1 + 100), fill=(140, 96, 60), r=4)
    for x in (100, 270):
        c.rect((x, by1 + 140, x + 12, by1 + 190), fill=(70, 70, 76))


# ================================================================== 9. ES · стол с ноутбуком: урок онлайн
def scene_laptop_desk(c, top=520):
    BLUE = (26, 86, 180)
    c.vgrad((0, 0, W, W), (30, 100, 200), (18, 64, 150))
    c.dots((0, top - 80, W, W), 44, 3, WH, alpha=30)
    # стол
    c.rect((0, top + 330, W, W), fill=(236, 206, 160))
    c.rect((0, top + 322, W, top + 336), fill=(206, 170, 120))
    # ноутбук
    lx0, lx1 = 250, 830
    c.rect((lx0, top, lx1, top + 330), fill=(50, 56, 70), r=22)
    scr = (lx0 + 22, top + 22, lx1 - 22, top + 300)
    c.rect(scr, fill=WH, r=8)
    # экран: урок — плитка с видео и «слайд»
    c.rect((scr[0] + 16, scr[1] + 16, scr[0] + 330, scr[3] - 16), fill=(226, 238, 250), r=10)
    c.circle(scr[0] + 173, scr[1] + 118, 50, fill=BLUE)
    c.poly([(scr[0] + 160, scr[1] + 92), (scr[0] + 160, scr[1] + 144), (scr[0] + 200, scr[1] + 118)], WH)
    for k in range(3):
        c.rect((scr[0] + 40, scr[1] + 190 + k * 22, scr[0] + 300 - k * 50, scr[1] + 202 + k * 22), fill=(170, 190, 214), r=5)
    for k in range(3):
        y = scr[1] + 20 + k * 84
        c.rect((scr[0] + 350, y, scr[2] - 16, y + 70), fill=(240, 244, 248), r=10)
        c.circle(scr[0] + 386, y + 35, 20, fill=((240, 180, 60), (80, 170, 110), (220, 90, 80))[k])
        c.rect((scr[0] + 420, y + 22, scr[2] - 40, y + 32), fill=(190, 200, 214), r=5)
        c.rect((scr[0] + 420, y + 42, scr[2] - 90, y + 50), fill=(214, 222, 232), r=4)
    c.poly([(lx0 - 60, top + 330), (lx1 + 60, top + 330), (lx1 + 30, top + 360), (lx0 - 30, top + 360)], (80, 86, 100))
    # наушники, кружка, блокнот, очки
    c.arc((40, top + 150, 220, top + 330), 180, 360, (40, 40, 50), 16)
    c.rect((30, top + 240, 76, top + 320), fill=(230, 90, 70), r=16)
    c.rect((184, top + 240, 230, top + 320), fill=(230, 90, 70), r=16)
    S.teacup(c, 960, top + 290, 0.9, rim=BLUE)
    c.poly(rotpts([(860, top + 360), (1060, top + 360), (1060, top + 480), (860, top + 480)], 960, top + 420, 8), WH)
    S.glasses(c, 160, top + 420, 0.9, col=(30, 30, 34))
    c.rect((560, top + 400, 720, top + 470), fill=(240, 240, 244), r=30)
    c.line([(640, top + 400), (640, top + 430)], (200, 200, 210), 4)


# ================================================================== 10. ES · современная гостиная
def scene_salon(c, floor_y=820):
    SAGE = (140, 170, 140)
    c.rect((0, 0, W, floor_y), fill=(244, 238, 228))
    c.rect((0, 0, 380, floor_y), fill=(222, 200, 176))  # акцентная стена
    # стеллаж-полки на акцентной стене
    for k in range(3):
        y = 430 + k * 120
        c.rect((60, y, 320, y + 14), fill=(120, 86, 60), r=3)
    shelf_books(c, 70, 430, 200, seed=11)
    S.plant(c, 260, 430, 0.45, pot=(240, 240, 240), leaf=(80, 140, 90))
    c.rect((80, 490, 150, 550), fill=(200, 110, 80), r=35)
    c.rect((200, 500, 300, 550), fill=(250, 250, 250), r=8)
    shelf_books(c, 80, 670, 310, seed=12)
    # картины
    for (x0, y0, x1, y1, col) in ((470, 360, 620, 540, (214, 120, 80)), (650, 390, 770, 510, (90, 130, 150))):
        c.rect((x0, y0, x1, y1), fill=(250, 250, 250), outline=(60, 50, 40), width=6)
        c.circle((x0 + x1) / 2, (y0 + y1) / 2, (x1 - x0) * 0.28, fill=col)
        c.rect((x0 + 20, (y0 + y1) / 2 + 10, x1 - 20, y1 - 20), fill=mix(col, WH, 0.4))
    # торшер-дуга
    c.arc((790, 380, 1070, 900), 180, 290, (50, 50, 56), 10)
    c.line([(1016, 408), (1010, 812)], (50, 50, 56), 10)
    c.ellipse((760, 470, 850, 530), fill=(240, 200, 110))
    c.glow((720, 490, 920, 680), (255, 230, 170), alpha=60, blur=40)
    c.ellipse((960, floor_y - 18, 1060, floor_y + 6), fill=(50, 50, 56))
    # пол, ковёр
    c.rect((0, floor_y, W, W), fill=(206, 176, 140))
    for k in range(6):
        c.line([(0, floor_y + 20 + k * 44), (W, floor_y + 20 + k * 44)], (190, 160, 124), 3)
    c.ellipse((280, floor_y + 40, 1000, floor_y + 220), fill=(236, 228, 214))
    # диван
    c.rect((360, 600, 960, 760), fill=SAGE, r=40)
    c.rect((320, 680, 420, 820), fill=mix(SAGE, (0, 0, 0), 0.12), r=36)
    c.rect((900, 680, 1000, 820), fill=mix(SAGE, (0, 0, 0), 0.12), r=36)
    c.rect((400, 720, 920, 812), fill=mix(SAGE, WH, 0.15), r=24)
    c.line([(660, 724), (660, 808)], mix(SAGE, (0, 0, 0), 0.2), 3)
    c.rect((430, 630, 540, 720), fill=(230, 180, 90), r=20)
    c.rect((800, 640, 890, 720), fill=(214, 120, 90), r=20)
    for x in (350, 960):
        c.rect((x, 820, x + 14, 850), fill=(90, 64, 44))
    # журнальный столик
    c.ellipse((520, 860, 800, 920), fill=(150, 108, 72))
    c.rect((650, 900, 670, 960), fill=(120, 86, 58))
    c.ellipse((600, 950, 720, 972), fill=(120, 86, 58))
    c.rect((600, 846, 660, 866), fill=(60, 110, 150), r=4)
    S.teacup(c, 730, 850, 0.4, steam=False)


# ================================================================== герои для сеток
def hero_months(c, box):
    """Две отрывные страницы календаря JUNIO / NOVIEMBRE с лентой «+ paga extra» (ES: 14 pagas, доп. в июне и ноябре)."""
    x0, y0, x1, y1 = box
    c.shadow(box, r=28, alpha=50, blur=12, off=(0, 6))
    c.rect(box, fill=(252, 238, 214), r=28)
    c.dots((x0 + 20, y0 + 20, x1 - 20, y1 - 20), 40, 3, (190, 50, 50), alpha=30)
    cx = (x0 + x1) / 2
    h = y1 - y0
    for k, (m, col) in enumerate((("JUNIO", (230, 150, 40)), ("NOVIEMBRE", (190, 50, 50)))):
        px = cx - 230 + k * 460
        pb = (px - 170, y0 + 34, px + 170, y1 - 30)
        c.shadow(pb, r=14, alpha=70, blur=10, off=(0, 8))
        c.rect(pb, fill=WH, r=14)
        c.rect((pb[0], pb[1], pb[2], pb[1] + 70), fill=col, r=14)
        c.rect((pb[0], pb[1] + 40, pb[2], pb[1] + 70), fill=col)
        c.text((px, pb[1] + 36), m, "db", 36, WH, anchor="mm")
        c.text((px, pb[1] + 70 + (pb[3] - pb[1] - 70) * 0.42), "+1", "db", 96, col, anchor="mm")
        c.text((px, pb[3] - 38), "paga extra", "sb", 32, (60, 60, 70), anchor="mm")


def hero_power(c, box):
    """Лампочка и счётчик на ночном синем."""
    x0, y0, x1, y1 = box
    c.shadow(box, r=28, alpha=60, blur=12, off=(0, 6))
    c.rect(box, fill=(26, 40, 84), r=28)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    c.glow((cx - 200, cy - 110, cx + 200, cy + 110), (255, 214, 110), alpha=110, blur=36)
    I.ICONS["bulb"](c, cx, cy + 6, (y1 - y0) * 0.9, (70, 80, 110))
    I.ICONS["meter"](c, x0 + 150, cy + 10, 150, (236, 240, 248), bg=(26, 40, 84))
    I.ICONS["plug"](c, x1 - 150, cy + 10, 150, (236, 240, 248))
    c.text((x0 + 150, y1 - 30), "kWh", "sb", 26, (200, 210, 230), anchor="mm")
    c.text((x1 - 150, y1 - 30), "kW", "sb", 26, (200, 210, 230), anchor="mm")


def hero_tooth(c, box):
    x0, y0, x1, y1 = box
    c.shadow(box, r=28, alpha=50, blur=12, off=(0, 6))
    c.rect(box, fill=(214, 238, 242), r=28)
    c.dots((x0 + 20, y0 + 20, x1 - 20, y1 - 20), 40, 3, (0, 136, 156), alpha=40)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    I.ICONS["tooth"](c, cx - 60, cy + 10, (y1 - y0) * 0.78, (0, 110, 130), spark=(255, 200, 60))
    # облачко «ASL?»
    bx = (cx + 90, y0 + 40, cx + 330, y0 + 150)
    c.rect(bx, fill=WH, r=40)
    c.poly([(bx[0] + 30, bx[3] - 6), (bx[0] + 80, bx[3] - 6), (bx[0] + 10, bx[3] + 40)], WH)
    c.text(((bx[0] + bx[2]) / 2, (bx[1] + bx[3]) / 2), "ASL?", "db", 52, (0, 110, 130), anchor="mm")
    I.ICONS["toothbrush"](c, x0 + 140, cy + 20, 150, (0, 136, 156))
    I.ICONS["euro_q"](c, x1 - 130, y1 - 90, 110, (200, 70, 80))


def hero_autumn(c, box):
    """PL: осенняя панель с бейджами «75+» и «80+» (темы запросов)."""
    x0, y0, x1, y1 = box
    c.shadow(box, r=28, alpha=50, blur=12, off=(0, 6))
    c.rect(box, fill=(246, 224, 190), r=28)
    rnd = random.Random(9)
    for k in range(26):
        x, y = rnd.uniform(x0 + 20, x1 - 20), rnd.uniform(y0 + 20, y1 - 20)
        a = rnd.uniform(0, 180)
        c.poly(rotpts([(x - 16, y), (x, y - 9), (x + 16, y), (x, y + 9)], x, y, a), ((214, 110, 40), (236, 170, 60), (190, 80, 40))[k % 3], alpha=170)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    for k, (t, col) in enumerate((("75+", (150, 50, 40)), ("80+", (40, 70, 110)))):
        x = cx - 170 + k * 340
        c.shadow((x - 120, cy - 100, x + 120, cy + 100), r=100, alpha=60, blur=10, off=(0, 8))
        c.circle(x, cy, 110, fill=col)
        c.circle(x, cy, 94, outline=WH, width=4)
        c.text((x, cy + 4), t, "db", 84, WH, anchor="mm")


def hero_study(c, box):
    """ES: полка с книгами, шапочка, ноутбук — учёба на психолога."""
    x0, y0, x1, y1 = box
    c.shadow(box, r=28, alpha=50, blur=12, off=(0, 6))
    c.rect(box, fill=(230, 224, 246), r=28)
    c.rect((x0 + 40, y1 - 90, x1 - 40, y1 - 74), fill=(120, 86, 56), r=4)
    shelf_books(c, x0 + 60, y1 - 90, x0 + 420, seed=21)
    I.laptop(c, x1 - 260, y1 - 150, 200, (60, 70, 120))
    I.ICONS["cap"](c, (x0 + x1) / 2 + 40, y0 + 120, 190, (30, 30, 40))
    I.ICONS["talk"](c, x1 - 110, y0 + 90, 110, (110, 80, 170))


def hero_lar(c, box):
    """PT: маленький фасад дома для пожилых на зелёной панели (кадр из сцены d)."""
    from p60_lib import C as _C
    S.clip_draw(c, box, 28, lambda t: _lar_small(t, box))


def _lar_small(c, box):
    x0, y0, x1, y1 = box
    c.vgrad(box, (206, 232, 246), (238, 246, 250))
    cx = (x0 + x1) / 2
    bx0, bx1, by0, by1 = cx - 300, cx + 300, y0 + 110, y1 - 30
    c.rect((x0, by1 - 10, x1, y1), fill=(120, 176, 100))
    c.rect((bx0, by0, bx1, by1), fill=(250, 244, 230))
    c.poly([(bx0 - 24, by0 + 4), (cx, by0 - 80), (bx1 + 24, by0 + 4)], (196, 90, 60))
    for q in range(6):
        x = bx0 + 34 + q * 96
        c.rect((x, by0 + 26, x + 52, by0 + 86), fill=(150, 196, 226), r=5)
        c.rect((x, by0 + 26, x + 52, by0 + 86), outline=(120, 90, 70), width=3, r=5)
    c.rect((cx - 40, by1 - 66, cx + 40, by1), fill=(120, 80, 56), r=6)
    c.poly([(cx - 76, by1 - 66), (cx + 76, by1 - 66), (cx + 62, by1 - 92), (cx - 62, by1 - 92)], (0, 120, 110))
    for x in (x0 + 90, x1 - 90):
        c.circle(x, by1 - 100, 70, fill=(70, 140, 80))
        c.rect((x - 8, by1 - 40, x + 8, by1), fill=(120, 84, 56))
