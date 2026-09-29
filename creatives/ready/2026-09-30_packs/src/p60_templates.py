"""Четыре общих шаблона на все пакеты 30.09:
  a — сетка выбора (fake interactivity): '2x2', 'row4', 'list4', 'row2';
  b — карточка-опросник: 'card', 'phone', 'card2x2', 'calc';
  c — «сколько стоит / сравнение»: 'twocol', 'split', 'table', 'bars', 'stacked';
  d — сцена-иллюстрация: заголовок 'top' / 'card' / 'bars' / 'chalk' / 'left' поверх своей сцены.
Каждый пакет задаёт палитру и тексты в p60_packs.py."""
from p60_lib import C, W, mix
import p60_icons as I
import p60_scenes as S

WH = (255, 255, 255)


def icon(c, name, cx, cy, s, col, bg=WH):
    I.ICONS[name](c, cx, cy, s, col, bg=bg)


def header(c, t, y=46, col=(30, 30, 40), sub_col=(90, 96, 106), size=64, sub_size=32, maxw=980, lines=2,
           t2_col=None, hl=None, align="center", x=None):
    y = c.block(t["title"], "db", size, y, maxw, col, max_lines=lines, align=align, x=x)
    if t.get("title2"):
        y = c.block(t["title2"], "db", int(size * 0.86), y + (10 if hl else 2), maxw, t2_col or col, max_lines=1, highlight=hl, hl_pad=10,
                    align=align, x=x)
    if t.get("sub"):
        y = c.block(t["sub"], "s", sub_size, y + 10, maxw, sub_col, max_lines=2, align=align, x=x)
    return y


