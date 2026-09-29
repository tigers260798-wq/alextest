"""Волна 7 (29.09, креативщик w7-intl): 2 карточки «Готово к заливу» (US, en) × 4 статики 1:1, Pillow.
    python3 w7_intl.py            — оба пакета
    python3 w7_intl.py 1 2        — пакеты 1 и 2
    python3 w7_intl.py 1:a,c      — пакет 1, буквы a и c
Пишет /home/user/alextest/creatives/ready/2026-09-30_packs/<docId>/<a|b|c|d>.png и creatives.json рядом.
Движок — w6_products (раскладки grid2x2_art, quiz_art, poll3, vs2, callouts_scene, top_scene; импорт, файл не меняется)
+ своя раскладка vs3 (сравнение трёх) и свои рисунки: браслеты (цепь, манжета, теннисный, с камнями, бусины, шарм),
рука со стеком, сечение металла под лупой; окна с сотовыми шторами без шнура, комнаты, стена под камень.
Весь текст на картинках — только из статей article_drafts/<docId> (раздел — в поле src).
Браслеты: без брендов ювелирных домов и их узнаваемых дизайнов (винты, клевер, гвоздь, фирменный голубой, витой кабель,
бусины-шармы известной марки), без цен, скидок, «sale / free / limited / real / certified diamonds / investment».
Шторы: без брендов и магазинов, без «near me» и локации, без цифр экономии, цен, «free installation / sale / 100% child-safe /
guaranteed», без людей (ребёнок рядом со шнуром исключён). Общее: без «click here», без до/после."""
import json
import math
import os
import random
import sys

from PIL import ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import w6_products as W6  # noqa: E402  (тянет w4_ukde → w3_packs, p60_lib, шрифты Montserrat)
import p60_lib  # noqa: E402
from p60_lib import C, W, mix, rotpts  # noqa: E402
import p60_scenes as S  # noqa: E402

OUT7 = W6.OUT6
p60_lib.OUT = OUT7
WH = (255, 255, 255)
BLK = (0, 0, 0)
CONCEPT = W6.CONCEPT
PACKS = {}
head, cta_btn, bgfill = W6.head, W6.cta_btn, W6.bg


# =====================================================================  общие помощники
def epts(cx, cy, rx, ry, a0=0.0, a1=360.0, n=90):
    return [(cx + rx * math.cos(math.radians(a0 + (a1 - a0) * k / n)),
             cy + ry * math.sin(math.radians(a0 + (a1 - a0) * k / n))) for k in range(n + 1)]


def rell(c, cx, cy, a, b, ang, fill, alpha=255, n=40):
    """Эллипс с полуосями a (вдоль ang) и b, повёрнутый на ang градусов."""
    pts = rotpts(epts(cx, cy, a, b, 0, 360, n)[:-1], cx, cy, ang)
    c.poly(pts, fill, alpha=alpha)


def ring_shadow(c, cx, cy, rx, ry, w, alpha=60, blur=8, dy=8):
    lay = c.layer()
    ImageDraw.Draw(lay).ellipse(c.sb((cx - rx, cy - ry + dy, cx + rx, cy + ry + dy)), outline=(0, 0, 0, alpha),
                                width=max(1, c.s(w)))
    c.put(lay, blur=blur)


def soft_shadow_ellipse(c, box, alpha=50, blur=14):
    lay = c.layer()
    ImageDraw.Draw(lay).ellipse(c.sb(box), fill=(0, 0, 0, alpha))
    c.put(lay, blur=blur)


def capsule(c, p0, p1, w, fill, alpha=255):
    L = math.hypot(p1[0] - p0[0], p1[1] - p0[1])
    ang = math.degrees(math.atan2(p1[1] - p0[1], p1[0] - p0[0]))
    pts = rotpts(W6.rrect_pts(p0[0], p0[1] - w / 2, p0[0] + L, p0[1] + w / 2, w / 2, 6), p0[0], p0[1], ang)
    c.poly(pts, fill, alpha=alpha)


def sparkle(c, x, y, r, col=WH, alpha=255):
    c.poly([(x, y - r), (x + r * 0.22, y - r * 0.22), (x + r, y), (x + r * 0.22, y + r * 0.22), (x, y + r),
            (x - r * 0.22, y + r * 0.22), (x - r, y), (x - r * 0.22, y - r * 0.22)], col, alpha=alpha)


def interp(pts, x):
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        if x0 <= x <= x1:
            return y0 + (y1 - y0) * (x - x0) / (x1 - x0)
    return pts[0][1] if x < pts[0][0] else pts[-1][1]


def panel_bg(c, box, col, r=18):
    c.rect(box, fill=col, r=r)


# =====================================================================  1. US · товарка · украшения · браслеты
GOLD = (214, 168, 76)
GOLD_L = (248, 222, 150)
GOLD_M = (230, 192, 108)
GOLD_D = (158, 114, 46)
GOLD_DD = (120, 84, 32)
PLUM = (58, 36, 44)
BERRY = (176, 70, 92)
STONE = (246, 248, 252)
STONE_D = (196, 202, 214)
WHITE_METAL = (206, 210, 218)


def chain_loop(c, cx, cy, rx, ry, L=46, hole=(250, 242, 236), n=None):
    """Крупная цепь (панцирные «пухлые» звенья), лежит кольцом — вид сверху под углом."""
    per = math.pi * (3 * (rx + ry) - math.sqrt((3 * rx + ry) * (rx + 3 * ry)))
    n = n or int(per / (L * 0.8))
    n += n % 2
    ring_shadow(c, cx, cy, rx, ry, L * 0.55, alpha=55, blur=10, dy=12)
    links = []
    for k in range(n):
        th = 2 * math.pi * k / n
        x, y = cx + rx * math.cos(th), cy + ry * math.sin(th)
        tang = math.degrees(math.atan2(ry * math.cos(th), -rx * math.sin(th)))
        links.append((k, x, y, tang))
    for parity in (0, 1):
        for k, x, y, tang in links:
            if k % 2 != parity:
                continue
            a = L * 0.64
            b = L * 0.42 if parity == 0 else L * 0.3
            t = math.radians(tang)
            rell(c, x + 1.5, y + 3, a, b, tang, GOLD_DD)
            rell(c, x, y, a, b, tang, GOLD if parity == 0 else GOLD_M)
            # блик по верхней кромке звена
            u, v = -a * 0.08, -b * 0.5
            hx, hy = x + u * math.cos(t) - v * math.sin(t), y + u * math.sin(t) + v * math.cos(t)
            rell(c, hx, hy, a * 0.5, b * 0.16, tang, GOLD_L, alpha=220)
            # отверстие звена
            rell(c, x, y + 1, a * 0.5, b * 0.34, tang, GOLD_DD)
            rell(c, x, y + 2, a * 0.46, b * 0.26, tang, hole)


