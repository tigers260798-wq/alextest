"""Волна 5 (29.09, креативщик w5): 6 карточек «Готово к заливу» из article_drafts/*-2026-09-29 × 4 статики 1:1, Pillow.
    python3 w5_0929.py            — все пакеты
    python3 w5_0929.py 3 5        — пакеты 3 и 5
    python3 w5_0929.py 3:a,c      — пакет 3, буквы a и c
    python3 w5_0929.py icons      — лист новых иконок (scratch)
Пишет /home/user/alextest/creatives/ready/2026-09-29_drafts/<docId>/<a|b|c|d>.png и creatives.json рядом.
Движок — w3_packs / w4_ukde (импорт, файлы не меняются): p60_templates (grid / quiz / compare), w2b_layouts.scene_d,
w4 grid6 / list5 / table3, иконки p60/w2b/w3/w4. Здесь — свои иконки w5_*, «герои», сцены и раскладка lt_grid
(перенос доказанного LT-формата: заголовок + фото + 4 плитки + красные кнопки).
Весь текст на картинках — только из статей карточек (раздел — в поле src). Без сумм заработка и стипендий, без обещания
работы, без логотипов и гербов (Sodra, ZUS, mObywatel, SEPE, France Travail, IEFP — только словом в тексте, где это
название программы), без «in Ihrer Nähe / cerca de ti / près de chez vous / perto de si / šalia jūsų / w pobliżu»,
без «click here», до/после и утверждений о возрасте, финансах или профессии зрителя."""
import json
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import w4_ukde as W4  # noqa: E402  (тянет w3_packs и весь движок, регистрирует иконки и сцены)
import w3_packs as W3  # noqa: E402
import p60_lib  # noqa: E402
from p60_lib import C, W, mix, rotpts  # noqa: E402
import p60_icons as I  # noqa: E402
import p60_scenes as S  # noqa: E402
import p60_templates as T  # noqa: E402
import p60w2_art as A  # noqa: E402
import w2b_scenes as WS  # noqa: E402
import w2b_layouts as L  # noqa: E402

OUT5 = "/home/user/alextest/creatives/ready/2026-09-29_drafts"
p60_lib.OUT = OUT5  # C.save пишет в p60_lib.OUT
WH = (255, 255, 255)
SKIN = A.SKIN
CONCEPT = W3.CONCEPT
PACKS = {}
GREY_HAIR = (214, 214, 220)


def icon(c, name, cx, cy, s, col, bg=WH):
    I.ICONS[name](c, cx, cy, s, col, bg=bg)


# =====================================================================  иконки w5 (квадрат s, центр cx, cy)
def w5_forklift(c, cx, cy, s, col, bg=WH, acc=(240, 172, 30), box_col=(196, 150, 96)):
    c.rect((cx - s * 0.44, cy - s * 0.02, cx - s * 0.34, cy + s * 0.26), fill=col, r=s * 0.02)          # противовес
    c.rect((cx - s * 0.36, cy - s * 0.04, cx + s * 0.14, cy + s * 0.26), fill=acc, r=s * 0.04)          # корпус
    for x in (cx - s * 0.3, cx + s * 0.06):
        c.line([(x, cy - s * 0.04), (x, cy - s * 0.36)], col, s * 0.035)                               # стойки кабины
    c.rect((cx - s * 0.34, cy - s * 0.4, cx + s * 0.1, cy - s * 0.34), fill=col, r=s * 0.02)            # крыша
    c.rect((cx + s * 0.17, cy - s * 0.46, cx + s * 0.23, cy + s * 0.3), fill=col, r=s * 0.02)           # мачта
    c.rect((cx + s * 0.2, cy + s * 0.25, cx + s * 0.48, cy + s * 0.3), fill=col, r=s * 0.015)           # вилы
    c.rect((cx + s * 0.25, cy - s * 0.02, cx + s * 0.46, cy + s * 0.24), fill=box_col, r=s * 0.02)      # коробка
    c.line([(cx + s * 0.355, cy - s * 0.02), (cx + s * 0.355, cy + s * 0.08)], mix(box_col, WH, 0.5), s * 0.03)
    for x, r in ((cx - s * 0.22, 0.11), (cx + s * 0.04, 0.09)):
        c.circle(x, cy + s * 0.32, s * r, fill=col)
        c.circle(x, cy + s * 0.32, s * r * 0.42, fill=bg)


def w5_logs(c, cx, cy, s, col, bg=WH, wood=(176, 112, 60), ring=(222, 170, 110)):
    for dx, dy in ((-0.22, 0.2), (0.22, 0.2), (0.0, -0.16)):
        x, y = cx + dx * s, cy + dy * s
        c.circle(x, y, s * 0.22, fill=wood)
        c.circle(x, y, s * 0.16, fill=ring)
        c.circle(x, y, s * 0.1, outline=wood, width=s * 0.02)
        c.circle(x, y, s * 0.03, fill=wood)


def _teardrop(cx, by, w, h, n=24):
    """Капля/пламя: круглый низ (центр cx, by, радиус w/2), острый верх на высоте h над by."""
    r = w / 2
    pts = [(cx + math.cos(math.pi * k / n) * r, by + math.sin(math.pi * k / n) * r) for k in range(n + 1)]
    pts += [(cx - r * 0.86, by - h * 0.3), (cx - r * 0.45, by - h * 0.68), (cx, by - h),
            (cx + r * 0.45, by - h * 0.68), (cx + r * 0.86, by - h * 0.3)]
    return pts


def w5_flame(c, cx, cy, s, col, bg=WH, outer=(40, 110, 220), inner=(120, 190, 250)):
    c.poly(_teardrop(cx, cy + s * 0.14, s * 0.56, s * 0.72), outer)
    c.poly(_teardrop(cx, cy + s * 0.2, s * 0.28, s * 0.38), inner)
    c.rect((cx - s * 0.36, cy + s * 0.36, cx + s * 0.36, cy + s * 0.44), fill=col, r=s * 0.04)


def w5_tap(c, cx, cy, s, col, bg=WH, drop=(40, 150, 230)):
    c.rect((cx - s * 0.42, cy - s * 0.28, cx - s * 0.32, cy + s * 0.02), fill=col, r=s * 0.02)          # стена-фланец
    c.rect((cx - s * 0.36, cy - s * 0.2, cx + s * 0.18, cy - s * 0.08), fill=col, r=s * 0.04)          # труба
    c.arc((cx + s * 0.04, cy - s * 0.2, cx + s * 0.32, cy + s * 0.08), 270, 360, col, s * 0.12)         # излив
    c.rect((cx + s * 0.2, cy - s * 0.06, cx + s * 0.32, cy + s * 0.04), fill=col)
    c.rect((cx - s * 0.12, cy - s * 0.36, cx - s * 0.04, cy - s * 0.2), fill=col)
    c.rect((cx - s * 0.24, cy - s * 0.42, cx + s * 0.08, cy - s * 0.34), fill=(222, 64, 50), r=s * 0.04)  # красный вентиль
    c.poly(_teardrop(cx + s * 0.26, cy + s * 0.34, s * 0.16, s * 0.2), drop)
    c.poly(_teardrop(cx + s * 0.26, cy + s * 0.12, s * 0.1, s * 0.12), drop)


def w5_pool(c, cx, cy, s, col, bg=WH, water=(40, 150, 220)):
    for x in (cx - s * 0.14, cx + s * 0.14):
        c.arc((x - s * 0.2, cy - s * 0.46, x, cy - s * 0.26), 180, 270, col, s * 0.05)
        c.line([(x - s * 0.2, cy - s * 0.36), (x - s * 0.2, cy + s * 0.1)], col, s * 0.05)
    for y in (-0.2, -0.06):
        c.line([(cx - s * 0.34, cy + y * s), (cx - s * 0.06, cy + y * s)], col, s * 0.04)
    for k, y in enumerate((0.16, 0.32)):
        pts = [(cx - s * 0.46 + i * s * 0.023, cy + y * s + math.sin(i / 2.6 + k) * s * 0.035) for i in range(41)]
        c.line(pts, water, s * 0.06)


def w5_senior_card(c, cx, cy, s, col, bg=WH, acc=(236, 150, 40)):
    c.rect((cx - s * 0.46, cy - s * 0.3, cx + s * 0.46, cy + s * 0.3), fill=col, r=s * 0.06)
    c.rect((cx - s * 0.46, cy - s * 0.3, cx + s * 0.46, cy - s * 0.18), fill=acc, r=s * 0.06)
    c.rect((cx - s * 0.46, cy - s * 0.22, cx + s * 0.46, cy - s * 0.18), fill=acc)
    c.rect((cx - s * 0.38, cy - s * 0.1, cx - s * 0.1, cy + s * 0.22), fill=mix(col, WH, 0.85), r=s * 0.03)
    c.circle(cx - s * 0.24, cy - s * 0.0, s * 0.06, fill=col)
    c.pie((cx - s * 0.34, cy + s * 0.06, cx - s * 0.14, cy + s * 0.3), 180, 360, col)
    for k, w in enumerate((0.3, 0.24, 0.28)):
        c.rect((cx - s * 0.02, cy - s * 0.08 + k * s * 0.1, cx - s * 0.02 + w * s, cy - s * 0.04 + k * s * 0.1), fill=mix(col, WH, 0.7), r=s * 0.02)


def w5_bucket(c, cx, cy, s, col, bg=WH, acc=(40, 150, 220), mop=(170, 120, 70)):
    c.line([(cx + s * 0.34, cy - s * 0.48), (cx + s * 0.06, cy + s * 0.2)], mop, s * 0.05)                # ручка швабры
    c.poly([(cx - s * 0.36, cy - s * 0.06), (cx + s * 0.2, cy - s * 0.06), (cx + s * 0.14, cy + s * 0.42), (cx - s * 0.3, cy + s * 0.42)], acc)
    c.rect((cx - s * 0.4, cy - s * 0.1, cx + s * 0.24, cy - s * 0.02), fill=mix(acc, (0, 0, 0), 0.25), r=s * 0.03)
    c.arc((cx - s * 0.3, cy - s * 0.3, cx + s * 0.14, cy + s * 0.1), 200, 340, col, s * 0.035)          # дужка
    for dx in (-0.14, 0.0):
        c.circle(cx + dx * s, cy - s * 0.16, s * 0.07, fill=WH, outline=mix(acc, WH, 0.3), width=s * 0.015)   # пена
    c.circle(cx + s * 0.1, cy - s * 0.2, s * 0.05, fill=WH, outline=mix(acc, WH, 0.3), width=s * 0.015)


def w5_bell(c, cx, cy, s, col, bg=WH, gold=(232, 176, 50)):
    c.pie((cx - s * 0.36, cy - s * 0.26, cx + s * 0.36, cy + s * 0.46), 180, 360, gold)
    c.pie((cx - s * 0.26, cy - s * 0.18, cx - s * 0.02, cy + s * 0.2), 200, 250, mix(gold, WH, 0.5))
    c.rect((cx - s * 0.46, cy + s * 0.08, cx + s * 0.46, cy + s * 0.2), fill=col, r=s * 0.04)
    c.rect((cx - s * 0.05, cy - s * 0.38, cx + s * 0.05, cy - s * 0.26), fill=col)
    c.rect((cx - s * 0.12, cy - s * 0.44, cx + s * 0.12, cy - s * 0.36), fill=col, r=s * 0.03)


