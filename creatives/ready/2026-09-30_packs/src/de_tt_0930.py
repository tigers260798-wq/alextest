"""DE кредиты · TikTok · статья IRONFLI «Kredit mit Rente 2026: Welche Summe ist realistisch und worauf schaut die Bank?»
(кампании AlexZLoansDE). 4 вертикальные статики 1080×1920 целиком в Pillow — замена TT-крео, которые 27–28.09 дали
CTR 0.37 % (24 клика на 6 444 показа, hook2s 13 %). Запуск:
    python3 de_tt_0930.py          — все четыре
    python3 de_tt_0930.py a c      — только a и c
    python3 de_tt_0930.py sheet    — плюс контактный лист (scratch) для проверки глазами
Пишет /home/user/alextest/creatives/ready/2026-09-30_de_tt/{a,b,c,d}.png и creatives.json.

Правила, заложенные в вёрстку (и проверяемые в конце — assert_safe):
- текст только в безопасной зоне TikTok: y 170…1480; при y > 640 — x 70…900 (правее стоят иконки ленты);
  ниже 1480 — только фон и декор (подпись, ник и CTA-плашка TikTok);
- кнопка на картинке — «Mehr erfahren»; нет «hier klicken», «sofort», «ohne Schufa», «garantiert», процентов,
  сумм как обещания, логотипов банков и обращения к месту («in Ihrer Nähe»);
- нет вопросов и утверждений о возрасте, финансах или долгах зрителя («Sind Sie Rentner?», «Ihre Rente» и т. п.);
- флаг Германии — только на a (он был на FB-исходнике 0928-GE01, правило владельца 29.09), новых эмблем нет.
Шрифты (OFL, Google Fonts) лежат рядом: src/fonts/.
"""
import json
import math
import os
import random
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = "/home/user/alextest/creatives/ready/2026-09-30_de_tt"
W, H = 1080, 1920
K = 2  # суперсэмплинг

FONTS = {
    "anton": os.path.join(HERE, "fonts", "Anton-Regular.ttf"),
    "mblack": os.path.join(HERE, "fonts", "Montserrat-Black.ttf"),
    "mxb": os.path.join(HERE, "fonts", "Montserrat-ExtraBold.ttf"),
    "mb": os.path.join(HERE, "fonts", "Montserrat-Bold.ttf"),
    "msb": os.path.join(HERE, "fonts", "Montserrat-SemiBold.ttf"),
}

# безопасная зона TikTok (единицы 1080×1920)
SAFE_TOP, SAFE_BOTTOM = 170, 1480
SAFE_LEFT, SAFE_RIGHT_LOW, SAFE_RIGHT_HIGH, RAIL_Y = 70, 900, 1010, 640

WHITE = (255, 255, 255)
INK = (20, 20, 24)


