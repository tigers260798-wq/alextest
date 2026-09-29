"""Свои раскладки пакетов волны 2 (w2b, 30.09) — там, где общих шаблонов p60_templates мало:
  month_bars  — «год пенсии по месяцам» (ES paga extra, концепция c);
  bill        — счёт за свет с «? €» (ES bono social, c);
  price_tags  — ценники «? €» на трёх вариантах (ES vista cansada, c);
  tower       — «из чего складывается» столбик блоков (PL dodatki, c);
  floorplans  — два плана одной комнаты (ES muebles, c);
  laptop_grid — сетка курсов на экране ноутбука (ES informática, a);
  style_grid  — сетка стилей-«товаров» (ES muebles, a);
  poll        — опрос «A или B» (ES muebles, b);
  scene_d     — сцена + заголовок: 'band' / 'top' / 'card' / 'bottomcard' / 'bars' / 'left'.
Цифры, которых нет в гипотезе, — «?»."""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from p60_lib import C, W, mix, rotpts
import p60_icons as I
import p60_scenes as S
import p60_templates as T
import w2b_scenes as WS

WH = (255, 255, 255)


def icon(c, name, cx, cy, s, col, bg=WH, **kw):
    I.ICONS[name](c, cx, cy, s, col, bg=bg, **kw)


def _bg(c, p):
    if p.get("bg2"):
        c.vgrad((0, 0, W, W), p["bg"], p["bg2"])


# ===================================================================== month_bars
def month_bars(P, t):
    p = P["pal"]
    c = C(p["bg"])
    _bg(c, p)
    y = T.header(c, t, col=p["ink"], sub_col=p["sub"], size=t.get("size", 60))
    box = (60, y + 28, 1020, 868)
    c.card(box, r=28, sh_alpha=60, blur=14, off=(0, 8))
    months = t["months"]
    extra = set(t["extra"])
    x0, x1 = box[0] + 40, box[2] - 40
    base_y = box[3] - 80
    cw = (x1 - x0) / 12
    bh = (base_y - box[1] - 150) * 0.5
    for i, m in enumerate(months):
        cx = x0 + cw * (i + 0.5)
        bw = cw * 0.66
        c.rect((cx - bw / 2, base_y - bh, cx + bw / 2, base_y), fill=p["bar"], r=8)
        if i in extra:
            eh = bh * 0.8
            eb = (cx - bw / 2, base_y - bh - eh - 8, cx + bw / 2, base_y - bh - 8)
            c.rect(eb, fill=p["acc"], r=8)
            for k in range(0, int(eh) - 16, 22):
                c.line([(eb[0] + 4, eb[1] + k + 18), (eb[2] - 4, eb[1] + k + 2)], WH, 3, alpha=70)
            c.circle(cx, eb[1] + eh / 2, 28, fill=WH)
            c.text((cx, eb[1] + eh / 2 + 1), "?", "db", 36, p["acc"], anchor="mm")
            c.text((cx, eb[1] - 40), t["extra_label"], "sb", 22, p["acc"], anchor="mm")
            c.poly([(cx - 10, eb[1] - 22), (cx + 10, eb[1] - 22), (cx, eb[1] - 8)], p["acc"])
        c.text((cx, base_y + 34), m, "sb", 24, (60, 64, 74) if i not in extra else p["acc"], anchor="mm")
    c.line([(x0, base_y), (x1, base_y)], (200, 204, 212), 3)
    # легенда
    ly = box[1] + 44
    c.rect((x0, ly - 14, x0 + 28, ly + 14), fill=p["bar"], r=6)
    c.text((x0 + 42, ly), t["leg1"], "s", 26, (60, 64, 74), anchor="lm")
    lx = x0 + 42 + c.tw(t["leg1"], c.font("s", 26))[0] + 40
    c.rect((lx, ly - 14, lx + 28, ly + 14), fill=p["acc"], r=6)
    c.text((lx + 42, ly), t["leg2"], "s", 26, (60, 64, 74), anchor="lm")
    if t.get("foot"):
        c.block(t["foot"], "sb", 34, 886, 980, p["ink"], max_lines=1)
    c.button(P["cta"], W / 2, 994, size=42, fill=p["btn"])
    return c


