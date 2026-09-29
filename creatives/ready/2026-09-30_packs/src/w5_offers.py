"""Волна 5 «Готово к заливу» 30.09 (креативщик w5, офферы 60+): 5 пакетов × 4 статики 1:1, Pillow (ключ OpenAI истёк).
    python3 w5_offers.py            — все пакеты
    python3 w5_offers.py 2 4        — пакеты 2 и 4
    python3 w5_offers.py 3:a,c      — пакет 3, буквы a и c
    python3 w5_offers.py icons      — лист иконок w5 (в scratchpad, для проверки)
Пишет <OUT>/<docId>/<a|b|c|d>.png и <OUT>/<docId>/creatives.json.
Движок — p60_lib (холст C), иконки p60/w2b/w3/w4 (импорт w3_packs / w4_ukde / w4_us, их файлы не меняются),
шаблоны p60_templates. Здесь — свои иконки w5_*, раскладки и сцены. Текст на картинках — только то, что раскрывает
статья article_drafts/<docId> (раздел указан в note). Без сумм, процентов, «click here», локации зрителя, эмблем,
гербов, логотипов брендов и ведомств, до/после, утверждений о возрасте, здоровье, финансах или профессии зрителя."""
import json
import math
import os
import random
import sys

from PIL import Image, ImageDraw, ImageFilter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import w3_packs as W3  # noqa: E402,F401  (регистрирует иконки и сцены волн 1–3)
import w4_ukde as W4  # noqa: E402,F401  (иконки w4, людей и раскладки не меняем)
import w4_us as WU  # noqa: E402,F401
from p60_lib import C, W, OUT, mix, rotpts  # noqa: E402
import p60_icons as I  # noqa: E402
import p60_scenes as S  # noqa: E402
import p60_templates as T  # noqa: E402
import p60w2_art as A  # noqa: E402
import w2b_scenes as WS  # noqa: E402

WH = (255, 255, 255)
BLACK = (0, 0, 0)
SKIN = A.SKIN
CONCEPT = {"a": "сетка выбора (fake interactivity)", "b": "карточка-опросник", "c": "сколько стоит / сравнение",
           "d": "сцена-иллюстрация"}
PACKS = {}
SCRATCH = "/tmp/claude-0/-home-user-alextest/f5dce882-fce7-5270-9036-ca9a0fe43d5e/scratchpad/w5"


def icon(c, name, cx, cy, s, col, bg=WH, **kw):
    I.ICONS[name](c, cx, cy, s, col, bg=bg, **kw)