def band_ring(c, cx, cy, rx, ry, h, t, floor, face=GOLD, rim=GOLD_L, inner=GOLD_D, gap=0, hammered=True, seed=3):
    """Широкая манжета/бэнгл в перспективе: верхняя кромка-эллипс, видимая внутренняя стенка, наружная грань высотой h.
    gap > 0 — разрез спереди (открытая манжета)."""
    soft_shadow_ellipse(c, (cx - rx - 6, cy + h - ry * 0.6, cx + rx + 6, cy + h + ry + 18), alpha=60, blur=14)
    xs = [-rx + 2 * rx * k / 80 for k in range(81)]

    def lo(x, yc, r_x=rx, r_y=ry):
        return yc + r_y * math.sqrt(max(0.0, 1 - (x / r_x) ** 2))

    # наружная грань: полосы с затенением к краям (объём)
    nstr = 24
    for k in range(nstr):
        xa, xb = -rx + 2 * rx * k / nstr, -rx + 2 * rx * (k + 1) / nstr
        xm = (xa + xb) / 2
        f = max(0.0, math.cos(math.asin(max(-1, min(1, (xm + rx * 0.25) / (rx * 1.25))))))
        col = mix(GOLD_D, face, min(1, 0.35 + 0.8 * f))
        sub = [xa + (xb - xa) * j / 4 for j in range(5)]
        pts = [(cx + x, lo(x, cy)) for x in sub] + [(cx + x, lo(x, cy + h)) for x in reversed(sub)]
        c.poly(pts, col)
    # блик-полоса по грани
    c.line([(cx + x, lo(x, cy + h * 0.32)) for x in xs[14:52]], GOLD_L, 7, alpha=170)
    if hammered:
        rnd = random.Random(seed)
        for _ in range(70):
            x = rnd.uniform(-rx * 0.92, rx * 0.92)
            y0, y1 = lo(x, cy) + 6, lo(x, cy + h) - 6
            if y1 <= y0:
                continue
            y = rnd.uniform(y0, y1)
            rr = rnd.uniform(4, 8)
            c.ellipse((cx + x - rr * 1.3, y - rr * 0.8, cx + x + rr * 1.3, y + rr * 0.8),
                      fill=GOLD_L if rnd.random() < 0.55 else GOLD_D, alpha=110)
    # верхняя кромка + внутренняя стенка + «дно» (фон сквозь проём)
    c.ellipse((cx - rx, cy - ry, cx + rx, cy + ry), fill=rim)
    irx, iry = rx - t, ry - t * ry / rx
    c.ellipse((cx - irx, cy - iry, cx + irx, cy + iry), fill=inner)
    c.line(epts(cx, cy, irx, iry, 190, 350, 40), mix(inner, GOLD_L, 0.35), 5, alpha=200)
    if h < 2 * iry:
        xi = irx * math.sqrt(max(0.0, 1 - (h / 2 / iry) ** 2))
        xl = [-xi + 2 * xi * k / 60 for k in range(61)]
        top = [(cx + x, cy + h - iry * math.sqrt(max(0.0, 1 - (x / irx) ** 2))) for x in xl]
        bot = [(cx + x, cy + iry * math.sqrt(max(0.0, 1 - (x / irx) ** 2))) for x in reversed(xl)]
        c.poly(top + bot, floor)
    if gap:
        g = gap / 2
        gl = [-g + 2 * g * k / 10 for k in range(11)]
        pts = [(cx + x, lo(x, cy, irx, iry) - 1) for x in gl] + [(cx + x, lo(x, cy + h) + 2) for x in reversed(gl)]
        c.poly(pts, floor)
        for sx in (-g, g):
            c.line([(cx + sx, lo(sx, cy, irx, iry)), (cx + sx, lo(sx, cy + h))], GOLD_DD, 4)


def stone(c, x, y, r, setting=GOLD, sparkle_on=False):
    c.circle(x, y + r * 0.12, r * 1.24, fill=mix(setting, BLK, 0.25))
    c.circle(x, y, r * 1.2, fill=setting)
    c.circle(x, y, r, fill=STONE)
    c.pie((x - r, y - r, x + r, y + r), 20, 160, STONE_D)
    c.circle(x, y + r * 0.05, r * 0.55, fill=(234, 238, 246))
    c.poly([(x - r * 0.45, y - r * 0.2), (x - r * 0.1, y - r * 0.6), (x + r * 0.1, y - r * 0.45), (x - r * 0.3, y - r * 0.05)],
           WH)
    for a in (45, 135, 225, 315):  # крапан
        px, py = x + math.cos(math.radians(a)) * r * 1.02, y + math.sin(math.radians(a)) * r * 1.02
        c.circle(px, py, max(1.6, r * 0.2), fill=mix(setting, WH, 0.3))
    if sparkle_on:
        sparkle(c, x + r * 0.5, y - r * 0.6, r * 1.3)


def tennis_loop(c, cx, cy, rx, ry, r=11, setting=GOLD, n=None, clasp=True):
    per = math.pi * (3 * (rx + ry) - math.sqrt((3 * rx + ry) * (rx + 3 * ry)))
    n = n or int(per / (r * 2.45))
    ring_shadow(c, cx, cy, rx, ry, r * 1.6, alpha=45, blur=8, dy=9)
    c.line(epts(cx, cy, rx, ry, 0, 360, 120), mix(setting, BLK, 0.2), max(3, r * 0.5))
    items = []
    for k in range(n):
        th = 2 * math.pi * k / n + 0.13
        items.append((math.sin(th), cx + rx * math.cos(th), cy + ry * math.sin(th), k))
    items.sort()
    for s, x, y, k in items:
        rr = r * (0.86 + 0.14 * (s + 1) / 2)
        stone(c, x, y, rr, setting, sparkle_on=(k % 7 == 2 and s > -0.3))
    if clasp:
        x, y = cx + rx * math.cos(1.62), cy + ry * math.sin(1.62)
        c.rect((x - r * 1.5, y - r * 0.95, x + r * 1.5, y + r * 0.95), fill=mix(setting, BLK, 0.1), r=r * 0.35)
        c.rect((x - r * 1.3, y - r * 0.75, x + r * 1.3, y + r * 0.2), fill=mix(setting, WH, 0.25), r=r * 0.3)


BIRTH = [(196, 36, 60), (112, 64, 170), (30, 70, 160), (40, 150, 90), (236, 170, 40)]


def birthstone_loop(c, cx, cy, rx, ry, stones=BIRTH, r=10):
    ring_shadow(c, cx, cy, rx, ry, 5, alpha=45, blur=5, dy=6)
    pts = epts(cx, cy, rx, ry, 0, 360, 180)
    c.line(pts, GOLD_D, 4)
    for k, (x, y) in enumerate(pts[:-1]):
        if k % 2 == 0:
            c.circle(x, y - 0.6, 1.9, fill=GOLD_L)
    n = len(stones)
    for k, col in enumerate(stones):
        th = math.radians(40 + 100 * k / (n - 1))
        x, y = cx + rx * math.cos(th), cy + ry * math.sin(th)
        c.circle(x, y + 2, r + 5, fill=GOLD_DD)
        c.circle(x, y, r + 5, fill=GOLD)
        c.circle(x, y, r, fill=col)
        c.circle(x - r * 0.3, y - r * 0.35, r * 0.34, fill=mix(col, WH, 0.6))
    # застёжка-колечко сзади
    x, y = cx + rx * math.cos(math.radians(265)), cy + ry * math.sin(math.radians(265))
    c.ellipse((x - 7, y - 6, x + 7, y + 6), outline=GOLD_D, width=3)


# --- плитки сетки (a)
TILE_BG = [(248, 236, 228), (244, 234, 222), (240, 232, 236), (246, 238, 226)]


def br_tile_art(kind):
    def art(c, box):
        def fn(t):
            x0, y0, x1, y1 = box
            bgc = TILE_BG[kind]
            t.rect(box, fill=bgc)
            t.ellipse((x0 - 60, y0 + (y1 - y0) * 0.35, x1 + 60, y1 + 140), fill=mix(bgc, WH, 0.45))
            cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
            H = y1 - y0
            if kind == 0:
                chain_loop(t, cx, cy - 2, 150, H * 0.3, L=44, hole=mix(bgc, WH, 0.3))
            elif kind == 1:
                band_ring(t, cx, cy - H * 0.2, 128, H * 0.2, H * 0.3, 16, floor=mix(bgc, WH, 0.35), gap=46)
            elif kind == 2:
                tennis_loop(t, cx, cy, 160, H * 0.3, r=11.5, setting=WHITE_METAL)
            else:
                birthstone_loop(t, cx, cy - 6, 150, H * 0.3, r=12)
        S.clip_draw(c, box, 20, fn)
    return art