# ===================================================================== bill
def bill(P, t):
    p = P["pal"]
    c = C(p["bg"])
    _bg(c, p)
    y = T.header(c, t, col=p["ink"], sub_col=p["sub"], size=t.get("size", 58))
    box = (150, y + 30, 930, 856)
    c.shadow(box, r=10, alpha=90, blur=16, off=(0, 10))
    c.rect(box, fill=WH, r=10)
    c.rect((box[0], box[1], box[2], box[1] + 86), fill=p["acc"], r=10)
    c.rect((box[0], box[1] + 50, box[2], box[1] + 86), fill=p["acc"])
    icon(c, "bolt", box[0] + 56, box[1] + 43, 54, (255, 214, 80))
    c.text((box[0] + 96, box[1] + 43), t["bill"], "db", 32, WH, anchor="lm")
    c.text((box[2] - 36, box[1] + 43), t.get("bill_r", ""), "s", 28, WH, anchor="rm")
    for x in range(int(box[0]) + 20, int(box[2]) - 10, 28):
        c.circle(x, box[3], 7, fill=p["bg2"] if p.get("bg2") else p["bg"])
    rows = t["rows"]
    top = box[1] + 120
    rh = min(84, (box[3] - 40 - top) / (len(rows) + 1.3))
    xl, xr = box[0] + 44, box[2] - 44
    for k, (lab, val, hl) in enumerate(rows):
        ry = top + k * rh + rh / 2
        col = p["hlc"] if hl else (50, 54, 64)
        if hl:
            c.rect((xl - 16, ry - rh * 0.36, xr + 16, ry + rh * 0.36), fill=p["hl"], r=10, alpha=200)
        c.text((xl, ry), lab, "sb" if hl else "s", 32, col, anchor="lm")
        tw_ = c.tw(lab, c.font("sb" if hl else "s", 32))[0]
        vw = c.tw(val, c.font("db", 34))[0]
        for dx in range(int(xl + tw_ + 20), int(xr - vw - 20), 16):
            c.circle(dx, ry + 8, 2.4, fill=(180, 184, 192))
        c.text((xr, ry), val, "db", 34, col, anchor="rm")
    # итог
    ty = top + len(rows) * rh + 20
    c.line([(xl, ty - 10), (xr, ty - 10)], (60, 64, 74), 3)
    c.text((xl, ty + rh / 2 - 6), t["total"], "db", 40, (30, 34, 44), anchor="lm")
    c.text((xr, ty + rh / 2 - 6), "? €", "db", 48, p["btn"], anchor="rm")
    if t.get("sticker"):
        sr = 86
        sx, sy = box[2] - 30, box[1] + 10
        c.shadow((sx - sr, sy - sr, sx + sr, sy + sr), r=sr, alpha=90, blur=10, off=(0, 8))
        c.circle(sx, sy, sr, fill=p["sticker"])
        c.circle(sx, sy, sr - 10, outline=WH, width=3)
        c.block(t["sticker"], "db", 30, sy - 40, sr * 1.5, (30, 34, 44), cx=sx, max_lines=3, gap=1.02)
    if t.get("foot"):
        c.block(t["foot"], "sb", 32, 890, 980, p["ink"], max_lines=1)
    c.button(P["cta"], W / 2, 996, size=40, fill=p["btn"])
    return c


