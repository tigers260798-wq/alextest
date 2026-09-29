"""Вёрстка пакетов «Новые тесты» (NT-…-2026-09-30) целиком в Pillow (ключ OpenAI истёк 29.09). Основа — psy_lib.py из 2026-09-30_psy.

Координаты — в единицах 1080×1080, холст рисуется в K раз крупнее и уменьшается при сохранении
(сглаживание фигур). Итог — PNG 1080×1080, ≤ 400 КБ.
"""
import math
import os
from PIL import Image, ImageDraw, ImageFilter, ImageFont

OUT = "/home/user/alextest/creatives/ready/2026-09-30_packs"
W = 1080

F = {
    "sb": "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    "s": "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    "db": "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "d": "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "serb": "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
    "ser": "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
    "lserb": "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
    "lser": "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
}


def rgba(c, a=255):
    return tuple(c[:3]) + ((c[3],) if len(c) == 4 else (a,))


class C:
    def __init__(self, bg=(255, 255, 255), K=2):
        self.K = K
        self.im = Image.new("RGBA", (W * K, W * K), rgba(bg))

    # --- базовое
    def s(self, v):
        return int(round(v * self.K))

    def sb(self, box):
        return tuple(self.s(v) for v in box)

    def sp(self, pts):
        return [(self.s(x), self.s(y)) for x, y in pts]

    @property
    def d(self):
        return ImageDraw.Draw(self.im)

    def font(self, name, size):
        return ImageFont.truetype(F[name], self.s(size))

    def layer(self):
        return Image.new("RGBA", self.im.size, (0, 0, 0, 0))

    def put(self, lay, blur=0):
        if blur:
            lay = lay.filter(ImageFilter.GaussianBlur(self.s(blur)))
        self.im.alpha_composite(lay)

    # --- фигуры
    def rect(self, box, fill=None, r=0, outline=None, width=0, alpha=255):
        lay = self.layer()
        dd = ImageDraw.Draw(lay)
        f = rgba(fill, alpha) if fill is not None else None
        o = rgba(outline, alpha) if outline is not None else None
        if r:
            dd.rounded_rectangle(self.sb(box), self.s(r), fill=f, outline=o, width=self.s(width) if width else 0)
        else:
            dd.rectangle(self.sb(box), fill=f, outline=o, width=self.s(width) if width else 0)
        self.put(lay)

    def ellipse(self, box, fill=None, outline=None, width=0, alpha=255):
        lay = self.layer()
        ImageDraw.Draw(lay).ellipse(self.sb(box), fill=rgba(fill, alpha) if fill else None,
                                    outline=rgba(outline, alpha) if outline else None, width=self.s(width) if width else 0)
        self.put(lay)

    def poly(self, pts, fill, alpha=255):
        lay = self.layer()
        ImageDraw.Draw(lay).polygon(self.sp(pts), fill=rgba(fill, alpha))
        self.put(lay)

    def line(self, pts, fill, width=2, alpha=255, joint="curve"):
        lay = self.layer()
        ImageDraw.Draw(lay).line(self.sp(pts), fill=rgba(fill, alpha), width=self.s(width), joint=joint)
        self.put(lay)

    def arc(self, box, start, end, fill, width=2, alpha=255):
        lay = self.layer()
        ImageDraw.Draw(lay).arc(self.sb(box), start, end, fill=rgba(fill, alpha), width=self.s(width))
        self.put(lay)

    def shadow(self, box, r=24, alpha=90, blur=16, off=(0, 8), color=(0, 0, 0)):
        lay = self.layer()
        x0, y0, x1, y1 = box
        ImageDraw.Draw(lay).rounded_rectangle(self.sb((x0 + off[0], y0 + off[1], x1 + off[0], y1 + off[1])), self.s(r), fill=rgba(color, alpha))
        self.put(lay, blur=blur)

    def card(self, box, fill=(255, 255, 255), r=28, sh_alpha=90, blur=18, off=(0, 10), outline=None, width=0):
        self.shadow(box, r=r, alpha=sh_alpha, blur=blur, off=off)
        self.rect(box, fill=fill, r=r, outline=outline, width=width)

    def glow(self, box, color, alpha=200, blur=40, ellipse=True, r=0):
        lay = Image.new("RGBA", self.im.size, tuple(color[:3]) + (0,))
        dd = ImageDraw.Draw(lay)
        if ellipse:
            dd.ellipse(self.sb(box), fill=rgba(color, alpha))
        else:
            dd.rounded_rectangle(self.sb(box), self.s(r), fill=rgba(color, alpha))
        self.put(lay, blur=blur)

    def vgrad(self, box, c0, c1):
        x0, y0, x1, y1 = self.sb(box)
        lay = self.layer()
        dd = ImageDraw.Draw(lay)
        for y in range(y0, y1):
            t = (y - y0) / max(1, y1 - y0 - 1)
            c = tuple(int(c0[i] + (c1[i] - c0[i]) * t) for i in range(3))
            dd.line([(x0, y), (x1 - 1, y)], fill=c + (255,))
        self.put(lay)

    def hgrad(self, box, stops):
        """stops: список цветов, равномерно по ширине."""
        x0, y0, x1, y1 = self.sb(box)
        lay = self.layer()
        dd = ImageDraw.Draw(lay)
        n = len(stops) - 1
        for x in range(x0, x1):
            t = (x - x0) / max(1, x1 - x0 - 1) * n
            i = min(int(t), n - 1)
            f = t - i
            c = tuple(int(stops[i][k] + (stops[i + 1][k] - stops[i][k]) * f) for k in range(3))
            dd.line([(x, y0), (x, y1 - 1)], fill=c + (255,))
        self.put(lay)

    # --- текст
    def tw(self, text, fnt):
        b = self.d.textbbox((0, 0), text, font=fnt)
        return (b[2] - b[0]) / self.K, (b[3] - b[1]) / self.K

    def wrap(self, text, fnt, max_w):
        lines = []
        for para in text.split("\n"):
            cur = ""
            for w_ in para.split(" "):
                t = (cur + " " + w_).strip()
                if self.tw(t, fnt)[0] <= max_w:
                    cur = t
                else:
                    if cur:
                        lines.append(cur)
                    cur = w_
            lines.append(cur)
        return lines

    def fit(self, text, name, max_w, max_lines, start, min_size=18):
        size = start
        while size > min_size:
            fnt = self.font(name, size)
            ls = self.wrap(text, fnt, max_w)
            if len(ls) <= max_lines and all(self.tw(l, fnt)[0] <= max_w for l in ls):
                return size
            size -= 1
        return min_size

    def text(self, xy, text, name, size, fill, anchor="la", stroke=0, stroke_fill=None, alpha=255):
        lay = self.layer()
        ImageDraw.Draw(lay).text(self.sp([xy])[0], text, font=self.font(name, size), fill=rgba(fill, alpha), anchor=anchor,
                                 stroke_width=self.s(stroke), stroke_fill=rgba(stroke_fill) if stroke_fill else None)
        self.put(lay)

    def block(self, text, name, size, y, max_w, fill, cx=W / 2, align="center", x=None, gap=1.16, max_lines=None, highlight=None, hl_pad=8):
        """Текст с переносом; возвращает нижний y (в единицах 1080)."""
        if max_lines:
            size = self.fit(text, name, max_w, max_lines, size)
        fnt = self.font(name, size)
        lines = self.wrap(text, fnt, max_w)
        asc, desc = fnt.getmetrics()
        lh = (asc + desc) / self.K * gap
        for ln in lines:
            w_, _ = self.tw(ln, fnt)
            xx = cx - w_ / 2 if align == "center" else x
            if highlight:
                bb = self.d.textbbox(self.sp([(xx, y)])[0], ln, font=fnt)
                self.rect((bb[0] / self.K - hl_pad, bb[1] / self.K - hl_pad * 0.6, bb[2] / self.K + hl_pad, bb[3] / self.K + hl_pad * 0.8), fill=highlight, r=6)
            self.text((xx, y), ln, name, size, fill)
            y += lh
        return y

    def button(self, label, cx, cy, name="sb", size=40, fill=(229, 57, 53), color=(255, 255, 255), padx=56, pady=22, r=None, arrow=True, shadow=True, outline=None):
        t = label + ("  →" if arrow else "")
        fnt = self.font(name, size)
        w_, _ = self.tw(t, fnt)
        asc, desc = fnt.getmetrics()
        h_ = (asc + desc) / self.K
        bw, bh = w_ + 2 * padx, h_ + 2 * pady
        box = (cx - bw / 2, cy - bh / 2, cx + bw / 2, cy + bh / 2)
        rr = bh / 2 if r is None else r
        if shadow:
            self.shadow(box, r=rr, alpha=110, blur=8, off=(0, 6))
        self.rect(box, fill=fill, r=rr, outline=outline, width=3 if outline else 0)
        self.text((cx, cy), t, name, size, color, anchor="mm")
        return box

    def check(self, x, y, size, color, width=6):
        self.line([(x, y + size * 0.5), (x + size * 0.38, y + size * 0.88), (x + size, y + size * 0.1)], color, width)

    # --- сохранение
    def save(self, name):
        path = os.path.join(OUT, name)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        img = self.im.convert("RGB").resize((W, W), Image.LANCZOS)
        img.save(path, optimize=True)
        if os.path.getsize(path) <= 400 * 1024:
            print(name, os.path.getsize(path) // 1024, "KB", "truecolor")
            return path
        for colors in (256, 224, 192, 160, 128, 96):
            q = img.quantize(colors=colors, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.FLOYDSTEINBERG)
            q.save(path, optimize=True)
            if os.path.getsize(path) <= 400 * 1024:
                break
        print(name, os.path.getsize(path) // 1024, "KB", colors, "colors")
        return path


# --- дополнительные фигуры для пакетов NT 30.09
def leaf(c, cx, cy, L, w, ang, col, alpha=255):
    """Лист: заострённый эллипс длиной L, шириной w, угол ang в градусах (0 = вправо)."""
    a = math.radians(ang)
    ux, uy = math.cos(a), math.sin(a)
    nx, ny = -uy, ux
    pts_l, pts_r = [], []
    n = 18
    for i in range(n + 1):
        t = i / n
        hw = w / 2 * math.sin(math.pi * t) ** 0.9
        px, py = cx + ux * (t - 0.5) * L, cy + uy * (t - 0.5) * L
        pts_l.append((px + nx * hw, py + ny * hw))
        pts_r.append((px - nx * hw, py - ny * hw))
    c.poly(pts_l + pts_r[::-1], col, alpha=alpha)


def flower(c, cx, cy, r, petal, center, n=5, rot=0, alpha=255):
    for k in range(n):
        a = math.radians(rot + k * 360 / n)
        px, py = cx + math.cos(a) * r * 0.55, cy + math.sin(a) * r * 0.55
        c.ellipse((px - r * 0.52, py - r * 0.52, px + r * 0.52, py + r * 0.52), fill=petal, alpha=alpha)
    c.ellipse((cx - r * 0.3, cy - r * 0.3, cx + r * 0.3, cy + r * 0.3), fill=center, alpha=alpha)


def rotpoly(pts, cx, cy, ang):
    a = math.radians(ang)
    ca, sa = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * ca - (y - cy) * sa, cy + (x - cx) * sa + (y - cy) * ca) for x, y in pts]
