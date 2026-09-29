import math
import random
import sys
sys.path.insert(0, "/tmp/claude-0/-home-user-alextest/f5dce882-fce7-5270-9036-ca9a0fe43d5e/scratchpad")
from psy_lib import C, W

NAVY = (22, 30, 62)
RED = (226, 56, 48)
YEL = (255, 208, 104)
GRAY = (96, 104, 118)


def clock(c, cx, cy, r, face=(236, 238, 246), rim=(70, 78, 110), hand=(40, 44, 60)):
    c.ellipse((cx - r - 8, cy - r - 8, cx + r + 8, cy + r + 8), fill=rim)
    c.ellipse((cx - r, cy - r, cx + r, cy + r), fill=face)
    for k in range(12):
        a = math.radians(k * 30)
        r0 = r * (0.78 if k % 3 == 0 else 0.84)
        c.line([(cx + math.sin(a) * r0, cy - math.cos(a) * r0), (cx + math.sin(a) * r * 0.92, cy - math.cos(a) * r * 0.92)], hand, 5 if k % 3 == 0 else 3)
    ah = math.radians(210)   # 7 часов
    c.line([(cx, cy), (cx + math.sin(ah) * r * 0.5, cy - math.cos(ah) * r * 0.5)], hand, 9)
    c.line([(cx, cy), (cx, cy - r * 0.74)], hand, 6)   # минутная на 12
    c.ellipse((cx - 8, cy - 8, cx + 8, cy + 8), fill=RED)


def lamp(c, cx, top, w, h, glow=True, stand=(200, 204, 214)):
    """Лампа светотерапии: вертикальная панель на откидной ножке."""
    x0, x1, y0, y1 = cx - w / 2, cx + w / 2, top, top + h
    if glow:
        c.glow((x0 - 150, y0 - 130, x1 + 150, y1 + 130), (255, 246, 214), alpha=140, blur=70)
        c.glow((x0 - 50, y0 - 40, x1 + 50, y1 + 40), (255, 250, 232), alpha=200, blur=28)
    # откидная ножка сзади
    c.poly([(cx + w * 0.1, y0 + h * 0.45), (cx + w * 0.22, y0 + h * 0.45), (cx + w * 0.62, y1 + 58), (cx + w * 0.48, y1 + 58)], tuple(v - 40 for v in stand))
    # рамка и светящаяся панель
    c.rect((x0 - 12, y0 - 12, x1 + 12, y1 + 12), fill=(236, 238, 244), r=22)
    c.rect((x0, y0, x1, y1), fill=(255, 255, 250), r=14)
    for k in range(1, 4):
        yy = y0 + h * k / 4
        c.line([(x0 + 14, yy), (x1 - 14, yy)], (246, 244, 232), 2)
    # маленькая опора спереди
    c.rect((cx - w * 0.38, y1 + 10, cx + w * 0.38, y1 + 26), fill=stand, r=6)
    c.rect((cx - w * 0.08, y1 + 26, cx + w * 0.08, y1 + 58), fill=stand)
    c.rect((cx - w * 0.5, y1 + 52, cx + w * 0.7, y1 + 64), fill=stand, r=6)


def mug(c, x, y, col=(250, 250, 252), steam=True):
    c.rect((x, y, x + 86, y + 96), fill=col, r=14)
    c.ellipse((x + 70, y + 20, x + 116, y + 70), outline=col, width=12)
    c.ellipse((x + 6, y - 6, x + 80, y + 14), fill=(110, 70, 50))
    if steam:
        for k in range(2):
            pts = [(x + 28 + k * 28 + math.sin(t / 5 + k) * 8, y - 16 - t * 3) for t in range(22)]
            c.line(pts, (220, 224, 236), 4, alpha=150)