# --- квиз (b): два одинаковых теннисных браслета A и B на тёмном бархате
def ab_bracelets(c, box):
    def fn(t):
        x0, y0, x1, y1 = box
        t.vgrad(box, (86, 40, 60), (58, 24, 40))
        t.ellipse((x0 + 20, y0 + 30, x1 - 20, y1 + 120), fill=(104, 52, 74), alpha=120)
        H = y1 - y0
        for k, lab in enumerate("AB"):
            cx = x0 + (x1 - x0) * (0.27 + 0.46 * k)
            cy = y0 + H * 0.5
            tennis_loop(t, cx, cy, 170, H * 0.27, r=11, setting=WHITE_METAL)
            bx, by = cx, y0 + H * 0.5
            t.circle(bx, by, 30, fill=GOLD)
            t.circle(bx, by, 26, fill=(255, 250, 238))
            t.text((bx, by + 1), lab, "mxb", 30, PLUM, anchor="mm")
        t.circle((x0 + x1) / 2, y0 + H * 0.5, 22, fill=WH, alpha=230)
        t.text(((x0 + x1) / 2, y0 + H * 0.5), "?", "mxb", 28, BERRY, anchor="mm")
    S.clip_draw(c, box, 20, fn, bg=(70, 32, 50))


# --- сравнение трёх (c): сечение под лупой
def xsection_art(kind):
    """kind 0 — позолота (тонкий слой на латуни), 1 — вермель (толстый слой на серебре), 2 — цельное золото."""
    labels = {0: ("thin gold layer", "brass"), 1: ("thicker gold layer", "sterling silver"), 2: ("gold all the way", None)}

    def art(c, box):
        def fn(t):
            x0, y0, x1, y1 = box
            t.rect(box, fill=(250, 244, 238))
            cx, cy = (x0 + x1) / 2 - 4, (y0 + y1) / 2 + 2
            R = min(x1 - x0, y1 - y0) * 0.24
            # ручка лупы
            capsule(t, (cx + R * 0.78, cy + R * 0.78), (cx + R * 1.22, cy + R * 1.22), 20, (70, 58, 62))
            t.circle(cx, cy, R + 14, fill=(92, 80, 84))
            t.circle(cx, cy, R + 6, fill=(236, 232, 228))
            if kind == 0:
                t.circle(cx, cy, R, fill=GOLD)
                t.circle(cx, cy, R - 5, fill=(184, 150, 96))
                core = (184, 150, 96)
            elif kind == 1:
                t.circle(cx, cy, R, fill=GOLD)
                t.circle(cx, cy, R - 16, fill=(208, 212, 220))
                core = (208, 212, 220)
            else:
                t.circle(cx, cy, R, fill=GOLD)
                core = GOLD
            t.pie((cx - R, cy - R, cx + R, cy + R), 200, 290, GOLD_L, alpha=110 if kind == 2 else 0)
            t.ellipse((cx - R * 0.55, cy - R * 0.7, cx - R * 0.05, cy - R * 0.45), fill=WH, alpha=120)
            top, bot = labels[kind]
            t.text((cx, y0 + 18), top, "mb", 19, GOLD_DD, anchor="ma")
            if bot:
                t.text((cx, y1 - 14), bot, "mb", 19, mix(core, BLK, 0.45), anchor="md")
            elif kind == 2:
                t.text((cx, y1 - 14), "10k · 14k · 18k", "mb", 19, GOLD_DD, anchor="md")
        S.clip_draw(c, box, 18, fn)
    return art


def vs3(P, t):
    """Сравнение трёх: три колонки (рисунок, лента-название, строки «метка — текст»), подпись, кнопка."""
    p = P["pal"]
    c = C(p["bg"])
    bgfill(c, p)
    y = head(c, t, p, size=t.get("size", 56))
    top = y + 24
    bot = t.get("bot", 850)
    g = 16
    cw = (980 - 2 * g) / 3
    ah = t.get("art_h", 210)
    ry0 = top + 12 + ah + 12 + 56 + 16
    nrows = len(t["cols"][0][3])
    fs = t.get("row_size", 25)
    while True:
        hs = []
        for j in range(nrows):
            nl = max(len(c.wrap(col_[3][j][1], c.font("mb", fs), cw - 44)) for col_ in t["cols"])
            hs.append(26 + nl * c.lh("mb", fs, 1.05))
        if ry0 + sum(hs) + 12 * (nrows - 1) <= bot - 14 or fs <= 19:
            break
        fs -= 1
    spare = min(40, max(0, (bot - 14 - ry0 - sum(hs)) / max(1, nrows - 1)))
    for k, (name, col, art, rows) in enumerate(t["cols"]):
        x0 = 50 + k * (cw + g)
        c.card((x0, top, x0 + cw, bot), fill=mix(col, WH, 0.9), r=26, sh_alpha=55, blur=12, off=(0, 6))
        ab = (x0 + 10, top + 10, x0 + cw - 10, top + 10 + ah)
        art(c, ab)
        by = ab[3] + 12
        c.rect((x0 + 10, by, x0 + cw - 10, by + 56), fill=col, r=14)
        c.text((x0 + cw / 2, by + 28), name, "mxb", c.fit(name, "mxb", cw - 40, 1, 30), WH, anchor="mm")
        yy = ry0
        for j, (lab, txt) in enumerate(rows):
            if j:
                c.line([(x0 + 22, yy - spare / 2 - 2), (x0 + cw - 22, yy - spare / 2 - 2)], mix(col, WH, 0.65), 2)
            c.text((x0 + 22, yy), lab, "mb", 18, col)
            c.block(txt, "mb", fs, yy + 24, cw - 44, (36, 34, 40), align="left", x=x0 + 22, max_lines=3, gap=1.05)
            yy += hs[j] + spare
    if t.get("foot"):
        c.block(t["foot"], "mb", t.get("foot_size", 30), bot + 20, 990, p["ink"], max_lines=1, highlight=p.get("hl"),
                hl_pad=8)
    cta_btn(c, P, W / 2, t.get("btn_y", 988))
    return c


# --- сцена (d): рука со стеком
SK = (226, 178, 144)
SK_D = (204, 152, 118)
SK_L = (240, 204, 174)
SK_LN = (186, 134, 102)
YA = 600
ARM_TOP = [(-40, YA - 122), (150, YA - 114), (300, YA - 102), (440, YA - 88), (560, YA - 76), (625, YA - 73),
           (690, YA - 80), (760, YA - 90), (806, YA - 94)]
ARM_BOT = [(-40, YA + 132), (150, YA + 124), (300, YA + 110), (440, YA + 94), (560, YA + 82), (625, YA + 78),
           (690, YA + 80), (760, YA + 78), (814, YA + 66)]
STACK_X = {"charm": 440, "beads": 474, "tennis": 506, "cuff": 566}


def band_geom(xb, e=10, bulge=12, n=36):
    top, bot = interp(ARM_TOP, xb), interp(ARM_BOT, xb)
    yc, R = (top + bot) / 2, (bot - top) / 2 + e
    out = []
    for k in range(n + 1):
        ph = -math.pi / 2 + math.pi * k / n
        out.append((ph, xb + bulge * math.cos(ph), yc + R * math.sin(ph)))
    return out, yc, R


def shade_f(ph, ph0=-0.5):
    return max(0.0, math.cos(ph - ph0)) ** 1.4