def w5_newspaper(c, cx, cy, s, col, bg=WH, paper=(246, 244, 238)):
    c.rect((cx - s * 0.36, cy - s * 0.4, cx + s * 0.42, cy + s * 0.4), fill=mix(col, WH, 0.75), r=s * 0.03)
    c.rect((cx - s * 0.42, cy - s * 0.34, cx + s * 0.36, cy + s * 0.44), fill=paper, outline=col, width=s * 0.03, r=s * 0.03)
    c.rect((cx - s * 0.34, cy - s * 0.26, cx + s * 0.28, cy - s * 0.16), fill=col, r=s * 0.02)
    c.rect((cx - s * 0.34, cy - s * 0.08, cx - s * 0.06, cy + s * 0.16), fill=mix(col, WH, 0.55), r=s * 0.02)
    for k in range(3):
        c.rect((cx, cy - s * 0.07 + k * s * 0.09, cx + s * 0.28, cy - s * 0.03 + k * s * 0.09), fill=mix(col, WH, 0.4), r=s * 0.02)
    for k in range(2):
        c.rect((cx - s * 0.34, cy + s * 0.24 + k * s * 0.09, cx + s * 0.28, cy + s * 0.28 + k * s * 0.09), fill=mix(col, WH, 0.4), r=s * 0.02)


def w5_blocks(c, cx, cy, s, col, bg=WH, acc=(236, 150, 40), acc2=(40, 160, 110)):
    for (x0, y0, x1, y1), f in (((-0.42, 0.12, -0.04, 0.42), col), ((0.02, 0.12, 0.4, 0.42), acc2),
                                ((-0.22, -0.22, 0.16, 0.08), acc), ((-0.02, -0.5, 0.36, -0.26), mix(col, WH, 0.55))):
        c.rect((cx + x0 * s, cy + y0 * s, cx + x1 * s, cy + y1 * s), fill=f, r=s * 0.04)
    c.line([(cx + 0.18 * s, cy - 0.5 * s), (cx + 0.18 * s, cy - 0.26 * s)], WH, s * 0.02)


def w5_cert(c, cx, cy, s, col, bg=WH, seal=(222, 64, 50), paper=WH):
    c.rect((cx - s * 0.4, cy - s * 0.42, cx + s * 0.36, cy + s * 0.3), fill=paper, outline=col, width=s * 0.035, r=s * 0.03)
    c.rect((cx - s * 0.3, cy - s * 0.32, cx + s * 0.26, cy - s * 0.24), fill=col, r=s * 0.02)
    for k, w in enumerate((0.5, 0.42, 0.46)):
        c.rect((cx - s * 0.3, cy - s * 0.14 + k * s * 0.1, cx - s * 0.3 + w * s, cy - s * 0.1 + k * s * 0.1), fill=mix(col, WH, 0.55), r=s * 0.02)
    c.poly([(cx + s * 0.14, cy + s * 0.2), (cx + s * 0.08, cy + s * 0.48), (cx + s * 0.18, cy + s * 0.42), (cx + s * 0.24, cy + s * 0.5), (cx + s * 0.28, cy + s * 0.2)], seal)
    c.circle(cx + s * 0.21, cy + s * 0.16, s * 0.13, fill=seal)
    c.circle(cx + s * 0.21, cy + s * 0.16, s * 0.08, outline=WH, width=s * 0.02)


def w5_museum(c, cx, cy, s, col, bg=WH, acc=(236, 150, 40)):
    c.poly([(cx - s * 0.46, cy - s * 0.2), (cx, cy - s * 0.46), (cx + s * 0.46, cy - s * 0.2)], col)
    c.circle(cx, cy - s * 0.3, s * 0.05, fill=acc)
    c.rect((cx - s * 0.44, cy - s * 0.2, cx + s * 0.44, cy - s * 0.13), fill=col)
    for k in range(4):
        x = cx - s * 0.33 + k * s * 0.22
        c.rect((x - s * 0.05, cy - s * 0.1, x + s * 0.05, cy + s * 0.3), fill=col)
    c.rect((cx - s * 0.46, cy + s * 0.32, cx + s * 0.46, cy + s * 0.4), fill=col)
    c.rect((cx - s * 0.5, cy + s * 0.4, cx + s * 0.5, cy + s * 0.46), fill=col)


def w5_masks(c, cx, cy, s, col, bg=WH, acc=(236, 150, 40)):
    """Театр: две маски."""
    for dx, face, mouth in ((-0.14, col, 1), (0.16, acc, -1)):
        x = cx + dx * s
        c.ellipse((x - s * 0.24, cy - s * 0.34, x + s * 0.24, cy + s * 0.28), fill=face)
        for ex in (-0.09, 0.09):
            c.ellipse((x + (ex - 0.05) * s, cy - s * 0.12, x + (ex + 0.05) * s, cy - s * 0.04), fill=bg)
        if mouth > 0:
            c.arc((x - s * 0.1, cy - s * 0.02, x + s * 0.1, cy + s * 0.16), 20, 160, bg, s * 0.04)
        else:
            c.arc((x - s * 0.1, cy + s * 0.08, x + s * 0.1, cy + s * 0.24), 200, 340, bg, s * 0.04)


def w5_contract(c, cx, cy, s, col, bg=WH, acc=(40, 150, 90)):
    """Лист с галочкой и подписью (контракт / конвенция)."""
    c.rect((cx - s * 0.34, cy - s * 0.44, cx + s * 0.3, cy + s * 0.44), fill=WH, outline=col, width=s * 0.035, r=s * 0.04)
    for k, w in enumerate((0.44, 0.36, 0.44, 0.3)):
        c.rect((cx - s * 0.24, cy - s * 0.32 + k * s * 0.11, cx - s * 0.24 + w * s, cy - s * 0.28 + k * s * 0.11), fill=mix(col, WH, 0.55), r=s * 0.02)
    pts = [(cx - s * 0.22 + k * s * 0.02, cy + s * 0.26 + math.sin(k / 1.5) * s * 0.04) for k in range(14)]
    c.line(pts, col, s * 0.025)
    c.circle(cx + s * 0.24, cy + s * 0.3, s * 0.16, fill=acc)
    c.check(cx + s * 0.16, cy + s * 0.22, s * 0.16, WH, s * 0.035)


def w5_doc_euro(c, cx, cy, s, col, bg=WH):
    """Документ с монетой «€» (денежная поддержка; без «$» на EU-крео)."""
    I.doc(c, cx - s * 0.06, cy, s, col, bg)
    bx, by, br = cx + s * 0.24, cy + s * 0.26, s * 0.17
    c.circle(bx, by, br * 1.18, fill=bg)
    c.circle(bx, by, br, fill=(236, 176, 40))
    c.text((bx, by), "€", "db", s * 0.2, WH, anchor="mm")


W5_ICONS = {k: v for k, v in dict(globals()).items() if k.startswith("w5_") and callable(v)}
I.ICONS.update(W5_ICONS)