# ===================================================================== price_tags
def price_tag(c, cx, cy, w, h, col, ang, label, ic, price="? €", ic_col=None):
    """Ценник: рисуется на отдельном холсте и поворачивается."""
    from PIL import Image
    t = C((0, 0, 0), K=c.K)
    t.im = Image.new("RGBA", (c.s(w + 40), c.s(h + 40)), (0, 0, 0, 0))
    ox, oy = 20, 20
    pts = [(ox + h * 0.42, oy), (ox + w, oy), (ox + w, oy + h), (ox + h * 0.42, oy + h), (ox, oy + h / 2)]
    t.poly(pts, col)
    t.circle(ox + h * 0.3, oy + h / 2, 13, fill=(250, 248, 244))
    t.circle(ox + h * 0.3, oy + h / 2, 13, outline=mix(col, (0, 0, 0), 0.3), width=3)
    icx = ox + h * 0.42 + h * 0.62
    t.circle(icx, oy + h / 2, h * 0.36, fill=WH)
    I.ICONS[ic](t, icx, oy + h / 2, h * 0.5, ic_col or col, bg=WH)
    tx = icx + h * 0.5
    t.text((tx, oy + h * 0.36), price, "db", h * 0.3, WH, anchor="lm")
    t.block(label, "sb", 32, oy + h * 0.56, ox + w - tx - 24, WH, align="left", x=tx, max_lines=2, gap=1.05)
    rot = t.im.rotate(-ang, expand=True, resample=Image.BICUBIC)
    sh = Image.new("RGBA", rot.size, (0, 0, 0, 0))
    sh.putalpha(rot.getchannel("A").point(lambda v: v * 70 // 255))
    X, Y = c.s(cx), c.s(cy)
    c.im.alpha_composite(sh, (X - rot.width // 2 + 8 * c.K, Y - rot.height // 2 + 12 * c.K))
    c.im.alpha_composite(rot, (X - rot.width // 2, Y - rot.height // 2))


def price_tags(P, t):
    p = P["pal"]
    c = C(p["bg"])
    _bg(c, p)
    y = T.header(c, t, col=p["ink"], sub_col=p["sub"], size=t.get("size", 58))
    tags = t["tags"]
    n = len(tags)
    top = y + 34
    bot = 876
    h = min(190, (bot - top - 26 * (n - 1)) / n)
    top += (bot - top - (h * n + 26 * (n - 1))) / 2
    for k, (ic, lab, col) in enumerate(tags):
        cy = top + k * (h + 26) + h / 2
        ang = (-2.5, 2, -1.5)[k % 3]
        cx = 540 + (-20, 20, -6)[k % 3]
        hx = cx - 380 + h * 0.3
        c.arc((hx - 70, cy - 60, hx + 10, cy + 10), 150, 350, (120, 110, 100), 4)
        price_tag(c, cx, cy, 760, h, col, ang, lab, ic)
    if t.get("foot"):
        c.block(t["foot"], "sb", 32, 900, 980, p["ink"], max_lines=1)
    c.button(P["cta"], W / 2, 998, size=40, fill=p["btn"])
    return c


# ===================================================================== tower
def tower(P, t):
    p = P["pal"]
    c = C(p["bg"])
    _bg(c, p)
    y = T.header(c, t, col=p["ink"], sub_col=p["sub"], size=t.get("size", 56))
    blocks = t["blocks"]  # снизу вверх: (label, height, color)
    bot = 870
    x0, x1 = 90, 990
    gap = 12
    total_h = sum(b[1] for b in blocks) + gap * (len(blocks) - 1)
    top_avail = y + 40
    scale = min(1.0, (bot - top_avail) / total_h)
    yy = bot
    for k, (lab, h, col, val) in enumerate(blocks):
        h *= scale
        inset = k * 26
        box = (x0 + inset, yy - h, x1 - inset, yy)
        c.shadow(box, r=18, alpha=60, blur=8, off=(0, 6))
        c.rect(box, fill=col, r=18)
        ink = WH if sum(col) < 460 else (30, 34, 44)
        cy = (box[1] + box[3]) / 2
        c.text((box[0] + 36, cy), lab, "db", t.get("lab_size", 36) if k == 0 else 32, ink, anchor="lm")
        if val == "?":
            c.circle(box[2] - 60, cy, 30, fill=WH)
            c.text((box[2] - 60, cy + 1), "?", "db", 38, col, anchor="mm")
            c.text((box[2] - 104, cy), t.get("unit", ""), "sb", 30, ink, anchor="rm")
        if k > 0:
            c.circle(box[0] - 2, cy, 22, fill=p["acc"])
            c.text((box[0] - 2, cy + 1), "+", "db", 30, WH, anchor="mm")
        yy -= h + gap
    if t.get("foot"):
        c.block(t["foot"], "sb", 34, 890, 980, p["ink"], max_lines=1, highlight=p.get("hl"), hl_pad=8)
    c.button(P["cta"], W / 2, 994, size=40, fill=p["btn"])
    return c


# ===================================================================== floorplans
def _plan(c, box, variant, p):
    x0, y0, x1, y1 = box
    c.rect(box, fill=(250, 246, 238), r=6)
    c.rect(box, outline=(60, 60, 66), width=10, r=6)
    # дверь и окно
    c.rect((x0 + 30, y1 - 6, x0 + 120, y1 + 6), fill=(250, 246, 238))
    c.arc((x0 + 30, y1 - 90, x0 + 210, y1 + 90), 270, 360, (150, 150, 160), 3)
    c.rect((x1 - 170, y0 - 7, x1 - 40, y0 + 7), fill=(170, 210, 236))
    SOFA, TAB, RUG, SH = p["sofa"], (170, 124, 84), (230, 214, 190), (140, 104, 72)
    w, h = x1 - x0, y1 - y0
    if variant == "A":
        c.rect((x0 + w * 0.12, y0 + h * 0.36, x0 + w * 0.88, y0 + h * 0.78), fill=RUG, r=10)
        c.rect((x0 + 20, y0 + h * 0.3, x0 + 20 + w * 0.2, y0 + h * 0.84), fill=SOFA, r=14)
        c.rect((x0 + w * 0.38, y0 + h * 0.46, x0 + w * 0.58, y0 + h * 0.68), fill=TAB, r=8)
        c.rect((x1 - 20 - w * 0.1, y0 + h * 0.2, x1 - 20, y0 + h * 0.9), fill=SH, r=6)
        c.rect((x0 + w * 0.3, y0 + 20, x0 + w * 0.62, y0 + 20 + h * 0.12), fill=SH, r=6)
        c.circle(x1 - w * 0.3, y0 + h * 0.2, w * 0.07, fill=(90, 150, 100))
    else:
        c.rect((x0 + w * 0.3, y0 + h * 0.3, x1 - 30, y1 - 40), fill=RUG, r=10)
        c.rect((x0 + 20, y0 + h * 0.32, x0 + 20 + w * 0.18, y1 - 20), fill=SOFA, r=14)
        c.rect((x0 + 20, y1 - 20 - h * 0.18, x0 + w * 0.62, y1 - 20), fill=SOFA, r=14)
        c.circle(x0 + w * 0.46, y0 + h * 0.58, w * 0.09, fill=TAB)
        c.rect((x1 - 20 - w * 0.08, y0 + h * 0.28, x1 - 20, y0 + h * 0.62), fill=SH, r=6)
        c.rect((x0 + 20, y0 + 20, x0 + w * 0.4, y0 + 20 + h * 0.1), fill=SH, r=6)
        c.circle(x1 - w * 0.2, y1 - h * 0.18, w * 0.07, fill=(90, 150, 100))


def floorplans(P, t):
    p = P["pal"]
    c = C(p["bg"])
    _bg(c, p)
    y = T.header(c, t, col=p["ink"], sub_col=p["sub"], size=t.get("size", 56))
    top = y + 40
    for k, (lab, sub) in enumerate(t["plans"]):
        x0 = 60 + k * 500
        card = (x0, top, x0 + 460, 870)
        c.card(card, r=26, sh_alpha=60, blur=12, off=(0, 8))
        c.circle(x0 + 60, top + 56, 34, fill=p["acc"])
        c.text((x0 + 60, top + 57), lab, "db", 38, WH, anchor="mm")
        c.block(sub, "sb", 28, top + 34, 340, (40, 44, 54), align="left", x=x0 + 110, max_lines=2, gap=1.05)
        _plan(c, (x0 + 40, top + 130, x0 + 420, 840), lab, p)
    c.circle(W / 2, (top + 870) / 2, 40, fill=WH, outline=(200, 205, 212), width=3)
    c.text((W / 2, (top + 870) / 2), "vs", "db", 28, (90, 96, 106), anchor="mm")
    if t.get("foot"):
        c.block(t["foot"], "sb", 34, 892, 980, p["ink"], max_lines=1, highlight=p.get("hl"), hl_pad=8)
    c.button(P["cta"], W / 2, 994, size=40, fill=p["btn"])
    return c


# ===================================================================== laptop_grid
def laptop_grid(P, t):
    p = P["pal"]
    c = C(p["bg"])
    _bg(c, p)
    c.dots((0, 0, W, W), 46, 3, WH, alpha=24)
    y = T.header(c, t, col=p["ink"], sub_col=p["sub"], size=t.get("size", 58))
    lx0, lx1, ly0, ly1 = 70, 1010, y + 30, 1000
    c.shadow((lx0, ly0, lx1, ly1), r=30, alpha=110, blur=20, off=(0, 12))
    c.rect((lx0, ly0, lx1, ly1 - 40), fill=(44, 50, 64), r=30)
    c.poly([(lx0 - 50, ly1 - 44), (lx1 + 50, ly1 - 44), (lx1 + 20, ly1), (lx0 - 20, ly1)], (90, 96, 110))
    scr = (lx0 + 24, ly0 + 24, lx1 - 24, ly1 - 64)
    c.rect(scr, fill=(244, 247, 251), r=10)
    # «браузер»
    c.rect((scr[0], scr[1], scr[2], scr[1] + 44), fill=(226, 232, 240), r=10)
    c.rect((scr[0], scr[1] + 30, scr[2], scr[1] + 44), fill=(226, 232, 240))
    for k, col in enumerate(((236, 96, 90), (246, 190, 60), (90, 190, 100))):
        c.circle(scr[0] + 28 + k * 26, scr[1] + 22, 8, fill=col)
    c.rect((scr[0] + 120, scr[1] + 10, scr[2] - 30, scr[1] + 34), fill=WH, r=12)
    tiles = t["tiles"]
    g = 20
    tx0, ty0 = scr[0] + 24, scr[1] + 64
    tw = (scr[2] - scr[0] - 48 - g) / 2
    th = (scr[3] - ty0 - 22 - g) / 2
    for i, (ic, lab) in enumerate(tiles):
        x = tx0 + (i % 2) * (tw + g)
        yy = ty0 + (i // 2) * (th + g)
        c.rect((x, yy, x + tw, yy + th), fill=WH, r=18, outline=(214, 222, 232), width=3)
        c.circle(x + 84, yy + th / 2 - 10, 54, fill=mix(p["acc"], WH, 0.85))
        icon(c, ic, x + 84, yy + th / 2 - 10, 80, p["acc"], bg=mix(p["acc"], WH, 0.85))
        c.block(lab, "db", 30, yy + 34, tw - 170, (30, 40, 60), align="left", x=x + 156, max_lines=2, gap=1.05)
        c.pill(P["cta"], x + 156 + 100, yy + th - 44, size=21, fill=p["btn"], padx=18, pady=9)
    return c


# ===================================================================== style_grid (товарка)
def mini_room(c, box, style):
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    wall, floor, sofa, leg, deco = style["wall"], style["floor"], style["sofa"], style["leg"], style["deco"]
    c.rect((x0, y0, x1, y0 + h * 0.72), fill=wall)
    c.rect((x0, y0 + h * 0.72, x1, y1), fill=floor)
    if style.get("brick"):
        for r_ in range(7):
            for q in range(8):
                bx = x0 + q * w / 7 - (w / 14 if r_ % 2 else 0)
                by = y0 + 8 + r_ * h * 0.1
                c.rect((bx + 3, by, bx + w / 7 - 3, by + h * 0.1 - 5), fill=mix(wall, (0, 0, 0), 0.08), r=2)
    cx = (x0 + x1) / 2
    sy = y0 + h * 0.72
    low = style.get("low", False)
    sh = h * (0.18 if low else 0.26)
    c.rect((cx - w * 0.34, sy - sh - h * 0.06, cx + w * 0.34, sy - h * 0.06), fill=sofa, r=16)
    c.rect((cx - w * 0.38, sy - sh * 0.6 - h * 0.06, cx - w * 0.28, sy - h * 0.02), fill=mix(sofa, (0, 0, 0), 0.12), r=12)
    c.rect((cx + w * 0.28, sy - sh * 0.6 - h * 0.06, cx + w * 0.38, sy - h * 0.02), fill=mix(sofa, (0, 0, 0), 0.12), r=12)
    c.rect((cx - w * 0.3, sy - h * 0.1, cx + w * 0.3, sy - h * 0.01), fill=mix(sofa, WH, 0.15), r=10)
    for x in (cx - w * 0.32, cx + w * 0.32):
        c.rect((x - 4, sy - h * 0.02, x + 4, sy + h * 0.04), fill=leg)
    if style.get("tall"):
        c.rect((x0 + w * 0.02, y0 + h * 0.06, x0 + w * 0.2, sy + h * 0.02), fill=(60, 44, 36), r=6)
        for k in range(4):
            yy = y0 + h * (0.2 + k * 0.14)
            c.rect((x0 + w * 0.03, yy, x0 + w * 0.19, yy + 4), fill=(40, 30, 24))
        c.rect((x1 - w * 0.2, y0 + h * 0.1, x1 - w * 0.03, sy + h * 0.02), fill=(70, 50, 40), r=6)
        c.line([(x1 - w * 0.115, y0 + h * 0.12), (x1 - w * 0.115, sy)], (50, 36, 28), 3)
    kind = style["kind"]
    if kind == "plant":
        S.plant(c, x1 - w * 0.12, sy + h * 0.06, h * 0.0016, pot=(240, 240, 240), leaf=(70, 140, 90))
        c.circle(x0 + w * 0.2, y0 + h * 0.2, w * 0.08, fill=deco)
    elif kind == "frame":
        c.rect((cx - w * 0.14, y0 + h * 0.1, cx + w * 0.14, y0 + h * 0.3), fill=WH, outline=(40, 40, 44), width=4)
        c.line([(cx - w * 0.08, y0 + h * 0.26), (cx, y0 + h * 0.16), (cx + w * 0.08, y0 + h * 0.26)], deco, 5)
    elif kind == "lamp":
        c.line([(x1 - w * 0.12, sy + h * 0.04), (x1 - w * 0.12, y0 + h * 0.2)], (40, 40, 44), 6)
        c.poly([(x1 - w * 0.2, y0 + h * 0.2), (x1 - w * 0.04, y0 + h * 0.2), (x1 - w * 0.08, y0 + h * 0.1), (x1 - w * 0.16, y0 + h * 0.1)], deco)
        c.rect((x0 + w * 0.08, y0 + h * 0.12, x0 + w * 0.34, y0 + h * 0.15), fill=(60, 60, 64))
    elif kind == "japandi":
        c.circle(cx, y0 + h * 0.22, w * 0.12, fill=deco)
        c.rect((x0 + w * 0.06, sy - h * 0.18, x0 + w * 0.16, sy + h * 0.04), fill=(196, 160, 116), r=6)
        c.line([(x0 + w * 0.11, sy - h * 0.18), (x0 + w * 0.11, sy - h * 0.32)], (90, 110, 80), 4)


def style_grid(P, t):
    p = P["pal"]
    c = C(p["bg"])
    _bg(c, p)
    y = T.header(c, t, col=p["ink"], sub_col=p["sub"], size=t.get("size", 60))
    top = y + 28
    g = 24
    tw = (960 - g) / 2
    th = (1044 - top - g) / 2
    for i, (lab, st) in enumerate(t["tiles"]):
        x0 = 60 + (i % 2) * (tw + g)
        y0 = top + (i // 2) * (th + g)
        box = (x0, y0, x0 + tw, y0 + th)
        c.card(box, r=24, sh_alpha=60, blur=12, off=(0, 6))
        img = (x0 + 14, y0 + 14, x0 + tw - 14, y0 + th - 112)
        S.clip_draw(c, img, 16, lambda tt, b=img, s_=st: mini_room(tt, b, s_))
        c.text((x0 + 28, y0 + th - 80), lab, "db", 30, p["tile_ink"], anchor="lm")
        pb = c.pill(P["cta"], 0, -500, size=19, fill=p["btn"], padx=14, pady=9)
        pw = pb[2] - pb[0]
        c.pill(P["cta"], x0 + tw - 20 - pw / 2, y0 + th - 78, size=19, fill=p["btn"], padx=14, pady=9)
        c.text((x0 + 30, y0 + th - 34), st.get("tag", ""), "s", 23, (110, 116, 124), anchor="lm")
    return c


# ===================================================================== poll
def poll(P, t):
    p = P["pal"]
    c = C(p["bg"])
    _bg(c, p)
    y = T.header(c, t, col=p["ink"], sub_col=p["sub"], size=t.get("size", 58))
    box = (60, y + 30, 1020, 900)
    c.card(box, r=34, sh_alpha=90, blur=18)
    x0, x1 = box[0] + 36, box[2] - 36
    c.text((x0, box[1] + 42), t["tag"], "sb", 26, p["acc"], anchor="lm")
    c.text((x1, box[1] + 42), t["step"], "s", 26, (110, 116, 124), anchor="rm")
    g = 24
    ow = (x1 - x0 - g) / 2
    oy0 = box[1] + 80
    oy1 = box[3] - 150
    for k, (lab, st) in enumerate(t["opts"]):
        ox = x0 + k * (ow + g)
        img = (ox, oy0, ox + ow, oy1)
        S.clip_draw(c, img, 18, lambda tt, b=img, s_=st: mini_room(tt, b, s_))
        c.circle(ox + 44, oy0 + 44, 30, fill=p["acc"])
        c.text((ox + 44, oy0 + 45), "AB"[k], "db", 32, WH, anchor="mm")
        # строка опроса
        by = box[3] - 124
        c.rect((ox, by, ox + ow, by + 60), fill=(242, 244, 247), r=30, outline=(210, 214, 220), width=3)
        c.block(lab, "sb", 26, by + 14, ow - 110, (40, 44, 54), align="left", x=ox + 24, max_lines=1)
        c.text((ox + ow - 30, by + 30), "?%", "db", 28, p["acc"], anchor="rm")
        c.text((ox + ow / 2, box[3] - 40), st.get("note", ""), "s", 22, (110, 116, 124), anchor="mm")
    c.button(P["cta"], W / 2, 980, size=42, fill=p["btn"])
    return c


# ===================================================================== scene_d
def scene_d(P, t):
    p = P["pal"]
    cta = P["cta"]
    c = C(WH)
    getattr(WS, t["scene"])(c, **t.get("scene_kw", {}))
    style = t["style"]
    if style == "band":
        bh = t.get("band_h", 300)
        c.rect((0, 0, W, bh), fill=p["band"], alpha=t.get("band_alpha", 255))
        y = c.block(t["title"], "db", t.get("size", 62), 40, 980, p["band_ink"], max_lines=t.get("lines", 2))
        if t.get("sub"):
            c.block(t["sub"], "s", 32, y + 10, 960, p["band_sub"], max_lines=2)
    elif style == "top":
        y = t.get("y", 48)
        if t.get("kicker"):
            c.text((W / 2, y + 16), t["kicker"], "sb", 26, p["acc"], anchor="mm")
            y += 50
        y = c.block(t["title"], "db", t.get("size", 62), y, t.get("max_w", 980), p["ink"], max_lines=t.get("lines", 2), highlight=t.get("hl"), hl_pad=10)
        if t.get("sub"):
            y = c.block(t["sub"], "s", t.get("sub_size", 32), y + 12, 960, p["sub"], max_lines=2)
    elif style in ("card", "bottomcard"):
        box = t["card_box"]
        c.shadow(box, r=26, alpha=110, blur=18, off=(0, 10))
        c.rect(box, fill=WH, r=26, alpha=t.get("card_alpha", 250))
        if t.get("frame"):
            c.rect((box[0] + 14, box[1] + 14, box[2] - 14, box[3] - 14), outline=p["frame"], width=3, r=18)
        cx = (box[0] + box[2]) / 2
        y = box[1] + t.get("pad", 44)
        if t.get("kicker"):
            y = c.block(t["kicker"], "sb", 26, y, box[2] - box[0] - 100, p["acc"], cx=cx, max_lines=1) + 8
        y = c.block(t["title"], t.get("font", "db"), t.get("size", 60), y, box[2] - box[0] - 90, p["ink"], cx=cx, max_lines=t.get("lines", 2), gap=1.08)
        if t.get("sub"):
            y = c.block(t["sub"], "s", t.get("sub_size", 32), y + 10, box[2] - box[0] - 110, p["sub"], cx=cx, max_lines=2,
                        highlight=None)
        c.button(cta, cx, box[3] - t.get("btn_off", 66), size=t.get("btn_size", 40), fill=p["btn"])
        return c
    elif style in ("bars", "left"):
        if t.get("veil"):
            vb = t["veil"]
            c.shadow(vb, r=26, alpha=90, blur=18, off=(0, 10))
            c.rect(vb, fill=WH, r=26, alpha=t.get("veil_alpha", 236))
        align = "left" if style == "left" else "center"
        x = t.get("x", 60)
        y = c.bars(t["bars"], t.get("y", 40), size=t.get("bar_size", 80), cond=t.get("cond", 0.8), align=align, x=x,
                   max_w=t.get("max_w", 980), gap=t.get("gap", 8))
        bb = c.button(cta, 0, -600, size=t.get("btn_size", 44), fill=p["btn"], padx=56, pady=22)
        bw = bb[2] - bb[0]
        bx = W / 2 if align == "center" else x - 18 + bw / 2
        c.button(cta, bx, t.get("btn_y", y + 60), size=t.get("btn_size", 44), fill=p["btn"], padx=56, pady=22,
                 grad=(mix(p["btn"], WH, 0.35), p["btn"]), outline=WH)
        return c
    bx = t.get("btn_x", W / 2)
    if t.get("btn_x") is not None and t.get("btn_left"):
        bb = c.button(cta, 0, -600, size=t.get("btn_size", 44), fill=p["btn"])
        bx = t["btn_x"] + (bb[2] - bb[0]) / 2
    c.button(cta, bx, t.get("btn_y", 990), size=t.get("btn_size", 44), fill=p["btn"])
    return c