def draw_cuff(c, xb, wb=62):
    g, yc, R = band_geom(xb, e=12, bulge=14)
    # тень на коже слева
    lay = c.layer()
    d = ImageDraw.Draw(lay)
    d.polygon(c.sp([(x - wb / 2 - 14, y) for _, x, y in g] + [(x - wb / 2 + 4, y) for _, x, y in reversed(g)]),
              fill=(90, 50, 30, 70))
    c.put(lay, blur=6)
    for (p0, xa, ya), (p1, xb2, yb) in zip(g, g[1:]):
        f = shade_f((p0 + p1) / 2)
        col = mix(GOLD_DD, GOLD_L, min(1, 0.15 + 0.95 * f))
        c.poly([(xa - wb / 2, ya), (xa + wb / 2, ya), (xb2 + wb / 2, yb), (xb2 - wb / 2, yb)], col)
    rnd = random.Random(7)
    for _ in range(46):
        ph = rnd.uniform(-1.35, 1.35)
        u = rnd.uniform(-wb * 0.38, wb * 0.38)
        x = xb + 14 * math.cos(ph) + u
        y = yc + R * math.sin(ph)
        rr = rnd.uniform(3.5, 6.5)
        c.ellipse((x - rr, y - rr * 1.3 * max(0.35, math.cos(ph)), x + rr, y + rr * 1.3 * max(0.35, math.cos(ph))),
                  fill=GOLD_L if rnd.random() < 0.5 else GOLD_D, alpha=120)
    c.line([(x - wb / 2, y) for _, x, y in g], GOLD_DD, 3)
    c.line([(x + wb / 2, y) for _, x, y in g], GOLD_DD, 3)
    c.line([(x - wb / 2 + 6, y) for _, x, y in g[6:22]], GOLD_L, 3, alpha=200)


def draw_beads(c, xb, rb=13):
    g, yc, R = band_geom(xb, e=8, bulge=12)
    cols = [(44, 124, 88), GOLD, (232, 168, 170), GOLD, (38, 66, 150), GOLD]
    n = int(math.pi * R / (rb * 1.9))
    items = []
    for k in range(n + 1):
        ph = -math.pi / 2 + math.pi * k / n
        items.append((-abs(ph), ph, k))
    items.sort()
    for _, ph, k in items:
        x, y = xb + 12 * math.cos(ph), yc + R * math.sin(ph)
        col = cols[k % len(cols)]
        c.circle(x - 3, y + 3, rb, fill=(120, 70, 50), alpha=70)
        c.circle(x, y, rb, fill=col)
        c.circle(x, y, rb, outline=mix(col, BLK, 0.3), width=1.5)
        c.circle(x - rb * 0.32, y - rb * 0.36, rb * 0.34, fill=mix(col, WH, 0.65))


def draw_tennis_line(c, xb, r=8):
    g, yc, R = band_geom(xb, e=6, bulge=12)
    c.line([(x, y) for _, x, y in g], (150, 154, 164), 5)
    n = int(math.pi * R / (r * 2.35))
    items = []
    for k in range(n + 1):
        ph = -math.pi / 2 + math.pi * k / n
        items.append((-abs(ph), ph, k))
    items.sort()
    for _, ph, k in items:
        x, y = xb + 12 * math.cos(ph), yc + R * math.sin(ph)
        stone(c, x, y, r * (0.8 + 0.2 * math.cos(ph)), WHITE_METAL, sparkle_on=(k in (4, 9, 13)))


def draw_charm_chain(c, xb):
    g, yc, R = band_geom(xb, e=4, bulge=12, n=60)
    c.line([(x, y) for _, x, y in g], GOLD_D, 4)
    for k, (_, x, y) in enumerate(g):
        if k % 2 == 0:
            c.circle(x - 0.8, y, 1.8, fill=GOLD_L)
    # подвеска-медальон с гравировкой-инициалом, лежит на столе под запястьем
    _, x, y = g[-1]
    c.ellipse((x - 6, y - 2, x + 8, y + 14), outline=GOLD_D, width=3)
    mx, my = x + 10, y + 42
    soft_shadow_ellipse(c, (mx - 26, my - 18, mx + 34, my + 36), alpha=70, blur=8)
    c.line([(x + 2, y + 12), (mx, my - 26)], GOLD_D, 3)
    c.circle(mx, my, 28, fill=GOLD_D)
    c.circle(mx, my - 1.5, 27, fill=GOLD)
    c.circle(mx, my - 1.5, 21, fill=GOLD_M)
    c.text((mx, my - 1), "A", "mxb", 26, GOLD_DD, anchor="mm")
    c.arc((mx - 24, my - 25, mx + 24, my + 22), 200, 260, GOLD_L, 3)


def hand_and_arm(c):
    # большой палец (под кистью)
    capsule(c, (700, YA + 60), (826, YA + 150), 52, SK_LN)
    capsule(c, (700, YA + 58), (822, YA + 146), 46, SK)
    capsule(c, (790, YA + 124), (818, YA + 144), 26, (236, 196, 178))
    # предплечье + тыльная сторона кисти
    pts = ARM_TOP + [(820, YA - 60), (828, YA - 20), (828, YA + 20), (822, YA + 50)] + list(reversed(ARM_BOT))
    lay = c.layer()
    ImageDraw.Draw(lay).polygon(c.sp([(x + 6, y + 16) for x, y in pts]), fill=(110, 70, 40, 60))
    c.put(lay, blur=14)
    c.poly(pts, SK)
    c.line(pts + [pts[0]], SK_LN, 2.5)
    # объём: светлая полоса по верху предплечья
    hl = [(x, y + 26) for x, y in ARM_TOP[:7]] + [(x, y + 58) for x, y in reversed(ARM_TOP[:7])]
    c.poly(hl, SK_L, alpha=120)
    # пальцы: мизинец, безымянный, средний, указательный
    fingers = [((796, YA - 70), (916, YA - 96), 34), ((812, YA - 30), (978, YA - 44), 40),
               ((816, YA + 10), (1000, YA + 12), 42), ((812, YA + 48), (972, YA + 70), 40)]
    for p0, p1, w in fingers:
        capsule(c, p0, p1, w + 5, SK_LN)
        capsule(c, p0, p1, w, SK)
        L = math.hypot(p1[0] - p0[0], p1[1] - p0[1])
        ux, uy = (p1[0] - p0[0]) / L, (p1[1] - p0[1]) / L
        n0 = (p1[0] - ux * 34, p1[1] - uy * 34)
        n1 = (p1[0] - ux * 8, p1[1] - uy * 8)
        capsule(c, n0, n1, w * 0.6, (238, 194, 180))
        capsule(c, (n0[0] + ux * 3, n0[1] + uy * 3 - 3), (n1[0] - ux * 6, n1[1] - uy * 6 - 3), w * 0.18, WH, alpha=120)
        # складки суставов
        for d in (0.36, 0.64):
            qx, qy = p0[0] + (p1[0] - p0[0]) * d, p0[1] + (p1[1] - p0[1]) * d
            c.line([(qx - uy * w * 0.22, qy + ux * w * 0.22), (qx + uy * w * 0.22, qy - ux * w * 0.22)], SK_D, 2)
    # костяшки
    for (p0, _, w) in fingers:
        c.ellipse((p0[0] - 20, p0[1] - w * 0.3, p0[0] + 4, p0[1] + w * 0.3), fill=SK_L, alpha=110)
    # сухожилия на тыльной стороне
    for (p0, _, w) in fingers[1:]:
        c.line([(660, YA + (p0[1] - YA) * 0.35), (p0[0] - 26, p0[1])], SK_D, 2, alpha=110)


def stack_scene(c):
    c.vgrad((0, 0, W, W), (248, 238, 228), (236, 222, 208))
    for k in range(40):
        y = 230 + k * 22
        c.line([(0, y), (W, y + 6)], (230, 214, 198), 1, alpha=90)
    # рукав свитера
    hand_and_arm(c)
    draw_charm_chain(c, STACK_X["charm"])
    draw_beads(c, STACK_X["beads"])
    draw_tennis_line(c, STACK_X["tennis"])
    draw_cuff(c, STACK_X["cuff"])
    sl = (184, 138, 100)
    top = [(-40, YA - 170), (120, YA - 166), (250, YA - 150)]
    c.poly([(-40, YA - 170), (250, YA - 150), (262, YA + 160), (-40, YA + 176)], sl)
    for k in range(9):
        x = 196 + k * 7
        c.line([(x, YA - 148), (x + 3, YA + 158)], mix(sl, BLK, 0.14), 3)
    c.line([(250, YA - 150), (262, YA + 160)], mix(sl, BLK, 0.22), 4)
    for k in range(5):
        c.line([(10 + k * 36, YA - 160), (20 + k * 36, YA + 170)], mix(sl, WH, 0.12), 6, alpha=160)
    del top