# =====================================================================  A: сетка выбора
def grid(P, t):
    p = P["pal"]
    c = C(p["bg"])
    if p.get("bg2"):
        c.vgrad((0, 0, W, W), p["bg"], p["bg2"])
    lay = t["layout"]
    y = header(c, t, col=p["ink"], sub_col=p["sub"], size=t.get("size", 64), t2_col=p.get("acc"))
    tiles = t["tiles"]
    cta = P["cta"]
    if lay == "2x2":
        top = y + 30
        g = 24
        tw = (960 - g) / 2
        th = (1044 - top - g) / 2
        for i, (ic, lab) in enumerate(tiles):
            x0 = 60 + (i % 2) * (tw + g)
            y0 = top + (i // 2) * (th + g)
            box = (x0, y0, x0 + tw, y0 + th)
            if p.get("note"):
                # «стикер» с полоской скотча (вариант для доски)
                ang_fill = p["note"][i % len(p["note"])]
                c.shadow(box, r=6, alpha=90, blur=10, off=(0, 8))
                c.rect(box, fill=ang_fill, r=6)
                c.rect((x0 + tw / 2 - 60, y0 - 14, x0 + tw / 2 + 60, y0 + 18), fill=(250, 246, 230), alpha=200)
            else:
                c.card(box, fill=p["tile"], r=28, sh_alpha=p.get("sh", 60), blur=14, off=(0, 8))
            isz = min(120, th * 0.36)
            if ic:
                c.circle(x0 + tw / 2, y0 + th * 0.3, isz * 0.72, fill=p["iconbg"])
                icon(c, ic, x0 + tw / 2, y0 + th * 0.3, isz, p["icon"], bg=p["iconbg"])
            c.block(lab, "sb", 36, y0 + th * 0.56, tw - 50, p["tile_ink"], cx=x0 + tw / 2, max_lines=2, gap=1.08)
            c.pill(cta, x0 + tw / 2, y0 + th - 44, size=24, fill=p["btn"], padx=24, pady=11)
    elif lay == "row4":
        hero_h = t.get("hero_h", 330)
        hb = (60, y + 22, 1020, y + 22 + hero_h)
        t["hero"](c, hb)
        top = hb[3] + 28
        g = 18
        tw = (960 - 3 * g) / 4
        th = 1044 - top
        for i, (ic, lab) in enumerate(tiles):
            x0 = 60 + i * (tw + g)
            box = (x0, top, x0 + tw, top + th)
            c.card(box, fill=p["tile"], r=24, sh_alpha=p.get("sh", 60), blur=12, off=(0, 6), outline=p.get("tile_line"), width=3 if p.get("tile_line") else 0)
            cx = x0 + tw / 2
            if ic:
                icon(c, ic, cx, top + th * 0.28, min(96, th * 0.36), p["icon"], bg=p["tile"])
                c.block(lab, "sb", 28, top + th * 0.5, tw - 26, p["tile_ink"], cx=cx, max_lines=2, gap=1.05)
            else:
                big = t.get("big_size", 78)
                c.text((cx, top + th * 0.36), lab, "db", big, p["acc"], anchor="mm")
                if t.get("tile_sub"):
                    c.block(t["tile_sub"], "s", 24, top + th * 0.56, tw - 30, p["tile_ink"], cx=cx, max_lines=2)
            c.pill(cta, cx, top + th - 38, size=20, fill=p["btn"], padx=16, pady=10)
    elif lay == "list4":
        hero_h = t.get("hero_h", 300)
        hb = (60, y + 20, 1020, y + 20 + hero_h)
        t["hero"](c, hb)
        top = hb[3] + 22
        g = 14
        rh = (1044 - top - 3 * g) / 4
        for i, (ic, lab) in enumerate(tiles):
            y0 = top + i * (rh + g)
            box = (60, y0, 1020, y0 + rh)
            c.card(box, fill=p["tile"], r=rh / 2, sh_alpha=p.get("sh", 50), blur=10, off=(0, 5))
            c.circle(60 + rh / 2 + 6, y0 + rh / 2, rh * 0.4, fill=p["iconbg"])
            icon(c, ic, 60 + rh / 2 + 6, y0 + rh / 2, rh * 0.58, p["icon"], bg=p["iconbg"])
            pb = c.pill(cta, 0, -500, size=22, fill=p["btn"], padx=22, pady=11)  # измерить ширину
            pw = pb[2] - pb[0]
            c.pill(cta, 1020 - 18 - pw / 2, y0 + rh / 2, size=22, fill=p["btn"], padx=22, pady=11)
            c.block(lab, "sb", 34, y0 + rh / 2 - 20, 1020 - 18 - pw - 30 - (60 + rh + 24), p["tile_ink"], align="left", x=60 + rh + 24, max_lines=1)
    elif lay == "row2":
        hero_h = t.get("hero_h", 370)
        hb = (60, y + 20, 1020, y + 20 + hero_h)
        t["hero"](c, hb)
        top = hb[3] + 26
        bottom = 1044 - (70 if t.get("foot") else 0)
        g = 24
        tw = (960 - g) / 2
        for i, (ic, lab) in enumerate(tiles):
            x0 = 60 + i * (tw + g)
            box = (x0, top, x0 + tw, bottom)
            c.card(box, fill=p["tile"], r=28, sh_alpha=p.get("sh", 60), blur=14, off=(0, 8), outline=p.get("tile_line"), width=3 if p.get("tile_line") else 0)
            h = bottom - top
            c.circle(x0 + 100, top + h * 0.42, 70, fill=p["iconbg"])
            icon(c, ic, x0 + 100, top + h * 0.42, 100, p["icon"], bg=p["iconbg"])
            c.block(lab, "db", 40, top + h * 0.42 - 26, tw - 200, p["tile_ink"], align="left", x=x0 + 186, max_lines=1)
            c.pill(cta, x0 + tw / 2, bottom - 44, size=26, fill=p["btn"], padx=30, pady=12)
        if t.get("foot"):
            c.block(t["foot"], "sb", 36, bottom + 18, 980, p["ink"], max_lines=1, highlight=p.get("hl"), hl_pad=8)
    if t.get("foot") and lay != "row2":
        pass
    return c


# =====================================================================  B: опросник
def radio_opts(c, opts, x0, x1, y, h, gap, p, size=34, sel=None):
    for k, o in enumerate(opts):
        c.rect((x0, y, x1, y + h), fill=p.get("opt", (246, 248, 249)), r=h / 2, outline=p.get("opt_line", (206, 214, 220)), width=3)
        c.circle(x0 + h / 2 + 4, y + h / 2, h * 0.22, fill=WH, outline=(150, 160, 170), width=3)
        c.block(o, "sb", size, y + h / 2 - size * 0.62, x1 - x0 - h - 30, (48, 52, 60), align="left", x=x0 + h + 8, max_lines=1)
        y += h + gap
    return y


def quiz(P, t):
    p = P["pal"]
    lay = t["layout"]
    cta = P["cta"]
    c = C(p["bg"])
    if p.get("bg2"):
        c.vgrad((0, 0, W, W), p["bg"], p["bg2"])
    if p.get("deco"):
        c.ellipse((760, -140, 1240, 340), fill=WH, alpha=18)
        c.ellipse((-180, 780, 260, 1220), fill=WH, alpha=14)
    if lay in ("card", "card2x2", "calc"):
        if p.get("chalk"):
            S.classroom_board_bg(c)
        y = header(c, t, col=p["ink"], sub_col=p["sub"], size=t.get("size", 60), t2_col=p.get("acc"), hl=p.get("hl"))
        box = (70, y + 26, 1010, 900)
        c.card(box, r=36, sh_alpha=120, blur=22)
        x0, x1 = box[0] + 50, box[2] - 50
        yy = box[1] + 40
        if lay == "calc":
            # степпер из 3 шагов
            steps = t["steps"]
            sx = [x0 + 60, (x0 + x1) / 2, x1 - 60]
            c.line([(sx[0], yy + 34), (sx[2], yy + 34)], (220, 226, 232), 8)
            c.line([(sx[0], yy + 34), (sx[1], yy + 34)], p["acc"], 8)
            for k, (lab, st) in enumerate(steps):
                col = (40, 170, 90) if st == "done" else (p["acc"] if st == "now" else (200, 206, 214))
                c.circle(sx[k], yy + 34, 30, fill=col)
                if st == "done":
                    c.check(sx[k] - 14, yy + 20, 28, WH, 6)
                else:
                    c.text((sx[k], yy + 34), str(k + 1), "db", 28, WH, anchor="mm")
                c.text((sx[k], yy + 92), lab, "sb", 26, (60, 66, 76), anchor="mm")
            yy += 130
            icon(c, "calc", x1 - 30, box[1] - 60, 120, p["acc"], bg=p["bg"])
        c.text((x0, yy), t["tag"], "sb", 26, p["acc"])
        c.text((x1, yy), t["step"], "s", 28, (110, 116, 124), anchor="ra")
        if lay != "calc":
            c.rect((x0, yy + 50, x1, yy + 64), fill=(226, 232, 236), r=7)
            c.rect((x0, yy + 50, x0 + (x1 - x0) * t["prog"], yy + 64), fill=p["acc"], r=7)
            yy += 96
        else:
            yy += 50
        yy = c.block(t["q"], "db", t.get("q_size", 44), yy, x1 - x0, (38, 38, 46), align="left", x=x0, max_lines=3, gap=1.12)
        yy += 16
        if lay == "card":
            n = len(t["opts"])
            h = min(80, (box[3] - 36 - yy - (n - 1) * 14) / n)
            radio_opts(c, t["opts"], x0, x1, yy, h, 14, p, size=34)
        else:
            g = 20
            ow = (x1 - x0 - g) / 2
            oh = min(120, (box[3] - 40 - yy - g) / 2)
            for k, o in enumerate(t["opts"]):
                ox = x0 + (k % 2) * (ow + g)
                oy = yy + (k // 2) * (oh + g)
                c.rect((ox, oy, ox + ow, oy + oh), fill=p.get("opt", (244, 247, 249)), r=22, outline=p.get("opt_line", (206, 214, 220)), width=3)
                badge = "ABCD"[k]
                c.circle(ox + 44, oy + oh / 2, 24, fill=p["acc"])
                c.text((ox + 44, oy + oh / 2), badge, "db", 24, WH, anchor="mm")
                lines = c.wrap(o, c.font("sb", 30), ow - 100)
                sz = 30 if len(lines) <= 2 else 26
                lh = c.lh("sb", sz, 1.1)
                nl = len(c.wrap(o, c.font("sb", sz), ow - 100))
                c.block(o, "sb", sz, oy + oh / 2 - nl * lh / 2 + 2, ow - 100, (44, 48, 58), align="left", x=ox + 84, max_lines=2, gap=1.1)
        c.button(cta, W / 2, 975, size=42, fill=p["btn"])
    elif lay == "phone":
        # слева текст и кнопка, справа телефон
        lx = 60
        y = 170
        y = c.block(t["title"], "db", t.get("size", 58), y, 440, p["ink"], align="left", x=lx, max_lines=4, gap=1.1)
        if t.get("title2"):
            y = c.block(t["title2"], "db", int(t.get("size", 58) * 0.9), y + 4, 440, p["acc"], align="left", x=lx, max_lines=4, gap=1.1)
        if t.get("sub"):
            y = c.block(t["sub"], "s", 32, y + 18, 430, p["sub"], align="left", x=lx, max_lines=3)
        bb = c.button(cta, 0, -600, size=40, fill=p["btn"])
        bw = bb[2] - bb[0]
        c.button(cta, lx + bw / 2, y + 90, size=40, fill=p["btn"])
        ph = (560, 60, 1020, 1020)
        c.shadow(ph, r=64, alpha=110, blur=26, off=(0, 16))
        c.rect(ph, fill=(28, 30, 36), r=64)
        sc = (ph[0] + 16, ph[1] + 16, ph[2] - 16, ph[3] - 16)
        c.rect(sc, fill=WH, r=50)
        c.rect(((ph[0] + ph[2]) / 2 - 70, ph[1] + 30, (ph[0] + ph[2]) / 2 + 70, ph[1] + 62), fill=(28, 30, 36), r=16)
        c.text((sc[0] + 36, ph[1] + 46), "9:41", "sb", 22, (40, 40, 40), anchor="lm")
        x0, x1 = sc[0] + 34, sc[2] - 34
        yy = sc[1] + 90
        c.rect((x0, yy, x0 + c.tw(t["tag"], c.font("sb", 22))[0] + 28, yy + 38), fill=mix(p["acc"], WH, 0.85), r=19)
        c.text((x0 + 14, yy + 19), t["tag"], "sb", 22, p["acc"], anchor="lm")
        yy += 60
        c.text((x0, yy), t["step"], "s", 24, (110, 116, 124))
        c.rect((x0, yy + 40, x1, yy + 50), fill=(226, 232, 236), r=5)
        c.rect((x0, yy + 40, x0 + (x1 - x0) * t["prog"], yy + 50), fill=p["acc"], r=5)
        yy += 76
        yy = c.block(t["q"], "db", t.get("q_size", 34), yy, x1 - x0, (38, 38, 46), align="left", x=x0, max_lines=5, gap=1.12)
        yy += 16
        n = len(t["opts"])
        h = min(72, (sc[3] - 70 - yy - (n - 1) * 12) / n)
        radio_opts(c, t["opts"], x0, x1, yy, h, 12, p, size=26)
        for k in range(6):
            c.circle((sc[0] + sc[2]) / 2 - 50 + k * 20, sc[3] - 30, 5, fill=p["acc"] if k == 0 else (210, 214, 220))
    return c


# =====================================================================  C: сравнение / сколько стоит
def compare(P, t):
    p = P["pal"]
    lay = t["layout"]
    cta = P["cta"]
    c = C(p["bg"])
    if p.get("bg2") and lay not in ("split",):
        c.vgrad((0, 0, W, W), p["bg"], p["bg2"])
    if lay == "twocol":
        y = header(c, t, col=p["ink"], sub_col=p["sub"], size=t.get("size", 58))
        top = y + 28
        bot = 842 if t.get("foot") else 900
        L, R = (60, top, 522, bot), (558, top, 1020, bot)
        for box, (head, ic, col) in zip((L, R), t["cols"]):
            c.card(box, fill=mix(col, WH, 0.9), r=30, sh_alpha=50, blur=12, off=(0, 6))
            c.rect((box[0], box[1], box[2], box[1] + 92), fill=col, r=30)
            c.rect((box[0], box[1] + 60, box[2], box[1] + 92), fill=col)
            c.block(head, "db", 34, box[1] + 26, box[2] - box[0] - 40, WH, cx=(box[0] + box[2]) / 2, max_lines=1)
            c.circle((box[0] + box[2]) / 2, box[1] + 175, 62, fill=WH)
            icon(c, ic, (box[0] + box[2]) / 2, box[1] + 175, 96, col)
        ry = top + 270
        rh = (bot - ry - 20) / len(t["rows"])
        for lab, lt, rt in t["rows"]:
            for box, txt, (_, _, col) in ((L, lt, t["cols"][0]), (R, rt, t["cols"][1])):
                c.text((box[0] + 36, ry), lab, "sb", 22, col)
                c.block(txt, "sb", 34, ry + 32, box[2] - box[0] - 72, (36, 38, 44), align="left", x=box[0] + 36, max_lines=2, gap=1.05)
            ry += rh
        c.circle(W / 2, top + 175, 44, fill=WH, outline=(200, 205, 212), width=3)
        c.text((W / 2, top + 175), t.get("vs", "vs"), "db", 28, (90, 96, 106), anchor="mm")
        if t.get("foot"):
            c.block(t["foot"], "sb", 36, 862, 980, p["ink"], max_lines=1)
        c.button(cta, W / 2, 975, size=42, fill=p["btn"])
    elif lay == "split":
        (lh, lic, lcol, lrows), (rh, ric, rcol, rrows) = t["cols"]
        band = 262 if not t.get("band") else t["band"]
        c.rect((0, 0, W, band), fill=p["bg"])
        diag = t.get("diag", 0)
        c.poly([(0, band), (W / 2 + diag, band), (W / 2 - diag, W), (0, W)], lcol)
        c.poly([(W / 2 + diag, band), (W, band), (W, W), (W / 2 - diag, W)], rcol)
        header(c, t, y=40, col=p["ink"], sub_col=p["sub"], size=t.get("size", 56))
        for (head, ic, col, rows), cx in (((lh, lic, lcol, lrows), W / 4), ((rh, ric, rcol, rrows), 3 * W / 4)):
            c.circle(cx, band + 130, 88, fill=WH)
            icon(c, ic, cx, band + 130, 124, col)
            c.block(head, "db", 38, band + 240, 470, WH, cx=cx, max_lines=1)
            yy = band + 320
            for r_ in rows:
                x0 = cx - 215
                c.circle(x0 + 16, yy + 20, 16, fill=WH, alpha=235)
                if r_.endswith("?"):
                    c.text((x0 + 16, yy + 20), "?", "db", 22, col, anchor="mm")
                else:
                    c.check(x0 + 7, yy + 11, 18, col, 4)
                c.block(r_, "sb", 31, yy, 400, WH, align="left", x=x0 + 46, max_lines=2, gap=1.05)
                nl = len(c.wrap(r_, c.font("sb", 31), 400))
                yy += 40 * nl + 30
        c.circle(W / 2, band + 130, 50, fill=p.get("vs_bg", WH), outline=(210, 214, 220), width=3)
        c.text((W / 2, band + 130), t.get("vs", "vs"), "db", 32, p.get("vs_ink", (60, 64, 72)), anchor="mm")
        c.button(cta, W / 2, 985, size=42, fill=p["btn"], color=p.get("btn_ink", WH))
    elif lay == "table":
        y = header(c, t, col=p["ink"], sub_col=p["sub"], size=t.get("size", 56))
        top = y + 26
        bot = 862 if t.get("foot") else 900
        box = (60, top, 1020, bot)
        c.card(box, r=28, sh_alpha=60, blur=14, off=(0, 8))
        colx = [box[0], box[0] + 270, box[0] + 270 + 345, box[2]]
        hh = 170
        (ha, ica, cola), (hb, icb, colb) = t["cols"]
        c.rect((colx[2], box[1], colx[3], box[3]), fill=mix(colb, WH, 0.9), r=28)
        c.rect((colx[2], box[1], colx[2] + 30, box[3]), fill=mix(colb, WH, 0.9))
        for (head, ic, col), x0, x1 in (((ha, ica, cola), colx[1], colx[2]), ((hb, icb, colb), colx[2], colx[3])):
            cx = (x0 + x1) / 2
            icon(c, ic, cx, box[1] + 62, 82, col)
            c.block(head, "db", 28, box[1] + 112, x1 - x0 - 24, col, cx=cx, max_lines=2, gap=1.0)
        rows = t["rows"]
        rh = (box[3] - box[1] - hh - (60 if t.get("banner") else 10)) / len(rows)
        ry = box[1] + hh
        for k, (lab, a, b) in enumerate(rows):
            c.line([(box[0] + 24, ry), (box[2] - 24, ry)], (224, 228, 234), 2)
            c.block(lab, "sb", 28, ry + rh / 2 - 17, colx[1] - colx[0] - 40, (70, 76, 88), align="left", x=colx[0] + 30, max_lines=1)
            for txt, x0, x1, col in ((a, colx[1], colx[2], (46, 50, 60)), (b, colx[2], colx[3], (30, 34, 44))):
                if txt.strip() == "?":
                    c.circle((x0 + x1) / 2, ry + rh / 2, 30, fill=p["acc"])
                    c.text(((x0 + x1) / 2, ry + rh / 2), "?", "db", 36, WH, anchor="mm")
                    continue
                nl = len(c.wrap(txt, c.font("sb", 28), x1 - x0 - 36))
                sz = 28 if nl <= 2 else 24
                nl = min(2, len(c.wrap(txt, c.font("sb", sz), x1 - x0 - 36)))
                c.block(txt, "sb", sz, ry + rh / 2 - nl * c.lh("sb", sz, 1.04) / 2 + 2, x1 - x0 - 36, col, cx=(x0 + x1) / 2, max_lines=2, gap=1.04)
            ry += rh
        if t.get("banner"):
            c.rect((colx[2] + 14, box[3] - 64, colx[3] - 14, box[3] - 14), fill=p["acc"], r=14)
            c.block(t["banner"], "sb", 24, box[3] - 54, colx[3] - colx[2] - 50, WH, cx=(colx[2] + colx[3]) / 2, max_lines=1)
        if t.get("foot"):
            c.block(t["foot"], "sb", 36, 884, 980, p["ink"], max_lines=1, highlight=p.get("hl"), hl_pad=8)
        c.button(cta, W / 2, 986, size=42, fill=p["btn"])
    elif lay == "bars":
        y = header(c, t, col=p["ink"], sub_col=p["sub"], size=t.get("size", 58))
        top = y + 26
        bot = 862
        box = (90, top, 990, bot)
        c.card(box, r=10, sh_alpha=70, blur=14, off=(0, 8))
        c.rect((box[0], box[1], box[2], box[1] + 70), fill=p["acc"], r=10)
        c.rect((box[0], box[1] + 40, box[2], box[1] + 70), fill=p["acc"])
        c.text((box[0] + 36, box[1] + 35), t["bill"], "sb", 28, WH, anchor="lm")
        c.text((box[2] - 36, box[1] + 35), t.get("bill_r", ""), "s", 26, WH, anchor="rm")
        # «перфорация» внизу счёта
        for x in range(int(box[0]) + 20, int(box[2]) - 10, 28):
            c.circle(x, box[3], 7, fill=p["bg"])
        rows = t["bars"]
        rh = (box[3] - box[1] - 110) / len(rows)
        ry = box[1] + 100
        bx0, bx1 = box[0] + 40, box[2] - 40
        for lab, frac, val, col in rows:
            c.text((bx0, ry), lab, "sb", 32, (40, 44, 54))
            c.rect((bx0, ry + 52, bx1, ry + 104), fill=(234, 237, 241), r=14)
            if frac is None:
                # неизвестная доля: штриховка + «?»
                for k in range(0, int(bx1 - bx0), 34):
                    c.line([(bx0 + k, ry + 104), (bx0 + k + 30, ry + 52)], mix(col, WH, 0.5), 10)
                c.rect((bx0, ry + 52, bx1, ry + 104), outline=col, width=3, r=14)
                c.circle(bx1 - 40, ry + 78, 24, fill=col)
                c.text((bx1 - 40, ry + 78), "?", "db", 30, WH, anchor="mm")
                c.text((bx0 + 20, ry + 78), val, "sb", 28, (40, 44, 54), anchor="lm")
            else:
                c.rect((bx0, ry + 52, bx0 + (bx1 - bx0) * frac, ry + 104), fill=col, r=14)
                c.text((bx0 + (bx1 - bx0) * frac - 20, ry + 78), val, "db", 32, WH, anchor="rm")
            ry += rh
        if t.get("foot"):
            c.block(t["foot"], "sb", 34, 888, 980, p["ink"], max_lines=1)
        c.button(cta, W / 2, 985, size=42, fill=p["btn"])
    elif lay == "stacked":
        y = header(c, t, col=p["ink"], sub_col=p["sub"], size=t.get("size", 56))
        top = y + 24
        bot = 846 if t.get("foot") else 900
        gap = 36
        ch = (bot - top - gap) / 2
        for k, (head, ic, col, fill, ink, items) in enumerate(t["cols"]):
            y0 = top + k * (ch + gap)
            box = (60, y0, 1020, y0 + ch)
            c.card(box, fill=fill, r=28, sh_alpha=60, blur=12, off=(0, 6))
            c.circle(60 + 120, y0 + ch / 2, 86, fill=WH if k else mix(col, WH, 0.85))
            icon(c, ic, 60 + 120, y0 + ch / 2, 120, col)
            c.block(head, "db", 36, y0 + 30, 700, ink, align="left", x=320, max_lines=1)
            yy = y0 + 92
            ih = (ch - 110) / len(items)
            for it in items:
                q = it.endswith("?")
                c.circle(336, yy + 18, 13, fill=(p["acc"] if q else (ink if k else col)))
                c.block(it, "sb" if q else "s", 32, yy, 640, ink, align="left", x=366, max_lines=1)
                yy += ih
        c.circle(W / 2, top + ch + gap / 2, 38, fill=WH, outline=(200, 205, 212), width=3)
        c.text((W / 2, top + ch + gap / 2), t.get("vs", "vs"), "db", 26, (90, 96, 106), anchor="mm")
        if t.get("foot"):
            c.block(t["foot"], "sb", 36, 868, 980, p["ink"], max_lines=1, highlight=p.get("hl"), hl_pad=8)
        c.button(cta, W / 2, 978, size=42, fill=p["btn"])
    return c


# =====================================================================  D: сцена-иллюстрация
def scene(P, t):
    p = P["pal"]
    cta = P["cta"]
    c = C(WH)
    style = t["style"]
    getattr(S, t["scene"])(c, **t.get("scene_kw", {}))
    if style == "top":
        y = 50
        if t.get("kicker"):
            c.text((W / 2, y + 16), t["kicker"], "sb", 26, p["acc"], anchor="mm")
            y += 50
        y = c.block(t["title"], "db", t.get("size", 66), y, 980, p["ink"], max_lines=t.get("lines", 2), highlight=t.get("hl"), hl_pad=10)
        if t.get("sub"):
            c.block(t["sub"], "s", 32, y + 12, 940, p["sub"], max_lines=2)
        if t.get("sticker"):
            sx, sy, sr = t["sticker_xy"]
            c.shadow((sx - sr, sy - sr, sx + sr, sy + sr), r=sr, alpha=90, blur=10, off=(0, 8))
            c.circle(sx, sy, sr, fill=p["sticker"])
            c.circle(sx, sy, sr - 12, outline=WH, width=3)
            c.block(t["sticker"], "db", 34, sy - 44, sr * 1.5, p["ink"], cx=sx, max_lines=3, gap=1.02)
        c.button(cta, W / 2, t.get("btn_y", 990), size=44, fill=p["btn"])
    elif style == "card":
        box = t["card_box"]
        c.shadow(box, r=18, alpha=120, blur=18, off=(0, 10))
        c.rect(box, fill=(252, 249, 242), r=18, alpha=242)
        c.rect((box[0] + 16, box[1] + 16, box[2] - 16, box[3] - 16), outline=p["frame"], width=3, r=12)
        c.rect((box[0] + 26, box[1] + 26, box[2] - 26, box[3] - 26), outline=p["frame"], width=1, r=8)
        cx = (box[0] + box[2]) / 2
        y = box[1] + 58
        if t.get("kicker"):
            y = c.block(t["kicker"], "sb", 26, y, box[2] - box[0] - 120, p["acc"], cx=cx, max_lines=2) + 10
        y = c.block(t["title"], "lserb", t.get("size", 68), y, box[2] - box[0] - 110, p["ink"], cx=cx, max_lines=3, gap=1.08)
        if t.get("sub"):
            y = c.block(t["sub"], "s", 32, y + 12, box[2] - box[0] - 140, p["sub"], cx=cx, max_lines=2)
        c.button(cta, cx, box[3] - 74, size=40, fill=p["btn"])
    elif style in ("bars", "chalk", "left"):
        if t.get("veil"):
            vb = t["veil"]
            c.shadow(vb, r=26, alpha=90, blur=18, off=(0, 10))
            c.rect(vb, fill=t.get("veil_col", WH), r=26, alpha=t.get("veil_alpha", 236))
        y = t.get("y", 60)
        align = "left" if style == "left" else "center"
        x = t.get("x", 70)
        cx = t.get("cx", W / 2)
        y = c.bars(t["bars"], y, size=t.get("bar_size", 86), cond=t.get("cond", 0.8), cx=cx, align=align, x=x,
                   max_w=t.get("max_w", 980), gap=t.get("gap", 8))
        bb = c.button(cta, 0, -600, size=t.get("btn_size", 50), fill=p["btn"], padx=64, pady=24)
        bw = bb[2] - bb[0]
        bx = cx if align == "center" else x - 18 + bw / 2
        c.button(cta, bx, t.get("btn_y", y + 70), size=t.get("btn_size", 50), fill=p["btn"], padx=64, pady=24,
                 grad=(mix(p["btn"], WH, 0.35), p["btn"]), outline=WH)
    return c