def mix(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def rgba(c, a=255):
    return tuple(c[:3]) + (a,)


class V:
    """Холст 1080×1920, рисуется в K раз крупнее. Все координаты — в единицах 1080×1920."""

    def __init__(self, bg=WHITE):
        self.im = Image.new("RGBA", (W * K, H * K), rgba(bg))
        self._f = {}
        self.text_boxes = []  # (x0, y0, x1, y1, text) — для проверки безопасной зоны
        self.buttons = []

    # --- база
    def s(self, v):
        return int(round(v * K))

    def sb(self, box):
        return tuple(self.s(v) for v in box)

    def sp(self, pts):
        return [(self.s(x), self.s(y)) for x, y in pts]

    def font(self, name, size):
        key = (name, size)
        if key not in self._f:
            self._f[key] = ImageFont.truetype(FONTS[name], self.s(size))
        return self._f[key]

    def layer(self):
        return Image.new("RGBA", self.im.size, (0, 0, 0, 0))

    def _dd(self, alpha):
        if alpha >= 255:
            return ImageDraw.Draw(self.im), None
        lay = self.layer()
        return ImageDraw.Draw(lay), lay

    def _done(self, lay, blur=0):
        if lay is not None:
            if blur:
                lay = lay.filter(ImageFilter.GaussianBlur(self.s(blur)))
            self.im.alpha_composite(lay)

    # --- фигуры
    def rect(self, box, fill=None, r=0, outline=None, width=0, alpha=255):
        dd, lay = self._dd(alpha)
        kw = dict(fill=rgba(fill, alpha) if fill else None, outline=rgba(outline, alpha) if outline else None,
                  width=self.s(width) if width else 0)
        if r:
            dd.rounded_rectangle(self.sb(box), self.s(r), **kw)
        else:
            dd.rectangle(self.sb(box), **kw)
        self._done(lay)

    def ellipse(self, box, fill=None, outline=None, width=0, alpha=255):
        dd, lay = self._dd(alpha)
        dd.ellipse(self.sb(box), fill=rgba(fill, alpha) if fill else None,
                   outline=rgba(outline, alpha) if outline else None, width=self.s(width) if width else 0)
        self._done(lay)

    def circle(self, cx, cy, r, **kw):
        self.ellipse((cx - r, cy - r, cx + r, cy + r), **kw)

    def poly(self, pts, fill, alpha=255):
        dd, lay = self._dd(alpha)
        dd.polygon(self.sp(pts), fill=rgba(fill, alpha))
        self._done(lay)

    def line(self, pts, fill, width=4, alpha=255):
        dd, lay = self._dd(alpha)
        dd.line(self.sp(pts), fill=rgba(fill, alpha), width=self.s(width), joint="curve")
        self._done(lay)

    def arc(self, box, a0, a1, fill, width=4, alpha=255):
        dd, lay = self._dd(alpha)
        dd.arc(self.sb(box), a0, a1, fill=rgba(fill, alpha), width=self.s(width))
        self._done(lay)

    def shadow(self, box, r=30, alpha=70, blur=22, off=(0, 14), color=(0, 0, 0)):
        lay = self.layer()
        ImageDraw.Draw(lay).rounded_rectangle(
            self.sb((box[0] + off[0], box[1] + off[1], box[2] + off[0], box[3] + off[1])), self.s(r), fill=rgba(color, alpha))
        self._done(lay, blur=blur)

    def vgrad(self, box, c0, c1):
        x0, y0, x1, y1 = self.sb(box)
        g = Image.new("RGBA", (1, 256))
        for i in range(256):
            g.putpixel((0, i), rgba(mix(c0, c1, i / 255)))
        g = g.resize((x1 - x0, y1 - y0), Image.BILINEAR)
        self.im.alpha_composite(g, (x0, y0))

    def glow(self, cx, cy, r, color, alpha=120):
        lay = self.layer()
        ImageDraw.Draw(lay).ellipse(self.sb((cx - r, cy - r, cx + r, cy + r)), fill=rgba(color, alpha))
        self._done(lay, blur=r * 0.45)

    # --- текст
    def tw(self, text, name, size):
        b = self.font(name, size).getbbox(text)
        return (b[2] - b[0]) / K

    def cap(self, name, size):
        """Высота прописной (для вертикального центрирования)."""
        b = self.font(name, size).getbbox("H")
        return b, (b[3] - b[1]) / K

    def fit(self, lines, name, size, max_w, min_size=24):
        while size > min_size and max(self.tw(l, name, size) for l in lines) > max_w:
            size -= 2
        return size

    def text(self, xy, text, name, size, fill, anchor="la", alpha=255, record=True):
        dd, lay = self._dd(alpha)
        dd.text(self.sp([xy])[0], text, font=self.font(name, size), fill=rgba(fill, alpha), anchor=anchor)
        self._done(lay)
        if record:
            b = dd.textbbox(self.sp([xy])[0], text, font=self.font(name, size), anchor=anchor)
            self.text_boxes.append((b[0] / K, b[1] / K, b[2] / K, b[3] / K, text))

    def rich(self, cx, y, parts, name, size, anchor_x="center", x=None):
        """Строка из кусков разного цвета: parts = [(text, color), ...]; y — верх строки (baseline-агностично: ascender)."""
        total = sum(self.tw(t, name, size) for t, _ in parts)
        # пробелы между кусками уже внутри текста; ширина по getbbox режет хвостовые пробелы — меряем через getlength
        f = self.font(name, size)
        total = sum(f.getlength(t) / K for t, _ in parts)
        xx = (cx - total / 2) if anchor_x == "center" else x
        for t, col in parts:
            self.text((xx, y), t, name, size, col, anchor="ls")
            xx += f.getlength(t) / K
        return total

    def lines_center(self, lines, name, size, cx, y_top, fill, gap=1.12, colors=None):
        """Центрированные строки; y_top — верх первой строки по прописной. Возвращает низ последней строки."""
        _, capH = self.cap(name, size)
        y = y_top + capH
        for i, l in enumerate(lines):
            if isinstance(l, list):
                self.rich(cx, y, l, name, size)
            else:
                self.text((cx, y), l, name, size, fill, anchor="ms")
            y += size * gap
        return y - size * gap

    def lines_left(self, lines, name, size, x, y_top, fill, gap=1.12):
        _, capH = self.cap(name, size)
        y = y_top + capH
        for l in lines:
            if isinstance(l, list):
                self.rich(None, y, l, name, size, anchor_x="left", x=x)
            else:
                self.text((x, y), l, name, size, fill, anchor="ls")
            y += size * gap
        return y - size * gap

    # --- кнопка «Mehr erfahren →» (стрелка рисуется фигурой, не глифом)
    def button(self, label, cx, cy, size=58, fill=(214, 38, 52), color=WHITE, h=124, padx=64, name="mxb",
               arrow=True, shadow=True, outline=None):
        tw = self.tw(label, name, size)
        aw = size * 0.9 if arrow else 0
        w = tw + aw + padx * 2
        box = (cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2)
        if shadow:
            self.shadow(box, r=h / 2, alpha=80, blur=16, off=(0, 10))
        self.rect(box, fill=fill, r=h / 2, outline=outline, width=4 if outline else 0)
        self.buttons.append(box)
        x = box[0] + padx
        b, capH = self.cap(name, size)
        self.text((x, cy + capH / 2), label, name, size, color, anchor="ls")
        if arrow:
            ax = x + tw + size * 0.3
            ah = size * 0.36
            self.line([(ax, cy), (ax + aw - size * 0.25, cy)], color, width=size * 0.12)
            tip = ax + aw - size * 0.12
            self.poly([(tip, cy), (tip - ah * 1.1, cy - ah), (tip - ah * 1.1, cy + ah)], color)
        return box

    # --- сохранение ≤ 400 КБ
    def save(self, name):
        os.makedirs(OUT, exist_ok=True)
        path = os.path.join(OUT, name)
        img = self.im.convert("RGB").resize((W, H), Image.LANCZOS)
        img.save(path, optimize=True)
        info = "truecolor"
        if os.path.getsize(path) > 400 * 1024:
            for colors in (256, 224, 192, 160, 128):
                q = img.quantize(colors=colors, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.FLOYDSTEINBERG)
                q.save(path, optimize=True)
                info = f"{colors} colors"
                if os.path.getsize(path) <= 400 * 1024:
                    break
        print(name, img.size, os.path.getsize(path) // 1024, "KB", info)
        return path


def assert_safe(c, tag):
    bad = []
    for x0, y0, x1, y1, t in c.text_boxes:
        right = SAFE_RIGHT_HIGH if y1 <= RAIL_Y else SAFE_RIGHT_LOW
        if y0 < SAFE_TOP or y1 > SAFE_BOTTOM or x0 < SAFE_LEFT or x1 > right:
            bad.append((round(x0), round(y0), round(x1), round(y1), t))
    if bad:
        raise SystemExit(f"{tag}: текст вне безопасной зоны TikTok: {bad}")
    for bx in c.buttons:
        if bx[3] > 1495 or bx[2] > SAFE_RIGHT_LOW + 10 or bx[0] < SAFE_LEFT:
            raise SystemExit(f"{tag}: кнопка вне зоны: {tuple(round(v) for v in bx)}")
    ys = [b[3] for b in c.text_boxes]
    print(f"  {tag}: {len(c.text_boxes)} текстовых блоков, все в зоне; самый низкий низ текста y={max(ys):.0f}")


# =====================================================================  декор
def leaf(c, cx, cy, L, w, ang, col, alpha=255):
    a = math.radians(ang)
    ux, uy = math.cos(a), math.sin(a)
    nx, ny = -uy, ux
    pl, pr = [], []
    n = 16
    for i in range(n + 1):
        t = i / n
        hw = w / 2 * math.sin(math.pi * t) ** 0.9
        px, py = cx + ux * (t - 0.5) * L, cy + uy * (t - 0.5) * L
        pl.append((px + nx * hw, py + ny * hw))
        pr.append((px - nx * hw, py - ny * hw))
    c.poly(pl + pr[::-1], col, alpha=alpha)
    c.line([(cx - ux * L * 0.45, cy - uy * L * 0.45), (cx + ux * L * 0.42, cy + uy * L * 0.42)], mix(col, (255, 255, 255), 0.35),
           width=max(1.5, w * 0.06), alpha=min(alpha, 160))


def petal(c, cx, cy, L, w, ang, col, alpha=255, edge=None):
    """Лепесток: эллипс длиной L и шириной w, повёрнутый на ang (градусы), центр (cx, cy)."""
    a = math.radians(ang)
    ca, sa = math.cos(a), math.sin(a)
    pts = []
    for i in range(36):
        t = 2 * math.pi * i / 36
        x, y = L / 2 * math.cos(t), w / 2 * math.sin(t)
        pts.append((cx + x * ca - y * sa, cy + x * sa + y * ca))
    c.poly(pts, col, alpha=alpha)
    if edge:
        c.line(pts[27:36] + pts[0:10], edge, width=max(1.5, w * 0.035), alpha=120)


def rose(c, cx, cy, r, col, seed=0):
    """Роза из трёх колец лепестков и тёмной «чашечки» в центре."""
    rnd = random.Random(seed)
    dark = mix(col, (150, 36, 66), 0.45)
    light = mix(col, WHITE, 0.45)
    rot = rnd.uniform(0, 60)
    c.circle(cx, cy + r * 0.06, r * 0.98, fill=mix(col, dark, 0.2), alpha=90)  # мягкая тень под цветком
    for k in range(6):  # внешнее кольцо
        ang = rot + k * 60
        a = math.radians(ang)
        petal(c, cx + math.cos(a) * r * 0.46, cy + math.sin(a) * r * 0.46, r * 0.98, r * 0.8, ang + 90,
              mix(light, col, 0.35), edge=mix(col, dark, 0.3))
    for k in range(5):  # среднее
        ang = rot + 30 + k * 72
        a = math.radians(ang)
        petal(c, cx + math.cos(a) * r * 0.26, cy + math.sin(a) * r * 0.26, r * 0.7, r * 0.58, ang + 90,
              col, edge=dark)
    for k in range(4):  # внутреннее
        ang = rot + 10 + k * 90
        a = math.radians(ang)
        petal(c, cx + math.cos(a) * r * 0.11, cy + math.sin(a) * r * 0.11, r * 0.44, r * 0.36, ang + 90,
              mix(col, dark, 0.35), edge=dark)
    c.circle(cx, cy, r * 0.17, fill=mix(col, dark, 0.55))
    petal(c, cx + r * 0.05, cy - r * 0.02, r * 0.3, r * 0.17, rot + 35, mix(col, dark, 0.2), edge=dark)
    petal(c, cx - r * 0.06, cy + r * 0.03, r * 0.24, r * 0.13, rot - 50, mix(col, light, 0.1), edge=dark)
    c.circle(cx - r * 0.34, cy - r * 0.36, r * 0.1, fill=WHITE, alpha=60)  # блик


def bud(c, cx, cy, r, col):
    c.ellipse((cx - r * 0.6, cy - r, cx + r * 0.6, cy + r * 0.5), fill=col)
    c.poly([(cx - r * 0.7, cy + r * 0.1), (cx, cy + r * 0.9), (cx + r * 0.7, cy + r * 0.1), (cx, cy + r * 0.45)], (96, 150, 96))


def blossom(c, cx, cy, r, col=(255, 255, 255), center=(246, 206, 90)):
    for k in range(5):
        a = math.radians(k * 72 - 90)
        c.circle(cx + math.cos(a) * r * 0.55, cy + math.sin(a) * r * 0.55, r * 0.5, fill=col)
    c.circle(cx, cy, r * 0.28, fill=center)


def rose_garland(c, y, flip=False, seed=1):
    """Гирлянда из роз сверху/снизу — как на FB-исходнике 0928-GE01 (белый фон, крупные розовые розы)."""
    rnd = random.Random(seed)
    s = -1 if flip else 1
    greens = [(116, 164, 110), (138, 182, 122), (96, 140, 98), (160, 196, 142)]
    pinks = [(244, 170, 178), (238, 150, 162), (248, 190, 196), (236, 136, 152)]
    # листья-веер
    for i in range(46):
        x = rnd.uniform(-20, W + 20)
        yy = y + s * rnd.uniform(-40, 70)
        ang = rnd.uniform(0, 360)
        leaf(c, x, yy, rnd.uniform(70, 120), rnd.uniform(24, 38), ang, rnd.choice(greens), alpha=235)
    # мелкие белые цветочки
    for i in range(12):
        blossom(c, rnd.uniform(20, W - 20), y + s * rnd.uniform(-30, 80), rnd.uniform(13, 19))
    # розы: крупные по углам и в центре, средние между
    spots = [(40, 0, 118), (230, 30, 84), (420, -10, 70), (560, 20, 96), (720, -6, 74), (890, 26, 88), (1060, -4, 120)]
    for k, (x, dy, r) in enumerate(spots):
        rose(c, x + rnd.uniform(-12, 12), y + s * dy, r, pinks[k % len(pinks)], seed=seed * 10 + k)
    for x in (140, 330, 650, 800, 990):
        bud(c, x + rnd.uniform(-10, 10), y + s * rnd.uniform(60, 100), rnd.uniform(16, 22), rnd.choice(pinks))


def de_flag(c, x, y, w=150, h=96):
    """Флаг Германии (был на FB-исходнике 0928-GE01 — оставляем по правилу владельца 29.09)."""
    c.shadow((x, y, x + w, y + h), r=10, alpha=60, blur=8, off=(0, 5))
    lay_cols = [(22, 22, 22), (221, 0, 0), (255, 206, 0)]
    for i, col in enumerate(lay_cols):
        c.rect((x, y + i * h / 3, x + w, y + (i + 1) * h / 3 + (0.5 if i < 2 else 0)), fill=col)
    c.rect((x, y, x + w, y + h), outline=(210, 210, 210), width=2, r=4)


def cross(c, cx, cy, r, col, width=26):
    c.line([(cx - r, cy - r), (cx + r, cy + r)], col, width=width)
    c.line([(cx - r, cy + r), (cx + r, cy - r)], col, width=width)


def check(c, cx, cy, r, col, width=26):
    c.line([(cx - r, cy + r * 0.05), (cx - r * 0.3, cy + r * 0.72), (cx + r, cy - r * 0.62)], col, width=width)


# =====================================================================  креативы
CTA = "Mehr erfahren"


def cr_a():
    """A · перенос FB-хука 0928-GE01 в вертикаль: белый фон, розы сверху и снизу, флаг, крупный вопрос, красная кнопка."""
    c = V((255, 253, 250))
    rose_garland(c, 70, seed=3)
    rose_garland(c, 1830, flip=True, seed=7)
    de_flag(c, 846, 262, w=150, h=96)
    # заголовок — сжатый жирный капс, как у рабочих кредитных крео владельца (RO/PT/AT)
    lines = ["KREDIT IM", "RUHESTAND:"]
    size = c.fit(lines, "anton", 210, 820)
    cx = 485
    y = c.lines_center(lines, "anton", size, cx, 450, INK, gap=1.08)
    red = (214, 38, 52)
    sub = [[("Welche", INK)], [("Möglichkeiten", INK)], [("gibt es ", INK), ("ab 60?", red)]]
    y = c.lines_center(sub, "mxb", 96, cx, y + 90, INK, gap=1.18)
    c.button(CTA, cx, y + 170, size=62, fill=red, h=132)
    assert_safe(c, "a")
    c.save("a.png")


def cr_b():
    """B · «как считает банк»: калькулятор без цифр — три множителя и «? €», ничего не обещает."""
    navy0, navy1 = (13, 27, 66), (28, 52, 118)
    yellow = (255, 200, 61)
    c = V(navy0)
    c.vgrad((0, 0, W, H), navy0, navy1)
    c.glow(900, 360, 300, (70, 110, 210), alpha=90)
    c.glow(140, 1600, 360, (60, 90, 190), alpha=80)
    cx = 485
    # кикер
    kick = "3 Zahlen entscheiden"
    kw = c.tw(kick, "mxb", 42)
    c.rect((cx - kw / 2 - 30, 188, cx + kw / 2 + 30, 258), fill=yellow, r=35)
    c.text((cx, 223 + c.cap("mxb", 42)[1] / 2), kick, "mxb", 42, navy0, anchor="ms")
    # заголовок «KREDIT MIT / RENTE 2026», год в жёлтой плашке
    size = c.fit(["KREDIT MIT", "RENTE 2026"], "anton", 150, 800)
    capH = c.cap("anton", size)[1]
    y1 = 300 + capH
    c.text((cx, y1), "KREDIT MIT", "anton", size, WHITE, anchor="ms")
    y2 = y1 + size * 1.08
    f = c.font("anton", size)
    wr, w2 = f.getlength("RENTE ") / K, f.getlength("2026") / K
    x = cx - (wr + w2) / 2
    c.rect((x + wr - 18, y2 - capH - 20, x + wr + w2 + 18, y2 + 22), fill=yellow, r=18)
    c.text((x, y2), "RENTE ", "anton", size, WHITE, anchor="ls")
    c.text((x + wr, y2), "2026", "anton", size, navy0, anchor="ls")
    y = c.lines_center(["Welche Summe", "ist realistisch?"], "mxb", 68, cx, y2 + 52, WHITE, gap=1.18)
    # карточка «So rechnet die Bank»
    top = y + 44
    box = (80, top, 900, top + 522)
    c.shadow(box, r=40, alpha=120, blur=26, off=(0, 18))
    c.rect(box, fill=WHITE, r=40)
    x0, x1 = box[0] + 40, box[2] - 40
    ix, iy = x0, top + 32
    c.rect((ix, iy, ix + 52, iy + 66), fill=navy1, r=10)
    c.rect((ix + 8, iy + 8, ix + 44, iy + 23), fill=(190, 214, 255), r=4)
    for r_ in range(3):
        for k_ in range(3):
            c.rect((ix + 8 + k_ * 13, iy + 30 + r_ * 11.5, ix + 17 + k_ * 13, iy + 37 + r_ * 11.5), fill=WHITE, r=2)
    c.text((ix + 76, iy + 33 + c.cap("mxb", 44)[1] / 2), "So rechnet die Bank", "mxb", 44, navy0, anchor="ls")
    rows = [("Netto-Rente", "? €"), ("Laufzeit", "? Jahre"), ("Alter bei der letzten Rate", "?")]
    ry = top + 124
    for lab, val in rows:
        c.text((x0, ry + 31 + c.cap("mb", 34)[1] / 2), lab, "mb", 34, (70, 78, 98), anchor="ls")
        vw = max(140, c.tw(val, "mxb", 38) + 48)
        c.rect((x1 - vw, ry, x1, ry + 62), fill=(240, 244, 252), r=16, outline=(200, 210, 230), width=2)
        c.text((x1 - vw / 2, ry + 31 + c.cap("mxb", 38)[1] / 2), val, "mxb", 38, navy1, anchor="ms")
        c.line([(x0, ry + 80), (x1, ry + 80)], (230, 234, 242), width=2)
        ry += 92
    rb = (x0 - 12, ry + 4, x1 + 12, ry + 106)
    c.rect(rb, fill=(255, 241, 204), r=22, outline=(245, 184, 60), width=3)
    c.text((rb[0] + 28, (rb[1] + rb[3]) / 2 + c.cap("mxb", 40)[1] / 2), "Realistische Summe", "mxb", 40, (110, 64, 0), anchor="ls")
    c.text((rb[2] - 28, (rb[1] + rb[3]) / 2 + c.cap("anton", 66)[1] / 2), "? €", "anton", 66, (214, 38, 52), anchor="rs")
    c.button(CTA, cx, box[3] + 86, size=56, fill=yellow, color=navy0, h=116)
    assert_safe(c, "b")
    c.save("b.png")


def cr_c():
    """C · квиз в стиле опроса TikTok: вопрос из FB-заголовка «Worauf kommt es … wirklich an?» + три варианта-кнопки."""
    bg0, bg1 = (255, 222, 89), (255, 196, 60)
    c = V(bg0)
    c.vgrad((0, 0, W, H), bg0, bg1)
    for i in range(10):  # лёгкие круги-конфетти вне текстовой зоны
        rnd = random.Random(40 + i)
        c.circle(rnd.uniform(930, 1060), rnd.uniform(200, 1800), rnd.uniform(10, 26), fill=WHITE, alpha=110)
    cx = 485
    # тема крупно в первой строке: чёрная лента «QUIZ | KREDIT MIT RENTE 2026»
    band = (80, 188, 900, 300)
    c.rect(band, fill=INK, r=26)
    chip = (band[0] + 18, band[1] + 18, band[0] + 198, band[3] - 18)
    c.rect(chip, fill=bg0, r=18)
    c.text(((chip[0] + chip[2]) / 2, (chip[1] + chip[3]) / 2 + c.cap("mblack", 44)[1] / 2), "QUIZ", "mblack", 44, INK, anchor="ms")
    ts = c.fit(["KREDIT MIT RENTE 2026"], "anton", 76, band[2] - chip[2] - 40)
    c.text((chip[2] + 22, (band[1] + band[3]) / 2 + c.cap("anton", ts)[1] / 2), "KREDIT MIT RENTE 2026", "anton", ts, WHITE, anchor="ls")
    q = ["Worauf schaut", "die Bank", "zuerst?"]
    size = c.fit(q, "anton", 156, 820)
    y = c.lines_center(q, "anton", size, cx, 346, INK, gap=1.06)
    opts = [("A", "Das Alter"), ("B", "Die Höhe der Rente"), ("C", "Die Laufzeit")]
    oy = y + 64
    for letter, t in opts:
        box = (80, oy, 900, oy + 120)
        c.rect((box[0] + 8, box[1] + 10, box[2] + 8, box[3] + 10), fill=INK, r=34)
        c.rect(box, fill=WHITE, r=34, outline=INK, width=5)
        c.circle(box[0] + 76, (box[1] + box[3]) / 2, 42, fill=INK)
        c.text((box[0] + 76, (box[1] + box[3]) / 2 + c.cap("mblack", 46)[1] / 2), letter, "mblack", 46, bg0, anchor="ms")
        c.text((box[0] + 146, (box[1] + box[3]) / 2 + c.cap("mxb", 52)[1] / 2), t, "mxb", 52, INK, anchor="ls")
        oy += 146
    c.lines_center(["Die Antwort überrascht viele."], "mb", 46, cx, oy + 8, INK)
    c.button(CTA, cx, oy + 128, size=56, fill=INK, color=WHITE, h=116)
    assert_safe(c, "c")
    c.save("c.png")


def cr_d():
    """D · сравнение «Mythos / Fakt»: хук «Kein Gesetz verbietet einen Kredit mit 70» (FB CTR 8.5 %) в вертикали."""
    bg = (247, 244, 238)
    c = V(bg)
    # декор в нижней трети (зона подписи TikTok — без текста): мягкие волны
    for i, (yy, col, a) in enumerate(((1640, (222, 232, 246), 255), (1730, (205, 220, 242), 255), (1820, (186, 206, 236), 255))):
        pts = [(x, yy + 36 * math.sin(x / 170 + i)) for x in range(0, W + 21, 20)] + [(W, H), (0, H)]
        c.poly(pts, col, alpha=a)
    navy = (18, 36, 84)
    red, redbg = (206, 40, 48), (253, 226, 224)
    green, greenbg = (22, 132, 76), (220, 243, 228)
    cx = 485
    size = c.fit(["KREDIT MIT RENTE 2026"], "anton", 110, 820)
    c.lines_center(["KREDIT MIT RENTE 2026"], "anton", size, cx, 196, navy)
    # МИФ
    m = (80, 350, 900, 700)
    c.shadow(m, r=34, alpha=45, blur=16, off=(0, 10))
    c.rect(m, fill=redbg, r=34)
    c.rect((m[0] + 40, m[1] + 38, m[0] + 290, m[1] + 108), fill=red, r=35)
    c.text((m[0] + 165, m[1] + 73 + c.cap("mblack", 40)[1] / 2), "MYTHOS", "mblack", 40, WHITE, anchor="ms")
    cross(c, m[2] - 90, m[1] + 74, 30, red, width=16)
    ms = c.fit(["Mit 70 gibt es", "keinen Kredit mehr."], "mxb", 70, 740)
    c.lines_left(["Mit 70 gibt es", "keinen Kredit mehr."], "mxb", ms, m[0] + 40, m[1] + 150, (90, 30, 34), gap=1.2)
    # стрелка вниз
    ax, ay = 490, 712
    c.poly([(ax - 46, ay), (ax + 46, ay), (ax, ay + 50)], navy)
    # ФАКТ
    f = (80, 772, 900, 1236)
    c.shadow(f, r=34, alpha=55, blur=18, off=(0, 12))
    c.rect(f, fill=greenbg, r=34, outline=green, width=5)
    c.rect((f[0] + 40, f[1] + 38, f[0] + 230, f[1] + 108), fill=green, r=35)
    c.text((f[0] + 135, f[1] + 73 + c.cap("mblack", 40)[1] / 2), "FAKT", "mblack", 40, WHITE, anchor="ms")
    check(c, f[2] - 92, f[1] + 74, 30, green, width=16)
    fs = c.fit(["Kein Gesetz verbietet", "einen Kredit mit 70."], "mblack", 66, 740)
    yb = c.lines_left(["Kein Gesetz verbietet", "einen Kredit mit 70."], "mblack", fs, f[0] + 40, f[1] + 150, (14, 70, 40), gap=1.2)
    es = c.fit(["Entscheidend ist das Alter", "bei der letzten Rate."], "mb", 46, 740)
    c.lines_left(["Entscheidend ist das Alter", "bei der letzten Rate."], "mb", es, f[0] + 40, yb + 60, (40, 60, 50), gap=1.25)
    qs = c.fit(["Was heißt das für die Summe?"], "mxb", 54, 800)
    c.lines_center([[("Was heißt das ", navy), ("für die Summe?", red)]], "mxb", qs, cx, 1278, navy)
    c.button(CTA, cx, 1400, size=56, fill=navy, color=WHITE, h=118)
    assert_safe(c, "d")
    c.save("d.png")


BASIS_NOTE = ("Что стояло в TikTok на этой статье 27–28.09: 3 адгруппы (vb-AlexZLoansDE-tg_7-tk-intl-a-0927-GE01, "
              "…-tk-de-a-0927-GE03, …-tk-de-a-0927-GE01), 6 444 показа, 24 клика, CTR 0.37 % при медиане TT кабинета 1.42 %, "
              "hook2s 13.4 %, hook6s 2.8 %, vcr 1.1 %, $6.67 → $0.56, 1 лид. Превью TT-объявлений в кабинете нет; по карточкам панели "
              "там стояли квадратные статики 1:1 (рамки O60 про пенсию в intl-GE01 — лучшая из трёх, CTR 0.55 %; крео «кредитка на 5 000» "
              "и «три рассрочки» в de-GE03/GE01 — CTR 0.24 % и 0.22 %). ")

CREATIVES = [
    {
        "letter": "a",
        "file": "cr/de_tt/a.png",
        "concept": "Перенос FB-хука в вертикаль 9:16: белый фон, крупные розовые розы сверху и снизу, флаг Германии справа вверху (как на исходнике), сжатый жирный капс «KREDIT IM RUHESTAND:» на пол-экрана, вопрос «Welche Möglichkeiten gibt es ab 60?» («ab 60?» красным), красная кнопка «Mehr erfahren →».",
        "text": "KREDIT IM RUHESTAND: · Welche Möglichkeiten gibt es ab 60? · [Mehr erfahren →]",
        "caption": "Kredit im Ruhestand: Welche Möglichkeiten gibt es ab 60? Worauf die Bank schaut – im Artikel.",
        "cta": "Learn more / Mehr erfahren (на картинке: «Mehr erfahren →»)",
        "basis": "FB этой же статьи, РК vb-AlexZLoansDE-tg_7-fb-de-a-0928-GE01-p (27–29.09): 116 показов, 10 кликов, CTR 8.6 %, 4 лида, $4.01 → $3.12; лучшее объявление — именно этот макет (розы, флаг, «Kredit im Ruhestand: Welche Möglichkeiten gibt es ab 60?», красная кнопка): 102 показа, 7 кликов, CTR 6.9 %, 2 лида. Текст и визуал перенесены без изменений; меняется только формат (1:1 → 9:16) и размер шрифта — заголовок занимает ~40 % кадра, как на TT-победителях кредитов кабинета (RO пенсионеры vb-AlexZLoansRO-tg_2-tk-ro-a-0925-GE01: CTR 2.72 %, hook2s 68.8 %; ES vb-alexzloansSP-tg1_auto-tk-es-a-0814-GE01: CTR 2.31 %, hook2s 28.4 %), у которых в РК стояли крео владельца со сжатым жирным капсом на весь кадр. Какое именно объявление в тех РК дало CTR — в кабинете не видно (превью TT нет). Хуки FB и TT между собой не сравниваю. " + BASIS_NOTE,
    },
    {
        "letter": "b",
        "file": "cr/de_tt/b.png",
        "concept": "«Как считает банк» — калькулятор без цифр: тёмно-синий фон, кикер «3 Zahlen entscheiden», «KREDIT MIT RENTE 2026» (год в жёлтой плашке), «Welche Summe ist realistisch?», белая карточка «So rechnet die Bank» с тремя полями (Netto-Rente ? € · Laufzeit ? Jahre · Alter bei der letzten Rate ?) и итогом «Realistische Summe ? €», жёлтая кнопка «Mehr erfahren →». Ни одной суммы, ставки или обещания — только вопросительные знаки.",
        "text": "3 Zahlen entscheiden · KREDIT MIT RENTE 2026 · Welche Summe ist realistisch? · So rechnet die Bank · Netto-Rente ? € · Laufzeit ? Jahre · Alter bei der letzten Rate ? · Realistische Summe ? € · [Mehr erfahren →]",
        "caption": "Kredit mit Rente 2026: Drei Zahlen entscheiden, welche Summe realistisch ist.",
        "cta": "Learn more / Mehr erfahren (на картинке: «Mehr erfahren →»)",
        "basis": "Заголовок статьи = вопрос о сумме («Welche Summe ist realistisch…») и правило плейбука владельца для кредитов 60+ «вопрос о сумме, год в заголовке»; поля калькулятора — те три фактора, которые разбирает статья (Rente как доход, Laufzeit, возраст на последнем платеже). Формат «выбор/поля ввода» — приём владельца «множество вариаций выбора, как кнопки». На TT у этой статьи такого крео не было; на FB вопрос «Welche Summe ist realistisch?» стоял в наборе intl (vb-AlexZLoansDE-tg_7-fb-intl-a-0927-GE01-p, CTR 8.5 % на весь набор из 4, по объявлению не разделить). Доказанного крео с этим визуалом нет — гипотеза. " + BASIS_NOTE,
    },
    {
        "letter": "c",
        "file": "cr/de_tt/c.png",
        "concept": "Квиз в стиле опроса TikTok: жёлтый фон, чёрная лента «QUIZ | KREDIT MIT RENTE 2026» (тема читается первой), огромный вопрос «Worauf schaut die Bank zuerst?», три белые кнопки-варианта A «Das Alter» · B «Die Höhe der Rente» · C «Die Laufzeit», «Die Antwort überrascht viele.», чёрная кнопка «Mehr erfahren →». Вопрос о банке, не о зрителе.",
        "text": "QUIZ · KREDIT MIT RENTE 2026 · Worauf schaut die Bank zuerst? · A Das Alter · B Die Höhe der Rente · C Die Laufzeit · Die Antwort überrascht viele. · [Mehr erfahren →]",
        "caption": "Worauf schaut die Bank bei einem Kredit mit Rente zuerst? Die Antwort überrascht viele.",
        "cta": "Learn more / Mehr erfahren (на картинке: «Mehr erfahren →»)",
        "basis": "Вопрос взят из заголовка FB-объявлений лучшей FB-РК этой статьи (vb-AlexZLoansDE-tg_7-fb-de-a-0928-GE01-p, CTR 8.6 %): «Kredit ab 60: Worauf kommt es im Ruhestand wirklich an?» и из заголовка статьи («…worauf schaut die Bank?»). Интерактивность «вариантов-кнопок» — приём владельца для выбора (сетки H у товарки: LT тепловые насосы, 4 кнопки площади). На TT у этой статьи стояли только плоские карточки — hook2s 9–17 %; квиз даёт повод задержаться на кадре. Доказанного крео с этим визуалом нет — гипотеза. " + BASIS_NOTE,
    },
    {
        "letter": "d",
        "file": "cr/de_tt/d.png",
        "concept": "Сравнение «Mythos / Fakt»: светлый фон, «KREDIT MIT RENTE 2026», красная карточка MYTHOS «Mit 70 gibt es keinen Kredit mehr.» (зачёркнуто, крест), стрелка вниз, зелёная карточка FAKT «Kein Gesetz verbietet einen Kredit mit 70. Entscheidend ist das Alter bei der letzten Rate.» (галочка), «Was heißt das für die Summe?», тёмно-синяя кнопка «Mehr erfahren →».",
        "text": "KREDIT MIT RENTE 2026 · MYTHOS: Mit 70 gibt es keinen Kredit mehr. · FAKT: Kein Gesetz verbietet einen Kredit mit 70. Entscheidend ist das Alter bei der letzten Rate. · Was heißt das für die Summe? · [Mehr erfahren →]",
        "caption": "Kein Gesetz verbietet einen Kredit mit 70. Was wirklich zählt – im Artikel.",
        "cta": "Learn more / Mehr erfahren (на картинке: «Mehr erfahren →»)",
        "basis": "Хук «закон не запрещает кредит в 70» — самый кликабельный DE-кредитный хук на FB по тратам: объявление с «Kein Gesetz verbietet einen Kredit mit 70. Warum sagen Banken trotzdem so oft Nein?» в vb-AlexZLoansDE-tg_5-fb-de-a-0927-GE01-p — 106 показов, 9 кликов, CTR 8.5 %, $3.73 → $3.96, 2 лида (стояло на статье «Konto im Minus», не на этой); тот же смысл в тексте FB intl-РК этой статьи («…obwohl es keine gesetzliche Altersgrenze gibt», набор CTR 8.5 %). Вторая строка факта — раздел статьи про возраст на последнем платеже. Сравнение вынесено в два крупных блока, чтобы читалось за 1–2 секунды. " + BASIS_NOTE,
    },
]


def sheet():
    """Контактный лист 4×(270×480) для проверки глазами (в scratch, не в OUT)."""
    ims = [Image.open(os.path.join(OUT, f"{l}.png")).convert("RGB").resize((540, 960)) for l in "abcd"]
    S = Image.new("RGB", (2160, 960), WHITE)
    for i, im in enumerate(ims):
        S.paste(im, (i * 540, 0))
    p = os.environ.get("SHEET", "/tmp/de_tt_sheet.jpg")
    S.save(p, quality=85)
    print("sheet", p)


if __name__ == "__main__":
    args = sys.argv[1:] or ["a", "b", "c", "d"]
    fn = {"a": cr_a, "b": cr_b, "c": cr_c, "d": cr_d}
    for a in args:
        if a in fn:
            fn[a]()
    with open(os.path.join(OUT, "creatives.json"), "w", encoding="utf-8") as fh:
        json.dump(CREATIVES, fh, ensure_ascii=False, indent=1)
    if "sheet" in args:
        sheet()
