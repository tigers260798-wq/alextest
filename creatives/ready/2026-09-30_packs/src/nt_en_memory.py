"""EN · тест памяти 60+ → memory care — 4 статики 1:1 (Pillow), стиль 2026-09-30_psy.

Без «your memory / your parents», без растерянных лиц, людей и медицинских эмблем.
Цифры стоимости — из гипотезы new_tests/psy-memory-us-0929 (seniorliving.org, 2026).
"""
import math
import random
import sys
sys.path.insert(0, "/home/user/alextest/creatives/ready/2026-09-30_packs/src")
from nt_lib import C, W, leaf, flower, rotpoly

DOC = "NT-psy-memory-en-2026-09-30"
INK = (32, 38, 66)
PLUM = (96, 64, 140)
TEAL = (20, 128, 128)
RED = (226, 56, 48)
GRAY = (96, 102, 116)
PENCIL = (60, 62, 72)
CTA = "Learn more"


def wobble_circle(c, cx, cy, r, col, width=5, seed=1, amp=4):
    random.seed(seed)
    pts = []
    ph = [random.uniform(0, 6.28) for _ in range(3)]
    for i in range(0, 361, 4):
        a = math.radians(i)
        rr = r + amp * math.sin(a * 3 + ph[0]) + amp * 0.6 * math.sin(a * 5 + ph[1])
        pts.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr))
    c.line(pts, col, width)


def hand_clock(c, cx, cy, r, mode="ok", seed=1, col=PENCIL, num_size=None, jitter=5):
    """Нарисованный от руки циферблат. mode: ok — 10 past 11; crowd — цифры сбились на правую половину; hands — стрелки на 11 и 10."""
    random.seed(seed)
    wobble_circle(c, cx, cy, r, col, width=max(3, r / 36), seed=seed)
    ns = num_size or int(r * 0.2)
    for n in range(1, 13):
        if mode == "crowd":
            a = math.radians(-80 + (n - 1) * 15)   # все цифры на правой половине
        else:
            a = math.radians(n * 30 - 90)
        rr = r * 0.78
        x = cx + math.cos(a) * rr + random.uniform(-jitter, jitter)
        y = cy + math.sin(a) * rr + random.uniform(-jitter, jitter)
        c.text((x, y), str(n), "s", ns, col, anchor="mm")
    if mode == "ok":
        hour_to, min_to = 11 + 10 / 60, 2
    elif mode == "hands":
        hour_to, min_to = 11, 10
    else:
        hour_to, min_to = 11 + 10 / 60, 2
    ah = math.radians(hour_to * 30 - 90)
    am = math.radians(min_to * 30 - 90)
    w = max(3, r / 30)
    c.line([(cx, cy), (cx + math.cos(ah) * r * 0.45, cy + math.sin(ah) * r * 0.45)], col, w * 1.4)
    c.line([(cx, cy), (cx + math.cos(am) * r * 0.66, cy + math.sin(am) * r * 0.66)], col, w)
    c.ellipse((cx - w * 1.4, cy - w * 1.4, cx + w * 1.4, cy + w * 1.4), fill=col)


def pencil(c, x0, y0, x1, y1, w=26):
    ang = math.atan2(y1 - y0, x1 - x0)
    nx, ny = -math.sin(ang) * w / 2, math.cos(ang) * w / 2
    L = math.hypot(x1 - x0, y1 - y0)
    ux, uy = (x1 - x0) / L, (y1 - y0) / L

    def pt(t, side):
        return (x0 + ux * t + nx * side, y0 + uy * t + ny * side)
    c.poly([pt(0, 1), pt(40, 1), pt(40, -1), pt(0, -1)], (240, 140, 150))
    c.poly([pt(40, 1), pt(58, 1), pt(58, -1), pt(40, -1)], (170, 170, 176))
    c.poly([pt(58, 1), pt(L - 70, 1), pt(L - 70, -1), pt(58, -1)], (248, 196, 44))
    c.poly([pt(L - 70, 1), pt(L - 70, -1), (x1, y1)], (236, 204, 160))
    c.poly([pt(L - 22, 0.32), pt(L - 22, -0.32), (x1, y1)], (60, 60, 64))


def word_card(c, cx, cy, word, ang, fill=(255, 255, 255), col=INK):
    w, h = 230, 96
    pts = rotpoly([(cx - w / 2, cy - h / 2), (cx + w / 2, cy - h / 2), (cx + w / 2, cy + h / 2), (cx - w / 2, cy + h / 2)], cx, cy, ang)
    c.poly([(x + 6, y + 10) for x, y in pts], (0, 0, 0), alpha=50)
    c.poly(pts, fill)
    # текст на отдельном слое с поворотом
    from PIL import Image, ImageDraw
    K = c.K
    lay = Image.new("RGBA", (int(w * K), int(h * K)), (0, 0, 0, 0))
    ImageDraw.Draw(lay).text((w * K / 2, h * K / 2), word, font=c.font("db", 40), fill=col + (255,), anchor="mm")
    lay = lay.rotate(-ang, resample=Image.BICUBIC, expand=True)
    full = c.layer()
    full.alpha_composite(lay, (int(cx * K - lay.width / 2), int(cy * K - lay.height / 2)))
    c.put(full)