P_BR = dict(bg=(250, 242, 236), bg2=(244, 230, 222), ink=PLUM, sub=(122, 98, 104), acc=BERRY, btn=(150, 44, 70),
            tile=WH, tile_ink=PLUM, iconbg=(248, 236, 230))
PACKS[1] = dict(
    doc="NT-bracelet-trends-US-2026-09-30", cta="Learn more", pal=P_BR,
    a=dict(fn="grid2x2_art", title="Bracelet trends 2026:", title2="which style is yours?", size=58, t2k=0.92,
           tiles=[(br_tile_art(0), "Chunky gold chain", "wide curb or puffy links, worn alone"),
                  (br_tile_art(1), "Sculptural cuff", "domed shapes, hammered textures"),
                  (br_tile_art(2), "Everyday tennis bracelet", "a thin line of stones, worn daily"),
                  (br_tile_art(3), "Birthstone bracelet", "a stone for each child, add more later")],
           badge=["TREND 1", "TREND 2", "TREND 4", "TREND 5"], art_k=0.54, name_size=33, sub_size=23,
           extra_text="метки на плитках: TREND 1 / TREND 2 / TREND 4 / TREND 5",
           src="разделы «Gold goes bold» (Trend 1 chunky chains: wide curb, puffy links, worn alone; Trend 2 sculptural cuffs: "
               "domed shapes, hammered textures), «The tennis bracelet becomes everyday wear» (Trend 4: a thin line of stones "
               "worn every day), «Bracelets that mean something» (Trend 5: birthstone bracelet for mom, one stone for each child, "
               "new stones added later)",
           note="сетка 2×2: 4 стиля из 7 — у каждой плитки рисунок браслета (панцирная цепь, открытая манжета с молотковой "
                "фактурой, теннисный в белом металле, тонкая цепочка с 5 цветными камнями), метка TREND с номером из статьи и "
                "кнопка «Learn more»; числа «7 styles» над плитками нет; без брендов, узнаваемых дизайнов, фирменного голубого и цен"),
    b=dict(fn="quiz_art", title="Tennis bracelet:", title2="lab-grown or mined diamonds?", size=58, t2k=0.84,
           tag="POLL", step="Question 1 of 3", art=ab_bracelets, art_h=270, q_size=32,
           q="They look identical to the naked eye. Which would you pick?",
           opts=["Lab-grown: usually less for the same carat weight", "Mined: tends to keep resale value better"],
           opt_layout="list", opt_size=28, card_bot=912, btn_y=990,
           extra_text="рисунок: два одинаковых теннисных браслета с метками A и B, между ними «?»",
           pal=dict(bg=(84, 34, 56), bg2=(46, 18, 32), ink=WH, sub=(236, 210, 220), acc=(186, 128, 34), t2=(246, 210, 140),
                    btn=(214, 72, 100), deco=True),
           src="раздел «The tennis bracelet becomes everyday wear» (lab-grown: same chemical makeup and hardness, look identical "
               "to the naked eye, usually cost noticeably less for the same total carat weight; mined: tend to keep resale value better)",
           note="опрос A/B на тёмном бархате: два одинаковых теннисных браслета A и B, вопрос-выбор и 2 ответа с фактами статьи; "
                "без «real / certified diamonds», «investment», цен и брендов"),
    c=dict(fn="vs3", title="Gold-plated, vermeil or solid gold?", sub="The difference matters more than the photos show",
           size=54, sub_size=29, art_h=214, bot=842,
           cols=[("GOLD-PLATED", (160, 116, 56), xsection_art(0),
                  [("GOLD", "a very thin layer"), ("OVER", "brass or another base metal"), ("DAILY WEAR", "the color can wear off")]),
                 ("VERMEIL", (112, 118, 136), xsection_art(1),
                  [("GOLD", "a thicker layer"), ("OVER", "sterling silver"), ("DAILY WEAR", "a middle ground")]),
                 ("SOLID GOLD", (176, 126, 26), xsection_art(2),
                  [("GOLD", "all the way through"), ("KARAT", "10k, 14k or 18k"), ("DAILY WEAR", "can be worn every day for years")])],
           foot="14k: the usual balance of rich color and strength", pal=dict(hl=(255, 236, 196)), btn_y=990,
           extra_text="подписи в лупах: thin gold layer / brass; thicker gold layer / sterling silver; gold all the way / 10k · 14k · 18k",
           src="раздел «Before buying: metal, fit and care» (gold-plated: very thin layer over brass or another base metal, color can "
               "wear off with daily use; vermeil: thicker layer over sterling silver, a middle ground; solid gold: 10k/14k/18k all the "
               "way through, can be worn every day and polished for years; 14k — the usual balance between rich color and strength)",
           note="сравнение трёх: сечение проволоки под лупой (тонкий слой золота на латуни / толстый слой на серебре / золото насквозь), "
                "три строки фактов из статьи; без цен и слов «affordable / expensive»"),
    d=dict(fn="callouts_scene", scene=stack_scene, title="The 2026 bracelet stack:", title2="edited, not piled on", size=56, y=40,
           callouts=[("1–2 slimmer pieces,\na different texture", (476, 512), 36, 318, "l"),
                     ("Anchor piece:\na cuff or chunky chain", (572, 536), 1044, 318, "r"),
                     ("Something personal:\na charm or engraved bar", (452, 736), 36, 872, "l"),
                     ("3 to 5 pieces,\nso each one stays visible", (560, 690), 1044, 872, "r")],
           co_w=440, co_size=27, btn_y=1000,
           src="раздел «The art of the stack» (Trend 3, the edited stack: one anchor piece — cuff or chunky chain; one or two slimmer "
               "pieces with a different texture — bead bracelet or a thin line of stones; something personal — charm or engraved bar; "
               "three to five pieces so each one stays visible)",
           note="сцена: запястье с 4 браслетами на льняной ткани — манжета-якорь, бусины (малахит, лазурит, розовый опал, золото), "
                "тонкая линия камней, цепочка с медальоном-инициалом; 4 сноски-правила стека; без брендов, до/после и цен"),
)


# =====================================================================  2. US · товарка · дом · сотовые шторы без шнура
NAVY2 = (36, 52, 78)
TEAL2 = (42, 110, 118)
CORAL2 = (206, 92, 62)
LINEN = (246, 240, 230)
TRIM = (252, 251, 248)


def cell_shade(c, x0, top, x1, bot, fab, pleat=11, alpha=255, rail=None, bottom_rail=True, top_rail=True):
    """Сотовая штора: полотно из горизонтальных «сот»-складок, рейки сверху и снизу, без шнура."""
    if bot - top < 2:
        return
    c.rect((x0, top, x1, bot), fill=fab, alpha=alpha)
    dk = mix(fab, BLK, 0.13)
    lt = mix(fab, WH, 0.45)
    y = top + pleat
    while y < bot - 3:
        c.line([(x0, y), (x1, y)], dk, 2, alpha=min(255, alpha))
        c.line([(x0, y + 2.2), (x1, y + 2.2)], lt, 1.4, alpha=min(255, alpha))
        y += pleat
    rail = rail or mix(fab, WH, 0.55)
    if top_rail:
        c.rect((x0 - 2, top - 3, x1 + 2, top + 6), fill=rail, r=3)
    if bottom_rail:
        c.rect((x0 - 2, bot - 6, x1 + 2, bot + 3), fill=mix(rail, BLK, 0.06), r=3)