def subcanvas(c, box, ang, draw, paper=WH, shadow=60, r=0):
    """Отдельный лист (бумага, экран) размера box: draw(t, w, h) рисует в его координатах, лист поворачивается на ang°."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    t = C(paper, K=c.K)
    t.im = Image.new("RGBA", (c.s(w), c.s(h)), tuple(paper) + (255,))
    draw(t, w, h)
    im = t.im
    if r:
        m = Image.new("L", im.size, 0)
        ImageDraw.Draw(m).rounded_rectangle((0, 0, im.width - 1, im.height - 1), c.s(r), fill=255)
        im.putalpha(m)
    rot = im.rotate(-ang, expand=True, resample=Image.BICUBIC)
    X, Y = c.s((x0 + x1) / 2) - rot.width // 2, c.s((y0 + y1) / 2) - rot.height // 2
    if shadow:
        sh = Image.new("RGBA", rot.size, (0, 0, 0, 0))
        sh.putalpha(rot.getchannel("A").point(lambda v: v * shadow // 255))
        sh = sh.filter(ImageFilter.GaussianBlur(c.s(5)))
        c.im.paste(sh, (X + c.s(6), Y + c.s(10)), sh)
    c.im.paste(rot, (X, Y), rot)


def hdr(c, title, sub=None, y=46, col=(30, 30, 40), sub_col=(90, 96, 106), size=60, sub_size=32, lines=2, title2=None,
        t2_col=None, hl=None, maxw=980):
    return T.header(c, dict(title=title, sub=sub, title2=title2), y=y, col=col, sub_col=sub_col, size=size,
                    sub_size=sub_size, lines=lines, t2_col=t2_col, hl=hl, maxw=maxw)


def pill_w(c, label, size, padx):
    b = c.pill(label, 0, -900, size=size, padx=padx, pady=10)
    return b[2] - b[0]


def num_badge(c, cx, cy, r, n, fill, ink=WH):
    c.circle(cx, cy, r, fill=fill)
    c.text((cx, cy + 1), str(n), "db", r * 1.1, ink, anchor="mm")


def checkmark_circle(c, cx, cy, r, fill, ink=WH):
    c.circle(cx, cy, r, fill=fill)
    c.check(cx - r * 0.5, cy - r * 0.48, r * 1.0, ink, max(3, r * 0.22))


# =====================================================================  иконки w5 (квадрат s, центр cx, cy)
def w5_roundabout(c, cx, cy, s, col, bg=WH, isl=(70, 150, 90)):
    w = s * 0.18
    c.rect((cx - w / 2, cy - s * 0.5, cx + w / 2, cy + s * 0.5), fill=col)
    c.rect((cx - s * 0.5, cy - w / 2, cx + s * 0.5, cy + w / 2), fill=col)
    c.circle(cx, cy, s * 0.37, fill=col)
    c.circle(cx, cy, s * 0.17, fill=isl)
    c.circle(cx, cy, s * 0.17, outline=WH, width=s * 0.02)
    for ang in (35, 155, 275):
        a = math.radians(ang)
        r = s * 0.27
        px, py = cx + math.cos(a) * r, cy + math.sin(a) * r
        tx, ty = math.sin(a), -math.cos(a)  # против часовой (как на схеме)
        nx, ny = math.cos(a), math.sin(a)
        L, Wd = s * 0.075, s * 0.055
        c.poly([(px + tx * L, py + ty * L), (px - tx * L * 0.6 + nx * Wd, py - ty * L * 0.6 + ny * Wd),
                (px - tx * L * 0.6 - nx * Wd, py - ty * L * 0.6 - ny * Wd)], WH)


def w5_merge(c, cx, cy, s, col, bg=WH, acc=(240, 150, 30)):
    """Вид сверху: двухполосная дорога и съезд, вливающийся справа."""
    c.line([(cx + s * 0.44, cy + s * 0.5), (cx + s * 0.02, cy - s * 0.06)], mix(col, bg, 0.22), s * 0.2)
    c.rect((cx - s * 0.34, cy - s * 0.5, cx + s * 0.1, cy + s * 0.5), fill=col)
    for k in range(5):
        y0 = cy - s * 0.46 + k * s * 0.2
        c.rect((cx - s * 0.13, y0, cx - s * 0.1, y0 + s * 0.1), fill=WH)
    a = math.atan2(-(s * 0.56), -(s * 0.42))
    px, py = cx + s * 0.3, cy + s * 0.3
    tx, ty = math.cos(a), math.sin(a)
    nx, ny = -ty, tx
    c.line([(px - tx * s * 0.08, py - ty * s * 0.08), (px + tx * s * 0.06, py + ty * s * 0.06)], WH, s * 0.035)
    tip = (px + tx * s * 0.13, py + ty * s * 0.13)
    c.poly([tip, (px + tx * s * 0.04 + nx * s * 0.05, py + ty * s * 0.04 + ny * s * 0.05),
            (px + tx * s * 0.04 - nx * s * 0.05, py + ty * s * 0.04 - ny * s * 0.05)], WH)
    c.rect((cx - s * 0.03, cy - s * 0.36, cx + s * 0.07, cy - s * 0.18), fill=acc, r=s * 0.03)
    c.rect((cx - s * 0.28, cy + s * 0.02, cx - s * 0.18, cy + s * 0.2), fill=WH, r=s * 0.03)


def w5_glare(c, cx, cy, s, col, bg=WH, light=(255, 214, 90)):
    """Машина анфас ночью: фары, лучи, месяц."""
    for k in (-1, 1):
        hx = cx + k * s * 0.22
        c.poly([(hx, cy + s * 0.14), (hx + k * s * 0.3, cy + s * 0.5), (hx - k * s * 0.02, cy + s * 0.5)], mix(light, WH, 0.5), alpha=150)
    c.poly([(cx - s * 0.25, cy + s * 0.0), (cx - s * 0.17, cy - s * 0.2), (cx + s * 0.17, cy - s * 0.2), (cx + s * 0.25, cy + s * 0.0)], col)
    c.poly([(cx - s * 0.2, cy - s * 0.01), (cx - s * 0.14, cy - s * 0.16), (cx + s * 0.14, cy - s * 0.16), (cx + s * 0.2, cy - s * 0.01)], mix(col, bg, 0.6))
    c.rect((cx - s * 0.36, cy - s * 0.02, cx + s * 0.36, cy + s * 0.24), fill=col, r=s * 0.07)
    for k in (-1, 1):
        c.rect((cx + k * s * 0.28 - s * 0.05, cy + s * 0.2, cx + k * s * 0.28 + s * 0.05, cy + s * 0.32), fill=col, r=s * 0.02)
        c.circle(cx + k * s * 0.22, cy + s * 0.1, s * 0.065, fill=light)
    c.rect((cx - s * 0.08, cy + s * 0.08, cx + s * 0.08, cy + s * 0.13), fill=mix(col, bg, 0.5), r=s * 0.02)
    c.circle(cx + s * 0.3, cy - s * 0.36, s * 0.12, fill=light)
    c.circle(cx + s * 0.36, cy - s * 0.4, s * 0.1, fill=bg)


def w5_assist(c, cx, cy, s, col, bg=WH, acc=(240, 150, 30)):
    """Машина сверху, дуги датчиков слепых зон и камеры заднего вида."""
    for k in (-1, 1):
        for r in (0.12, 0.2):
            c.arc((cx + k * s * 0.2 - s * r, cy + s * 0.06 - s * r, cx + k * s * 0.2 + s * r, cy + s * 0.06 + s * r),
                  (-40 if k > 0 else 140), (40 if k > 0 else 220), acc, s * 0.035)
    for r in (0.1, 0.18):
        c.arc((cx - s * r, cy + s * 0.34 - s * r, cx + s * r, cy + s * 0.34 + s * r), 50, 130, acc, s * 0.035)
    c.rect((cx - s * 0.15, cy - s * 0.42, cx + s * 0.15, cy + s * 0.32), fill=col, r=s * 0.09)
    c.rect((cx - s * 0.11, cy - s * 0.26, cx + s * 0.11, cy - s * 0.12), fill=mix(col, bg, 0.6), r=s * 0.03)
    c.rect((cx - s * 0.11, cy + s * 0.14, cx + s * 0.11, cy + s * 0.24), fill=mix(col, bg, 0.6), r=s * 0.03)


def w5_cert(c, cx, cy, s, col, bg=WH, gold=(236, 176, 40), paper=WH):
    c.rect((cx - s * 0.4, cy - s * 0.3, cx + s * 0.4, cy + s * 0.3), fill=paper, outline=col, width=s * 0.04, r=s * 0.03)
    c.rect((cx - s * 0.33, cy - s * 0.23, cx + s * 0.33, cy + s * 0.23), outline=mix(col, paper, 0.5), width=s * 0.015)
    c.rect((cx - s * 0.22, cy - s * 0.15, cx + s * 0.22, cy - s * 0.1), fill=col, r=s * 0.02)
    for k in range(2):
        c.rect((cx - s * 0.25, cy - s * 0.03 + k * s * 0.08, cx + s * 0.1, cy + s * 0.0 + k * s * 0.08), fill=mix(col, paper, 0.55), r=s * 0.01)
    c.poly([(cx + s * 0.18, cy + s * 0.12), (cx + s * 0.14, cy + s * 0.38), (cx + s * 0.2, cy + s * 0.33), (cx + s * 0.25, cy + s * 0.4), (cx + s * 0.27, cy + s * 0.14)], mix(gold, BLACK, 0.2))
    c.circle(cx + s * 0.22, cy + s * 0.1, s * 0.1, fill=gold)
    c.circle(cx + s * 0.22, cy + s * 0.1, s * 0.06, outline=WH, width=s * 0.015)


def w5_forklift(c, cx, cy, s, col, bg=WH, body=(248, 186, 40), fork_up=0.0, load=False):
    """Погрузчик сбоку (смотрит вправо), без логотипов. col — тёмные детали."""
    gy = cy + s * 0.36  # уровень земли по центру колёс
    c.rect((cx + s * 0.22, cy - s * 0.46, cx + s * 0.27, gy + s * 0.02), fill=col, r=s * 0.01)
    c.rect((cx + s * 0.29, cy - s * 0.4, cx + s * 0.33, gy + s * 0.02), fill=mix(col, bg, 0.2), r=s * 0.01)
    fy = gy + s * 0.06 - fork_up * s
    c.rect((cx + s * 0.31, fy - s * 0.2, cx + s * 0.35, fy + s * 0.02), fill=col)
    c.rect((cx + s * 0.31, fy - s * 0.02, cx + s * 0.52, fy + s * 0.02), fill=col)
    if load:
        c.rect((cx + s * 0.34, fy - s * 0.06, cx + s * 0.52, fy - s * 0.02), fill=(170, 120, 70))
        c.rect((cx + s * 0.35, fy - s * 0.24, cx + s * 0.51, fy - s * 0.06), fill=(196, 150, 96))
        c.line([(cx + s * 0.43, fy - s * 0.24), (cx + s * 0.43, fy - s * 0.06)], (232, 206, 150), s * 0.012)
    c.line([(cx - s * 0.2, cy - s * 0.36), (cx + s * 0.18, cy - s * 0.36)], col, s * 0.035)
    c.line([(cx - s * 0.18, cy - s * 0.36), (cx - s * 0.22, cy - s * 0.02)], col, s * 0.03)
    c.line([(cx + s * 0.16, cy - s * 0.36), (cx + s * 0.2, cy + s * 0.02)], col, s * 0.03)
    c.poly([(cx - s * 0.44, cy + s * 0.0), (cx + s * 0.22, cy + s * 0.0), (cx + s * 0.22, gy - s * 0.02), (cx - s * 0.46, gy - s * 0.02)], body)
    c.rect((cx - s * 0.48, cy - s * 0.12, cx - s * 0.24, gy - s * 0.02), fill=mix(body, BLACK, 0.18), r=s * 0.04)
    c.rect((cx - s * 0.16, cy - s * 0.14, cx + s * 0.0, cy + s * 0.0), fill=mix(col, bg, 0.15), r=s * 0.03)
    c.rect((cx - s * 0.2, cy - s * 0.04, cx + s * 0.04, cy + s * 0.02), fill=mix(col, bg, 0.15), r=s * 0.02)
    for x, r in ((cx - s * 0.3, 0.13), (cx + s * 0.12, 0.12)):
        c.circle(x, gy, s * r, fill=col)
        c.circle(x, gy, s * r * 0.45, fill=mix(col, bg, 0.55))


def w5_truck(c, cx, cy, s, col, bg=WH, acc=(40, 140, 200)):
    c.rect((cx - s * 0.48, cy - s * 0.3, cx + s * 0.12, cy + s * 0.18), fill=mix(col, bg, 0.15), r=s * 0.03)
    c.poly([(cx + s * 0.15, cy - s * 0.16), (cx + s * 0.34, cy - s * 0.16), (cx + s * 0.48, cy + s * 0.02), (cx + s * 0.48, cy + s * 0.18), (cx + s * 0.15, cy + s * 0.18)], acc)
    c.poly([(cx + s * 0.2, cy - s * 0.11), (cx + s * 0.32, cy - s * 0.11), (cx + s * 0.42, cy + s * 0.01), (cx + s * 0.2, cy + s * 0.01)], mix(acc, WH, 0.65))
    c.rect((cx - s * 0.48, cy + s * 0.15, cx + s * 0.48, cy + s * 0.22), fill=col)
    for x in (cx - s * 0.34, cx - s * 0.16, cx + s * 0.34):
        c.circle(x, cy + s * 0.26, s * 0.09, fill=col)
        c.circle(x, cy + s * 0.26, s * 0.035, fill=bg)


def w5_server(c, cx, cy, s, col, bg=WH, led=(60, 200, 110)):
    for k in range(3):
        y0 = cy - s * 0.4 + k * s * 0.27
        c.rect((cx - s * 0.34, y0, cx + s * 0.34, y0 + s * 0.22), fill=col, r=s * 0.04)
        c.circle(cx - s * 0.22, y0 + s * 0.11, s * 0.035, fill=led)
        c.circle(cx - s * 0.12, y0 + s * 0.11, s * 0.035, fill=(250, 190, 50) if k == 1 else led)
        for j in range(3):
            c.rect((cx + s * 0.0 + j * s * 0.09, y0 + s * 0.06, cx + s * 0.05 + j * s * 0.09, y0 + s * 0.16), fill=mix(col, bg, 0.5), r=s * 0.01)


def w5_code(c, cx, cy, s, col, bg=WH, acc=(60, 200, 150)):
    c.rect((cx - s * 0.38, cy - s * 0.34, cx + s * 0.38, cy + s * 0.18), fill=col, r=s * 0.05)
    c.rect((cx - s * 0.32, cy - s * 0.28, cx + s * 0.32, cy + s * 0.12), fill=(28, 34, 44), r=s * 0.02)
    c.poly([(cx - s * 0.48, cy + s * 0.22), (cx + s * 0.48, cy + s * 0.22), (cx + s * 0.42, cy + s * 0.3), (cx - s * 0.42, cy + s * 0.3)], col)
    c.line([(cx - s * 0.1, cy - s * 0.18), (cx - s * 0.2, cy - s * 0.08), (cx - s * 0.1, cy + s * 0.02)], acc, s * 0.035)
    c.line([(cx + s * 0.1, cy - s * 0.18), (cx + s * 0.2, cy - s * 0.08), (cx + s * 0.1, cy + s * 0.02)], acc, s * 0.035)
    c.line([(cx + s * 0.04, cy - s * 0.2), (cx - s * 0.04, cy + s * 0.04)], WH, s * 0.03)


def w5_breakers(c, cx, cy, s, col, bg=WH, acc=(232, 88, 60)):
    """Щиток с автоматами (disjuntor): один выключен."""
    c.rect((cx - s * 0.42, cy - s * 0.36, cx + s * 0.42, cy + s * 0.36), fill=col, r=s * 0.06)
    c.rect((cx - s * 0.36, cy - s * 0.1, cx + s * 0.36, cy + s * 0.2), fill=mix(col, bg, 0.8), r=s * 0.02)
    for k in range(4):
        x = cx - s * 0.27 + k * s * 0.18
        c.rect((x - s * 0.06, cy - s * 0.07, x + s * 0.06, cy + s * 0.17), fill=WH, r=s * 0.02)
        down = k == 2
        c.rect((x - s * 0.03, cy + (s * 0.05 if down else -s * 0.04), x + s * 0.03, cy + (s * 0.14 if down else s * 0.04)), fill=acc if down else col, r=s * 0.01)
    c.rect((cx - s * 0.3, cy - s * 0.28, cx + s * 0.05, cy - s * 0.2), fill=mix(col, bg, 0.6), r=s * 0.02)


def w5_daynight(c, cx, cy, s, col, bg=WH, day=(250, 196, 60), night=(40, 60, 120)):
    """Циферблат: половина — день (солнце), половина — ночь (месяц)."""
    c.circle(cx, cy, s * 0.44, fill=col)
    c.pie((cx - s * 0.38, cy - s * 0.38, cx + s * 0.38, cy + s * 0.38), 270, 450, mix(day, WH, 0.55))
    c.pie((cx - s * 0.38, cy - s * 0.38, cx + s * 0.38, cy + s * 0.38), 90, 270, mix(night, WH, 0.25))
    c.circle(cx + s * 0.18, cy - s * 0.02, s * 0.08, fill=day)
    c.circle(cx - s * 0.18, cy - s * 0.02, s * 0.08, fill=(250, 240, 200))
    c.circle(cx - s * 0.14, cy - s * 0.05, s * 0.07, fill=mix(night, WH, 0.25))
    c.line([(cx, cy), (cx, cy - s * 0.28)], col, s * 0.04)
    c.line([(cx, cy), (cx + s * 0.12, cy + s * 0.18)], col, s * 0.04)
    c.circle(cx, cy, s * 0.04, fill=col)


def w5_meter_q(c, cx, cy, s, col, bg=WH, acc=(236, 140, 40)):
    """Счётчик с цифрами и знаком «?» — расчётные показания."""
    c.rect((cx - s * 0.32, cy - s * 0.42, cx + s * 0.28, cy + s * 0.42), fill=col, r=s * 0.06)
    c.rect((cx - s * 0.25, cy - s * 0.32, cx + s * 0.21, cy - s * 0.12), fill=(206, 232, 214), r=s * 0.02)
    for k in range(5):
        x = cx - s * 0.21 + k * s * 0.085
        c.rect((x, cy - s * 0.28, x + s * 0.06, cy - s * 0.16), fill=(60, 80, 70), r=s * 0.01)
    c.circle(cx - s * 0.02, cy + s * 0.14, s * 0.13, fill=mix(col, bg, 0.75))
    c.line([(cx - s * 0.02, cy + s * 0.14), (cx + s * 0.06, cy + s * 0.07)], col, s * 0.03)
    c.circle(cx + s * 0.3, cy + s * 0.28, s * 0.17, fill=acc, outline=bg, width=s * 0.04)
    c.text((cx + s * 0.3, cy + s * 0.29), "?", "db", s * 0.24, WH, anchor="mm")


def w5_doc_plus(c, cx, cy, s, col, bg=WH, acc=(236, 140, 40), paper=WH):
    """Лист с лишними строками и значком «+» — доп. услуги."""
    c.poly([(cx - s * 0.32, cy - s * 0.42), (cx + s * 0.14, cy - s * 0.42), (cx + s * 0.3, cy - s * 0.26), (cx + s * 0.3, cy + s * 0.42), (cx - s * 0.32, cy + s * 0.42)], col)
    c.poly([(cx - s * 0.26, cy - s * 0.36), (cx + s * 0.11, cy - s * 0.36), (cx + s * 0.24, cy - s * 0.23), (cx + s * 0.24, cy + s * 0.36), (cx - s * 0.26, cy + s * 0.36)], paper)
    for k in range(5):
        y = cy - s * 0.2 + k * s * 0.1
        c.rect((cx - s * 0.18, y, cx + (s * 0.16 if k % 2 == 0 else s * 0.04), y + s * 0.04), fill=mix(col, paper, 0.4 if k < 3 else 0.7), r=s * 0.01)
    c.circle(cx + s * 0.26, cy + s * 0.28, s * 0.17, fill=acc, outline=bg, width=s * 0.04)
    c.rect((cx + s * 0.26 - s * 0.09, cy + s * 0.28 - s * 0.025, cx + s * 0.26 + s * 0.09, cy + s * 0.28 + s * 0.025), fill=WH)
    c.rect((cx + s * 0.26 - s * 0.025, cy + s * 0.28 - s * 0.09, cx + s * 0.26 + s * 0.025, cy + s * 0.28 + s * 0.09), fill=WH)


def w5_cal_x(c, cx, cy, s, col, bg=WH, acc=(222, 70, 50)):
    """Календарь с отметкой окончания — истёкшее предложение."""
    I.ICONS["calendar"](c, cx - s * 0.06, cy - s * 0.02, s * 0.9, col, bg=bg)
    c.circle(cx + s * 0.28, cy + s * 0.28, s * 0.18, fill=acc, outline=bg, width=s * 0.04)
    c.rect((cx + s * 0.27, cy + s * 0.17, cx + s * 0.29, cy + s * 0.29), fill=WH)
    c.line([(cx + s * 0.28, cy + s * 0.28), (cx + s * 0.36, cy + s * 0.32)], WH, s * 0.03)
    c.line([(cx + s * 0.28, cy + s * 0.18), (cx + s * 0.28, cy + s * 0.29)], WH, s * 0.03)


def w5_gauge(c, cx, cy, s, col, bg=WH, acc=(222, 70, 50), label="kW"):
    c.pie((cx - s * 0.46, cy - s * 0.38, cx + s * 0.46, cy + s * 0.54), 180, 360, col)
    c.pie((cx - s * 0.34, cy - s * 0.26, cx + s * 0.34, cy + s * 0.42), 180, 360, bg)
    for k, colr in enumerate(((70, 170, 100), (250, 190, 50), acc)):
        c.arc((cx - s * 0.42, cy - s * 0.34, cx + s * 0.42, cy + s * 0.5), 180 + k * 60, 240 + k * 60, colr, s * 0.07)
    a = math.radians(-35)
    c.line([(cx, cy + s * 0.08), (cx + math.cos(a) * s * 0.3, cy + s * 0.08 + math.sin(a) * s * 0.3)], col, s * 0.045)
    c.circle(cx, cy + s * 0.08, s * 0.06, fill=col)
    c.text((cx, cy + s * 0.3), label, "db", s * 0.2, col, anchor="mm")


def w5_fasce(c, cx, cy, s, col, bg=WH, cols=((232, 110, 60), (250, 190, 60), (70, 160, 110))):
    """Циферблат, поделённый на три цветные зоны (фасце)."""
    c.circle(cx, cy, s * 0.45, fill=col)
    box = (cx - s * 0.39, cy - s * 0.39, cx + s * 0.39, cy + s * 0.39)
    c.pie(box, 240, 360 + 30, mix(cols[0], WH, 0.2))
    c.pie(box, 30, 130, mix(cols[1], WH, 0.2))
    c.pie(box, 130, 240, mix(cols[2], WH, 0.2))
    c.circle(cx, cy, s * 0.2, fill=WH)
    c.line([(cx, cy), (cx, cy - s * 0.16)], col, s * 0.04)
    c.line([(cx, cy), (cx + s * 0.12, cy + s * 0.05)], col, s * 0.04)
    c.circle(cx, cy, s * 0.035, fill=col)


def w5_shop(c, cx, cy, s, col, bg=WH, awn=(222, 70, 60)):
    """Магазин без вывески и логотипа."""
    c.rect((cx - s * 0.4, cy - s * 0.12, cx + s * 0.4, cy + s * 0.42), fill=col, r=s * 0.02)
    for k in range(5):
        x0 = cx - s * 0.46 + k * s * 0.184
        c.pie((x0, cy - s * 0.3, x0 + s * 0.184, cy - s * 0.06), 0, 180, awn if k % 2 == 0 else WH)
        c.rect((x0, cy - s * 0.4, x0 + s * 0.184, cy - s * 0.18), fill=awn if k % 2 == 0 else WH)
    c.rect((cx - s * 0.46, cy - s * 0.44, cx + s * 0.46, cy - s * 0.38), fill=mix(awn, BLACK, 0.2), r=s * 0.02)
    c.rect((cx - s * 0.32, cy + s * 0.0, cx + s * 0.02, cy + s * 0.24), fill=mix(col, bg, 0.75), r=s * 0.02)
    c.rect((cx - s * 0.26, cy + s * 0.12, cx - s * 0.1, cy + s * 0.24), fill=col, r=s * 0.02)
    c.rect((cx + s * 0.1, cy + s * 0.0, cx + s * 0.3, cy + s * 0.42), fill=mix(col, bg, 0.6), r=s * 0.02)
    c.circle(cx + s * 0.14, cy + s * 0.22, s * 0.02, fill=col)


def w5_tower_phone(c, cx, cy, s, col, bg=WH, acc=(40, 140, 220)):
    """Мачта связи + телефон (оператор)."""
    c.poly([(cx - s * 0.2, cy + s * 0.44), (cx - s * 0.06, cy - s * 0.24), (cx + s * 0.0, cy - s * 0.24), (cx - s * 0.1, cy + s * 0.44)], col)
    c.poly([(cx + s * 0.04, cy + s * 0.44), (cx - s * 0.02, cy - s * 0.24), (cx + s * 0.04, cy - s * 0.24), (cx + s * 0.14, cy + s * 0.44)], col)
    c.line([(cx - s * 0.13, cy + s * 0.14), (cx + s * 0.08, cy + s * 0.14)], col, s * 0.03)
    c.circle(cx - s * 0.03, cy - s * 0.28, s * 0.05, fill=col)
    for r in (0.13, 0.22):
        c.arc((cx - s * 0.03 - s * r, cy - s * 0.28 - s * r, cx - s * 0.03 + s * r, cy - s * 0.28 + s * r), 200, 250, acc, s * 0.035)
        c.arc((cx - s * 0.03 - s * r, cy - s * 0.28 - s * r, cx - s * 0.03 + s * r, cy - s * 0.28 + s * r), 290, 340, acc, s * 0.035)
    c.rect((cx + s * 0.18, cy - s * 0.06, cx + s * 0.44, cy + s * 0.44), fill=col, r=s * 0.05)
    c.rect((cx + s * 0.21, cy - s * 0.01, cx + s * 0.41, cy + s * 0.36), fill=mix(acc, WH, 0.6), r=s * 0.02)


def w5_online_loan(c, cx, cy, s, col, bg=WH, gold=(236, 180, 50), acc=(40, 160, 100)):
    """Ноутбук и стрелка перевода на счёт (кредит наличными онлайн)."""
    c.rect((cx - s * 0.4, cy - s * 0.3, cx + s * 0.3, cy + s * 0.16), fill=col, r=s * 0.04)
    c.rect((cx - s * 0.34, cy - s * 0.24, cx + s * 0.24, cy + s * 0.1), fill=mix(col, bg, 0.8), r=s * 0.02)
    c.poly([(cx - s * 0.48, cy + s * 0.2), (cx + s * 0.38, cy + s * 0.2), (cx + s * 0.32, cy + s * 0.27), (cx - s * 0.42, cy + s * 0.27)], col)
    c.line([(cx - s * 0.24, cy - s * 0.04), (cx + s * 0.08, cy - s * 0.04)], acc, s * 0.05)
    c.poly([(cx + s * 0.14, cy - s * 0.04), (cx + s * 0.04, cy - s * 0.12), (cx + s * 0.04, cy + s * 0.04)], acc)
    c.circle(cx + s * 0.32, cy + s * 0.3, s * 0.16, fill=gold, outline=bg, width=s * 0.035)
    c.circle(cx + s * 0.32, cy + s * 0.3, s * 0.08, outline=mix(gold, BLACK, 0.3), width=s * 0.02)


W5_ICONS = {k: v for k, v in dict(globals()).items() if k.startswith("w5_") and callable(v)}
I.ICONS.update(W5_ICONS)


def icon_sheet():
    names = sorted(W5_ICONS)
    c = C(WH)
    for i, n in enumerate(names):
        x = (i % 5) * 216 + 108
        y = (i // 5) * 216 + 96
        c.circle(x, y, 74, fill=(236, 240, 246))
        icon(c, n, x, y, 110, (30, 40, 70), bg=(236, 240, 246))
        c.text((x, y + 92), n, "s", 20, BLACK, anchor="mm")
    img = c.im.convert("RGB").resize((W, W), Image.LANCZOS)
    os.makedirs(SCRATCH, exist_ok=True)
    img.save(os.path.join(SCRATCH, "w5_icons.png"))
    print("icons ->", os.path.join(SCRATCH, "w5_icons.png"))


# =====================================================================  1. US · обучение 60+ · курсы вождения (refresher)
NAVY1, BLUE1, AMB1, ORG1 = (20, 36, 74), (28, 110, 190), (242, 164, 32), (232, 96, 28)


def us_grid(P, t):
    """2×2 плитки тем курса: цветная панель с крупной иконкой, подпись, пояснение из статьи, «Learn more»."""
    p = P["pal"]
    c = C(p["bg"])
    c.vgrad((0, 0, W, W), p["bg"], p["bg2"])
    y = hdr(c, t["title"], t.get("sub"), y=44, col=NAVY1, sub_col=(70, 84, 104), size=58, sub_size=32)
    top = y + 26
    g = 24
    tw = (960 - g) / 2
    th = (1046 - top - g) / 2
    for i, (ic, lab, desc, c0, c1, icol) in enumerate(t["tiles"]):
        x0 = 60 + (i % 2) * (tw + g)
        y0 = top + (i // 2) * (th + g)
        box = (x0, y0, x0 + tw, y0 + th)
        c.card(box, fill=WH, r=28, sh_alpha=60, blur=14, off=(0, 8))
        ph = th * 0.46
        c.rect((x0, y0, x0 + tw, y0 + ph), fill=c0, r=28)
        c.rect((x0, y0 + ph - 30, x0 + tw, y0 + ph), fill=c0)
        c.vgrad((x0 + 1, y0 + 28, x0 + tw - 1, y0 + ph), c0, c1)
        icon(c, ic, x0 + tw / 2, y0 + ph / 2 + 4, ph * 0.86, icol, bg=c1)
        num_badge(c, x0 + 40, y0 + 40, 22, i + 1, ORG1)
        ly = y0 + ph + 16
        ly = c.block(lab, "db", c.fit(lab, "db", tw - 40, 1, 36), ly, tw - 40, NAVY1, cx=x0 + tw / 2, max_lines=1)
        c.block(desc, "s", 26, ly + 2, tw - 40, (90, 100, 116), cx=x0 + tw / 2, max_lines=1)
        c.pill(P["cta"], x0 + tw / 2, y0 + th - 40, size=24, fill=p["btn"], padx=26, pady=11)
    return c


def us_checklist(P, t):
    """Слева заголовок и кнопка, справа телефон с чек-листом «4 вопроса страховщику» (1 из 4 отмечен)."""
    p = P["pal"]
    c = C(p["bg"])
    c.vgrad((0, 0, W, W), p["bg"], p["bg2"])
    c.ellipse((-160, 760, 300, 1220), fill=WH, alpha=40)
    lx = 60
    y = 250
    y = c.block(t["title"], "db", 58, y, 450, NAVY1, align="left", x=lx, max_lines=3, gap=1.08)
    y = c.block(t["title2"], "db", 52, y + 6, 450, ORG1, align="left", x=lx, max_lines=3, gap=1.08)
    y = c.block(t["sub"], "s", 32, y + 22, 440, (80, 76, 70), align="left", x=lx, max_lines=3, gap=1.14)
    bb = c.button(P["cta"], 0, -700, size=40, fill=p["btn"])
    c.button(P["cta"], lx + (bb[2] - bb[0]) / 2, y + 90, size=40, fill=p["btn"])
    ph = (552, 50, 1030, 1030)
    c.shadow(ph, r=66, alpha=120, blur=26, off=(0, 16))
    c.rect(ph, fill=(26, 28, 34), r=66)
    sc = (ph[0] + 16, ph[1] + 16, ph[2] - 16, ph[3] - 16)
    c.rect(sc, fill=(248, 249, 251), r=52)
    c.rect(((ph[0] + ph[2]) / 2 - 70, ph[1] + 28, (ph[0] + ph[2]) / 2 + 70, ph[1] + 60), fill=(26, 28, 34), r=16)
    c.text((sc[0] + 40, ph[1] + 44), "9:41", "sb", 22, (40, 40, 40), anchor="lm")
    x0, x1 = sc[0] + 32, sc[2] - 32
    yy = sc[1] + 88
    tag = t["tag"]
    tw_ = c.tw(tag, c.font("sb", 22))[0]
    c.rect((x0, yy, x0 + tw_ + 30, yy + 40), fill=mix(BLUE1, WH, 0.86), r=20)
    c.text((x0 + 15, yy + 20), tag, "sb", 22, BLUE1, anchor="lm")
    yy += 62
    yy = c.block(t["q"], "db", 28, yy, x1 - x0, (30, 34, 44), align="left", x=x0, max_lines=2, gap=1.1)
    yy += 14
    c.text((x0, yy), t["step"], "s", 23, (110, 116, 124))
    c.rect((x0, yy + 36, x1, yy + 46), fill=(224, 228, 234), r=5)
    c.rect((x0, yy + 36, x0 + (x1 - x0) * 0.25, yy + 46), fill=(40, 160, 90), r=5)
    yy += 70
    n = len(t["items"])
    gap = 14
    rh = (sc[3] - 40 - yy - (n - 1) * gap) / n
    for k, it in enumerate(t["items"]):
        rb = (x0, yy, x1, yy + rh)
        done = k == 0
        c.rect(rb, fill=WH if not done else (234, 246, 238), r=20, outline=(40, 160, 90) if done else (212, 218, 226), width=3)
        bx = x0 + 22
        if done:
            c.rect((bx, yy + rh / 2 - 20, bx + 40, yy + rh / 2 + 20), fill=(40, 160, 90), r=8)
            c.check(bx + 8, yy + rh / 2 - 12, 24, WH, 5)
        else:
            c.rect((bx, yy + rh / 2 - 20, bx + 40, yy + rh / 2 + 20), fill=WH, r=8, outline=(160, 168, 180), width=3)
        tx = bx + 60
        sz = 28
        nl = len(c.wrap(it, c.font("sb", sz), x1 - tx - 18))
        c.block(it, "sb", sz, yy + rh / 2 - nl * c.lh("sb", sz, 1.06) / 2 + 2, x1 - tx - 18, (40, 44, 56), align="left", x=tx,
                max_lines=2, gap=1.06)
        yy += rh + gap
    return c


def laptop_modules(c, box, rows, acc=BLUE1):
    """Иллюстрация: ноутбук с модулями курса и финальным тестом."""
    x0, y0, x1, y1 = box
    cx = (x0 + x1) / 2
    lw, lh = (x1 - x0) * 0.78, (y1 - y0) * 0.66
    sx0, sy0 = cx - lw / 2, y0 + (y1 - y0) * 0.1
    c.rect((sx0, sy0, sx0 + lw, sy0 + lh), fill=(36, 40, 52), r=14)
    scr = (sx0 + 12, sy0 + 12, sx0 + lw - 12, sy0 + lh - 10)
    c.rect(scr, fill=WH, r=6)
    c.poly([(sx0 - 30, sy0 + lh + 4), (sx0 + lw + 30, sy0 + lh + 4), (sx0 + lw + 10, sy0 + lh + 24), (sx0 - 10, sy0 + lh + 24)], (70, 76, 90))
    c.rect((cx - 40, sy0 + lh + 4, cx + 40, sy0 + lh + 10), fill=(50, 54, 66), r=3)
    n = len(rows)
    rh = (scr[3] - scr[1] - 16) / n
    for k, (lab, st) in enumerate(rows):
        ry = scr[1] + 8 + k * rh
        fill = (234, 246, 238) if st == "done" else ((226, 238, 252) if st == "now" else (244, 245, 248))
        c.rect((scr[0] + 10, ry + 3, scr[2] - 10, ry + rh - 3), fill=fill, r=6)
        if st == "done":
            checkmark_circle(c, scr[0] + 32, ry + rh / 2, 12, (40, 160, 90))
        elif st == "now":
            c.circle(scr[0] + 32, ry + rh / 2, 12, fill=acc)
        else:
            c.circle(scr[0] + 32, ry + rh / 2, 11, outline=(170, 176, 186), width=3)
        c.text((scr[0] + 54, ry + rh / 2), lab, "sb", min(24, rh * 0.5), (40, 44, 56), anchor="lm")


def classroom_mini(c, box):
    """Иллюстрация: доска со схемой кольца, инструктор, группа (со спины)."""
    x0, y0, x1, y1 = box
    bw = (x1 - x0) * 0.62
    bx0 = x0 + (x1 - x0) * 0.08
    by0, by1 = y0 + 18, y0 + (y1 - y0) * 0.58
    c.rect((bx0 - 8, by0 - 8, bx0 + bw + 8, by1 + 8), fill=(150, 110, 70), r=8)
    c.rect((bx0, by0, bx0 + bw, by1), fill=(46, 92, 72), r=4)
    bcx, bcy = bx0 + bw / 2, (by0 + by1) / 2
    r = (by1 - by0) * 0.3
    c.circle(bcx, bcy, r, outline=WH, width=5)
    for a in (0, 90, 180, 270):
        ax, ay = bcx + math.cos(math.radians(a)) * r, bcy + math.sin(math.radians(a)) * r
        ex, ey = bcx + math.cos(math.radians(a)) * r * 1.7, bcy + math.sin(math.radians(a)) * r * 1.7
        c.line([(ax, ay), (ex, ey)], WH, 5)
    c.poly([(bcx + r * 0.72, bcy - r * 0.9), (bcx + r * 1.0, bcy - r * 0.62), (bcx + r * 0.6, bcy - r * 0.55)], (250, 210, 80))
    A.standing(c, x1 - (x1 - x0) * 0.16, y1 - 6, (y1 - y0) * 0.86, SKIN[1], (50, 40, 36), "short", (40, 110, 170), (50, 56, 70),
               arm_l=(bx0 + bw + 6, by0 + (by1 - by0) * 0.45))
    for k, (hx, hair, coat) in enumerate(((0.16, (90, 60, 40), (200, 90, 60)), (0.38, (210, 210, 214), (70, 130, 110)),
                                          (0.6, (40, 34, 30), (230, 170, 60)))):
        cx = x0 + (x1 - x0) * hx
        c.rect((cx - 50, y1 - 60, cx + 50, y1 + 30), fill=coat, r=36)
        c.circle(cx, y1 - 82, 30, fill=hair)


def us_formats(P, t):
    """Сравнение: онлайн-курс vs класс — иллюстрации, 2 строки на формат, общая плашка 4–8 часов, строка о премии."""
    p = P["pal"]
    c = C(p["bg"])
    c.vgrad((0, 0, W, W), p["bg"], p["bg2"])
    y = hdr(c, t["title"], None, y=40, col=NAVY1, size=58, title2=t["title2"], t2_col=BLUE1)
    top, bot = y + 24, 702
    g = 28
    cw = (960 - g) / 2
    for k, (lab, l1, l2, col, tint) in enumerate(t["cols"]):
        x0 = 60 + k * (cw + g)
        box = (x0, top, x0 + cw, bot)
        c.card(box, fill=WH, r=28, sh_alpha=60, blur=14, off=(0, 8))
        il = (x0 + 14, top + 14, x0 + cw - 14, top + 14 + (bot - top) * 0.6)
        if k == 0:
            subcanvas(c, il, 0, lambda tt, w, h: laptop_modules(tt, (0, 40, w, h - 4), t["modules"]), paper=tint, shadow=0, r=20)
        else:
            subcanvas(c, il, 0, lambda tt, w, h: classroom_mini(tt, (10, 48, w - 10, h)), paper=tint, shadow=0, r=20)
        pw = c.tw(lab, c.font("db", 24))[0] + 36
        c.rect((il[0] + 16, il[1] + 14, il[0] + 16 + pw, il[1] + 56), fill=col, r=21)
        c.text((il[0] + 16 + pw / 2, il[1] + 35), lab, "db", 24, WH, anchor="mm")
        ty = il[3] + 22
        ty = c.block(l1, "db", c.fit(l1, "db", cw - 50, 1, 34), ty, cw - 50, NAVY1, cx=x0 + cw / 2, max_lines=1)
        c.block(l2, "s", 28, ty + 6, cw - 50, (80, 90, 106), cx=x0 + cw / 2, max_lines=2, gap=1.1)
    c.circle(W / 2, top + (bot - top) * 0.3, 40, fill=WH, outline=(200, 206, 214), width=3)
    c.text((W / 2, top + (bot - top) * 0.3), "vs", "db", 28, (90, 96, 106), anchor="mm")
    band = (60, 726, 1020, 814)
    c.card(band, fill=NAVY1, r=26, sh_alpha=50, blur=10, off=(0, 6))
    (i1, s1), (i2, s2) = t["band"]
    half = (band[2] - band[0]) / 2
    for k, (ic, s_) in enumerate(((i1, s1), (i2, s2))):
        bx = band[0] + k * half
        icon(c, ic, bx + 56, (band[1] + band[3]) / 2, 60, WH, bg=NAVY1)
        c.block(s_, "sb", c.fit(s_, "sb", half - 110, 1, 32), (band[1] + band[3]) / 2 - 20, half - 110, WH, align="left", x=bx + 100, max_lines=1)
    c.line([(W / 2, band[1] + 18), (W / 2, band[3] - 18)], (70, 90, 130), 3)
    c.block(t["foot"], "sb", 31, 842, 980, (50, 60, 80), max_lines=1)
    c.button(P["cta"], W / 2, 966, size=42, fill=p["btn"])
    return c


def yield_sign_roundabout(c, cx, cy, s):
    """Жёлтый ромб с тремя стрелками по кругу (типовой знак «кольцо впереди», без эмблем)."""
    c.poly([(cx, cy - s), (cx + s, cy), (cx, cy + s), (cx - s, cy)], (250, 200, 40))
    c.poly([(cx, cy - s * 0.9), (cx + s * 0.9, cy), (cx, cy + s * 0.9), (cx - s * 0.9, cy)], (250, 200, 40), outline=(30, 30, 30), width=3)
    r = s * 0.38
    for a0 in (20, 140, 260):
        c.arc((cx - r, cy - r, cx + r, cy + r), a0, a0 + 80, (30, 30, 30), s * 0.1)
        a = math.radians(a0)
        px, py = cx + math.cos(a) * r, cy + math.sin(a) * r
        tx, ty = math.sin(a), -math.cos(a)
        nx, ny = math.cos(a), math.sin(a)
        c.poly([(px + tx * s * 0.16, py + ty * s * 0.16), (px + nx * s * 0.12, py + ny * s * 0.12), (px - nx * s * 0.12, py - ny * s * 0.12)], (30, 30, 30))


def sc_us_car(c):
    """Салон машины в сумерках: дорога, знак кольца, навигатор, руль, на пассажирском сиденье — сертификат курса."""
    c.vgrad((0, 0, W, 400), (14, 24, 58), (74, 62, 122))
    c.vgrad((0, 400, W, 560), (74, 62, 122), (238, 138, 80))
    c.glow((360, 470, 760, 640), (255, 176, 96), alpha=170, blur=50)
    rnd = random.Random(7)
    for _ in range(14):
        c.circle(rnd.choice((rnd.uniform(20, 90), rnd.uniform(990, 1060))), rnd.uniform(20, 380), rnd.uniform(1.2, 2.6), fill=WH, alpha=150)
    c.poly([(0, 540), (140, 500), (300, 520), (430, 494), (560, 522), (700, 498), (860, 516), (1080, 490), (1080, 560), (0, 560)], (52, 46, 84))
    c.rect((0, 548, W, W), fill=(34, 38, 52))
    vx, vy = 566, 548
    c.poly([(vx - 40, vy), (vx + 40, vy), (1240, 1080), (-120, 1080)], (66, 70, 84))
    for side in (-1, 1):
        c.line([(vx + side * 36, vy + 2), (560 + side * 700, 1080)], (220, 220, 226), 4, alpha=200)
    for k in range(7):
        f0, f1 = (k / 7) ** 1.6, ((k + 0.45) / 7) ** 1.6
        ya, yb = vy + f0 * 540, vy + f1 * 540
        xa, xb = vx + (560 - vx) * f0 - 6, vx + (560 - vx) * f1 - 6
        c.line([(xa, ya), (xb, yb)], (250, 214, 90), 2 + 10 * f1)
    c.glow((574, 540, 610, 560), (255, 250, 220), alpha=240, blur=8)
    c.circle(584, 551, 3.5, fill=WH)
    c.circle(598, 551, 3.5, fill=WH)
    c.line([(860, 470), (860, 640)], (120, 124, 134), 8)
    yield_sign_roundabout(c, 860, 450, 50)
    dark = (22, 24, 30)
    c.poly([(0, 380), (70, 380), (210, 720), (0, 760)], dark)
    c.poly([(W, 380), (W - 70, 380), (W - 210, 720), (W, 760)], dark)
    c.poly([(0, 704), (240, 674), (840, 674), (W, 704), (W, W), (0, W)], (36, 38, 46))
    c.line([(0, 704), (240, 674), (840, 674), (W, 704)], (70, 72, 84), 4)
    c.pie((160, 706, 440, 880), 180, 360, (24, 26, 32))
    for gx in (252, 348):
        c.circle(gx, 796, 42, fill=(16, 18, 24))
        c.arc((gx - 36, 760, gx + 36, 832), 140, 400, (80, 170, 255), 5)
        c.line([(gx, 796), (gx + 22, 776)], (255, 120, 60), 4)
    # навигатор
    c.rect((528, 724, 800, 886), fill=(14, 14, 18), r=18)
    scr = (540, 736, 788, 874)
    c.rect(scr, fill=(34, 46, 70), r=10)
    for xx, yy_, x2, y2 in ((560, 860, 700, 750), (600, 740, 780, 800), (540, 790, 790, 830)):
        c.line([(xx, yy_), (x2, y2)], (70, 88, 120), 8)
    c.line([(600, 866), (640, 820), (680, 800)], (70, 170, 255), 9)
    c.circle(700, 790, 22, outline=(70, 170, 255), width=8)
    c.line([(716, 774), (760, 744)], (70, 170, 255), 9)
    c.poly([(600, 846), (614, 872), (586, 872)], WH)
    for vxs in (470, 820):
        c.rect((vxs, 744, vxs + 44, 800), fill=(24, 26, 32), r=8)
        for k in range(3):
            c.line([(vxs + 6, 758 + k * 14), (vxs + 38, 758 + k * 14)], (60, 62, 72), 3)
    # руль
    c.circle(300, 952, 196, outline=(14, 14, 18), width=36)
    c.line([(120, 952), (240, 952)], (14, 14, 18), 30)
    c.line([(360, 952), (480, 952)], (14, 14, 18), 30)
    c.line([(300, 1000), (300, 1080)], (14, 14, 18), 34)
    c.circle(300, 962, 62, fill=(26, 26, 32))
    # пассажирское сиденье, ремень, сертификат
    c.poly([(930, 760), (1080, 736), (1080, W), (960, W)], (92, 70, 58))
    c.poly([(780, 944), (1080, 910), (1080, W), (760, W)], (104, 80, 66))
    c.line([(790, 990), (1080, 956)], (84, 64, 52), 4)
    c.line([(1060, 760), (940, 1000)], (96, 100, 110), 26)
    c.rect((906, 990, 968, 1030), fill=(60, 62, 70), r=8)
    c.rect((920, 1000, 954, 1020), fill=(210, 60, 50), r=5)

    def cert(t, w, h):
        t.rect((8, 8, w - 8, h - 8), outline=(40, 70, 120), width=4, r=4)
        t.rect((16, 16, w - 16, h - 16), outline=(200, 170, 90), width=2, r=3)
        t.text((w / 2, 40), "CERTIFICATE", "serb", 26, (30, 50, 90), anchor="mm")
        t.text((w / 2, 70), "OF COMPLETION", "sb", 16, (30, 50, 90), anchor="mm")
        t.line([(40, 92), (w - 40, 92)], (190, 196, 206), 2)
        t.text((w / 2, 114), "Driving Safety Course", "lseri", 20, (60, 66, 80), anchor="mm")
        t.circle(56, h - 42, 22, fill=(232, 176, 40))
        t.circle(56, h - 42, 14, outline=WH, width=2)
        t.line([(w - 150, h - 34), (w - 40, h - 34)], (150, 156, 166), 2)
    subcanvas(c, (774, 850, 1060, 1030), -9, cert, paper=(252, 249, 238), shadow=90)


def us_scene(P, t):
    p = P["pal"]
    c = C(WH)
    sc_us_car(c)
    y = c.block(t["title"], "db", 64, 40, 980, WH, max_lines=2, gap=1.1)
    y = c.block(t["sub"], "s", 31, y + 10, 900, (220, 226, 240), max_lines=2, gap=1.14)
    c.button(P["cta"], W / 2, y + 66, size=42, fill=p["btn"])
    return c


PACKS[1] = dict(
    doc="P60-senior-driving-us-2026-09-30", cta="Learn more",
    pal=dict(bg=(240, 246, 252), bg2=(222, 234, 248), btn=ORG1),
    a=dict(fn=us_grid, title="What a driving refresher course usually covers", sub="Most programs include – pick a topic:",
           tiles=[("w5_roundabout", "Roundabouts", "and newer intersection designs", (208, 230, 250), (180, 212, 242), NAVY1),
                  ("w5_merge", "Highway merging", "left turns, safe following distance", (214, 236, 226), (186, 220, 204), NAVY1),
                  ("w5_glare", "Night driving & glare", "and driving in the rain", (40, 52, 96), (22, 30, 64), (220, 226, 240)),
                  ("w5_assist", "Driver-assist features", "backup camera, blind-spot warning", (252, 236, 206), (248, 220, 170), NAVY1)],
           text="What a driving refresher course usually covers / Most programs include – pick a topic: / 1 Roundabouts – and newer "
                "intersection designs / 2 Highway merging – left turns, safe following distance / 3 Night driving & glare – and driving in the "
                "rain / 4 Driver-assist features – backup camera, blind-spot warning (у каждой плитки «Learn more →»)",
           note="4 плитки-темы курса с крупными иконками (кольцо, съезд на шоссе, фары ночью, датчики слепых зон); опора — раздел "
                "«What the course usually covers»; без возраста и здоровья зрителя, без «no road test» как гарантии"),
    b=dict(fn=us_checklist, title="Course first,", title2="then ask the insurer",
           sub="4 questions before paying for a driving safety course",
           tag="INSURER CHECKLIST", q="Some insurers may offer a discount – ask first:", step="1 of 4 checked",
           items=["Is there a discount on this policy?", "Which courses are accepted?", "Does the online version count?",
                  "How long does the discount last?"],
           pal=dict(bg=(255, 248, 232), bg2=(252, 226, 186)),
           text="Course first, / then ask the insurer / 4 questions before paying for a driving safety course / кнопка «Learn more →» / "
                "на телефоне: INSURER CHECKLIST / Some insurers may offer a discount – ask first: / 1 of 4 checked / "
                "Is there a discount on this policy? (отмечен) / Which courses are accepted? / Does the online version count? / "
                "How long does the discount last?",
           note="слева заголовок (хук РК 2) и кнопка, справа телефон с чек-листом из 4 вопросов страховщику, первый отмечен; опора — "
                "раздел «Defensive driving course for insurance discount: how it may work» (4 вопроса); скидка только «Some insurers may offer»"),
    c=dict(fn=us_formats, title="Defensive driving course:", title2="online or classroom?",
           cols=[("ONLINE", "Self-paced short modules", "A timer tracks the hours, then a final quiz", BLUE1, (224, 238, 252)),
                 ("CLASSROOM", "1–2 sessions", "With an instructor and a group", ORG1, (253, 238, 214))],
           modules=[("Module 1", "done"), ("Module 2", "done"), ("Module 3", "now"), ("Final quiz", "todo")],
           band=[("clock", "Usually 4–8 hours in total"), ("w5_cert", "Certificate at the end")],
           foot="Premium depends on: record · car · mileage · coverage",
           pal=dict(bg=(246, 249, 253), bg2=(230, 238, 248)),
           text="Defensive driving course: / online or classroom? / ONLINE: Self-paced short modules – A timer tracks the hours, then a "
                "final quiz (на экране ноутбука: Module 1 ✓ / Module 2 ✓ / Module 3 / Final quiz) / vs / CLASSROOM: 1–2 sessions – "
                "With an instructor and a group / Usually 4–8 hours in total · Certificate at the end / Premium depends on: record · "
                "car · mileage · coverage / кнопка «Learn more →»",
           note="две карточки-иллюстрации (ноутбук с модулями и тестом / класс с доской и инструктором), плашка «4–8 часов, "
                "сертификат», строка «от чего зависит премия»; опора — разделы «Online defensive driving course or classroom» и "
                "«Comparing the numbers before and after»; цен и процентов нет"),
    d=dict(fn=us_scene, title="Stay confident\nbehind the wheel",
           sub="How driving refresher courses work – and when some insurers may offer a discount",
           text="Stay confident behind the wheel / How driving refresher courses work – and when some insurers may offer a discount / "
                "кнопка «Learn more →» / на сертификате: CERTIFICATE OF COMPLETION · Driving Safety Course",
           note="салон машины в сумерках без людей: дорога, жёлтый знак кольца впереди, навигатор с маршрутом, руль, на пассажирском "
                "сиденье сертификат о прохождении курса; заголовок = заголовок статьи; опора — лид и раздел «What a refresher course is»"),
)


# =====================================================================  2. DE · обучение · Bildungsgutschein (курс → предприятие)
INK2, TEAL2, YEL2, ORG2 = (18, 52, 72), (0, 128, 120), (255, 204, 64), (232, 96, 28)


def de_grid(P, t):
    """3×2 карточки курсов: иконка в круге, тип курса, название, «Mehr erfahren»."""
    p = P["pal"]
    c = C(p["bg"])
    c.vgrad((0, 0, W, W), p["bg"], p["bg2"])
    y = hdr(c, t["title"], t["sub"], y=40, col=INK2, sub_col=(70, 90, 96), size=58, title2=t["title2"], t2_col=TEAL2, sub_size=30)
    top = y + 24
    g = 20
    tw = (980 - 2 * g) / 3
    th = (1048 - top - g) / 2
    for i, (ic, lab, kind) in enumerate(t["tiles"]):
        x0 = 50 + (i % 3) * (tw + g)
        y0 = top + (i // 3) * (th + g)
        c.card((x0, y0, x0 + tw, y0 + th), fill=WH, r=24, sh_alpha=55, blur=12, off=(0, 6))
        c.rect((x0, y0, x0 + 12, y0 + th), fill=TEAL2, r=6)
        cx = x0 + tw / 2 + 4
        isz = min(118, th * 0.32)
        icy = y0 + 22 + isz * 0.72
        c.circle(cx, icy, isz * 0.72, fill=(222, 240, 236))
        icon(c, ic, cx, icy, isz * 0.98, INK2, bg=(222, 240, 236))
        ky = icy + isz * 0.72 + 14
        kw = c.tw(kind, c.font("sb", 20))[0] + 26
        c.rect((cx - kw / 2, ky, cx + kw / 2, ky + 32), fill=mix(TEAL2, WH, 0.85), r=16)
        c.text((cx, ky + 16), kind, "sb", 20, TEAL2, anchor="mm")
        fs = min(30, c.fit(lab, "db", tw - 36, 2, 30))
        nl = len(c.wrap(lab, c.font("db", fs), tw - 36))
        ly = ky + 44 + (2 - nl) * c.lh("db", fs, 1.05) / 2
        c.block(lab, "db", fs, ly, tw - 36, INK2, cx=cx, max_lines=2, gap=1.05)
        c.pill(P["cta"], cx, y0 + th - 36, size=21, fill=p["btn"], padx=18, pady=9)
    return c


def de_steps(P, t):
    """Опросник: тёмный фон, карточка со степпером из 5 шагов (шаг 2 активен), вопрос, 4 варианта, строка о сроке ваучера."""
    p = P["pal"]
    c = C(p["bg"])
    c.vgrad((0, 0, W, W), p["bg"], p["bg2"])
    c.ellipse((780, -160, 1260, 320), fill=WH, alpha=16)
    c.ellipse((-200, 820, 240, 1260), fill=WH, alpha=12)
    y = c.block(t["title"], "db", 56, 40, 980, WH, max_lines=1)
    y = c.block(t["title2"], "db", 52, y + 2, 980, YEL2, max_lines=1)
    box = (60, y + 26, 1020, 842)
    c.card(box, r=34, sh_alpha=120, blur=22)
    x0, x1 = box[0] + 50, box[2] - 50
    yy = box[1] + 44
    steps = t["steps"]
    n = len(steps)
    xs = [x0 + 40 + k * (x1 - x0 - 80) / (n - 1) for k in range(n)]
    c.line([(xs[0], yy + 30), (xs[-1], yy + 30)], (220, 226, 232), 8)
    c.line([(xs[0], yy + 30), (xs[1], yy + 30)], TEAL2, 8)
    for k, (lab, st) in enumerate(steps):
        col = (40, 160, 90) if st == "done" else (TEAL2 if st == "now" else (196, 204, 212))
        if st == "now":
            c.circle(xs[k], yy + 30, 38, fill=mix(TEAL2, WH, 0.75))
        c.circle(xs[k], yy + 30, 28, fill=col)
        if st == "done":
            c.check(xs[k] - 13, yy + 17, 26, WH, 6)
        else:
            c.text((xs[k], yy + 31), str(k + 1), "db", 26, WH, anchor="mm")
        c.block(lab, "sb", 21, yy + 76, 170, INK2 if st != "todo" else (120, 128, 138), cx=xs[k], max_lines=2, gap=1.02)
    yy += 150
    c.line([(x0, yy), (x1, yy)], (230, 234, 238), 2)
    yy += 24
    c.text((x0, yy), t["tag"], "sb", 26, TEAL2)
    yy += 46
    yy = c.block(t["q"], "db", 42, yy, x1 - x0, (30, 36, 46), align="left", x=x0, max_lines=2, gap=1.1)
    yy += 18
    g = 18
    ow = (x1 - x0 - g) / 2
    oh = min(104, (box[3] - 40 - yy - g) / 2)
    for k, o in enumerate(t["opts"]):
        ox = x0 + (k % 2) * (ow + g)
        oy = yy + (k // 2) * (oh + g)
        c.rect((ox, oy, ox + ow, oy + oh), fill=(244, 248, 247), r=20, outline=(200, 214, 212), width=3)
        c.circle(ox + 40, oy + oh / 2, 22, fill=TEAL2)
        c.text((ox + 40, oy + oh / 2), "ABCD"[k], "db", 22, WH, anchor="mm")
        fs = c.fit(o, "sb", ow - 96, 2, 29)
        nl = len(c.wrap(o, c.font("sb", fs), ow - 96))
        c.block(o, "sb", fs, oy + oh / 2 - nl * c.lh("sb", fs, 1.06) / 2 + 2, ow - 96, (40, 46, 56), align="left", x=ox + 76,
                max_lines=2, gap=1.06)
    c.block(t["foot"], "sb", 30, 866, 980, (220, 240, 236), max_lines=1)
    c.button(P["cta"], W / 2, 978, size=42, fill=p["btn"])
    return c


def de_costs(P, t):
    """«Сколько стоит»: лист «Kosten der Weiterbildung» — что покрывает ваучер, что может быть оплачено, что идёт во время курса."""
    p = P["pal"]
    c = C(p["bg"])
    c.vgrad((0, 0, W, W), p["bg"], p["bg2"])
    y = hdr(c, t["title"], None, y=38, col=INK2, size=56, title2=t["title2"], t2_col=INK2, hl=YEL2)

    def sheet(s_, w, h):
        s_.rect((0, 0, w, 70), fill=TEAL2)
        s_.text((34, 35), t["sheet_head"], "db", 28, WH, anchor="lm")
        yy = 92
        for sec_title, rows, kind in t["sections"]:
            s_.text((34, yy), sec_title, "db", 27, INK2)
            yy += 44
            for r_ in rows:
                if kind == "ok":
                    checkmark_circle(s_, 52, yy + 18, 17, (40, 160, 90))
                    s_.text((84, yy + 18), r_, "sb", 28, (40, 46, 56), anchor="lm")
                elif kind == "plus":
                    checkmark_circle(s_, 52, yy + 18, 17, TEAL2)
                    s_.text((84, yy + 18), r_, "sb", 28, (40, 46, 56), anchor="lm")
                else:
                    lab, val = r_
                    s_.circle(52, yy + 18, 8, fill=INK2)
                    s_.text((84, yy + 18), lab, "sb", 28, (40, 46, 56), anchor="lm")
                    if val:
                        vw = s_.tw(val, s_.font("db", 28))[0] + 30
                        s_.rect((w - 34 - vw, yy - 2, w - 34, yy + 38), fill=YEL2, r=10)
                        s_.text((w - 34 - vw / 2, yy + 18), val, "db", 28, INK2, anchor="mm")
                yy += 48
            yy += 12
            if kind != "info":
                for xx in range(34, int(w) - 34, 22):
                    s_.line([(xx, yy - 6), (xx + 11, yy - 6)], (206, 212, 218), 2)
                yy += 14
    subcanvas(c, (84, y + 26, 996, 884), -1.0, sheet, paper=WH, shadow=70, r=10)
    c.block(t["foot"], "si", 28, 900, 980, (90, 96, 106), max_lines=1)
    c.button(P["cta"], W / 2, 986, size=40, fill=p["btn"])
    return c


def hi_vis(c, info, col=(250, 140, 30), stripe=(226, 230, 234)):
    """Сигнальный жилет и каска поверх фигуры standing()."""
    (lx, ly), (rx, ry) = info["sh_l"], info["sh_r"]
    hip = info["hip"]
    c.poly([(lx - 4, ly - 10), (rx + 4, ry - 10), (rx + 8, hip + 20), (lx - 8, hip + 20)], col)
    for f in (0.45, 0.7):
        yy = ly + (hip - ly) * f
        c.rect((lx - 6, yy, rx + 6, yy + 12), fill=stripe)
    c.poly([((lx + rx) / 2 - 18, ly - 10), ((lx + rx) / 2 + 18, ly - 10), ((lx + rx) / 2, ly + 34)], mix(col, BLACK, 0.2))
    hx, hy = info["head"]
    r = info["r"]
    c.pie((hx - r * 1.2, hy - r * 1.35, hx + r * 1.2, hy + r * 0.75), 180, 360, (250, 250, 250))
    c.rect((hx - r * 1.35, hy - r * 0.36, hx + r * 1.35, hy - r * 0.2), fill=(236, 236, 236), r=4)


def sc_de_warehouse(c):
    c.vgrad((0, 0, W, 870), (236, 241, 245), (212, 220, 228))
    for x in range(0, W, 120):
        c.line([(x, 360), (x, 870)], (222, 228, 234), 2)
    rnd = random.Random(12)
    levels = (400, 540, 690, 870)
    for k in range(3):
        y0, y1 = levels[k], levels[k + 1]
        x = 40
        while x < 1030:
            bw = rnd.uniform(70, 150)
            bh = (y1 - y0) * rnd.uniform(0.55, 0.85)
            if x + bw > 1030:
                break
            col = rnd.choice(((196, 150, 96), (206, 164, 110), (184, 138, 88), (150, 170, 196)))
            c.rect((x, y1 - bh - 12, x + bw, y1 - 12), fill=col, r=3)
            c.line([(x + bw / 2, y1 - bh - 12), (x + bw / 2, y1 - bh + 14)], (232, 210, 160), 6)
            x += bw + rnd.uniform(8, 26)
    for yy in levels:
        c.rect((20, yy - 12, 1060, yy), fill=(40, 96, 170))
    for xx in (20, 290, 550, 810, 1044):
        c.rect((xx, levels[0] - 24, xx + 16, 870), fill=(232, 120, 40))
    c.vgrad((0, 870, W, W), (176, 178, 176), (150, 152, 150))
    c.rect((0, 900, W, 912), fill=(250, 200, 40))
    for xx in range(0, W, 60):
        c.poly([(xx, 900), (xx + 24, 900), (xx + 12, 912), (xx - 12, 912)], (40, 40, 40))
    c.ellipse((90, 930, 520, 980), fill=BLACK, alpha=50)
    icon(c, "w5_forklift", 300, 770, 400, (40, 44, 52), bg=(230, 234, 238), fork_up=0.26, load=True)
    # стол с сертификатом и каской
    c.rect((860, 850, 1070, 870), fill=(150, 110, 70), r=4)
    c.rect((876, 870, 892, 1000), fill=(120, 86, 56))
    c.rect((1036, 870, 1052, 1000), fill=(120, 86, 56))
    c.pie((1000, 812, 1068, 876), 180, 360, (250, 200, 40))
    c.rect((994, 838, 1074, 848), fill=(230, 180, 30), r=4)

    def cert(t_, w, h):
        t_.rect((6, 6, w - 6, h - 6), outline=TEAL2, width=4, r=4)
        t_.text((w / 2, 34), "ZERTIFIKAT", "serb", 21, INK2, anchor="mm")
        t_.text((w / 2, 66), "Staplerschein", "lseri", 20, (70, 76, 90), anchor="mm")
        t_.line([(24, 88), (w - 24, 88)], (190, 196, 206), 2)
        t_.circle(w - 34, h - 26, 15, fill=(232, 176, 40))
        t_.line([(22, h - 24), (84, h - 24)], (150, 156, 166), 2)
    subcanvas(c, (858, 704, 1044, 846), -5, cert, paper=(252, 250, 242), shadow=80)
    # наставник показывает на погрузчик, обучающийся с планшетом (без лиц)
    mt = A.standing(c, 570, 1010, 470, SKIN[0], (200, 200, 204), "short", (46, 120, 110), (60, 64, 76),
                    arm_l=(450, 690))
    hi_vis(c, mt, col=(252, 200, 40))
    tr = A.standing(c, 735, 1000, 450, SKIN[2], (40, 30, 26), "short", (60, 90, 140), (50, 56, 70),
                    arm_l=(700, 770))
    hi_vis(c, tr)
    c.rect((676, 730, 736, 800), fill=(120, 90, 60), r=4)
    c.rect((682, 740, 730, 796), fill=WH, r=2)
    for k in range(4):
        c.line([(688, 752 + k * 11), (724, 752 + k * 11)], (180, 186, 196), 3)


def de_scene(P, t):
    p = P["pal"]
    c = C(WH)
    sc_de_warehouse(c)
    y = c.bars(t["bars"], 36, size=78, cond=0.8, max_w=1000, gap=8)
    c.button(P["cta"], W / 2, y + 58, size=42, fill=p["btn"], padx=56, pady=22, grad=(mix(p["btn"], WH, 0.35), p["btn"]), outline=WH)
    return c


PACKS[2] = dict(
    doc="P60-course-then-job-de-2026-09-30", cta="Mehr erfahren",
    pal=dict(bg=(240, 247, 245), bg2=(218, 236, 232), btn=ORG2),
    a=dict(fn=de_grid, title="Bildungsgutschein 2026:", title2="welche Weiterbildung kommt infrage?",
           sub="Gefördert werden nur zugelassene Kurse – Beispiele:",
           tiles=[("w5_server", "Fachinformatiker", "Umschulung"), ("briefcase", "Kaufmann/-frau Büromanagement", "Umschulung"),
                  ("w5_truck", "Berufskraftfahrer", "Umschulung"), ("w5_forklift", "Staplerschein", "kurzer Lehrgang"),
                  ("shield_check", "Sachkunde Bewachung", "kurzer Lehrgang"), ("w5_code", "IT für Quereinsteiger", "ohne Vorkenntnisse")],
           text="Bildungsgutschein 2026: / welche Weiterbildung kommt infrage? / Gefördert werden nur zugelassene Kurse – Beispiele: / "
                "Umschulung: Fachinformatiker / Umschulung: Kaufmann/-frau Büromanagement / Umschulung: Berufskraftfahrer / "
                "kurzer Lehrgang: Staplerschein / kurzer Lehrgang: Sachkunde Bewachung / ohne Vorkenntnisse: IT für Quereinsteiger "
                "(у каждой карточки «Mehr erfahren →»)",
           note="6 карточек курсов 3×2 (иконка, тип курса, название, кнопка); опора — раздел «Welche Kurse infrage kommen» "
                "(Umschulungen, kurze Lehrgänge, IT Umschulung Quereinsteiger); без логотипов ведомств, без зарплаты и обещания работы"),
    b=dict(fn=de_steps, title="Bildungsgutschein beantragen:", title2="der Ablauf in 5 Schritten",
           steps=[("Beratung", "done"), ("Kurs finden", "now"), ("Ziel begründen", "todo"), ("Gutschein", "todo"), ("Träger", "todo")],
           tag="SCHRITT 2 VON 5", q="Was zeigt eine Kursdatenbank?",
           opts=["Inhalte und Dauer", "Kursbeginn", "Ob der Kurs zugelassen ist", "Alles davon"],
           foot="Gutschein meist 3 Monate gültig · Kursstart erst mit Gutschein",
           pal=dict(bg=(0, 96, 100), bg2=(0, 54, 64)),
           text="Bildungsgutschein beantragen: / der Ablauf in 5 Schritten / Beratung ✓ · Kurs finden · Ziel begründen · Gutschein · "
                "Träger / SCHRITT 2 VON 5 / Was zeigt eine Kursdatenbank? / A Inhalte und Dauer / B Kursbeginn / C Ob der Kurs "
                "zugelassen ist / D Alles davon / Gutschein meist 3 Monate gültig · Kursstart erst mit Gutschein / кнопка «Mehr erfahren →»",
           note="тёмно-бирюзовый фон, карточка со степпером из 5 шагов заявки (шаг 2 активен) и вопросом о курсовой базе; опора — "
                "раздел «Bildungsgutschein beantragen: Schritt für Schritt» (5 шагов, Kursdatenbanken zeigen Inhalte, Dauer, Beginn, "
                "Zulassung; Gültigkeit meist drei Monate; Kurs erst mit Gutschein beginnen)"),
    c=dict(fn=de_costs, title="Geförderte Weiterbildung:", title2="was übernommen werden kann",
           sheet_head="KOSTEN DER WEITERBILDUNG 2026",
           sections=[("Deckt der Bildungsgutschein:", ["Lehrgangskosten", "Prüfungsgebühren"], "ok"),
                     ("Kann zusätzlich übernommen werden:", ["Fahrtkosten zum Kursort", "Kinderbetreuung",
                                                              "Unterkunft, wenn der Kurs weit entfernt ist"], "plus"),
                     ("Während des Kurses:", [("Arbeitslosengeld läuft in vielen Fällen weiter", None),
                                              ("Weiterbildungsgeld bei Umschulung", "? € / Monat")], "info")],
           foot="Was im Einzelfall gilt, steht im Bescheid.",
           pal=dict(bg=(251, 248, 240), bg2=(238, 232, 216)),
           text="Geförderte Weiterbildung: / was übernommen werden kann (жёлтая подсветка) / лист «KOSTEN DER WEITERBILDUNG 2026»: "
                "Deckt der Bildungsgutschein: ✓ Lehrgangskosten ✓ Prüfungsgebühren / Kann zusätzlich übernommen werden: ✓ Fahrtkosten "
                "zum Kursort ✓ Kinderbetreuung ✓ Unterkunft, wenn der Kurs weit entfernt ist / Während des Kurses: Arbeitslosengeld läuft "
                "in vielen Fällen weiter · Weiterbildungsgeld bei Umschulung: ? € / Monat / Was im Einzelfall gilt, steht im Bescheid. / "
                "кнопка «Mehr erfahren →»",
           note="лист-смета «кто что оплачивает»: ваучер (курс, экзамен), возможные доп. расходы, пособие; сумма Weiterbildungsgeld — "
                "«? €» до сверки; опора — раздел «Was während der Weiterbildung übernommen werden kann» + лид; не как безусловная оплата"),
    d=dict(fn=de_scene, bars=[("BILDUNGSGUTSCHEIN 2026:", WH, TEAL2), ("VOM KURS IN DEN BETRIEB", INK2, YEL2)],
           text="BILDUNGSGUTSCHEIN 2026: / VOM KURS IN DEN BETRIEB / кнопка «Mehr erfahren →» / на сертификате: ZERTIFIKAT · Staplerschein",
           note="склад: стеллажи с коробками, погрузчик без логотипа, наставник и обучающийся в сигнальных жилетах и касках (без лиц), "
                "на столе сертификат «Staplerschein» и каска; плашки = хук РК 3; опора — разделы «Vom Kurs in den Betrieb» и "
                "«Kurze Wege: Bewachung und Lager»; без «Job garantiert», зарплаты, логотипов"),
)


# =====================================================================  3. PT · субсидии 60+ · счёт за свет (tarifa social)
AZ3, INK3, YEL3, GRN3, ORG3 = (28, 78, 160), (20, 40, 80), (250, 196, 50), (0, 140, 100), (236, 120, 40)


def azulejo(c, x0, y0, size, fg, bg, grout=None):
    """Плитка-азулежу: цветок из кругов и четверти кругов по углам (узор, без символики)."""
    c.rect((x0, y0, x0 + size, y0 + size), fill=bg)
    cx, cy = x0 + size / 2, y0 + size / 2
    for k in range(4):
        a = math.radians(k * 90 + 45)
        c.circle(cx + math.cos(a) * size * 0.2, cy + math.sin(a) * size * 0.2, size * 0.1, fill=fg)
    c.circle(cx, cy, size * 0.11, fill=fg)
    c.circle(cx, cy, size * 0.05, fill=bg)
    for dx, dy in ((0, 0), (1, 0), (0, 1), (1, 1)):
        c.pie((x0 + dx * size - size * 0.2, y0 + dy * size - size * 0.2, x0 + dx * size + size * 0.2, y0 + dy * size + size * 0.2),
              0, 360, fg)
    for k in range(4):
        a = math.radians(k * 90)
        c.circle(cx + math.cos(a) * size * 0.36, cy + math.sin(a) * size * 0.36, size * 0.035, fill=fg)
    if grout:
        c.rect((x0, y0, x0 + size, y0 + size), outline=grout, width=2)


def azulejo_wall(c, box, size, fg, bg, grout=None):
    x0, y0, x1, y1 = box
    y = y0
    while y < y1:
        x = x0
        while x < x1:
            azulejo(c, x, y, size, fg, bg, grout)
            x += size
        y += size


def pt_grid(P, t):
    """Фон-азулежу, белая шапка, 2×2 плитки: иконка с номером, пункт, пояснение из статьи, «Saiba mais»."""
    p = P["pal"]
    c = C(p["bg"])
    azulejo_wall(c, (0, 0, W, W), 120, (214, 226, 244), (246, 249, 253))
    c.card((40, 30, 1040, 262), fill=WH, r=30, sh_alpha=40, blur=12, off=(0, 6))
    y = hdr(c, t["title"], t["sub"], y=52, col=INK3, sub_col=(80, 92, 110), size=58, title2=t["title2"], t2_col=AZ3, sub_size=30)
    top = max(y + 30, 292)
    g = 22
    tw = (1000 - g) / 2
    th = (1046 - top - g) / 2
    for i, (ic, lab, desc) in enumerate(t["tiles"]):
        x0 = 40 + (i % 2) * (tw + g)
        y0 = top + (i // 2) * (th + g)
        c.card((x0, y0, x0 + tw, y0 + th), fill=WH, r=26, sh_alpha=60, blur=12, off=(0, 6), outline=(200, 214, 238), width=3)
        c.circle(x0 + 88, y0 + 92, 64, fill=(226, 236, 250))
        icon(c, ic, x0 + 88, y0 + 92, 96, INK3, bg=(226, 236, 250))
        num_badge(c, x0 + 136, y0 + 40, 20, i + 1, ORG3)
        fs = c.fit(lab, "db", tw - 200, 2, 34)
        nl = len(c.wrap(lab, c.font("db", fs), tw - 200))
        c.block(lab, "db", fs, y0 + 92 - nl * c.lh("db", fs, 1.05) / 2, tw - 200, INK3, align="left", x=x0 + 176, max_lines=2, gap=1.05)
        c.block(desc, "s", 28, y0 + 178, tw - 60, (84, 94, 110), align="left", x=x0 + 32, max_lines=2, gap=1.12)
        pw = pill_w(c, P["cta"], 24, 26)
        c.pill(P["cta"], x0 + 32 + pw / 2, y0 + th - 44, size=24, fill=p["btn"], padx=26, pady=11)
    return c


def pt_gauge(P, t):
    """Опросник: синий фон, карточка со шкалой мощности (кВА) и стрелкой на «?», 4 кнопки-варианта."""
    p = P["pal"]
    c = C(p["bg"])
    c.vgrad((0, 0, W, W), p["bg"], p["bg2"])
    azulejo_wall(c, (0, 880, W, W), 100, (44, 96, 178), (30, 80, 162))
    y = c.block(t["title"], "db", 56, 40, 980, WH, max_lines=1)
    y = c.block(t["title2"], "db", 54, y + 2, 980, YEL3, max_lines=1)
    box = (60, y + 22, 1020, 822)
    c.card(box, r=34, sh_alpha=120, blur=22)
    x0, x1 = box[0] + 50, box[2] - 50
    yy = box[1] + 34
    c.text((x0, yy), t["tag"], "sb", 25, AZ3)
    c.text((x1, yy), t["step"], "s", 25, (110, 116, 124), anchor="ra")
    c.rect((x0, yy + 44, x1, yy + 56), fill=(226, 232, 238), r=6)
    c.rect((x0, yy + 44, x0 + (x1 - x0) * 0.5, yy + 56), fill=AZ3, r=6)
    # шкала
    gcx, gcy, R = W / 2, yy + 300, 200
    labs = t["scale"]
    cols = ((120, 190, 140), (190, 214, 120), (250, 200, 80), (240, 140, 70))
    for k in range(4):
        c.pie((gcx - R, gcy - R, gcx + R, gcy + R), 180 + k * 45, 180 + (k + 1) * 45, cols[k])
    c.pie((gcx - R + 46, gcy - R + 46, gcx + R - 46, gcy + R - 46), 180, 360, WH)
    for k, lab in enumerate(labs):
        a = math.radians(180 + 22.5 + k * 45)
        c.text((gcx + math.cos(a) * (R + 34), gcy + math.sin(a) * (R + 30)), lab, "db", 26, INK3, anchor="mm")
    c.line([(gcx, gcy), (gcx, gcy - R + 60)], INK3, 10)
    c.poly([(gcx - 14, gcy - R + 66), (gcx + 14, gcy - R + 66), (gcx, gcy - R + 40)], INK3)
    c.circle(gcx, gcy, 26, fill=INK3)
    c.circle(gcx, gcy - 86, 30, fill=ORG3)
    c.text((gcx, gcy - 85), "?", "db", 36, WH, anchor="mm")
    c.text((gcx, gcy + 52), "kVA", "db", 26, (110, 120, 136), anchor="mm")
    yy = gcy + 82
    yy = c.block(t["q"], "db", 38, yy, x1 - x0, (30, 36, 46), max_lines=1)
    yy += 18
    g = 16
    bw = (x1 - x0 - 3 * g) / 4
    for k, o in enumerate(t["opts"]):
        bx = x0 + k * (bw + g)
        c.rect((bx, yy, bx + bw, yy + 84), fill=(240, 245, 252), r=18, outline=(190, 206, 230), width=3)
        c.text((bx + bw / 2, yy + 42), o, "db", c.fit(o, "db", bw - 20, 1, 32), INK3, anchor="mm")
    c.block(t["foot"], "sb", 30, 840, 980, WH, max_lines=1)
    c.button(P["cta"], W / 2, 966, size=42, fill=p["btn"], outline=WH)
    return c


def dial24(c, cx, cy, R, segs, ring=46):
    """Сутки кольцом (0 ч сверху): segs = [(час_от, час_до, цвет)]."""
    c.circle(cx, cy, R + 6, fill=(230, 234, 240))
    for h0, h1, col in segs:
        c.pie((cx - R, cy - R, cx + R, cy + R), h0 / 24 * 360 - 90, h1 / 24 * 360 - 90, col)
    c.circle(cx, cy, R - ring, fill=WH)
    for h in range(24):
        a = math.radians(h / 24 * 360 - 90)
        L = 14 if h % 6 == 0 else 7
        c.line([(cx + math.cos(a) * (R - ring - 4), cy + math.sin(a) * (R - ring - 4)),
                (cx + math.cos(a) * (R - ring - 4 - L), cy + math.sin(a) * (R - ring - 4 - L))], (170, 176, 186), 3)


def sun_small(c, x, y, r, col=(250, 190, 40)):
    for k in range(8):
        a = math.radians(k * 45)
        c.line([(x + math.cos(a) * r * 1.3, y + math.sin(a) * r * 1.3), (x + math.cos(a) * r * 1.8, y + math.sin(a) * r * 1.8)], col, r * 0.3)
    c.circle(x, y, r, fill=col)


def moon_small(c, x, y, r, col=(250, 236, 180), bg=(60, 80, 140)):
    c.circle(x, y, r, fill=col)
    c.circle(x + r * 0.5, y - r * 0.35, r * 0.85, fill=bg)


def pt_dials(P, t):
    """Сравнение «simples / bi-horária»: два суточных кольца, пояснения из статьи, строка счёта с «? €»."""
    p = P["pal"]
    c = C(p["bg"])
    c.vgrad((0, 0, W, W), p["bg"], p["bg2"])
    y = hdr(c, t["title"], t["sub"], y=40, col=INK3, sub_col=(80, 92, 110), size=64, sub_size=32)
    top, bot = y + 26, 736
    g = 26
    cw = (960 - g) / 2
    for k, (lab, segs, l1, l2, col) in enumerate(t["cols"]):
        x0 = 60 + k * (cw + g)
        c.card((x0, top, x0 + cw, bot), fill=WH, r=28, sh_alpha=60, blur=14, off=(0, 8))
        c.rect((x0, top, x0 + cw, top + 70), fill=col, r=28)
        c.rect((x0, top + 40, x0 + cw, top + 70), fill=col)
        c.text((x0 + cw / 2, top + 36), lab, "db", 32, WH, anchor="mm")
        R = 118
        dcx, dcy = x0 + cw / 2, top + 70 + 30 + R
        dial24(c, dcx, dcy, R, segs)
        if k == 0:
            sun_small(c, dcx - 30, dcy, 16)
            moon_small(c, dcx + 32, dcy, 18, col=(120, 130, 170), bg=WH)
        else:
            moon_small(c, dcx + 66, dcy - 60, 15, col=WH, bg=(60, 150, 110))
            sun_small(c, dcx - 70, dcy + 58, 11, col=WH)
            c.text((dcx, dcy), "24 h", "db", 30, (90, 96, 110), anchor="mm")
        if k == 0:
            c.text((dcx, dcy + 36), "24 h", "db", 26, (90, 96, 110), anchor="mm")
        ty = dcy + R + 26
        ty = c.block(l1, "db", c.fit(l1, "db", cw - 50, 2, 30), ty, cw - 50, INK3, cx=dcx, max_lines=2, gap=1.08)
        c.block(l2, "s", 26, ty + 6, cw - 50, (84, 94, 110), cx=dcx, max_lines=2, gap=1.1)
    c.circle(W / 2, top + 70 + 30 + 118, 40, fill=WH, outline=(200, 206, 214), width=3)
    c.text((W / 2, top + 70 + 30 + 118), "ou", "db", 28, (90, 96, 106), anchor="mm")
    # строка счёта
    band = (60, 760, 1020, 880)
    c.card(band, fill=WH, r=22, sh_alpha=50, blur=10, off=(0, 6), outline=(206, 214, 226), width=2)
    c.text((band[0] + 30, band[1] + 30), t["bill_head"], "db", 24, AZ3, anchor="lm")
    chips = t["bill"]
    cwid = (band[2] - band[0] - 60 - 2 * 16) / 3
    for k, ch in enumerate(chips):
        bx = band[0] + 30 + k * (cwid + 16)
        c.rect((bx, band[1] + 56, bx + cwid, band[3] - 14), fill=(240, 244, 250), r=14)
        c.text((bx + cwid / 2, (band[1] + 56 + band[3] - 14) / 2), ch, "sb", c.fit(ch, "sb", cwid - 20, 1, 27), INK3, anchor="mm")
    c.button(P["cta"], W / 2, 972, size=42, fill=p["btn"])
    return c


def sc_pt_kitchen(c):
    """Кухня вечером: стена с азулежу, щиток с автоматами и счётчик, лампа, на столе счёт, очки, чашка."""
    c.vgrad((0, 0, W, 600), (80, 70, 96), (170, 138, 116))
    azulejo_wall(c, (0, 600, W, 800), 65, (46, 96, 176), (236, 240, 248), grout=(210, 216, 228))
    c.rect((0, 590, W, 604), fill=(210, 196, 176))
    # щиток и счётчик
    qb = (60, 400, 300, 600)
    c.shadow(qb, r=10, alpha=80, blur=8, off=(0, 6))
    c.rect(qb, fill=(236, 236, 232), r=10)
    c.rect((qb[0] + 14, qb[1] + 14, qb[2] - 14, qb[3] - 14), fill=(214, 216, 212), r=6)
    icon(c, "w5_breakers", 180, 500, 200, (60, 66, 80), bg=(214, 216, 212))
    mb = (330, 420, 450, 590)
    c.shadow(mb, r=10, alpha=80, blur=8, off=(0, 6))
    c.rect(mb, fill=(226, 228, 224), r=10)
    c.rect((346, 440, 434, 486), fill=(170, 210, 180), r=4)
    c.text((390, 463), "kWh", "db", 22, (40, 70, 50), anchor="mm")
    c.circle(390, 530, 22, fill=(190, 194, 190))
    c.circle(420, 566, 6, fill=(230, 60, 50))
    # лампа и свет
    c.glow((520, 560, 1000, 1000), (255, 214, 140), alpha=110, blur=70)
    c.line([(760, 330), (760, 470)], (60, 56, 60), 4)
    c.poly([(700, 540), (820, 540), (790, 470), (730, 470)], (236, 170, 60))
    c.ellipse((730, 526, 790, 556), fill=(255, 246, 210))
    # стол
    S.wood(c, (0, 800, W, W), (170, 118, 76), (140, 94, 58), lines=7, seed=5)
    c.rect((0, 796, W, 812), fill=(120, 80, 50))
    S.teacup(c, 170, 900, 0.95, rim=(46, 96, 176))

    def bill(t_, w, h):
        t_.rect((0, 0, w, 50), fill=AZ3)
        t_.text((24, 25), "FATURA DA LUZ", "db", 25, WH, anchor="lm")
        rows = (("Potência contratada", "? kVA", True), ("Energia consumida", "? kWh", False), ("Taxas e impostos", "? €", False))
        yy = 80
        for lab, val, hl in rows:
            if hl:
                t_.rect((14, yy - 20, w - 14, yy + 20), fill=(255, 226, 90), r=6)
            t_.text((24, yy), lab, "sb", 24, (40, 44, 56), anchor="lm")
            t_.text((w - 24, yy), val, "db", 24, (40, 44, 56), anchor="rm")
            yy += 44
        t_.line([(24, yy - 18), (w - 24, yy - 18)], (200, 206, 214), 2)
        t_.text((24, yy + 10), "Total", "db", 26, INK3, anchor="lm")
        t_.text((w - 24, yy + 10), "? €", "db", 28, INK3, anchor="rm")
    subcanvas(c, (380, 810, 790, 1066), -4, bill, paper=WH, shadow=80)
    S.glasses(c, 880, 980, 0.95)
    S.pen(c, 250, 1040, 340, 980, col=(40, 70, 150), w=12)


def pt_scene(P, t):
    p = P["pal"]
    c = C(WH)
    sc_pt_kitchen(c)
    box = (70, 34, 1010, 360)
    c.shadow(box, r=18, alpha=120, blur=18, off=(0, 10))
    c.rect(box, fill=(252, 249, 242), r=18)
    c.rect((box[0] + 14, box[1] + 14, box[2] - 14, box[3] - 14), outline=AZ3, width=3, r=12)
    c.rect((box[0] + 24, box[1] + 24, box[2] - 24, box[3] - 24), outline=AZ3, width=1, r=8)
    y = c.block(t["title"], "lserb", 54, box[1] + 44, box[2] - box[0] - 110, INK3, max_lines=2, gap=1.06)
    c.block(t["sub"], "s", 29, y + 6, box[2] - box[0] - 130, (84, 90, 104), max_lines=2, gap=1.1)
    c.button(P["cta"], W / 2, box[3] + 4, size=40, fill=p["btn"], outline=WH)
    return c


PACKS[3] = dict(
    doc="P60-energy-subsidy-pt-2026-09-30", cta="Saiba mais",
    pal=dict(bg=(246, 249, 253), bg2=(226, 236, 250), btn=GRN3),
    a=dict(fn=pt_grid, title="Fatura da luz 2026:", title2="4 coisas a rever", sub="Sinais de que se paga mais do que o necessário",
           tiles=[("w5_breakers", "Potência contratada", "Valor fixo por dia, pago mesmo sem consumo"),
                  ("w5_daynight", "Opção horária", "Simples, bi-horária ou tri-horária"),
                  ("w5_meter_q", "Leituras estimadas", "O acerto pode chegar de uma só vez"),
                  ("w5_doc_plus", "Serviços extra", "Assistência, seguros e pacotes à parte")],
           text="Fatura da luz 2026: / 4 coisas a rever / Sinais de que se paga mais do que o necessário / 1 Potência contratada – Valor "
                "fixo por dia, pago mesmo sem consumo / 2 Opção horária – Simples, bi-horária ou tri-horária / 3 Leituras estimadas – O "
                "acerto pode chegar de uma só vez / 4 Serviços extra – Assistência, seguros e pacotes à parte (у каждой плитки «Saiba mais →»)",
           note="фон-узор азулежу, 2×2 плитки «4 признака» с иконками (щиток, день/ночь, счётчик с «?», лист с «+»); опора — разделы "
                "«O que se paga na fatura da luz» и «Quatro sinais de que a fatura está mais alta do que devia»; безлично, без сумм и "
                "логотипов"),
    b=dict(fn=pt_gauge, title="Potência contratada:", title2="qual é a certa?", tag="TESTE RÁPIDO", step="Pergunta 1 de 2",
           scale=["3,45", "4,6", "5,75", "6,9"], q="Qual é a potência na fatura?",
           opts=["3,45 kVA", "4,6 kVA", "5,75 kVA", "6,9 kVA"],
           foot="Tarifa social: só em contratos até 6,9 kVA",
           pal=dict(bg=(30, 82, 166), bg2=(16, 48, 112)),
           text="Potência contratada: / qual é a certa? / TESTE RÁPIDO · Pergunta 1 de 2 / шкала kVA: 3,45 · 4,6 · 5,75 · 6,9, стрелка "
                "на «?» / Qual é a potência na fatura? / 3,45 kVA / 4,6 kVA / 5,75 kVA / 6,9 kVA / Tarifa social: só em contratos até "
                "6,9 kVA / кнопка «Saiba mais →»",
           note="синий фон с полосой азулежу, карточка-тест со шкалой мощности и 4 кнопками-ступенями; опора — раздел «Potência "
                "contratada: como saber qual é a certa» (ступени 3,45 / 4,6 / 5,75 / 6,9 кВА; tarifa social до 6,9 кВА)"),
    c=dict(fn=pt_dials, title="Simples ou bi-horária?", sub="Qual combina com os hábitos da casa",
           cols=[("SIMPLES", [(0, 24, (246, 190, 70))], "O mesmo preço do kWh", "a qualquer hora do dia", (214, 140, 30)),
                 ("BI-HORÁRIA", [(8, 22, (240, 130, 70)), (22, 32, (60, 150, 110))], "Mais barato nas horas de vazio",
                  "sobretudo à noite e ao fim de semana; mais caro fora delas", AZ3)],
           bill_head="NA FATURA:", bill=["Potência: ? €", "Energia: ? €", "Taxas e impostos: ? €"],
           pal=dict(bg=(248, 250, 253), bg2=(230, 238, 250)),
           text="Simples ou bi-horária? / Qual combina com os hábitos da casa / SIMPLES: O mesmo preço do kWh – a qualquer hora do dia "
                "(кольцо суток одного цвета, 24 h) / ou / BI-HORÁRIA: Mais barato nas horas de vazio – sobretudo à noite e ao fim de "
                "semana; mais caro fora delas (кольцо суток: ночная часть зелёная, дневная оранжевая) / NA FATURA: Potência: ? € · "
                "Energia: ? € · Taxas e impostos: ? € / кнопка «Saiba mais →»",
           note="два суточных кольца «simples / bi-horária» и строка счёта из трёх блоков с «? €» (статья объясняет, из чего "
                "складывается сумма); опора — раздел «O que se paga na fatura da luz»; без сумм и процентов"),
    d=dict(fn=pt_scene, title="A parte da fatura da luz que se paga todos os dias",
           sub="Mesmo sem consumir: como saber se a\npotência contratada é a certa",
           text="A parte da fatura da luz que se paga todos os dias / Mesmo sem consumir: como saber se a potência contratada é a certa / "
                "кнопка «Saiba mais →» / на счётчике: kWh / на счёте: FATURA DA LUZ · Potência contratada ? kVA (подсветка) · Energia "
                "consumida ? kWh · Taxas e impostos ? € · Total ? €",
           note="кухня вечером: стена с азулежу, щиток с автоматами (один выключен) и счётчик, лампа, на столе счёт с подсвеченной "
                "строкой мощности, очки, чашка; карточка в рамке = хук РК 3; опора — разделы «O que se paga…» и «Potência contratada»"),
)


# =====================================================================  4. IT · субсидии 60+ · bolletta luce (bonus sociale)
INK4, TERRA4, OLIVE4, BLUE4, CREAM4 = (40, 36, 52), (198, 84, 44), (96, 128, 64), (0, 106, 176), (252, 246, 236)
VOCI4 = ((198, 84, 44), (236, 164, 60), (96, 128, 64), (110, 120, 150))


def bill_markers(c, box):
    """«Герой»: бумажная bolletta с 4 пронумерованными строками и лупой."""
    c.rect(box, fill=(246, 226, 206), r=26)
    x0, y0, x1, y1 = box
    c.dots((x0 + 10, y0 + 10, x1 - 10, y1 - 10), 34, 3, TERRA4, alpha=40)

    def paper(t_, w, h):
        t_.rect((0, 0, w, 46), fill=TERRA4)
        t_.text((22, 23), "BOLLETTA LUCE", "db", 22, WH, anchor="lm")
        for k in range(4):
            yy = 68 + k * 44
            num_badge(t_, 30, yy + 8, 15, k + 1, INK4)
            t_.rect((56, yy, 56 + (w - 120) * (0.9 - 0.12 * (k % 2)), yy + 16), fill=(206, 210, 220), r=6)
            t_.rect((w - 70, yy, w - 24, yy + 16), fill=(236, 190, 120), r=6)
    subcanvas(c, (x0 + 250, y0 + 22, x0 + 650, y1 - 22), -3, paper, paper=WH, shadow=70)
    lx, ly = x0 + 740, y0 + (y1 - y0) * 0.5
    c.circle(lx, ly, 70, fill=WH, alpha=120)
    c.circle(lx, ly, 70, outline=INK4, width=14)
    c.line([(lx + 50, ly + 50), (lx + 110, ly + 110)], INK4, 22)
    icon(c, "bulb", x0 + 120, ly, 150, INK4, bg=(246, 226, 206))


def it_grid(P, t):
    p = P["pal"]
    c = C(p["bg"])
    c.vgrad((0, 0, W, W), p["bg"], p["bg2"])
    y = hdr(c, t["title"], t["sub"], y=40, col=INK4, sub_col=(96, 90, 86), size=58, title2=t["title2"], t2_col=TERRA4, sub_size=30)
    hb = (60, y + 22, 1020, y + 22 + 300)
    bill_markers(c, hb)
    top = hb[3] + 24
    g = 18
    tw = (960 - 3 * g) / 4
    th = 1046 - top
    for i, (ic, lab, desc) in enumerate(t["tiles"]):
        x0 = 60 + i * (tw + g)
        cx = x0 + tw / 2
        c.card((x0, top, x0 + tw, top + th), fill=WH, r=24, sh_alpha=55, blur=12, off=(0, 6))
        num_badge(c, x0 + 30, top + 30, 17, i + 1, TERRA4)
        icy = top + 96
        c.circle(cx, icy, 64, fill=(250, 234, 218))
        icon(c, ic, cx, icy, 96, INK4, bg=(250, 234, 218))
        fs = min(c.fit(x[1], "db", tw - 24, 2, 27) for x in t["tiles"])
        ly = c.block(lab, "db", fs, icy + 82, tw - 24, INK4, cx=cx, max_lines=2, gap=1.04)
        c.block(desc, "s", 23, ly + 8, tw - 26, (100, 96, 96), cx=cx, max_lines=3, gap=1.1)
        c.pill(P["cta"], cx, top + th - 34, size=19, fill=p["btn"], padx=15, pady=9)
    return c


def it_phone_steps(P, t):
    """Слева 3 шага бонуса (DSU → ISEE → скидка в счёте), справа телефон с вопросом."""
    p = P["pal"]
    c = C(p["bg"])
    c.vgrad((0, 0, W, W), p["bg"], p["bg2"])
    c.ellipse((-220, -200, 360, 300), fill=WH, alpha=40)
    lx = 56
    y = c.block(t["title"], "db", 50, 52, 470, INK4, align="left", x=lx, max_lines=2, gap=1.06)
    y = c.block(t["title2"], "db", 46, y + 4, 470, OLIVE4, align="left", x=lx, max_lines=2, gap=1.06)
    y += 30
    steps = t["steps"]
    sh = 150
    for k, (ic, lab, desc) in enumerate(steps):
        yy = y + k * sh
        if k < len(steps) - 1:
            c.line([(lx + 42, yy + 84), (lx + 42, yy + sh)], mix(OLIVE4, WH, 0.4), 6)
        c.circle(lx + 42, yy + 42, 42, fill=OLIVE4)
        icon(c, ic, lx + 42, yy + 42, 52, WH, bg=OLIVE4)
        c.text((lx + 104, yy + 4), f"{k + 1}. {lab}", "db", 32, INK4)
        c.block(desc, "s", 25, yy + 48, 370, (90, 86, 80), align="left", x=lx + 104, max_lines=2, gap=1.08)
    bb = c.button(P["cta"], 0, -700, size=38, fill=p["btn"])
    c.button(P["cta"], lx + (bb[2] - bb[0]) / 2, y + len(steps) * sh + 50, size=38, fill=p["btn"])
    ph = (548, 60, 1030, 1030)
    c.shadow(ph, r=64, alpha=110, blur=24, off=(0, 16))
    c.rect(ph, fill=(30, 30, 36), r=64)
    sc = (ph[0] + 16, ph[1] + 16, ph[2] - 16, ph[3] - 16)
    c.rect(sc, fill=WH, r=50)
    c.rect(((ph[0] + ph[2]) / 2 - 70, ph[1] + 28, (ph[0] + ph[2]) / 2 + 70, ph[1] + 60), fill=(30, 30, 36), r=16)
    c.text((sc[0] + 38, ph[1] + 44), "19:00", "sb", 22, (40, 40, 40), anchor="lm")
    x0, x1 = sc[0] + 32, sc[2] - 32
    yy = sc[1] + 92
    tag = t["tag"]
    tw_ = c.tw(tag, c.font("sb", 22))[0]
    c.rect((x0, yy, x0 + tw_ + 30, yy + 40), fill=mix(OLIVE4, WH, 0.82), r=20)
    c.text((x0 + 15, yy + 20), tag, "sb", 22, OLIVE4, anchor="lm")
    yy += 64
    c.text((x0, yy), t["step"], "s", 24, (110, 116, 124))
    c.rect((x0, yy + 40, x1, yy + 50), fill=(226, 232, 236), r=5)
    c.rect((x0, yy + 40, x0 + (x1 - x0) / 3, yy + 50), fill=OLIVE4, r=5)
    yy += 80
    yy = c.block(t["q"], "db", 32, yy, x1 - x0, (34, 34, 44), align="left", x=x0, max_lines=4, gap=1.1)
    yy += 20
    n = len(t["opts"])
    h = 76
    for k, o in enumerate(t["opts"]):
        c.rect((x0, yy, x1, yy + h), fill=(246, 246, 242), r=h / 2, outline=(214, 212, 204), width=3)
        c.circle(x0 + h / 2 + 2, yy + h / 2, 15, fill=WH, outline=(150, 156, 164), width=3)
        c.block(o, "sb", c.fit(o, "sb", x1 - x0 - h - 30, 1, 27), yy + h / 2 - 17, x1 - x0 - h - 30, (48, 50, 58), align="left", x=x0 + h + 4, max_lines=1)
        yy += h + 14
    c.rect((x0, yy + 16, x1, yy + 110), fill=mix(OLIVE4, WH, 0.86), r=18)
    c.block(t["foot"], "sb", 26, yy + 30, x1 - x0 - 40, OLIVE4, cx=(x0 + x1) / 2, max_lines=2, gap=1.08)
    return c


def it_bars(P, t):
    """«Сколько стоит»: две оферты — столбики годовой суммы из 4 статей счёта, у каждой «? €»; легенда справа."""
    p = P["pal"]
    c = C(p["bg"])
    c.vgrad((0, 0, W, W), p["bg"], p["bg2"])
    y = hdr(c, t["title"], t["sub"], y=44, col=INK4, sub_col=(96, 90, 86), size=60, sub_size=31, lines=1)
    box = (50, y + 28, 1030, 900)
    c.card(box, r=28, sh_alpha=60, blur=14, off=(0, 8))
    base = box[3] - 150
    topmax = box[1] + 110
    Hmax = base - topmax
    bw = 170
    for k, (name, tag, segs, best) in enumerate(t["offers"]):
        bx = box[0] + 70 + k * 270
        cx = bx + bw / 2
        total = sum(segs)
        yy = base
        for j, f in enumerate(segs):
            h = Hmax * f
            c.rect((bx, yy - h, bx + bw, yy), fill=VOCI4[j])
            c.line([(bx, yy - h), (bx + bw, yy - h)], WH, 3)
            if h > 32:
                c.text((cx, yy - h / 2), "? €", "db", 26 if h > 44 else 22, WH, anchor="mm")
            yy -= h
        top_y = base - Hmax * total
        c.text((cx, top_y - 58), "Totale anno", "sb", 22, (90, 86, 84), anchor="mm")
        c.text((cx, top_y - 26), "? €", "db", 34, INK4, anchor="mm")
        c.text((cx, base + 30), name, "db", 26, INK4, anchor="mm")
        c.block(tag, "sb", 21, base + 52, bw + 60, OLIVE4 if best else (120, 110, 104), cx=cx, max_lines=2, gap=1.04)
        if best:
            checkmark_circle(c, bx + bw + 34, top_y - 30, 26, (40, 150, 80))
    c.line([(box[0] + 40, base), (box[0] + 600, base)], (170, 164, 156), 4)
    lx = box[0] + 640
    ly = box[1] + 70
    c.text((lx, ly), t["legend_head"], "db", 25, INK4)
    ly += 56
    for j, lab in enumerate(t["legend"]):
        c.rect((lx, ly, lx + 36, ly + 36), fill=VOCI4[j], r=8)
        c.block(lab, "sb", 25, ly + 2, 270, INK4, align="left", x=lx + 50, max_lines=2, gap=1.04)
        nl = len(c.wrap(lab, c.font("sb", 25), 270))
        ly += 40 + nl * 30
    c.line([(lx, ly + 4), (box[2] - 40, ly + 4)], (224, 218, 208), 2)
    c.block(t["legend_foot"], "s", 23, ly + 20, 300, (96, 90, 86), align="left", x=lx, max_lines=4, gap=1.12)
    c.button(P["cta"], W / 2, 978, size=42, fill=p["btn"])
    return c


def moka(c, cx, by, s=1.0):
    """Гейзерная кофеварка (силуэт, без бренда)."""
    m = (176, 180, 188)
    d = (120, 124, 132)
    c.poly([(cx - 46 * s, by), (cx + 46 * s, by), (cx + 36 * s, by - 70 * s), (cx - 36 * s, by - 70 * s)], m)
    c.rect((cx - 40 * s, by - 80 * s, cx + 40 * s, by - 68 * s), fill=d, r=3)
    c.poly([(cx - 36 * s, by - 80 * s), (cx + 36 * s, by - 80 * s), (cx + 46 * s, by - 150 * s), (cx - 46 * s, by - 150 * s)], m)
    c.poly([(cx - 46 * s, by - 150 * s), (cx + 46 * s, by - 150 * s), (cx + 20 * s, by - 172 * s), (cx - 20 * s, by - 172 * s)], d)
    c.circle(cx, by - 176 * s, 8 * s, fill=(40, 40, 44))
    c.poly([(cx + 42 * s, by - 140 * s), (cx + 70 * s, by - 160 * s), (cx + 48 * s, by - 124 * s)], m)
    c.arc((cx - 86 * s, by - 150 * s, cx - 30 * s, by - 90 * s), 90, 270, (40, 40, 44), 10 * s)
    for k in range(3):
        c.line([(cx - 20 * s + k * 20 * s, by - 60 * s), (cx - 20 * s + k * 20 * s, by - 12 * s)], mix(m, WH, 0.35), 4 * s)


def sc_it_kitchen(c):
    """Кухня вечером: окно с черепичными крышами в сумерках, часы на 19:00, электронный счётчик, лампа, на столе bolletta."""
    c.vgrad((0, 0, W, 860), (232, 206, 176), (206, 170, 136))
    # окно
    wb = (70, 424, 470, 764)
    c.rect((wb[0] - 16, wb[1] - 16, wb[2] + 16, wb[3] + 16), fill=(250, 246, 238), r=6)
    c.vgrad(wb, (70, 70, 130), (250, 160, 100))
    c.glow((180, 690, 400, 790), (255, 200, 120), alpha=200, blur=30)
    rnd = random.Random(4)
    for k in range(6):
        x0 = wb[0] + k * 70 - 10
        hgt = rnd.uniform(60, 120)
        col = rnd.choice(((178, 82, 50), (160, 72, 44), (196, 104, 62)))
        c.rect((x0, wb[3] - hgt, x0 + 80, wb[3]), fill=mix(col, (60, 50, 70), 0.35))
        c.poly([(x0 - 6, wb[3] - hgt), (x0 + 40, wb[3] - hgt - 30), (x0 + 86, wb[3] - hgt)], col)
        c.rect((x0 + 16, wb[3] - hgt + 20, x0 + 30, wb[3] - hgt + 38), fill=(255, 214, 120))
    c.rect((wb[0] + 250, wb[1] + 150, wb[0] + 290, wb[3] - 60), fill=(122, 84, 76))
    c.poly([(wb[0] + 244, wb[1] + 150), (wb[0] + 270, wb[1] + 116), (wb[0] + 296, wb[1] + 150)], (160, 76, 50))
    c.line([((wb[0] + wb[2]) / 2, wb[1]), ((wb[0] + wb[2]) / 2, wb[3])], (250, 246, 238), 12)
    c.line([(wb[0], (wb[1] + wb[3]) / 2), (wb[2], (wb[1] + wb[3]) / 2)], (250, 246, 238), 12)
    # часы 19:00
    ccx, ccy = 640, 560
    c.circle(ccx, ccy, 64, fill=(60, 56, 60))
    c.circle(ccx, ccy, 54, fill=WH)
    for h in range(12):
        a = math.radians(h * 30 - 90)
        c.line([(ccx + math.cos(a) * 44, ccy + math.sin(a) * 44), (ccx + math.cos(a) * 50, ccy + math.sin(a) * 50)], (60, 56, 60), 4)
    a = math.radians(7 * 30 - 90)
    c.line([(ccx, ccy), (ccx + math.cos(a) * 28, ccy + math.sin(a) * 28)], (40, 36, 40), 7)
    c.line([(ccx, ccy), (ccx, ccy - 42)], (40, 36, 40), 5)
    c.circle(ccx, ccy, 6, fill=TERRA4)
    # электронный счётчик
    mb = (850, 470, 1010, 690)
    c.shadow(mb, r=12, alpha=80, blur=8, off=(0, 6))
    c.rect(mb, fill=(210, 212, 214), r=12)
    c.rect((870, 494, 990, 548), fill=(40, 46, 44), r=6)
    c.text((930, 521), "kWh", "db", 24, (120, 230, 150), anchor="mm")
    c.circle(890, 580, 8, fill=(230, 50, 40))
    c.rect((910, 572, 990, 588), fill=(180, 184, 188), r=4)
    c.rect((900, 612, 960, 660), fill=(190, 194, 198), r=8)
    # лампа
    c.line([(760, 400), (760, 470)], (60, 56, 60), 4)
    c.pie((700, 460, 820, 580), 180, 360, OLIVE4)
    c.ellipse((740, 512, 780, 530), fill=(255, 246, 210))
    c.glow((560, 520, 1000, 960), (255, 220, 150), alpha=90, blur=60)
    # стол
    S.wood(c, (0, 818, W, W), (132, 88, 58), (106, 68, 44), lines=7, seed=9)
    c.rect((0, 810, W, 826), fill=(96, 62, 40))
    moka(c, 170, 990, 0.95)

    def bolletta(t_, w, h):
        t_.rect((0, 0, w, 50), fill=TERRA4)
        t_.text((22, 25), "BOLLETTA LUCE", "db", 24, WH, anchor="lm")
        yy = 76
        for lab in ("Materia energia", "Trasporto e contatore", "Oneri di sistema", "Imposte"):
            t_.text((22, yy), lab, "sb", 22, (44, 44, 54), anchor="lm")
            t_.text((w - 22, yy), "? €", "db", 22, (44, 44, 54), anchor="rm")
            yy += 36
        t_.line([(22, yy - 14), (w - 22, yy - 14)], (206, 206, 214), 2)
        t_.text((22, yy + 10), "Totale", "db", 24, INK4, anchor="lm")
        t_.text((w - 22, yy + 10), "? €", "db", 26, TERRA4, anchor="rm")
    subcanvas(c, (420, 826, 790, 1072), 4, bolletta, paper=WH, shadow=80)
    S.glasses(c, 900, 930, 0.9)


def it_scene(P, t):
    p = P["pal"]
    c = C(WH)
    sc_it_kitchen(c)
    y = c.bars(t["bars"], 34, size=70, cond=0.8, max_w=1000, gap=8)
    c.button(P["cta"], W / 2, y + 52, size=40, fill=p["btn"], padx=56, pady=20, grad=(mix(p["btn"], WH, 0.35), p["btn"]), outline=WH)
    return c


PACKS[4] = dict(
    doc="P60-energy-subsidy-it-2026-09-30", cta="Scopri di più",
    pal=dict(bg=CREAM4, bg2=(244, 232, 214), btn=BLUE4),
    a=dict(fn=it_grid, title="Bolletta della luce 2026:", title2="4 cose da controllare",
           sub="Come capire se si paga più del necessario",
           tiles=[("w5_cal_x", "Offerta scaduta", "alla scadenza il prezzo può salire"),
                  ("w5_gauge", "Potenza impegnata", "troppo alta = quota fissa più alta"),
                  ("w5_fasce", "Fasce orarie", "F1: giorni feriali dalle 8 alle 19"),
                  ("w5_doc_plus", "Servizi aggiuntivi", "polizze e assistenza come voci a parte")],
           text="Bolletta della luce 2026: / 4 cose da controllare / Come capire se si paga più del necessario / на счёте: BOLLETTA LUCE, "
                "строки 1–4 / 1 Offerta scaduta – alla scadenza il prezzo può salire / 2 Potenza impegnata – troppo alta = quota fissa più "
                "alta / 3 Fasce orarie – F1: giorni feriali dalle 8 alle 19 / 4 Servizi aggiuntivi – polizze e assistenza come voci a parte "
                "(у каждой плитки «Scopri di più →»)",
           note="панель: бумажная bolletta с 4 пронумерованными строками, лупа, лампочка; ниже 4 плитки-признака с иконками; опора — "
                "разделы «Quattro segnali che si paga più del necessario» и «Cosa si paga in una bolletta luce» (F1 8–19); безлично"),
    b=dict(fn=it_phone_steps, title="Bonus sociale bollette 2026:", title2="come funziona in 3 passi",
           steps=[("doc", "DSU", "la dichiarazione per ottenere l'ISEE"), ("calc", "ISEE", "sotto la soglia fissata per l'anno"),
                  ("bulb", "Sconto in bolletta", "voce separata, dura 12 mesi")],
           tag="BONUS SOCIALE", step="Domanda 1 di 3", q="Il bonus sociale va chiesto con una domanda a parte?",
           opts=["Sì, sempre", "No, parte dalla DSU", "Solo cambiando fornitore", "Non so"],
           foot="Si rinnova ogni anno con una nuova DSU",
           pal=dict(bg=(246, 244, 234), bg2=(226, 232, 208)),
           text="Bonus sociale bollette 2026: / come funziona in 3 passi / 1. DSU – la dichiarazione per ottenere l'ISEE / 2. ISEE – sotto "
                "la soglia fissata per l'anno / 3. Sconto in bolletta – voce separata, dura 12 mesi / кнопка «Scopri di più →» / на "
                "телефоне: BONUS SOCIALE · Domanda 1 di 3 / Il bonus sociale va chiesto con una domanda a parte? / Sì, sempre / No, parte "
                "dalla DSU / Solo cambiando fornitore / Non so / Si rinnova ogni anno con una nuova DSU",
           note="слева 3 шага DSU → ISEE → скидка в счёте, справа телефон с вопросом о механике бонуса (не о зрителе); опора — разделы "
                "«Bonus sociale: chi ha diritto» и «quanto dura e come si rinnova»; без порогов ISEE и суммы бонуса"),
    c=dict(fn=it_bars, title="Prezzo al kWh o spesa annua?", sub="Nelle offerte luce conta il totale dell'anno",
           offers=[("OFFERTA A", "prezzo al kWh più basso", (0.36, 0.2, 0.18, 0.14), False),
                   ("OFFERTA B", "spesa annua più bassa", (0.26, 0.2, 0.18, 0.12), True)],
           legend_head="Voci della bolletta:", legend=["Materia energia", "Trasporto e contatore", "Oneri di sistema", "Imposte"],
           legend_foot="Per il confronto: consumo annuo, potenza impegnata, codice POD",
           pal=dict(bg=(252, 248, 240), bg2=(240, 230, 214)),
           text="Prezzo al kWh o spesa annua? / Nelle offerte luce conta il totale dell'anno / OFFERTA A – prezzo al kWh più basso / "
                "OFFERTA B – spesa annua più bassa (✓) / над столбиками: Totale anno ? € / в сегментах: ? € / Voci della bolletta: "
                "Materia energia · Trasporto e contatore · Oneri di sistema · Imposte / Per il confronto: consumo annuo, potenza "
                "impegnata, codice POD / кнопка «Scopri di più →»",
           note="две оферты столбиками годовой суммы из 4 статей счёта, везде «? €» (статья объясняет состав счёта); высоты — "
                "иллюстрация тезиса статьи «дешевле не та, у которой ниже цена кВт·ч, а та, у которой ниже годовая сумма»; опора — "
                "разделы «Cosa si paga in una bolletta luce» и «Confronto tariffe luce»"),
    d=dict(fn=it_scene, bars=[("BOLLETTA DELLA LUCE:", WH, TERRA4), ("4 SEGNALI CHE SI PAGA", INK4, (255, 236, 200)),
                              ("PIÙ DEL NECESSARIO", INK4, (255, 236, 200))],
           text="BOLLETTA DELLA LUCE: / 4 SEGNALI CHE SI PAGA / PIÙ DEL NECESSARIO / кнопка «Scopri di più →» / на счётчике: kWh / на "
                "счёте: BOLLETTA LUCE · Materia energia ? € · Trasporto e contatore ? € · Oneri di sistema ? € · Imposte ? € · Totale ? €",
           note="кухня вечером: окно с черепичными крышами в сумерках, часы на 19:00 (конец F1), электронный счётчик, лампа, на столе "
                "bolletta с «? €», очки, гейзерная кофеварка; плашки = хук РК 1, безлично; опора — разделы «Quattro segnali…» и «Cosa si paga…»"),
)


# =====================================================================  5. PL · кредиты · telefon na raty 12–24 мес.
INK5, VIO5, YEL5, RED5, GRN5 = (24, 30, 56), (92, 64, 196), (255, 210, 64), (220, 48, 60), (40, 160, 90)


def pl_ways(P, t):
    """3 высокие карточки-пути покупки: иконка, название, пояснение из статьи, «Dowiedz się więcej»."""
    p = P["pal"]
    c = C(p["bg"])
    c.vgrad((0, 0, W, W), p["bg"], p["bg2"])
    y = hdr(c, t["title"], t["sub"], y=42, col=INK5, sub_col=(80, 84, 104), size=60, title2=t["title2"], t2_col=VIO5, sub_size=30)
    top, bot = y + 30, 1046
    g = 22
    cw = (960 - 2 * g) / 3
    for i, (ic, lab, desc, tint) in enumerate(t["cards"]):
        x0 = 60 + i * (cw + g)
        cx = x0 + cw / 2
        c.card((x0, top, x0 + cw, bot), fill=WH, r=28, sh_alpha=60, blur=14, off=(0, 8))
        ih = (bot - top) * 0.5
        c.rect((x0 + 12, top + 12, x0 + cw - 12, top + ih), fill=tint, r=22)
        num_badge(c, x0 + 42, top + 42, 20, i + 1, VIO5)
        icon(c, ic, cx, top + 12 + (ih - 12) / 2 + 6, ih * 0.66, INK5, bg=tint)
        fs = min(c.fit(x[1], "db", cw - 34, 2, 32) for x in t["cards"])
        ly = c.block(lab, "db", fs, top + ih + 28, cw - 34, INK5, cx=cx, max_lines=2, gap=1.05)
        c.block(desc, "s", 27, ly + 12, cw - 40, (84, 88, 108), cx=cx, max_lines=3, gap=1.12)
        c.pill(P["cta"], cx, bot - 44, size=21, fill=p["btn"], padx=18, pady=11)
    return c


def pl_contract(P, t):
    """Опросник-чек-лист договора: прогресс 3 из 8, пункты 1–2 отмечены, пункт 3 раскрыт с вариантами."""
    p = P["pal"]
    c = C(p["bg"])
    c.vgrad((0, 0, W, W), p["bg"], p["bg2"])
    c.ellipse((760, -180, 1240, 300), fill=WH, alpha=18)
    y = c.block(t["title"], "db", 58, 40, 980, WH, max_lines=1)
    y = c.block(t["title2"], "db", 50, y + 2, 980, YEL5, max_lines=1)
    box = (60, y + 26, 1020, 900)
    c.card(box, r=34, sh_alpha=120, blur=22)
    x0, x1 = box[0] + 44, box[2] - 44
    yy = box[1] + 36
    c.text((x0, yy), t["tag"], "sb", 25, VIO5)
    c.text((x1, yy), t["step"], "db", 25, INK5, anchor="ra")
    yy += 44
    seg = (x1 - x0 - 7 * 8) / 8
    for k in range(8):
        sx = x0 + k * (seg + 8)
        c.rect((sx, yy, sx + seg, yy + 12), fill=(VIO5 if k < 3 else (226, 226, 236)), r=6)
    yy += 36
    for k, (lab, st) in enumerate(t["items"]):
        if st == "now":
            h = 206
            c.rect((x0, yy, x1, yy + h), fill=(246, 243, 255), r=20, outline=VIO5, width=3)
            num_badge(c, x0 + 36, yy + 40, 20, k + 1, VIO5)
            c.block(lab, "db", c.fit(lab, "db", x1 - x0 - 90, 1, 30), yy + 22, x1 - x0 - 90, INK5, align="left", x=x0 + 72, max_lines=1)
            ow = (x1 - x0 - 40 - 2 * 14) / 3
            for j, o in enumerate(t["opts"]):
                ox = x0 + 20 + j * (ow + 14)
                c.rect((ox, yy + 86, ox + ow, yy + 176), fill=WH, r=18, outline=(200, 194, 230), width=3)
                c.circle(ox + 34, yy + 131, 13, fill=WH, outline=(150, 146, 170), width=3)
                c.text((ox + 58, yy + 131), o, "sb", c.fit(o, "sb", ow - 76, 1, 27), INK5, anchor="lm")
            yy += h + 12
        else:
            h = 62
            done = st == "done"
            c.rect((x0, yy, x1, yy + h), fill=(236, 248, 240) if done else (246, 247, 250), r=18)
            if done:
                checkmark_circle(c, x0 + 36, yy + h / 2, 18, GRN5)
            else:
                c.circle(x0 + 36, yy + h / 2, 17, outline=(170, 172, 186), width=3)
                c.text((x0 + 36, yy + h / 2 + 1), str(k + 1), "db", 18, (140, 142, 156), anchor="mm")
            c.text((x0 + 72, yy + h / 2), lab, "sb", c.fit(lab, "sb", x1 - x0 - 90, 1, 28), INK5 if done else (90, 92, 108), anchor="lm")
            yy += h + 10
    c.text((W / 2, yy + 4), t["more"], "si", 25, (110, 112, 128), anchor="ma")
    c.button(P["cta"], W / 2, 974, size=40, fill=p["btn"], outline=WH)
    return c


def pl_calendars(P, t):
    """Сравнение: сетка из 12 и из 24 платежей, «rata wyższa / niższa», «Całkowita kwota: ? zł» в обеих колонках."""
    p = P["pal"]
    c = C(p["bg"])
    c.vgrad((0, 0, W, W), p["bg"], p["bg2"])
    y = hdr(c, t["title"], t["sub"], y=40, col=INK5, sub_col=(80, 84, 104), size=72, sub_size=31, lines=1)
    top, bot = y + 26, 846
    g = 26
    cw = (960 - g) / 2
    for k, (lab, n, cols, rata, col) in enumerate(t["cols"]):
        x0 = 60 + k * (cw + g)
        cx = x0 + cw / 2
        c.card((x0, top, x0 + cw, bot), fill=WH, r=28, sh_alpha=60, blur=14, off=(0, 8))
        c.rect((x0, top, x0 + cw, top + 76), fill=col, r=28)
        c.rect((x0, top + 46, x0 + cw, top + 76), fill=col)
        c.text((cx, top + 39), lab, "db", 36, WH, anchor="mm")
        rows = n // cols
        gx0, gx1 = x0 + 40, x0 + cw - 40
        gy0 = top + 104
        gh = 290
        cell_w = (gx1 - gx0 - (cols - 1) * 10) / cols
        cell_h = min(cell_w, (gh - (rows - 1) * 10) / rows)
        gy0 += (gh - (rows * cell_h + (rows - 1) * 10)) / 2
        for r_ in range(rows):
            for q in range(cols):
                bx = gx0 + q * (cell_w + 10)
                by = gy0 + r_ * (cell_h + 10)
                c.rect((bx, by, bx + cell_w, by + cell_h), fill=mix(col, WH, 0.78), r=8, outline=mix(col, WH, 0.4), width=2)
                idx = r_ * cols + q + 1
                c.text((bx + cell_w / 2, by + cell_h / 2 + 1), str(idx), "sb", min(24, cell_h * 0.45), mix(col, BLACK, 0.2), anchor="mm")
        yy = top + 104 + gh + 26
        c.text((x0 + 36, yy), t["rata_lab"], "sb", 27, (90, 94, 110))
        c.text((x0 + cw - 36, yy), rata, "db", 28, INK5, anchor="ra")
        yy += 50
        c.line([(x0 + 36, yy), (x0 + cw - 36, yy)], (226, 228, 236), 2)
        yy += 18
        c.rect((x0 + 24, yy, x0 + cw - 24, yy + 96), fill=(255, 244, 196), r=18)
        c.text((cx, yy + 28), t["total_lab"], "sb", 26, (90, 80, 40), anchor="mm")
        c.text((cx, yy + 66), "? zł", "db", 38, INK5, anchor="mm")
    c.circle(W / 2, top + 104 + 145, 40, fill=WH, outline=(200, 206, 214), width=3)
    c.text((W / 2, top + 104 + 145), "czy", "db", 24, (90, 96, 106), anchor="mm")
    c.block(t["foot"], "sb", 31, 866, 980, INK5, max_lines=1)
    c.button(P["cta"], W / 2, 978, size=40, fill=p["btn"])
    return c


def sc_pl_flatlay(c):
    """Вид сверху на стол: смартфон без логотипа, лист «harmonogram spłat» с сетками 12 и 24, калькулятор, ручка, кофе."""
    S.wood(c, (0, 0, W, W), (214, 172, 126), (196, 150, 104), lines=14, seed=21)

    def phone(t_, w, h):
        t_.rect((0, 0, w, h), fill=(28, 30, 36), r=44)
        t_.rect((12, 12, w - 12, h - 12), fill=(246, 246, 250), r=34)
        t_.rect((w / 2 - 40, 22, w / 2 + 40, 40), fill=(28, 30, 36), r=9)
        t_.text((30, 76), "Raty", "db", 30, INK5)
        t_.rect((30, 120, w - 30, 172), fill=(232, 228, 250), r=26)
        t_.rect((34, 124, w / 2 - 2, 168), fill=VIO5, r=22)
        t_.text(((34 + w / 2) / 2, 146), "12", "db", 24, WH, anchor="mm")
        t_.text((w * 0.75 - 6, 146), "24", "db", 24, VIO5, anchor="mm")
        for k in range(5):
            yy = 200 + k * 58
            t_.rect((30, yy, w - 30, yy + 44), fill=WH, r=12)
            t_.rect((44, yy + 14, 44 + (w - 120) * (0.8 - 0.1 * (k % 3)), yy + 28), fill=(214, 216, 226), r=6)
        t_.rect((30, h - 90, w - 30, h - 40), fill=YEL5, r=14)
        t_.text((w / 2, h - 65), "? zł", "db", 26, INK5, anchor="mm")
    subcanvas(c, (70, 430, 350, 1000), 7, phone, paper=(28, 30, 36), shadow=110, r=44)

    def sheet(t_, w, h):
        t_.text((30, 26), "HARMONOGRAM SPŁAT", "db", 26, INK5)
        t_.line([(30, 66), (w - 30, 66)], (200, 204, 214), 2)
        yy = 86
        for lab, n, cols, col in (("12 rat", 12, 6, (70, 150, 230)), ("24 raty", 24, 8, VIO5)):
            t_.text((30, yy), lab, "db", 24, col)
            t_.text((w - 30, yy), "razem: ? zł", "sb", 22, (90, 92, 104), anchor="ra")
            yy += 40
            cwid = (w - 60 - (cols - 1) * 6) / cols
            for k in range(n):
                q, r_ = k % cols, k // cols
                bx = 30 + q * (cwid + 6)
                by = yy + r_ * 34
                t_.rect((bx, by, bx + cwid, by + 28), fill=mix(col, WH, 0.82), r=5, outline=mix(col, WH, 0.45), width=2)
            yy += (n // cols) * 34 + 28
        t_.line([(30, h - 70), (w - 30, h - 70)], (200, 204, 214), 2)
        t_.text((30, h - 44), "RRSO · prowizja · ubezpieczenie", "sb", 21, (110, 112, 124), anchor="lm")
    subcanvas(c, (400, 440, 900, 900), -4, sheet, paper=(254, 253, 248), shadow=90)
    W3.calc_obj(c, 800, 790, 200, 270, shown="?")
    S.pen(c, 470, 1040, 700, 960, col=(40, 50, 90), w=14)
    c.circle(990, 480, 74, fill=(240, 240, 240))
    c.circle(990, 480, 58, fill=(120, 76, 44))
    c.circle(990, 480, 58, outline=(250, 250, 250), width=4)
    c.ellipse((960, 452, 1000, 472), fill=(170, 120, 80))


def pl_scene(P, t):
    p = P["pal"]
    c = C(WH)
    sc_pl_flatlay(c)
    box = (50, 36, 1030, 350)
    c.shadow(box, r=26, alpha=110, blur=18, off=(0, 10))
    c.rect(box, fill=WH, r=26)
    c.rect((box[0], box[1], box[0] + 16, box[3]), fill=VIO5, r=8)
    y = c.block(t["title"], "db", 56, box[1] + 34, 900, INK5, max_lines=2, gap=1.06)
    c.block(t["sub"], "s", 30, y + 8, 900, (80, 84, 104), max_lines=1)
    c.button(P["cta"], W / 2, box[3] + 4, size=40, fill=p["btn"], outline=WH)
    return c


PACKS[5] = dict(
    doc="P60-phone-installments-pl-2026-09-30", cta="Dowiedz się więcej",
    pal=dict(bg=(247, 246, 253), bg2=(232, 230, 248), btn=RED5),
    a=dict(fn=pl_ways, title="Telefon na raty 2026:", title2="która droga?",
           sub="Porównanie po RRSO i całkowitej kwocie do zapłaty",
           cards=[("w5_shop", "Raty w sklepie", "spłata zwykle od 12 do 24 miesięcy", (252, 234, 230)),
                  ("w5_tower_phone", "Telefon u operatora", "raty razem z abonamentem, najczęściej 24 miesiące", (228, 238, 252)),
                  ("w5_online_loan", "Kredyt gotówkowy online", "pieniądze na konto, zakup w dowolnym miejscu", (232, 246, 236))],
           text="Telefon na raty 2026: / która droga? / Porównanie po RRSO i całkowitej kwocie do zapłaty / 1 Raty w sklepie – spłata "
                "zwykle od 12 do 24 miesięcy / 2 Telefon u operatora – raty razem z abonamentem, najczęściej 24 miesiące / 3 Kredyt "
                "gotówkowy online – pieniądze na konto, zakup w dowolnym miejscu (у каждой карточки «Dowiedz się więcej →»)",
           note="3 карточки-пути (магазин без вывески, мачта связи + телефон, ноутбук с переводом на счёт); опора — раздел «Trzy drogi: "
                "sklep, operator, kredyt gotówkowy»; без брендов операторов, магазинов и телефонов, без сумм, «0%», «bez BIK», "
                "отложенного платежа"),
    b=dict(fn=pl_contract, title="Telefon na raty:", title2="8 rzeczy do sprawdzenia w umowie",
           tag="CHECKLISTA UMOWY", step="Punkt 3 z 8",
           items=[("RRSO", "done"), ("Całkowita kwota do zapłaty", "done"), ("Ubezpieczenie: obowiązkowe czy dobrowolne?", "now"),
                  ("Prawo do odstąpienia w ciągu 14 dni", "todo"), ("Zasady wcześniejszej spłaty", "todo")],
           opts=["Obowiązkowe", "Dobrowolne", "Nie wiem"], more="…i 3 kolejne punkty",
           pal=dict(bg=(64, 44, 150), bg2=(34, 24, 90)),
           text="Telefon na raty: / 8 rzeczy do sprawdzenia w umowie / CHECKLISTA UMOWY · Punkt 3 z 8 (прогресс 3/8) / ✓ RRSO / "
                "✓ Całkowita kwota do zapłaty / 3 Ubezpieczenie: obowiązkowe czy dobrowolne? – Obowiązkowe / Dobrowolne / Nie wiem / "
                "4 Prawo do odstąpienia w ciągu 14 dni / 5 Zasady wcześniejszej spłaty / …i 3 kolejne punkty / кнопка «Dowiedz się więcej →»",
           note="фиолетовый фон, карточка-чек-лист договора: 2 пункта отмечены, пункт 3 раскрыт с 3 вариантами ответа; опора — раздел "
                "«Co sprawdzić w umowie przed podpisaniem» (8 пунктов); без цифр стоимости и платежей"),
    c=dict(fn=pl_calendars, title="12 czy 24 raty?", sub="Co zmienia się w całkowitej kwocie do zapłaty",
           cols=[("12 RAT", 12, 4, "wyższa", (60, 140, 220)), ("24 RATY", 24, 6, "niższa", VIO5)],
           rata_lab="Rata:", total_lab="Całkowita kwota do zapłaty:",
           foot="O koszcie decyduje całkowita kwota, nie sama rata",
           pal=dict(bg=(248, 247, 253), bg2=(234, 232, 248)),
           text="12 czy 24 raty? / Co zmienia się w całkowitej kwocie do zapłaty / 12 RAT: сетка из 12 клеток 1–12 · Rata: wyższa · "
                "Całkowita kwota do zapłaty: ? zł / czy / 24 RATY: сетка из 24 клеток 1–24 · Rata: niższa · Całkowita kwota do zapłaty: "
                "? zł / O koszcie decyduje całkowita kwota, nie sama rata / кнопка «Dowiedz się więcej →»",
           note="две колонки-сетки платежей 12 и 24, «rata wyższa / niższa» и «Całkowita kwota: ? zł» в обеих; цифры примера статьи "
                "(250/150 zł, 3060/3600 zł) не вынесены; опора — раздел «12 czy 24 raty: ile kosztuje w sumie» и лид"),
    d=dict(fn=pl_scene, title="Telefon na raty: ile naprawdę kosztuje w sumie?", sub="Co sprawdzić przed podpisaniem umowy",
           text="Telefon na raty: ile naprawdę kosztuje w sumie? / Co sprawdzić przed podpisaniem umowy / кнопка «Dowiedz się więcej →» / "
                "на телефоне: Raty · 12 | 24 · ? zł / на листе: HARMONOGRAM SPŁAT · 12 rat – razem: ? zł · 24 raty – razem: ? zł · "
                "RRSO · prowizja · ubezpieczenie / на калькуляторе: ?",
           note="вид сверху на стол: смартфон без логотипа с переключателем 12/24, лист «harmonogram spłat» с сетками 12 и 24 клеток, "
                "калькулятор «?», ручка, кофе; карточка сверху = заголовок статьи + вопрос «ile naprawdę kosztuje»; опора — лид, разделы "
                "«12 czy 24 raty» и «Co sprawdzić w umowie»"),
)


# =====================================================================  сборка
def build(n, letters="abcd"):
    P = PACKS[n]
    doc = P["doc"]
    items = []
    for Lt in "abcd":
        t = P[Lt]
        PPk = dict(P, pal={**P["pal"], **t.get("pal", {})})
        if Lt in letters:
            c = t["fn"](PPk, t)
            c.save(f"{doc}/{Lt}.png")
        items.append(dict(letter=Lt, file=f"cr/packs/{doc}/{Lt}.png", concept=CONCEPT[Lt] + " — " + t["note"],
                          text=t["text"], cta=P["cta"]))
    os.makedirs(os.path.join(OUT, doc), exist_ok=True)
    with open(os.path.join(OUT, doc, "creatives.json"), "w", encoding="utf-8") as f:
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
