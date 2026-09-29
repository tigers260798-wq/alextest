"""Волна 4 «Готово к заливу» 30.09 (креативщик w4): 5 US-пакетов × 4 статики 1:1, Pillow. Запуск:
    python3 w4_us.py            — все пакеты
    python3 w4_us.py 2 4        — пакеты 2 и 4
    python3 w4_us.py 3:a,c      — пакет 3, буквы a и c
    python3 w4_us.py icons      — лист новых иконок (scratch, для проверки)
Пишет <OUT>/<docId>/<a|b|c|d>.png и <OUT>/<docId>/creatives.json.
Движок — w3_packs (иконки/сцены волн 1–3, шаблоны p60_templates grid/quiz/compare, w2b_layouts scene_d/price_tag);
w3_packs не меняется, всё новое — в этом файле.
Тексты на картинках — только из карточек article_drafts/<docId> (headline, text, adPosts, gaps «что статья раскрывает»).
Здоровье: без вопросов/утверждений о состоянии зрителя, без обещаний результата, без «free»/«covered» без условия,
без до/после, без «near me», без эмблем Medicare/CMS/IRS и брендов. Налоги: не от имени налоговой, без обещаний возврата."""
import json
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import w3_packs as W3  # noqa: E402  (регистрирует иконки и сцены волн 1–3)
from p60_lib import C, W, OUT, mix, rotpts  # noqa: E402
import p60_icons as I  # noqa: E402
import p60_scenes as S  # noqa: E402
import p60_templates as T  # noqa: E402
import p60w2_art as A  # noqa: E402
import w2b_scenes as WS  # noqa: E402
import w2b_layouts as L  # noqa: E402

WH = (255, 255, 255)
SKIN = A.SKIN
CONCEPT = W3.CONCEPT
PACKS = {}
SCR = "/tmp/claude-0/-home-user-alextest/f5dce882-fce7-5270-9036-ca9a0fe43d5e/scratchpad/w4"


# =====================================================================  иконки (квадрат s, центр cx, cy)
def w4_cpap(c, cx, cy, s, col, bg=WH, water=(150, 200, 236), screen=(170, 226, 214), arc=True):
    """CPAP-аппарат: корпус с экраном и кнопкой, прозрачная камера увлажнителя, патрубок и начало шланга."""
    c.rect((cx - s * 0.44, cy - s * 0.16, cx + s * 0.18, cy + s * 0.32), fill=col, r=s * 0.08)
    c.rect((cx - s * 0.36, cy - s * 0.08, cx - s * 0.02, cy + s * 0.1), fill=screen, r=s * 0.03)
    c.line([(cx - s * 0.3, cy + s * 0.02), (cx - s * 0.22, cy - s * 0.02), (cx - s * 0.16, cy + s * 0.04), (cx - s * 0.08, cy - s * 0.03)], mix(col, screen, 0.3), s * 0.025)
    c.circle(cx + s * 0.08, cy + s * 0.01, s * 0.06, fill=mix(col, bg, 0.6))
    c.rect((cx - s * 0.36, cy + s * 0.18, cx + s * 0.1, cy + s * 0.22), fill=mix(col, bg, 0.3), r=s * 0.02)
    c.rect((cx + s * 0.14, cy - s * 0.1, cx + s * 0.44, cy + s * 0.32), fill=mix(water, bg, 0.35), r=s * 0.06, outline=col, width=s * 0.03)
    c.rect((cx + s * 0.17, cy + s * 0.1, cx + s * 0.41, cy + s * 0.29), fill=water, r=s * 0.04)
    c.rect((cx - s * 0.2, cy - s * 0.26, cx - s * 0.06, cy - s * 0.14), fill=col, r=s * 0.02)
    if arc:
        c.arc((cx - s * 0.13, cy - s * 0.48, cx + s * 0.27, cy - s * 0.14), 180, 300, mix(col, bg, 0.35), s * 0.07)


def w4_mask(c, cx, cy, s, col, bg=WH, cushion=(206, 226, 240), tail=True):
    """Носовая маска CPAP с оголовьем и шлангом."""
    c.arc((cx - s * 0.44, cy - s * 0.44, cx + s * 0.44, cy + s * 0.3), 200, 340, col, s * 0.05)
    c.line([(cx - s * 0.41, cy - s * 0.14), (cx - s * 0.2, cy + s * 0.02)], col, s * 0.05)
    c.line([(cx + s * 0.41, cy - s * 0.14), (cx + s * 0.2, cy + s * 0.02)], col, s * 0.05)
    c.poly([(cx, cy - s * 0.24), (cx + s * 0.24, cy + s * 0.14), (cx + s * 0.18, cy + s * 0.22), (cx - s * 0.18, cy + s * 0.22), (cx - s * 0.24, cy + s * 0.14)], cushion,
           outline=col, width=s * 0.035)
    c.poly([(cx, cy - s * 0.14), (cx + s * 0.14, cy + s * 0.1), (cx - s * 0.14, cy + s * 0.1)], mix(cushion, WH, 0.5))
    c.rect((cx - s * 0.07, cy + s * 0.2, cx + s * 0.07, cy + s * 0.3), fill=col, r=s * 0.02)
    if tail:
        c.line([(cx, cy + s * 0.3), (cx + s * 0.04, cy + s * 0.4), (cx + s * 0.2, cy + s * 0.46), (cx + s * 0.4, cy + s * 0.44)], mix(col, bg, 0.35), s * 0.07)


def w4_oral(c, cx, cy, s, col, bg=WH, tray=(206, 232, 246)):
    """Внутриротовая шина (капа) — вид сверху, подкова."""
    c.ellipse((cx - s * 0.42, cy - s * 0.4, cx + s * 0.42, cy + s * 0.44), fill=tray, outline=col, width=s * 0.05)
    c.ellipse((cx - s * 0.24, cy - s * 0.2, cx + s * 0.24, cy + s * 0.5), fill=bg, outline=col, width=s * 0.04)
    c.rect((cx - s * 0.46, cy + s * 0.14, cx + s * 0.46, cy + s * 0.5), fill=bg)
    for k in (-1, 1):
        c.rect((cx + k * s * 0.33 - s * 0.09, cy + s * 0.02, cx + k * s * 0.33 + s * 0.09, cy + s * 0.16), fill=tray, outline=col, width=s * 0.04, r=s * 0.04)
    for a in range(200, 341, 28):
        r = s * 0.33
        c.circle(cx + math.cos(math.radians(a)) * r, cy + s * 0.02 + math.sin(math.radians(a)) * r, s * 0.035, fill=mix(col, tray, 0.5))


def w4_side_sleep(c, cx, cy, s, col, bg=WH, pillow=(226, 232, 244), blanket=None):
    """Человек спит на боку: подушка, голова, одеяло."""
    blanket = blanket or mix(col, bg, 0.35)
    c.rect((cx - s * 0.46, cy - s * 0.02, cx - s * 0.1, cy + s * 0.18), fill=pillow, r=s * 0.09)
    c.circle(cx - s * 0.26, cy - s * 0.08, s * 0.13, fill=col)
    c.poly([(cx - s * 0.16, cy + s * 0.06), (cx + s * 0.12, cy - s * 0.1), (cx + s * 0.46, cy - s * 0.02), (cx + s * 0.46, cy + s * 0.22), (cx - s * 0.16, cy + s * 0.22)], blanket)
    c.rect((cx - s * 0.46, cy + s * 0.2, cx + s * 0.46, cy + s * 0.28), fill=col, r=s * 0.03)
    c.line([(cx - s * 0.1, cy + s * 0.02), (cx + s * 0.1, cy - s * 0.04)], mix(blanket, bg, 0.4), s * 0.025)
    c.text((cx + s * 0.08, cy - s * 0.34), "z", "db", s * 0.16, col, anchor="mm")
    c.text((cx + s * 0.22, cy - s * 0.42), "z", "db", s * 0.12, mix(col, bg, 0.3), anchor="mm")


def w4_scale(c, cx, cy, s, col, bg=WH, acc=(232, 88, 70)):
    """Напольные весы."""
    c.rect((cx - s * 0.38, cy - s * 0.38, cx + s * 0.38, cy + s * 0.4), fill=col, r=s * 0.12)
    c.rect((cx - s * 0.2, cy - s * 0.28, cx + s * 0.2, cy - s * 0.06), fill=bg, r=s * 0.06)
    for a in range(200, 341, 20):
        ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
        c.line([(cx + ca * s * 0.15, cy - s * 0.1 + sa * s * 0.15), (cx + ca * s * 0.12, cy - s * 0.1 + sa * s * 0.12)], col, s * 0.015)
    c.line([(cx, cy - s * 0.09), (cx + s * 0.07, cy - s * 0.22)], acc, s * 0.03)
    for k in (-1, 1):
        c.rect((cx + k * s * 0.17 - s * 0.1, cy + s * 0.04, cx + k * s * 0.17 + s * 0.1, cy + s * 0.3), fill=mix(col, bg, 0.25), r=s * 0.05)


def w4_nerve(c, cx, cy, s, col, bg=WH, acc=(232, 88, 70)):
    """Имплантируемый стимулятор: корпус-галька, электрод и импульс."""
    c.ellipse((cx - s * 0.42, cy - s * 0.3, cx + s * 0.02, cy + s * 0.1), fill=col)
    c.ellipse((cx - s * 0.34, cy - s * 0.22, cx - s * 0.06, cy + s * 0.02), fill=mix(col, bg, 0.25))
    c.line([(cx + s * 0.0, cy - s * 0.1), (cx + s * 0.14, cy - s * 0.02), (cx + s * 0.16, cy + s * 0.16), (cx + s * 0.3, cy + s * 0.3)], mix(col, bg, 0.3), s * 0.04)
    c.circle(cx + s * 0.32, cy + s * 0.32, s * 0.05, fill=col)
    pts = [(-0.44, 0.34), (-0.3, 0.34), (-0.24, 0.22), (-0.18, 0.44), (-0.12, 0.3), (-0.06, 0.34), (0.08, 0.34)]
    c.line([(cx + x * s, cy + y * s) for x, y in pts], acc, s * 0.035)