def a():
    """Иллюстрированная сцена: 7:00, за окном темно, светится лампа."""
    random.seed(7)
    c = C(NAVY)
    c.vgrad((0, 0, W, W), (28, 36, 72), (18, 24, 50))
    y = c.block("Winter blues or\nseasonal depression?", "db", 58, 36, 1000, (255, 255, 255), max_lines=2)
    c.block("7 questions doctors ask", "sb", 46, y + 6, 1000, YEL, max_lines=1)
    # окно
    wx = (500, 290, 1010, 740)
    c.rect((wx[0] - 18, wx[1] - 18, wx[2] + 18, wx[3] + 18), fill=(58, 66, 104), r=10)
    c.vgrad(wx, (10, 16, 46), (44, 62, 122))
    for _ in range(26):
        sx, sy = random.uniform(wx[0] + 10, wx[2] - 10), random.uniform(wx[1] + 10, wx[1] + 240)
        rr = random.choice((1.5, 2, 2.5))
        c.ellipse((sx - rr, sy - rr, sx + rr, sy + rr), fill=(230, 234, 255), alpha=200)
    # силуэт города
    bx = wx[0]
    while bx < wx[2]:
        bw = random.randint(40, 90)
        bh = random.randint(60, 190)
        c.rect((bx, wx[3] - bh, min(bx + bw, wx[2]), wx[3]), fill=(16, 20, 40))
        for _ in range(random.randint(0, 3)):
            lx = random.uniform(bx + 8, min(bx + bw, wx[2]) - 16)
            ly = random.uniform(wx[3] - bh + 12, wx[3] - 20)
            c.rect((lx, ly, lx + 9, ly + 12), fill=(255, 214, 120), alpha=230)
        bx += bw + 4
    c.rect(((wx[0] + wx[2]) / 2 - 8, wx[1], (wx[0] + wx[2]) / 2 + 8, wx[3]), fill=(58, 66, 104))
    c.rect((wx[0], (wx[1] + wx[3]) / 2 - 8, wx[2], (wx[1] + wx[3]) / 2 + 8), fill=(58, 66, 104))
    clock(c, 230, 372, 82)
    # стол
    c.rect((0, 770, W, W), fill=(84, 58, 44))
    c.rect((0, 760, W, 786), fill=(112, 80, 60))
    lamp(c, 230, 506, 190, 240)
    c.glow((60, 770, 520, 860), (255, 238, 190), alpha=90, blur=30)
    mug(c, 390, 676)
    c.button("Learn more", W / 2, 960, size=42, fill=RED)
    c.save("psy-winterblues-multi-0929_a.png")


def leaf(c, cx, cy, L, ang, col, alpha=255):
    pts = []
    for k in range(40):
        t = 2 * math.pi * k / 40
        x = L * math.cos(t)
        y = L * 0.45 * math.sin(t) * abs(math.sin(t)) ** 0.4
        a = math.radians(ang)
        pts.append((cx + x * math.cos(a) - y * math.sin(a), cy + x * math.sin(a) + y * math.cos(a)))
    c.poly(pts, col, alpha=alpha)
    a = math.radians(ang)
    c.line([(cx - L * math.cos(a), cy - L * math.sin(a)), (cx + L * 1.25 * math.cos(a), cy + L * 1.25 * math.sin(a))], tuple(max(0, v - 50) for v in col), 3, alpha=alpha)