def a():
    """Сцена-иллюстрация по брифу: лист с нарисованным циферблатом, карандаш и три карточки со словами."""
    c = C((236, 232, 246))
    c.vgrad((0, 0, W, W), (240, 236, 248), (222, 216, 238))
    y = c.block("The 5-minute memory check\ndoctors use after 60", "db", 60, 36, 1010, INK, max_lines=2)
    y = c.block("Draw a clock. Recall 3 words.", "sb", 44, y + 6, 1000, PLUM, max_lines=1)
    # стол-лист
    paper = rotpoly([(90, 330), (640, 330), (640, 920), (90, 920)], 365, 625, -3)
    c.poly([(x + 8, yy + 12) for x, yy in paper], (0, 0, 0), alpha=45)
    c.poly(paper, (255, 255, 255))
    hand_clock(c, 365, 610, 220, mode="ok", seed=4, num_size=44, jitter=9)
    pencil(c, 700, 420, 560, 760, w=28)
    for (cx, cy, wd, ang) in ((840, 470, "RIVER", -6), (850, 630, "GARDEN", 4), (835, 790, "CHAIR", -3)):
        word_card(c, cx, cy, wd, ang)
    c.button(CTA, W / 2, 996, size=44, fill=RED, padx=60)
    c.save(f"{DOC}/a.png")


def b():
    """Карточка-опросник: какой из трёх рисунков «10 past 11» врач засчитает как норму."""
    c = C((250, 247, 240))
    c.rect((0, 0, W, 300), fill=(32, 38, 66))
    c.text((W / 2, 62), "THE CLOCK TEST DOCTORS USE AFTER 60", "sb", 30, (160, 214, 210), anchor="mm")
    y = c.block("“Draw a clock showing 10 past 11.”", "db", 50, 104, 1000, (255, 255, 255), max_lines=1)
    c.block("Which one would a doctor score as normal?", "sb", 40, y + 14, 1000, (255, 206, 92), max_lines=1)
    modes = [("A", "crowd", 2), ("B", "ok", 5), ("C", "hands", 7)]
    for i, (L, m, sd) in enumerate(modes):
        cx = 190 + i * 350
        box = (cx - 160, 350, cx + 160, 810)
        c.card(box, fill=(255, 255, 255), r=26, sh_alpha=55, blur=12, off=(0, 6))
        hand_clock(c, cx, 540, 128, mode=m, seed=sd, num_size=26, jitter=5)
        c.ellipse((cx - 38, 700, cx + 38, 776), fill=(234, 236, 246), outline=(180, 186, 204), width=3)
        c.text((cx, 738), L, "db", 40, INK, anchor="mm")
    c.text((W / 2, 870), "Answer + what the result shows", "sb", 36, INK, anchor="mm")
    c.button(CTA, W / 2, 976, size=44, fill=RED, padx=60)
    c.save(f"{DOC}/b.png")


def c_():
    """Сколько стоит: memory care по штатам, 2026 (мин / среднее / макс)."""
    c = C((244, 247, 252))
    y = c.block("Memory care in 2026:", "db", 58, 40, 1000, INK, max_lines=1)
    y = c.block("what it costs, state by state", "db", 58, y, 1000, TEAL, max_lines=1)
    c.block("Average monthly cost", "s", 34, y + 10, 1000, GRAY, max_lines=1)
    panel = (60, y + 76, 1020, 800)
    c.card(panel, fill=(255, 255, 255), r=30, sh_alpha=45, blur=14, off=(0, 6))
    rows = [("South Dakota", "lowest", 5538, (120, 190, 180)), ("U.S. average", "", 7645, (20, 128, 128)), ("Hawaii", "highest", 14399, (96, 64, 140))]
    x0, x1 = panel[0] + 44, panel[2] - 44
    ry = panel[1] + 50
    for lab, tag, v, col in rows:
        c.text((x0, ry + 18), lab, "db", 38, INK, anchor="lm")
        if tag:
            tw_ = c.tw(lab, c.font("db", 38))[0]
            c.rect((x0 + tw_ + 16, ry + 2, x0 + tw_ + 16 + 130, ry + 36), fill=(236, 238, 246), r=17)
            c.text((x0 + tw_ + 81, ry + 19), tag, "sb", 22, GRAY, anchor="mm")
        bw = (x1 - x0 - 10) * v / 14399
        c.rect((x0, ry + 50, x0 + bw, ry + 112), fill=col, r=14)
        label = f"${v:,}/mo"
        if bw > 330:
            c.text((x0 + bw - 20, ry + 81), label, "db", 36, (255, 255, 255), anchor="rm")
        else:
            c.text((x0 + bw + 16, ry + 81), label, "db", 36, INK, anchor="lm")
        ry += 172
    c.text((W / 2, 856), "+ what Medicare does and does not pay", "sb", 34, INK, anchor="mm")
    c.button(CTA, W / 2, 966, size=44, fill=RED, padx=60)
    c.save(f"{DOC}/c.png")