def w4_sleep_lab(c, cx, cy, s, col, bg=WH, acc=(60, 170, 150)):
    """Лаборатория сна: кровать и монитор с кривой."""
    c.rect((cx - s * 0.44, cy + s * 0.06, cx + s * 0.2, cy + s * 0.22), fill=col, r=s * 0.03)
    c.rect((cx - s * 0.44, cy - s * 0.06, cx - s * 0.38, cy + s * 0.36), fill=col, r=s * 0.02)
    c.rect((cx + s * 0.14, cy + s * 0.1, cx + s * 0.2, cy + s * 0.36), fill=col, r=s * 0.02)
    c.rect((cx - s * 0.36, cy - s * 0.02, cx - s * 0.18, cy + s * 0.06), fill=mix(col, bg, 0.6), r=s * 0.03)
    c.rect((cx + s * 0.02, cy - s * 0.44, cx + s * 0.46, cy - s * 0.1), fill=col, r=s * 0.04)
    c.rect((cx + s * 0.06, cy - s * 0.4, cx + s * 0.42, cy - s * 0.14), fill=mix(acc, bg, 0.85), r=s * 0.02)
    pts = [(0.08, -0.26), (0.16, -0.26), (0.2, -0.36), (0.25, -0.18), (0.3, -0.3), (0.34, -0.26), (0.4, -0.26)]
    c.line([(cx + x * s, cy + y * s) for x, y in pts], acc, s * 0.025)
    c.rect((cx + s * 0.22, cy - s * 0.1, cx + s * 0.26, cy + s * 0.06), fill=col)


def w4_home_kit(c, cx, cy, s, col, bg=WH, acc=(60, 170, 150), moon=(250, 206, 90)):
    """Домашний тест сна: небольшой прибор на ремешке с датчиком на палец, луна."""
    c.rect((cx - s * 0.44, cy + s * 0.06, cx + s * 0.44, cy + s * 0.16), fill=mix(col, bg, 0.4), r=s * 0.05)
    c.rect((cx - s * 0.2, cy - s * 0.14, cx + s * 0.2, cy + s * 0.3), fill=col, r=s * 0.08)
    c.rect((cx - s * 0.13, cy - s * 0.07, cx + s * 0.13, cy + s * 0.08), fill=mix(acc, bg, 0.8), r=s * 0.03)
    c.line([(cx - s * 0.1, cy), (cx - s * 0.04, cy), (cx - s * 0.01, cy - s * 0.05), (cx + s * 0.03, cy + s * 0.04), (cx + s * 0.1, cy)], acc, s * 0.02)
    c.line([(cx + s * 0.2, cy + s * 0.22), (cx + s * 0.32, cy + s * 0.3), (cx + s * 0.36, cy + s * 0.4)], col, s * 0.03)
    c.rect((cx + s * 0.3, cy + s * 0.34, cx + s * 0.44, cy + s * 0.46), fill=col, r=s * 0.04)
    c.circle(cx - s * 0.26, cy - s * 0.32, s * 0.13, fill=moon)
    c.circle(cx - s * 0.2, cy - s * 0.37, s * 0.11, fill=bg)


def w4_implant_denture(c, cx, cy, s, col, bg=WH, gum=(236, 130, 140), metal=(160, 170, 184)):
    """Протез на имплантах: дуга зубов на 4 штифтах."""
    for x in (-0.3, -0.1, 0.1, 0.3):
        px = cx + x * s
        c.poly([(px - s * 0.05, cy + s * 0.06), (px + s * 0.05, cy + s * 0.06), (px + s * 0.03, cy + s * 0.44), (px - s * 0.03, cy + s * 0.44)], metal)
        for k in range(4):
            y = cy + s * (0.14 + k * 0.08)
            c.line([(px - s * 0.055, y), (px + s * 0.055, y + s * 0.02)], mix(metal, (0, 0, 0), 0.3), s * 0.018)
    c.rect((cx - s * 0.46, cy - s * 0.1, cx + s * 0.46, cy + s * 0.08), fill=gum, r=s * 0.06)
    for i in range(7):
        x = cx - s * 0.38 + i * s * 0.127
        c.rect((x - s * 0.055, cy - s * 0.34, x + s * 0.055, cy - s * 0.06), fill=WH, r=s * 0.04, outline=col, width=s * 0.02)


def w4_glucometer(c, cx, cy, s, col, bg=WH, screen=(200, 232, 220), strip=(236, 236, 240)):
    """Глюкометр с вставленной тест-полоской (без цифр)."""
    c.rect((cx - s * 0.05, cy - s * 0.48, cx + s * 0.07, cy - s * 0.26), fill=strip, outline=mix(col, bg, 0.4), width=s * 0.015, r=s * 0.01)
    c.rect((cx - s * 0.03, cy - s * 0.46, cx + s * 0.05, cy - s * 0.42), fill=(232, 88, 70), r=s * 0.01)
    c.rect((cx - s * 0.26, cy - s * 0.3, cx + s * 0.28, cy + s * 0.44), fill=col, r=s * 0.12)
    c.rect((cx - s * 0.18, cy - s * 0.2, cx + s * 0.2, cy + s * 0.08), fill=screen, r=s * 0.04)
    c.rect((cx - s * 0.12, cy - s * 0.12, cx + s * 0.06, cy - s * 0.02), fill=mix(col, screen, 0.55), r=s * 0.02)
    c.rect((cx - s * 0.12, cy + s * 0.0, cx + s * 0.13, cy + s * 0.03), fill=mix(col, screen, 0.7), r=s * 0.01)
    for k in (-1, 1):
        c.circle(cx + k * s * 0.1, cy + s * 0.24, s * 0.06, fill=mix(col, bg, 0.45))


def w4_strips(c, cx, cy, s, col, bg=WH, strip=(248, 248, 250), acc=(232, 88, 70)):
    """Коробка тест-полосок с выглядывающими полосками."""
    for k, dx in enumerate((-0.14, -0.04, 0.06, 0.16)):
        x = cx + dx * s
        top = cy - s * (0.44 - (k % 2) * 0.06)
        c.rect((x - s * 0.035, top, x + s * 0.035, cy - s * 0.1), fill=strip, outline=mix(col, bg, 0.3), width=s * 0.012, r=s * 0.01)
        c.rect((x - s * 0.025, top + s * 0.02, x + s * 0.025, top + s * 0.06), fill=acc, r=s * 0.008)
    c.rect((cx - s * 0.34, cy - s * 0.16, cx + s * 0.34, cy + s * 0.44), fill=col, r=s * 0.05)
    c.rect((cx - s * 0.34, cy - s * 0.16, cx + s * 0.34, cy - s * 0.06), fill=mix(col, (0, 0, 0), 0.2), r=s * 0.05)
    c.rect((cx - s * 0.22, cy + s * 0.04, cx + s * 0.22, cy + s * 0.3), fill=mix(col, bg, 0.82), r=s * 0.04)
    for k in range(3):
        c.rect((cx - s * 0.15, cy + s * (0.09 + k * 0.07), cx + s * (0.15 - k * 0.07), cy + s * (0.12 + k * 0.07)), fill=col, r=s * 0.01)


def w4_lancet(c, cx, cy, s, col, bg=WH, acc=(80, 170, 220)):
    """Ручка-скарификатор (без иглы на виду)."""
    body = rotpts([(cx - s * 0.1, cy - s * 0.44), (cx + s * 0.1, cy - s * 0.44), (cx + s * 0.1, cy + s * 0.22), (cx + s * 0.05, cy + s * 0.4), (cx - s * 0.05, cy + s * 0.4), (cx - s * 0.1, cy + s * 0.22)], cx, cy, 35)
    c.poly(body, col)
    cap = rotpts([(cx - s * 0.1, cy + s * 0.14), (cx + s * 0.1, cy + s * 0.14), (cx + s * 0.1, cy + s * 0.22), (cx + s * 0.05, cy + s * 0.4), (cx - s * 0.05, cy + s * 0.4), (cx - s * 0.1, cy + s * 0.22)], cx, cy, 35)
    c.poly(cap, acc)
    btn = rotpts([(cx - s * 0.06, cy - s * 0.5), (cx + s * 0.06, cy - s * 0.5), (cx + s * 0.06, cy - s * 0.42), (cx - s * 0.06, cy - s * 0.42)], cx, cy, 35)
    c.poly(btn, mix(col, bg, 0.4))
    clip = rotpts([(cx + s * 0.1, cy - s * 0.3), (cx + s * 0.16, cy - s * 0.3), (cx + s * 0.16, cy - s * 0.04), (cx + s * 0.1, cy - s * 0.04)], cx, cy, 35)
    c.poly(clip, mix(col, bg, 0.3))


def w4_cgm(c, cx, cy, s, col, bg=WH, acc=(80, 170, 220)):
    """Датчик непрерывного мониторинга глюкозы (диск) и сигнал на телефон."""
    c.circle(cx - s * 0.1, cy + s * 0.08, s * 0.3, fill=mix(col, bg, 0.85), outline=col, width=s * 0.04)
    c.circle(cx - s * 0.1, cy + s * 0.08, s * 0.17, fill=col)
    c.circle(cx - s * 0.1, cy + s * 0.08, s * 0.05, fill=mix(col, bg, 0.6))
    for r in (0.12, 0.2, 0.28):
        c.arc((cx + s * 0.18 - s * r, cy - s * 0.26 - s * r, cx + s * 0.18 + s * r, cy - s * 0.26 + s * r), 280, 350, acc, s * 0.035)


def w4_shoe(c, cx, cy, s, col, bg=WH, sole=(60, 60, 70)):
    """Ботинок (терапевтическая обувь) в профиль."""
    c.poly([(cx - s * 0.4, cy - s * 0.3), (cx - s * 0.12, cy - s * 0.3), (cx - s * 0.08, cy - s * 0.06), (cx + s * 0.22, cy + s * 0.02), (cx + s * 0.42, cy + s * 0.12),
            (cx + s * 0.44, cy + s * 0.24), (cx - s * 0.42, cy + s * 0.24)], col)
    c.rect((cx - s * 0.44, cy + s * 0.22, cx + s * 0.46, cy + s * 0.34), fill=sole, r=s * 0.05)
    for k in range(3):
        x = cx - s * (0.06 - k * 0.09)
        c.line([(x, cy - s * 0.04 + k * s * 0.02), (x + s * 0.06, cy + s * 0.06 + k * s * 0.02)], mix(col, bg, 0.6), s * 0.025)
    c.rect((cx - s * 0.4, cy - s * 0.34, cx - s * 0.1, cy - s * 0.26), fill=mix(col, (0, 0, 0), 0.2), r=s * 0.03)


def _roofhouse(c, cx, cy, s, col, bg=WH):
    c.poly([(cx - s * 0.44, cy - s * 0.02), (cx, cy - s * 0.42), (cx + s * 0.44, cy - s * 0.02)], col)
    c.rect((cx - s * 0.32, cy - s * 0.06, cx + s * 0.32, cy + s * 0.4), fill=col)
    c.rect((cx - s * 0.08, cy + s * 0.16, cx + s * 0.08, cy + s * 0.4), fill=bg)


def w4_house_down(c, cx, cy, s, col, bg=WH, acc=(40, 150, 90)):
    """Льгота на основное жильё: дом и стрелка вниз (облагаемая стоимость меньше)."""
    _roofhouse(c, cx - s * 0.08, cy, s * 0.9, col, bg)
    c.circle(cx + s * 0.28, cy + s * 0.2, s * 0.18, fill=acc, outline=bg, width=s * 0.04)
    c.line([(cx + s * 0.28, cy + s * 0.1), (cx + s * 0.28, cy + s * 0.3)], bg, s * 0.05)
    c.poly([(cx + s * 0.19, cy + s * 0.22), (cx + s * 0.37, cy + s * 0.22), (cx + s * 0.28, cy + s * 0.32)], bg)


