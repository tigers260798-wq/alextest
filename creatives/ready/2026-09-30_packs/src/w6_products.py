"""Волна 6 (29.09, креативщик w6-products): 5 карточек «Готово к заливу» × 4 статики 1:1, Pillow.
    python3 w6_products.py            — все пакеты
    python3 w6_products.py 3 5        — пакеты 3 и 5
    python3 w6_products.py 3:a,c      — пакет 3, буквы a и c
Пишет /home/user/alextest/creatives/ready/2026-09-30_packs/<docId>/<a|b|c|d>.png и creatives.json рядом.
Движок — w3_packs / w4_ukde (импорт, файлы не меняются) + p60_lib (холст C), шрифты Montserrat из src/fonts.
Здесь — свои раскладки (row4_hero, grid2x2_art, poll3, quiz_art, vs2, callouts_scene, route_map, top_scene) и
свои рисунки (тумбы, кресла, бассейны, электромобили, авто, паром и лайнер без ливреи, набережная).
Весь текст на картинках — только из статей article_drafts/<docId> (раздел — в поле src).
Без брендов, логотипов и фирменных цветов (Ikea, Intex, Bestway, Microlino, банки, консорсиумы, круизные и паромные
компании), без «vicino a te / in Ihrer Nähe / perto de você / near you», без «click here», без цен, которых нет в статье,
без возраста зрителя, без «sem consulta / aprovado na hora / nome sujo / sem entrada», без сумм и процентов в BR."""
import json
import math
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import w4_ukde as W4  # noqa: E402,F401  (тянет w3_packs и весь движок, регистрирует иконки)
import w3_packs as W3  # noqa: E402
import p60_lib  # noqa: E402
from p60_lib import C, W, mix, rotpts  # noqa: E402
import p60_icons as I  # noqa: E402
import p60_scenes as S  # noqa: E402
import p60w2_art as A  # noqa: E402

OUT6 = "/home/user/alextest/creatives/ready/2026-09-30_packs"
p60_lib.OUT = OUT6
p60_lib.F.update({
    "mblack": os.path.join(HERE, "fonts", "Montserrat-Black.ttf"),
    "mxb": os.path.join(HERE, "fonts", "Montserrat-ExtraBold.ttf"),
    "mb": os.path.join(HERE, "fonts", "Montserrat-Bold.ttf"),
    "msb": os.path.join(HERE, "fonts", "Montserrat-SemiBold.ttf"),
    "anton": os.path.join(HERE, "fonts", "Anton-Regular.ttf"),
})
WH = (255, 255, 255)
CONCEPT = W3.CONCEPT
PACKS = {}
SKIN = A.SKIN


def icon(c, name, cx, cy, s, col, bg=WH):
    I.ICONS[name](c, cx, cy, s, col, bg=bg)


def rrect_pts(x0, y0, x1, y1, r, n=5):
    """Точки скруглённого прямоугольника (для поворота через rotpts)."""
    r = min(r, (x1 - x0) / 2, (y1 - y0) / 2)
    pts = []
    for cx, cy, a0 in ((x1 - r, y0 + r, -90), (x1 - r, y1 - r, 0), (x0 + r, y1 - r, 90), (x0 + r, y0 + r, 180)):
        for k in range(n + 1):
            a = math.radians(a0 + 90 * k / n)
            pts.append((cx + math.cos(a) * r, cy + math.sin(a) * r))
    return pts


def rpoly(c, box, r, ang, pivot, fill, alpha=255):
    """Скруглённый прямоугольник, повёрнутый на ang° вокруг pivot."""
    pts = rotpts(rrect_pts(*box, r), pivot[0], pivot[1], ang)
    c.poly(pts, fill, alpha=alpha)
    return pts


def arrow_line(c, p0, p1, col, w=4, head=16, both=True):
    c.line([p0, p1], col, w)
    ang = math.atan2(p1[1] - p0[1], p1[0] - p0[0])
    ends = ((p1, ang), (p0, ang + math.pi)) if both else ((p1, ang),)
    for (x, y), a in ends:
        c.poly([(x, y), (x - head * math.cos(a - 0.45), y - head * math.sin(a - 0.45)),
                (x - head * math.cos(a + 0.45), y - head * math.sin(a + 0.45))], col)


def head(c, t, p, y=42, size=60, font="mxb", maxw=980, lines=2, sub_size=31, align="center", x=None, gap=1.1):
    """Заголовок: title (+ title2 акцентом) + sub. Возвращает нижний y."""
    y = c.block(t["title"], font, t.get("size", size), y, maxw, p["ink"], max_lines=t.get("lines", lines), gap=gap,
                align=align, x=x)
    if t.get("title2"):
        y = c.block(t["title2"], font, int(t.get("size", size) * t.get("t2k", 0.9)), y + 2, maxw, p.get("t2", p["acc"]),
                    max_lines=t.get("lines2", 1), gap=gap, align=align, x=x)
    if t.get("sub"):
        y = c.block(t["sub"], "msb", t.get("sub_size", sub_size), y + 12, maxw, p["sub"], max_lines=2, align=align, x=x)
    return y


def block_h(c, text, font, size, maxw, max_lines, gap=1.16):
    size = c.fit(text, font, maxw, max_lines, size)
    return len(c.wrap(text, c.font(font, size), maxw)) * c.lh(font, size, gap)


def head_h(c, t, size, maxw, lines=2, sub_size=31, gap=1.1):
    h = block_h(c, t["title"], "mxb", t.get("size", size), maxw, t.get("lines", lines), gap)
    if t.get("title2"):
        h += 2 + block_h(c, t["title2"], "mxb", int(t.get("size", size) * t.get("t2k", 0.9)), maxw, t.get("lines2", 1), gap)
    if t.get("sub"):
        h += 12 + block_h(c, t["sub"], "msb", t.get("sub_size", sub_size), maxw, 2)
    return h


def bg(c, p):
    if p.get("bg2"):
        c.vgrad((0, 0, W, W), p["bg"], p["bg2"])


def cta_btn(c, P, cx, cy, size=42, fill=None, color=WH, **kw):
    p = P["pal"]
    return c.button(P["cta"], cx, cy, name="mb", size=size, fill=fill or p["btn"], color=color, **kw)


def cta_pill(c, P, cx, cy, size=21, fill=None, padx=18, pady=10, min_w=0):
    p = P["pal"]
    return c.pill(P["cta"], cx, cy, size=size, fill=fill or p["btn"], padx=padx, pady=pady, name="mb", min_w=min_w)


def pill_w(c, P, size=21, padx=18):
    fnt = c.font("mb", size)
    return c.tw(P["cta"] + "  →", fnt)[0] + 2 * padx


# =====================================================================  РАСКЛАДКИ
def row4_hero(P, t):
    """Товарка-сетка: заголовок + «фото» товара + 4 плитки-варианта в ряд (мини-рисунок, крупная подпись), у каждой кнопка."""
    p = P["pal"]
    c = C(p["bg"])
    bg(c, p)
    y = head(c, t, p, size=t.get("size", 58))
    hb = (50, y + 22, 1030, y + 22 + t.get("hero_h", 330))
    t["hero"](c, hb)
    top = hb[3] + 24
    g = 16
    tw = (980 - 3 * g) / 4
    bot = 1044
    for i, (lab, sub) in enumerate(t["tiles"]):
        x0 = 50 + i * (tw + g)
        box = (x0, top, x0 + tw, bot)
        c.card(box, fill=p["tile"], r=24, sh_alpha=55, blur=12, off=(0, 6), outline=p.get("tile_line"), width=2 if p.get("tile_line") else 0)
        cx = x0 + tw / 2
        th = bot - top
        t["tile_art"](c, cx, top + th * 0.3, min(tw * 0.98, th * 0.46), i)
        c.text((cx, top + th * 0.63), lab, "mxb", t.get("lab_size", 46), p["tile_ink"], anchor="mm")
        if sub:
            c.block(sub, "msb", 22, top + th * 0.7, tw - 20, p["sub"], cx=cx, max_lines=1)
        cta_pill(c, P, cx, bot - 38, size=t.get("pill_size", 19), padx=14, pady=10)
    return c