def b():
    """Сравнение: Winter blues против Seasonal depression, два окна."""
    random.seed(3)
    c = C((246, 243, 238))
    y = c.block("Winter blues vs.\nseasonal depression", "db", 60, 40, 1000, NAVY, max_lines=2)
    c.block("7 questions doctors use to tell them apart", "s", 36, y + 4, 1000, GRAY, max_lines=1)
    L, R = (50, 262, 525, 910), (555, 262, 1030, 910)
    # левое окно: серый осенний день
    for box in (L, R):
        c.card(box, fill=(255, 255, 255), r=28, sh_alpha=50, blur=12, off=(0, 6))
    lw = (L[0] + 30, L[1] + 30, L[2] - 30, L[1] + 310)
    c.vgrad(lw, (172, 182, 198), (206, 212, 222))
    for _ in range(40):
        rx, ry = random.uniform(lw[0] + 6, lw[2] - 20), random.uniform(lw[1] + 6, lw[3] - 30)
        c.line([(rx, ry), (rx + 8, ry + 22)], (140, 152, 172), 2, alpha=180)
    for _ in range(6):
        leaf(c, random.uniform(lw[0] + 30, lw[2] - 30), random.uniform(lw[1] + 40, lw[3] - 30), 20, random.uniform(0, 180),
             random.choice([(226, 120, 50), (236, 160, 60), (200, 90, 50)]))
    c.rect(((lw[0] + lw[2]) / 2 - 6, lw[1], (lw[0] + lw[2]) / 2 + 6, lw[3]), fill=(236, 232, 226))
    c.rect(lw, outline=(236, 232, 226), width=12)
    # правое окно: тёмное утро, одна лампа
    rw = (R[0] + 30, R[1] + 30, R[2] - 30, R[1] + 310)
    c.vgrad(rw, (12, 18, 50), (36, 50, 104))
    c.ellipse((rw[2] - 110, rw[1] + 40, rw[2] - 60, rw[1] + 90), fill=(232, 236, 250))
    c.ellipse((rw[2] - 96, rw[1] + 34, rw[2] - 50, rw[1] + 80), fill=(20, 28, 64))
    c.line([(rw[0] + 10, rw[1] + 220), (rw[0] + 120, rw[1] + 170), (rw[0] + 200, rw[1] + 120)], (8, 12, 30), 7)
    c.line([(rw[0] + 120, rw[1] + 170), (rw[0] + 150, rw[1] + 230)], (8, 12, 30), 5)
    c.glow((rw[0] + 270, rw[3] - 130, rw[0] + 380, rw[3] - 30), (255, 214, 120), alpha=170, blur=18)
    c.rect((rw[0] + 312, rw[3] - 92, rw[0] + 338, rw[3] - 64), fill=(255, 226, 150), r=6)
    c.rect(((rw[0] + rw[2]) / 2 - 6, rw[1], (rw[0] + rw[2]) / 2 + 6, rw[3]), fill=(236, 232, 226))
    c.rect(rw, outline=(236, 232, 226), width=12)
    for box, head, col in ((L, "WINTER BLUES", (200, 110, 50)), (R, "SEASONAL DEPRESSION", (46, 70, 150))):
        cx = (box[0] + box[2]) / 2
        c.block(head, "db", 32, box[1] + 350, box[2] - box[0] - 40, col, cx=cx, max_lines=1)
    rows = [("HOW OFTEN", "comes and goes", "most days, for weeks"), ("DAILY LIFE", "mostly unchanged", "often disrupted")]
    ry = 668
    for lab, lt, rt in rows:
        for box, t, col in ((L, lt, (200, 110, 50)), (R, rt, (46, 70, 150))):
            c.text((box[0] + 40, ry), lab, "sb", 22, col)
            c.block(t, "sb", 34, ry + 30, box[2] - box[0] - 70, (36, 38, 44), align="left", x=box[0] + 40, max_lines=1)
        ry += 116
    c.button("Learn more", W / 2, 994, size=42, fill=RED)
    c.save("psy-winterblues-multi-0929_b.png")


def c_():
    """Сетка выбора (товарка): лампа сверху, 4 одинаковые плитки с «Learn more»."""
    c = C((243, 241, 237))
    c.vgrad((0, 0, W, W), (250, 248, 244), (236, 232, 226))
    c.card((40, 172, 1040, 566), fill=(30, 42, 88), r=28, sh_alpha=50, blur=10, off=(0, 5))
    c.rect((40, 470, 1040, 566), fill=(70, 52, 44), r=28)
    c.rect((40, 470, 1040, 500), fill=(70, 52, 44))
    c.rect((40, 462, 1040, 476), fill=(98, 72, 58))
    lamp(c, 540, 206, 200, 240, stand=(196, 200, 212))
    c.rect((0, 0, W, 166), fill=(249, 247, 243))
    y = c.block("Light therapy lamps 2026", "db", 60, 38, 1000, NAVY, max_lines=1)
    c.block("What to check before buying", "s", 36, y + 2, 1000, GRAY, max_lines=1)
    tiles = [("10,000", "lux"), ("20–30", "minutes"), ("Morning", "after waking"), ("UV", "filtered")]
    x0, gap, tw_ = 40, 16, (1000 - 3 * 16) / 4
    for i, (big, small) in enumerate(tiles):
        bx = (x0 + i * (tw_ + gap), 600, x0 + i * (tw_ + gap) + tw_, 920)
        cx = (bx[0] + bx[2]) / 2
        c.card(bx, fill=(255, 255, 255), r=24, sh_alpha=45, blur=10, off=(0, 5), outline=(226, 222, 214), width=2)
        c.block(big, "db", 50, bx[1] + 44, tw_ - 24, NAVY, cx=cx, max_lines=1)
        c.block(small, "s", 30, bx[1] + 118, tw_ - 20, GRAY, cx=cx, max_lines=1)
        c.rect((bx[0] + 30, bx[1] + 180, bx[2] - 30, bx[1] + 183), fill=(232, 228, 220))
        c.button("Learn more", cx, bx[1] + 250, size=24, fill=RED, padx=20, pady=14, arrow=False, shadow=False)
    c.block("+ the 7-question check: winter blues or seasonal depression?", "sb", 30, 966, 1000, NAVY, max_lines=1)
    c.save("psy-winterblues-multi-0929_c.png")