def w4_house_lock(c, cx, cy, s, col, bg=WH, acc=(236, 164, 48)):
    """Заморозка оценки: дом и замок."""
    _roofhouse(c, cx - s * 0.08, cy, s * 0.9, col, bg)
    lx, ly = cx + s * 0.28, cy + s * 0.22
    c.rect((lx - s * 0.2, ly - s * 0.3, lx + s * 0.2, ly + s * 0.2), fill=bg, r=s * 0.06)
    c.arc((lx - s * 0.1, ly - s * 0.24, lx + s * 0.1, ly - s * 0.04), 180, 360, acc, s * 0.045)
    for k in (-1, 1):
        c.line([(lx + k * s * 0.1, ly - s * 0.14), (lx + k * s * 0.1, ly - s * 0.08)], acc, s * 0.045)
    c.rect((lx - s * 0.16, ly - s * 0.1, lx + s * 0.16, ly + s * 0.16), fill=acc, r=s * 0.04)
    c.circle(lx, ly + s * 0.02, s * 0.035, fill=bg)


def w4_breaker(c, cx, cy, s, col, bg=WH, acc=(232, 88, 70)):
    """«Circuit breaker»: доля дохода (круговая диаграмма) и потолок налога."""
    c.circle(cx - s * 0.06, cy + s * 0.04, s * 0.36, fill=mix(col, bg, 0.75))
    c.pie((cx - s * 0.42, cy - s * 0.32, cx + s * 0.3, cy + s * 0.4), 270, 340, acc)
    c.circle(cx - s * 0.06, cy + s * 0.04, s * 0.36, outline=col, width=s * 0.04)
    c.line([(cx + s * 0.16, cy - s * 0.4), (cx + s * 0.46, cy - s * 0.4)], col, s * 0.05)
    c.line([(cx + s * 0.31, cy - s * 0.4), (cx + s * 0.31, cy - s * 0.24)], col, s * 0.04)
    c.poly([(cx + s * 0.24, cy - s * 0.26), (cx + s * 0.38, cy - s * 0.26), (cx + s * 0.31, cy - s * 0.17)], col)


def w4_house_clock(c, cx, cy, s, col, bg=WH, acc=(236, 164, 48)):
    """Отсрочка: дом и часы («позже»)."""
    _roofhouse(c, cx - s * 0.08, cy, s * 0.9, col, bg)
    kx, ky = cx + s * 0.28, cy + s * 0.2
    c.circle(kx, ky, s * 0.19, fill=acc, outline=bg, width=s * 0.04)
    c.line([(kx, ky), (kx, ky - s * 0.1)], bg, s * 0.035)
    c.line([(kx, ky), (kx + s * 0.08, ky + s * 0.03)], bg, s * 0.035)


def w4_age65(c, cx, cy, s, col, bg=WH):
    c.circle(cx, cy, s * 0.42, fill=col)
    c.circle(cx, cy, s * 0.34, outline=bg, width=s * 0.025)
    c.text((cx, cy + s * 0.01), "65+", "db", s * 0.23, bg, anchor="mm")


def w4_under65(c, cx, cy, s, col, bg=WH):
    c.circle(cx, cy, s * 0.42, fill=col)
    c.circle(cx, cy, s * 0.34, outline=bg, width=s * 0.025)
    c.text((cx, cy + s * 0.01), "<65", "db", s * 0.22, bg, anchor="mm")


def w4_pharmacy(c, cx, cy, s, col, bg=WH, awn=(40, 150, 110)):
    """Аптека: витрина с полосатым навесом и знаком Rx."""
    c.rect((cx - s * 0.4, cy - s * 0.2, cx + s * 0.4, cy + s * 0.42), fill=col, r=s * 0.03)
    for k in range(5):
        x0 = cx - s * 0.44 + k * s * 0.176
        c.poly([(x0, cy - s * 0.3), (x0 + s * 0.176, cy - s * 0.3), (x0 + s * 0.176, cy - s * 0.14), (x0, cy - s * 0.14)], awn if k % 2 == 0 else WH)
    c.rect((cx - s * 0.44, cy - s * 0.44, cx + s * 0.44, cy - s * 0.3), fill=col, r=s * 0.03)
    c.text((cx, cy - s * 0.37), "Rx", "db", s * 0.12, WH, anchor="mm")
    c.rect((cx - s * 0.32, cy - s * 0.06, cx - s * 0.04, cy + s * 0.2), fill=mix(col, bg, 0.8), r=s * 0.02)
    c.rect((cx + s * 0.04, cy - s * 0.06, cx + s * 0.3, cy + s * 0.42), fill=mix(col, bg, 0.6), r=s * 0.02)
    c.circle(cx + s * 0.09, cy + s * 0.2, s * 0.02, fill=col)


def w4_doctor(c, cx, cy, s, col, bg=WH, acc=(232, 88, 70)):
    """Кабинет врача: стетоскоп."""
    s = s * 0.86
    cy = cy + s * 0.04
    c.arc((cx - s * 0.36, cy - s * 0.46, cx + s * 0.08, cy + s * 0.04), 0, 180, col, s * 0.06)
    for x in (cx - s * 0.36, cx + s * 0.08):
        c.line([(x, cy - s * 0.44), (x, cy - s * 0.2)], col, s * 0.06)
        c.circle(x, cy - s * 0.46, s * 0.05, fill=col)
    c.line([(cx - s * 0.14, cy + s * 0.04), (cx - s * 0.14, cy + s * 0.2)], col, s * 0.06)
    c.arc((cx - s * 0.14, cy - s * 0.02, cx + s * 0.3, cy + s * 0.42), 90, 180, col, s * 0.06)
    c.arc((cx + s * 0.02, cy - s * 0.02, cx + s * 0.32, cy + s * 0.42), 0, 90, col, s * 0.06)
    c.line([(cx + s * 0.32, cy + s * 0.2), (cx + s * 0.32, cy + s * 0.0)], col, s * 0.06)
    c.circle(cx + s * 0.32, cy - s * 0.06, s * 0.14, fill=col)
    c.circle(cx + s * 0.32, cy - s * 0.06, s * 0.07, fill=acc)


def w4_clinic(c, cx, cy, s, col, bg=WH, acc=(232, 88, 70)):
    """Клиника: здание с крестом."""
    c.rect((cx - s * 0.4, cy - s * 0.24, cx + s * 0.4, cy + s * 0.42), fill=col, r=s * 0.03)
    c.rect((cx - s * 0.16, cy - s * 0.44, cx + s * 0.16, cy - s * 0.2), fill=col, r=s * 0.03)
    c.rect((cx - s * 0.03, cy - s * 0.4, cx + s * 0.03, cy - s * 0.24), fill=acc)
    c.rect((cx - s * 0.08, cy - s * 0.35, cx + s * 0.08, cy - s * 0.29), fill=acc)
    for i in range(3):
        for j in range(2):
            x = cx - s * 0.28 + i * s * 0.2
            y = cy - s * 0.12 + j * s * 0.18
            if (i, j) != (1, 1):
                c.rect((x - s * 0.05, y - s * 0.05, x + s * 0.09, y + s * 0.07), fill=mix(col, bg, 0.75), r=s * 0.01)
    c.rect((cx - s * 0.08, cy + s * 0.18, cx + s * 0.08, cy + s * 0.42), fill=mix(col, bg, 0.6), r=s * 0.02)


def w4_pill_plan(c, cx, cy, s, col, bg=WH, acc=(40, 150, 110)):
    """План лекарств: карточка плана и таблетка."""
    c.rect((cx - s * 0.42, cy - s * 0.28, cx + s * 0.3, cy + s * 0.2), fill=col, r=s * 0.06)
    c.rect((cx - s * 0.34, cy - s * 0.18, cx - s * 0.1, cy - s * 0.04), fill=mix(col, bg, 0.7), r=s * 0.02)
    c.rect((cx - s * 0.34, cy + s * 0.04, cx + s * 0.16, cy + s * 0.09), fill=mix(col, bg, 0.5), r=s * 0.02)
    pill = rotpts([(cx + s * 0.06, cy + s * 0.14), (cx + s * 0.44, cy + s * 0.14), (cx + s * 0.44, cy + s * 0.34), (cx + s * 0.06, cy + s * 0.34)], cx + s * 0.25, cy + s * 0.24, -30)
    c.poly(pill, WH)
    c.line(pill + [pill[0]], col, s * 0.02)
    half = rotpts([(cx + s * 0.25, cy + s * 0.14), (cx + s * 0.44, cy + s * 0.14), (cx + s * 0.44, cy + s * 0.34), (cx + s * 0.25, cy + s * 0.34)], cx + s * 0.25, cy + s * 0.24, -30)
    c.poly(half, acc)


def w4_no_cover(c, cx, cy, s, col, bg=WH):
    """Без страховки: кошелёк."""
    c.rect((cx - s * 0.42, cy - s * 0.26, cx + s * 0.38, cy + s * 0.34), fill=col, r=s * 0.08)
    c.rect((cx - s * 0.38, cy - s * 0.36, cx + s * 0.22, cy - s * 0.2), fill=mix(col, bg, 0.5), r=s * 0.04)
    c.rect((cx + s * 0.1, cy - s * 0.06, cx + s * 0.44, cy + s * 0.14), fill=mix(col, (0, 0, 0), 0.2), r=s * 0.05)
    c.circle(cx + s * 0.24, cy + s * 0.04, s * 0.04, fill=bg)


def w4_id_card(c, cx, cy, s, col, bg=WH):
    c.rect((cx - s * 0.44, cy - s * 0.28, cx + s * 0.44, cy + s * 0.28), fill=col, r=s * 0.06)
    c.circle(cx - s * 0.22, cy - s * 0.04, s * 0.1, fill=mix(col, bg, 0.7))
    c.rect((cx - s * 0.34, cy + s * 0.06, cx - s * 0.1, cy + s * 0.18), fill=mix(col, bg, 0.7), r=s * 0.05)
    for k in range(3):
        c.rect((cx + s * 0.0, cy - s * 0.14 + k * s * 0.12, cx + s * (0.34 - k * 0.08), cy - s * 0.09 + k * s * 0.12), fill=mix(col, bg, 0.6), r=s * 0.02)


W4_ICONS = {k: v for k, v in dict(globals()).items() if k.startswith("w4_") and callable(v)}
I.ICONS.update(W4_ICONS)