def window_open(c, box, trim=12, sky=((150, 196, 232), (222, 238, 248)), sill=True, trees=True, seed=1, roofs=False):
    x0, y0, x1, y1 = box
    c.rect((x0 - trim, y0 - trim, x1 + trim, y1 + trim), fill=TRIM, r=3)
    c.vgrad(box, *sky)
    if trees:
        rnd = random.Random(seed)
        for k in range(6):
            tx = x0 + (x1 - x0) * rnd.random()
            r = (x1 - x0) * rnd.uniform(0.12, 0.2)
            c.circle(tx, y1 - r * 0.3, r, fill=(120, 170, 110) if k % 2 else (98, 150, 96))
    if roofs:
        rx = x0 + (x1 - x0) * 0.15
        c.poly([(rx, y0 + (y1 - y0) * 0.42), (rx + (x1 - x0) * 0.35, y0 + (y1 - y0) * 0.22),
                (rx + (x1 - x0) * 0.7, y0 + (y1 - y0) * 0.42)], (176, 92, 74))
        c.rect((rx + 10, y0 + (y1 - y0) * 0.42, rx + (x1 - x0) * 0.7 - 10, y1), fill=(232, 214, 190))
        for k in range(2):
            wx = rx + 26 + k * (x1 - x0) * 0.28
            c.rect((wx, y0 + (y1 - y0) * 0.5, wx + (x1 - x0) * 0.14, y0 + (y1 - y0) * 0.72), fill=(120, 150, 176))
    if sill:
        c.rect((x0 - trim - 8, y1 + trim - 3, x1 + trim + 8, y1 + trim + 8), fill=TRIM, r=3)
    return box


def phone_remote(c, cx, cy, s, col=NAVY2):
    c.rect((cx - s * 0.3, cy - s * 0.52, cx + s * 0.3, cy + s * 0.52), fill=col, r=s * 0.1)
    c.rect((cx - s * 0.24, cy - s * 0.42, cx + s * 0.24, cy + s * 0.38), fill=(236, 242, 248), r=s * 0.05)
    c.rect((cx - s * 0.14, cy - s * 0.26, cx + s * 0.14, cy - s * 0.1), fill=TEAL2, r=s * 0.03)
    c.rect((cx - s * 0.14, cy - s * 0.02, cx + s * 0.14, cy + s * 0.14), fill=(190, 200, 212), r=s * 0.03)
    for k in range(3):
        r = s * (0.5 + 0.22 * k)
        c.arc((cx + s * 0.1 - r, cy - s * 0.62 - r, cx + s * 0.1 + r, cy - s * 0.62 + r), 290, 340, TEAL2, 4)


def room_art(kind):
    """kind: 0 спальня (блэкаут), 1 гостиная (светорассеивающая), 2 ванная у улицы (сверху-вниз), 3 высокое окно (мотор)."""
    def art(c, box):
        def fn(t):
            x0, y0, x1, y1 = box
            H, Wd = y1 - y0, x1 - x0
            fl = y0 + H * 0.8
            if kind == 0:
                t.rect(box, fill=(198, 196, 206))
                t.rect((x0, fl, x1, y1), fill=(170, 150, 136))
                wb = window_open(t, (x0 + Wd * 0.56, y0 + H * 0.18, x0 + Wd * 0.86, y0 + H * 0.66), trim=9, trees=True, seed=2)
                cell_shade(t, wb[0], wb[1] + 2, wb[2], wb[3], NAVY2, pleat=9)
                # кровать
                bx0, bx1 = x0 + Wd * 0.06, x0 + Wd * 0.5
                t.rect((bx0, y0 + H * 0.36, bx0 + 16, fl + 6), fill=(120, 96, 80), r=4)
                t.rect((bx0, y0 + H * 0.36, bx0 + (bx1 - bx0) * 0.12, y0 + H * 0.62), fill=(150, 120, 100), r=8)
                t.rect((bx0 + 10, y0 + H * 0.58, bx1, fl - 4), fill=(236, 232, 226), r=8)
                t.rect((bx0 + 26, y0 + H * 0.5, bx0 + 110, y0 + H * 0.62), fill=WH, r=10)
                t.rect((bx0 + 90, y0 + H * 0.6, bx1 + 4, fl), fill=(120, 140, 170), r=8)
                # тумбочка с лампой
                nx = x0 + Wd * 0.93
                t.rect((nx - 26, y0 + H * 0.6, nx + 30, fl), fill=(150, 120, 100), r=3)
                t.glow((nx - 40, y0 + H * 0.3, nx + 44, y0 + H * 0.66), (255, 220, 150), alpha=120, blur=14)
                t.poly([(nx - 16, y0 + H * 0.44), (nx + 20, y0 + H * 0.44), (nx + 12, y0 + H * 0.34), (nx - 8, y0 + H * 0.34)],
                       (250, 226, 170))
                t.line([(nx + 2, y0 + H * 0.44), (nx + 2, y0 + H * 0.6)], (90, 80, 70), 3)
            elif kind == 1:
                t.rect(box, fill=(246, 236, 220))
                t.rect((x0, fl, x1, y1), fill=(206, 170, 128))
                wb = window_open(t, (x0 + Wd * 0.18, y0 + H * 0.1, x0 + Wd * 0.62, y0 + H * 0.62), trim=10, trees=True, seed=4)
                t.circle(wb[0] + (wb[2] - wb[0]) * 0.7, wb[1] + 36, 26, fill=(255, 236, 170))
                cell_shade(t, wb[0], wb[1] + 2, wb[2], wb[3], (252, 248, 238), pleat=9, alpha=222)
                t.glow((wb[0] - 20, wb[1] - 10, wb[2] + 30, wb[3] + 90), (255, 246, 214), alpha=110, blur=24)
                t.poly([(wb[0], wb[3] + 10), (wb[2], wb[3] + 10), (wb[2] + 60, fl + 30), (wb[0] - 40, fl + 30)], (255, 248, 222), alpha=70)
                # диван
                sx0, sx1, sy = x0 + Wd * 0.08, x0 + Wd * 0.7, y0 + H * 0.6
                t.rect((sx0, sy, sx1, fl - 2), fill=(126, 150, 132), r=12)
                t.rect((sx0 + 20, sy + 26, sx1 - 20, fl - 14), fill=(140, 166, 146), r=8)
                t.rect((sx0 - 8, sy + 16, sx0 + 26, fl + 2), fill=(112, 136, 118), r=10)
                t.rect((sx1 - 26, sy + 16, sx1 + 8, fl + 2), fill=(112, 136, 118), r=10)
                t.rect((sx0 + 40, sy + 8, sx0 + 96, sy + 44), fill=(232, 176, 120), r=8)
                S.plant(t, x0 + Wd * 0.86, fl + 6, 0.5, pot=(236, 232, 226), leaf=(92, 140, 100))
            elif kind == 2:
                W6.wall_tiles(t, (x0, y0, x1, fl), base=(236, 240, 238), grout=(214, 222, 220), tw=52, th=28)
                t.rect((x0, fl, x1, y1), fill=(196, 204, 206))
                wb = window_open(t, (x0 + Wd * 0.3, y0 + H * 0.08, x0 + Wd * 0.7, y0 + H * 0.58), trim=9, trees=False, roofs=True)
                mid = wb[1] + (wb[3] - wb[1]) * 0.36
                t.rect((wb[0] - 2, wb[1] - 2, wb[2] + 2, wb[1] + 7), fill=(236, 232, 224), r=3)
                cell_shade(t, wb[0], mid, wb[2], wb[3], (250, 246, 238), pleat=8)
                W6.arrow_line(t, (wb[2] + 24, wb[1] + 10), (wb[2] + 24, mid - 4), CORAL2, 4, 10, both=False)
                # ванна
                tx0, tx1, ty = x0 + Wd * 0.1, x0 + Wd * 0.9, y0 + H * 0.64
                t.rect((tx0, ty, tx1, fl + 8), fill=WH, r=18)
                t.rect((tx0 - 6, ty - 8, tx1 + 6, ty + 8), fill=(244, 246, 248), r=6)
                t.rect((tx1 - 70, ty - 40, tx1 - 62, ty - 6), fill=(160, 166, 176), r=3)
                t.rect((tx1 - 70, ty - 40, tx1 - 40, ty - 32), fill=(160, 166, 176), r=3)
            else:
                t.rect(box, fill=(240, 236, 228))
                t.rect((x0, y1 - H * 0.1, x1, y1), fill=(190, 160, 124))
                for k in range(2):
                    wx0 = x0 + Wd * (0.14 + 0.32 * k)
                    wb = window_open(t, (wx0, y0 + H * 0.06, wx0 + Wd * 0.26, y1 - H * 0.14), trim=8, trees=True, seed=5 + k, sill=False)
                    cell_shade(t, wb[0], wb[1] + 2, wb[2], wb[1] + (wb[3] - wb[1]) * 0.55, (238, 226, 206), pleat=9)
                phone_remote(t, x0 + Wd * 0.86, y0 + H * 0.52, H * 0.34)
        S.clip_draw(c, box, 20, fn)
    return art