def d():
    """Фейковая интерактивность: вопрос 1 из 7 с месяцами-кнопками, осенний фон с листьями."""
    random.seed(11)
    c = C((214, 120, 62))
    c.vgrad((0, 0, W, W), (236, 160, 76), (190, 88, 52))
    spots = [(40, 70), (1030, 60), (60, 330), (1040, 300), (30, 620), (1050, 640), (70, 900), (1020, 880),
             (210, 1040), (880, 1040), (30, 470), (1050, 470)]
    for i, (lx, ly) in enumerate(spots):
        leaf(c, lx, ly, random.uniform(20, 32), random.uniform(0, 360),
             [(250, 196, 90), (170, 70, 40), (240, 130, 60), (120, 60, 36)][i % 4], alpha=210)
    y = c.block("Winter blues or\nseasonal depression?", "db", 58, 40, 1000, (255, 255, 255), max_lines=2)
    q = "In which months do sleep and energy change the most?"
    top = y + 40
    qs = c.fit(q, "db", 800, 2, 42)
    fq = c.font("db", qs)
    asc, desc = fq.getmetrics()
    q_end = top + 158 + len(c.wrap(q, fq, 800)) * (asc + desc) / c.K * 1.16
    box = (90, top, 990, q_end + 26 + 2 * 96 + 20 + 56)
    c.card(box, r=36, sh_alpha=110, blur=20)
    c.rect((140, box[1] + 42, 420, box[1] + 90), fill=(255, 238, 214), r=24)
    c.text((280, box[1] + 66), "7-QUESTION CHECK", "sb", 24, (190, 88, 52), anchor="mm")
    c.text((940, box[1] + 66), "1 / 7", "sb", 28, GRAY, anchor="rm")
    c.rect((140, box[1] + 116, 940, box[1] + 128), fill=(236, 232, 226), r=6)
    c.rect((140, box[1] + 116, 140 + 800 / 7, box[1] + 128), fill=(214, 110, 56), r=6)
    qy = c.block(q, "db", 42, box[1] + 158, 800, NAVY, align="left", x=140, max_lines=2)
    opts = ["Oct – Nov", "Dec – Jan", "Feb – Mar", "No change"]
    cw, chh = 390, 96
    for i, o in enumerate(opts):
        cx0 = 140 + (i % 2) * (cw + 20)
        cy0 = qy + 26 + (i // 2) * (chh + 20)
        c.rect((cx0, cy0, cx0 + cw, cy0 + chh), fill=(250, 247, 242), r=22, outline=(222, 214, 202), width=3)
        # маленький календарь
        ix, iy = cx0 + 28, cy0 + 26
        c.rect((ix, iy, ix + 44, iy + 44), fill=(255, 255, 255), outline=(190, 88, 52), width=3, r=6)
        c.rect((ix, iy, ix + 44, iy + 12), fill=(190, 88, 52), r=4)
        c.text((ix + 70, cy0 + chh / 2), o, "sb", 36, (44, 48, 60), anchor="lm")
    c.button("Learn more", W / 2, (box[3] + W) / 2, size=42, fill=NAVY)
    c.save("psy-winterblues-multi-0929_d.png")


if __name__ == "__main__":
    for f in sys.argv[1:]:
        globals()[f if f != "c" else "c_"]()