def grid2x2_art(P, t):
    """2×2 плитки: панель-рисунок, название, строка конкретики, кнопка."""
    p = P["pal"]
    c = C(p["bg"])
    bg(c, p)
    y = head(c, t, p, size=t.get("size", 58))
    top = y + 26
    g = 20
    tw = (980 - g) / 2
    th = (1046 - top - g) / 2
    for i, (art, name, sub) in enumerate(t["tiles"]):
        x0 = 50 + (i % 2) * (tw + g)
        y0 = top + (i // 2) * (th + g)
        box = (x0, y0, x0 + tw, y0 + th)
        c.card(box, fill=p["tile"], r=26, sh_alpha=55, blur=12, off=(0, 6))
        ab = (x0 + 12, y0 + 12, x0 + tw - 12, y0 + th * t.get("art_k", 0.5))
        art(c, ab)
        ty = ab[3] + 12
        if t.get("badge"):
            bl = t["badge"][i]
            bw = c.tw(bl, c.font("mxb", 30))[0] + 30
            c.rect((ab[0] + 14, ab[1] + 14, ab[0] + 14 + bw, ab[1] + 64), fill=p["acc"], r=14)
            c.text((ab[0] + 14 + bw / 2, ab[1] + 39), bl, "mxb", 30, WH, anchor="mm")
        ns = c.fit(name, "mxb", tw - 40, 1, t.get("name_size", 34))
        c.text((x0 + 24, ty), name, "mxb", ns, p["tile_ink"])
        ty += c.lh("mxb", ns, 1.12)
        if sub:
            c.block(sub, "msb", t.get("sub_size", 23), ty, tw - 48, p["sub"], align="left", x=x0 + 24, max_lines=2, gap=1.08)
        pw = pill_w(c, P, 20, 16)
        cta_pill(c, P, x0 + 24 + pw / 2, y0 + th - 34, size=20, padx=16, pady=9)
    return c


def poll3(P, t):
    """Карточка-опрос: 3 варианта строками (рисунок слева, название + описание, радиокнопка справа)."""
    p = P["pal"]
    c = C(p["bg"])
    bg(c, p)
    if p.get("deco"):
        c.ellipse((760, -160, 1260, 340), fill=WH, alpha=26)
        c.ellipse((-200, 800, 260, 1240), fill=WH, alpha=20)
    y = head(c, t, p, size=t.get("size", 56))
    box = (60, y + 24, 1020, t.get("card_bot", 910))
    c.card(box, r=34, sh_alpha=110, blur=22)
    x0, x1 = box[0] + 40, box[2] - 40
    yy = box[1] + 34
    c.text((x0, yy), t["tag"], "mb", 24, p["acc"])
    c.text((x1, yy), t["step"], "msb", 24, (120, 120, 126), anchor="ra")
    c.rect((x0, yy + 42, x1, yy + 54), fill=(232, 228, 222), r=6)
    c.rect((x0, yy + 42, x0 + (x1 - x0) * t.get("prog", 0.33), yy + 54), fill=p["acc"], r=6)
    yy += 78
    yy = c.block(t["q"], "mxb", t.get("q_size", 36), yy, x1 - x0, (40, 36, 34), align="left", x=x0, max_lines=2, gap=1.1)
    yy += 14
    n = len(t["opts"])
    gap = 14
    oh = (box[3] - 30 - yy - (n - 1) * gap) / n
    for k, (art, name, desc) in enumerate(t["opts"]):
        ob = (x0, yy, x1, yy + oh)
        c.rect(ob, fill=p.get("opt", (250, 247, 243)), r=22, outline=p.get("opt_line", (222, 214, 204)), width=3)
        ib = (ob[0] + 10, ob[1] + 10, ob[0] + 10 + oh * 1.35, ob[3] - 10)
        c.rect(ib, fill=p.get("iconbg", (240, 232, 222)), r=16)
        art(c, ib)
        tx = ib[2] + 26
        c.text((tx, ob[1] + oh * 0.2), name, "mxb", 34, p["ink"])
        c.block(desc, "msb", 25, ob[1] + oh * 0.2 + 48, ob[2] - 90 - tx, p["sub"], align="left", x=tx, max_lines=2, gap=1.06)
        c.circle(ob[2] - 46, (ob[1] + ob[3]) / 2, 20, fill=WH, outline=(170, 160, 150), width=3)
        yy += oh + gap
    if t.get("foot"):
        c.block(t["foot"], "mb", 28, box[3] + 16, 960, p["ink"], max_lines=1, highlight=p.get("hl"), hl_pad=8)
    cta_btn(c, P, W / 2, t.get("btn_y", 992))
    return c


def quiz_art(P, t):
    """Квиз: заголовок, карточка с рисунком-условием, вопрос и варианты (A/B/C/D) в ряд или 2×2, кнопка."""
    p = P["pal"]
    c = C(p["bg"])
    bg(c, p)
    if p.get("deco"):
        c.ellipse((780, -170, 1260, 320), fill=WH, alpha=24)
        c.ellipse((-220, 820, 240, 1260), fill=WH, alpha=18)
    y = head(c, t, p, size=t.get("size", 56))
    box = (56, y + 22, 1024, t.get("card_bot", 912))
    c.card(box, r=34, sh_alpha=110, blur=22, fill=p.get("card", WH))
    x0, x1 = box[0] + 36, box[2] - 36
    yy = box[1] + 30
    c.text((x0, yy), t["tag"], "mb", 24, p["acc"])
    c.text((x1, yy), t["step"], "msb", 24, (120, 124, 130), anchor="ra")
    c.rect((x0, yy + 40, x1, yy + 52), fill=(228, 232, 236), r=6)
    c.rect((x0, yy + 40, x0 + (x1 - x0) * t.get("prog", 0.33), yy + 52), fill=p["acc"], r=6)
    yy += 70
    ah = t.get("art_h", 250)
    ab = (x0, yy, x1, yy + ah)
    t["art"](c, ab)
    yy = ab[3] + 18
    yy = c.block(t["q"], "mxb", t.get("q_size", 34), yy, x1 - x0, (34, 38, 46), align="left", x=x0, max_lines=2, gap=1.1)
    yy += 12
    opts = t["opts"]
    lay = t.get("opt_layout", "2x2")
    bottom = box[3] - 28
    if lay == "row":
        n = len(opts)
        g = 16
        ow = (x1 - x0 - (n - 1) * g) / n
        oh = bottom - yy
        for k, o in enumerate(opts):
            ox = x0 + k * (ow + g)
            ob = (ox, yy, ox + ow, yy + oh)
            c.rect(ob, fill=p.get("opt", (244, 247, 249)), r=20, outline=p.get("opt_line", (206, 214, 220)), width=3)
            c.circle(ox + 36, yy + oh / 2, 20, fill=p["acc"])
            c.text((ox + 36, yy + oh / 2), "ABCD"[k], "mxb", 22, WH, anchor="mm")
            fs = c.fit(o, "mxb", ow - 80, 1, t.get("opt_size", 34))
            c.text((ox + 66 + (ow - 66) / 2 - 6, yy + oh / 2), o, "mxb", fs, (40, 44, 52), anchor="mm")
    elif lay == "list":
        n = len(opts)
        g = 12
        oh = (bottom - yy - (n - 1) * g) / n
        for k, o in enumerate(opts):
            ob = (x0, yy, x1, yy + oh)
            c.rect(ob, fill=p.get("opt", (244, 247, 249)), r=oh / 2, outline=p.get("opt_line", (206, 214, 220)), width=3)
            c.circle(x0 + oh / 2 + 4, yy + oh / 2, oh * 0.3, fill=p["acc"])
            c.text((x0 + oh / 2 + 4, yy + oh / 2), "ABCD"[k], "mxb", int(oh * 0.3), WH, anchor="mm")
            fs = c.fit(o, "mb", x1 - x0 - oh - 40, 1, t.get("opt_size", 30))
            c.text((x0 + oh + 20, yy + oh / 2), o, "mb", fs, (40, 44, 52), anchor="lm")
            yy += oh + g
    else:
        g = 16
        ow = (x1 - x0 - g) / 2
        oh = (bottom - yy - g) / 2
        for k, o in enumerate(opts):
            ox = x0 + (k % 2) * (ow + g)
            oy = yy + (k // 2) * (oh + g)
            c.rect((ox, oy, ox + ow, oy + oh), fill=p.get("opt", (244, 247, 249)), r=20, outline=p.get("opt_line", (206, 214, 220)), width=3)
            c.circle(ox + 38, oy + oh / 2, 21, fill=p["acc"])
            c.text((ox + 38, oy + oh / 2), "ABCD"[k], "mxb", 22, WH, anchor="mm")
            fs = t.get("opt_size", 27)
            while fs > 18 and len(c.wrap(o, c.font("mb", fs), ow - 90)) > 2:
                fs -= 1
            nl = len(c.wrap(o, c.font("mb", fs), ow - 90))
            c.block(o, "mb", fs, oy + oh / 2 - nl * c.lh("mb", fs, 1.06) / 2 + 2, ow - 90, (40, 44, 52), align="left",
                    x=ox + 72, max_lines=2, gap=1.06)
    cta_btn(c, P, W / 2, t.get("btn_y", 988))
    return c


def vs2(P, t):
    """Сравнение двух вариантов: две карточки с рисунком сверху, лента с названием, строки «метка — текст», VS, кнопка."""
    p = P["pal"]
    c = C(p["bg"])
    bg(c, p)
    y = head(c, t, p, size=t.get("size", 58))
    top = y + 26
    bot = t.get("bot", 846 if t.get("foot") else 900)
    g = 24
    cw = (980 - g) / 2
    ah = t.get("art_h", 250)
    # общая сетка строк: высота строки = максимум по двум колонкам
    ry0 = top + 12 + ah + 12 + 62 + 18
    nrows = len(t["cols"][0][3])
    fs = t.get("row_size", 27)
    while True:
        hs = []
        for j in range(nrows):
            nl = max(len(c.wrap(col_[3][j][1], c.font("mb", fs), cw - 56)) for col_ in t["cols"])
            hs.append(28 + nl * c.lh("mb", fs, 1.05))
        if ry0 + sum(hs) + 14 * (nrows - 1) <= bot - 16 or fs <= 20:
            break
        fs -= 1
    spare = max(0, (bot - 16 - ry0 - sum(hs)) / max(1, nrows - 1))
    spare = min(spare, 44)
    for k, (name, col, art, rows) in enumerate(t["cols"]):
        x0 = 50 + k * (cw + g)
        box = (x0, top, x0 + cw, bot)
        c.card(box, fill=mix(col, WH, 0.92), r=28, sh_alpha=55, blur=12, off=(0, 6))
        ab = (x0 + 12, top + 12, x0 + cw - 12, top + 12 + ah)
        art(c, ab)
        by = ab[3] + 12
        c.rect((x0 + 12, by, x0 + cw - 12, by + 62), fill=col, r=16)
        c.text((x0 + cw / 2, by + 31), name, "mxb", c.fit(name, "mxb", cw - 50, 1, 32), WH, anchor="mm")
        yy = ry0
        for j, (lab, txt) in enumerate(rows):
            if j:
                c.line([(x0 + 28, yy - spare / 2 - 2), (x0 + cw - 28, yy - spare / 2 - 2)], mix(col, WH, 0.7), 2)
            c.text((x0 + 28, yy), lab, "mb", 19, col)
            c.block(txt, "mb", fs, yy + 26, cw - 56, (36, 38, 44), align="left", x=x0 + 28, max_lines=3, gap=1.05)
            yy += hs[j] + spare
    cy = top + 12 + ah / 2
    c.circle(W / 2, cy, 40, fill=WH, outline=mix(p["ink"], WH, 0.7), width=3)
    c.text((W / 2, cy), "vs", "mxb", 28, p["ink"], anchor="mm")
    if t.get("foot"):
        c.block(t["foot"], "mb", t.get("foot_size", 30), bot + 20, 990, p["ink"], max_lines=1, highlight=p.get("hl"), hl_pad=8)
    cta_btn(c, P, W / 2, t.get("btn_y", 984))
    return c


def callouts_scene(P, t):
    """Сцена на весь кадр + заголовок + пронумерованные сноски с линиями к деталям + кнопка."""
    p = P["pal"]
    c = C(p["bg"])
    t["scene"](c)
    y = t.get("y", 40)
    if t.get("veil"):
        vb = t["veil"]
        c.shadow(vb, r=26, alpha=70, blur=16, off=(0, 8))
        c.rect(vb, fill=WH, r=26, alpha=t.get("veil_alpha", 240))
    y = head(c, t, p, y=y, size=t.get("size", 56))
    for k, (lab, anchor, bx, by, side) in enumerate(t["callouts"]):
        fs = t.get("co_size", 26)
        maxw = t.get("co_w", 300)
        lines = c.wrap(lab, c.font("mb", fs), maxw - 70)
        while len(lines) > 2 and fs > 18:
            fs -= 1
            lines = c.wrap(lab, c.font("mb", fs), maxw - 70)
        lw_ = max(c.tw(l, c.font("mb", fs))[0] for l in lines)
        bw = lw_ + 84
        bh = 26 + len(lines) * c.lh("mb", fs, 1.05)
        x0 = bx if side == "l" else bx - bw
        bb = (x0, by - bh / 2, x0 + bw, by + bh / 2)
        ax, ay = anchor
        ex = bb[2] if side == "l" else bb[0]
        c.line([(ex, by), (ax, ay)], p["acc"], 4)
        c.circle(ax, ay, 10, fill=p["acc"], outline=WH, width=3)
        c.card(bb, fill=WH, r=min(bh / 2, 26), sh_alpha=60, blur=8, off=(0, 4))
        c.circle(bb[0] + 34, by, 20, fill=p["acc"])
        c.text((bb[0] + 34, by + 1), str(k + 1), "mxb", 22, WH, anchor="mm")
        c.block(lab, "mb", fs, by - len(lines) * c.lh("mb", fs, 1.05) / 2 + 2, maxw - 70, p["ink"], align="left", x=bb[0] + 64,
                max_lines=2, gap=1.05)
    cta_btn(c, P, t.get("btn_x", W / 2), t.get("btn_y", 996), size=t.get("btn_size", 42))
    return c


def top_scene(P, t):
    """Сцена на весь кадр + карточка-заголовок (сверху или снизу) + кнопка; опционально — полоса чипов."""
    p = P["pal"]
    c = C(p["bg"])
    t["scene"](c)
    if t.get("card_box"):
        box = list(t["card_box"])
        pad = t.get("pad", 40)
        maxw = box[2] - box[0] - 90
        tt = dict(t)
        tt.pop("kicker", None)
        ch = pad + (33 if t.get("kicker") else 0) + head_h(c, tt, t.get("size", 54), maxw)
        bh = c.lh("mb", t.get("btn_size", 40), 1.0) + 44
        if t.get("btn_in_card", True):
            box[3] = box[1] + ch + 26 + bh + pad - 6
        c.shadow(box, r=28, alpha=100, blur=18, off=(0, 10))
        c.rect(box, fill=p.get("card", WH), r=28, alpha=t.get("card_alpha", 246))
        if t.get("frame"):
            c.rect((box[0] + 14, box[1] + 14, box[2] - 14, box[3] - 14), outline=p["acc"], width=3, r=18)
        cx = (box[0] + box[2]) / 2
        y = box[1] + pad
        if t.get("kicker"):
            y = c.block(t["kicker"], "mb", 25, y, box[2] - box[0] - 100, p["acc"], cx=cx, max_lines=1) + 4
        y = head(c, tt, p, y=y, size=t.get("size", 54), maxw=maxw)
        if t.get("btn_in_card", True):
            cta_btn(c, P, cx, y + 26 + bh / 2, size=t.get("btn_size", 40))
    else:
        y = head(c, t, p, y=t.get("y", 40), size=t.get("size", 56))
    if t.get("chips"):
        t["chips"](c, P)
    if not t.get("card_box") or not t.get("btn_in_card", True):
        cta_btn(c, P, t.get("btn_x", W / 2), t.get("btn_y", 996), size=t.get("btn_size", 42))
    return c


FN = {"route_map": lambda P, t: route_map(P, t), "row4_hero": row4_hero, "grid2x2_art": grid2x2_art, "poll3": poll3, "quiz_art": quiz_art, "vs2": vs2,
      "callouts_scene": callouts_scene, "top_scene": top_scene}


# =====================================================================  1. IT · товарка · мебель для ванной и кресла
WOOD1 = (190, 138, 92)
WOOD1D = (150, 104, 66)
TERRA1 = (186, 84, 52)
SAGE1 = (126, 150, 118)
INK1 = (46, 38, 34)


def wall_tiles(t, box, base=(238, 233, 225), grout=(222, 214, 204), tw=70, th=36):
    x0, y0, x1, y1 = box
    t.rect(box, fill=grout)
    row = 0
    y = y0
    while y < y1:
        x = x0 - (tw / 2 if row % 2 else 0)
        while x < x1:
            t.rect((x + 2, y + 2, x + tw - 2, y + th - 2), fill=base, r=2)
            x += tw
        y += th
        row += 1


def faucet(t, cx, base_y, s, col=(150, 156, 166)):
    t.rect((cx - 5 * s, base_y - 40 * s, cx + 5 * s, base_y), fill=col, r=3 * s)
    t.rect((cx - 5 * s, base_y - 40 * s, cx + 22 * s, base_y - 32 * s), fill=col, r=3 * s)
    t.rect((cx - 12 * s, base_y - 30 * s, cx - 4 * s, base_y - 24 * s), fill=col, r=2 * s)


def vanity(t, cx, top_y, w, h, kind="hung", sinks=1, wood=WOOD1, woodd=WOOD1D, floor_y=None, drawers=2):
    """Тумба с раковиной: kind 'hung' (подвесная) или 'floor' (напольная на цоколе)."""
    x0, x1 = cx - w / 2, cx + w / 2
    if kind == "hung":
        t.rect((x0 + 8, top_y + h + 2, x1 - 8, top_y + h + 16), fill=(0, 0, 0), alpha=28)
    body_bot = top_y + h if kind == "hung" else floor_y - 14
    t.rect((x0, top_y, x1, body_bot), fill=wood, r=4)
    # фасады-ящики
    dh = (body_bot - top_y - 22) / drawers
    for k in range(drawers):
        yy = top_y + 18 + k * dh
        t.rect((x0 + 8, yy, x1 - 8, yy + dh - 6), fill=mix(wood, WH, 0.06), r=3)
        t.line([(x0 + 8, yy + dh - 6), (x1 - 8, yy + dh - 6)], woodd, 2)
        t.rect((cx - w * 0.12, yy + 10, cx + w * 0.12, yy + 16), fill=(70, 62, 56), r=3)
    if kind == "floor":
        t.rect((x0 + 10, body_bot, x1 - 10, floor_y), fill=woodd)
    # столешница + раковины
    t.rect((x0 - 8, top_y - 14, x1 + 8, top_y + 4), fill=(248, 247, 244), r=4)
    t.line([(x0 - 8, top_y + 4), (x1 + 8, top_y + 4)], (214, 210, 204), 2)
    for k in range(sinks):
        scx = cx if sinks == 1 else cx + (k - 0.5) * w * 0.5
        bw = min(w * 0.42, 150) if sinks == 1 else w * 0.3
        t.ellipse((scx - bw / 2, top_y - 40, scx + bw / 2, top_y - 4), fill=(250, 250, 250), outline=(214, 210, 204), width=2)
        t.ellipse((scx - bw * 0.38, top_y - 34, scx + bw * 0.38, top_y - 18), fill=(228, 230, 232))
        faucet(t, scx, top_y - 30, 0.9 if sinks == 1 else 0.7)


def mirror(t, cx, cy, r, frame=WOOD1D):
    t.circle(cx, cy, r + 8, fill=frame)
    t.circle(cx, cy, r, fill=(214, 228, 232))
    t.poly([(cx - r * 0.5, cy - r * 0.2), (cx - r * 0.2, cy - r * 0.6), (cx - r * 0.05, cy - r * 0.45), (cx - r * 0.35, cy - r * 0.05)],
           (240, 248, 250), alpha=160)


def towel(t, x, y, w, h, col=(214, 150, 120)):
    t.circle(x + w / 2, y - 8, 7, fill=(150, 156, 166))
    t.rect((x, y, x + w, y + h), fill=col, r=8)
    t.rect((x, y + h - 22, x + w, y + h - 14), fill=mix(col, WH, 0.4))


def hero_bath(c, box):
    """Светлая ванная: подвесная деревянная тумба, круглое зеркало, плитка, свободный пол; стрелка ширины."""
    def fn(t):
        x0, y0, x1, y1 = box
        H = y1 - y0
        fl = y0 + H * 0.8
        wall_tiles(t, (x0, y0, x1, fl))
        t.rect((x0, fl, x1, y1), fill=(214, 200, 182))
        for k in range(8):
            t.line([(x0 + k * 140 - 40, y1), (x0 + k * 140 + 30, fl)], (200, 186, 168), 3)
        t.rect((x0, fl - 6, x1, fl + 4), fill=(206, 194, 178))
        cx = x0 + (x1 - x0) * 0.46
        vw, vt, vh = 360, y0 + H * 0.5, H * 0.22
        mirror(t, cx, y0 + H * 0.2, H * 0.15)
        vanity(t, cx, vt, vw, vh, "hung")
        # стрелка ширины над полом, под тумбой
        ay = vt + vh + 34
        arrow_line(t, (cx - vw / 2, ay), (cx + vw / 2, ay), TERRA1, 4, 16)
        t.line([(cx - vw / 2, ay - 16), (cx - vw / 2, ay + 16)], TERRA1, 4)
        t.line([(cx + vw / 2, ay - 16), (cx + vw / 2, ay + 16)], TERRA1, 4)
        # полка, растение, полотенце
        S.plant(t, x1 - 110, fl + 10, 0.62, pot=(236, 232, 226), leaf=(92, 140, 100))
        towel(t, x0 + 90, y0 + H * 0.36, 80, 120)
        t.rect((x1 - 250, y0 + H * 0.3, x1 - 60, y0 + H * 0.3 + 12), fill=WOOD1D, r=3)
        for k, (hh, col) in enumerate(((50, (236, 226, 214)), (70, (170, 196, 186)), (40, (226, 170, 140)))):
            bx = x1 - 230 + k * 55
            t.rect((bx, y0 + H * 0.3 - hh, bx + 38, y0 + H * 0.3), fill=col, r=6)
    S.clip_draw(c, box, 24, fn)


def mini_vanity(c, cx, cy, s, i):
    widths = (60, 80, 100, 120)
    wcm = widths[i]
    w = s * (0.42 + 0.58 * (wcm - 60) / 60)
    sinks = 2 if wcm == 120 else 1
    h = s * 0.34
    top = cy - h * 0.2
    x0, x1 = cx - w / 2, cx + w / 2
    c.rect((x0, top, x1, top + h), fill=WOOD1, r=4)
    c.rect((x0 + 5, top + 10, x1 - 5, top + h / 2 - 2), fill=mix(WOOD1, WH, 0.08), r=3)
    c.rect((x0 + 5, top + h / 2 + 2, x1 - 5, top + h - 6), fill=mix(WOOD1, WH, 0.08), r=3)
    for yy in (top + h * 0.3, top + h * 0.72):
        c.rect((cx - w * 0.12, yy - 3, cx + w * 0.12, yy + 3), fill=(70, 62, 56), r=3)
    c.rect((x0 - 5, top - 9, x1 + 5, top + 3), fill=(236, 234, 230), r=3)
    for k in range(sinks):
        scx = cx if sinks == 1 else cx + (k - 0.5) * w * 0.5
        bw = s * 0.26
        c.ellipse((scx - bw / 2, top - 30, scx + bw / 2, top - 4), fill=(246, 246, 246), outline=(200, 196, 190), width=2)
        c.rect((scx - 3, top - 44, scx + 3, top - 26), fill=(150, 156, 166), r=2)
        c.rect((scx - 3, top - 44, scx + 12, top - 39), fill=(150, 156, 166), r=2)
    # стрелка ширины
    ay = top + h + 20
    arrow_line(c, (x0, ay), (x1, ay), TERRA1, 3, 10)


def recliner(t, x, fy, s, state="upright", col=SAGE1):
    """Кресло-релакс сбоку, лицом вправо. x — центр кресла, fy — пол, s — высота кресла.
    state: 'upright' | 'reclined' (спинка назад + подножка) | 'lift' (корпус приподнят и наклонён вперёд)."""
    dk = mix(col, (0, 0, 0), 0.2)
    lt = mix(col, WH, 0.14)
    ang = 0
    lift_dy = 0
    if state == "lift":
        ang, lift_dy = 20, -s * 0.1
    piv = (x + s * 0.34, fy - s * 0.1)

    def P(box, r, fill, extra=0, epiv=None):
        x0, y0, x1, y1 = box
        pts = rrect_pts(x0, y0 + lift_dy, x1, y1 + lift_dy, r)
        if extra:
            ep = epiv or piv
            pts = rotpts(pts, ep[0], ep[1] + lift_dy, extra)
        if ang:
            pts = rotpts(pts, piv[0], piv[1] + lift_dy, ang)
        t.poly(pts, fill)

    # основание
    t.rect((x - s * 0.3, fy - s * 0.07, x + s * 0.3, fy), fill=(84, 76, 70), r=s * 0.025)
    if state == "lift":
        for a0, a1 in (((-0.24, 0), (0.14, -0.2)), ((0.2, 0), (-0.16, -0.22))):
            t.line([(x + a0[0] * s, fy - s * 0.07), (x + a1[0] * s, fy - s * 0.07 + a1[1] * s)], (120, 112, 104), s * 0.03)
    # спинка (за подлокотником)
    bpiv = (x - s * 0.26, fy - s * 0.42)
    back_ang = -12 if state != "reclined" else -42
    P((x - s * 0.4, fy - s * 1.0, x - s * 0.14, fy - s * 0.3), s * 0.09, dk, back_ang, bpiv)
    P((x - s * 0.34, fy - s * 0.97, x - s * 0.1, fy - s * 0.78), s * 0.08, lt, back_ang, bpiv)
    # сиденье
    P((x - s * 0.24, fy - s * 0.5, x + s * 0.38, fy - s * 0.38), s * 0.05, col)
    # подножка
    if state == "reclined":
        P((x + s * 0.3, fy - s * 0.44, x + s * 0.74, fy - s * 0.32), s * 0.05, dk, -8, (x + s * 0.3, fy - s * 0.38))
    # корпус-подлокотник (боковина) + вставка-обивка
    P((x - s * 0.3, fy - s * 0.64, x + s * 0.34, fy - s * 0.08), s * 0.1, col)
    if s > 300:
        P((x - s * 0.25, fy - s * 0.5, x + s * 0.29, fy - s * 0.13), s * 0.07, mix(col, WH, 0.06))
    P((x - s * 0.3, fy - s * 0.66, x + s * 0.36, fy - s * 0.54), s * 0.06, lt)


def _recl_fit(box, wk=1.5):
    x0, y0, x1, y1 = box
    s = min((y1 - y0) * 0.8, (x1 - x0) / wk)
    return s, (x0 + x1) / 2, y1 - (y1 - y0) * 0.1


def recliner_manual(c, box):
    s, cx, fy = _recl_fit(box)
    x = cx - s * 0.05
    recliner(c, x, fy, s, "reclined")
    c.line([(x + s * 0.12, fy - s * 0.36), (x + s * 0.02, fy - s * 0.2)], (60, 56, 52), s * 0.04)
    c.circle(x + s * 0.13, fy - s * 0.37, s * 0.045, fill=TERRA1)


def recliner_electric(c, box):
    s, cx, fy = _recl_fit(box)
    x = cx - s * 0.12
    recliner(c, x, fy, s, "reclined")
    px = box[2] - 16
    c.line([(x - s * 0.24, fy - s * 0.04), (x - s * 0.3, fy - 3), (px - 8, fy - 3), (px - 8, fy - s * 0.18)], (60, 56, 52), 3)
    c.rect((px - 20, fy - s * 0.32, px + 4, fy - s * 0.16), fill=WH, r=5, outline=(170, 164, 156), width=2)
    c.circle(px - 8, fy - s * 0.24, 3, fill=(90, 86, 80))
    bx, by = x + s * 0.02, fy - s * 0.98
    k = s / 130
    c.poly([(bx, by), (bx - 12 * k, by + 22 * k), (bx - 2 * k, by + 22 * k), (bx - 8 * k, by + 42 * k), (bx + 12 * k, by + 14 * k),
            (bx + 2 * k, by + 14 * k), (bx + 8 * k, by)], (236, 150, 40))


def recliner_lift(c, box):
    s, cx, fy = _recl_fit(box, 1.3)
    x = cx - s * 0.12
    recliner(c, x, fy, s, "lift")
    arrow_line(c, (x + s * 0.62, fy - s * 0.25), (x + s * 0.62, fy - s * 0.75), TERRA1, 4, 12, both=False)


def vanity_panel(kind):
    def art(c, box):
        def fn(t):
            x0, y0, x1, y1 = box
            H = y1 - y0
            fl = y0 + H * 0.8
            wall_tiles(t, (x0, y0, x1, fl), tw=56, th=30)
            t.rect((x0, fl, x1, y1), fill=(214, 200, 182))
            t.rect((x0, fl - 5, x1, fl + 3), fill=(206, 194, 178))
            cx = (x0 + x1) / 2
            mirror(t, cx, y0 + H * 0.17, H * 0.1)
            if kind == "hung":
                vanity(t, cx, y0 + H * 0.48, 250, H * 0.2, "hung")
                # швабра под тумбой: свободный пол
                t.line([(cx + 30, fl + 6), (cx + 170, y0 + H * 0.5)], (170, 120, 70), 6)
                t.rect((cx - 10, fl - 2, cx + 64, fl + 14), fill=(120, 170, 200), r=5)
            else:
                vanity(t, cx, y0 + H * 0.48, 250, 0, "floor", floor_y=fl, drawers=3)
        S.clip_draw(c, box, 20, fn)
    return art


def hero_living_chair(c):
    """Гостиная: стена, окно со светом, торшер, растение, большое кресло-релакс сбоку (для сносок-размеров)."""
    c.vgrad((0, 0, W, W), (242, 234, 222), (236, 226, 212))
    fl = 900
    c.rect((0, fl, W, W), fill=(206, 170, 128))
    for k in range(12):
        c.line([(k * 100 - 30, W), (k * 100 + 10, fl)], (192, 156, 116), 3)
    c.rect((0, fl - 10, W, fl + 2), fill=(250, 246, 240))
    # окно справа
    wx0, wy0, wx1, wy1 = 800, 300, 1040, 700
    c.rect((wx0 - 12, wy0 - 12, wx1 + 12, wy1 + 12), fill=(250, 248, 244), r=6)
    c.vgrad((wx0, wy0, wx1, wy1), (196, 222, 236), (234, 242, 246))
    c.rect(((wx0 + wx1) / 2 - 5, wy0, (wx0 + wx1) / 2 + 5, wy1), fill=(250, 248, 244))
    c.rect((wx0, (wy0 + wy1) / 2 - 5, wx1, (wy0 + wy1) / 2 + 5), fill=(250, 248, 244))
    c.poly([(wx0, wy1 + 12), (wx1, wy1 + 12), (wx1 - 80, fl), (wx0 - 200, fl)], (255, 250, 230), alpha=60)
    S.plant(c, 960, fl + 6, 0.9, pot=(236, 232, 226), leaf=(92, 140, 100))
    # торшер слева
    c.line([(90, fl - 4), (90, 430)], (60, 56, 52), 8)
    c.ellipse((50, fl - 14, 130, fl + 4), fill=(60, 56, 52))
    c.poly([(40, 430), (140, 430), (120, 350), (60, 350)], (236, 214, 170))
    c.glow((20, 360, 160, 520), (255, 236, 180), alpha=90, blur=30)


def chair_measure_scene(c):
    hero_living_chair(c)
    fl, x, sz = 900, 420, 560
    c.ellipse((180, fl - 10, 800, fl + 44), fill=(226, 206, 180), alpha=170)
    recliner(c, x, fl, sz, "upright", col=TERRA1)
    # высота сиденья — спереди
    sx, seat_top = x + sz * 0.46, fl - sz * 0.5
    for yy in (seat_top, fl):
        c.line([(sx - 16, yy), (sx + 16, yy)], INK1, 4)
    c.line([(x + sz * 0.38, seat_top), (sx - 16, seat_top)], INK1, 2, alpha=150)
    arrow_line(c, (sx, seat_top + 4), (sx, fl - 4), INK1, 4, 14)
    # глубина сиденья — над подлокотником
    dy = fl - sz * 0.74
    xa, xb = x - sz * 0.14, x + sz * 0.38
    arrow_line(c, (xa + 4, dy), (xb - 4, dy), INK1, 4, 14)
    for xx in (xa, xb):
        c.line([(xx, dy - 14), (xx, dy + 14)], INK1, 4)


P1 = dict(bg=(247, 241, 233), ink=INK1, sub=(112, 100, 92), acc=TERRA1, btn=(196, 70, 44), tile=WH, tile_ink=INK1,
          iconbg=(244, 234, 222))
PACKS[1] = dict(
    doc="NT-bathroom-furniture-it-2026-09-30", cta="Scopri di più", pal=P1,
    a=dict(fn="row4_hero", title="Mobile lavabo bagno 2026:", title2="quale larghezza?", size=60, hero=hero_bath, hero_h=340,
           tiles=[("60 cm", ""), ("80 cm", ""), ("100 cm", ""), ("120 cm", "doppio lavabo")], tile_art=mini_vanity,
           src="раздел «Mobile lavabo bagno: sospeso o a terra?» (самые частые ширины 60 / 80 / 100 / 120 см; двойная раковина 120–140 см)",
           note="товарка-сетка: «фото» светлой ванной с подвесной деревянной тумбой и стрелкой ширины + 4 плитки ширины с мини-тумбой (растёт с шириной, у 120 — две раковины), у каждой «Scopri di più»; без цен и бренда"),
    b=dict(fn="poll3", title="Poltrone reclinabili:", title2="manuale, elettrica o con alzata?", size=54, t2k=0.8,
           tag="SONDAGGIO", step="Domanda 1 di 3", q="Quale meccanismo scegliere?",
           opts=[(recliner_manual, "Manuale", "leva laterale o a spinta, senza cavi"),
                 (recliner_electric, "Elettrica", "1 o 2 motori, serve una presa vicina"),
                 (recliner_lift, "Con alzata", "solleva in avanti l'intera seduta")],
           foot="Salvaspazio: a 10–15 cm dal muro", card_bot=880, btn_y=1000,
           pal=dict(bg=(236, 226, 214), bg2=(226, 212, 196), hl=(255, 255, 255), deco=True),
           src="раздел «Poltrone reclinabili: manuali, elettriche o con alzata» (3 механизма + модели salvaspazio 10–15 см от стены)",
           note="опрос на 3 варианта механизма с рисунком кресла в каждом состоянии (рычаг / кабель к розетке / подъём сиденья); без медицинских обещаний и возраста"),
    c=dict(fn="vs2", title="Mobile bagno: sospeso o a terra?", sub="Cosa cambia, secondo la guida 2026", size=56,
           cols=[("SOSPESO", SAGE1, vanity_panel("hung"),
                  [("PAVIMENTO", "libero: pulizia più facile"), ("EFFETTO", "il bagno sembra più ampio"),
                   ("PARETE", "serve una parete solida")]),
                 ("A TERRA", WOOD1D, vanity_panel("floor"),
                  [("PAVIMENTO", "zoccolo o piedini"), ("SPAZIO", "contiene qualcosa in più"),
                   ("PARETE", "adatto a pareti leggere")])],
           foot="Sul cartongesso: rinforzi o tasselli specifici", art_h=270,
           src="раздел «Mobile lavabo bagno: sospeso o a terra?» (плюсы подвесной и напольной, parete solida, cartongesso)",
           note="две карточки: подвесная тумба со шваброй под ней vs напольная на цоколе; пункты — из статьи; без цен"),
    d=dict(fn="callouts_scene", scene=chair_measure_scene, title="Poltrona relax:", title2="le 4 misure da controllare",
           size=58, y=40,
           callouts=[("Schienale alto\ncon poggiatesta", (244, 411), 36, 262, "l"),
                     ("Profondità seduta:\n50–55 cm", (510, 486), 1044, 330, "r"),
                     ("Braccioli\nsolidi", (500, 540), 1044, 580, "r"),
                     ("Altezza seduta:\n42–48 cm", (678, 760), 736, 770, "l")],
           co_w=420, co_size=27, btn_y=1000,
           src="раздел «Poltrone: misure e rivestimenti per la poltrona relax giusta» (4 пункта: 42–48 см, 50–55 см, schienale alto, braccioli)",
           note="гостиная у окна, крупное кресло-релакс сбоку с размерными стрелками и 4 сносками; людей нет, без возраста"),
)


# =====================================================================  2. IT · товарка · бассейны
TEAL2 = (0, 128, 146)
INK2 = (14, 50, 66)
CORAL2 = (236, 92, 62)
WATER = ((70, 190, 214), (24, 140, 180))
GRASS = (132, 184, 104)


def garden_bg(t, box, horizon=0.55, sky=((196, 230, 246), (236, 246, 250)), hedge=True, seed=2):
    x0, y0, x1, y1 = box
    H = y1 - y0
    hz = y0 + H * horizon
    t.vgrad((x0, y0, x1, hz), sky[0], sky[1])
    if hedge:
        rnd = random.Random(seed)
        x = x0 - 30
        while x < x1 + 30:
            r = rnd.uniform(30, 56)
            t.circle(x, hz - r * 0.35, r, fill=(78, 138, 86))
            x += r * 1.2
        t.rect((x0, hz - 20, x1, hz), fill=(78, 138, 86))
    t.vgrad((x0, hz, x1, y1), (150, 198, 116), (118, 172, 94))


def water_ellipse(t, box):
    x0, y0, x1, y1 = box
    t.ellipse(box, fill=WATER[0])
    t.ellipse((x0 + (x1 - x0) * 0.08, y0 + (y1 - y0) * 0.25, x1 - (x1 - x0) * 0.04, y1), fill=mix(WATER[0], WATER[1], 0.35))
    for k in range(3):
        yy = y0 + (y1 - y0) * (0.35 + k * 0.18)
        xx = x0 + (x1 - x0) * (0.25 + 0.15 * k)
        t.arc((xx, yy - 8, xx + (x1 - x0) * 0.22, yy + 8), 200, 340, (220, 246, 250), 3)


def pool_round(t, cx, top_y, rx, ry, h, wall, rim, kind="rigid"):
    """Круглый наземный бассейн в перспективе: цилиндр высотой h, верхний эллипс (rx, ry)."""
    if kind == "inflatable":
        rb = rx * 1.12
        t.ellipse((cx - rb, top_y + h - ry * 1.1, cx + rb, top_y + h + ry * 1.1), fill=mix(wall, (0, 0, 0), 0.25), alpha=90)
        t.poly([(cx - rx, top_y), (cx + rx, top_y), (cx + rb, top_y + h), (cx - rb, top_y + h)], wall)
        t.pie((cx - rb, top_y + h - ry * 1.1, cx + rb, top_y + h + ry * 1.1), 0, 180, wall)
        water_ellipse(t, (cx - rx * 0.86, top_y - ry * 0.86, cx + rx * 0.86, top_y + ry * 0.86))
        # надувное кольцо
        t.ellipse((cx - rx * 1.06, top_y - ry * 1.18, cx + rx * 1.06, top_y + ry * 1.18), outline=rim, width=max(10, rx * 0.12))
        t.arc((cx - rx * 1.0, top_y - ry * 1.1, cx + rx * 1.0, top_y + ry * 1.1), 200, 330, mix(rim, WH, 0.5), max(3, rx * 0.03))
        return
    t.ellipse((cx - rx, top_y + h - ry, cx + rx, top_y + h + ry), fill=mix(wall, (0, 0, 0), 0.3), alpha=80)
    t.rect((cx - rx, top_y, cx + rx, top_y + h), fill=wall)
    t.pie((cx - rx, top_y + h - ry, cx + rx, top_y + h + ry), 0, 180, wall)
    if kind == "wood":
        n = 18
        for k in range(1, n):
            a = math.pi * k / n
            xx = cx - rx * math.cos(a)
            yb = top_y + h + ry * math.sin(a)
            t.line([(xx, top_y + 4), (xx, yb - 2)], mix(wall, (0, 0, 0), 0.22), 3)
    elif kind == "steel":
        for k in range(1, 8):
            a = math.pi * k / 8
            xx = cx - rx * math.cos(a)
            t.rect((xx - 5, top_y, xx + 5, top_y + h + ry * math.sin(a)), fill=mix(wall, (0, 0, 0), 0.12))
    # бортик и вода
    t.ellipse((cx - rx - 8, top_y - ry - 6, cx + rx + 8, top_y + ry + 6), fill=rim)
    water_ellipse(t, (cx - rx + 6, top_y - ry + 5, cx + rx - 6, top_y + ry - 4))


def pool_frame(t, x0, top_y, L, h, depth, wall=(214, 222, 228), tube=(90, 98, 110)):
    """Прямоугольный каркасный бассейн: передняя стенка, поверхность воды, трубы-стойки с опорами."""
    x1 = x0 + L
    dx, dy = depth * 0.45, depth * 0.55
    # поверхность воды (параллелограмм)
    t.poly([(x0, top_y), (x1, top_y), (x1 + dx, top_y - dy), (x0 + dx, top_y - dy)], WATER[1])
    t.poly([(x0 + 10, top_y - 4), (x1 - 4, top_y - 4), (x1 + dx - 8, top_y - dy + 4), (x0 + dx + 4, top_y - dy + 4)], WATER[0])
    for k in range(3):
        yy = top_y - dy * (0.3 + 0.2 * k)
        xx = x0 + dx * (0.3 + 0.2 * k) + L * (0.2 + 0.15 * k)
        t.arc((xx, yy - 6, xx + L * 0.18, yy + 6), 200, 340, (220, 246, 250), 3)
    # боковая стенка и передняя
    t.poly([(x1, top_y), (x1 + dx, top_y - dy), (x1 + dx, top_y - dy + h), (x1, top_y + h)], mix(wall, (0, 0, 0), 0.15))
    t.rect((x0, top_y, x1, top_y + h), fill=wall)
    # верхняя труба и стойки
    t.line([(x0 - 4, top_y), (x1 + 4, top_y), (x1 + dx + 2, top_y - dy)], tube, 10)
    t.line([(x0 + dx, top_y - dy), (x1 + dx, top_y - dy)], tube, 7)
    n = 5
    for k in range(n + 1):
        xx = x0 + L * k / n
        t.line([(xx, top_y), (xx, top_y + h + 6)], tube, 9)
        t.poly([(xx - 16, top_y + h + 12), (xx + 16, top_y + h + 12), (xx + 10, top_y + h + 2), (xx - 10, top_y + h + 2)], tube)
    t.line([(x1 + dx, top_y - dy), (x1 + dx, top_y - dy + h + 4)], tube, 8)


def ladder(t, x, top_y, h, col=(180, 186, 194)):
    t.line([(x - 26, top_y - 40), (x - 26, top_y + h)], col, 7)
    t.line([(x + 26, top_y - 40), (x + 26, top_y + h)], col, 7)
    t.arc((x - 26, top_y - 64, x + 26, top_y - 16), 180, 360, col, 7)
    for k in range(4):
        yy = top_y - 10 + k * h / 4
        t.rect((x - 26, yy, x + 26, yy + 8), fill=mix(col, (0, 0, 0), 0.15), r=3)


def pool_art(kind):
    def art(c, box):
        def fn(t):
            x0, y0, x1, y1 = box
            W_, H = x1 - x0, y1 - y0
            garden_bg(t, box, horizon=0.42, seed=len(kind))
            cx = (x0 + x1) / 2
            if kind == "inflatable":
                pool_round(t, cx, y0 + H * 0.52, W_ * 0.3, H * 0.13, H * 0.2, (40, 150, 190), (236, 240, 244), "inflatable")
            elif kind == "frame":
                pool_frame(t, x0 + W_ * 0.14, y0 + H * 0.54, W_ * 0.6, H * 0.26, H * 0.28)
            elif kind == "rigid":
                pool_round(t, cx - W_ * 0.04, y0 + H * 0.5, W_ * 0.3, H * 0.12, H * 0.3, (176, 124, 80), (206, 170, 128), "wood")
                ladder(t, cx + W_ * 0.3, y0 + H * 0.52, H * 0.3)
            else:  # semi-inground: разрез грунта, деревянный настил
                gy = y0 + H * 0.56
                t.rect((x0, gy, x1, y1), fill=(150, 108, 74))
                for k, yy in enumerate((0.7, 0.84)):
                    t.line([(x0, y0 + H * yy), (x1, y0 + H * yy + 6)], (132, 94, 62), 4)
                t.rect((x0, gy - 8, x1, gy + 6), fill=GRASS)
                px0, px1 = x0 + W_ * 0.18, x1 - W_ * 0.18
                t.rect((px0, gy - H * 0.12, px1, y1 - H * 0.08), fill=(206, 214, 220))
                t.vgrad((px0 + 10, gy - H * 0.08, px1 - 10, y1 - H * 0.08 - 10), WATER[0], WATER[1])
                # настил
                t.rect((px0 - W_ * 0.12, gy - H * 0.14, px0, gy - H * 0.1), fill=(186, 136, 90))
                t.rect((px1, gy - H * 0.14, px1 + W_ * 0.12, gy - H * 0.1), fill=(186, 136, 90))
                t.line([(px0 - W_ * 0.12, gy - H * 0.1), (px0 - W_ * 0.12, gy)], (150, 104, 66), 6)
                t.line([(px1 + W_ * 0.12, gy - H * 0.1), (px1 + W_ * 0.12, gy)], (150, 104, 66), 6)
                t.rect((px0 - 6, gy - H * 0.16, px1 + 6, gy - H * 0.12), fill=(236, 232, 224))
                # линия грунта поверх стенки
                t.line([(px0, gy), (px1, gy)], (110, 80, 54), 3, alpha=160)
        S.clip_draw(c, box, 18, fn)
    return art


def litres_art(c, box):
    """Условие квиза: прямоугольная ёмкость 4 × 2 м, вода до 1,2 м, размерные стрелки; справа «? litri»."""
    x0, y0, x1, y1 = box
    c.rect(box, fill=(236, 246, 248), r=20)
    sc = 118
    ox, oy = x0 + 70, y1 - 44
    vL, vW, vH = (sc, 0), (sc * 0.5, -sc * 0.3), (0, -sc)

    def P(l, w, h):
        return (ox + l * vL[0] + w * vW[0] + h * vH[0], oy + l * vL[1] + w * vW[1] + h * vH[1])
    Lm, Wm, Hm, Wl = 4, 2, 1.45, 1.2
    wall = (214, 224, 230)
    # задние стенки
    c.poly([P(0, Wm, 0), P(Lm, Wm, 0), P(Lm, Wm, Hm), P(0, Wm, Hm)], mix(wall, (0, 0, 0), 0.08))
    c.poly([P(0, 0, 0), P(0, Wm, 0), P(0, Wm, Hm), P(0, 0, Hm)], mix(wall, (0, 0, 0), 0.14))
    # вода: объём
    c.poly([P(0, 0, 0), P(Lm, 0, 0), P(Lm, Wm, 0), P(Lm, Wm, Wl), P(0, Wm, Wl), P(0, 0, Wl)], WATER[1], alpha=210)
    c.poly([P(0, 0, Wl), P(Lm, 0, Wl), P(Lm, Wm, Wl), P(0, Wm, Wl)], WATER[0], alpha=235)
    # передняя и правая стенки — прозрачные
    c.poly([P(0, 0, 0), P(Lm, 0, 0), P(Lm, 0, Hm), P(0, 0, Hm)], (255, 255, 255), alpha=60)
    c.poly([P(Lm, 0, 0), P(Lm, Wm, 0), P(Lm, Wm, Hm), P(Lm, 0, Hm)], (255, 255, 255), alpha=40)
    edge = (60, 90, 110)
    for a_, b_ in ((P(0, 0, 0), P(Lm, 0, 0)), (P(Lm, 0, 0), P(Lm, Wm, 0)), (P(0, 0, 0), P(0, 0, Hm)), (P(Lm, 0, 0), P(Lm, 0, Hm)),
                   (P(Lm, Wm, 0), P(Lm, Wm, Hm)), (P(0, 0, Hm), P(Lm, 0, Hm)), (P(Lm, 0, Hm), P(Lm, Wm, Hm)),
                   (P(0, 0, Hm), P(0, Wm, Hm)), (P(0, Wm, Hm), P(Lm, Wm, Hm))):
        c.line([a_, b_], edge, 4)
    # размерные стрелки
    col = CORAL2
    a, b = P(0, 0, 0), P(Lm, 0, 0)
    arrow_line(c, (a[0] + 4, a[1] + 24), (b[0] - 4, b[1] + 24), col, 4, 14)
    a, b = P(Lm, 0, 0), P(Lm, Wm, 0)
    arrow_line(c, (a[0] + 26, a[1] + 14), (b[0] + 26, b[1] + 14), col, 4, 14)
    a, b = P(0, 0, 0), P(0, 0, Wl)
    arrow_line(c, (a[0] - 26, a[1] - 4), (b[0] - 26, b[1] + 4), col, 4, 14)

    def chip(xy, txt):
        fw = c.tw(txt, c.font("mxb", 28))[0] + 28
        c.rect((xy[0] - fw / 2, xy[1] - 22, xy[0] + fw / 2, xy[1] + 22), fill=col, r=22)
        c.text(xy, txt, "mxb", 28, WH, anchor="mm")
    a, b = P(0, 0, 0), P(Lm, 0, 0)
    chip(((a[0] + b[0]) / 2, a[1] + 26), "4 m")
    a, b = P(Lm, 0, 0), P(Lm, Wm, 0)
    chip(((a[0] + b[0]) / 2 + 70, (a[1] + b[1]) / 2 + 8), "2 m")
    a, b = P(0, 0, 0), P(0, 0, Wl)
    chip((a[0] - 26, (a[1] + b[1]) / 2), "1,2 m")
    # «? litri»
    qx, qy = x1 - 130, y0 + (y1 - y0) * 0.45
    c.circle(qx, qy, 84, fill=INK2)
    c.text((qx, qy - 20), "?", "mblack", 70, WH, anchor="mm")
    c.text((qx, qy + 40), "litri", "mb", 28, (200, 232, 240), anchor="mm")


def pool_garden_scene(c):
    """Сад: круглый жёсткий бассейн с деревянной обшивкой, лестница, натянутое покрытие наполовину, насос-фильтр сбоку."""
    garden_bg(c, (0, 0, W, W), horizon=0.46, seed=7)
    for x, h in ((120, 260), (980, 300)):
        c.rect((x - 10, 496 - h * 0.4, x + 10, 500), fill=(120, 86, 56))
        c.circle(x, 496 - h * 0.5, h * 0.3, fill=(64, 124, 74))
        c.circle(x - h * 0.15, 496 - h * 0.42, h * 0.22, fill=(76, 140, 84))
    cx, top, rx, ry, h = 500, 700, 330, 96, 190
    pool_round(c, cx, top, rx, ry, h, (176, 124, 80), (206, 170, 128), "wood")
    # покрытие: натянутый тент на правой трети
    c.pie((cx - rx + 6, top - ry + 5, cx + rx - 6, top + ry - 4), -70, 70, (58, 96, 116))
    c.pie((cx - rx + 16, top - ry + 12, cx + rx - 16, top + ry - 10), -70, 70, (72, 114, 136))
    for k in range(1, 4):
        a = math.radians(-70 + k * 35)
        c.line([(cx, top), (cx + (rx - 16) * math.cos(a), top + (ry - 10) * math.sin(a))], (58, 96, 116), 3)
    for k in range(4):
        a = math.radians(-60 + k * 40)
        c.circle(cx + (rx - 14) * math.cos(a), top + (ry - 8) * math.sin(a), 5, fill=(220, 224, 228))
    ladder(c, cx - rx + 40, top + 6, h * 0.8)
    # насос-фильтр
    fx, fy = cx + rx + 70, top + h + 30
    c.ellipse((fx - 60, fy - 10, fx + 60, fy + 14), fill=(0, 0, 0), alpha=40)
    c.rect((fx - 34, fy - 130, fx + 34, fy), fill=(226, 230, 234), r=14)
    c.ellipse((fx - 34, fy - 146, fx + 34, fy - 118), fill=(200, 206, 212))
    c.rect((fx - 44, fy - 40, fx + 44, fy), fill=(90, 98, 110), r=10)
    c.line([(fx - 34, fy - 60), (cx + rx - 10, top + h * 0.5)], (60, 66, 76), 9)
    c.line([(fx - 30, fy - 20), (cx + rx - 6, top + h * 0.8)], (60, 66, 76), 9)
    # цветы и плитка-дорожка
    for k in range(6):
        c.ellipse((40 + k * 70, 960 + (k % 2) * 20, 110 + k * 70, 990 + (k % 2) * 20), fill=(222, 214, 196))
    for x, col in ((70, (236, 120, 110)), (140, (250, 206, 90)), (1010, (236, 120, 110)), (950, (250, 206, 90))):
        c.circle(x, 560, 12, fill=col)
        c.circle(x + 26, 574, 10, fill=col)


P2 = dict(bg=(232, 244, 247), ink=INK2, sub=(70, 96, 108), acc=TEAL2, btn=CORAL2, tile=WH, tile_ink=INK2, iconbg=(222, 240, 244))
PACKS[2] = dict(
    doc="NT-pool-guide-it-2026-09-30", cta="Scopri di più", pal=P2,
    a=dict(fn="grid2x2_art", title="Piscina fuori terra 2026:", title2="quale fa per te?", size=58,
           tiles=[(pool_art("inflatable"), "Gonfiabile", "adatta a una o due estati"),
                  (pool_art("frame"), "Tubolare", "telaio in acciaio, si smonta per l'inverno"),
                  (pool_art("rigid"), "Rigida", "acciaio o legno, resta montata tutto l'anno"),
                  (pool_art("semi"), "Seminterrata", "incassata in parte nel terreno")],
           art_k=0.56, sub_size=22,
           src="разделы «Gonfiabili, tubolari e piscine fuori terra rigide» (1–2 estati / si smontano per l'inverno / restano montate tutto l'anno) и «Piscina seminterrata o interrata: quando ha senso» (incassata per una parte dell'altezza)",
           note="сетка 2×2: сад и 4 типа бассейна (надувной с кольцом, каркасный на стойках, жёсткий в деревянной обшивке с лестницей, полузаглублённый в разрезе грунта), у каждого «Scopri di più»; без цен, людей и брендов"),
    b=dict(fn="quiz_art", title="Piscina 4 × 2 m, acqua a 1,2 m:", title2="quanti litri?", size=54,
           tag="QUIZ", step="Domanda 1 di 3", art=litres_art, art_h=300,
           q="Quanta acqua serve per riempirla?", opts=["4.800 litri", "9.600 litri", "12.000 litri"], opt_layout="row",
           opt_size=30, card_bot=900, btn_y=984, extra_text="на рисунке: 4 m / 2 m / 1,2 m / ? litri",
           pal=dict(bg=(20, 70, 90), bg2=(12, 44, 60), ink=WH, sub=(190, 220, 230), acc=TEAL2, t2=(120, 220, 236), deco=True),
           src="раздел «L'acqua: quanta ne serve e come gestirla» (4 × 2 м при воде 1,2 м = 9,6 м³ = 9.600 литров)",
           note="тёмно-бирюзовый фон, квиз с «прозрачной» ёмкостью 4 × 2 м и уровнем воды 1,2 м, размерные стрелки и «? litri»; верный ответ 9.600 — в статье"),
    c=dict(fn="vs2", title="Piscina tubolare o rigida?", sub="Struttura, inverno e prezzi indicativi 2026", size=58,
           cols=[("TUBOLARE", (80, 100, 118), pool_art("frame"),
                  [("STRUTTURA", "tubi in acciaio, vasca in PVC rinforzato"), ("INVERNO", "si smonta"),
                   ("PREZZO 2026", "da 150 a 1.500 € con pompa")]),
                 ("RIGIDA", (150, 100, 60), pool_art("rigid"),
                  [("STRUTTURA", "pareti in acciaio o legno, con liner"), ("INVERNO", "può restare montata"),
                   ("PREZZO 2026", "da 800 a 4.000 € in acciaio")])],
           foot="Rigida in legno o rivestita: da 2.000 a 8.000 €", art_h=220,
           src="разделы «Gonfiabili, tubolari e piscine fuori terra rigide» (конструкция, зима) и «Piscina fuori terra: prezzi indicativi 2026» (диапазоны цен)",
           note="сравнение каркасного и жёсткого бассейна: рисунки в саду, конструкция, зима, диапазоны цен 2026 — только из раздела 6, без «da 49 €» и скидок"),
    d=dict(fn="top_scene", scene=pool_garden_scene, card_box=(60, 40, 1020, 424), frame=True,
           kicker="PISCINA FUORI TERRA · GUIDA 2026", title="Due piscine della stessa misura possono durare tre estati o dieci",
           sub="I 6 dettagli da controllare prima di comprare", size=46, lines=3, btn_off=58, btn_size=38,
           src="раздел «Qualità: i dettagli che fanno la differenza» (первая фраза и список из 6 пунктов) + лид (сравнение надувного и жёсткого)",
           note="сад: круглый жёсткий бассейн в деревянной обшивке, лестница, натянутое покрытие, насос-фильтр сбоку, людей в воде нет; карточка с крючком-цитатой из статьи"),
)


# =====================================================================  3. DE · товарка · электромобили
INK3 = (22, 40, 54)
GREEN3 = (0, 138, 104)
ORANGE3 = (230, 84, 40)


def wheel(t, cx, cy, r, tire=(44, 46, 52), rim=(196, 200, 206)):
    t.circle(cx, cy, r, fill=tire)
    t.circle(cx, cy, r * 0.55, fill=rim)
    t.circle(cx, cy, r * 0.18, fill=(120, 124, 132))


def scooter(t, x, gy, s, col=(200, 60, 50), canopy=False, basket=True):
    """Открытый электромобиль (4 колеса, сиденье, руль-колонка, корзина), вид сбоку, лицом вправо."""
    wr = s * (0.14 if canopy else 0.12)
    dark = mix(col, (0, 0, 0), 0.25)
    wheel(t, x - s * 0.36, gy - wr, wr)
    wheel(t, x + s * 0.42, gy - wr, wr)
    # платформа и обтекатели
    t.rect((x - s * 0.52, gy - s * 0.3, x + s * 0.3, gy - s * 0.16), fill=(60, 64, 72), r=s * 0.05)
    t.pie((x - s * 0.36 - wr * 1.5, gy - wr - wr * 1.5, x - s * 0.36 + wr * 1.5, gy - wr + wr * 1.5), 180, 360, col)
    t.poly([(x + s * 0.2, gy - s * 0.18), (x + s * 0.3, gy - s * 0.46), (x + s * 0.5, gy - s * 0.42), (x + s * 0.62, gy - s * 0.2),
            (x + s * 0.62, gy - s * 0.16), (x + s * 0.2, gy - s * 0.16)], col)
    t.pie((x + s * 0.42 - wr * 1.45, gy - wr - wr * 1.45, x + s * 0.42 + wr * 1.45, gy - wr + wr * 1.45), 180, 360, col)
    t.circle(x + s * 0.6, gy - s * 0.3, s * 0.03, fill=(255, 236, 170))
    # стойка сиденья, сиденье, спинка, подлокотник
    t.rect((x - s * 0.2, gy - s * 0.52, x - s * 0.14, gy - s * 0.28), fill=(80, 84, 92))
    t.rect((x - s * 0.36, gy - s * 0.6, x + s * 0.02, gy - s * 0.5), fill=(50, 54, 62), r=s * 0.04)
    t.rect((x - s * 0.4, gy - s * 0.98, x - s * 0.3, gy - s * 0.56), fill=(50, 54, 62), r=s * 0.04)
    t.rect((x - s * 0.34, gy - s * 0.72, x - s * 0.04, gy - s * 0.67), fill=(80, 84, 92), r=s * 0.02)
    # рулевая колонка
    t.line([(x + s * 0.32, gy - s * 0.4), (x + s * 0.2, gy - s * 0.86)], dark, s * 0.05)
    t.line([(x + s * 0.12, gy - s * 0.88), (x + s * 0.28, gy - s * 0.86)], (50, 54, 62), s * 0.04)
    if basket:
        bx = x + s * 0.34
        t.poly([(bx, gy - s * 0.66), (bx + s * 0.26, gy - s * 0.66), (bx + s * 0.22, gy - s * 0.48), (bx + s * 0.04, gy - s * 0.48)],
               (210, 214, 220))
        for k in range(1, 5):
            xx = bx + s * 0.26 * k / 5
            t.line([(xx, gy - s * 0.66), (xx - s * 0.01 * (k - 2.5), gy - s * 0.48)], (150, 156, 166), 2)
        t.line([(bx, gy - s * 0.66), (bx + s * 0.26, gy - s * 0.66)], (150, 156, 166), 3)
    if canopy:
        t.line([(x - s * 0.42, gy - s * 0.3), (x - s * 0.42, gy - s * 1.22)], (120, 124, 132), s * 0.025)
        t.rect((x - s * 0.5, gy - s * 1.28, x + s * 0.44, gy - s * 1.2), fill=(236, 238, 240), r=s * 0.03)
        t.poly([(x + s * 0.44, gy - s * 1.2), (x + s * 0.3, gy - s * 0.5), (x + s * 0.36, gy - s * 0.5), (x + s * 0.48, gy - s * 1.2)],
               (190, 220, 236), alpha=180)
        t.line([(x + s * 0.44, gy - s * 1.22), (x + s * 0.3, gy - s * 0.5)], (150, 156, 166), 3)


def cabin_car(t, x, gy, s, col=(62, 150, 130), two=False):
    """Кабинка-электромобиль (1 место) или лёгкий квадрицикл 45 км/ч (2 места), лицом вправо; без логотипов."""
    wr = s * 0.13
    dark = mix(col, (0, 0, 0), 0.25)
    L0, L1 = (x - s * 0.5, x + s * (0.62 if two else 0.5))
    t.ellipse((L0, gy - s * 0.05, L1, gy + s * 0.05), fill=(0, 0, 0), alpha=40)
    # кузов
    body = [(L0, gy - s * 0.2), (L0, gy - s * 0.56), (L0 + s * 0.06, gy - s * 0.98), (x + s * (0.12 if two else 0.06), gy - s * 1.02),
            (x + s * (0.34 if two else 0.28), gy - s * 0.6), (L1, gy - s * 0.5), (L1, gy - s * 0.2)]
    t.poly(body, col)
    t.rect((L0 - s * 0.02, gy - s * 0.3, L1 + s * 0.02, gy - s * 0.14), fill=dark, r=s * 0.04)
    # окна
    t.poly([(L0 + s * 0.08, gy - s * 0.58), (L0 + s * 0.12, gy - s * 0.92), (x - s * 0.1, gy - s * 0.94), (x - s * 0.1, gy - s * 0.58)],
           (196, 224, 238))
    t.poly([(x - s * 0.04, gy - s * 0.58), (x - s * 0.04, gy - s * 0.94), (x + s * (0.1 if two else 0.04), gy - s * 0.94),
            (x + s * (0.3 if two else 0.24), gy - s * 0.6)], (196, 224, 238))
    if two:
        t.line([(x - s * 0.36, gy - s * 0.58), (x - s * 0.36, gy - s * 0.94)], col, s * 0.04)
    # дверь, ручка, фары
    t.line([(x - s * 0.1, gy - s * 0.56), (x - s * 0.1, gy - s * 0.24)], dark, 3)
    t.line([(x + s * (0.3 if two else 0.24), gy - s * 0.56), (x + s * (0.3 if two else 0.24), gy - s * 0.24)], dark, 3)
    t.rect((x + s * 0.02, gy - s * 0.48, x + s * 0.1, gy - s * 0.45), fill=dark, r=2)
    t.ellipse((L1 - s * 0.07, gy - s * 0.46, L1 + s * 0.01, gy - s * 0.38), fill=(255, 236, 170))
    t.rect((L0 - s * 0.01, gy - s * 0.5, L0 + s * 0.04, gy - s * 0.42), fill=(220, 60, 50), r=3)
    wheel(t, L0 + s * 0.2, gy - wr, wr)
    wheel(t, L1 - s * 0.2, gy - wr, wr)
    # зеркало
    t.rect((x + s * 0.2, gy - s * 0.68, x + s * 0.28, gy - s * 0.62), fill=dark, r=3)


def ev_art(kind):
    def art(c, box):
        def fn(t):
            x0, y0, x1, y1 = box
            W_, H = x1 - x0, y1 - y0
            t.vgrad(box, (226, 238, 242), (242, 246, 246))
            gy = y1 - H * 0.12
            t.rect((x0, gy, x1, y1), fill=(196, 200, 204))
            t.rect((x0, gy, x1, gy + 5), fill=(170, 176, 182))
            for k in range(6):
                t.rect((x0 + k * 110 - 20, gy + 16, x0 + k * 110 + 40, gy + 22), fill=WH, alpha=160)
            cx = (x0 + x1) / 2 + W_ * 0.04
            if kind == 6:
                scooter(t, cx, gy, H * 0.84, col=(214, 64, 52))
            elif kind == 15:
                scooter(t, cx, gy, H * 0.66, col=(44, 110, 170), canopy=True)
            elif kind == 25:
                cabin_car(t, cx - W_ * 0.04, gy, H * 0.8, col=(236, 170, 60))
            else:
                cabin_car(t, cx - W_ * 0.06, gy, H * 0.72, col=GREEN3, two=True)
        S.clip_draw(c, box, 18, fn)
    return art


def speedo_art(c, box):
    """Спидометр со стрелкой на 45 + маленькая кабинка 45 км/ч справа."""
    x0, y0, x1, y1 = box
    c.rect(box, fill=(236, 244, 242), r=20)
    cx, cy, r = x0 + 200, y1 - 26, 176
    c.pie((cx - r, cy - r, cx + r, cy + r), 180, 360, INK3)
    c.pie((cx - r + 16, cy - r + 16, cx + r - 16, cy + r - 16), 180, 360, (34, 56, 72))
    c.arc((cx - r + 30, cy - r + 30, cx + r - 30, cy + r - 30), 180 + 180 * 40 / 60, 180 + 180 * 50 / 60, (250, 190, 60), 14)
    for v in range(0, 61, 5):
        a = math.radians(180 + 180 * v / 60)
        rr0 = r - 34 if v % 15 == 0 else r - 28
        c.line([(cx + math.cos(a) * rr0, cy + math.sin(a) * rr0), (cx + math.cos(a) * (r - 18), cy + math.sin(a) * (r - 18))], WH, 4 if v % 15 == 0 else 2)
        if v % 15 == 0 and v != 45:
            c.text((cx + math.cos(a) * (r - 60), cy + math.sin(a) * (r - 60) - (12 if v in (0, 60) else 0)), str(v), "mb", 24,
                   (200, 220, 226), anchor="mm")
    a = math.radians(180 + 180 * 45 / 60)
    c.line([(cx, cy), (cx + math.cos(a) * (r - 44), cy + math.sin(a) * (r - 44))], ORANGE3, 9)
    c.circle(cx, cy, 20, fill=ORANGE3)
    c.text((cx + r + 150, cy - 110), "45", "mblack", 110, INK3, anchor="mm")
    c.text((cx + r + 150, cy - 30), "km/h", "mxb", 40, GREEN3, anchor="mm")
    cabin_car(c, x1 - 180, y1 - 20, 170, col=GREEN3, two=True)


def battery_art(kind):
    def art(c, box):
        def fn(t):
            x0, y0, x1, y1 = box
            W_, H = x1 - x0, y1 - y0
            t.vgrad(box, (236, 242, 244), (224, 232, 236))
            t.rect((x0, y1 - H * 0.16, x1, y1), fill=(206, 212, 216))
            cx, by = (x0 + x1) / 2, y1 - H * 0.16
            if kind == "lead":
                bw, bh = W_ * 0.5, H * 0.52
                t.shadow((cx - bw / 2, by - bh, cx + bw / 2, by), r=10, alpha=60, blur=8, off=(0, 6))
                t.rect((cx - bw / 2, by - bh, cx + bw / 2, by), fill=(52, 56, 64), r=10)
                t.rect((cx - bw / 2, by - bh, cx + bw / 2, by - bh + 26), fill=(70, 74, 84), r=10)
                for k, col in ((-1, (60, 60, 64)), (1, (214, 60, 50))):
                    t.rect((cx + k * bw * 0.3 - 16, by - bh - 22, cx + k * bw * 0.3 + 16, by - bh + 4), fill=col, r=4)
                t.text((cx + bw * 0.3, by - bh + 50), "+", "mblack", 30, (214, 60, 50), anchor="mm")
                t.text((cx - bw * 0.3, by - bh + 50), "–", "mblack", 30, (200, 200, 204), anchor="mm")
                # гиря «schwer»
                gx, gy = x0 + W_ * 0.14, by
                t.poly([(gx - 34, gy), (gx + 34, gy), (gx + 26, gy - 56), (gx - 26, gy - 56)], (90, 94, 102))
                t.arc((gx - 20, gy - 84, gx + 20, gy - 44), 180, 360, (90, 94, 102), 8)
                t.text((gx, gy - 24), "kg", "mb", 22, WH, anchor="mm")
            else:
                bw, bh = W_ * 0.44, H * 0.3
                t.shadow((cx - bw / 2, by - bh, cx + bw / 2, by), r=16, alpha=50, blur=8, off=(0, 6))
                t.rect((cx - bw / 2, by - bh, cx + bw / 2, by), fill=(206, 214, 220), r=16)
                t.rect((cx - bw / 2 + 10, by - bh + 10, cx + bw / 2 - 10, by - 10), fill=(236, 240, 242), r=10)
                for k in range(4):
                    t.rect((cx - bw / 2 + 24 + k * (bw - 60) / 4, by - bh + 22, cx - bw / 2 + 24 + (k + 1) * (bw - 60) / 4 - 10, by - 22),
                           fill=GREEN3, r=5)
                t.rect((cx + bw / 2, by - bh * 0.7, cx + bw / 2 + 12, by - bh * 0.3), fill=(150, 156, 166), r=3)
                bx, byy = cx, by - bh - 70
                t.poly([(bx + 10, byy - 40), (bx - 18, byy + 6), (bx, byy + 6), (bx - 10, byy + 44), (bx + 20, byy - 4), (bx + 2, byy - 4),
                        (bx + 14, byy - 40)], (250, 190, 50))
                # розетка «lädt schneller»
                sx = x1 - W_ * 0.16
                t.rect((sx - 30, by - 100, sx + 30, by - 40), fill=WH, r=10, outline=(170, 176, 182), width=2)
                t.circle(sx - 10, by - 70, 5, fill=(90, 96, 104))
                t.circle(sx + 10, by - 70, 5, fill=(90, 96, 104))
                t.line([(sx - 30, by - 60), (cx + bw / 2 + 12, by - bh * 0.5)], (70, 76, 84), 4)
        S.clip_draw(c, box, 20, fn)
    return art


def bakery_street(c):
    """Тихая улица у пекарни: фасад, витрина с хлебом, маркиза, тротуар; кабинка 25 км/ч и открытый электромобиль с корзиной."""
    c.vgrad((0, 0, W, 560), (206, 230, 242), (236, 244, 246))
    # дома
    c.rect((0, 300, 360, 860), fill=(236, 214, 184))
    c.rect((360, 250, 820, 860), fill=(244, 236, 222))
    c.rect((820, 330, W, 860), fill=(214, 196, 176))
    for bx, by, cols, rows, col in ((30, 470, 3, 1, (196, 222, 236)), (860, 490, 2, 1, (196, 222, 236))):
        for i in range(cols):
            for j in range(rows):
                x, y = bx + i * 110, by + j * 120
                c.rect((x, y, x + 70, y + 86), fill=WH, r=4)
                c.rect((x + 6, y + 6, x + 64, y + 80), fill=col, r=2)
    # пекарня (ниже карточки-заголовка)
    c.text((590, 506), "BÄCKEREI", "mxb", 44, (120, 80, 56), anchor="mm")
    c.rect((380, 530, 800, 548), fill=(120, 80, 56))
    for k in range(8):
        col = (196, 64, 54) if k % 2 == 0 else (250, 246, 240)
        c.poly([(380 + k * 52.5, 548), (380 + (k + 1) * 52.5, 548), (380 + (k + 1) * 52.5 + 6, 604), (380 + k * 52.5 + 6, 604)], col)
    c.rect((400, 622, 640, 800), fill=(214, 232, 240), r=4, outline=(120, 80, 56), width=8)
    for bx, by_ in ((440, 760), (510, 760), (580, 760), (470, 712), (550, 712)):
        c.ellipse((bx - 34, by_ - 18, bx + 34, by_ + 18), fill=(212, 150, 80))
        for j in range(3):
            c.line([(bx - 16 + j * 14, by_ - 10), (bx - 10 + j * 14, by_ + 10)], (176, 110, 50), 3)
    c.rect((400, 790, 640, 800), fill=(120, 80, 56))
    c.rect((670, 622, 780, 860), fill=(120, 80, 56), r=4)
    c.rect((682, 636, 768, 740), fill=(214, 232, 240), r=3)
    c.circle(760, 760, 6, fill=(230, 200, 120))
    # тротуар, бордюр, дорога
    c.rect((0, 860, W, 940), fill=(214, 206, 196))
    for k in range(14):
        c.line([(k * 80, 860), (k * 80 - 10, 940)], (196, 188, 178), 3)
    c.rect((0, 940, W, 956), fill=(170, 164, 156))
    c.rect((0, 956, W, W), fill=(96, 100, 108))
    # растения у витрины
    S.plant(c, 340, 866, 0.55, pot=(200, 110, 70), leaf=(80, 140, 90))
    # открытый электромобиль у тротуара и кабинка на обочине
    scooter(c, 200, 900, 190, col=(214, 64, 52))
    cabin_car(c, 840, 990, 250, col=(236, 170, 60))


P3 = dict(bg=(238, 245, 243), ink=INK3, sub=(78, 94, 104), acc=GREEN3, btn=ORANGE3, tile=WH, tile_ink=INK3, iconbg=(224, 240, 236))
PACKS[3] = dict(
    doc="NT-ev-guide-de-2026-09-30", cta="Mehr erfahren", pal=P3,
    a=dict(fn="grid2x2_art", title="Elektromobil kaufen 2026:", title2="welche Klasse passt?", size=58,
           tiles=[(ev_art(6), "bis 6 km/h", "ohne Führerschein, ohne Versicherungskennzeichen"),
                  (ev_art(15), "bis 15 km/h", "ohne Führerschein, mit Versicherungskennzeichen"),
                  (ev_art(25), "bis 25 km/h", "Kabine; Mofa-Prüfbescheinigung je nach Geburtsjahr"),
                  (ev_art(45), "bis 45 km/h", "Kabine; Führerschein Klasse AM, in Klasse B enthalten")],
           art_k=0.55, sub_size=22,
           src="раздел «Die Klassen im Überblick» (6 / 15 / 25 / 45 км/ч: права, страховой номер, Mofa-Prüfbescheinigung, класс AM в B) + разделы 2–4 (открытый / кабина / 2 места)",
           note="сетка 2×2: 4 класса по скорости с рисунком машины (открытый с корзиной / с навесом / кабинка / двухместный 45 км/ч), у каждой «Mehr erfahren»; без возраста, брендов и цен"),
    b=dict(fn="quiz_art", title="45 km/h:", title2="welche Fahrerlaubnis?", size=60, t2k=0.92,
           tag="QUIZ", step="Frage 1 von 3", art=speedo_art, art_h=230, q_size=31,
           q="Was braucht man für ein Leichtkraftfahrzeug mit 45\u00a0km/h?",
           opts=["Keine", "Mofa-Prüfbescheinigung", "Klasse AM", "Weiß nicht"], opt_layout="2x2", opt_size=28,
           card_bot=906, btn_y=986, pal=dict(bg=(226, 240, 236), bg2=(206, 228, 222), deco=True),
           extra_text="на рисунке: спидометр 0 / 15 / 30 / 60, стрелка и «45 km/h»",
           src="раздел «Mit 45 km/h: Leichtkraftfahrzeug oder kleines Elektroauto» (Klasse AM, в B и старой Klasse 3)",
           note="квиз про правило, не про зрителя: спидометр со стрелкой на 45 и двухместная кабинка; верный ответ «Klasse AM» — в статье"),
    c=dict(fn="vs2", title="Blei-Gel oder Lithium?", sub="Der Akku im Elektromobil: der Unterschied", size=60,
           cols=[("BLEI-GEL", (70, 76, 88), battery_art("lead"),
                  [("PREIS", "günstiger"), ("GEWICHT", "schwer"), ("HALTBARKEIT", "meist einige hundert Ladezyklen")]),
                 ("LITHIUM", GREEN3, battery_art("li"),
                  [("PREIS", "teurer"), ("GEWICHT", "leichter, lädt schneller"), ("HALTBARKEIT", "hält deutlich länger")])],
           foot="Laden: normale Steckdose, meist 6–8 Stunden", art_h=230,
           src="раздел «Akku, Reichweite und Laden» (Blei-Gel vs Lithium, бытовая розетка, 6–8 часов)",
           note="сравнение двух аккумуляторов: тяжёлый свинцово-гелевый блок с гирей vs литиевый пакет с индикатором и розеткой; только пункты статьи"),
    d=dict(fn="top_scene", scene=bakery_street, card_box=(60, 36, 1020, 360), frame=True,
           kicker="RATGEBER 2026", title="Elektromobil kaufen: 6, 15, 25 oder 45 km/h?",
           sub="Wann ein Führerschein nötig ist und was es kostet", size=50, lines=2, btn_off=56, btn_size=38,
           extra_text="вывеска в сцене: BÄCKEREI",
           src="заголовок статьи + лид («für kurze Wege zum Bäcker…», от открытого с корзиной до кабинки)",
           note="тихая улица у пекарни: открытый электромобиль с корзиной у тротуара и кабинка на обочине; без людей, логотипов и медицинских мотивов"),
)


# =====================================================================  4. BR · кредиты · б/у авто в рассрочку без банка
INK4 = (18, 58, 66)
TEAL4 = (0, 122, 120)
CORAL4 = (226, 84, 50)
SAND4 = (250, 245, 236)


def car_side(t, x, gy, s, col=(196, 60, 56)):
    """Хэтчбек сбоку, лицом вправо, без марки и номеров. s — длина кузова."""
    dark = mix(col, (0, 0, 0), 0.28)
    lite = mix(col, WH, 0.18)
    wr = s * 0.1
    x0, x1 = x - s / 2, x + s / 2
    t.ellipse((x0 + s * 0.02, gy - s * 0.03, x1 - s * 0.02, gy + s * 0.03), fill=(0, 0, 0), alpha=45)
    body = [(x0, gy - s * 0.12), (x0 + s * 0.01, gy - s * 0.26), (x0 + s * 0.06, gy - s * 0.3), (x0 + s * 0.14, gy - s * 0.48),
            (x0 + s * 0.52, gy - s * 0.5), (x0 + s * 0.66, gy - s * 0.33), (x1 - s * 0.04, gy - s * 0.29), (x1, gy - s * 0.22),
            (x1, gy - s * 0.12)]
    t.poly(body, col)
    t.poly([(x0 + s * 0.06, gy - s * 0.3), (x0 + s * 0.14, gy - s * 0.48), (x0 + s * 0.52, gy - s * 0.5), (x0 + s * 0.66, gy - s * 0.33)],
           lite)
    # окна
    t.poly([(x0 + s * 0.16, gy - s * 0.44), (x0 + s * 0.34, gy - s * 0.46), (x0 + s * 0.34, gy - s * 0.33), (x0 + s * 0.1, gy - s * 0.32)],
           (190, 216, 232))
    t.poly([(x0 + s * 0.37, gy - s * 0.46), (x0 + s * 0.51, gy - s * 0.46), (x0 + s * 0.62, gy - s * 0.33), (x0 + s * 0.37, gy - s * 0.33)],
           (190, 216, 232))
    t.line([(x0 + s * 0.355, gy - s * 0.47), (x0 + s * 0.355, gy - s * 0.14)], dark, 3)
    t.line([(x0 + s * 0.62, gy - s * 0.33), (x0 + s * 0.62, gy - s * 0.14)], dark, 3)
    for hx in (x0 + s * 0.3, x0 + s * 0.56):
        t.rect((hx - s * 0.03, gy - s * 0.29, hx, gy - s * 0.275), fill=dark, r=2)
    t.rect((x0 - s * 0.01, gy - s * 0.17, x1 + s * 0.01, gy - s * 0.11), fill=dark, r=s * 0.02)
    t.ellipse((x1 - s * 0.05, gy - s * 0.27, x1 + s * 0.005, gy - s * 0.22), fill=(255, 236, 170))
    t.rect((x0 - s * 0.005, gy - s * 0.28, x0 + s * 0.025, gy - s * 0.22), fill=(220, 50, 40), r=3)
    for wx in (x0 + s * 0.2, x1 - s * 0.19):
        t.pie((wx - wr * 1.25, gy - wr - wr * 1.25, wx + wr * 1.25, gy - wr + wr * 1.25), 180, 360, (40, 42, 48))
        wheel(t, wx, gy - wr, wr)
    t.rect((x0 + s * 0.57, gy - s * 0.37, x0 + s * 0.61, gy - s * 0.34), fill=dark, r=2)


def boleto_doc(t, cx, cy, s, col=INK4):
    """Лист-болето: шапка, строки, штрих-код (без сумм)."""
    w, h = s * 0.62, s * 0.8
    t.shadow((cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2), r=8, alpha=50, blur=6, off=(0, 4))
    t.rect((cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2), fill=WH, r=8)
    t.rect((cx - w / 2, cy - h / 2, cx + w / 2, cy - h / 2 + h * 0.16), fill=col, r=8)
    t.rect((cx - w / 2, cy - h / 2 + h * 0.1, cx + w / 2, cy - h / 2 + h * 0.16), fill=col)
    for k in range(3):
        yy = cy - h * 0.22 + k * h * 0.12
        t.rect((cx - w * 0.38, yy, cx + w * (0.1 + 0.1 * (k % 2)), yy + h * 0.04), fill=(214, 220, 224), r=3)
    bx0, by0 = cx - w * 0.38, cy + h * 0.2
    rnd = random.Random(3)
    x = bx0
    while x < cx + w * 0.38:
        bw = rnd.choice((2, 3, 5))
        t.rect((x, by0, x + bw, by0 + h * 0.18), fill=(40, 42, 48))
        x += bw + rnd.choice((2, 3, 4))


def store_front(t, cx, by, s, col=CORAL4):
    """Магазин-автосалон: вывеска LOJA, навес в полоску, витрина, дверь."""
    w, h = s, s * 0.8
    x0 = cx - w / 2
    top = by - h
    t.rect((x0, top, x0 + w, by), fill=(244, 240, 232), r=6)
    t.rect((x0 + w * 0.12, top + h * 0.04, x0 + w * 0.88, top + h * 0.2), fill=WH, r=6, outline=col, width=3)
    t.text((cx, top + h * 0.12), "LOJA", "mxb", s * 0.11, INK4, anchor="mm")
    ay = top + h * 0.26
    for k in range(6):
        c_ = col if k % 2 == 0 else WH
        t.rect((x0 + k * w / 6, ay, x0 + (k + 1) * w / 6, ay + h * 0.12), fill=c_)
    for k in range(6):
        c_ = col if k % 2 == 0 else (236, 236, 232)
        t.pie((x0 + k * w / 6, ay + h * 0.06, x0 + (k + 1) * w / 6, ay + h * 0.18), 0, 180, c_)
    t.rect((x0 + w * 0.08, by - h * 0.5, x0 + w * 0.6, by - h * 0.06), fill=(200, 226, 238), r=4)
    t.rect((x0 + w * 0.68, by - h * 0.5, x0 + w * 0.9, by), fill=mix(col, (0, 0, 0), 0.3), r=4)


def people_group(t, cx, by, s, cols=((226, 84, 50), (0, 122, 120), (236, 170, 60), (90, 110, 160))):
    for k, (dx, hs) in enumerate(((-0.33, 0.8), (-0.11, 0.92), (0.11, 0.86), (0.33, 0.78))):
        x = cx + dx * s
        h = s * 0.62 * hs
        t.rect((x - s * 0.09, by - h * 0.62, x + s * 0.09, by), fill=cols[k % len(cols)], r=s * 0.08)
        t.circle(x, by - h * 0.62 - s * 0.08, s * 0.075, fill=SKIN[k % 4])


def ball(t, cx, cy, r, col, num):
    t.circle(cx, cy, r, fill=col)
    t.circle(cx, cy, r * 0.55, fill=WH)
    t.text((cx, cy + 1), num, "mxb", r * 0.62, INK4, anchor="mm")


def handshake_art(t, cx, cy, s):
    icon(t, "handshake", cx - s * 0.12, cy - s * 0.02, s * 1.0, INK4, bg=(234, 236, 246))
    # контракт
    w, h = s * 0.4, s * 0.52
    x0, y0 = cx + s * 0.36, cy - s * 0.26
    t.rect((x0, y0, x0 + w, y0 + h), fill=WH, r=6, outline=(200, 196, 188), width=2)
    for k in range(4):
        t.rect((x0 + w * 0.14, y0 + h * (0.16 + 0.16 * k), x0 + w * (0.86 - 0.12 * (k % 2)), y0 + h * (0.16 + 0.16 * k) + 5), fill=(210, 214, 218), r=2)
    t.line([(x0 + w * 0.2, y0 + h * 0.86), (x0 + w * 0.45, y0 + h * 0.8), (x0 + w * 0.7, y0 + h * 0.88)], TEAL4, 3)


def br_art(kind):
    def art(c, box):
        def fn(t):
            x0, y0, x1, y1 = box
            W_, H = x1 - x0, y1 - y0
            bgc = {"boleto": (252, 232, 220), "store": (222, 240, 238), "cons": (252, 240, 214), "priv": (234, 236, 246)}[kind]
            t.rect(box, fill=bgc)
            t.circle(x1 - W_ * 0.1, y0 + H * 0.1, H * 0.5, fill=WH, alpha=60)
            cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
            if kind == "boleto":
                car_side(t, cx - W_ * 0.12, y1 - H * 0.12, W_ * 0.5, col=(196, 60, 56))
                boleto_doc(t, cx + W_ * 0.26, cy - H * 0.02, H * 0.9)
            elif kind == "store":
                store_front(t, cx - W_ * 0.14, y1 - H * 0.1, W_ * 0.44, col=TEAL4)
                car_side(t, cx + W_ * 0.24, y1 - H * 0.1, W_ * 0.4, col=(70, 110, 170))
            elif kind == "cons":
                people_group(t, cx - W_ * 0.14, y1 - H * 0.08, H * 1.0)
                for k, (dx, dy, col, n) in enumerate(((0.2, -0.18, CORAL4, "7"), (0.33, 0.02, TEAL4, "12"), (0.18, 0.18, (236, 170, 60), "3"))):
                    ball(t, cx + W_ * dx, cy + H * dy, H * 0.13, col, n)
            else:
                handshake_art(t, cx - W_ * 0.1, cy, H * 0.95)
        S.clip_draw(c, box, 18, fn)
    return art


def cet_art(c, box):
    """Условие квиза: предложение по рассрочке с тремя полями без цифр (серые плашки) и лупа."""
    x0, y0, x1, y1 = box
    c.rect(box, fill=(246, 240, 230), r=20)
    car_side(c, x0 + 190, y1 - 30, 300, col=(196, 60, 56))
    px0, py0, px1, py1 = x0 + 390, y0 + 22, x1 - 40, y1 - 22
    c.shadow((px0, py0, px1, py1), r=14, alpha=60, blur=10, off=(0, 6))
    c.rect((px0, py0, px1, py1), fill=WH, r=14)
    c.rect((px0, py0, px1, py0 + 48), fill=INK4, r=14)
    c.rect((px0, py0 + 30, px1, py0 + 48), fill=INK4)
    c.text((px0 + 24, py0 + 24), "PROPOSTA · CARRO USADO", "mb", 22, WH, anchor="lm")
    rows = ("Valor da parcela", "Número de parcelas", "CET")
    rh = (py1 - py0 - 60) / 3
    for k, lab in enumerate(rows):
        yy = py0 + 60 + k * rh
        c.text((px0 + 24, yy + rh / 2), lab, "mb", 25, (60, 64, 70), anchor="lm")
        c.rect((px1 - 150, yy + rh / 2 - 14, px1 - 24, yy + rh / 2 + 14), fill=(222, 226, 230), r=8)
        c.text((px1 - 87, yy + rh / 2), "?", "mxb", 24, CORAL4, anchor="mm")
        if k < 2:
            c.line([(px0 + 20, yy + rh), (px1 - 20, yy + rh)], (230, 232, 234), 2)
    # лупа вокруг «?» в строке CET
    yy = py0 + 60 + 2 * rh + rh / 2
    mx, my = px1 - 87, yy
    c.circle(mx, my, 50, outline=INK4, width=8)
    c.line([(mx + 36, my + 36), (mx + 70, my + 60)], INK4, 14)


def br_lot_scene(c):
    """Двор автосалона: навес-флажки, б/у хэтчбек без марки и номеров; на переднем плане планшет-чек-лист с галочками."""
    c.vgrad((0, 0, W, 700), (214, 236, 244), (244, 244, 238))
    for cx_, cy_, k in ((700, 250, 1.0), (930, 200, 0.7), (170, 250, 0.8)):
        for dx, dy, r in ((-50, 8, 34), (-10, -10, 44), (36, 4, 36), (70, 12, 26)):
            c.circle(cx_ + dx * k, cy_ + dy * k, r * k, fill=WH, alpha=230)
    c.rect((0, 560, W, W), fill=(206, 204, 198))
    for k in range(9):
        c.line([(k * 140 - 60, W), (k * 140 + 40, 560)], (192, 190, 184), 3)
    # фон: здание и флажки
    c.rect((560, 330, 1080, 560), fill=(240, 236, 228))
    c.rect((560, 330, 1080, 360), fill=TEAL4)
    c.rect((600, 390, 1040, 540), fill=(200, 226, 238), r=6)
    for k in range(3):
        car_side(c, 690 + k * 140, 540, 130, col=((236, 170, 60), (90, 110, 160), (220, 220, 224))[k])
    c.line([(540, 300), (1080, 280)], (120, 124, 132), 2)
    for k in range(12):
        x = 560 + k * 44
        y = 300 - (x - 540) * 20 / 540
        c.poly([(x, y), (x + 30, y), (x + 15, y + 30)], (CORAL4, (236, 170, 60), TEAL4)[k % 3])
    # главный автомобиль
    car_side(c, 800, 900, 500, col=(196, 60, 56))
    # планшет с чек-листом
    bx0, by0, bx1, by1 = 36, 300, 540, 1050
    c.shadow((bx0, by0, bx1, by1), r=22, alpha=90, blur=14, off=(0, 10))
    c.rect((bx0, by0, bx1, by1), fill=(150, 104, 66), r=22)
    c.rect((bx0 + 18, by0 + 40, bx1 - 18, by1 - 18), fill=WH, r=10)
    c.rect(((bx0 + bx1) / 2 - 80, by0 - 14, (bx0 + bx1) / 2 + 80, by0 + 40), fill=(120, 124, 132), r=10)
    c.text((bx0 + 42, by0 + 78), "Antes de assinar,", "mxb", 30, INK4)
    c.text((bx0 + 42, by0 + 116), "confira:", "mxb", 30, CORAL4)
    items = ("Documento do veículo", "IPVA, licenciamento e multas", "Gravame ou alienação", "Vistoria cautelar",
             "Contrato por escrito")
    yy = by0 + 180
    for it in items:
        c.rect((bx0 + 42, yy, bx0 + 84, yy + 42), fill=WH, r=8, outline=TEAL4, width=4)
        c.check(bx0 + 49, yy + 6, 30, TEAL4, 6)
        c.block(it, "mb", 28, yy + 4, bx1 - bx0 - 140, INK4, align="left", x=bx0 + 100, max_lines=2, gap=1.05)
        nl = len(c.wrap(it, c.font("mb", 28), bx1 - bx0 - 140))
        yy += max(44, nl * 34) + 64


P4 = dict(bg=SAND4, ink=INK4, sub=(86, 98, 102), acc=TEAL4, t2=CORAL4, btn=CORAL4, tile=WH, tile_ink=INK4, iconbg=(236, 244, 242))
PACKS[4] = dict(
    doc="NT-used-car-installments-br-2026-09-30", cta="Saiba mais", pal=P4,
    a=dict(fn="grid2x2_art", title="Carro usado parcelado sem banco:", title2="qual caminho?", size=50, t2k=1.1, lines=1,
           tiles=[(br_art("boleto"), "Boleto da loja", "parcelas mensais direto com a revenda"),
                  (br_art("store"), "Crediário da loja", "financeira parceira, com análise e juros"),
                  (br_art("cons"), "Consórcio", "carta de crédito por sorteio ou lance"),
                  (br_art("priv"), "Entre particulares", "parcelas combinadas em contrato")],
           art_k=0.5, sub_size=23,
           src="раздел «Carro usado sem financiamento: as formas mais comuns» (4 из 5 способов: boleto da loja, crediário por financeira parceira, consórcio, compra entre particulares)",
           note="сетка 2×2 способов без банка с рисунками (машина + болето, магазин, группа + шары жеребьёвки, рукопожатие + договор), у каждого «Saiba mais»; без сумм, процентов, логотипов банков и консорсиумов"),
    b=dict(fn="quiz_art", title="Parcela baixa, custo alto?", title2="Faça o teste", size=58, t2k=0.72,
           tag="QUIZ", step="Pergunta 1 de 3", art=cet_art, art_h=250, q_size=30,
           q="Qual número mostra o custo real do carro parcelado?",
           opts=["Valor da parcela", "Número de parcelas", "CET – custo efetivo total", "Não sei"], opt_layout="list", opt_size=29,
           extra_text="на рисунке: PROPOSTA · CARRO USADO / Valor da parcela ? / Número de parcelas ? / CET ?",
           card_bot=916, btn_y=990, pal=dict(bg=(18, 58, 66), bg2=(10, 38, 44), ink=WH, sub=(190, 214, 216), acc=TEAL4, t2=(250, 176, 150), deco=True),
           src="раздел «Na simulação, compare o custo total» (сравнивать по custo total, просить CET — juros, tarifas e seguros) + «Os riscos…» (parcelas baixas por muitos meses)",
           note="тёмно-бирюзовый фон, квиз-крючок «parcela baixa, custo alto?»: предложение по рассрочке с тремя полями «?» без цифр и лупа; верный ответ CET — в статье; без сумм и процентов"),
    c=dict(fn="vs2", title="Boleto da loja ou consórcio?", sub="Compare pelo custo total, não pelo valor da parcela", size=56,
           cols=[("BOLETO DA LOJA", CORAL4, br_art("boleto"),
                  [("O CARRO", "usa desde a compra, vinculado à loja até quitar"), ("CUSTO", "juros embutidos nas parcelas"),
                   ("ATENÇÃO", "atraso pode levar à retomada")]),
                 ("CONSÓRCIO", TEAL4, br_art("cons"),
                  [("O CARRO", "só quando for contemplado"), ("CUSTO", "sem juros: taxa de administração e fundo de reserva"),
                   ("ATENÇÃO", "não há data certa de contemplação")])],
           foot="Peça por escrito o CET", art_h=220, row_size=26,
           src="разделы «Comprar carro no boleto sem financiamento: como funciona» (juros embutidos, reserva de domínio до последней parcela), «Consórcio vale a pena…» (taxa de administração, fundo de reserva, sem data certa), «Os riscos…» (atraso → retomada) и «Na simulação…» (CET por escrito)",
           note="сравнение болето магазина и консорсиума: когда пользуешься машиной, из чего стоимость, главный риск; без сумм, процентов и обещаний одобрения"),
    d=dict(fn="top_scene", scene=br_lot_scene, title="Carro usado parcelado:", title2="o que conferir antes de assinar", size=54, t2k=0.8,
           y=40, btn_x=800, btn_y=1000,
           extra_text="планшет: Antes de assinar, confira: Documento do veículo / IPVA, licenciamento e multas / Gravame ou alienação / Vistoria cautelar / Contrato por escrito",
           src="раздел «O que conferir no carro e no vendedor» (документ, IPVA/licenciamento/multas, gravame/alienação, vistoria cautelar, всё в договоре)",
           note="двор автосалона: б/у хэтчбек без марки и номеров, на переднем плане планшет с чек-листом из 5 пунктов статьи и галочками; без людей, логотипов и «ключей с неба»"),
)


# =====================================================================  5. GB · путешествия · мини-круизы из Ливерпуля
NAVY5 = (18, 40, 72)
SEA5 = (0, 118, 158)
RASP5 = (214, 54, 78)


def anchor_icon(c, cx, cy, s, col):
    c.circle(cx, cy - s * 0.36, s * 0.1, outline=col, width=max(3, s * 0.05))
    c.line([(cx, cy - s * 0.26), (cx, cy + s * 0.36)], col, max(3, s * 0.07))
    c.line([(cx - s * 0.2, cy - s * 0.12), (cx + s * 0.2, cy - s * 0.12)], col, max(3, s * 0.06))
    c.arc((cx - s * 0.36, cy - s * 0.06, cx + s * 0.36, cy + s * 0.4), 20, 160, col, max(3, s * 0.07))
    for k in (-1, 1):
        x = cx + k * s * 0.34
        c.poly([(x, cy + s * 0.04), (x - k * s * 0.02, cy + s * 0.18), (x + k * s * 0.1, cy + s * 0.14)], col)


def small_ship(c, cx, cy, s, hull=NAVY5):
    c.poly([(cx - s * 0.5, cy), (cx + s * 0.5, cy), (cx + s * 0.4, cy + s * 0.2), (cx - s * 0.44, cy + s * 0.2)], hull)
    c.rect((cx - s * 0.36, cy - s * 0.14, cx + s * 0.24, cy + 1), fill=WH, r=2)
    c.rect((cx - s * 0.24, cy - s * 0.26, cx + s * 0.1, cy - s * 0.13), fill=WH, r=2)
    c.rect((cx - s * 0.12, cy - s * 0.4, cx - s * 0.02, cy - s * 0.25), fill=(200, 206, 214))


def route_map(P, t):
    """Схема маршрутов: Ливерпуль-хаб справа, пунктирные линии к 4 карточкам портов слева, у каждой кнопка."""
    p = P["pal"]
    c = C(p["bg"])
    c.vgrad((0, 0, W, W), (226, 241, 249), (198, 226, 242))
    rnd = random.Random(5)
    for _ in range(26):
        x, y = rnd.uniform(0, W), rnd.uniform(240, 1060)
        c.arc((x, y, x + 60, y + 16), 200, 340, WH, 3, alpha=150)
    # условная береговая линия справа (без географической точности)
    land = [(1080, 190), (1010, 240), (980, 330), (1000, 400), (950, 470), (975, 560), (930, 640), (955, 720), (900, 790),
            (925, 860), (960, 930), (940, 1000), (1000, 1080), (1080, 1080)]
    c.poly(land, (236, 228, 206))
    c.line(land[:-1], (214, 202, 176), 4)
    y = head(c, t, p, size=t.get("size", 56))
    hub = (900, 870)
    ports = t["ports"]
    n = len(ports)
    top = y + 26
    g = 22
    ch = (1046 - top - (n - 1) * g) / n
    for k, (name, sub, col) in enumerate(ports):
        y0 = top + k * (ch + g)
        box = (40, y0, 640, y0 + ch)
        ex, ey = box[2], (box[1] + box[3]) / 2
        mx, my = (ex + hub[0]) / 2 + 40, ey - 30 if k < n - 1 else ey
        pts = []
        for i in range(31):
            u = i / 30
            px = (1 - u) ** 2 * hub[0] + 2 * (1 - u) * u * mx + u ** 2 * (ex + 16)
            py = (1 - u) ** 2 * hub[1] + 2 * (1 - u) * u * my + u ** 2 * ey
            pts.append((px, py))
        for i in range(0, 30, 2):
            c.line([pts[i], pts[i + 1]], col, 6)
        c.circle(ex + 16, ey, 12, fill=col, outline=WH, width=4)
        c.card(box, fill=WH, r=22, sh_alpha=60, blur=10, off=(0, 5))
        c.rect((box[0], box[1], box[0] + 16, box[3]), fill=col, r=8)
        c.text((box[0] + 40, box[1] + ch * 0.2), name, "mxb", 36, p["ink"])
        c.block(sub, "msb", 23, box[1] + ch * 0.2 + 50, 560, p["sub"], align="left", x=box[0] + 40, max_lines=1)
        pw = pill_w(c, P, 21, 18)
        cta_pill(c, P, box[2] - 22 - pw / 2, box[3] - 32, size=21, padx=18, pady=9)
    small_ship(c, 760, 760, 70)
    c.circle(hub[0], hub[1], 58, fill=NAVY5, outline=WH, width=6)
    anchor_icon(c, hub[0], hub[1] + 2, 70, WH)
    lw = c.tw("LIVERPOOL", c.font("mxb", 28))[0] + 36
    c.rect((hub[0] - lw / 2, hub[1] + 72, hub[0] + lw / 2, hub[1] + 122), fill=NAVY5, r=25)
    c.text((hub[0], hub[1] + 97), "LIVERPOOL", "mxb", 28, WH, anchor="mm")
    return c


def departures_art(c, box):
    """Табло отправлений (амбер на тёмном): три обычных порта и AMSTERDAM ?"""
    x0, y0, x1, y1 = box
    c.rect(box, fill=(26, 32, 44), r=20)
    c.rect((x0 + 14, y0 + 14, x1 - 14, y1 - 14), fill=(16, 20, 28), r=12)
    amber = (250, 190, 70)
    c.text((x0 + 40, y0 + 34), "DEPARTURES", "anton", 34, amber)
    c.text((x1 - 40, y0 + 34), "FROM LIVERPOOL", "anton", 34, amber, anchor="ra")
    c.line([(x0 + 30, y0 + 86), (x1 - 30, y0 + 86)], (60, 66, 80), 2)
    rows = (("DUBLIN", False), ("BELFAST", False), ("DOUGLAS, ISLE OF MAN", False), ("AMSTERDAM", True))
    rh = (y1 - y0 - 110) / len(rows)
    for k, (dest, q) in enumerate(rows):
        yy = y0 + 96 + k * rh + rh / 2
        c.text((x0 + 40, yy), dest, "anton", 32, (255, 120, 110) if q else amber, anchor="lm")
        if q:
            c.circle(x1 - 70, yy, 22, fill=RASP5)
            c.text((x1 - 70, yy), "?", "mxb", 28, WH, anchor="mm")
        else:
            small_ship(c, x1 - 70, yy - 2, 44, hull=(120, 130, 146))
        # точки «матрицы»
        for i in range(8):
            c.circle(x0 + 520 + i * 22, yy, 3, fill=(60, 66, 80))


def sea_panel(t, box):
    x0, y0, x1, y1 = box
    H = y1 - y0
    t.vgrad((x0, y0, x1, y0 + H * 0.7), (190, 222, 240), (232, 242, 248))
    t.vgrad((x0, y0 + H * 0.7, x1, y1), (60, 140, 180), (30, 100, 146))
    for k in range(5):
        yy = y0 + H * (0.8 + 0.04 * k)
        t.line([(x0 + 20 + k * 37, yy), (x0 + 80 + k * 37, yy)], (200, 230, 244), 3, alpha=150)
        t.line([(x1 - 120 - k * 25, yy + 8), (x1 - 60 - k * 25, yy + 8)], (200, 230, 244), 3, alpha=150)


def ferry(t, x0, base, L):
    """Паром (без ливреи): тёмный низ, белый корпус, надстройка в носовой части, проём автопалубы, серая труба."""
    h = L * 0.2
    hull = [(x0, base - h), (x0 + L * 0.92, base - h), (x0 + L, base - h * 1.12), (x0 + L * 0.94, base), (x0 + L * 0.03, base)]
    t.poly(hull, WH)
    t.poly([(x0 + L * 0.015, base - h * 0.3), (x0 + L * 0.965, base - h * 0.3), (x0 + L * 0.94, base), (x0 + L * 0.03, base)], (70, 76, 88))
    t.rect((x0 + L * 0.02, base - h * 0.85, x0 + L * 0.12, base - h * 0.35), fill=(60, 66, 78), r=3)  # проём кормы
    for k in range(16):
        t.rect((x0 + L * (0.16 + k * 0.047), base - h * 0.74, x0 + L * (0.16 + k * 0.047) + L * 0.022, base - h * 0.56), fill=(120, 150, 180), r=2)
    t.rect((x0 + L * 0.3, base - h * 1.7, x0 + L * 0.86, base - h + 1), fill=WH, r=4)
    for k in range(10):
        t.rect((x0 + L * (0.33 + k * 0.05), base - h * 1.5, x0 + L * (0.33 + k * 0.05) + L * 0.03, base - h * 1.25), fill=(90, 120, 160), r=2)
    t.rect((x0 + L * 0.7, base - h * 2.1, x0 + L * 0.86, base - h * 1.68), fill=WH, r=3)
    t.rect((x0 + L * 0.72, base - h * 1.98, x0 + L * 0.85, base - h * 1.84), fill=(60, 80, 110), r=2)
    t.poly([(x0 + L * 0.44, base - h * 1.7), (x0 + L * 0.54, base - h * 1.7), (x0 + L * 0.53, base - h * 2.35), (x0 + L * 0.45, base - h * 2.35)],
           (206, 210, 216))
    t.rect((x0 + L * 0.45, base - h * 2.42, x0 + L * 0.53, base - h * 2.3), fill=(60, 64, 72), r=2)


def cruise_ship(t, x0, base, L):
    """Лайнер (без ливреи и названия): белый, ряд балконов, шлюпки, белая труба."""
    h = L * 0.13
    t.poly([(x0, base - h), (x0 + L * 0.86, base - h), (x0 + L, base - h * 1.45), (x0 + L * 0.93, base), (x0 + L * 0.04, base)], WH)
    t.poly([(x0 + L * 0.02, base - h * 0.28), (x0 + L * 0.95, base - h * 0.28), (x0 + L * 0.93, base), (x0 + L * 0.04, base)], (44, 58, 84))
    for k in range(26):
        t.circle(x0 + L * (0.06 + k * 0.032), base - h * 0.6, max(1.5, L * 0.005), fill=(120, 150, 180))
    y = base - h
    for a, b, hh in ((0.04, 0.84, 0.5), (0.07, 0.8, 0.48), (0.1, 0.76, 0.46), (0.16, 0.7, 0.44)):
        dh = h * hh
        t.rect((x0 + L * a, y - dh, x0 + L * b, y + 1), fill=WH, r=2)
        n = int((b - a) / 0.022)
        for k in range(n):
            wx = x0 + L * a + L * 0.008 + k * L * 0.022
            t.rect((wx, y - dh * 0.75, wx + L * 0.013, y - dh * 0.3), fill=(110, 140, 176), r=1)
        y -= dh
    for k in range(7):
        bx = x0 + L * (0.14 + k * 0.08)
        t.rect((bx, base - h * 1.3, bx + L * 0.05, base - h * 1.08), fill=(236, 140, 40), r=L * 0.01)
    t.rect((x0 + L * 0.62, y - h * 0.3, x0 + L * 0.72, y + 1), fill=WH, r=2)
    t.poly([(x0 + L * 0.3, y), (x0 + L * 0.4, y), (x0 + L * 0.39, y - h * 0.62), (x0 + L * 0.315, y - h * 0.62)], (230, 232, 236))
    t.rect((x0 + L * 0.315, y - h * 0.7, x0 + L * 0.39, y - h * 0.6), fill=(60, 64, 72), r=2)


def ship_art(kind):
    def art(c, box):
        def fn(t):
            x0, y0, x1, y1 = box
            W_, H = x1 - x0, y1 - y0
            sea_panel(t, box)
            base = y0 + H * 0.8
            if kind == "ferry":
                ferry(t, x0 + W_ * 0.13, base, W_ * 0.74)
            else:
                cruise_ship(t, x0 + W_ * 0.1, base, W_ * 0.78)
        S.clip_draw(c, box, 20, fn)
    return art


def deck_sunset_scene(c):
    """С кормы на закате: удаляющаяся набережная-силуэт, кильватер, поручни, люди разного возраста у борта (со спины)."""
    c.vgrad((0, 0, W, 330), (54, 66, 118), (196, 120, 128))
    c.vgrad((0, 330, W, 560), (196, 120, 128), (252, 196, 140))
    hz = 560
    c.glow((380, 420, 700, 700), (255, 220, 150), alpha=180, blur=50)
    c.circle(540, hz - 10, 64, fill=(255, 226, 160))
    # силуэт набережной (обобщённый)
    sil = (86, 64, 96)
    xs = [(60, 90, 70), (130, 60, 110), (200, 80, 60), (300, 140, 40), (360, 70, 90), (640, 110, 60), (720, 60, 130),
          (800, 90, 80), (900, 70, 100), (980, 100, 60)]
    for x, w, h in xs:
        c.rect((x, hz - h, x + w, hz), fill=sil)
    c.rect((440, hz - 150, 470, hz), fill=sil)
    c.poly([(436, hz - 150), (474, hz - 150), (455, hz - 186)], sil)
    c.pie((600, hz - 150, 680, hz - 70), 180, 360, sil)
    c.rect((600, hz - 110, 680, hz), fill=sil)
    for x in (230, 860):
        c.line([(x, hz), (x, hz - 170)], sil, 6)
        c.line([(x - 60, hz - 160), (x + 50, hz - 170)], sil, 5)
    c.rect((0, hz - 6, W, hz), fill=sil)
    # море и кильватер
    c.vgrad((0, hz, W, W), (226, 150, 130), (40, 70, 110))
    c.poly([(540, hz + 10), (620, W), (460, W)], (250, 236, 220), alpha=70)
    c.poly([(500, hz + 40), (340, W), (260, W)], WH, alpha=110)
    c.poly([(580, hz + 40), (740, W), (820, W)], WH, alpha=110)
    for k in range(8):
        y = hz + 40 + k * 40
        c.line([(540 - 40 - k * 28, y), (540 - 10 - k * 24, y)], (255, 230, 200), 3, alpha=150)
        c.line([(540 + 10 + k * 24, y), (540 + 40 + k * 28, y)], (255, 230, 200), 3, alpha=150)
    # палуба и поручни
    c.rect((0, 900, W, W), fill=(160, 112, 76))
    for k in range(10):
        c.line([(k * 120, 900), (k * 150 - 200, W)], (140, 96, 64), 3)
    c.rect((0, 752, W, 766), fill=(240, 240, 236))
    c.rect((0, 820, W, 828), fill=(220, 220, 214))
    for x in range(20, W, 90):
        c.rect((x, 752, x + 10, 900), fill=(236, 236, 232))
    # люди со спины у поручней (перед поручнями, на палубе)
    people = ((200, 360, (240, 212, 186), (70, 50, 40), "long", (60, 110, 160), (46, 52, 70)),
              (330, 390, (196, 142, 104), (40, 32, 30), "short", (226, 110, 70), (60, 64, 80)),
              (760, 250, (238, 198, 166), (190, 120, 60), "short", (60, 150, 120), (60, 64, 80)),
              (880, 350, (244, 212, 186), (214, 214, 220), "bun", (140, 90, 150), (70, 70, 84)))
    for x, h, skin, hair, kind, top, bottom in people:
        back_person(c, x, 1010, h, skin, hair, kind, top, bottom)


def back_person(c, x, fy, h, skin, hair, kind, top, bottom):
    """Человек со спины: ноги, корпус, руки на поручне, шея, затылок волосами (без лица)."""
    tw = h * 0.15
    hip = fy - h * 0.46
    sh = fy - h * 0.8
    lw = h * 0.07
    for k in (-1, 1):
        c.rect((x + k * lw * 0.75 - lw * 0.55, hip - h * 0.02, x + k * lw * 0.75 + lw * 0.55, fy), fill=bottom, r=lw * 0.3)
    # руки к поручню
    for k in (-1, 1):
        c.line([(x + k * tw * 0.85, sh + h * 0.06), (x + k * tw * 1.25, fy - h * 0.72 + h * 0.2)], top, h * 0.06)
    c.rect((x - tw, sh, x + tw, hip + h * 0.04), fill=top, r=tw * 0.55)
    r = h * 0.085
    c.rect((x - r * 0.4, sh - r * 0.7, x + r * 0.4, sh + r * 0.3), fill=skin)
    hy = sh - r * 1.2
    c.circle(x - r * 0.95, hy + r * 0.1, r * 0.22, fill=skin)
    c.circle(x + r * 0.95, hy + r * 0.1, r * 0.22, fill=skin)
    if kind == "long":
        c.rect((x - r * 1.05, hy, x + r * 1.05, sh + r * 1.4), fill=hair, r=r * 0.5)
    c.circle(x, hy, r, fill=hair)
    if kind == "bun":
        c.circle(x, hy - r * 0.95, r * 0.42, fill=hair)


def plan_chips(c, P):
    items = (("DAY 1", "Board"), ("DAY 2", "Dublin"), ("DAY 3", "Belfast or at sea"), ("DAY 4", "Home"))
    y0, y1 = 236, 330
    g = 16
    n = len(items)
    ws = [180, 190, 330, 180]
    tot = sum(ws) + g * (n - 1)
    x = (W - tot) / 2
    for k, (d, lab) in enumerate(items):
        box = (x, y0, x + ws[k], y1)
        c.shadow(box, r=20, alpha=80, blur=8, off=(0, 5))
        c.rect(box, fill=WH, r=20, alpha=246)
        c.text(((box[0] + box[2]) / 2, y0 + 28), d, "mb", 21, SEA5, anchor="mm")
        c.text(((box[0] + box[2]) / 2, y0 + 62), lab, "mxb", c.fit(lab, "mxb", ws[k] - 24, 1, 28), NAVY5, anchor="mm")
        if k < n - 1:
            arrow_line(c, (box[2] + 2, (y0 + y1) / 2), (box[2] + g - 2, (y0 + y1) / 2), WH, 3, 7, both=False)
        x += ws[k] + g


P5 = dict(bg=(230, 242, 250), ink=NAVY5, sub=(80, 96, 116), acc=SEA5, btn=RASP5, tile=WH, tile_ink=NAVY5, iconbg=(220, 236, 246))
PACKS[5] = dict(
    doc="NT-mini-cruises-liverpool-gb-2026-09-30", cta="Learn more", pal=P5,
    a=dict(fn="route_map", title="Mini cruises from Liverpool 2026:", title2="pick a port", size=52, t2k=1.0,
           ports=[("Greenock", "for day trips to Glasgow and Loch Lomond", (0, 150, 136)),
                  ("Belfast", "Titanic Quarter and the city centre", (236, 140, 40)),
                  ("Douglas, Isle of Man", "the island's capital", (120, 90, 170)),
                  ("Dublin", "Georgian squares, compact centre", (214, 54, 78))],
           src="раздел «Where a mini cruise from Liverpool usually goes» (Dublin, Belfast, Douglas, Greenock — порты, которые часто встречаются в маршрутах)",
           note="схема маршрутов: Ливерпуль-хаб у условного берега, пунктиры к 4 карточкам портов, у каждой «Learn more»; без названий и ливрей круизных и паромных компаний, без цен"),
    b=dict(fn="quiz_art", title="Liverpool to Amsterdam", title2="on a mini cruise?", size=58, t2k=0.9,
           tag="QUIZ", step="Question 1 of 3", art=departures_art, art_h=300, q_size=31,
           q="How often does a cruise from Liverpool call at Amsterdam?",
           opts=["Every weekend", "Only on longer round-Britain cruises", "Every night, by ferry", "Not sure"], opt_layout="2x2", opt_size=27,
           extra_text="табло: DEPARTURES / FROM LIVERPOOL / DUBLIN / BELFAST / DOUGLAS, ISLE OF MAN / AMSTERDAM ?",
           card_bot=912, btn_y=988, pal=dict(bg=(18, 40, 72), bg2=(10, 24, 46), ink=WH, sub=(190, 206, 226), acc=SEA5, t2=(120, 206, 236), deco=True),
           src="раздел «Where a mini cruise from Liverpool usually goes» (Амстердам из Ливерпуля — только в длинных круизах вокруг Британии, паромы в Амстердам — с восточного побережья)",
           note="тёмно-синий фон, табло отправлений (Dublin, Belfast, Douglas и «AMSTERDAM ?») и квиз с неожиданным ответом из статьи"),
    c=dict(fn="vs2", title="Ferry break or cruise ship?", sub="Two kinds of mini cruise from Liverpool", size=58,
           cols=[("FERRY BREAK", (60, 76, 100), ship_art("ferry"),
                  [("NIGHTS", "often a night on board"), ("ON BOARD", "restaurants, a bar and cabins"),
                   ("ASHORE", "a few hours or a full day")]),
                 ("CRUISE SHIP", SEA5, ship_art("cruise"),
                  [("NIGHTS", "two to four nights"), ("ON BOARD", "meals, entertainment and cabin in the fare"),
                   ("ASHORE", "one or more ports")])],
           foot="Ferry break: simpler, and usually costs less", art_h=230,
           src="раздел «Two kinds of mini cruise: ferry break or cruise ship» (ночь на борту, рестораны/бар/каюты, несколько часов или день на берегу; 2–4 ночи, питание и шоу в стоимости, один или несколько портов; паром проще и обычно дешевле)",
           note="сравнение: паром и лайнер без ливреи, логотипов и узнаваемых силуэтов; без цен и «all inclusive»"),
    d=dict(fn="top_scene", scene=deck_sunset_scene, title="Mini cruise from Liverpool:", title2="a simple three-night plan", size=56,
           y=44, chips=plan_chips, btn_y=1000,
           extra_text="план: DAY 1 Board / DAY 2 Dublin / DAY 3 Belfast or at sea / DAY 4 Home", pal=dict(ink=WH, sub=(250, 230, 220), t2=(255, 214, 160)),
           src="разделы «A simple three-night plan» (Day 1 board, Day 2 Dublin, Day 3 Belfast/Douglas or a day at sea, Day 4 home) и «sailing out past the waterfront is one of the highlights»",
           note="закат с кормы: обобщённый силуэт набережной, кильватер, у поручней люди разного возраста со спины; полоса-план из 4 дней; без названия судна, возраста 60+ и цен"),
)


# =====================================================================  сборка
def texts(t, cta):
    parts = [t.get("kicker", ""), t.get("title", "")]
    if t.get("title2"):
        parts.append(t["title2"])
    if t.get("sub"):
        parts.append(t["sub"])
    for k in ("tag", "step", "q"):
        if t.get(k):
            parts.append(t[k])
    if t.get("tiles"):
        tl = []
        for x in t["tiles"]:
            if isinstance(x, tuple) and len(x) == 3:
                tl.append(" – ".join(v for v in x[1:] if v))
            elif isinstance(x, tuple):
                tl.append(" – ".join(v for v in x if v))
        parts.append(" / ".join(tl) + f" (у каждой «{cta}»)")
    if t.get("opts"):
        ol = []
        for o in t["opts"]:
            ol.append(" – ".join(o[1:]) if isinstance(o, tuple) else o)
        parts.append(" / ".join(ol))
    if t.get("cols"):
        for name, _, _, rows in t["cols"]:
            parts.append(name + ": " + "; ".join(f"{a} — {b}" for a, b in rows))
    if t.get("ports"):
        parts.append("LIVERPOOL / " + " / ".join(f"{a} – {b}" for a, b, _ in t["ports"]) + f" (у каждой «{cta}»)")
    if t.get("callouts"):
        parts.append(" / ".join(f"{k + 1}. {x[0]}" for k, x in enumerate(t["callouts"])))
    if t.get("extra_text"):
        parts.append(t["extra_text"])
    if t.get("foot"):
        parts.append(t["foot"])
    if t["fn"] not in ("row4_hero", "grid2x2_art", "route_map"):
        parts.append(f"кнопка «{cta} →»")
    return " / ".join(p_ for p_ in parts if p_).replace("\n", " ").replace("\u00a0", " ")


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
    os.makedirs(os.path.join(OUT6, doc), exist_ok=True)
    with open(os.path.join(OUT6, doc, "creatives.json"), "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    args = sys.argv[1:] or [str(k) for k in PACKS]
    for a in args:
        if ":" in a:
            n, ls = a.split(":")
            build(int(n), ls.replace(",", ""))
        else:
            build(int(a))