def honeycomb(c, box, double):
    """Сечение сотовой шторы сбоку: окно (стекло) слева, колонка сот (одна или две), комната справа."""
    x0, y0, x1, y1 = box
    c.rect(box, fill=(232, 240, 244), r=16)
    gx = x0 + 22
    c.rect((gx, y0 + 12, gx + 14, y1 - 12), fill=(170, 210, 232), r=4)
    c.rect((gx - 6, y0 + 12, gx, y1 - 12), fill=TRIM)
    ccx = x0 + (x1 - x0) * 0.46
    hh = 30
    hw = 44
    cols = [ccx - hw * 0.55, ccx + hw * 0.55] if double else [ccx]
    fab = (250, 246, 238)
    edge = (150, 140, 124)
    n = int((y1 - y0 - 30) / hh)
    for cxk in cols:
        for k in range(n):
            cy = y0 + 18 + hh / 2 + k * hh
            pts = [(cxk - hw / 2, cy), (cxk - hw / 4, cy - hh / 2), (cxk + hw / 4, cy - hh / 2), (cxk + hw / 2, cy),
                   (cxk + hw / 4, cy + hh / 2), (cxk - hw / 4, cy + hh / 2)]
            c.poly(pts, fab)
            c.line(pts + [pts[0]], edge, 2.5)
    # воздух в сотах — точки
    for cxk in cols:
        for k in range(n):
            cy = y0 + 18 + hh / 2 + k * hh
            c.circle(cxk, cy, 3.5, fill=(170, 210, 232))
    # тёплая сторона — комната
    rx = x1 - 40
    for k in range(3):
        yy = y0 + (y1 - y0) * (0.3 + 0.2 * k)
        W6.arrow_line(c, (rx + 20, yy), (rx - 16, yy), CORAL2, 3, 9, both=False)


def mount_art(kind):
    """kind 0 — внутренний монтаж (штора в проёме, 3 замера ширины), 1 — наружный (перекрывает раму, +1½–3 in с каждой стороны)."""
    def art(c, box):
        def fn(t):
            x0, y0, x1, y1 = box
            t.rect(box, fill=(238, 232, 222))
            cx = (x0 + x1) / 2
            ow, oh = 190, (y1 - y0) * 0.66
            oy0 = y0 + (y1 - y0) * 0.18
            ob = (cx - ow / 2, oy0, cx + ow / 2, oy0 + oh)
            tr = 16
            t.rect((ob[0] - tr, ob[1] - tr, ob[2] + tr, ob[3] + tr), fill=TRIM, r=3)
            t.rect((ob[0] - tr - 1, ob[1] - tr - 1, ob[2] + tr + 1, ob[3] + tr + 1), outline=(214, 206, 194), width=2, r=3)
            t.vgrad(ob, (150, 196, 232), (222, 238, 248))
            t.rect((ob[0] - tr - 10, ob[3] + tr - 3, ob[2] + tr + 10, ob[3] + tr + 8), fill=TRIM, r=3)
            fab = (246, 238, 222)
            if kind == 0:
                cell_shade(t, ob[0], ob[1] + 3, ob[2], ob[1] + oh * 0.62, fab, pleat=9)
                t.rect((ob[0], ob[1], ob[2], ob[1] + 8), fill=(230, 224, 212))
                for k, fy in enumerate((0.12, 0.5, 0.88)):
                    yy = ob[1] + oh * fy
                    W6.arrow_line(t, (ob[0] + 5, yy), (ob[2] - 5, yy), CORAL2, 3, 10)
                t.text((cx, ob[3] + tr + 14), "3 width checks", "mb", 17, (110, 96, 84), anchor="ma")
            else:
                ext = 40
                sx0, sx1 = ob[0] - tr - ext, ob[2] + tr + ext
                t.rect((sx0 - 3, ob[1] - tr - 18, sx1 + 3, ob[1] - tr - 6), fill=(230, 224, 212), r=3)
                cell_shade(t, sx0, ob[1] - tr - 10, sx1, ob[1] + oh * 0.66, fab, pleat=9)
                yy = ob[1] + oh * 0.8
                for a, b in ((sx0, ob[0] - tr), (ob[2] + tr, sx1)):
                    W6.arrow_line(t, (a + 2, yy), (b - 2, yy), CORAL2, 3, 8)
                    t.line([(a, yy - 12), (a, yy + 12)], CORAL2, 3)
                    t.line([(b, yy - 12), (b, yy + 12)], CORAL2, 3)
                t.text((cx, ob[3] + tr + 14), "1½–3 in on each side", "mb", 17, (110, 96, 84), anchor="ma")
        S.clip_draw(c, box, 18, fn)
    return art


def stone_wall(c, box, seed=11):
    x0, y0, x1, y1 = box
    c.rect(box, fill=(188, 176, 160))
    rnd = random.Random(seed)
    tones = [(226, 214, 196), (214, 200, 180), (234, 224, 208), (204, 190, 172), (222, 206, 184)]
    y = y0 + 4
    while y < y1:
        h = rnd.uniform(30, 52)
        x = x0 - rnd.uniform(0, 40)
        while x < x1:
            w = rnd.uniform(56, 120)
            col = rnd.choice(tones)
            c.rect((x + 3, y + 3, x + w - 3, y + h - 3), fill=mix(col, BLK, 0.1), r=10)
            c.rect((x + 3, y + 2, x + w - 4, y + h - 5), fill=col, r=10)
            c.line([(x + 10, y + 7), (x + w * 0.6, y + 7)], mix(col, WH, 0.35), 2, alpha=150)
            x += w
        y += h