# ---------- иконки для сетки
def ic_building(c, cx, cy, col):
    c.rect((cx - 70, cy - 50, cx + 70, cy + 56), fill=col, r=6)
    c.poly([(cx - 82, cy - 46), (cx, cy - 92), (cx + 82, cy - 46)], col)
    for r_ in range(2):
        for q in range(4):
            x = cx - 54 + q * 30
            c.rect((x, cy - 38 + r_ * 30, x + 18, cy - 20 + r_ * 30), fill=(255, 255, 255), r=3)
    c.rect((cx - 14, cy + 26, cx + 14, cy + 56), fill=(255, 255, 255), r=3)


def ic_bed(c, cx, cy, col):
    c.rect((cx - 80, cy - 40, cx - 64, cy + 50), fill=col, r=4)
    c.rect((cx - 64, cy + 4, cx + 80, cy + 28), fill=col, r=4)
    c.rect((cx + 68, cy - 10, cx + 82, cy + 50), fill=col, r=3)
    c.rect((cx - 60, cy - 16, cx + 70, cy + 6), fill=(255, 255, 255), r=8)
    c.rect((cx - 58, cy - 36, cx - 18, cy - 12), fill=(255, 255, 255), r=10)


def ic_home(c, cx, cy, col):
    c.poly([(cx - 80, cy - 4), (cx, cy - 76), (cx + 80, cy - 4)], col)
    c.rect((cx - 60, cy - 10, cx + 60, cy + 56), fill=col)
    c.ellipse((cx - 24, cy + 2, cx + 2, cy + 28), fill=(255, 255, 255))
    c.ellipse((cx - 2, cy + 2, cx + 24, cy + 28), fill=(255, 255, 255))
    c.poly([(cx - 23, cy + 19), (cx + 23, cy + 19), (cx, cy + 44)], (255, 255, 255))


def ic_sun(c, cx, cy, col):
    for k in range(8):
        a = math.radians(k * 45)
        c.line([(cx + math.cos(a) * 46, cy + math.sin(a) * 46), (cx + math.cos(a) * 68, cy + math.sin(a) * 68)], col, 9)
    c.ellipse((cx - 36, cy - 36, cx + 36, cy + 36), fill=col)


def d():
    """Сетка выбора 2×2: форматы memory care, у каждой плитки одинаковое «Learn more»."""
    c = C((255, 251, 244))
    c.vgrad((0, 0, W, W), (255, 250, 242), (246, 238, 226))
    y = c.block("Memory care options in 2026", "db", 58, 40, 1000, INK, max_lines=1)
    c.block("How they compare – and what each one costs", "s", 34, y + 4, 1000, GRAY, max_lines=1)
    tiles = [("Assisted living\n+ memory care", ic_building, (20, 128, 128), (224, 242, 240)),
             ("Nursing home\nmemory care", ic_bed, (96, 64, 140), (236, 230, 246)),
             ("In-home\nmemory care", ic_home, (214, 110, 60), (250, 232, 220)),
             ("Adult day\nprograms", ic_sun, (220, 160, 30), (250, 242, 214))]
    boxes = [(40, 196, 530, 598), (550, 196, 1040, 598), (40, 618, 530, 1020), (550, 618, 1040, 1020)]
    for (lab, ic, col, bg), bx in zip(tiles, boxes):
        c.card(bx, fill=(255, 255, 255), r=28, sh_alpha=50, blur=10, off=(0, 5))
        cx = (bx[0] + bx[2]) / 2
        c.ellipse((cx - 84, bx[1] + 24, cx + 84, bx[1] + 192), fill=bg)
        ic(c, cx, bx[1] + 112, col)
        c.block(lab, "db", 36, bx[1] + 212, 440, INK, cx=cx, max_lines=2, gap=1.1)
        c.button(CTA, cx, bx[3] - 52, size=30, fill=RED, padx=36, pady=14, shadow=False)
    c.save(f"{DOC}/d.png")


if __name__ == "__main__":
    for f in sys.argv[1:] or ["a", "b", "c", "d"]:
        globals()[f if f != "c" else "c_"]()