def icon_sheet():
    names = list(W4_ICONS)
    c = C((244, 244, 246))
    n = 5
    for k, nm in enumerate(names):
        x = 110 + (k % n) * 215
        y = 110 + (k // n) * 200
        c.circle(x, y, 86, fill=WH)
        I.ICONS[nm](c, x, y, 120, (30, 50, 90), bg=WH)
        c.text((x, y + 96), nm[3:], "s", 18, (60, 60, 60), anchor="mm")
    os.makedirs(SCR, exist_ok=True)
    p = os.path.join(SCR, "w4_icons.png")
    c.im.convert("RGB").resize((W, W)).save(p)
    print(p)


# =====================================================================  мелкие помощники
def sheet_list(c, box, ang, head, rows, head_col=(30, 40, 70), ok=(40, 150, 90), q=(232, 140, 40), size=26, paper=WH,
               ink=(40, 44, 54), line=(206, 210, 218)):
    """Лист с заголовком и читаемыми строками; rows = [(текст, 'ok' | 'q' | None)]. Поворот ang вокруг центра."""
    from PIL import Image
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    t = C(paper, K=c.K)
    t.im = Image.new("RGBA", (c.s(w), c.s(h)), paper + (255,))
    t.text((28, 24), head, "db", size + 2, head_col)
    hy = 24 + (size + 2) * 1.2 + 10
    t.line([(28, hy), (w - 28, hy)], line, 3)
    y = hy + 12
    step = (h - y - 18) / len(rows)
    for txt, mark in rows:
        cy = y + step / 2
        if mark == "ok":
            t.circle(46, cy, 15, fill=ok)
            t.check(38, cy - 8, 16, WH, 4)
        elif mark == "q":
            t.circle(46, cy, 15, fill=q)
            t.text((46, cy + 1), "?", "db", 20, WH, anchor="mm")
        else:
            t.circle(46, cy, 7, fill=head_col)
        t.text((74, cy), txt, "sb", size, ink if mark != "q" else mix(ink, WH, 0.25), anchor="lm")
        y += step
    rot = t.im.rotate(-ang, expand=True, resample=Image.BICUBIC)
    cx, cy = c.s((x0 + x1) / 2), c.s((y0 + y1) / 2)
    sh = Image.new("RGBA", rot.size, (0, 0, 0, 0))
    sh.putalpha(rot.getchannel("A").point(lambda v: v * 60 // 255))
    c.im.alpha_composite(sh, (cx - rot.width // 2 + 8 * c.K, cy - rot.height // 2 + 12 * c.K))
    c.im.alpha_composite(rot, (cx - rot.width // 2, cy - rot.height // 2))


def hose(c, pts, col=(150, 162, 180), w=20):
    """Гофрированный шланг CPAP: кубическая кривая Безье по 4 точкам pts."""
    (x0, y0), (x1, y1), (x2, y2), (x3, y3) = pts
    sm = []
    for k in range(61):
        u = k / 60
        a, b, cc, d = (1 - u) ** 3, 3 * u * (1 - u) ** 2, 3 * u * u * (1 - u), u ** 3
        sm.append((a * x0 + b * x1 + cc * x2 + d * x3, a * y0 + b * y1 + cc * y2 + d * y3))
    c.line(sm, mix(col, (0, 0, 0), 0.2), w + 4)
    c.line(sm, col, w)
    for k in range(0, len(sm) - 1, 1):
        (xa, ya), (xb, yb) = sm[k], sm[k + 1]
        dx, dy = xb - xa, yb - ya
        n = math.hypot(dx, dy) or 1
        nx, ny = -dy / n * w * 0.45, dx / n * w * 0.45
        c.line([(xa + nx, ya + ny), (xa - nx, ya - ny)], mix(col, (0, 0, 0), 0.15), 3)


def cal_card(c, box, head, head_col, body_lines, ink=(40, 40, 50), mark=None, paper=WH):
    """Лист-напоминание: цветная шапка и строки текста (body_lines = [(текст, шрифт, размер, цвет)])."""
    x0, y0, x1, y1 = box
    c.shadow(box, r=12, alpha=80, blur=12, off=(0, 8))
    c.rect(box, fill=paper, r=12)
    c.rect((x0, y0, x1, y0 + 64), fill=head_col, r=12)
    c.rect((x0, y0 + 40, x1, y0 + 64), fill=head_col)
    for k in range(4):
        xx = x0 + 40 + k * (x1 - x0 - 80) / 3
        c.rect((xx - 4, y0 - 14, xx + 4, y0 + 14), fill=(150, 150, 160), r=3)
    c.text(((x0 + x1) / 2, y0 + 34), head, "db", c.fit(head, "db", x1 - x0 - 40, 1, 28), WH, anchor="mm")
    y = y0 + 84
    for txt, fn, sz, col in body_lines:
        sz = c.fit(txt, fn, x1 - x0 - 40, 1, sz)
        c.text(((x0 + x1) / 2, y), txt, fn, sz, col, anchor="ma")
        y += sz * 1.3


# =====================================================================  свои раскладки
def _bg(c, p):
    if p.get("bg2"):
        c.vgrad((0, 0, W, W), p["bg"], p["bg2"])


def row3(P, t):
    """Три высокие карточки-варианта: иконка, название, строка-особенность, цена, подпись, кнопка (сетка выбора)."""
    p = P["pal"]
    c = C(p["bg"])
    _bg(c, p)
    y = T.header(c, t, col=p["ink"], sub_col=p["sub"], size=t.get("size", 58), t2_col=p.get("acc"))
    top, bot = y + 30, 1046
    g = 22
    tw = (960 - 2 * g) / 3
    cards = t["cards"]
    lsz = min(c.fit(x[1], "db", tw - 36, 2, 34) for x in cards)
    psz = min(c.fit(x[2], "db", tw - 30, 1, 44) for x in cards)
    lab_h = max(len(c.wrap(x[1], c.font("db", lsz), tw - 36)) for x in cards) * c.lh("db", lsz, 1.08)
    feat_h = max(len(c.wrap(x[4], c.font("s", 27), tw - 40)) for x in cards) * c.lh("s", 27, 1.12)
    for i, (ic, lab, price, cap, feat) in enumerate(cards):
        x0 = 60 + i * (tw + g)
        box = (x0, top, x0 + tw, bot)
        cx = x0 + tw / 2
        c.card(box, fill=p["tile"], r=28, sh_alpha=60, blur=14, off=(0, 8))
        c.rect((x0, top, x0 + tw, top + 44), fill=p["acc"], r=28)
        c.rect((x0, top + 16, x0 + tw, top + 44), fill=p["tile"])
        icy = top + 140
        c.circle(cx, icy, 96, fill=p["iconbg"])
        I.ICONS[ic](c, cx, icy, 148, p["icon"], bg=p["iconbg"])
        c.block(lab, "db", lsz, icy + 124, tw - 36, p["tile_ink"], cx=cx, max_lines=2, gap=1.08)
        fy = icy + 124 + lab_h + 18
        c.block(feat, "s", 27, fy, tw - 40, p["sub"], cx=cx, max_lines=2, gap=1.12)
        dy = fy + feat_h + 28
        c.line([(x0 + 40, dy), (x0 + tw - 40, dy)], mix(p["acc"], WH, 0.7), 3)
        py = dy + 62
        c.text((cx, py), price, "db", psz, p["price"], anchor="mm")
        c.block(cap, "s", 26, py + 34, tw - 36, p["tile_ink"], cx=cx, max_lines=2)
        c.pill(P["cta"], cx, bot - 52, size=24, fill=p["btn"], padx=24, pady=12)
    return c


def gapbars(P, t):
    """Две полосы на общей шкале в $: годовой лимит против полной челюсти (сравнение)."""
    p = P["pal"]
    c = C(p["bg"])
    _bg(c, p)
    y = T.header(c, t, col=p["ink"], sub_col=p["sub"], size=t.get("size", 56), t2_col=p.get("acc"))
    box = (60, y + 30, 1020, 858)
    c.card(box, r=28, sh_alpha=60, blur=14, off=(0, 8))
    vmax = t["vmax"]
    bx0, bx1 = box[0] + 44, box[2] - 44

    def X(v):
        return bx0 + (bx1 - bx0) * v / vmax

    rows = t["gbars"]
    area_top = box[1] + 40
    axis_y = box[3] - 70
    rh = (axis_y - area_top - 10) / len(rows)
    for k, (lab, lo, hi, val, col) in enumerate(rows):
        ry = area_top + k * rh
        ly = c.block(lab, "sb", 30, ry, bx1 - bx0, (40, 44, 54), align="left", x=bx0, max_lines=2, gap=1.08)
        bt = ly + 12
        bh = 58
        c.rect((bx0, bt, bx1, bt + bh), fill=(236, 239, 243), r=14)
        c.rect((bx0, bt, max(X(lo), bx0 + 28), bt + bh), fill=col, r=14)
        # диапазон lo–hi — светлее, со штриховкой
        rb = (X(lo) - 14, bt, X(hi), bt + bh)
        c.rect(rb, fill=mix(col, WH, 0.45), r=14)
        for xx in range(int(rb[0]) + 10, int(rb[2]) - 8, 22):
            c.line([(xx, bt + bh - 6), (min(xx + 20, rb[2] - 6), bt + 6)], mix(col, WH, 0.2), 5)
        c.rect((bx0, bt, X(lo), bt + bh), fill=col, r=14)
        vs = c.fit(val, "db", bx1 - bx0, 1, 38)
        vx = X(hi) + 20
        if vx + c.tw(val, c.font("db", vs))[0] > bx1:
            c.text((bx0, bt + bh + 14), val, "db", vs, col)
        else:
            c.text((vx, bt + bh / 2), val, "db", vs, col, anchor="lm")
    c.line([(bx0, axis_y), (bx1, axis_y)], (190, 196, 206), 3)
    for v, lab in t["ticks"]:
        xx = X(v)
        c.line([(xx, axis_y - 10), (xx, axis_y + 10)], (150, 156, 166), 3)
        anc = "la" if v == 0 else ("ra" if v == vmax else "ma")
        c.text((xx, axis_y + 18), lab, "s", 24, (110, 116, 126), anchor=anc)
    if t.get("foot"):
        c.block(t["foot"], "sb", 32, 880, 980, p["ink"], max_lines=2, gap=1.1)
    c.button(P["cta"], W / 2, 990, size=42, fill=p["btn"])
    return c


def grid_desc(P, t):
    """Сетка 2×2: иконка, название, строка-пояснение из статьи, кнопка на каждой плитке."""
    p = P["pal"]
    c = C(p["bg"])
    _bg(c, p)
    y = T.header(c, t, col=p["ink"], sub_col=p["sub"], size=t.get("size", 58), t2_col=p.get("acc"))
    top = y + 28
    g = 22
    tw = (960 - g) / 2
    th = (1046 - top - g) / 2
    for i, (ic, lab, desc) in enumerate(t["dtiles"]):
        x0 = 60 + (i % 2) * (tw + g)
        y0 = top + (i // 2) * (th + g)
        box = (x0, y0, x0 + tw, y0 + th)
        c.card(box, fill=p["tile"], r=26, sh_alpha=55, blur=12, off=(0, 6))
        c.circle(x0 + 78, y0 + 78, 52, fill=p["iconbg"])
        I.ICONS[ic](c, x0 + 78, y0 + 78, 78, p["icon"], bg=p["iconbg"])
        nl = len(c.wrap(lab, c.font("db", 32), tw - 170))
        c.block(lab, "db", 32, y0 + 78 - nl * 19, tw - 170, p["tile_ink"], align="left", x=x0 + 148, max_lines=2, gap=1.05)
        c.block(desc, "s", 28, y0 + 150, tw - 56, p["sub"], align="left", x=x0 + 28, max_lines=3, gap=1.12)
        pb = c.pill(P["cta"], 0, -500, size=22, fill=p["btn"], padx=22, pady=11)
        pw = pb[2] - pb[0]
        c.pill(P["cta"], x0 + 28 + pw / 2, y0 + th - 44, size=22, fill=p["btn"], padx=22, pady=11)
    return c


def list3(P, t):
    """Панель-«герой» + 3 строки-варианта (иконка, название, пояснение, кнопка справа)."""
    p = P["pal"]
    c = C(p["bg"])
    _bg(c, p)
    y = T.header(c, t, col=p["ink"], sub_col=p["sub"], size=t.get("size", 58), t2_col=p.get("acc"))
    hb = (60, y + 22, 1020, y + 22 + t.get("hero_h", 250))
    t["hero"](c, hb)
    top = hb[3] + 24
    g = 18
    rh = (1046 - top - 2 * g) / 3
    pb = c.pill(P["cta"], 0, -500, size=24, fill=p["btn"], padx=24, pady=12)
    pw = pb[2] - pb[0]
    for i, (ic, lab, desc) in enumerate(t["rows3"]):
        y0 = top + i * (rh + g)
        box = (60, y0, 1020, y0 + rh)
        c.card(box, fill=p["tile"], r=26, sh_alpha=50, blur=10, off=(0, 5))
        c.circle(60 + rh / 2 + 4, y0 + rh / 2, rh * 0.38, fill=p["iconbg"])
        I.ICONS[ic](c, 60 + rh / 2 + 4, y0 + rh / 2, rh * 0.52, p["icon"], bg=p["iconbg"])
        tx = 60 + rh + 20
        tw_ = 1020 - 24 - pw - 24 - tx
        c.block(lab, "db", 32, y0 + rh / 2 - 38, tw_, p["tile_ink"], align="left", x=tx, max_lines=1)
        c.block(desc, "s", 26, y0 + rh / 2 + 6, tw_, p["sub"], align="left", x=tx, max_lines=1)
        c.pill(P["cta"], 1020 - 24 - pw / 2, y0 + rh / 2, size=24, fill=p["btn"], padx=24, pady=12)
    return c


# =====================================================================  «герои»
def hero_diabetic(c, box):
    def fn(t):
        x0, y0, x1, y1 = box
        W3._panel(t, box, (255, 240, 222), (250, 222, 190))
        t.dots((x0 + 20, y0 + 20, x1 - 20, y1 - 20), 40, 3, (200, 120, 60), alpha=26)
        cx = (x0 + x1) / 2
        ty = y1 - 64
        t.rect((x0, ty, x1, y1), fill=(214, 170, 124))
        t.rect((x0, ty, x1, ty + 10), fill=(196, 150, 104))
        BG = (253, 232, 206)
        I.ICONS["w4_glucometer"](t, cx - 330, ty - 0.44 * 250 + 4, 250, (30, 70, 130), bg=BG)
        I.ICONS["w4_strips"](t, cx - 110, ty - 0.44 * 240 + 4, 240, (234, 128, 44), bg=BG)
        pb = (cx + 60, ty - 236, cx + 190, ty + 6)
        t.shadow(pb, r=20, alpha=70, blur=8, off=(0, 6))
        t.rect(pb, fill=(40, 44, 56), r=20)
        t.rect((pb[0] + 10, pb[1] + 14, pb[2] - 10, pb[3] - 14), fill=(236, 246, 252), r=12)
        pts = [(pb[0] + 22 + k * 11, (pb[1] + pb[3]) / 2 - 10 + math.sin(k / 1.6) * 24 - k * 1.5) for k in range(9)]
        t.line(pts, (60, 150, 220), 5)
        for k in range(3):
            t.rect((pb[0] + 22, pb[3] - 64 + k * 14, pb[2] - 22 - k * 18, pb[3] - 57 + k * 14), fill=(196, 210, 222), r=3)
        I.ICONS["w4_cgm"](t, cx + 340, ty - 0.38 * 190, 190, (30, 70, 130), bg=BG)
    S.clip_draw(c, box, 28, fn)


def hero_places(c, box):
    """Улица: аптека, кабинет врача, клиника (без вывесок брендов)."""
    def fn(t):
        x0, y0, x1, y1 = box
        t.vgrad(box, (206, 230, 246), (236, 244, 250))
        t.circle(x1 - 90, y0 + 56, 34, fill=(255, 226, 130))
        t.rect((x0, y1 - 44, x1, y1), fill=(196, 200, 208))
        t.rect((x0, y1 - 50, x1, y1 - 42), fill=(226, 228, 232))
        bw = (x1 - x0 - 80) / 3
        for k, (ic, col) in enumerate((("w4_pharmacy", (60, 50, 110)), ("w4_doctor", (0, 118, 118)), ("w4_clinic", (60, 50, 110)))):
            bx = x0 + 20 + k * (bw + 20)
            if ic == "w4_doctor":
                b = (bx + 20, y0 + 40, bx + bw - 20, y1 - 46)
                t.rect(b, fill=(250, 244, 236), r=8)
                t.poly([(b[0] - 14, b[1] + 6), ((b[0] + b[2]) / 2, b[1] - 40), (b[2] + 14, b[1] + 6)], (150, 90, 70))
                t.rect(((b[0] + b[2]) / 2 - 26, b[3] - 90, (b[0] + b[2]) / 2 + 26, b[3]), fill=(0, 118, 118), r=4)
                for wx in (b[0] + 40, b[2] - 90):
                    t.rect((wx, b[1] + 40, wx + 50, b[1] + 96), fill=(200, 226, 240), r=4)
                t.circle((b[0] + b[2]) / 2, b[1] + 64, 40, fill=WH)
                I.ICONS["w4_doctor"](t, (b[0] + b[2]) / 2, b[1] + 64, 58, (0, 118, 118), bg=WH)
            else:
                I.ICONS[ic](t, bx + bw / 2, y1 - 44 - (y1 - y0 - 60) * 0.44, (y1 - y0 - 60) * 0.98, col, bg=(236, 244, 250))
    S.clip_draw(c, box, 28, fn)


# =====================================================================  сцены (концепция d), холст 1080
def sc_cpap_bedroom(c):
    """Спальня ночью: цепочка шагов Medicare-аренды на стене, кровать, тумбочка с CPAP, шланг и маска на подставке.
    Верх (до y≈290) — белый заголовок на тёмной стене."""
    c.vgrad((0, 0, W, 860), (26, 36, 72), (58, 66, 118))
    rnd = random.Random(5)
    # шаги
    steps = [("Sleep", "test"), ("Prescription", "+ supplier"), ("12-week", "trial"), ("Up to 13", "months"), ("Then", "owned")]
    n = len(steps)
    g = 26
    cw = (980 - g * (n - 1)) / n
    fs = min(c.fit(x, "db", cw - 22, 1, 26) for st in steps for x in st)
    y0, y1 = 338, 446
    for k, (l1, l2) in enumerate(steps):
        x0 = 50 + k * (cw + g)
        last = k == n - 1
        fill = (250, 196, 80) if last else WH
        c.shadow((x0, y0, x0 + cw, y1), r=18, alpha=90, blur=8, off=(0, 5))
        c.rect((x0, y0, x0 + cw, y1), fill=fill, r=18)
        c.circle(x0 + cw / 2, y0, 20, fill=(250, 196, 80) if not last else (26, 36, 72), outline=(26, 36, 72) if not last else WH, width=3)
        c.text((x0 + cw / 2, y0 + 1), str(k + 1), "db", 22, (26, 36, 72) if not last else WH, anchor="mm")
        c.text((x0 + cw / 2, y0 + 44), l1, "db", fs, (26, 36, 72), anchor="mm")
        c.text((x0 + cw / 2, y0 + 80), l2, "db", fs, (26, 36, 72), anchor="mm")
        if k < n - 1:
            ax = x0 + cw + g / 2
            c.poly([(ax - 7, (y0 + y1) / 2 - 11), (ax + 8, (y0 + y1) / 2), (ax - 7, (y0 + y1) / 2 + 11)], (250, 196, 80))
    # окно с луной
    wb = (70, 480, 330, 700)
    c.rect((wb[0] - 12, wb[1] - 12, wb[2] + 12, wb[3] + 12), fill=(88, 96, 140), r=6)
    c.vgrad(wb, (16, 22, 50), (40, 50, 96))
    for _ in range(14):
        c.circle(rnd.uniform(wb[0] + 10, wb[2] - 10), rnd.uniform(wb[1] + 10, wb[3] - 60), rnd.uniform(1.5, 3), fill=(230, 230, 250))
    c.circle(270, 540, 28, fill=(250, 236, 180))
    c.circle(284, 530, 24, fill=(22, 30, 62))
    c.line([((wb[0] + wb[2]) / 2, wb[1]), ((wb[0] + wb[2]) / 2, wb[3])], (88, 96, 140), 10)
    # пол
    c.rect((0, 860, W, W), fill=(90, 70, 70))
    S.wood(c, (0, 866, W, W), (104, 80, 76), (88, 66, 62), lines=5, seed=9)
    # кровать слева
    c.rect((20, 600, 600, 790), fill=(120, 90, 80), r=24)
    c.rect((40, 620, 580, 780), fill=(140, 106, 92), r=18)
    c.rect((0, 760, 640, 880), fill=(236, 238, 246), r=26)
    c.rect((60, 712, 330, 790), fill=(250, 250, 252), r=34)
    c.poly([(0, 800), (620, 790), (640, 820), (640, W), (0, W)], (70, 104, 170))
    c.line([(0, 800), (620, 790)], (96, 132, 196), 16)
    for x in range(60, 620, 110):
        c.line([(x, 860), (x + 40, W)], (62, 94, 156), 4)
    # тумбочка
    c.rect((660, 712, 1060, 740), fill=(150, 108, 80), r=8)
    c.rect((680, 740, 1040, W), fill=(166, 122, 90), r=6)
    c.rect((702, 772, 1018, 870), outline=(136, 96, 70), width=4, r=6)
    c.circle(860, 820, 8, fill=(110, 80, 58))
    # лампа (у правого края)
    c.glow((860, 460, 1120, 760), (255, 220, 150), alpha=110, blur=50)
    c.rect((1036, 580, 1048, 712), fill=(70, 70, 80))
    c.ellipse((1006, 700, 1078, 716), fill=(70, 70, 80))
    c.poly([(996, 500), (1096, 500), (1110, 590), (982, 590)], (252, 222, 160))
    # CPAP, шланг и маска на подставке
    I.ICONS["w4_cpap"](c, 790, 634, 236, (44, 52, 70), bg=(240, 236, 226), arc=False)
    c.rect((934, 620, 946, 712), fill=(90, 96, 110))
    c.ellipse((912, 704, 968, 716), fill=(90, 96, 110))
    hose(c, [(760, 574), (740, 470), (930, 460), (940, 600)], col=(170, 182, 200), w=16)
    I.ICONS["w4_mask"](c, 940, 604, 104, (60, 66, 84), bg=(200, 190, 170), tail=False)


def sc_dental_desk(c):
    """Стол консультации: два письменных плана лечения рядом (один полный, в другом не хватает пунктов), ручка, очки,
    модель импланта на подставке, растение, окно с жалюзи. Рта крупным планом нет. Верх (до y≈440) — карточка."""
    c.vgrad((0, 0, W, 740), (228, 242, 242), (206, 228, 230))
    c.dots((0, 0, W, 740), 46, 3, (0, 110, 120), alpha=20)
    # окно с жалюзи справа
    WS.window(c, (760, 470, 1010, 690), sky0=(176, 214, 236), sky1=(226, 240, 248), bars=False)
    for k in range(6):
        c.rect((760, 476 + k * 36, 1010, 494 + k * 36), fill=(245, 246, 248), alpha=200)
    # полка с моделью импланта и растением
    c.rect((60, 640, 420, 656), fill=(236, 236, 232), r=4)
    c.rect((110, 600, 230, 640), fill=(90, 110, 130), r=8)
    I.ICONS["implant"](c, 170, 530, 150, (60, 80, 110), bg=(214, 232, 234))
    S.plant(c, 330, 640, 0.5, pot=(236, 120, 90))
    # стол
    c.rect((0, 740, W, W), fill=(190, 150, 110))
    S.wood(c, (0, 752, W, W), (200, 160, 118), (182, 142, 100), lines=6, seed=21)
    c.rect((0, 740, W, 756), fill=(170, 128, 90))
    sheet_list(c, (70, 770, 520, 1060), -3, "TREATMENT PLAN A",
               [("3D scans", "ok"), ("Extractions, grafting", "ok"), ("Implants, abutments", "ok"), ("Temporary teeth", "ok"), ("Final bridge", "ok")],
               head_col=(0, 100, 110))
    sheet_list(c, (560, 776, 1010, 1066), 3, "TREATMENT PLAN B",
               [("3D scans", "ok"), ("Extractions, grafting", "q"), ("Implants, abutments", "ok"), ("Temporary teeth", "q"), ("Final bridge", "ok")],
               head_col=(190, 80, 60))
    S.pen(c, 470, 1050, 560, 990)
    S.glasses(c, 540, 770, 0.7)


def sc_diabetic_kitchen(c):
    """Кухонный стол: глюкометр, коробка тест-полосок, ручка-скарификатор, телефон с кривой и датчик CGM; на стене две записки.
    Верх (до y≈420) — плашки заголовка и кнопка."""
    c.vgrad((0, 0, W, 800), (254, 246, 234), (248, 232, 210))
    # плитка-фартук
    for yy in range(470, 800, 60):
        for xx in range(-30 if (yy // 60) % 2 else 0, W, 120):
            c.rect((xx + 3, yy + 3, xx + 117, yy + 57), fill=(250, 240, 226), r=6)
    c.rect((0, 460, W, 470), fill=(236, 214, 186))
    WS.note(c, 250, 560, 330, 130, -3, (255, 226, 110), ["METER:", "a one-time buy"], size=34, font="db")
    WS.note(c, 770, 556, 360, 130, 3, (170, 220, 250), ["STRIPS:", "the ongoing cost"], size=34, font="db")
    # стол
    c.rect((0, 790, W, W), fill=(186, 138, 96))
    S.wood(c, (0, 804, W, W), (196, 148, 104), (176, 128, 88), lines=6, seed=33)
    c.rect((0, 784, W, 806), fill=(160, 114, 76))
    BG = (196, 148, 104)
    I.ICONS["w4_glucometer"](c, 200, 792, 250, (30, 70, 130), bg=BG)
    I.ICONS["w4_strips"](c, 440, 780, 230, (234, 128, 44), bg=BG)
    I.ICONS["w4_lancet"](c, 330, 930, 160, (30, 70, 130), bg=BG)
    # телефон с кривой и датчик
    pb = (640, 640, 790, 900)
    c.shadow(pb, r=22, alpha=80, blur=8, off=(0, 6))
    c.rect(pb, fill=(36, 40, 52), r=22)
    c.rect((pb[0] + 10, pb[1] + 16, pb[2] - 10, pb[3] - 16), fill=(236, 246, 252), r=14)
    pts = [(pb[0] + 22 + k * 14, (pb[1] + pb[3]) / 2 + math.sin(k / 1.7) * 30 - k * 2) for k in range(9)]
    c.line(pts, (60, 150, 220), 6)
    for k in range(3):
        c.rect((pb[0] + 22, pb[3] - 70 + k * 16, pb[2] - 22 - k * 20, pb[3] - 62 + k * 16), fill=(196, 210, 222), r=4)
    I.ICONS["w4_cgm"](c, 880, 860, 170, (30, 70, 130), bg=BG)
    WS.mug(c, 1000, 800, 0.4, (40, 150, 110))


def sc_tax_library(c):
    """Библиотека: полки, настенный лист «APPLY BY», за столом волонтёр с ноутбуком и пожилая пара с папкой;
    на столе список «что взять» и счёт налога на дом. Верх (до y≈300) — полоса заголовка. Без эмблем и бланков ведомств."""
    c.vgrad((0, 240, W, 840), (240, 234, 222), (226, 216, 198))
    for y in (300, 415, 530):
        WS.shelf_books(c, 40, y + 96, 700, seed=int(y))
        c.rect((30, y + 96, 710, y + 108), fill=(150, 108, 72), r=3)
    # лист со сроком на стене
    cal_card(c, (770, 320, 1030, 570), "PROPERTY TAX RELIEF", (26, 92, 74),
             [("APPLY BY", "db", 40, (190, 60, 50)), ("the deadline", "sb", 30, (60, 60, 70)), ("renew on time", "sb", 30, (60, 60, 70))])
    # люди
    A.seated(c, 250, 930, 1100, 560, SKIN[0], (232, 232, 236), "bun", (200, 110, 96), (70, 80, 110), arm_l=(180, 846), arm_r=(330, 842))
    A.seated(c, 440, 930, 1100, 600, SKIN[3], (214, 214, 218), "short", (70, 110, 150), (60, 64, 80), arm_l=(370, 846), arm_r=(520, 842))
    A.seated(c, 820, 930, 1100, 580, SKIN[1], (50, 36, 30), "long", (26, 92, 74), (50, 54, 70), arm_l=(740, 842), arm_r=(900, 846))
    # стол
    c.rect((0, 820, W, W), fill=(150, 108, 72))
    S.wood(c, (0, 834, W, W), (162, 118, 80), (142, 100, 66), lines=6, seed=61)
    c.rect((0, 820, W, 836), fill=(130, 90, 60))
    # ноутбук волонтёра (крышкой к зрителю)
    c.rect((730, 766, 910, 850), fill=(60, 66, 80), r=10)
    c.circle(820, 808, 10, fill=(120, 126, 140))
    c.rect((714, 846, 926, 858), fill=(80, 86, 100), r=4)
    sheet_list(c, (30, 824, 380, 1052), -3, "WHAT TO BRING",
               [("Photo ID", None), ("Income statements", None), ("Last year's return", None)], head_col=(26, 92, 74), size=25)
    S.paper(c, (724, 866, 1044, 1066), 5, head="PROPERTY TAX BILL", head_size=24, lines=5)


def sc_shingles_pharmacy(c):
    """Аптечная стойка: полки с безымянными коробками, фармацевт за стойкой, покупатель 60+ со спины,
    лист-напоминание «Dose 1 → Dose 2 in 2–6 months», телефон с напоминанием. Без шприца и брендов. Верх (до y≈300) — заголовок."""
    c.vgrad((0, 0, W, 760), (244, 240, 250), (226, 220, 240))
    # полки
    rnd = random.Random(11)
    for y in (330, 440, 550):
        c.rect((440, y + 88, 1060, y + 100), fill=(200, 200, 212), r=3)
        x = 450
        while x < 1040:
            bw = rnd.randint(34, 70)
            bh = rnd.randint(46, 84)
            col = rnd.choice([(250, 250, 252), (200, 226, 240), (230, 214, 244), (214, 236, 222), (252, 232, 214)])
            c.rect((x, y + 88 - bh, x + bw, y + 88), fill=col, r=4, outline=(180, 180, 196), width=2)
            c.rect((x + 6, y + 88 - bh + 12, x + bw - 6, y + 88 - bh + 20), fill=(170, 160, 200), r=2)
            x += bw + rnd.randint(6, 14)
    # фармацевт
    A.standing(c, 760, 1040, 640, SKIN[2], (60, 44, 36), "short", (250, 250, 252), (70, 80, 110), arm_l=(700, 770), arm_r=(820, 770))
    c.rect((736, 560, 784, 610), fill=(0, 140, 140), r=4)
    # лист-напоминание на стене слева
    cal_card(c, (60, 316, 400, 606), "SHINGLES VACCINE", (104, 60, 140),
             [("Dose 1", "db", 40, (40, 40, 50)), ("↓", "db", 34, (104, 60, 140)), ("Dose 2", "db", 40, (40, 40, 50)),
              ("in 2–6 months", "sb", 30, (190, 70, 60))])
    # стойка
    c.rect((0, 760, W, W), fill=(104, 60, 140))
    c.rect((0, 744, W, 772), fill=(236, 232, 244), r=4)
    for x in range(0, W, 180):
        c.rect((x + 10, 800, x + 170, 1060), outline=(126, 84, 162), width=4, r=10)
    # телефон с напоминанием на стойке
    pb = (560, 610, 700, 760)
    c.rect(pb, fill=(36, 40, 52), r=18)
    c.rect((pb[0] + 8, pb[1] + 12, pb[2] - 8, pb[3] - 4), fill=WH, r=10)
    c.text(((pb[0] + pb[2]) / 2, pb[1] + 44), "Reminder", "sb", 20, (104, 60, 140), anchor="mm")
    c.text(((pb[0] + pb[2]) / 2, pb[1] + 80), "Dose 2", "db", 26, (40, 40, 50), anchor="mm")
    # покупатель со спины
    WS.senior_back(c, 250, 1010, 1.25, (0, 118, 118), hair=(226, 226, 232))


SCENES = dict(w4_cpap_bedroom=sc_cpap_bedroom, w4_dental_desk=sc_dental_desk, w4_diabetic_kitchen=sc_diabetic_kitchen,
              w4_tax_library=sc_tax_library, w4_shingles_pharmacy=sc_shingles_pharmacy)
for _k, _v in SCENES.items():
    setattr(WS, _k, _v)

FN = {"grid": T.grid, "quiz": T.quiz, "compare": T.compare, "scene_d": L.scene_d, "row3": row3, "gapbars": gapbars,
      "grid_desc": grid_desc, "list3": list3, "tags": W3.gbp_tags}


# =====================================================================  ПАКЕТЫ
# ---------------------------------------------------------------- 1. US · CPAP-аппараты (товарка 60+)
NAVY1, TEAL1, AMB1 = (26, 36, 72), (0, 124, 128), (230, 132, 30)
PACKS[1] = dict(
    doc="P60-cpap-us-2026-09-30", cta="Learn more",
    pal=dict(bg=(244, 242, 252), ink=NAVY1, sub=(88, 94, 112), acc=TEAL1, btn=AMB1, tile=WH, tile_ink=NAVY1, icon=NAVY1,
             iconbg=(228, 234, 248)),
    a=dict(fn="grid", layout="2x2", title="Sleep apnea treatment without CPAP", sub="4 options a doctor may discuss – pick one:", size=58,
           tiles=[("w4_oral", "Oral appliance"), ("w4_side_sleep", "Positional therapy"), ("w4_scale", "Weight management"),
                  ("w4_nerve", "Surgery or implant")],
           pal=dict(bg=(242, 242, 252), bg2=(222, 226, 246)),
           src="раздел 6 «Sleep apnea treatment without CPAP» (4 пункта списка «a doctor may discuss»)",
           note="2×2 вариантов без CPAP ровно по списку статьи; подпись «a doctor may discuss» из текста; обещаний результата нет"),
    b=dict(fn="quiz", layout="phone", title="CPAP & Medicare quiz:", title2="rent or own?", sub="What the 12-week trial checks, and what comes next",
           size=56, tag="CPAP QUIZ", step="Question 1 of 3", prog=0.33,
           q="How long does Medicare usually rent a CPAP machine before the patient owns it?",
           opts=["3 months", "6 months", "13 months", "Not sure"],
           pal=dict(bg=(0, 96, 104), bg2=(0, 50, 60), ink=WH, sub=(200, 232, 232), acc=AMB1, btn=AMB1),
           src="раздел 4 «Is a CPAP machine covered by Medicare? The 13-month path» (ответ: до 13 месяцев)",
           note="тёмно-бирюзовый фон, телефон с тестом; вопрос о правиле Medicare, не о зрителе"),
    c=dict(fn="compare", layout="table", title="CPAP machine price 2026:", title2="$500 or $1,650?", sub="Bought without insurance – what the difference buys",
           size=54, cols=[("BASIC", "w4_cpap", TEAL1), ("AUTO-ADJUSTING", "w4_cpap", NAVY1)],
           rows=[("Pressure", "one fixed setting", "adjusts through the night"), ("Extras", "fewer", "humidifier + wireless data"),
                 ("No insurance", "about $500", "up to about $1,650")],
           foot="Plus masks, cushions, tubing and filters on a schedule",
           pal=dict(bg=(250, 248, 242), acc=AMB1),
           src="раздел 3 «CPAP machine price in 2026» ($500–1,650; basic fixed-pressure vs auto-adjusting с увлажнителем и wireless) + раздел 5 (расходники)",
           note="таблица нижний/верхний край цены; цифры — только из статьи (в gaps: сверить $500–1,650 до залива)"),
    d=dict(fn="scene_d", scene="w4_cpap_bedroom", style="top", y=40, kicker="CPAP MACHINES 2026",
           title="Rented for up to 13 months, then owned", sub="How Medicare's CPAP rental usually works, step by step",
           size=56, lines=2, btn_y=1000, btn_size=44,
           pal=dict(ink=WH, sub=(210, 216, 240), acc=(250, 196, 80), btn=AMB1),
           scene_text="1 Sleep test → 2 Prescription + supplier → 3 12-week trial → 4 Up to 13 months → 5 Then owned",
           src="раздел 4 — список шагов пути Medicare (sleep test → prescription/supplier → 12-week trial → up to 13 months → belongs to the patient); хук РК 1",
           note="ночная спальня: на стене цепочка из 5 шагов, кровать, тумбочка с CPAP, шланг, маска на подставке, лампа; людей нет"),
)

# ---------------------------------------------------------------- 2. US · протезы и импланты (стоматология 60+)
TEAL2, CORAL2, INK2 = (0, 118, 130), (226, 96, 76), (24, 40, 70)
PACKS[2] = dict(
    doc="P60-dental-implants-us-2026-09-30", cta="Learn more",
    pal=dict(bg=(240, 248, 248), ink=INK2, sub=(88, 98, 110), acc=TEAL2, btn=CORAL2, tile=WH, tile_ink=INK2, icon=INK2,
             iconbg=(222, 240, 242), price=TEAL2),
    a=dict(fn="row3", title="Replacing teeth after 60:", title2="2026 price ranges", sub="Pick an option:", size=60,
           cards=[("denture", "Denture", "$1,500–3,000", "per plate", "No surgery, but it can move"),
                  ("implant", "Implant", "$1,600–2,200", "the implant itself; crown often extra", "Surgery and months of healing"),
                  ("w4_implant_denture", "Denture on implants", "$10,000–30,000", "per arch", "More stable than a regular denture")],
           pal=dict(bg=(240, 248, 248), bg2=(222, 238, 240)),
           src="раздел 1 «Dentures and implants: how the options differ» (3 варианта) + раздел 2 «Dental implants cost in 2026» (цены)",
           note="3 карточки-варианта с диапазонами цен из статьи; у импланта подпись «сам имплант, коронка часто отдельно» — как в тексте"),
    b=dict(fn="quiz", layout="card2x2", title="Medicare dental quiz:", title2="dentures & implants", size=58,
           sub="Original Medicare vs. Medicare Advantage in 2026",
           tag="QUIZ", step="Question 1 of 3", prog=0.33,
           q="Does Original Medicare pay for dentures or implants?", opts=["Yes", "Partly", "Generally no", "Not sure"],
           pal=dict(bg=(255, 244, 238), bg2=(248, 222, 208), acc=CORAL2, t2=TEAL2, deco=True),
           src="раздел 4 «What Medicare covers, and what it does not» (ответ: как правило, нет)",
           note="персиковый фон, 4 варианта-плитки; вопрос о программе, не о зрителе"),
    c=dict(fn="gapbars", title="Medicare Advantage dental", title2="vs. a full arch of implants", sub="Typical 2026 numbers on one scale", size=56,
           vmax=30000,
           gbars=[("Yearly dental maximum in many Medicare Advantage plans", 1000, 3000, "often $1,000–3,000 a year", TEAL2),
                  ("Full arch of implant-supported teeth", 10000, 30000, "commonly $10,000–30,000 per arch", CORAL2)],
           ticks=[(0, "$0"), (10000, "$10,000"), (20000, "$20,000"), (30000, "$30,000")],
           foot="Why a plan more often pays part of a denture than a full arch",
           pal=dict(bg=(240, 248, 248), bg2=(226, 240, 242)),
           src="раздел 4 (годовой максимум Medicare Advantage $1,000–3,000; «more likely to pay for part of a denture… than for a full arch») + раздел 2 (full arch $10,000–30,000)",
           note="две полосы на общей шкале $0–30,000; без «covers implants», без рассрочки"),
    d=dict(fn="scene_d", scene="w4_dental_desk", style="card", card_box=(80, 40, 1000, 450), frame=True, font="lserb",
           kicker="DENTURES OR IMPLANTS · 2026", title="Why two implant quotes can differ by thousands",
           sub="What a full-arch price should include", size=58, lines=3, btn_size=40, btn_off=66,
           pal=dict(frame=TEAL2, ink=INK2, sub=(88, 98, 110), acc=CORAL2, btn=CORAL2),
           scene_text="TREATMENT PLAN A: 3D scans ✓ · Extractions, grafting ✓ · Implants, abutments ✓ · Temporary teeth ✓ · Final bridge ✓ / "
                      "TREATMENT PLAN B: 3D scans ✓ · Extractions, grafting ? · Implants, abutments ✓ · Temporary teeth ? · Final bridge ✓",
           src="раздел 3 «Full mouth dental implants: what the price includes» (5 пунктов сметы; «the difference is often in what is left out»)",
           note="стол консультации: два письменных плана рядом, в плане B пропущены пункты («?»), модель импланта на полке; рта и кресла нет"),
)

# ---------------------------------------------------------------- 3. US · расходники для диабета (товарка 60+)
BLUE3, ORG3, INK3 = (30, 90, 160), (228, 118, 34), (26, 38, 70)
PACKS[3] = dict(
    doc="P60-diabetic-supplies-us-2026-09-30", cta="Learn more",
    pal=dict(bg=(253, 247, 238), ink=INK3, sub=(96, 100, 110), acc=BLUE3, btn=ORG3, tile=WH, tile_ink=INK3, icon=BLUE3,
             iconbg=(226, 238, 250)),
    a=dict(fn="grid", layout="row4", title="Diabetic supplies 2026:", title2="what Medicare pays for, and when", sub="Pick an item to see the rules:",
           size=58, hero=hero_diabetic, hero_h=320,
           tiles=[("w4_strips", "Test strips"), ("w4_lancet", "Lancets"), ("w4_cgm", "CGM sensors"), ("w4_shoe", "Therapeutic shoes")],
           src="разделы 2 (test strips, lancets), 3 (CGM), 6 (therapeutic shoes — «may cover one pair… when…»)",
           note="панель: глюкометр, коробка полосок, телефон с кривой, датчик CGM (без брендов) + 4 плитки; «and when» — у каждого пункта свои условия"),
    b=dict(fn="quiz", layout="card", title="Test strip quiz:", title2="the 3-month limit", size=60,
           tag="QUIZ", step="Question 1 of 3", prog=0.33,
           q="How many test strips does Medicare usually allow every 3 months for people on insulin?",
           opts=["100", "200", "300", "Not sure"],
           pal=dict(bg=(232, 242, 252), bg2=(204, 222, 246), acc=BLUE3, t2=ORG3, deco=True),
           src="раздел 2 «Diabetic test strips: how many Medicare usually allows» (ответ: до 300 на инсулине, 100 без)",
           note="голубой фон, вопрос о лимите Medicare в 3-м лице («for people on insulin»), не о зрителе"),
    c=dict(fn="compare", layout="split", title="300 test strips or 100?", sub="What Medicare usually allows every 3 months", size=60, band=214,
           cols=[("USES INSULIN", "w4_strips", BLUE3, ["Up to 300 test strips", "Up to 300 lancets", "More: only with documented need"]),
                 ("NO INSULIN", "w4_glucometer", ORG3, ["Up to 100 test strips", "Up to 100 lancets", "More: only with documented need"])],
           pal=dict(bg=(253, 247, 238), ink=INK3, sub=(96, 100, 110), btn=INK3, vs_bg=INK3, vs_ink=WH),
           src="раздел 2 (300 / 100 полосок и ланцетов за 3 месяца; «A doctor can request more when there is a documented medical need»); хук РК 1",
           note="сплит «на инсулине / без инсулина» — третьим лицом; $35 за инсулин не выносится (gaps)"),
    d=dict(fn="scene_d", scene="w4_diabetic_kitchen", style="bars", y=40,
           bars=[("WHY GLUCOSE METERS", WH, BLUE3), ("ARE OFTEN GIVEN AWAY", WH, ORG3), ("The real cost is in the test strips", INK3, None, 52)],
           bar_size=80, cond=0.8, btn_y=370, btn_size=44, max_w=960, pal=dict(btn=ORG3),
           scene_text="METER: a one-time buy / STRIPS: the ongoing cost",
           src="раздел 5 «Free blood glucose meter offers: where the catch is» (meter — one-time purchase, strips — the ongoing cost); хук РК 2",
           note="плашки + кухонный стол: глюкометр, коробка полосок, ручка-скарификатор, телефон с кривой, датчик CGM, кружка; слово «free» не используется"),
)

# ---------------------------------------------------------------- 4. US · налоговые льготы 60+ (субсидии)
GREEN4, GOLD4, INK4, BTN4 = (26, 92, 74), (226, 164, 44), (22, 36, 64), (206, 98, 34)
PACKS[4] = dict(
    doc="P60-senior-tax-help-us-2026-09-30", cta="Learn more",
    pal=dict(bg=(246, 244, 236), ink=INK4, sub=(84, 90, 100), acc=GREEN4, btn=BTN4, tile=WH, tile_ink=INK4, icon=GREEN4,
             iconbg=(226, 240, 232)),
    a=dict(fn="grid_desc", title="Senior property tax relief:", title2="4 common types", sub="Most need an application before a deadline – pick one:",
           size=58,
           dtiles=[("w4_house_down", "Homestead exemption", "Reduces the taxable value of a primary home"),
                   ("w4_house_lock", "Assessment freeze", "Locks the home's taxable value once the owner reaches a certain age"),
                   ("w4_breaker", "Circuit breaker credit", "Limits property tax to a share of household income"),
                   ("w4_house_clock", "Deferral", "Postpones the tax until the home is sold or the estate is settled")],
           pal=dict(bg=(246, 244, 236), bg2=(232, 228, 214)),
           src="раздел 2 «Senior property tax relief: four common types» (4 пункта) + раздел 3 (заявление и сроки)",
           note="2×2 с пояснением из статьи под каждым типом; без сумм и без «save / refund»"),
    b=dict(fn="quiz", layout="phone", title="Retirement tax quiz:", title2="when Social Security gets taxed",
           sub="What counts as combined income, and the cutoff", size=54, left_y=250,
           tag="TAX QUIZ", step="Question 1 of 3", prog=0.33,
           q="Below what combined income are Social Security benefits generally not taxed for a single filer?",
           opts=["$15,000", "$25,000", "$50,000", "Not sure"],
           pal=dict(bg=(26, 92, 74), bg2=(10, 50, 40), ink=WH, sub=(206, 230, 220), acc=GOLD4, btn=BTN4),
           src="раздел 1 «Federal tax breaks after 65», пункт Social Security income (ответ: $25,000 для одиночки, $32,000 для пары)",
           note="тёмно-зелёный фон, телефон с тестом; вопрос о правиле, не о доходе зрителя"),
    c=dict(fn="compare", layout="twocol", title="Turning 65 changes", title2="the tax return", sub="Federal basics before and after 65", size=60,
           cols=[("UNDER 65", "w4_under65", INK4), ("65 AND OLDER", "w4_age65", GREEN4)],
           rows=[("STANDARD DEDUCTION", "the regular amount", "regular + an extra amount"),
                 ("SENIOR DEDUCTION", "not available", "temporary, tax years 2025–2028"),
                 ("ITEMIZING NEEDED?", "–", "no, claimed either way")],
           foot="Deductions lower taxable income – they are not payments",
           src="вступление («Turning 65 changes a household's taxes…») + раздел 1 (увеличенный стандартный вычет, временный вычет 2025–2028 «whether or not the filer itemizes», «they are not payments»)",
           note="две колонки до/после 65 без сумм ($6,000 на крео не выносится — gaps); без «refund / get»"),
    d=dict(fn="scene_d", scene="w4_tax_library", style="band", band_h=244, title="Volunteer tax prep after 60",
           sub="Trained volunteers prepare returns at no charge in tax season – what to bring", size=60, lines=1, btn_y=1026, btn_size=40,
           pal=dict(band=INK4, band_ink=WH, band_sub=(214, 222, 236), btn=BTN4),
           scene_text="PROPERTY TAX RELIEF: APPLY BY the deadline, renew on time / WHAT TO BRING: Photo ID · Income statements · Last year's return / PROPERTY TAX BILL",
           src="раздел 4 «Tax counseling for the elderly and other free help» (волонтёры, 60+, сезон, что взять) + раздел 3 (заявление и сроки); хук РК 3",
           note="библиотека: полки, волонтёр с ноутбуком и пожилая пара, лист «что взять», счёт налога на дом, лист со сроком заявления; без названия ведомства, орла, печатей"),
)

# ---------------------------------------------------------------- 5. US · прививка от опоясывающего лишая (медицина 60+)
PLUM5, TEAL5, INK5 = (104, 60, 140), (0, 124, 124), (40, 30, 70)
PACKS[5] = dict(
    doc="P60-shingles-vaccine-us-2026-09-30", cta="Learn more",
    pal=dict(bg=(248, 244, 252), ink=INK5, sub=(96, 90, 110), acc=PLUM5, btn=TEAL5, tile=WH, tile_ink=INK5, icon=PLUM5,
             iconbg=(238, 230, 248)),
    a=dict(fn="list3", title="Shingles vaccine 2026:", title2="where the shot is given", sub="The place can change the bill – pick one:", size=58,
           hero=hero_places, hero_h=240,
           rows3=[("w4_pharmacy", "Pharmacy", "Often bills the drug plan directly"),
                  ("w4_doctor", "Doctor's office", "Reviews health history and timing"),
                  ("w4_clinic", "Public health clinic", "May serve people without insurance")],
           pal=dict(bg=(248, 244, 252), bg2=(234, 226, 246)),
           src="раздел 6 «Where people get the shingles vaccine» (3 вида мест) + раздел 5 (почему место меняет счёт); угол РК 2",
           note="улица с тремя зданиями (аптека Rx, кабинет врача, клиника — без брендов) + 3 строки-варианта"),
    b=dict(fn="quiz", layout="card", title="Medicare & the shingles shot:", title2="which part handles it?", size=54,
           tag="QUIZ", step="Question 1 of 3", prog=0.33,
           q="Under Medicare, which part handles the shingles vaccine?", opts=["Part A", "Part B", "Part D", "Not sure"],
           pal=dict(bg=(236, 246, 244), bg2=(204, 230, 226), acc=TEAL5, t2=PLUM5, deco=True),
           src="раздел 5 «Shingrix vaccine insurance coverage» (ответ: Part D, не Part B)",
           note="мятный фон; вопрос о программе, без «$0 / free shot»"),
    c=dict(fn="tags", title="Shingles shot price 2026", sub="Same two doses – the plan and the place set the bill", size=60,
           tags=[("w4_pill_plan", "Medicare Part D", PLUM5), ("shield_check", "Private health insurance", TEAL5),
                 ("doc_heart", "Medicaid: depends on the state", (186, 84, 66)), ("w4_no_cover", "No coverage", (70, 76, 96))],
           price="$?", foot="2 doses, usually 2–6 months apart",
           src="раздел 4 «Shingrix vaccine cost and shingles shot price» + раздел 5 (Part D / частная страховка / Medicaid по штатам)",
           note="4 ценника «$?» — цена зависит от плана и места (так в статье); без «$0», без бренда вакцины"),
    d=dict(fn="scene_d", scene="w4_shingles_pharmacy", style="top", y=40, kicker="SHINGLES VACCINE 2026",
           title="Two doses, months apart", sub="Who it's recommended for after 50, what it costs, how it's billed",
           size=62, lines=2, btn_y=1000, btn_size=44,
           pal=dict(ink=INK5, sub=(90, 84, 110), acc=PLUM5, btn=TEAL5),
           scene_text="SHINGLES VACCINE: Dose 1 ↓ Dose 2 in 2–6 months / телефон: Reminder · Dose 2",
           src="раздел 2 (две дозы через 2–6 месяцев, взрослым 50+) + раздел 6 (аптека напоминает о второй дозе); хук РК 1",
           note="аптечная стойка: полки с безымянными коробками, фармацевт, покупатель 60+ со спины, лист «Dose 1 → Dose 2 in 2–6 months», телефон-напоминание; шприца нет"),
)


# =====================================================================  сборка
def texts(t, cta):
    out = [W3.texts({k: v for k, v in t.items() if k not in ("tags",)}, cta)]
    if t.get("cards"):
        out.append(" / ".join(f"{lab} – {ft}: {pr} ({cap})" for _, lab, pr, cap, ft in t["cards"]) + f" (у каждой «{cta}»)")
    if t.get("gbars"):
        out.append(" / ".join(f"{lab}: {val}" for lab, _, _, val, _ in t["gbars"]))
        out.append("шкала " + " · ".join(x[1] for x in t["ticks"]))
    if t.get("dtiles"):
        out.append(" / ".join(f"{lab} – {d}" for _, lab, d in t["dtiles"]) + f" (у каждой «{cta}»)")
    if t.get("rows3"):
        out.append(" / ".join(f"{lab} – {d}" for _, lab, d in t["rows3"]) + f" (у каждой «{cta}»)")
    if t.get("tags"):
        out.append(" · ".join(f"{x[1]}: {t.get('price', '$?')}" for x in t["tags"]))
    out.append(f"кнопка «{cta}»" if not (t.get("tiles") or t.get("cards") or t.get("dtiles") or t.get("rows3")) else "")
    return W3._clean(" / ".join(x for x in out if x))


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
        items.append(dict(letter=Lt, file=f"cr/packs/{doc}/{Lt}.png", concept=CONCEPT[Lt] + " — " + t.get("note", ""),
                          text=texts(t, P["cta"]), cta=P["cta"], source=t.get("src", "")))
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