def living_stone_scene(c):
    c.rect((0, 0, W, W), fill=(244, 238, 228))
    fl = 900
    # стена под камень слева
    stone_wall(c, (0, 330, 470, fl))
    c.rect((466, 330, 476, fl), fill=(220, 210, 196))
    # окна справа, шторы опущены сверху (верх открыт)
    for k, wx in enumerate((560, 810)):
        wb = window_open(c, (wx, 420, wx + 200, 820), trim=16, trees=True, seed=3 + k)
        c.rect((wb[0] - 2, wb[1] - 2, wb[2] + 2, wb[1] + 10), fill=(236, 230, 218), r=3)
        mid = wb[1] + 132
        cell_shade(c, wb[0], mid, wb[2], wb[3], (250, 245, 236), pleat=12)
        c.glow((wb[0] - 10, wb[1] - 20, wb[2] + 10, mid + 40), (255, 250, 226), alpha=70, blur=26)
    # пол, ковёр
    c.rect((0, fl, W, W), fill=(200, 164, 122))
    for k in range(12):
        c.line([(k * 100 - 30, W), (k * 100 + 10, fl)], (188, 152, 112), 3)
    c.rect((0, fl - 8, W, fl + 2), fill=(250, 246, 240))
    c.ellipse((60, fl + 20, 760, fl + 150), fill=(226, 212, 190))
    # диван перед каменной стеной
    sx0, sx1, sy = 50, 440, 700
    c.shadow((sx0, sy, sx1, fl), r=18, alpha=60, blur=12, off=(0, 10))
    c.rect((sx0, sy, sx1, fl - 6), fill=(92, 112, 104), r=20)
    c.rect((sx0 + 34, sy + 60, sx1 - 34, fl - 30), fill=(108, 130, 120), r=12)
    c.line([((sx0 + sx1) / 2, sy + 64), ((sx0 + sx1) / 2, fl - 34)], (86, 104, 96), 3)
    c.rect((sx0 - 14, sy + 44, sx0 + 44, fl + 4), fill=(80, 98, 90), r=16)
    c.rect((sx1 - 44, sy + 44, sx1 + 14, fl + 4), fill=(80, 98, 90), r=16)
    c.rect((sx0 + 60, sy + 22, sx0 + 150, sy + 90), fill=(232, 184, 128), r=14)
    c.rect((sx1 - 150, sy + 22, sx1 - 60, sy + 90), fill=(236, 226, 206), r=14)
    for x in (sx0 + 10, sx1 - 18):
        c.rect((x, fl - 6, x + 8, fl + 10), fill=(70, 56, 44))
    # торшер между диваном и окнами + растение у окна
    c.line([(500, fl - 4), (500, 560)], (60, 56, 52), 6)
    c.ellipse((476, fl - 12, 524, fl + 2), fill=(60, 56, 52))
    c.poly([(466, 560), (534, 560), (520, 500), (480, 500)], (240, 222, 186))
    S.plant(c, 1026, fl + 8, 0.72, pot=(236, 232, 226), leaf=(92, 140, 100))


P_SH = dict(bg=(238, 242, 240), bg2=(228, 234, 232), ink=(30, 44, 56), sub=(88, 104, 112), acc=TEAL2, btn=CORAL2,
            tile=WH, tile_ink=(30, 44, 56), iconbg=(226, 236, 238))
PACKS[2] = dict(
    doc="NT-home-products-US-2026-09-30", cta="Learn more", pal=P_SH,
    a=dict(fn="grid2x2_art", title="Which cellular shade", title2="fits the room?", size=60, t2k=0.95,
           tiles=[(room_art(0), "Blackout", "an opaque inner lining"),
                  (room_art(1), "Light filtering", "softens the sun, keeps privacy"),
                  (room_art(2), "Top down bottom up", "daylight in at the top, privacy from the street"),
                  (room_art(3), "Motorized", "from a remote or a phone app")],
           badge=["BEDROOM", "LIVING ROOM", "BATHROOM", "TALL WINDOW"], art_k=0.55, name_size=33, sub_size=23,
           extra_text="метки на плитках: BEDROOM / LIVING ROOM / BATHROOM / TALL WINDOW",
           src="разделы «Light control» (light filtering — soften the sun and keep privacy, living rooms; blackout — opaque inner "
               "lining, bedrooms) и «Top down bottom up, day-night and motorized options» (top down — daylight through the upper part, "
               "lower part covered, bathrooms that face a street; motorized — tall windows, remote or phone app)",
           note="сетка 2×2 «комната → тип шторы»: спальня с тёмной шторой, гостиная со светлой полупрозрачной, ванная со шторой, "
                "опущенной сверху, два высоких окна и телефон-пульт; у каждой плитки «Learn more»; людей нет, без брендов и цен"),
    b=dict(fn="poll3", title="Cellular shades:", title2="single cell or double cell?", size=58, t2k=0.86,
           tag="POLL", step="Question 1 of 3", q="Which one fits the room?",
           opts=[(lambda c, b: honeycomb(c, b, False), "Single cell", "lighter and costs less"),
                 (lambda c, b: honeycomb(c, b, True), "Double cell", "more insulation and softer sound: large windows, colder rooms")],
           foot="The cells trap air between the glass and the room", card_bot=872, btn_y=996,
           pal=dict(bg=(226, 236, 236), bg2=(208, 224, 226), hl=WH, deco=True, iconbg=(232, 240, 244)),
           src="раздел «How cellular shades work and why cordless matters» (single cell — lighter, cost less; double cell — second row "
               "of pockets, more insulation and softer sound, large windows and colder rooms; the cells trap air between the glass and the room)",
           note="опрос A/B: сечение шторы сбоку — один или два ряда сот у стекла, тёплые стрелки со стороны комнаты; радиокнопки; "
                "без цифр экономии и цен"),
    c=dict(fn="vs2", title="Inside or outside mount?", sub="How to measure for cellular shades", size=58,
           cols=[("INSIDE MOUNT", TEAL2, mount_art(0),
                  [("WIDTH", "top, middle, bottom: use the narrowest"), ("HEIGHT", "left, center, right: use the longest"),
                   ("FRAME DEPTH", "roughly an inch or a little more")]),
                 ("OUTSIDE MOUNT", CORAL2, mount_art(1),
                  [("SIDES", "add about 1½ to 3 in on each side"), ("FRAME", "the shade overlaps the frame"),
                   ("LIGHT", "closes most of the edge gap")])],
           foot="Custom shades: made to the nearest ⅛ inch", art_h=250, pal=dict(hl=(255, 255, 255)),
           extra_text="подписи на рисунках: 3 width checks / 1½–3 in on each side",
           src="раздел «Measuring, and ready-made versus custom window treatments» (inside mount: width at top, middle, bottom — narrowest; "
               "height left, center, right — longest; depth roughly an inch or a little more; outside mount: 1½–3 in on each side, overlaps "
               "the frame; custom — to the nearest eighth of an inch) и «Light control» (outside mount closes most of the edge gap)",
           note="сравнение монтажа: окно со шторой в проёме и тремя стрелками ширины vs штора шире рамы со стрелками запаса по бокам; "
                "чек-лист замера из статьи; без цен (ориентир-диапазон статьи на крео не вынесен)"),
    d=dict(fn="top_scene", scene=living_stone_scene, title="Cordless cellular shades:", title2="how to choose", size=58, t2k=0.95,
           kicker="A ROOM-BY-ROOM GUIDE FOR 2026", sub="Light filtering or blackout, top down or motorized", sub_size=28,
           card_box=(110, 40, 970, 0), pad=34, btn_size=38,
           src="заголовок и лид статьи («Cordless Cellular Shades: How to Choose the Right Type for Every Room in 2026», room by room), "
               "разделы «Light control», «Top down bottom up…» и «One more easy upgrade: a faux stone accent wall» (warm gray or "
               "sand-colored stone pairs with white or linen shades)",
           note="сцена: гостиная — диван у стены под светлый песочный камень, два окна со светлыми шторами без шнура, опущенными сверху "
                "(верх окна открыт), торшер, растение; карточка-заголовок с кнопкой; людей нет, без брендов, до/после и цен"),
)


# =====================================================================  сборка
FN = dict(W6.FN)
FN["vs3"] = vs3


def texts(t, cta):
    return W6.texts(t, cta)


def build(n, letters="abcd"):
    P = PACKS[n]
    doc = P["doc"]
    items = []
    for Lt in "abcd":
        t = P[Lt]
        PPk = dict(P, pal={**P["pal"], **t.get("pal", {})})
        if Lt in letters:
            c = FN[t["fn"]](PPk, t)
            c.save(f"{doc}/{Lt}.png")
        items.append(dict(letter=Lt, file=f"cr/packs/{doc}/{Lt}.png",
                          concept=CONCEPT[Lt] + " — " + t.get("note", "") + "; опора: " + t.get("src", ""),
                          text=texts(t, P["cta"]), cta=P["cta"]))
    os.makedirs(os.path.join(OUT7, doc), exist_ok=True)
    with open(os.path.join(OUT7, doc, "creatives.json"), "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    args = sys.argv[1:] or [str(k) for k in PACKS]
    for a in args:
        if ":" in a:
            n, ls = a.split(":")
            build(int(n), ls.replace(",", ""))
        else:
            build(int(a))
