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
def w4_cpap(c, cx, cy, s, col, bg=WH, water=(150, 200, 236), screen=(170, 226, 214)):
    """CPAP-аппарат: корпус с экраном и кнопкой, прозрачная камера увлажнителя, патрубок и начало шланга."""
    c.rect((cx - s * 0.44, cy - s * 0.16, cx + s * 0.18, cy + s * 0.32), fill=col, r=s * 0.08)
    c.rect((cx - s * 0.36, cy - s * 0.08, cx - s * 0.02, cy + s * 0.1), fill=screen, r=s * 0.03)
    c.line([(cx - s * 0.3, cy + s * 0.02), (cx - s * 0.22, cy - s * 0.02), (cx - s * 0.16, cy + s * 0.04), (cx - s * 0.08, cy - s * 0.03)], mix(col, screen, 0.3), s * 0.025)
    c.circle(cx + s * 0.08, cy + s * 0.01, s * 0.06, fill=mix(col, bg, 0.6))
    c.rect((cx - s * 0.36, cy + s * 0.18, cx + s * 0.1, cy + s * 0.22), fill=mix(col, bg, 0.3), r=s * 0.02)
    c.rect((cx + s * 0.14, cy - s * 0.1, cx + s * 0.44, cy + s * 0.32), fill=mix(water, bg, 0.35), r=s * 0.06, outline=col, width=s * 0.03)
    c.rect((cx + s * 0.17, cy + s * 0.1, cx + s * 0.41, cy + s * 0.29), fill=water, r=s * 0.04)
    c.rect((cx - s * 0.2, cy - s * 0.26, cx - s * 0.06, cy - s * 0.14), fill=col, r=s * 0.02)
    c.arc((cx - s * 0.13, cy - s * 0.48, cx + s * 0.27, cy - s * 0.14), 180, 300, mix(col, bg, 0.35), s * 0.07)


def w4_mask(c, cx, cy, s, col, bg=WH, cushion=(206, 226, 240)):
    """Носовая маска CPAP с оголовьем и шлангом."""
    c.arc((cx - s * 0.44, cy - s * 0.44, cx + s * 0.44, cy + s * 0.3), 200, 340, col, s * 0.05)
    c.line([(cx - s * 0.41, cy - s * 0.14), (cx - s * 0.2, cy + s * 0.02)], col, s * 0.05)
    c.line([(cx + s * 0.41, cy - s * 0.14), (cx + s * 0.2, cy + s * 0.02)], col, s * 0.05)
    c.poly([(cx, cy - s * 0.24), (cx + s * 0.24, cy + s * 0.14), (cx + s * 0.18, cy + s * 0.22), (cx - s * 0.18, cy + s * 0.22), (cx - s * 0.24, cy + s * 0.14)], cushion,
           outline=col, width=s * 0.035)
    c.poly([(cx, cy - s * 0.14), (cx + s * 0.14, cy + s * 0.1), (cx - s * 0.14, cy + s * 0.1)], mix(cushion, WH, 0.5))
    c.rect((cx - s * 0.07, cy + s * 0.2, cx + s * 0.07, cy + s * 0.3), fill=col, r=s * 0.02)
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
    c.arc((lx - s * 0.1, ly - s * 0.22, lx + s * 0.1, ly - s * 0.02), 180, 360, acc, s * 0.045)
    c.rect((lx - s * 0.16, ly - s * 0.1, lx + s * 0.16, ly + s * 0.16), fill=acc, r=s * 0.04, outline=bg, width=s * 0.03)
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
    c.text((cx, cy + s * 0.01), "65+", "db", s * 0.3, bg, anchor="mm")


def w4_under65(c, cx, cy, s, col, bg=WH):
    c.circle(cx, cy, s * 0.42, fill=col)
    c.circle(cx, cy, s * 0.34, outline=bg, width=s * 0.025)
    c.text((cx, cy + s * 0.01), "<65", "db", s * 0.28, bg, anchor="mm")


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


if __name__ == "__main__":
    if sys.argv[1:] == ["icons"]:
        icon_sheet()