def icon_sheet():
    c = C(WH)
    names = sorted(W5_ICONS)
    for i, n in enumerate(names):
        x, y = 135 + (i % 4) * 270, 135 + (i // 4) * 270
        c.circle(x, y, 90, fill=(232, 240, 246))
        icon(c, n, x, y, 130, (30, 50, 80), bg=(232, 240, 246))
        c.text((x, y + 116), n, "s", 20, (0, 0, 0), anchor="mm")
    p = "/tmp/claude-0/-home-user-alextest/f5dce882-fce7-5270-9036-ca9a0fe43d5e/scratchpad/w5/w5_icons.png"
    c.im.convert("RGB").resize((W, W)).save(p)
    print(p)


# =====================================================================  примитивы людей и предметов
def helmet(c, x, y, r, col=(250, 250, 250)):
    """Каска на голову радиуса r с центром (x, y)."""
    c.pie((x - r * 1.12, y - r * 1.2, x + r * 1.12, y + r * 0.7), 180, 360, col)
    c.rect((x - r * 1.3, y - r * 0.3, x + r * 1.3, y - r * 0.14), fill=mix(col, (0, 0, 0), 0.12), r=r * 0.08)
    c.rect((x - r * 0.12, y - r * 1.2, x + r * 0.12, y - r * 0.3), fill=mix(col, (0, 0, 0), 0.08))


def vest(c, x, sh_y, hip_y, tw, col=(210, 236, 60), stripe=(236, 238, 240)):
    """Светоотражающий жилет поверх торса (tw — полуширина торса)."""
    c.rect((x - tw * 0.98, sh_y + 6, x + tw * 0.98, hip_y), fill=col, r=tw * 0.4)
    c.poly([(x - tw * 0.3, sh_y + 4), (x + tw * 0.3, sh_y + 4), (x, sh_y + tw * 0.9)], mix(col, (0, 0, 0), 0.25))
    for yy in (sh_y + (hip_y - sh_y) * 0.55, sh_y + (hip_y - sh_y) * 0.75):
        c.rect((x - tw * 0.98, yy, x + tw * 0.98, yy + tw * 0.14), fill=stripe)


def clock_face(c, cx, cy, r, h=6, m=0, col=(50, 56, 70), face=WH):
    c.circle(cx, cy, r, fill=face, outline=col, width=r * 0.1)
    for k in range(12):
        a = math.radians(k * 30)
        c.line([(cx + math.cos(a) * r * 0.72, cy + math.sin(a) * r * 0.72), (cx + math.cos(a) * r * 0.84, cy + math.sin(a) * r * 0.84)], col, r * 0.05)
    am = math.radians(m * 6 - 90)
    ah = math.radians((h % 12 + m / 60) * 30 - 90)
    c.line([(cx, cy), (cx + math.cos(ah) * r * 0.48, cy + math.sin(ah) * r * 0.48)], col, r * 0.1)
    c.line([(cx, cy), (cx + math.cos(am) * r * 0.7, cy + math.sin(am) * r * 0.7)], col, r * 0.06)
    c.circle(cx, cy, r * 0.08, fill=col)


def box_stack(c, x0, y_base, w, h, n, col=(200, 156, 104), seed=1):
    rnd = random.Random(seed)
    x = x0
    for k in range(n):
        bw = w * rnd.uniform(0.8, 1.0)
        bh = h * rnd.uniform(0.75, 1.0)
        f = mix(col, (0, 0, 0), rnd.uniform(0, 0.12))
        c.rect((x, y_base - bh, x + bw, y_base), fill=f, r=3)
        c.rect((x + bw * 0.42, y_base - bh, x + bw * 0.58, y_base - bh * 0.7), fill=mix(f, WH, 0.35))
        x += bw + 6


def rack(c, x0, x1, y_top, y_bot, levels, upright=(40, 80, 150), beam=(232, 120, 40), seed=3):
    for x in (x0, x1):
        c.rect((x - 10, y_top, x + 10, y_bot), fill=upright)
        for y in range(int(y_top) + 10, int(y_bot), 26):
            c.circle(x, y, 3, fill=mix(upright, WH, 0.5))
    ys = [y_top + (y_bot - y_top) * f for f in levels]
    for k, y in enumerate(ys):
        c.rect((x0 - 10, y, x1 + 10, y + 16), fill=beam)
        if k < len(ys) - 1 or True:
            box_stack(c, x0 + 18, y, (x1 - x0 - 50) / 3, min(110, (ys[k] - (ys[k - 1] if k else y_top)) - 26) if k else 90, 3, seed=seed + k)


# =====================================================================  «герои» для раскладок с панелью
def hero_poei_flow(c, box):
    """3 шага POEI: offre d'emploi → formation jusqu'à 450 h → contrat visé. Текст — из раздела «La POEI en bref»."""
    x0, y0, x1, y1 = box
    c.card(box, fill=WH, r=26, sh_alpha=50, blur=12, off=(0, 6))
    steps = [("doc", "Offre d'emploi", "réelle", (0, 96, 170)),
             ("clock", "Formation", "jusqu'à 450 h", (230, 70, 80)),
             ("w5_contract", "Contrat visé", "CDI ou 6 mois +", (40, 140, 90))]
    n = len(steps)
    cw = (x1 - x0) / n
    cy = y0 + (y1 - y0) * 0.36
    for k, (ic, a, b, col) in enumerate(steps):
        cx = x0 + cw * (k + 0.5)
        c.circle(cx, cy, 52, fill=mix(col, WH, 0.86))
        icon(c, ic, cx, cy, 74, col, bg=mix(col, WH, 0.86))
        c.text((cx, y1 - 70), a, "db", 27, (30, 36, 50), anchor="mm")
        c.text((cx, y1 - 34), b, "sb", 25, col, anchor="mm")
        if k < n - 1:
            ax = cx + cw / 2
            c.line([(ax - 30, cy), (ax + 22, cy)], (180, 186, 196), 7)
            c.poly([(ax + 30, cy), (ax + 14, cy - 14), (ax + 14, cy + 14)], (180, 186, 196))


def hero_aula(c, box):
    """Мини-сцена «аудитория взрослых»: доска, преподаватель, спины трёх слушателей (без лиц)."""
    def fn(t):
        x0, y0, x1, y1 = box
        t.vgrad((x0, y0, x1, y1), (238, 232, 220), (226, 216, 198))
        bb = (x0 + 250, y0 + 26, x1 - 70, y0 + 190)
        t.rect((bb[0] - 10, bb[1] - 10, bb[2] + 10, bb[3] + 10), fill=(170, 176, 186), r=8)
        t.rect(bb, fill=(250, 252, 252), r=4)
        # схема на доске: блоки и стрелки (без текста)
        for k, col in enumerate(((0, 120, 160), (232, 120, 40), (40, 150, 90))):
            bx = bb[0] + 40 + k * 190
            t.rect((bx, bb[1] + 40, bx + 130, bb[1] + 100), outline=col, width=5, r=10)
            t.rect((bx + 20, bb[1] + 60, bx + 110, bb[1] + 70), fill=col, r=4)
            t.rect((bx + 20, bb[1] + 78, bx + 80, bb[1] + 86), fill=mix(col, WH, 0.4), r=4)
            if k < 2:
                t.line([(bx + 140, bb[1] + 70), (bx + 180, bb[1] + 70)], (120, 126, 136), 5)
        # преподаватель
        A.standing(t, x0 + 150, y1 + 60, 300, SKIN[1], (60, 44, 36), "short", (0, 110, 130), (50, 56, 70),
                   arm_r=(x0 + 250, y0 + 110))
        # спины слушателей
        for k, (x, hair, coat) in enumerate(((x0 + 360, (90, 64, 44), (200, 90, 60)), (x0 + 600, GREY_HAIR, (60, 90, 140)),
                                             (x0 + 840, (40, 34, 30), (90, 140, 90)))):
            WS.senior_back(t, x, y1 + 40, 0.72, coat, hair=hair)
        t.rect((x0, y1 - 26, x1, y1), fill=(176, 130, 92))
    S.clip_draw(c, box, 24, fn)


# =====================================================================  сцены концепции d (под заголовком)
def sc_de_supermarket(c):
    """Супермаркет: пожилой человек (седые волосы, без лица) выкладывает товар на полку; тележка с коробкой. Верх — заголовок."""
    c.vgrad((0, 0, W, 860), (246, 244, 238), (232, 228, 220))
    # стеллаж с товаром справа
    sx0, sx1 = 470, 1060
    c.rect((sx0, 330, sx1, 900), fill=(214, 218, 224))
    c.rect((sx0 + 14, 344, sx1 - 14, 900), fill=(236, 238, 242))
    rnd = random.Random(8)
    shelves = [440, 580, 720, 860]
    cols = [(222, 64, 50), (40, 120, 200), (250, 190, 40), (60, 160, 100), (240, 130, 40), (140, 90, 160), (250, 250, 250)]
    for k, y in enumerate(shelves):
        c.rect((sx0, y, sx1, y + 16), fill=(170, 176, 186))
        c.rect((sx0, y + 16, sx1, y + 34), fill=(250, 216, 60))                 # ценник-полоса
        x = sx0 + 24
        while x < sx1 - 60:
            if k == 1 and 640 < x < 820:           # пустое место, куда ставят товар
                x += 40
                continue
            wbx = rnd.choice((44, 52, 60))
            hbx = rnd.choice((70, 86, 100))
            col = rnd.choice(cols)
            if rnd.random() < 0.5:
                c.rect((x, y - hbx, x + wbx, y), fill=col, r=6)
                c.rect((x + 6, y - hbx * 0.66, x + wbx - 6, y - hbx * 0.4), fill=WH, alpha=200, r=4)
            else:
                c.rect((x + 8, y - hbx, x + wbx - 8, y - hbx + 14), fill=mix(col, (0, 0, 0), 0.3), r=4)
                c.rect((x + 2, y - hbx + 12, x + wbx - 2, y), fill=col, r=12)
                c.rect((x + 8, y - hbx * 0.55, x + wbx - 8, y - hbx * 0.3), fill=WH, alpha=200, r=4)
            x += wbx + 10
    # пол
    c.rect((0, 900, W, W), fill=(206, 208, 212))
    for x in range(0, W, 120):
        c.line([(x, 900), (x - 60, W)], (194, 196, 200), 3)
    # тележка-роллкейдж с коробками слева
    c.rect((60, 640, 330, 980), outline=(150, 156, 166), width=8, r=6)
    for x in (110, 170, 230, 290):
        c.line([(x, 640), (x, 980)], (170, 176, 186), 4)
    box_stack(c, 80, 820, 120, 110, 2, seed=4)
    box_stack(c, 90, 972, 110, 130, 2, seed=6)
    for x in (90, 300):
        c.circle(x, 1000, 18, fill=(60, 64, 72))
    # человек: седые волосы, фартук, тянется к полке
    px, pby, h = 560, 1080, 640
    fig = A.standing(c, px, pby, h, SKIN[0], GREY_HAIR, "short", (60, 110, 170), (50, 56, 70),
                     arm_r=(700, 560), arm_l=(640, 600))
    # фартук
    sh = pby - h * 0.79
    hip = pby - h * 0.46
    c.rect((px - h * 0.11, sh + h * 0.1, px + h * 0.11, hip + h * 0.16), fill=(0, 128, 128), r=h * 0.03)
    c.rect((px - h * 0.07, sh + h * 0.2, px + h * 0.07, sh + h * 0.26), fill=mix((0, 128, 128), WH, 0.3), r=6)
    # товар в руках
    c.rect((676, 500, 730, 590), fill=(40, 120, 200), r=8)
    c.rect((682, 530, 724, 556), fill=WH, alpha=210, r=4)
    return fig


def sc_es_almacen(c):
    """Учебный склад: стеллажи, погрузчик с учеником за рулём (каска, жилет), наставник с планшетом. Под карточкой сверху."""
    c.vgrad((0, 0, W, 860), (228, 234, 240), (212, 220, 228))
    for x in range(0, W, 180):
        c.rect((x, 0, x + 8, 860), fill=(206, 212, 220))
    rack(c, 40, 380, 300, 880, (0.25, 0.55, 0.85), seed=2)
    rack(c, 760, 1050, 300, 880, (0.25, 0.55, 0.85), seed=7)
    # пол
    c.rect((0, 880, W, W), fill=(196, 198, 196))
    c.rect((0, 930, W, 944), fill=(250, 204, 40))
    for x in range(0, W, 60):
        c.rect((x, 930, x + 30, 944), fill=(40, 40, 44))
    # погрузчик
    fx, fb = 470, 960        # центр корпуса, линия пола
    Y = (246, 176, 30)
    D = (44, 48, 58)
    c.rect((fx - 250, fb - 250, fx - 200, fb - 60), fill=D, r=10)                      # противовес
    c.rect((fx - 220, fb - 220, fx + 90, fb - 60), fill=Y, r=18)                        # корпус
    c.rect((fx - 190, fb - 200, fx + 60, fb - 180), fill=mix(Y, WH, 0.35), r=8)
    for x in (fx - 190, fx + 60):
        c.rect((x - 8, fb - 470, x + 8, fb - 210), fill=D)                              # стойки
    c.rect((fx - 210, fb - 490, fx + 80, fb - 462), fill=D, r=8)                       # крыша
    c.rect((fx + 110, fb - 560, fx + 140, fb - 50), fill=D, r=4)                        # мачта
    c.rect((fx + 150, fb - 560, fx + 170, fb - 50), fill=mix(D, WH, 0.2), r=4)
    c.rect((fx + 150, fb - 70, fx + 330, fb - 54), fill=D, r=4)                         # вилы
    c.rect((fx + 160, fb - 90, fx + 320, fb - 70), fill=(176, 130, 80))                 # паллет
    box_stack(c, fx + 170, fb - 90, 70, 120, 2, seed=11)
    # ученик за рулём
    sx, sy = fx - 70, fb - 200
    c.rect((sx - 46, sy - 150, sx + 46, sy + 10), fill=(60, 90, 140), r=40)              # торс
    vest(c, sx, sy - 150, sy + 5, 46)
    c.rect((sx - 12, sy - 176, sx + 12, sy - 148), fill=SKIN[1])
    c.circle(sx, sy - 206, 38, fill=SKIN[1])
    c.pie((sx - 40, sy - 246, sx + 40, sy - 170), 180, 360, (60, 44, 36))
    helmet(c, sx, sy - 206, 38, col=(250, 250, 250))
    c.line([(sx + 30, sy - 110), (sx + 110, sy - 80)], (60, 90, 140), 22)            # рука к рулю
    c.circle(sx + 116, sy - 80, 12, fill=SKIN[1])
    c.line([(sx + 90, sy - 110), (sx + 130, sy - 50)], D, 10)                          # руль
    c.ellipse((sx + 96, sy - 124, sx + 150, sy - 104), outline=D, width=8)
    for x, r in ((fx - 150, 62), (fx + 60, 50)):
        c.circle(x, fb - 10, r, fill=D)
        c.circle(x, fb - 10, r * 0.42, fill=(150, 156, 166))
    # наставник с планшетом справа
    mx = 900
    fig = A.standing(c, mx, 1080, 560, SKIN[2], (40, 34, 30), "short", (70, 76, 90), (50, 56, 70),
                     arm_l=(mx - 80, 760), arm_r=(mx - 40, 780))
    sh = 1080 - 560 * 0.79
    vest(c, mx, sh, 1080 - 560 * 0.46, 560 * 0.14, col=(250, 130, 40))
    hx, hy = fig["head"]
    helmet(c, hx, hy, fig["r"], col=(250, 210, 40))
    c.rect((mx - 130, 700, mx - 30, 830), fill=(120, 90, 60), r=8)                      # планшет
    c.rect((mx - 120, 716, mx - 40, 820), fill=WH, r=4)
    for k in range(4):
        c.rect((mx - 110, 732 + k * 20, mx - 52, 740 + k * 20), fill=(180, 186, 196), r=3)
    c.circle(mx - 80 + 60 * 0, 760, 0.1, fill=WH)


ROUGE_BADGE = (226, 58, 70)


def sc_fr_reception(c):
    """Ресепшн отеля: стойка, звонок, доска с ключами, стажёр (бейдж «EN FORMATION») и наставник. Сверху — плашки."""
    c.vgrad((0, 0, W, W), (250, 242, 230), (236, 222, 204))
    # стеновые панели
    for x in range(0, W, 216):
        c.rect((x + 6, 430, x + 210, 760), fill=(242, 230, 212), r=6)
    # доска с ключами
    kb = (640, 470, 1000, 660)
    c.shadow(kb, r=10, alpha=60, blur=8, off=(0, 6))
    c.rect(kb, fill=(126, 84, 52), r=10)
    for j in range(2):
        for i in range(6):
            x = kb[0] + 40 + i * 56
            y = kb[1] + 40 + j * 86
            c.circle(x, y, 6, fill=(230, 200, 120))
            c.line([(x, y), (x, y + 26)], (210, 180, 100), 4)
            c.rect((x - 12, y + 24, x + 12, y + 54), fill=(236, 176, 60) if (i + j) % 3 else (200, 80, 60), r=5)
    # лампа-бра
    c.glow((130, 450, 270, 560), (255, 230, 170), alpha=90, blur=24)
    c.rect((150, 470, 250, 540), fill=(250, 226, 170), r=30)
    c.rect((190, 540, 210, 560), fill=(170, 150, 120))
    # люди за стойкой (ноги скрыты стойкой)
    tx, ty = 420, 1180
    f1 = A.standing(c, tx, ty, 700, SKIN[0], (150, 96, 50), "bun", (30, 50, 90), (30, 40, 70), arm_r=(520, 800), arm_l=(360, 810))
    bx0, by0 = tx + 4, ty - 700 * 0.72
    c.rect((bx0, by0, bx0 + 96, by0 + 34), fill=WH, r=5, outline=(200, 206, 214), width=2)
    c.rect((bx0, by0, bx0 + 96, by0 + 9), fill=ROUGE_BADGE, r=4)
    c.text((bx0 + 48, by0 + 22), "EN FORMATION", "sb", 12, (30, 50, 90), anchor="mm")
    mx, my = 720, 1170
    A.standing(c, mx, my, 690, SKIN[2], (40, 34, 30), "short", (120, 30, 50), (40, 30, 40), arm_l=(620, 790), arm_r=(790, 820))
    c.rect((598, 760, 650, 830), fill=(40, 44, 54), r=6)                                  # планшет у наставника
    c.rect((604, 766, 644, 824), fill=(200, 226, 246), r=4)
    # стойка
    c.rect((40, 830, 1040, 862), fill=(240, 236, 228), r=6)
    c.rect((60, 862, 1020, W), fill=(160, 106, 66))
    S.wood(c, (60, 870, 1020, W), (170, 114, 72), (150, 98, 60), lines=5, seed=31)
    for x in range(60, 1020, 240):
        c.rect((x, 862, x + 10, W), fill=(136, 88, 54))
    # звонок, монитор, растение
    I.ICONS["w5_bell"](c, 250, 790, 110, (60, 64, 72))
    c.rect((820, 700, 990, 812), fill=(40, 44, 54), r=8)
    c.rect((890, 812, 920, 832), fill=(60, 64, 72))
    S.plant(c, 980, 832, 0.34, pot=(210, 110, 70))
    return f1


def sc_pt_flatlay(c):
    """Стол сверху: лист «CERTIFICADO» с печатью, проездной с автобусом, ланч-бокс, тетрадь, ручка, очки, кофе. Сверху — полоса-заголовок."""
    S.wood(c, (0, 0, W, W), (214, 170, 124), (196, 150, 106), lines=12, seed=9)
    # сертификат
    S.paper(c, (110, 400, 560, 900), -6, head="CERTIFICADO", lines=6, head_col=(20, 90, 70), head_size=34)
    c.circle(470, 820, 46, fill=(214, 60, 50))
    c.circle(470, 820, 30, outline=WH, width=4)
    c.poly([(440, 850), (426, 920), (452, 904), (466, 930), (476, 856)], (214, 60, 50))
    # тетрадь
    nb = (640, 380, 960, 700)
    c.shadow(nb, r=10, alpha=70, blur=10, off=(6, 10))
    c.rect(nb, fill=(0, 140, 110), r=10)
    c.rect((nb[0] + 30, nb[1] + 40, nb[2] - 30, nb[1] + 110), fill=WH, alpha=220, r=6)
    for k in range(10):
        c.circle(nb[0] + 4, nb[1] + 30 + k * 30, 9, fill=(200, 204, 210))
    S.pen(c, 680, 740, 990, 640, col=(30, 60, 140), w=14)
    # проездной
    pc = (620, 790, 900, 960)
    pts = rotpts([(pc[0], pc[1]), (pc[2], pc[1]), (pc[2], pc[3]), (pc[0], pc[3])], (pc[0] + pc[2]) / 2, (pc[1] + pc[3]) / 2, 8)
    c.poly([(x + 6, y + 10) for x, y in pts], (120, 90, 60), alpha=90)
    c.poly(pts, (30, 110, 190))
    icon(c, "bus", 700, 880, 100, WH, bg=(30, 110, 190))
    c.text((820, 870), "PASSE", "db", 34, WH, anchor="mm")
    # ланч-бокс (слева, не под кнопкой)
    lb = (36, 930, 330, 1090)
    c.shadow(lb, r=30, alpha=70, blur=10, off=(6, 10))
    c.rect(lb, fill=(236, 238, 240), r=30)
    c.rect((lb[0] + 16, lb[1] + 16, lb[2] - 16, lb[3]), fill=(250, 250, 250), r=24)
    c.poly([(70, 1060), (170, 966), (190, 1060)], (236, 200, 140))
    c.poly([(76, 1054), (170, 974), (184, 1054)], (250, 226, 170))
    c.line([(80, 1046), (178, 1046)], (100, 170, 80), 10)
    c.circle(262, 1010, 42, fill=(214, 44, 40))
    c.line([(262, 970), (268, 950)], (100, 64, 36), 6)
    c.poly([(268, 958), (302, 942), (288, 968)], (80, 160, 70))
    # кофе и очки
    c.circle(980, 1010, 70, fill=WH)
    c.circle(980, 1010, 54, fill=(120, 76, 44))
    c.circle(968, 1000, 16, fill=(160, 110, 70))


def sc_lt_radiator(c):
    """Комната: окно с зимой, батарея под окном, настенный календарь «RUGSĖJIS 2026» с обведённым 1, счёт и чашка на тумбе."""
    c.vgrad((0, 0, W, 880), (248, 244, 238), (236, 228, 218))
    # окно с зимним пейзажем
    wx0, wy0, wx1, wy1 = 560, 330, 1010, 640
    winter_window(c, (wx0, wy0, wx1, wy1), ((0.2, 150), (0.73, 190)), seed=3)
    c.rect((wx0, (wy0 + wy1) / 2 - 6, wx1, (wy0 + wy1) / 2 + 6), fill=WH)
    c.rect((wx0 - 36, wy1 + 16, wx1 + 36, wy1 + 34), fill=(240, 236, 228), r=4)
    # батарея
    rx0, rx1, ry0, ry1 = 590, 980, 700, 850
    c.shadow((rx0, ry0, rx1, ry1), r=10, alpha=50, blur=8, off=(0, 6))
    n = 11
    fw = (rx1 - rx0) / n
    for k in range(n):
        c.rect((rx0 + k * fw + 3, ry0, rx0 + (k + 1) * fw - 3, ry1), fill=(248, 248, 246), r=fw * 0.45)
        c.rect((rx0 + k * fw + fw * 0.3, ry0 + 16, rx0 + k * fw + fw * 0.42, ry1 - 16), fill=(226, 226, 222), r=4)
    c.rect((rx0 - 20, ry1 - 30, rx0 + 4, ry1 - 10), fill=(200, 200, 204), r=4)
    c.circle(rx0 - 36, ry1 - 20, 22, fill=WH, outline=(200, 200, 204), width=4)          # термостат
    c.line([(rx0 - 36, ry1 - 36), (rx0 - 36, ry1 - 26)], (220, 60, 50), 5)
    for k in range(3):                                                                      # тёплый воздух
        x = rx0 + 90 + k * 110
        pts = [(x + math.sin(i / 2.0) * 10, ry0 - 16 - i * 7) for i in range(10)]
        c.line(pts, (240, 150, 90), 5, alpha=160)
    # календарь
    cb = (70, 330, 470, 760)
    gy, cw, rh = WS.cal_month(c, cb, "RUGSĖJIS 2026", 1, 30, (200, 60, 50), week=("P", "A", "T", "K", "Pn", "Š", "S"))
    cx1 = cb[0] + 20 + cw * 1.5
    cy1 = gy + 44
    c.circle(cx1, cy1, 30, outline=(200, 60, 50), width=6)
    # пол
    c.rect((0, 880, W, W), fill=(196, 150, 108))
    S.wood(c, (0, 892, W, W), (206, 160, 116), (186, 140, 98), lines=5, seed=17)
    c.rect((0, 872, W, 892), fill=(250, 246, 238))
    # тумба со счётом и чашкой
    c.rect((90, 800, 440, 830), fill=(170, 120, 80), r=6)
    c.rect((110, 830, 420, 960), fill=(186, 136, 94), r=6)
    c.rect((140, 852, 390, 900), outline=(150, 104, 66), width=4, r=6)
    S.paper(c, (130, 700, 330, 820), -5, head="SĄSKAITA", lines=2, head_col=(200, 60, 50), head_size=22)
    S.teacup(c, 390, 790, 0.6, rim=(200, 60, 50))


def winter_window(c, box, trees, seed=3, frame=16):
    """Окно с зимним пейзажем; всё содержимое обрезано по стеклу (clip_draw)."""
    wx0, wy0, wx1, wy1 = box
    c.rect((wx0 - frame, wy0 - frame, wx1 + frame, wy1 + frame), fill=WH, r=8)

    def fn(t):
        t.vgrad((wx0, wy0, wx1, wy1), (150, 190, 226), (222, 236, 248))
        t.ellipse((wx0 - 80, wy1 - (wy1 - wy0) * 0.22, wx0 + (wx1 - wx0) * 0.6, wy1 + 80), fill=(250, 252, 255))
        t.ellipse((wx0 + (wx1 - wx0) * 0.4, wy1 - (wy1 - wy0) * 0.16, wx1 + 80, wy1 + 90), fill=(242, 246, 252))
        for fx, h in trees:
            W3.pine(t, wx0 + (wx1 - wx0) * fx, wy1 - (wy1 - wy0) * 0.08, h, snow=True)
        rnd = random.Random(seed)
        for _ in range(40):
            t.circle(rnd.uniform(wx0 + 8, wx1 - 8), rnd.uniform(wy0 + 8, wy1 - 8), rnd.uniform(2, 5), fill=WH, alpha=220)
    S.clip_draw(c, box, 4, fn)
    c.rect(((wx0 + wx1) / 2 - frame / 2, wy0, (wx0 + wx1) / 2 + frame / 2, wy1), fill=WH)


def phone_hand(c, cx, top, h, screen_fn):
    """Рука держит смартфон (кисть снизу слева, большой палец справа); screen_fn(c, box) рисует экран."""
    w = h * 0.5
    x0, x1 = cx - w / 2, cx + w / 2
    y0, y1 = top, top + h
    sk = SKIN[0]
    skd = mix(sk, (0, 0, 0), 0.12)
    # ладонь за телефоном
    c.rect((x0 - 30, y1 - h * 0.34, x1 + 10, y1 + 160), fill=skd, r=90)
    c.shadow((x0, y0, x1, y1), r=w * 0.13, alpha=110, blur=20, off=(0, 16))
    c.rect((x0, y0, x1, y1), fill=(28, 30, 36), r=w * 0.13)
    sc = (x0 + 14, y0 + 14, x1 - 14, y1 - 14)
    c.rect(sc, fill=WH, r=w * 0.1)
    c.rect(((x0 + x1) / 2 - 50, y0 + 26, (x0 + x1) / 2 + 50, y0 + 52), fill=(28, 30, 36), r=12)
    screen_fn(c, sc)
    # пальцы слева
    for k in range(4):
        fy = y1 - h * 0.3 + k * 58
        c.rect((x0 - 44, fy, x0 + 22, fy + 50), fill=sk, r=25)
    # большой палец справа
    c.rect((x1 - 44, y1 - h * 0.24, x1 + 22, y1 - h * 0.24 + 150), fill=sk, r=32)
    c.rect((x1 - 36, y1 - h * 0.24 + 10, x1 + 12, y1 - h * 0.24 + 52), fill=mix(sk, WH, 0.35), r=20)
    # манжета
    c.rect((x0 - 60, y1 + 60, x1 + 40, y1 + 200), fill=(70, 110, 160), r=20)


def pl_screen(c, sc):
    """Нейтральный макет экрана: карточка «Legitymacja emeryta-rencisty» без орла, герба, флага и логотипов."""
    x0, y0, x1, y1 = sc
    c.text((x0 + 26, y0 + 40), "9:41", "sb", 20, (40, 40, 40), anchor="lm")
    c.text((x0 + 26, y0 + 96), "Dokumenty", "db", 30, (30, 36, 50), anchor="lm")
    cb = (x0 + 20, y0 + 130, x1 - 20, y0 + 390)
    c.shadow(cb, r=20, alpha=70, blur=10, off=(0, 6))
    c.rect(cb, fill=(24, 96, 120), r=20)
    c.poly([(cb[0] + (cb[2] - cb[0]) * 0.55, cb[1]), (cb[2] - 20, cb[1]), (cb[2], cb[1] + 20), (cb[2], cb[3] - 20),
            (cb[2] - 20, cb[3]), (cb[0] + (cb[2] - cb[0]) * 0.3, cb[3])], (40, 132, 146))
    fs = c.fit("EMERYTA-RENCISTY", "db", cb[2] - cb[0] - 44, 1, 24)
    c.text((cb[0] + 22, cb[1] + 40), "LEGITYMACJA", "db", fs, WH, anchor="lm")
    c.text((cb[0] + 22, cb[1] + 72), "EMERYTA-RENCISTY", "db", fs, WH, anchor="lm")
    ph = (cb[0] + 22, cb[1] + 104, cb[0] + 112, cb[3] - 24)
    c.rect(ph, fill=(214, 232, 236), r=10)
    c.circle((ph[0] + ph[2]) / 2, ph[1] + 44, 22, fill=(120, 150, 160))
    c.pie((ph[0] + 12, ph[1] + 72, ph[2] - 12, ph[3] + 40), 180, 360, (120, 150, 160))
    avail = cb[2] - 20 - (ph[2] + 18)
    for k, f in enumerate((0.95, 0.7, 0.85, 0.55)):
        c.rect((ph[2] + 18, ph[1] + 12 + k * 32, ph[2] + 18 + avail * f, ph[1] + 26 + k * 32), fill=(200, 230, 234), r=6, alpha=200)
    # другие документы — серые строки
    for k in range(3):
        ry = cb[3] + 30 + k * 86
        c.rect((x0 + 20, ry, x1 - 20, ry + 70), fill=(242, 244, 247), r=14)
        c.rect((x0 + 40, ry + 18, x0 + 90, ry + 52), fill=(214, 220, 228), r=6)
        c.rect((x0 + 110, ry + 22, x0 + 110 + (170 - k * 30), ry + 34), fill=(200, 206, 214), r=5)
        c.rect((x0 + 110, ry + 42, x0 + 110 + (110 - k * 10), ry + 50), fill=(222, 226, 232), r=4)


def sc_pl_phone(c):
    """Рука с телефоном справа (нейтральный макет карточки), слева — 3 шага из статьи. Сверху — заголовок."""
    c.vgrad((0, 0, W, W), (238, 245, 250), (214, 230, 242))
    c.circle(160, 900, 120, fill=WH, alpha=60)
    c.circle(980, 300, 90, fill=WH, alpha=60)
    phone_hand(c, 835, 300, 700, pl_screen)
    steps = ["Pobierz aplikację", "Potwierdź tożsamość", "Dodaj legitymację"]
    for k, s_ in enumerate(steps):
        y = 380 + k * 150
        c.card((50, y, 540, y + 110), fill=WH, r=55, sh_alpha=60, blur=10, off=(0, 6))
        c.circle(105, y + 55, 36, fill=(20, 120, 160))
        c.text((105, y + 56), str(k + 1), "db", 36, WH, anchor="mm")
        c.block(s_, "sb", 34, y + 34, 380, (30, 40, 70), align="left", x=160, max_lines=1)
        if k < 2:
            c.line([(105, y + 112), (105, y + 148)], (20, 120, 160), 6)


SCENES = dict(w5_de_supermarket=sc_de_supermarket, w5_es_almacen=sc_es_almacen, w5_fr_reception=sc_fr_reception,
              w5_pt_flatlay=sc_pt_flatlay, w5_lt_radiator=sc_lt_radiator, w5_pl_phone=sc_pl_phone)
for _k, _v in SCENES.items():
    setattr(WS, _k, _v)


# =====================================================================  своя раскладка: перенос LT-формата
def lt_grid(P, t):
    """Доказанный LT-формат (AlexZHeatPumpsLT / 0819-GE02): рамка-градиент, заголовок, «фото», 4 плитки, 4 красные кнопки.
    Плитки — с иконкой и подписью в 2 строки; кнопки «SUŽINOKITE / DAUGIAU»."""
    p = P["pal"]
    c = C(WH)
    c.hgrad((0, 0, W, W), (70, 140, 200), (240, 140, 60))
    c.rect((18, 18, 1062, 1062), fill=WH, r=34)
    c.block(t["title"], "db", t.get("size", 58), 44, 980, (20, 22, 26), max_lines=1)
    t["hero"](c, (40, 136, 1040, 520))
    g = 22
    tw = (1000 - 3 * g) / 4
    for k, (ic, lab) in enumerate(t["tiles"]):
        x0 = 40 + k * (tw + g)
        tb = (x0, 548, x0 + tw, 770)
        c.shadow(tb, r=16, alpha=70, blur=6, off=(0, 4))
        c.rect(tb, fill=(234, 236, 238), r=16, outline=(150, 152, 156), width=3)
        icon(c, ic, (tb[0] + tb[2]) / 2, tb[1] + 70, 96, p["icon"], bg=(234, 236, 238))
        fs = min(c.fit(x, "sb", tw - 24, 2, 32) for _, x in t["tiles"])
        nl = len(c.wrap(lab, c.font("sb", fs), tw - 24))
        c.block(lab, "sb", fs, tb[1] + 168 - nl * c.lh("sb", fs, 1.04) / 2, tw - 24, (20, 22, 26), cx=(tb[0] + tb[2]) / 2,
                max_lines=2, gap=1.04)
        bb = (x0, 792, x0 + tw, 912)
        c.shadow(bb, r=18, alpha=110, blur=8, off=(0, 6))
        c.rect(bb, fill=p["btn"], r=18)
        c.rect((bb[0] + 8, bb[1] + 6, bb[2] - 8, bb[1] + 46), fill=WH, r=14, alpha=40)
        l1, l2 = t["btn_lines"]
        sz = min(c.fit(l1, "db", tw - 26, 1, 36), c.fit(l2, "db", tw - 26, 1, 36))
        c.text(((bb[0] + bb[2]) / 2, bb[1] + 40), l1, "db", sz, WH, anchor="mm")
        c.text(((bb[0] + bb[2]) / 2, bb[1] + 84), l2, "db", sz, WH, anchor="mm")
    if t.get("foot"):
        c.block(t["foot"], "sb", 34, 950, 980, (60, 64, 72), max_lines=1)
    return c


def hero_lt_room(c, box):
    """«Фото» для lt_grid: батарея под окном, зима за окном, счёт на подоконнике (без сумм)."""
    def fn(t):
        x0, y0, x1, y1 = box
        H = y1 - y0
        t.vgrad((x0, y0, x1, y1), (246, 240, 230), (232, 222, 208))
        wx0, wy0, wx1, wy1 = x0 + 330, y0 + 20, x1 - 40, y0 + H * 0.52
        winter_window(t, (wx0, wy0, wx1, wy1), ((0.14, 110), (0.62, 130), (0.83, 90)), seed=5, frame=12)
        t.rect((wx0 - 30, wy1 + 12, wx1 + 30, wy1 + 28), fill=(240, 236, 228), r=4)
        rx0, rx1, ry0, ry1 = wx0 + 20, wx1 - 20, wy1 + 60, y1 - 30
        n = 14
        fw = (rx1 - rx0) / n
        t.shadow((rx0, ry0, rx1, ry1), r=10, alpha=50, blur=8, off=(0, 6))
        for k in range(n):
            t.rect((rx0 + k * fw + 3, ry0, rx0 + (k + 1) * fw - 3, ry1), fill=(250, 250, 248), r=fw * 0.45)
            t.rect((rx0 + k * fw + fw * 0.3, ry0 + 12, rx0 + k * fw + fw * 0.42, ry1 - 12), fill=(226, 226, 222), r=4)
        t.circle(rx0 - 28, ry1 - 18, 18, fill=WH, outline=(200, 200, 204), width=4)
        t.line([(rx0 - 28, ry1 - 32), (rx0 - 28, ry1 - 22)], (220, 60, 50), 4)
        for k in range(4):
            x = rx0 + 60 + k * 120
            pts = [(x + math.sin(i / 2.0) * 8, ry0 - 10 - i * 5) for i in range(8)]
            t.line(pts, (240, 150, 90), 4, alpha=160)
        # слева — счёт и календарный лист с «1»
        S.paper(t, (x0 + 40, y0 + 40, x0 + 280, y0 + 250), -4, head="SĄSKAITA", lines=4, head_col=(200, 60, 50), head_size=24)
        cb = (x0 + 70, y0 + 230, x0 + 270, y1 - 20)
        t.shadow(cb, r=10, alpha=70, blur=10, off=(0, 8))
        t.rect(cb, fill=WH, r=10)
        t.rect((cb[0], cb[1], cb[2], cb[1] + 44), fill=(200, 60, 50), r=10)
        t.rect((cb[0], cb[1] + 24, cb[2], cb[1] + 44), fill=(200, 60, 50))
        t.text(((cb[0] + cb[2]) / 2, cb[1] + 24), "RUGSĖJIS", "db", 24, WH, anchor="mm")
        t.text(((cb[0] + cb[2]) / 2, (cb[1] + 44 + cb[3]) / 2 + 4), "1", "db", 80, (40, 40, 50), anchor="mm")
    S.clip_draw(c, box, 22, fn)


# =====================================================================  своя раскладка: карточка «сколько стоит» LT (3 колонки)
FN = dict(W4.FN)
FN.update({"lt_grid": lt_grid})


def hero_de_dawn(c, box):
    """«Фото» для pills6 DE: офис на рассвете — окно с восходом, часы около 6, тележка уборщика, стол с монитором. Людей нет."""
    def fn(t):
        x0, y0, x1, y1 = box
        H = y1 - y0
        t.vgrad((x0, y0, x1, y1), (244, 240, 234), (230, 224, 214))
        wx0, wy0, wx1, wy1 = x0 + 360, y0 + 22, x1 - 30, y0 + H * 0.66
        t.rect((wx0 - 10, wy0 - 10, wx1 + 10, wy1 + 10), fill=(250, 250, 248), r=6)
        t.vgrad((wx0, wy0, wx1, wy1), (250, 170, 116), (252, 228, 184))
        t.circle(wx0 + 330, wy1 - 58, 46, fill=(255, 238, 176))
        rnd = random.Random(4)
        x = wx0
        while x < wx1 - 20:
            bw = min(rnd.uniform(40, 90), wx1 - x)
            bh = rnd.uniform(30, 90)
            t.rect((x, wy1 - bh, x + bw, wy1), fill=(206, 150, 140))
            x += bw + 6
        for k in range(1, 4):
            xx = wx0 + (wx1 - wx0) * k / 4
            t.rect((xx - 5, wy0, xx + 5, wy1), fill=(250, 250, 248))
        t.rect((wx0 - 20, wy1 + 10, wx1 + 20, wy1 + 22), fill=(236, 232, 224), r=3)
        clock_face(t, x0 + 84, y0 + 76, 48, h=6, m=0)
        # стол и монитор (справа, перед окном)
        t.rect((wx0 + 120, y1 - 58, x1, y1 - 40), fill=(196, 164, 124))
        t.rect((wx0 + 200, y1 - 40, wx0 + 214, y1), fill=(170, 140, 104))
        t.rect((x1 - 60, y1 - 40, x1 - 46, y1), fill=(170, 140, 104))
        t.rect((wx0 + 420, y1 - 150, wx0 + 560, y1 - 70), fill=(50, 54, 64), r=6)
        t.rect((wx0 + 484, y1 - 72, wx0 + 496, y1 - 58), fill=(70, 74, 84))
        t.rect((wx0 + 180, y1 - 90, wx0 + 300, y1 - 58), fill=(246, 246, 244), r=3)
        # тележка уборщика
        cx0, cy1 = x0 + 150, y1 - 18
        t.line([(cx0 + 96, cy1 - 250), (cx0 + 76, cy1 - 150)], (170, 120, 70), 8)
        t.rect((cx0, cy1 - 150, cx0 + 180, cy1 - 132), fill=(60, 64, 74), r=6)
        t.rect((cx0 + 8, cy1 - 132, cx0 + 22, cy1 - 20), fill=(60, 64, 74))
        t.rect((cx0 + 158, cy1 - 132, cx0 + 172, cy1 - 20), fill=(60, 64, 74))
        t.rect((cx0, cy1 - 36, cx0 + 180, cy1 - 22), fill=(60, 64, 74), r=6)
        t.poly([(cx0 + 28, cy1 - 130), (cx0 + 104, cy1 - 130), (cx0 + 96, cy1 - 40), (cx0 + 36, cy1 - 40)], (40, 150, 220))
        t.rect((cx0 + 120, cy1 - 206, cx0 + 156, cy1 - 150), fill=(250, 196, 40), r=8)
        t.rect((cx0 + 130, cy1 - 222, cx0 + 146, cy1 - 204), fill=(60, 64, 74), r=3)
        for x in (cx0 + 16, cx0 + 164):
            t.circle(x, cy1 - 8, 11, fill=(40, 44, 50))
    S.clip_draw(c, box, 22, fn)


# =====================================================================  ПАКЕТЫ
# ---------------------------------------------------------------- 1. DE · джобсы · мини-джоб на пенсии (Employment: без сумм, без обещания работы)
NAVY1, TEAL1, ORG1 = (26, 40, 70), (0, 128, 128), (226, 92, 36)
PACKS[1] = dict(
    doc="DE-minijob-rentner-2026-09-29", cta="Mehr erfahren",
    pal=dict(bg=(243, 246, 248), ink=NAVY1, sub=(84, 96, 108), acc=TEAL1, btn=ORG1, tile=WH, tile_ink=NAVY1, icon=NAVY1,
             iconbg=(222, 240, 238)),
    a=dict(fn="pills6", title="Minijob im Ruhestand: Welche Tätigkeiten passen?", sub="Feste, kurze Einsätze – typische Beispiele:",
           size=54, hero=hero_de_dawn, hero_h=250,
           tiles=[("w5_bucket", "Büroreinigung"), ("med_bag", "Praxisreinigung"), ("home_help", "Privathaushalt"),
                  ("basket", "Einzelhandel"), ("w5_newspaper", "Prospekte, Zeitungen"), ("w5_bell", "Empfang, Pforte")],
           src="раздел «Welche Jobs passen? Typische Beispiele» (6 из 8 пунктов списка) + «Reinigung: der häufigste Einstieg» (панель: офис рано утром)",
           note="панель «офис на рассвете» (окно с восходом, часы около 6, тележка уборщика, без людей) + 6 плиток-кнопок с видами мини-джоба, у каждой «Mehr erfahren»; без 603 €, без сумм, без «Wir stellen ein»"),
    b=dict(fn="quiz", layout="card", title="Minijob in Rente 2026:", title2="Wird die Rente gekürzt?", size=58,
           sub="Die häufigste Frage vor dem ersten Arbeitstag", tag="QUIZ", step="Frage 1 von 3", prog=0.33,
           q="Kürzt ein Minijob die Altersrente, wenn die Regelaltersgrenze erreicht ist?",
           opts=["Ja, immer", "Nein", "Nur ab 10 Stunden pro Woche", "Weiß nicht"],
           pal=dict(bg=(255, 246, 222), bg2=(252, 230, 176), ink=NAVY1, sub=(96, 90, 70), acc=TEAL1, t2=ORG1, deco=True),
           src="раздел «Kürzt der Minijob die Rente?» (после Regelaltersgrenze — без ограничений) + «Die Minijob-Grenze 2026 in Zahlen» (≈10 ч в неделю)",
           note="тёплый жёлтый фон, карточка-тест; вопрос о правиле, не о зрителе; правильный ответ «Nein» — в статье"),
    c=dict(fn="compare", layout="twocol", title="Minijob oder kurzfristige Beschäftigung?", sub="Zwei Wege im Ruhestand – was 2026 gilt",
           size=54, cols=[("MINIJOB", "calendar", TEAL1), ("KURZFRISTIG", "hourglass", ORG1)],
           rows=[("DAUER", "dauerhaft, jeden Monat", "höchstens 3 Monate oder 70 Arbeitstage im Jahr"),
                 ("VERDIENSTGRENZE", "feste Monatsgrenze", "keine feste Verdienstgrenze"),
                 ("PASST ZU", "festen, kurzen Einsätzen", "Saisonarbeit: Weihnachtsgeschäft, Ernte")],
           foot="Bei Erwerbsminderungsrente gelten eigene Grenzen",
           src="раздел «Kurzfristig oder dauerhaft? Eine Checkliste vor dem Start» + «Welche Jobs passen?» (feste, kurze Einsätze)",
           note="две колонки мини-джоб vs краткосрочная занятость; граница — словами, без суммы"),
    d=dict(fn="scene_d", scene="w5_de_supermarket", style="card", card_box=(60, 34, 1020, 400), frame=True, font="lserb",
           kicker="MINIJOB 2026", title="Wie viel darf man im Ruhestand dazuverdienen?", size=54, lines=2, btn_size=38, btn_off=64, pad=46,
           pal=dict(frame=TEAL1, ink=NAVY1, sub=(84, 96, 108), acc=TEAL1, btn=ORG1),
           src="заголовок статьи «…Wie viel man dazuverdienen darf…» + раздел «Welche Jobs passen?» (Aushilfe im Einzelhandel, Auffüllen der Regale)",
           note="супермаркет: человек с седыми волосами (без лица) в фартуке ставит товар на полку, роллкейдж с коробками; карточка в рамке с вопросом-крючком без суммы"),
)

# ---------------------------------------------------------------- 2. ES · обучение · курсы с compromiso de contratación (без обещания работы)
NAVY2, ORG2, RED2 = (28, 36, 64), (232, 120, 30), (208, 48, 48)
PACKS[2] = dict(
    doc="ES-cursos-compromiso-2026-09-29", cta="Más información",
    pal=dict(bg=(252, 246, 236), ink=NAVY2, sub=(96, 90, 84), acc=ORG2, btn=RED2, tile=WH, tile_ink=NAVY2, icon=NAVY2,
             iconbg=(252, 232, 206)),
    a=dict(fn="grid6", title="Cursos gratuitos con compromiso de contratación", sub="Especialidades habituales en 2026 – elige un área:",
           size=54, tiles=[("w5_forklift", "Carretillero y almacén"), ("care_hands", "Atención sociosanitaria"),
                           ("soup_bowl", "Hostelería y cocina"), ("squeegee", "Limpieza profesional"),
                           ("bolt", "Soldadura y electricidad"), ("w3_headset", "Atención al cliente")],
           src="раздел «Del curso de carretillero al sector sociosanitario: especialidades habituales» + лид (gratuitos)",
           note="6 плиток 3×2 = специальности из статьи, у каждой «Más información»; без зарплаты, без «te contratamos»"),
    b=dict(fn="quiz", layout="card2x2", title="Cursos con compromiso de contratación:", title2="¿cuánto se contrata?", size=54,
           tag="TEST", step="Pregunta 1 de 3", prog=0.33,
           q="En Madrid y Castilla y León, ¿a qué parte de los alumnos se comprometen a contratar las empresas?",
           opts=["Al 10 %", "Del 40 % al 50 %", "Al 100 %", "No lo sé"],
           pal=dict(bg=(28, 36, 64), bg2=(14, 20, 40), ink=WH, sub=(210, 214, 230), acc=ORG2, t2=(250, 190, 90), btn=RED2, deco=True),
           src="раздел «Cuánto se contrata: del 40 % al 50 % de los alumnos» (Madrid ≥ 40 %, Castilla y León ≥ 50 %)",
           note="тёмно-синий фон, тест 2×2; вопрос о правиле программы, не о зрителе; регионы названы как факт статьи, не локация зрителя"),
    c=dict(fn="compare", layout="table", title="¿Curso normal o con compromiso de contratación?", sub="Qué cambia para el alumno", size=52,
           cols=[("CURSO NORMAL", "w5_cert", (110, 116, 130)), ("CON COMPROMISO", "handshake", ORG2)],
           rows=[("Al terminar", "un certificado", "certificado y contratos para parte del grupo"),
                 ("Empleo", "se busca después", "empresa comprometida antes de empezar"),
                 ("Contrato", "probabilidad habitual", "probabilidad mucho más alta, no asegurada")],
           foot="Gratis para el alumno: con fondos públicos",
           src="раздел «Qué es un curso con compromiso de contratación» (порядок меняется; не plaza asegurada, «probabilidad mucho más alta que en un curso normal») + последний абзац (gratuitos, fondos públicos)",
           note="таблица обычный курс vs с compromiso; прямо сказано «no asegurada» — без обещания работы"),
    d=dict(fn="scene_d", scene="w5_es_almacen", style="card", card_box=(60, 34, 1020, 392), frame=True, font="lserb",
           kicker="FORMACIÓN PARA EL EMPLEO 2026", title="Cursos gratuitos con compromiso de contratación: cómo funcionan",
           sub="Porcentajes, especialidades y quién puede apuntarse", size=48, lines=2, btn_size=36, btn_off=56, pad=40,
           pal=dict(frame=ORG2, ink=NAVY2, sub=(96, 90, 84), acc=ORG2, btn=RED2),
           src="заголовок и лид статьи + раздел «Del curso de carretillero…» (logística y almacén) + «El certificado de profesionalidad» (prácticas en empresa)",
           note="учебный склад: стеллажи, погрузчик с учеником (каска, жилет), наставник с планшетом; лиц нет; карточка в рамке"),
)

# ---------------------------------------------------------------- 3. FR · обучение · POEI (без обещания работы и зарплаты)
BLEU3, ROUGE3, CIEL3 = (20, 44, 100), (226, 58, 70), (0, 96, 170)
PACKS[3] = dict(
    doc="FR-poei-2026-09-29", cta="En savoir plus",
    pal=dict(bg=(240, 245, 252), ink=BLEU3, sub=(80, 92, 110), acc=CIEL3, btn=ROUGE3, tile=WH, tile_ink=BLEU3, icon=BLEU3,
             iconbg=(222, 232, 248)),
    a=dict(fn="list5", title="POEI\u00a0: formation financée avant l'embauche", sub="Dans quels métiers\u00a0? Choisissez un secteur\u00a0:", size=54,
           hero=hero_poei_flow, hero_h=210,
           tiles=[("w5_forklift", "Transport et logistique"), ("helmet", "Bâtiment et industrie"),
                  ("care_hands", "Aide à la personne et santé"), ("squeegee", "Propreté, sécurité, commerce"),
                  ("w5_bell", "Hôtellerie et restauration")],
           hero_text="Offre d'emploi réelle → Formation jusqu'à 450 h → Contrat visé CDI ou 6 mois +",
           src="раздел «La POEI en bref» (3 шага, CDI или ≥ 6 мес.) + «Jusqu'à 450 heures» + «Métiers qui recrutent : où la POEI est la plus fréquente» (5 секторов)",
           note="панель из 3 шагов механизма POEI + 5 строк-кнопок по секторам из статьи, у каждой «En savoir plus»; без зарплаты, без «nous recrutons»"),
    b=dict(fn="quiz", layout="card", title="Formation rémunérée\u00a0?", title2="Le statut pendant la POEI", size=60,
           tag="QUIZ POEI", step="Question 1 sur 3", prog=0.33,
           q="Pendant la formation POEI, le candidat a le statut de…",
           opts=["Salarié en CDI", "Stagiaire de la formation professionnelle", "Intérimaire", "Je ne sais pas"],
           pal=dict(bg=(255, 244, 236), bg2=(252, 224, 206), ink=BLEU3, sub=(90, 80, 80), acc=ROUGE3, t2=CIEL3, deco=True),
           src="раздел «Formation rémunérée ? Ce que perçoit le candidat pendant la POEI» (статус stagiaire, не salarié)",
           note="персиковый фон, карточка-тест; вопрос о статусе в программе, не о зрителе; без сумм"),
    c=dict(fn="compare", layout="split", title="POEI ou POEC\u00a0: quelle différence\u00a0?", sub="Formation avant l'embauche, individuelle ou collective",
           size=52, cols=[("POEI", "person_check", CIEL3, ["Une offre d'emploi réelle", "Sur mesure, jusqu'à 450\u00a0h", "Engagement de l'entreprise"]),
                          ("POEC", "people2", ROUGE3, ["Un groupe de candidats", "Un secteur qui recrute", "Pas d'engagement individuel"])],
           pal=dict(bg=(240, 245, 252), ink=BLEU3, sub=(80, 92, 110), btn=BLEU3, vs_bg=WH, vs_ink=BLEU3),
           src="раздел «Avant de signer» (последний абзац про POEC) + «La POEI en bref» + «Jusqu'à 450 heures»",
           note="сплит POEI vs POEC (синий / красный), пункты — из статьи"),
    d=dict(fn="scene_d", scene="w5_fr_reception", style="bars", y=40,
           bars=[("FORMATION FINANCÉE", WH, BLEU3), ("AVANT L'EMBAUCHE\u00a0:", BLEU3, None), ("JUSQU'À 450 HEURES", WH, ROUGE3)],
           bar_size=76, cond=0.8, btn_size=42, max_w=960, pal=dict(btn=ROUGE3),
           scene_text="бейдж «EN FORMATION» на стажёре",
           src="заголовок и лид статьи + раздел «Métiers qui recrutent…» (formation hôtellerie: réceptionniste, part des heures dans l'établissement)",
           note="плашки (формула рабочих крео владельца) + ресепшн отеля: стажёр с бейджем и наставник за стойкой, звонок, доска с ключами; лиц нет"),
)

# ---------------------------------------------------------------- 4. PT · обучение · курсы IEFP (без сумм стипендии и обещания работы)
VERDE4, LAR4, MENTA4 = (16, 70, 56), (232, 110, 20), (0, 140, 100)
PACKS[4] = dict(
    doc="PT-cursos-iefp-2026-09-29", cta="Saiba mais",
    pal=dict(bg=(240, 248, 244), ink=VERDE4, sub=(80, 100, 94), acc=MENTA4, btn=LAR4, tile=WH, tile_ink=VERDE4, icon=VERDE4,
             iconbg=(220, 240, 230)),
    a=dict(fn="grid", layout="2x2", title="Cursos IEFP 2026: que modalidade escolher?", sub="Formação gratuita e certificada – escolha uma:",
           size=56, tiles=[("cap", "EFA: 9.º ou 12.º ano + qualificação"), ("w3_wrench", "Aprendizagem com formação em empresa"),
                           ("w5_blocks", "Formação modular de 25 ou 50 horas"), ("laptop", "Módulos online à distância")],
           src="раздел «Que cursos IEFP existem em 2026» (EFA, aprendizagem, modular 25/50 h) + «Cursos online: o que existe à distância» + лид (gratuitos)",
           note="2×2 модальностей курсов из статьи, у каждой «Saiba mais»; без сумм, без «estamos a contratar»"),
    b=dict(fn="quiz", layout="card", title="Bolsa de formação IEFP:", title2="a regra que muitos não conhecem", size=58,
           tag="QUIZ", step="Pergunta 1 de 3", prog=0.33,
           q="Quem já recebe subsídio de desemprego recebe também a bolsa de formação?",
           opts=["Sim, sempre", "Em regra, não", "Só nos cursos online", "Não sei"],
           pal=dict(bg=(40, 78, 62), ink=WH, sub=(214, 230, 220), acc=LAR4, t2=(250, 214, 100), btn=LAR4, chalk=True),
           src="раздел «Bolsa de formação, subsídio de alimentação e transporte» (bolsa não se acumula com o subsídio de desemprego)",
           note="школьная доска, карточка-тест; вопрос о правиле про третье лицо, не о зрителе; без сумм"),
    c=dict(fn="compare", layout="stacked", title="Curso IEFP presencial ou online?", sub="O que muda nos apoios em 2026", size=54,
           cols=[("PRESENCIAL", "people2", MENTA4, (226, 244, 236), VERDE4,
                  ["Gratuito e com certificado", "Horário laboral ou pós-laboral", "Pode ter bolsa, alimentação, transporte"]),
                 ("ONLINE", "laptop", LAR4, (254, 238, 222), (90, 50, 10),
                  ["Gratuito, certificado por unidade", "À distância, com sessões online", "Bolsa e apoios: nem sempre se aplicam"])],
           foot="Peça por escrito a lista de apoios da turma",
           src="раздел «Cursos online: o que existe à distância» (apoios nem sempre se aplicam) + «Que cursos IEFP existem» (horário laboral e pós-laboral) + «Bolsa…» (pedir por escrito)",
           note="две карточки друг над другом: очно vs онлайн, что меняется в поддержке; без сумм"),
    d=dict(fn="scene_d", scene="w5_pt_flatlay", style="band", band_h=330, size=54, lines=3,
           title="Curso gratuito com certificado – e, em muitos casos, bolsa, alimentação e transporte",
           sub="Como funcionam os cursos IEFP em 2026", btn_y=1000,
           pal=dict(band=VERDE4, band_ink=WH, band_sub=(200, 236, 220), btn=LAR4),
           scene_text="на предметах: CERTIFICADO / PASSE",
           src="лид статьи + раздел «Bolsa de formação, subsídio de alimentação e transporte» + «Formação certificada: o que vale o certificado»",
           note="стол сверху: лист «CERTIFICADO» с печатью (без логотипа), проездной «PASSE» с автобусом, ланч-бокс, тетрадь, кофе; «em muitos casos» — как в статье"),
)

# ---------------------------------------------------------------- 5. LT · пенсионеры · компенсация за отопление (без суммы компенсации и «jums priklauso»)
RED5, BLUE5, INK5 = (206, 32, 40), (24, 90, 160), (20, 40, 80)
PACKS[5] = dict(
    doc="LT-sildymo-kompensacija-2026-09-29", cta="Sužinokite daugiau",
    pal=dict(bg=(236, 242, 250), ink=INK5, sub=(80, 90, 104), acc=BLUE5, btn=RED5, tile=WH, tile_ink=INK5, icon=(30, 50, 80),
             iconbg=(222, 234, 248)),
    a=dict(fn="lt_grid", title="Kompensacija už šildymą 2026", hero=hero_lt_room, size=58,
           tiles=[("w3_radiator", "Centralizuotas šildymas"), ("w5_logs", "Malkos, kietasis kuras"), ("w5_flame", "Dujos"),
                  ("w5_tap", "Karštas vanduo")],
           btn_lines=("SUŽINOKITE", "DAUGIAU"), foot="Kas gali būti kompensuojama? Pasirinkite",
           scene_text="на «фото»: SĄSKAITA / RUGSĖJIS 1",
           src="раздел «Kas yra kompensacija už šildymą» (центральное, дрова/газ по нормам топлива, горячая вода) + «Registracija…» (с 1 сентября)",
           note="перенос доказанного LT-формата теплонасосов (градиентная рамка, «фото», 4 плитки, красные кнопки «SUŽINOKITE DAUGIAU»): батарея под окном, зима, счёт и лист календаря «1»; без суммы компенсации, без герба и логотипа SPIS"),
    b=dict(fn="quiz", layout="calc", title="Kompensacija už šildymą:", title2="kodėl delsti neverta", size=58,
           steps=[("Sąskaita", "done"), ("Prašymas", "now"), ("Kompensacija", "todo")], tag="KLAUSIMAS 1 / 3", step="", prog=0.33,
           q="Nuo kada paprastai skiriama kompensacija už šildymą?",
           opts=["Nuo sezono pradžios", "Nuo prašymo mėnesio", "Nuo sausio 1 d.", "Nežinau"],
           pal=dict(bg=(236, 242, 250), bg2=(206, 222, 242), ink=INK5, sub=(70, 84, 104), acc=BLUE5, t2=RED5, btn=RED5),
           src="раздел «Registracija dėl šildymo kompensacijos» («skiriama nuo to mėnesio, kurį pateiktas prašymas, todėl… delsti neverta»)",
           note="опросник-степпер (счёт → заявление → компенсация) и вопрос о правиле; не о зрителе, без сумм"),
    c=dict(fn="table3", title="Mažesnė sąskaita už šildymą: 3\u00a0keliai", sub="Kas padeda šį sezoną, o kas – ilgainiui", size=54,
           cols=[("KOMPENSACIJA", "w5_doc_euro", BLUE5), ("ORAS–ORAS", "w3_split_unit", (0, 130, 110)),
                 ("ORAS–VANDUO", "w3_outdoor_unit", (226, 110, 30))],
           rows=[("Kada padeda", "šį šildymo sezoną", "ilgainiui", "ilgainiui"),
                 ("Kaip veikia", "tiekėjas išrašo mažesnę sąskaitą", "šildo orą, kaip kondicionierius",
                  "šildo radiatorius, ruošia karštą vandenį"),
                 ("Kaina su montavimu", "–", "apie 1\u00a0000–2\u00a0000\u00a0€ (1 vidinis blokas)", "apie 6\u00a0000–12\u00a0000\u00a0€")],
           foot="Pirmiausia – prašymas dėl kompensacijos",
           src="раздел «Kaip sumažinti sąskaitą: apšiltinimas ar šilumos siurblys, kaina su montavimu» (ориентиры цен) + «Jei reikia lėšų…» (pirmiausia – prašymas)",
           note="таблица на 3 колонки: компенсация / воздух-воздух / воздух-вода (ключи Oras Oras … Kaina, Oras Vanduo Kaina su Montavimu); цены — ориентиры статьи, суммы компенсации нет"),
    d=dict(fn="scene_d", scene="w5_lt_radiator", style="top", y=40, size=54, lines=2,
           title="Kompensacija už šildymą 2026: prašymai – nuo rugsėjo 1 d.", sub="Kam ji priklauso ir kaip užsiregistruoti per SPIS",
           btn_y=1000, pal=dict(ink=INK5, sub=(70, 84, 104), acc=BLUE5, btn=RED5),
           scene_text="на календаре: RUGSĖJIS 2026 (1 обведено), на листе: SĄSKAITA",
           src="заголовок статьи + раздел «Registracija dėl šildymo kompensacijos: per SPIS arba savivaldybėje» (с 1 сентября)",
           note="комната: батарея под окном, зима, настенный календарь сентября с обведённым 1, счёт и чашка на тумбе; без герба и логотипа SPIS/министерства"),
)

# ---------------------------------------------------------------- 6. PL · пенсионеры · легитимация в телефоне (не от имени госоргана, без орла и логотипов)
NAVY6, TEAL6, RED6 = (26, 38, 70), (20, 120, 160), (214, 48, 60)
PACKS[6] = dict(
    doc="PL-legitymacja-emeryta-mobywatel-2026-09-29", cta="Dowiedz się więcej",
    pal=dict(bg=(242, 247, 250), ink=NAVY6, sub=(84, 96, 110), acc=TEAL6, btn=RED6, tile=WH, tile_ink=NAVY6, icon=NAVY6,
             iconbg=(222, 238, 246)),
    a=dict(fn="grid", layout="2x2", title="Legitymacja emeryta w\u00a0telefonie:", title2="gdzie działa zniżka?", size=58,
           tiles=[("train", "Kolej: 37% na 2\u00a0przejazdy w\u00a0roku"), ("w5_museum", "Muzea, teatry i kina"), ("w5_pool", "Baseny"),
                  ("w5_senior_card", "Gminne karty seniora")],
           src="раздел «Gdzie działa zniżka dla emerytów i rencistów» (kolej 37% na 2 przejazdy, muzea/teatry/kina/baseny, gminne karty seniora)",
           note="2×2 мест со скидкой из статьи, у каждой «Dowiedz się więcej»; без орла, герба и логотипов"),
    b=dict(fn="quiz", layout="card2x2", title="Ulga 37% na kolej dla emerytów:", title2="ile przejazdów w\u00a0roku?", size=56,
           tag="QUIZ", step="Pytanie 1 z 3", prog=0.33,
           q="Na ile przejazdów pociągiem w\u00a0roku kalendarzowym przysługuje ustawowa ulga 37%?",
           opts=["1 przejazd", "2 przejazdy", "6 przejazdów", "Bez limitu"],
           pal=dict(bg=(255, 248, 230), bg2=(252, 232, 190), ink=NAVY6, sub=(96, 90, 70), acc=TEAL6, t2=RED6, btn=RED6, deco=True),
           src="раздел «Gdzie działa zniżka…» (Kolej: ustawowa zniżka 37% na dwa przejazdy w roku kalendarzowym)",
           note="кремовый фон, тест 2×2 о правиле скидки; «dla emerytów» — тема, не вопрос о зрителе"),
    c=dict(fn="compare", layout="twocol", title="Legitymacja papierowa czy w\u00a0telefonie?", sub="Co daje wersja cyfrowa w\u00a0aplikacji mObywatel",
           size=52, cols=[("PAPIEROWA", "w5_senior_card", (120, 106, 92)), ("W TELEFONIE", "phone", TEAL6)],
           rows=[("GDZIE", "w\u00a0portfelu", "w\u00a0aplikacji w\u00a0telefonie"),
                 ("NA CO DZIEŃ", "łatwo zgubić lub zniszczyć", "zawsze pod ręką"),
                 ("WARTO", "zachować jako zapas", "sprawdzić, czy kasa ją akceptuje")],
           foot="Dodanie legitymacji: kilka minut pracy",
           src="раздел «Czym jest cyfrowa legitymacja emeryta-rencisty» (те же данные, zawsze pod ręką, papierową zachować jako zapas) + «Gdzie działa zniżka…» (upewnić się, że kasa akceptuje) + итог (kilka minut)",
           note="две колонки бумажная vs в телефоне; mObywatel — только словом в подзаголовке как название приложения, без логотипа"),
    d=dict(fn="scene_d", scene="w5_pl_phone", style="top", y=40, size=54, lines=2,
           title="Legitymacja emeryta w\u00a0telefonie – jak ją dodać?", sub="Krok po kroku i gdzie pokazać ją przy zniżkach",
           btn_x=50, btn_left=True, btn_y=915, btn_size=40, pal=dict(ink=NAVY6, sub=(70, 84, 104), acc=TEAL6, btn=RED6),
           scene_text="шаги: 1 Pobierz aplikację / 2 Potwierdź tożsamość / 3 Dodaj legitymację; на экране: Dokumenty / LEGITYMACJA EMERYTA-RENCISTY",
           src="разделы «mObywatel – jak założyć aplikację krok po kroku» и «Jak dodać legitymację emeryta-rencisty» (3 шага)",
           note="рука с телефоном: нейтральный макет карточки без орла, флага и логотипов, серые строки вместо данных; слева 3 шага из статьи"),
)


# =====================================================================  сборка
def texts(t, cta):
    s = W4.texts(t, cta)
    extra = []
    if t.get("btn_lines"):
        extra.append("кнопки под плитками «" + " ".join(t["btn_lines"]) + "»")
    if t.get("hero_text"):
        extra.append("панель: " + t["hero_text"])
    if extra:
        s = s.replace(f" / кнопка «{cta} →»", "") + " / " + " / ".join(extra)
        if t["fn"] != "lt_grid":
            s += f" / кнопка «{cta} →»"
    return s


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
    os.makedirs(os.path.join(OUT5, doc), exist_ok=True)
    with open(os.path.join(OUT5, doc, "creatives.json"), "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    args = sys.argv[1:] or [str(k) for k in PACKS]
    for a in args:
        if a == "icons":
            icon_sheet()
        elif ":" in a:
            n, ls = a.split(":")
            build(int(n), ls.replace(",", ""))
        else:
            build(int(a))
